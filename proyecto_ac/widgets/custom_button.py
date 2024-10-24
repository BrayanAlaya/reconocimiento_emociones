# widgets/custom_button.py
from PyQt6.QtWidgets import QPushButton

class CustomButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #95d989;  
                color: #475244;  
                border: none;  
                border-radius: 10px;  
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #aae39c;  
                color: #319300;
            }
            QPushButton:pressed {
                background-color: #c5ffb6;  
            }
        """)

