import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import json
import os
import unidecode  # Para quitar tildes
from PyQt6.QtWidgets import QWidget, QVBoxLayout

class ChartRenderer(QWidget):
    def __init__(self, theme):
        super().__init__()
        self.theme = theme
        self.data = self.load_data()

        # Create the Matplotlib canvas and add it to the widget layout
        self.canvas = FigureCanvas(plt.Figure(figsize=(12, 6)))  # Adjusted size for better visibility
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.canvas)
        self.render_chart()

    def load_data(self):
        """Load data from JSON based on the theme."""
        file_theme = unidecode.unidecode(self.theme).lower()  
        file_path = f"data/history/{file_theme}.json"
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return json.load(file)
        else:
            print(f"No data found for file: {file_path}")
            return {}

    def render_chart(self):
        dates = list(self.data.keys())

        # Check if there are available data
        if not dates:
            fig = self.canvas.figure
            fig.clear()

            ax = fig.add_subplot(1, 1, 1)
            ax.text(0.5, 0.5, 'Sesiones no realizadas', ha='center', va='center', fontsize=16, color='gray')
            ax.set_xticks([])
            ax.set_yticks([])
            self.canvas.draw()
            print("No data available to render charts.")
            return

        # Extract durations and emotions
        durations = []
        emotions = []
        valid_dates = []
        
        for date in dates:
            entry = self.data[date]
            if isinstance(entry, dict) and "duration" in entry and isinstance(entry["duration"], (int, float)):
                durations.append(entry["duration"])
                valid_dates.append(date)
                # Extraer las emociones y formatearlas como una cadena
                emotion_data = entry.get("emotions", {})
                emotion_str = ', '.join([f"{emotion}: {value}" for emotion, value in emotion_data.items()])
                emotions.append(emotion_str if emotion_str else "Sin emoción")  # Valor por defecto si no hay emoción
            else:
                print(f"Advertencia: El formato de los datos para la fecha '{date}' es incorrecto: {entry}")

        if not durations:
            fig = self.canvas.figure
            fig.clear()
            ax = fig.add_subplot(1, 1, 1)
            ax.text(0.5, 0.5, 'Sesiones no realizadas', ha='center', va='center', fontsize=16, color='gray')
            ax.set_xticks([])
            ax.set_yticks([])
            self.canvas.draw()
            return

        # Create the figure and plot
        fig = self.canvas.figure
        fig.clear()

        # Increase marker size for better visibility
        ax = fig.add_subplot(1, 1, 1)
        line, = ax.plot(valid_dates, durations, color='#66cc66', marker='o', linestyle='-', markersize=8)  # Increased marker size
        
        # Remove x-ticks
        ax.set_xticks([])  # No x-ticks will be shown
        ax.set_ylabel('Duration (minutes)')

        # Tooltip for hovering
        tooltip = ax.annotate(
            text='', 
            xy=(0, 0), 
            xytext=(15, -25),  # Ajustar el desplazamiento hacia abajo por defecto
            textcoords='offset points',
            bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="lightyellow"),
            arrowprops=dict(arrowstyle="->", color="black")
        )
        tooltip.set_visible(False)

        # Increase tolerance to make hover detection easier
        tolerance = 0.8  # Adjusted for a larger area of detection

        def on_hover(event):
            # Check if the mouse is over the plot
            if event.inaxes == ax:
                for i, point in enumerate(line.get_xydata()):
                    # Use the increased tolerance to make the tooltip easier to trigger
                    if abs(point[0] - event.xdata) < tolerance and abs(point[1] - event.ydata) < tolerance:
                        tooltip.xy = (point[0], point[1])
                        tooltip.set_text(f"Fecha: {valid_dates[i]}\nDuración: {durations[i]} min\nEmociones: {emotions[i]}")
                        
                        # Mover el tooltip hacia abajo si la duración es mayor a 80 minutos
                        if durations[i] > 80:
                            tooltip.xytext = (15, -40)  # Ajustar la posición hacia abajo más para duraciones altas
                        else:
                            tooltip.xytext = (15, -25)  # Posición normal
                        
                        tooltip.set_visible(True)
                        self.canvas.draw_idle()
                        return
                tooltip.set_visible(False)
                self.canvas.draw_idle()

        fig.canvas.mpl_connect("motion_notify_event", on_hover)

        fig.tight_layout()
        self.canvas.draw()
