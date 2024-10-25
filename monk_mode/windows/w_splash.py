import json
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QFrame, QProgressBar, QLabel, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QFont
from windows.w_login import WLogin  # Asegúrate de que esta ruta sea correcta

class WSplash(QMainWindow):
    finished = pyqtSignal()  # Señal que emitiremos cuando termine el splash

    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(600, 400)

        # Cargar ajustes de usuario desde userSettings.json
        self.user_settings = self.load_user_settings()

        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.layout = QVBoxLayout(self.centralwidget)
        self.layout.setContentsMargins(10, 10, 10, 10)

        self.dropShadowFrame = QFrame(self.centralwidget)
        # Aplicar colores desde los ajustes de usuario
        self.dropShadowFrame.setStyleSheet(f"""
            QFrame {{
                background-color: rgb(255, 255, 255);
                color: {self.user_settings["colors"]["darkerColor"]};
                border-radius: 10px;
            }}
        """)
        self.layout.addWidget(self.dropShadowFrame)

        # Layout para el contenido del splash
        self.frame_layout = QVBoxLayout(self.dropShadowFrame)

        # Añadir un espacio expansible para centrar el contenido
        self.frame_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Título de la aplicación
        self.label_title = QLabel("<strong>MONK MODE</strong>", self.dropShadowFrame)
        self.label_title.setFont(QFont("Segoe UI", 40))
        # Aplicar el color de acento (verde)
        self.label_title.setStyleSheet(f"color: {self.user_settings['colors']['accentColor']};")
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame_layout.addWidget(self.label_title)

        # Descripción de la aplicación
        self.label_description = QLabel("<strong>Haz seguimiento de tu estudio</strong>", self.dropShadowFrame)
        self.label_description.setFont(QFont("Segoe UI", 14))
        self.label_description.setStyleSheet(f"color: {self.user_settings['colors']['darkerColor']};")
        self.label_description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame_layout.addWidget(self.label_description)

        # Barra de progreso
        self.progressBar = QProgressBar(self.dropShadowFrame)
        # Aplicar colores a la barra de progreso
        self.progressBar.setStyleSheet(f"""
            QProgressBar {{
                background-color: rgb(220, 220, 220);
                color: {self.user_settings["colors"]["darkerColor"]};
                border-radius: 10px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                border-radius: 10px;
                background-color: {self.user_settings['colors']['accentColor']};
            }}
        """)
        self.progressBar.setValue(0)
        self.frame_layout.addWidget(self.progressBar)

        # Texto de carga (opcional)
        self.label_loading = QLabel("Cargando...", self.dropShadowFrame)
        self.label_loading.setFont(QFont("Segoe UI", 12))
        self.label_loading.setStyleSheet(f"color: {self.user_settings['colors']['darkerColor']};")
        self.label_loading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frame_layout.addWidget(self.label_loading)

        # Añadir otro espacio expansible para centrar el contenido
        self.frame_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Configurar temporizador para la barra de progreso
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(35)  # Actualiza cada 35 ms

        self.counter = 0

        # Conectar la señal finished a open_login_window
        self.finished.connect(self.open_login_window)

    def update_progress(self):
        self.counter += 1
        self.progressBar.setValue(self.counter)

        if self.counter >= 100:
            self.timer.stop()
            self.finished.emit()  # Emitir la señal cuando termine el splash

    def open_login_window(self):
        self.login_window = WLogin()  # Crear la ventana de login
        self.login_window.show()  # Mostrar la ventana de login
        self.close()  # Cerrar el splash

    def load_user_settings(self):
        # Cargar el archivo userSettings.json y devolver los ajustes
        try:
            with open("userSettings.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            # Si el archivo no existe, devuelve colores por defecto con tonos de verde
            return {
                "colors": {
                    "accentColor": "#4CAF50",  # Verde
                    "darkerColor": "#388E3C",  # Verde más oscuro
                    "lighterColor": "#66BB6A"  # Verde más claro
                }
            }
