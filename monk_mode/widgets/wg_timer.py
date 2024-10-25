from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont 

class WgTimer(QWidget):
    def __init__(self, total_seconds, activity, position="Arriba Izquierda"):
        super().__init__()
        self.setWindowTitle("Contador")

        # Ajustar la ventana para ser semitransparente y no interferir con clics
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.WindowTransparentForInput)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.5); color: white; border-radius: 10px;")
        self.setGeometry(100, 100, 200, 100)  # Tamaño inicial
    
        layout = QVBoxLayout()

        # Etiqueta con actividad
        self.activity_label = QLabel(activity)
        font = QFont("Arial", 14, QFont.Weight.Bold)
        self.activity_label.setFont(font)
        self.activity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.activity_label)

        # Etiqueta con el tiempo restante
        self.time_label = QLabel()
        self.time_label.setFont(QFont("Arial", 24))
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.time_label)

        self.setLayout(layout)

        # Guardar los segundos totales para el contador
        self.total_seconds = total_seconds
        self.remaining_seconds = total_seconds  # Para llevar el tiempo restante
        self.update_timer_label(self.total_seconds)

        # Inicializar el temporizador
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  # Iniciar el temporizador con intervalos de 1 segundo

    def update_timer(self):
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.update_timer_label(self.remaining_seconds)
        else:
            self.finish_timer()

    def set_position(self, position):
        screen_geometry = self.screen().geometry()

        if position == "Arriba Izquierda":
            self.move(0, 0)
        elif position == "Arriba Derecha":
            self.move(screen_geometry.width() - self.width(), 0)
        elif position == "Abajo Izquierda":
            self.move(0, screen_geometry.height() - self.height())
        elif position == "Abajo Derecha":
            self.move(screen_geometry.width() - self.width(), screen_geometry.height() - self.height())

    def update_timer_label(self, total_seconds):
        minutes, seconds = divmod(total_seconds, 60)
        self.time_label.setText(f"{minutes:02}:{seconds:02}")

    def finish_timer(self):
        self.time_label.setText("¡Terminado!")
        self.timer.stop()  # Detener el temporizador
        QTimer.singleShot(2000, self.close)  # Cerrar la ventana después de 2 segundos
