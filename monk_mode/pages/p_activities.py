from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QListWidget, QLineEdit, QPushButton
from widgets.wg_button import WgButton
import uuid

def generate_id():
    return str(uuid.uuid4())

class PActivities(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        # Etiqueta para indicar que es la página de "Actividades"
        label = QLabel("Actividades de estudio")
        label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(label)

        # Lista de actividades
        self.activities_list = QListWidget()
        layout.addWidget(self.activities_list)

        # Campo de entrada para agregar nuevas actividades
        self.activity_input = QLineEdit()
        self.activity_input.setPlaceholderText("Agregar nueva actividad...")
        layout.addWidget(self.activity_input)

        # Botón para agregar una actividad
        add_activity_button = WgButton("Agregar")
        add_activity_button.clicked.connect(self.add_activity)
        layout.addWidget(add_activity_button)

        # Botón para borrar la actividad seleccionada
        delete_activity_button = WgButton("Borrar seleccionada")
        delete_activity_button.clicked.connect(self.delete_activity)
        layout.addWidget(delete_activity_button)

        self.setLayout(layout)

    def add_activity(self):
      # Agregar la actividad a la lista con un ID
      activity_name = self.activity_input.text()
      if activity_name:
          activity_id = generate_id()
          self.activities_list.addItem(f"{activity_name} ({activity_id})")
          self.activity_input.clear()

    def get_data(self):
        """Retorna una lista de diccionarios con ID y nombre de las actividades."""
        activities = []
        for index in range(self.activities_list.count()):
            item_text = self.activities_list.item(index).text()
            # Separar el nombre y el ID
            name, activity_id = item_text.rsplit(' ', 1)
            activity_id = activity_id.strip('()')  # Remover paréntesis
            activities.append({"id": activity_id, "name": name})
        return activities

    def delete_activity(self):
        # Borrar la actividad seleccionada
        selected_item = self.activities_list.currentItem()
        if selected_item:
            self.activities_list.takeItem(self.activities_list.row(selected_item))

