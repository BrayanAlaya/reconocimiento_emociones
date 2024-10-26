from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QSpinBox, QLabel
from PyQt6.QtCore import Qt
from widgets.wg_timer import WgTimer
from widgets.wg_circle_progress import WgCircleProgress
from widgets.wg_button import WgButton
import json
from datetime import datetime
from unidecode import unidecode
import os
import psutil

class PConcentration(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        # Inicializar variables
        self.remaining_seconds = 0  
        self.total_seconds = 0  
        self.start_time = None  

        # Configurar interfaz
        self.progress_circle = WgCircleProgress()
        layout.addWidget(self.progress_circle, alignment=Qt.AlignmentFlag.AlignCenter)

        self.activities = self.load_activities()

        activity_layout = QHBoxLayout()
        self.activity_label = QLabel("Selecciona una actividad:")
        self.activity_combo = QComboBox()

        if self.activities:
            for activity in self.activities:
                self.activity_combo.addItem(activity)
        else:
            self.activity_combo.addItem("No hay actividades disponibles")

        activity_layout.addWidget(self.activity_label)
        activity_layout.addWidget(self.activity_combo)
        layout.addLayout(activity_layout)

        time_layout = QHBoxLayout()
        self.time_label = QLabel("Tiempo en minutos:")
        self.time_spinner = QSpinBox()
        self.time_spinner.setRange(1, 240)

        time_layout.addWidget(self.time_label)
        time_layout.addWidget(self.time_spinner)
        layout.addLayout(time_layout)

        button_layout = QHBoxLayout()
        self.confirm_button = WgButton("Play")
        self.cancel_button = WgButton("Cancel")
        
        self.confirm_button.clicked.connect(self.confirm_activity)
        self.cancel_button.clicked.connect(self.cancel_activity)

        button_layout.addWidget(self.confirm_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.activity_running = False

    def load_activities(self):
        """Cargar las actividades desde user.json."""
        try:
            with open('data/user.json', 'r') as file:
                user_data = json.load(file)
                activities = user_data.get("activities", [])
                return list(activities.keys()) if isinstance(activities, dict) else activities
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error al cargar las actividades.")
            return []

    def cancel_activity(self):
        """Detener el temporizador y desbloquear aplicaciones."""
        if hasattr(self, 'timer_window'):
            elapsed_time = self.total_seconds - self.remaining_seconds
            self.timer_window.timer.stop()
            self.timer_window.close()
            self.finish_activity(elapsed_time)

        self.release_blocking()  # Desbloquear aplicaciones al cancelar

        self.progress_circle.set_progress(0)
        self.activity_running = False
        self.confirm_button.setEnabled(True)

    def confirm_activity(self):
        if self.activity_running:
            return

        self.enforce_blocking()  # Bloquear aplicaciones al iniciar la actividad

        activity_name = unidecode(self.activity_combo.currentText().strip().lower())
        time = self.time_spinner.value()

        self.total_seconds = time * 60
        self.remaining_seconds = self.total_seconds
        self.start_time = datetime.now()
        self.timer_window = WgTimer(self.total_seconds, activity_name)
        self.timer_window.show()

        self.activity_running = True
        self.confirm_button.setEnabled(False)

        self.timer_window.timer.timeout.connect(self.update_progress)
        self.timer_window.timer.start(1000)
        self.progress_circle.update_timer_label(self.remaining_seconds)

    def update_progress(self):
        """Actualizar el progreso del temporizador y el círculo de progreso."""
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.progress_circle.set_progress((self.total_seconds - self.remaining_seconds) / self.total_seconds * 100)
            self.progress_circle.update_timer_label(self.remaining_seconds)
        else:
            self.finish_activity(self.total_seconds)

    def finish_activity(self, elapsed_time):
        """Manejar la finalización de la actividad y desbloquear aplicaciones."""
        self.progress_circle.set_progress(100)
        self.progress_circle.update_timer_label(0)
        self.update_activity_json(elapsed_time)

        self.release_blocking()  # Desbloquear aplicaciones al finalizar la actividad

        self.activity_running = False
        self.confirm_button.setEnabled(True)

    def update_activity_json(self, elapsed_time):
        """Actualizar el archivo JSON con los datos de la actividad completada."""
        activity_name = unidecode(self.activity_combo.currentText().strip().lower())
        duration = elapsed_time // 60
        today_date = datetime.now().strftime('%Y-%m-%d')

        activity_file = os.path.join('data', 'history', f"{activity_name}.json")

        try:
            if os.path.exists(activity_file):
                with open(activity_file, 'r') as file:
                    activity_data = json.load(file)
            else:
                activity_data = {}

            # Si la actividad de hoy ya existe, sumar la duración
            if today_date in activity_data:
                previous_duration = activity_data[today_date].get("duration", 0)
                new_duration = previous_duration + duration
            else:
                new_duration = duration

            activity_data[today_date] = {
                "duration": new_duration,
                "emotions": {
                    "happy": 80,  # Valores de ejemplo, puedes reemplazarlos
                    "neutral": 70,
                    "stressed": 90
                }
            }

            with open(activity_file, 'w') as file:
                json.dump(activity_data, file, indent=4)

        except (FileNotFoundError, json.JSONDecodeError):
            print("Error al actualizar el archivo de actividad.")

    def enforce_blocking(self):
        """Bloquear aplicaciones al iniciar la actividad."""
        # Aquí puedes definir la lógica para bloquear aplicaciones según tus necesidades
        blocked_apps = self.get_blocked_apps()  # Cargar aplicaciones bloqueadas
        for app in blocked_apps:
            self.enforce_app_blocking(app)

    def release_blocking(self):
        """Desbloquear todas las aplicaciones bloqueadas."""
        blocked_apps = self.get_blocked_apps()  # Cargar aplicaciones bloqueadas
        for app in blocked_apps:
            self.release_app_blocking(app)

    def get_blocked_apps(self):
        """Obtener la lista de aplicaciones bloqueadas desde JSON."""
        try:
            with open('data/user.json', 'r') as file:
                user_data = json.load(file)
                return user_data.get("block", [])
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error al cargar las aplicaciones bloqueadas.")
            return []

    def enforce_app_blocking(self, app_name):
        """Bloquear un proceso de aplicación."""
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == app_name:
                proc.suspend()

    def release_app_blocking(self, app_name):
        """Desbloquear un proceso de aplicación."""
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == app_name:
                proc.resume()
