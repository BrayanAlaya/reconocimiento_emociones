import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import json
import os
import unidecode  # Para quitar tildes
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class ChartRenderer(QWidget):
    def __init__(self, theme):
        super().__init__()
        self.theme = theme
        self.data = self.load_data()

        # Create the Matplotlib canvas and add it to the widget layout
        self.canvas = FigureCanvas(plt.Figure(figsize=(12, 6)))
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.canvas)

        # QLabel for displaying hover information
        self.info_label = QLabel(self)
        self.layout.addWidget(self.info_label)

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

        durations = []
        emotions = []
        valid_dates = []

        for date in dates:
            entry = self.data[date]
            if isinstance(entry, dict) and "duration" in entry and isinstance(entry["duration"], (int, float)):
                durations.append(entry["duration"])
                valid_dates.append(date)
                emotion_data = entry.get("emotions", {})

                # Calculate the total for percentages
                total_emotions = sum(emotion_data.values())
                emotion_str = ', '.join(
                    [f"{emotion}: {value / total_emotions * 100:.1f}%" for emotion, value in emotion_data.items()]
                )
                emotions.append(emotion_str if emotion_str else "Sin emoción")
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

        fig = self.canvas.figure
        fig.clear()

        ax = fig.add_subplot(1, 1, 1)
        line, = ax.plot(valid_dates, durations, color='#66cc66', marker='o', linestyle='-', markersize=8)
        
        ax.set_xticks([])
        ax.set_ylabel('Duration (minutes)')

        tolerance = 0.8  # Adjusted for a larger area of detection

        def on_hover(event):
            # Check if the mouse is within the plot area
            if event.inaxes == ax:
                for i, point in enumerate(line.get_xydata()):
                    if abs(point[0] - event.xdata) < tolerance and abs(point[1] - event.ydata) < tolerance:
                        # Update QLabel with information of the hovered point
                        self.info_label.setText(
                            f"Fecha: {valid_dates[i]} - Duración: {durations[i]} min - Emociones: {emotions[i]}"
                        )
                        return

        fig.canvas.mpl_connect("motion_notify_event", on_hover)

        fig.tight_layout()
        self.canvas.draw()
