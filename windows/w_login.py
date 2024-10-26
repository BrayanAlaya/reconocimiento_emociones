import json
import os
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QWidget, QApplication
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtCore import Qt
from widgets.wg_button import WgButton
from windows.w_main import WMain  # Importar MainWindow

class WLogin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(600, 400)
        self.center_window()

        # Establecer el modo claro
        self.set_light_mode()

        # Crear layout principal
        main_layout = QHBoxLayout()
        left_column = QVBoxLayout()
        self.right_column = QVBoxLayout()

        # Título en la columna izquierda
        self.title_label = QLabel("MONK\nMODE", self)
        title_font = QFont("Arial", 40, QFont.Weight.Bold)
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        left_column.addStretch()  # Añadir espacio flexible
        left_column.addWidget(self.title_label)
        left_column.addStretch()  # Añadir espacio flexible

        # Cargar datos de usuario y mostrar la interfaz correspondiente
        self.user_data = self.load_user()

        if self.user_data and 'name' in self.user_data:
            self.right_column.addWidget(self.create_login_interface())
        else:
            self.right_column.addWidget(self.create_account_interface())

        # Añadir columnas al layout principal
        main_layout.addLayout(left_column, 1)
        main_layout.addLayout(self.right_column, 1)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def set_light_mode(self):
        """Establece el esquema de colores del modo claro."""
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(255, 255, 255))  # Color de fondo blanco
        palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))  # Color de texto negro
        self.setPalette(palette)

    def create_login_interface(self):
        # Mensaje de bienvenida
        self.welcome_label = QLabel(f"Bienvenido, {self.user_data['name']}", self)  # Usar 'name'
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.setWordWrap(True)
        welcome_font = QFont("Arial", 24)
        self.welcome_label.setFont(welcome_font)

        # Botón de login
        self.login_button = WgButton("Iniciar Sesión", self)
        self.login_button.clicked.connect(self.on_login)

        login_layout = QVBoxLayout()
        login_layout.addWidget(self.welcome_label)
        login_layout.addWidget(self.login_button)

        widget = QWidget()
        widget.setLayout(login_layout)
        return widget

    def create_account_interface(self):
        # Entradas para registrar cuenta
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Nombre de Usuario")
        
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Botón de registrar cuenta
        self.register_button = WgButton("Registrar Cuenta", self)
        self.register_button.clicked.connect(self.on_register)

        account_layout = QVBoxLayout()
        account_layout.addWidget(self.username_input)
        account_layout.addWidget(self.password_input)
        account_layout.addWidget(self.register_button)

        widget = QWidget()
        widget.setLayout(account_layout)
        return widget

    def load_user(self):
        path = 'data/user.json'  # Actualizar la ruta del archivo
        if os.path.exists(path):
            try:
                with open(path, 'r') as file:
                    data = json.load(file)
                    print("Datos de usuario cargados:", data)  # Verificar el contenido
                    return data
            except json.JSONDecodeError:
                print("Error: Formato JSON no válido.")
            except Exception as e:
                print(f"Error al cargar el archivo: {e}")
        else:
            self.create_default_user(path)  # Crear usuario por defecto si no existe
        return None

    def create_default_user(self, path):
        """Crea un archivo JSON por defecto."""
        default_user_data = {
            "name": "",  # Inicialmente vacío
            "password": ""  # Inicialmente vacío
        }
        with open(path, 'w') as file:
            json.dump(default_user_data, file, indent=4)

    def save_user(self, username, password):
        user_data = {"name": username, "password": password}  # Asegúrate de usar el campo 'name'
        try:
            with open('data/user.json', 'w') as file:  # Actualizar la ruta del archivo
                json.dump(user_data, file, indent=4)
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")

    def center_window(self):
        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def on_login(self):
        if self.user_data and isinstance(self.user_data, dict):
            self.main_window = WMain()  # Asegúrate de que esta línea no tenga problemas
            self.main_window.show()
            self.close()
        else:
            print("No hay usuario registrado o los datos son incorrectos.")

    def on_register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username and password:
            self.save_user(username, password)
            print("¡Cuenta creada exitosamente!")
            
            # Recargar los datos del usuario desde el archivo
            self.user_data = self.load_user()
            
            # Verifica que los datos se carguen correctamente
            if self.user_data:
                # Elimina la interfaz de registro y muestra la de inicio de sesión
                self.right_column.itemAt(0).widget().deleteLater()  # Limpiar la interfaz anterior
                self.right_column.addWidget(self.create_login_interface())
            else:
                print("Error: No se pudieron cargar los datos del usuario después de registrarse.")
        else:
            print("Por favor, completa todos los campos.")
