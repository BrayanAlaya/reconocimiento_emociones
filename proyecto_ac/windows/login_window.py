from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap, QFont, QCursor
from PyQt6.QtCore import Qt
from windows.main_window import MainWindow
from widgets.custom_button import CustomButton
from widgets.custom_notification import NotificationWidget

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 300)

        # Título
        self.title_label = QLabel("MONK MODE", self)
        title_font = QFont("Arial", 24, QFont.Weight.Bold)  # Cambia el tamaño y estilo de la fuente
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Logo
        self.logo_label = QLabel(self)
        pixmap = QPixmap("assets/logo.png")
        scaled_pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.logo_label.setPixmap(scaled_pixmap)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Contenedor para el botón de iniciar sesión y el texto "Crear Cuenta"
        auth_layout = QVBoxLayout()

        # Botón de iniciar sesión
        self.login_button = CustomButton("Iniciar Sesión", self)
        self.login_button.clicked.connect(self.on_login)
        auth_layout.addWidget(self.login_button)

        # Texto "Crear Cuenta"
        self.create_account_label = QLabel("Crear Cuenta", self)
        self.create_account_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.create_account_label.setStyleSheet("color: blue; text-decoration: underline;")
        self.create_account_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))  # Cambiar el cursor al pasar el mouse
        self.create_account_label.mousePressEvent = self.open_create_account  # Conectar el clic a una función
        auth_layout.addWidget(self.create_account_label)

        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)  # Agregar título al layout
        layout.addWidget(self.logo_label)
        layout.addLayout(auth_layout)  # Añadir el layout de autenticación

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def on_login(self):
        # Mostrar la notificación al hacer clic en el botón
        notification = NotificationWidget("¡Esto es una notificación!")
        notification.show_notification()
        
        # Mostrar la ventana principal y cerrar la ventana de login
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

    def open_create_account(self, event):
        # Aquí puedes implementar la lógica para abrir la ventana de crear cuenta
        print("Abrir ventana de crear cuenta")  # Placeholder
