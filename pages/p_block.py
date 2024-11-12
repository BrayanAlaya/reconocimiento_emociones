import winreg
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QListWidget, QLineEdit, QListWidgetItem, QMessageBox
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import QTimer, QCoreApplication
import json
import psutil
import threading
import time
from widgets.wg_button import WgButton

class PBlock(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Configuración de la interfaz
        layout = QVBoxLayout()
        label = QLabel("Aplicaciones bloqueadas")
        label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(label)

        self.app_list = QListWidget()  # Lista de aplicaciones
        layout.addWidget(self.app_list)

        # Campo de búsqueda para filtrar aplicaciones
        self.search_input = QLineEdit()  
        self.search_input.setPlaceholderText("Buscar aplicación...")
        self.search_input.textChanged.connect(self.filter_apps)  # Conectar la búsqueda
        layout.addWidget(self.search_input)

        # Botón para agregar (bloquear) aplicación seleccionada
        self.block_app_button = WgButton("Bloquear seleccionada")
        self.block_app_button.clicked.connect(self.block_app)
        layout.addWidget(self.block_app_button)

        # Botón para borrar aplicación
        delete_app_button = WgButton("Borrar seleccionada")
        delete_app_button.clicked.connect(self.delete_app)
        layout.addWidget(delete_app_button)

        self.setLayout(layout)

        # Cargar aplicaciones bloqueadas desde JSON
        self.load_apps_from_json()
        self.load_running_executables()  # Listar ejecutables en ejecución

        # Atributo para verificar si la concentración está activa
        self.concentration_active = False
        self.enforce_thread = None  # Thread de aplicación de bloqueo

    def load_running_executables(self):
        """Carga todos los ejecutables actualmente en ejecución."""
        self.app_list.clear()
        blocked_apps = self.get_data()  # Obtener los bloqueados del JSON

        # Listar todos los procesos activos
        for proc in psutil.process_iter(attrs=['name']):
            try:
                exe_name = proc.name()
                item = QListWidgetItem(exe_name)

                # Marcar las aplicaciones bloqueadas
                if exe_name in blocked_apps:
                    font = QFont()
                    font.setBold(True)
                    item.setFont(font)
                    item.setBackground(QColor("#FFDDDD"))

                self.app_list.addItem(item)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    def block_app(self):
        """Bloquea la aplicación seleccionada."""
        if not self.concentration_active:  # Solo permitir si no hay concentración activa
            selected_item = self.app_list.currentItem()
            if selected_item:
                exe_name = selected_item.text()
                if exe_name not in self.get_data():  
                    item = QListWidgetItem(exe_name)
                    font = QFont()
                    font.setBold(True)
                    item.setFont(font)
                    item.setBackground(QColor("#FFDDDD"))
                    self.app_list.addItem(item)
                    self.save_apps_to_json()

    def delete_app(self):
        """Elimina la aplicación seleccionada."""
        selected_item = self.app_list.currentItem()
        if selected_item:
            self.app_list.takeItem(self.app_list.row(selected_item))
            self.save_apps_to_json()

    def save_apps_to_json(self):
        """Guarda las aplicaciones bloqueadas en JSON."""
        blocked_apps = [self.app_list.item(i).text() for i in range(self.app_list.count())
                        if self.app_list.item(i).background().color() == QColor("#FFDDDD")]

        # Guardar los datos en JSON
        with open('data/user.json', 'w') as file:
            json.dump({'block': blocked_apps}, file, indent=4)

    def load_apps_from_json(self):
        """Carga las aplicaciones bloqueadas desde el archivo JSON."""
        try:
            with open('data/user.json', 'r') as file:
                data = json.load(file)
                apps = data.get("block", [])
                for app in apps:
                    item = QListWidgetItem(app)
                    font = QFont()
                    font.setBold(True)
                    item.setFont(font)
                    item.setBackground(QColor("#FFDDDD"))
                    self.app_list.addItem(item)
        except FileNotFoundError:
            pass  # Si el archivo no existe, no cargar nada

    def get_data(self):
        """Obtiene la lista de aplicaciones bloqueadas."""
        return [self.app_list.item(i).text() for i in range(self.app_list.count())
                if self.app_list.item(i).background().color() == QColor("#FFDDDD")]

    def filter_apps(self):
        """Filtra aplicaciones según el texto de búsqueda."""
        search_text = self.search_input.text().lower()
        for i in range(self.app_list.count()):
            item = self.app_list.item(i)
            item.setHidden(search_text not in item.text().lower())

    