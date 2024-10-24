from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QSizePolicy, QSpacerItem
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from windows.estadisticas_page import EstadisticasPage
from windows.actividad_page import ActividadPage
from windows.ajustes_page import AjustesPage
from widgets.custom_button import CustomButton

# Temas
class Theme:
    LIGHT = {
        "bg_color": "white",
        "text_color": "black",
        "color": "black",
        "button_bg_color": "#f0f0f0",
        "button_border_color": "black"
    }
    DARK = {
        "bg_color": "#2e2e2e",
        "text_color": "white",
        "button_bg_color": "#4e4e4e",
        "button_border_color": "white"
    }

current_theme = Theme.LIGHT  # Tema inicial

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main")
        self.setGeometry(100, 100, 600, 400)

        main_layout = QHBoxLayout()

        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)

        self.central_widget = QStackedWidget()
        self.page_estadisticas = EstadisticasPage(self)
        self.page_actividad = ActividadPage(self)
        self.page_ajustes = AjustesPage(self)

        self.central_widget.addWidget(self.page_actividad)
        self.central_widget.addWidget(self.page_estadisticas)
        self.central_widget.addWidget(self.page_ajustes)

        main_layout.addWidget(self.central_widget)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.update_theme()  # Aplicar tema al iniciar

    def create_sidebar(self):
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout()

        # Título "Monk Mode" con fuente más grande y ajuste a varias líneas
        monk_mode_label = QLabel("Monk\nMode")
        monk_mode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        monk_mode_label.setStyleSheet("font-size: 48px; font-weight: bold;")
        monk_mode_label.setWordWrap(True)  # Permitir el ajuste de palabras

        # Agregar el QLabel al layout
        sidebar_layout.addWidget(monk_mode_label)

        # Espaciador para mejorar la separación visual
        sidebar_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        actividad_button = CustomButton("Actividad")
        actividad_button.clicked.connect(self.show_actividad)

        estadisticas_button = CustomButton("Estadísticas")
        estadisticas_button.clicked.connect(self.show_estadisticas)

        # Crear un widget horizontal para el botón de ajustes y el botón de tema
        settings_theme_widget = QWidget()
        settings_theme_layout = QHBoxLayout()

        # Botón de ajustes
        ajustes_button = CustomButton("ⓘ")
        ajustes_button.clicked.connect(self.show_ajustes)

        self.theme_button = CustomButton("☼ ⭢ ☾", self)
        self.theme_button.clicked.connect(self.toggle_theme)

        settings_theme_layout.addWidget(self.theme_button)
        settings_theme_layout.addWidget(ajustes_button)

        settings_theme_widget.setLayout(settings_theme_layout)

        # Espaciador para empujar los botones al centro
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        sidebar_layout.addItem(spacer)  # Espaciador para empujar hacia el medio
        sidebar_layout.addWidget(actividad_button)
        sidebar_layout.addWidget(estadisticas_button)
        sidebar_layout.addItem(spacer)  # Espaciador para empujar hacia el medio
        sidebar_layout.addWidget(settings_theme_widget)  # Agregar el widget de ajustes y tema

        sidebar.setLayout(sidebar_layout)
        sidebar.setMinimumWidth(100)
        sidebar.setMaximumWidth(200)
        sidebar.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)

        return sidebar







    def toggle_theme(self):
        global current_theme
        if current_theme == Theme.LIGHT:
            current_theme = Theme.DARK
            self.theme_button.setText("☾ ⭢ ☼")
        else:
            current_theme = Theme.LIGHT
            self.theme_button.setText("☼ ⭢ ☾")
        self.update_theme()  # Actualizar tema

    def show_estadisticas(self):
        self.central_widget.setCurrentWidget(self.page_estadisticas)

    def show_actividad(self):
        self.central_widget.setCurrentWidget(self.page_actividad)

    def show_ajustes(self):
        self.central_widget.setCurrentWidget(self.page_ajustes)

    def update_theme(self):
        style = f"""
            QWidget {{
                background-color: {current_theme['bg_color']};
                color: {current_theme['text_color']};
            }}
            QPushButton {{
                background-color: {current_theme['button_bg_color']};
                color: {current_theme['text_color']};
                border: 1px solid {current_theme['button_border_color']};
                padding: 5px;
            }}
        """
        self.setStyleSheet(style)
        self.central_widget.setStyleSheet(style)  # Aplicar tema a central_widget
