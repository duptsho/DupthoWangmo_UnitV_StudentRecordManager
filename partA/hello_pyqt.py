import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("PyQt6 Hello World")
window.resize(350, 180)

layout = QVBoxLayout()
message = QLabel("Hello from PyQt6!")
button = QPushButton("Click me")
button.clicked.connect(lambda: message.setText("Hello! You clicked the button."))

layout.addWidget(message)
layout.addWidget(button)
window.setLayout(layout)

window.show()
sys.exit(app.exec())
