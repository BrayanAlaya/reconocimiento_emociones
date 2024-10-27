import json
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt6.QtCore import Qt
from utils.chart_renderer import ChartRenderer  # Asegúrate de que la ruta sea correcta

class PDashboard(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.load_user_data()  # Cargar los datos del usuario
        self.setup_ui()

    def load_user_data(self):
        """Carga los datos del usuario desde el archivo JSON."""
        with open('data/user.json', 'r') as f:
            user_data = json.load(f)
            self.activities = user_data.get('activities', [])  # Obtener la lista de actividades

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Quitar márgenes
        layout.setSpacing(10)  # Reducir el espacio entre elementos

        # Área de desplazamiento para los gráficos
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { background-color: rgba(245, 245, 245, 0.9); }")  # Fondo más opaco
        layout.addWidget(self.scroll_area)

        # Widget contenedor para gráficos
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(10, 10, 10, 10)  # Margen ligero alrededor del contenido
        self.content_widget.setLayout(self.content_layout)
        self.scroll_area.setWidget(self.content_widget)

        # Cargar gráficos en el layout de contenido
        self.load_charts()

        self.setLayout(layout)

    def load_charts(self):
        """Cargar y mostrar gráficos para cada actividad en un layout desplazable."""
        for activity in self.activities:
            # Etiqueta de cada sección temática
            theme_label = QLabel(f"Gráficos para {activity}")
            theme_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 5px;")
            self.content_layout.addWidget(theme_label)

            # Crear y renderizar el ChartRenderer para cada actividad
            renderer = ChartRenderer(activity)  # Utiliza el nombre de la actividad
            renderer.setMinimumHeight(300)  # Altura mínima para gráficos más grandes
            renderer.setStyleSheet("background-color: rgba(255, 255, 255, 0.9);")  # Fondo blanco más opaco para los gráficos
            self.content_layout.addWidget(renderer)

            # Renderizar los datos del gráfico
            renderer.render_chart()
