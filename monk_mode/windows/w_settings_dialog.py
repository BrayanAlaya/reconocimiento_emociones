from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QStackedWidget, QFrame, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
from widgets.wg_button import WgButton  # Usar el botón personalizado
from pages.p_block import PBlock
from pages.p_activities import PActivities
import json

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
        self.overlay.setGeometry(parent.rect())
        self.overlay.setStyleSheet("""
            background-color: rgba(0, 0, 0, 100);  # Oscurecer con transparencia
        """)
        self.overlay.show()

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
        # Obtener los datos desde las páginas de ajustes
        settings_data = {
            "block": self.block_page.get_data(),
            "activities": self.activities_page.get_data()
        }

        # Guardar en data/user.json
        try:
            with open("data/user.json", "w") as file:
                json.dump(settings_data, file, indent=4)
            print("Ajustes guardados correctamente.")
            self.close()  # Cierra el settings dialog
        except Exception as e:
            print(f"Error guardando los ajustes: {e}")
