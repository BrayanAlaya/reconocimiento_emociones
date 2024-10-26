from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QStackedWidget, QFrame, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
from widgets.wg_button import WgButton  # Usar el botón personalizado
from pages.p_block import PBlock
from pages.p_activities import PActivities
import json
import os

class WSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Ajustes")
        self.setFixedSize(500, 350)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)  # Quitar botones de ventana

        # Aplicar bordes redondeados y quitar los bordes visibles
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 20px;
            }
        """)

        # Oscurecer la ventana principal
        self.overlay = QWidget(parent)
        self.overlay.setStyleSheet("""
            background-color: rgba(0, 0, 0, 100);  # Oscurecer con transparencia
        """)
        self.overlay.show()
        self.update_overlay_geometry()

        # Layout principal para el modal
        layout = QHBoxLayout()

        # Crear el aside con las opciones "Bloquear", "Actividades", y "Guardar"
        aside = self.create_aside()
        layout.addWidget(aside)

        # Contenedor donde se mostrarán las páginas correspondientes
        self.settings_pages = QStackedWidget()
        layout.addWidget(self.settings_pages)

        # Página de "Bloquear" donde se podrán agregar/borrar apps
        self.block_page = PBlock(self)
        self.settings_pages.addWidget(self.block_page)

        # Página de "Actividades"
        self.activities_page = PActivities(self)
        self.settings_pages.addWidget(self.activities_page)

        self.setLayout(layout)

    def update_overlay_geometry(self):
        """Actualizar la geometría del overlay para cubrir toda la ventana principal."""
        self.overlay.setGeometry(self.parent().rect())

    def showEvent(self, event):
        """Actualizar la geometría del overlay al mostrar el diálogo."""
        self.update_overlay_geometry()
        super().showEvent(event)

    def resizeEvent(self, event):
        """Actualizar la geometría del overlay cuando la ventana principal cambie de tamaño."""
        self.update_overlay_geometry()
        super().resizeEvent(event)

    def closeEvent(self, event):
        """Sobrescribir el evento de cierre para quitar el overlay"""
        self.overlay.hide()  # Esconder la capa oscura cuando se cierre la ventana
        super().closeEvent(event)

    def create_aside(self):
        """Crear el menú lateral (aside) con botones y un botón de guardar ajustes"""
        aside = QFrame()
        aside.setFixedWidth(120)
        aside.setStyleSheet("""
            QFrame {
                background-color: transparent;  /* Sin color de fondo */
            }
        """)

        aside_layout = QVBoxLayout()

        # Botón para ir a la página "Bloquear"
        block_button = WgButton("Bloquear")
        block_button.clicked.connect(lambda: self.settings_pages.setCurrentWidget(self.block_page))
        aside_layout.addWidget(block_button)

        # Botón para ir a la página "Actividades"
        activities_button = WgButton("Actividades")
        activities_button.clicked.connect(lambda: self.settings_pages.setCurrentWidget(self.activities_page))
        aside_layout.addWidget(activities_button)

        # Espacio expandible para alinear el botón de guardar al final
        aside_layout.addStretch()

        # Botón para guardar ajustes
        save_button = WgButton("Guardar")
        save_button.clicked.connect(self.save_settings)
        aside_layout.addWidget(save_button)

        aside.setLayout(aside_layout)
        return aside

    def save_settings(self):
        """Función para guardar los ajustes en un archivo JSON"""
        try:
            # Cargar los datos existentes
            existing_data = {}
            if os.path.exists("data/user.json"):
                with open("data/user.json", "r") as file:
                    existing_data = json.load(file)

            # Obtener los bloqueos actuales del archivo y los cambios en la lista
            current_blocked_apps = existing_data.get("block", [])
            new_blocked_apps = self.block_page.get_data()

            # Mantener la lista original si no hay cambios en el bloqueo
            if not new_blocked_apps and current_blocked_apps:
                new_blocked_apps = current_blocked_apps

            # Crear un nuevo diccionario con los ajustes
            settings_data = {
                "name": existing_data.get("name", ""),  # Conservar el nombre si existe
                "password": existing_data.get("password", ""),  # Conservar la contraseña si existe
                "block": new_blocked_apps,
                "activities": self.activities_page.get_data()
            }

            with open("data/user.json", "w") as file:
                json.dump(settings_data, file, indent=4)

            print("Ajustes guardados correctamente.")
            self.close()  # Cierra el settings dialog
        except Exception as e:
            print(f"Error guardando los ajustes: {e}")
