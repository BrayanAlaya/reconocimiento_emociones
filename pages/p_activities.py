from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QListWidget, QLineEdit
from widgets.wg_button import WgButton
from utils.json_manager import load_json, update_json_section
import json
import os
import unidecode  # Para normalizar el nombre de la actividad

class PActivities(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Configuración de la interfaz
        layout = QVBoxLayout()
        label = QLabel("Actividades de estudio")
        label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(label)

        self.activities_list = QListWidget()  # Lista de actividades
        layout.addWidget(self.activities_list)

        self.activity_input = QLineEdit()  # Campo de entrada para nueva actividad
        self.activity_input.setPlaceholderText("Agregar nueva actividad...")
        layout.addWidget(self.activity_input)

        add_activity_button = WgButton("Agregar")  # Botón para agregar actividad
        add_activity_button.clicked.connect(self.add_activity)
        layout.addWidget(add_activity_button)

        delete_activity_button = WgButton("Borrar seleccionada")  # Botón para borrar actividad
        delete_activity_button.clicked.connect(self.delete_activity)
        layout.addWidget(delete_activity_button)

        self.setLayout(layout)
        self.load_activities_from_json()  # Cargar actividades desde JSON al inicializar

    def normalize_activity_name(self, activity_name):
        """Normaliza el nombre de la actividad para el uso en archivos."""
        return unidecode.unidecode(activity_name).lower()

    def add_activity(self):
        """Agrega una nueva actividad a la lista y crea el archivo JSON correspondiente."""
        activity_name = self.activity_input.text().strip()
        if activity_name:
            self.activities_list.addItem(activity_name)
            self.activity_input.clear()
            self.save_activities_to_json()
            # Crear archivo JSON en data/history si no existe
            normalized_name = self.normalize_activity_name(activity_name)
            file_path = f"data/history/{normalized_name}.json"
            if not os.path.exists(file_path):
                with open(file_path, 'w') as file:
                    json.dump({"duration": 0, "sessions": []}, file, indent=4)  # Plantilla básica

    def delete_activity(self):
        """Elimina la actividad seleccionada y borra el archivo JSON correspondiente."""
        selected_item = self.activities_list.currentItem()
        if selected_item:
            activity_name = selected_item.text()
            normalized_name = self.normalize_activity_name(activity_name)
            file_path = f"data/history/{normalized_name}.json"
            # Eliminar el archivo JSON si existe
            if os.path.exists(file_path):
                os.remove(file_path)
            # Eliminar de la lista y actualizar JSON
            self.activities_list.takeItem(self.activities_list.row(selected_item))
            self.save_activities_to_json()

    def save_activities_to_json(self):
        """Guarda las actividades actuales en un archivo JSON sin sobrescribir los otros datos."""
        data = load_json('data/user.json')
        # Obtener actividades actuales
        activities = [self.activities_list.item(i).text() for i in range(self.activities_list.count())]
        # Actualizar la sección 'activities'
        data['activities'] = activities
        # Guardar en JSON
        with open('data/user.json', 'w') as file:
            json.dump(data, file, indent=4)

    def load_activities_from_json(self):
        """Carga actividades desde el archivo JSON."""
        data = load_json('data/user.json')
        activities = data.get("activities", [])
        # Asegúrate de que activities es una lista antes de procesar
        if isinstance(activities, list):
            for activity in activities:
                self.activities_list.addItem(activity)  # Agregar cada actividad a la lista

    def get_data(self):
        """Método para obtener la lista de actividades."""
        return [self.activities_list.item(i).text() for i in range(self.activities_list.count())]  # Retornar actividades
