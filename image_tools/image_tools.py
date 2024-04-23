import sys
from PyQt5.QtWidgets import QWidget, QApplication

app = QApplication(sys.argv)
widget = QWidget()
widget.resize(640, 480)
widget.setWindowTitle("Hello, PyQt5!")
widget.show()
sys.exit(app.exec())