import sys
from PyQt6 import QtWidgets

app = QtWidgets.QApplication(sys.argv)

window = QtWidgets.QWidget()
window.resize(300, 200)
window.setWindowTitle('Hello, World!')

window.show()
sys.exit(app.exec())