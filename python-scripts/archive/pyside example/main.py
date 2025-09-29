import sys
from PySide6.QtWidgets import QApplication
from ui.MainAppWindow import MainAppWindow


# if __name__ == "__main__":
app = QApplication(sys.argv)
window = MainAppWindow(app)
window.show()
app.exec()