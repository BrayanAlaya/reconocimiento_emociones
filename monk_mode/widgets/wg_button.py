from PyQt6.QtWidgets import QPushButton

class WgButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.apply_styles()

    def apply_styles(self):
        """Aplicar los colores directamente con tonos de gris"""
        self.setStyleSheet("""
            QPushButton {
                background-color: #D3D3D3;  /* Gris claro */
                color: #4F4F4F;  /* Texto gris oscuro */
                border: none;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #B0B0B0;  /* Gris medio - para hover */
                color: #323232;  /* Texto gris más oscuro en hover */
            }
            QPushButton:pressed {
                background-color: #8E8E8E;  /* Gris más oscuro - para estado presionado */
            }
        """)

    def update_style(self):
        """Actualizar el estilo del botón si es necesario en el futuro"""
        self.apply_styles()
