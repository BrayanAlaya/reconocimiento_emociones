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
        """Generate and display the chart from the loaded data or show a 'no sessions' message."""
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

        # Extract durations and validate
        durations = []
        valid_dates = []
        for date in dates:
            entry = self.data[date]
            if isinstance(entry, dict) and "duration" in entry and isinstance(entry["duration"], (int, float)):
                durations.append(entry["duration"])
                valid_dates.append(date)
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

        ax = fig.add_subplot(1, 1, 1)
        ax.plot(valid_dates, durations, color='#66cc66', marker='o', linestyle='-')  # Line plot with light green color
        
        # Remove the x-ticks and y-ticks
        ax.set_xticks([])  # No x-ticks will be shown
        ax.set_yticks([])  # No y-ticks will be shown

        # Clean up the axes
        ax.set_ylabel('Duration (minutes)')

        # Remove the grid
        ax.grid(False)  # Turn off the grid

        fig.tight_layout()
        self.canvas.draw()
