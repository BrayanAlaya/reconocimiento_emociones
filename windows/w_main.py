from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QSizePolicy, QSpacerItem, QScrollArea, QPushButton
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from pages.p_dashboard import PDashboard
from pages.p_concentration import PConcentration
from windows.w_settings_dialog import WSettingsDialog

class WMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main")
        self.setGeometry(100, 100, 1000, 700)

        # Centrar la ventana
        self.center()

        # Establecer el modo claro
        self.set_light_mode()

        # Layout principal con un aside izquierdo y el contenido central
        main_layout = QHBoxLayout()

        # Crear aside izquierdo con la página de concentración y el botón de ajustes
        self.left_sidebar = self.create_left_sidebar()
        main_layout.addWidget(self.left_sidebar)

        # Crear un área de desplazamiento para la página de estadísticas
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Crear el widget central que mostrará las estadísticas
        self.central_widget = QStackedWidget()
        self.page_statistics = PDashboard(self)
        scroll_area.setWidget(self.page_statistics)  # Añadir el dashboard al scroll
        self.central_widget.addWidget(scroll_area)
        self.central_widget.setCurrentWidget(scroll_area)

        main_layout.addWidget(self.central_widget)

        # Contenedor principal
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Crear la capa de fondo (overlay) para oscurecer cuando se abren los ajustes
        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 128);")  # Semitransparente
        self.overlay.setGeometry(self.rect())
        self.overlay.setVisible(False)  # Ocultar por defecto

    def set_light_mode(self):
        """Establece el esquema de colores del modo claro."""
        self.setStyleSheet("background-color: white; color: black;")

    def center(self):
        screen_geometry = self.screen().geometry()
        window_geometry = self.geometry()
        new_x = (screen_geometry.width() - window_geometry.width()) // 2
        new_y = (screen_geometry.height() - window_geometry.height()) // 2
        self.move(new_x, new_y)

    def create_left_sidebar(self):
        left_sidebar = QWidget()
        sidebar_layout = QVBoxLayout()

        # Título "Monk Mode" en negro
        monk_mode_label = QLabel("Monk\nMode")
        monk_mode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        monk_mode_label.setStyleSheet("font-size: 48px; font-weight: bold; color: black;")
        sidebar_layout.addWidget(monk_mode_label)
        sidebar_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Página de concentración
        self.page_concentration = PConcentration(self)
        sidebar_layout.addWidget(self.page_concentration)

        # Espaciador
        sidebar_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Crear un layout para el botón de ajustes y alinearlo a la derecha
        settings_layout = QHBoxLayout()
        settings_button = QPushButton()  # Usaremos un QPushButton para el SVG
        settings_icon = QIcon("assets/settings.svg")  # Ruta al archivo SVG
        settings_button.setIcon(settings_icon)
        settings_button.setIconSize(QSize(32, 32))  # Ajusta el tamaño del ícono
        settings_button.setCursor(Qt.CursorShape.PointingHandCursor)  # Establecer el cursor a la mano

        # Cambia el estilo para asegurarte de que sea interactivo
        settings_button.setStyleSheet("background-color: transparent; border: none; cursor: pointer;")  # Sin fondo ni borde y cursor

        # Configura la acción del botón
        settings_button.clicked.connect(self.show_settings_dialog)

        # Agregar el botón de ajustes al layout y agregar espaciador para alineación
        settings_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        settings_layout.addWidget(settings_button)

        # Agregar el layout de ajustes al layout principal
        sidebar_layout.addLayout(settings_layout)

        left_sidebar.setLayout(sidebar_layout)
        left_sidebar.setMinimumWidth(300)
        left_sidebar.setMaximumWidth(300)
        left_sidebar.setStyleSheet("background-color: white;")

        return left_sidebar

    def show_settings_dialog(self):
        # Mostrar la capa oscura
        self.overlay.setVisible(True)

        dialog = WSettingsDialog(self)

        # Ocultar la capa oscura cuando el diálogo se cierra
        dialog.finished.connect(lambda: self.overlay.setVisible(False))

        dialog.exec()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Ajusta el overlay al tamaño de la ventana principal
        self.overlay.setGeometry(self.rect())
