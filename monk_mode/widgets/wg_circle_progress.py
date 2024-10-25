from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen, QColor

class WgCircleProgress(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedSize(200, 200)
        self.progress = 1.0  # Progreso completo inicialmente
        self.progress_color = QColor("#95d989")  # Color verde para el progreso
        
        # Etiqueta para el contador
        self.timer_label = QLabel("00:00")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        # Layout para contener el círculo y la etiqueta
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.timer_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def set_progress(self, progress):
        self.progress = progress
        self.update()  # Redibujar el círculo

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Fondo del círculo
        pen = QPen(Qt.GlobalColor.lightGray, 10)
        painter.setPen(pen)
        painter.drawEllipse(10, 10, 180, 180)

        # Círculo de progreso
        pen.setColor(self.progress_color)
        painter.setPen(pen)

        # Ángulo de progreso basado en el tiempo restante
        angle = int(360 * self.progress)
        painter.drawArc(10, 10, 180, 180, 90 * 16, -angle * 16)

    def update_timer_label(self, remaining_seconds):
        minutes, seconds = divmod(remaining_seconds, 60)
        time_string = f"{minutes:02}:{seconds:02}"
        self.timer_label.setText(time_string)
