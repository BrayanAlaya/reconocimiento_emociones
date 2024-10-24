from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class EstadisticasPage(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        layout = QVBoxLayout()

        title_label = QLabel("Página de Estadísticas")
        layout.addWidget(title_label)

        # Aquí puedes agregar más elementos como gráficos, tablas, etc.
        
        # Ejemplo de un texto adicional
        description_label = QLabel("Aquí puedes ver las estadísticas y análisis.")
        layout.addWidget(description_label)

        self.setLayout(layout)
