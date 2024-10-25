from PyQt6.QtWidgets import QPushButton

class WgButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.apply_styles()

    def apply_styles(self):
        """Aplicar los colores con variantes del verde"""
        self.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;  /* Verde base */
                color: white;  /* Texto blanco */
                border: none;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #66BB6A;  /* Verde más claro para hover */
                color: white;
            }
            QPushButton:pressed {
                background-color: #388E3C;  /* Verde más oscuro para estado presionado */
                color: white;
            }
        """)

    def update_style(self):
        """Actualizar el estilo del botón si es necesario en el futuro"""
        self.apply_styles()
