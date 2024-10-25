from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QListWidget, QLineEdit, QPushButton
from widgets.wg_button import WgButton

class PBlock(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        # Etiqueta para indicar que es la página de "Bloquear"
        label = QLabel("Aplicaciones bloqueadas")
        label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(label)

        # Lista de aplicaciones bloqueadas
        self.blocked_apps_list = QListWidget()
        layout.addWidget(self.blocked_apps_list)

        # Campo de entrada para agregar nuevas apps
        self.app_input = QLineEdit()
        self.app_input.setPlaceholderText("Agregar nueva aplicación...")
        layout.addWidget(self.app_input)

        # Botón para agregar una aplicación
        add_app_button = WgButton("Agregar")
        add_app_button.clicked.connect(self.add_app)
        layout.addWidget(add_app_button)

        # Botón para borrar la aplicación seleccionada
        delete_app_button = WgButton("Borrar seleccionada")
        delete_app_button.clicked.connect(self.delete_app)
        layout.addWidget(delete_app_button)

        self.setLayout(layout)

    def add_app(self):
        # Agregar la aplicación a la lista
        app_name = self.app_input.text()
        if app_name:
            self.blocked_apps_list.addItem(app_name)
            self.app_input.clear()

    def delete_app(self):
        # Borrar la aplicación seleccionada
        selected_item = self.blocked_apps_list.currentItem()
        if selected_item:
            self.blocked_apps_list.takeItem(self.blocked_apps_list.row(selected_item))

    def get_data(self):
        """Retorna una lista con los nombres de las aplicaciones bloqueadas en el widget."""
        blocked_apps = []
        for index in range(self.blocked_apps_list.count()):
            blocked_apps.append(self.blocked_apps_list.item(index).text())
        return blocked_apps
