from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QSpinBox, QLabel
from PyQt6.QtCore import Qt
from widgets.wg_timer import WgTimer
from widgets.wg_circle_progress import WgCircleProgress
from widgets.wg_button import WgButton
import json
from datetime import datetime
from unidecode import unidecode
import threading
import time
import os
import psutil
from services.FaceEmotionVideo import EmotionDetector
from pages.p_dashboard import PDashboard

class PConcentration(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.RecoFacial = EmotionDetector
        self.concentration_active = False
        # Inicializar variables
        self.remaining_seconds = 0  
        self.total_seconds = 0  
        self.start_time = None  
        
        self.chart = PDashboard()

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

        self.RecoFacial.close()
        self.chart.remove()

        self.progress_circle.set_progress(0)
        self.activity_running = False
        self.confirm_button.setEnabled(True)

    def confirm_activity(self):
        if self.activity_running:
            return
        self.RecoFacial = EmotionDetector()
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

        self.RecoFacial.start_detection()

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
        self.RecoFacial.update_activity_json(elapsed_time,self.activity_combo.currentText().strip().lower())
        self.RecoFacial.close()
        self.chart.remove()
        self.release_blocking()  # Desbloquear aplicaciones al finalizar la actividad

        self.activity_running = False
        self.confirm_button.setEnabled(True)

    def enforce_blocking(self):
        """Inicia la sesión de concentración."""
        self.concentration_active = True
        
        self.enforce_thread = threading.Thread(target=self.start_blocking, daemon=True)
        self.enforce_thread.start()
        # self.enforce_blocking()

    def get_blocked_apps(self):
        """Obtener la lista de aplicaciones bloqueadas desde JSON."""
        try:
            with open('data/user.json', 'r') as file:
                user_data = json.load(file)
                return user_data.get("block", [])
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error al cargar las aplicaciones bloqueadas.")
            return []

    def release_blocking(self):
        self.concentration_active = False
        

    def start_blocking(self):
        """Bloquea de forma persistente las aplicaciones seleccionadas mientras la concentración está activa."""
        blocked_exe_names = self.get_blocked_apps()  # Obtiene los nombres exactos de .exe bloqueados

        while self.concentration_active:
            # Revisa los procesos en ejecución
            for proc in psutil.process_iter(attrs=['pid', 'name']):
                try:
                    # Compara el nombre del proceso con la lista de nombres bloqueados
                    if proc.info['name'] and proc.info['name'].lower() in (name.lower() for name in blocked_exe_names):
                        print(f"Bloqueando {proc.info['name']} (PID: {proc.info['pid']})")
                        proc.suspend()  
                except (psutil.NoSuchProcess, psutil.AccessDenied, KeyError):
                    # Ignora los procesos que no existen o no se pueden acceder
                    pass
        
            # Espera 5 segundos antes de revisar de nuevo, manteniendo el bloqueo activo
            time.sleep(2)
   
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            try:
                # Compara el nombre del proceso con la lista de nombres bloqueados
                if proc.info['name'] and proc.info['name'].lower() in (name.lower() for name in blocked_exe_names):
                    print(f"Desbloqueando {proc.info['name']} (PID: {proc.info['pid']})")
                    proc.kill()  
            except (psutil.NoSuchProcess, psutil.AccessDenied, KeyError):
                # Ignora los procesos que no existen o no se pueden acceder
                pass