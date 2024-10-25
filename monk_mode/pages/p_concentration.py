from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QSpinBox, QMessageBox, QLabel
from PyQt6.QtCore import Qt
from widgets.wg_timer import WgTimer  # Asegúrate de que la importación sea correcta
from widgets.wg_circle_progress import WgCircleProgress  # Asegúrate de que esta importación sea correcta
from widgets.wg_button import WgButton
import json

class PConcentration(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        # Inicializar remaining_seconds
        self.remaining_seconds = 0  
        self.total_seconds = 0  

        # Contenedor para el círculo de progreso
        self.progress_circle = WgCircleProgress()
        layout.addWidget(self.progress_circle, alignment=Qt.AlignmentFlag.AlignCenter)  # Centrar el círculo

        # Cargar actividades desde user.json
        self.activities = self.load_activities()

        # Selección de actividad
        activity_layout = QHBoxLayout()
        self.activity_label = QLabel("Selecciona una actividad:")
        self.activity_combo = QComboBox()
        for activity in self.activities:
            self.activity_combo.addItem(activity['name'], activity['id'])

        activity_layout.addWidget(self.activity_label)
        activity_layout.addWidget(self.activity_combo)
        layout.addLayout(activity_layout)

        # Selección de tiempo
        time_layout = QHBoxLayout()
        self.time_label = QLabel("Tiempo en minutos:")
        self.time_spinner = QSpinBox()
        self.time_spinner.setRange(1, 240)

        time_layout.addWidget(self.time_label)
        time_layout.addWidget(self.time_spinner)
        layout.addLayout(time_layout)

        # Layout para los botones
        button_layout = QHBoxLayout()
        self.confirm_button = WgButton("Play")
        self.cancel_button = WgButton("Cancel")
        
        self.confirm_button.clicked.connect(self.confirm_activity)
        self.cancel_button.clicked.connect(self.cancel_activity)  # Conectar el botón de cancelar

        button_layout.addWidget(self.confirm_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def load_activities(self):
        """Cargar las actividades desde user.json y asignar IDs."""
        try:
            with open('data/user.json', 'r') as file:
                settings = json.load(file)
                return settings.get('activities', [])  # Lista de actividades con IDs
        except FileNotFoundError:
            return []  # Lista vacía si no se encuentra el archivo
        
    def cancel_activity(self):
        # Detener el temporizador y restablecer los labels
        if hasattr(self, 'timer_window'):
            self.timer_window.timer.stop()
            self.timer_window.finish_timer()  # Actualiza la ventana del temporizador
        self.progress_circle.set_progress(0)
        self.progress_circle.update_timer_label(0)  # Restablece el label del círculo de progreso
        QMessageBox.information(self, "Actividad Cancelada", "La actividad ha sido cancelada.")

    def confirm_activity(self):
        activity = self.activity_combo.currentData()  # Usar el ID de la actividad seleccionada
        activity_name = self.activity_combo.currentText()  # Nombre de la actividad seleccionada
        time = self.time_spinner.value()

        # Iniciar la ventana de temporizador
        self.total_seconds = time * 60
        self.remaining_seconds = self.total_seconds
        self.timer_window = WgTimer(self.total_seconds, activity_name)
        self.timer_window.show()

        # Registrar la actividad en el historial
        self.log_activity(activity, activity_name, time)

        # Mostrar mensaje de inicio
        QMessageBox.information(self, "Actividad Iniciada",
                                f"Actividad: {activity_name}\nTiempo: {time} minutos",
                                QMessageBox.StandardButton.Ok)

        # Iniciar el temporizador
        self.timer_window.timer.timeout.connect(self.update_progress)
        self.timer_window.timer.start(1000)  # Iniciar temporizador cada 1 segundo

        # Actualiza el label del círculo de progreso inicialmente
        self.progress_circle.update_timer_label(self.remaining_seconds)

    def log_activity(self, activity_id, activity_name, time):
        """Registrar la actividad con ID en el historial."""
        entry = {
            "activity_id": activity_id,
            "activity_name": activity_name,
            "start": "2:00pm",  # Aquí puedes registrar el inicio real
            "end": "3:00pm",    # Registrar el final real cuando termine
            "duration": time,   # Duración en minutos
            "date": "xx-xx-xxxx"  # Fecha real de la actividad
        }

        try:
            with open('data/user.json', 'r+') as file:
                data = json.load(file)
                data["activities"].append(entry)
                file.seek(0)
                json.dump(data, file, indent=4)
        except FileNotFoundError:
            pass  # Manejar error si no existe el archivo


    def update_progress(self):
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.timer_window.update_timer_label(self.remaining_seconds)
            self.progress_circle.set_progress(self.remaining_seconds / self.total_seconds)
            self.progress_circle.update_timer_label(self.remaining_seconds)  # Actualiza el label en ProgressCircle
        else:
            self.timer_window.finish_timer()
            self.progress_circle.set_progress(0)
            self.timer_window.timer.stop()  # Detener el temporizador al finalizar

