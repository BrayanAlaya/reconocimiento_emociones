from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QComboBox, QMessageBox
from widgets.custom_button import CustomButton  # Importar el CustomButton
from widgets.custom_notification import NotificationWidget

class AjustesPage(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window

        layout = QVBoxLayout()

        # Selección de la posición del contador
        self.position_label = QLabel("Selecciona la posición del contador:")
        self.position_combo = QComboBox()
        self.position_combo.addItems(["Arriba Izquierda", "Arriba Derecha", "Abajo Izquierda", "Abajo Derecha", "Desactivar Contador"])

        layout.addWidget(self.position_label)
        layout.addWidget(self.position_combo)

        # Botón para confirmar configuración
        self.confirm_button = CustomButton("Guardar Configuración")
        self.confirm_button.clicked.connect(self.confirm_settings)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

    def confirm_settings(self):
        # Obtener la opción seleccionada de la posición del contador
        contador_posicion = self.position_combo.currentText()

        if contador_posicion == "Desactivar Contador":
            QMessageBox.information(self, "Configuración Guardada", "El contador ha sido desactivado.")
        else:
            QMessageBox.information(self, "Configuración Guardada", f"Posición del contador: {contador_posicion}")

        # Guardar las configuraciones en el main window o en alguna variable accesible
        self.main_window.contador_posicion = contador_posicion

        # Crear y mostrar la notificación en la posición fija
        notification = NotificationWidget("¡Esto es una notificación!")
        notification.show_notification()

        self.close()
