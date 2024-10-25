import sys
from PyQt6.QtWidgets import QApplication
from windows.w_splash import WSplash  # Importar el splash screen

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Crear y mostrar la ventana del splash screen
    splash = WSplash()
    splash.show()

    # Ejecutar la aplicación
    sys.exit(app.exec())
