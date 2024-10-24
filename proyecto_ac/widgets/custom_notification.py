from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer

class NotificationWidget(QWidget):
    def __init__(self, message):
        super().__init__()
        # Añadir la flag WindowStaysOnTopHint para que se sobreponga sobre cualquier ventana del sistema
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # Fondo transparente

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        # Establecer el estilo del contenedor: fondo rojo oscuro, borde redondeado, tamaño cuadrado
        self.setStyleSheet("""
            background-color: rgba(255, 0, 0, 0.8);
            color: white;
            border-radius: 20px;
            min-width: 200px;
            min-height: 100px;
            padding: 12px;
        """)

        # Crear una etiqueta de mensaje con texto grande
        message_label = QLabel(message)
        message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message_label.setStyleSheet("font-size: 18px;")  # Establecer el tamaño de la letra
        layout.addWidget(message_label)

        self.setLayout(layout)

        # Conectar el clic en la notificación para cerrarla
        self.mousePressEvent = self.close_notification

        # Crear un temporizador para cerrar la notificación después de 5 segundos (5000 ms)
        self.timer = QTimer(self)
        self.timer.setInterval(5000)  # 5000 ms = 5 segundos
        self.timer.timeout.connect(self.close_notification)
        self.timer.start()

        # Ajustar la posición de la notificación en la mitad superior
        self.set_position()

    def set_position(self):
        screen_geometry = self.screen().geometry()
        self.adjustSize()  # Ajustar el tamaño al contenido
        # Colocar la notificación en el centro de la parte superior
        x = (screen_geometry.width() - self.width()) // 2  # Centrar horizontalmente
        y = screen_geometry.height() // 10  # Posicionar en la parte superior (10% de la altura de la pantalla)
        self.move(x, y)

    def show_notification(self):
        self.show()  # Mostrar la notificación

    def close_notification(self, event=None):
        self.close()  # Cerrar la notificación al hacer clic o cuando el temporizador expire
