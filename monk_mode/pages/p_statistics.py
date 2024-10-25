from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class PStatistics (QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        label = QLabel("Página de Estadísticas")
        layout.addWidget(label)

        # Aquí puedes agregar widgets para mostrar gráficos, estadísticas de tiempo, etc.

        self.setLayout(layout)
