from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QListWidget, QLineEdit, QListWidgetItem
from PyQt6.QtGui import QFont, QColor
from widgets.wg_button import WgButton
from utils.json_manager import load_json
import json
import os
import psutil

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

        # Cargar aplicaciones desde JSON
        self.load_apps_from_json()

        # Atributo para verificar si la concentración está activa
        self.concentration_active = False

    def load_executables(self):
        """Carga todos los archivos .exe disponibles en el sistema."""        
        self.app_list.clear()  # Limpiar lista antes de cargar
        exe_files = self.scan_executables()  # Usar el escáner de ejecutables
        blocked_apps = self.get_data()  # Obtener las apps ya bloqueadas

        for exe in exe_files:
            item = QListWidgetItem(exe)

            # Si la aplicación ya está bloqueada, agregar estilo
            if exe in blocked_apps:
                font = QFont()
                font.setBold(True)
                item.setFont(font)
                item.setBackground(QColor("#FFDDDD"))  # Fondo distintivo

            self.app_list.addItem(item)

    def scan_executables(self):
        """Escanea el sistema en busca de archivos .exe."""
        exe_files = []
        directories = [os.getenv('ProgramFiles'), os.getenv('ProgramFiles(x86)'), os.getenv('LOCALAPPDATA')]

        for directory in directories:
            if directory and os.path.exists(directory):
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        if file.endswith('.exe'):
                            exe_files.append(file)
        return exe_files

    def block_app(self):
        """Bloquea la aplicación seleccionada."""        
        if not self.concentration_active:  # Solo permitir si no hay concentración activa
            selected_item = self.app_list.currentItem()
            if selected_item:
                app_name = selected_item.text()
                # Verifica si la aplicación ya está bloqueada
                if app_name not in self.get_data():  
                    item = QListWidgetItem(app_name)
                    font = QFont()
                    font.setBold(True)
                    item.setFont(font)
                    item.setBackground(QColor("#FFDDDD"))  # Fondo distintivo para bloqueados
                    self.app_list.addItem(item)
                    self.save_apps_to_json()

    def delete_app(self):
        """Elimina la aplicación seleccionada."""        
        selected_item = self.app_list.currentItem()
        if selected_item:
            self.app_list.takeItem(self.app_list.row(selected_item))
            self.save_apps_to_json()

    def save_apps_to_json(self):
        """Guarda solo las aplicaciones bloqueadas seleccionadas por el usuario en el archivo JSON."""
        blocked_apps = [self.app_list.item(i).text() for i in range(self.app_list.count())
                        if self.app_list.item(i).background().color() == QColor("#FFDDDD")]

        # Cargar datos existentes
        data = load_json('data/user.json')
        data['block'] = blocked_apps  # Actualizar la lista de bloqueados

        with open('data/user.json', 'w') as file:
            json.dump(data, file, indent=4)

    def load_apps_from_json(self):
        """Carga aplicaciones bloqueadas desde el archivo JSON."""
        data = load_json('data/user.json')
        apps = data.get("block", [])

        for app in apps:
            item = QListWidgetItem(app)
            font = QFont()
            font.setBold(True)
            item.setFont(font)
            item.setBackground(QColor("#FFDDDD"))  # Fondo distintivo
            self.app_list.addItem(item)

        # Cargar todos los ejecutables para la búsqueda
        self.load_executables()

    def get_data(self):
        """Retorna las aplicaciones bloqueadas actualmente."""
        return [self.app_list.item(i).text() for i in range(self.app_list.count())
                if self.app_list.item(i).background().color() == QColor("#FFDDDD")]

    def filter_apps(self):
        """Filtra las aplicaciones según el texto de búsqueda."""
        search_text = self.search_input.text().lower()
        for i in range(self.app_list.count()):
            item = self.app_list.item(i)
            item.setHidden(search_text not in item.text().lower())  # Ocultar o mostrar según la búsqueda

    def start_concentration(self):
        """Inicia la sesión de concentración."""
        self.concentration_active = True
        self.block_app_button.setEnabled(False)  # Deshabilitar el botón de bloquear
        self.enforce_blocking()  # Aplicar bloqueo de aplicaciones

    def end_concentration(self):
        """Finaliza la sesión de concentración."""
        self.concentration_active = False
        self.block_app_button.setEnabled(True)  # Habilitar el botón de bloquear
        self.release_blocking()  # Liberar bloqueo de aplicaciones

    def enforce_blocking(self):
        """Bloquea las aplicaciones seleccionadas mientras la concentración está activa."""
        blocked_apps = self.get_data()
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            try:
                if proc.info['name'] in blocked_apps:
                    proc.kill()  # Matar el proceso bloqueado
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    def release_blocking(self):
        """Liberar el bloqueo de las aplicaciones."""
        # Aquí puedes implementar lógica si necesitas realizar alguna acción específica
        pass
