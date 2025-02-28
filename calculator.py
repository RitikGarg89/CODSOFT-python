from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QGridLayout
from PyQt5.QtGui import QFont, QKeyEvent
from PyQt5.QtCore import Qt
import sys

class IOSCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("iOS Style Calculator")
        self.setGeometry(100, 100, 300, 400)
        self.setStyleSheet("background-color: #1C1C1E; color: white;")
        
        self.layout = QVBoxLayout()
        self.display = QLabel("0", self)
        self.display.setFont(QFont("Arial", 24))
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet("background: #2C2C2E; padding: 15px; border-radius: 10px;")
        self.layout.addWidget(self.display)
        
        grid_layout = QGridLayout()
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3)
        ]
        
        for text, row, col in buttons:
            button = QPushButton(text)
            button.setFont(QFont("Arial", 18))
            button.setFixedSize(60, 60)  # Ensuring circular shape
            button.setStyleSheet(
                "QPushButton {"
                "background: #3A3A3C; color: white; border-radius: 30px; padding: 10px;"
                "}"
                "QPushButton:pressed {"
                "background: #575757;"
                "}"
                if text not in ['+', '-', '*', '/'] else 
                "QPushButton {"
                "background: #FF9500; color: white; border-radius: 30px; padding: 10px;"
                "}"
                "QPushButton:pressed {"
                "background: #CC7700;"
                "}"
            )
            button.clicked.connect(self.on_button_click)
            grid_layout.addWidget(button, row, col)
        
        self.layout.addLayout(grid_layout)
        self.setLayout(self.layout)
        self.expression = ""
        self.result_displayed = False

    def on_button_click(self):
        sender = self.sender().text()
        self.process_input(sender)
    
    def keyPressEvent(self, event):
        key_map = {
            Qt.Key_0: '0', Qt.Key_1: '1', Qt.Key_2: '2', Qt.Key_3: '3',
            Qt.Key_4: '4', Qt.Key_5: '5', Qt.Key_6: '6', Qt.Key_7: '7',
            Qt.Key_8: '8', Qt.Key_9: '9', Qt.Key_Plus: '+', Qt.Key_Minus: '-',
            Qt.Key_Asterisk: '*', Qt.Key_Slash: '/', Qt.Key_Period: '.',
            Qt.Key_Equal: '=', Qt.Key_Return: '=', Qt.Key_Enter: '='
        }
        if event.key() in key_map:
            self.process_input(key_map[event.key()])
    
    def process_input(self, value):
        if self.result_displayed:
            if value in ['+', '-', '*', '/']:
                self.result_displayed = False  # Continue operation
            else:
                self.expression = ""  # Clear for new input
                self.result_displayed = False
        
        if value == "=":
            try:
                self.expression = str(eval(self.expression))
                self.result_displayed = True
            except:
                self.expression = "Error"
                self.result_displayed = False
        else:
            if self.expression == "Error":
                self.expression = ""
            self.expression += value
        self.display.setText(self.expression)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = IOSCalculator()
    calc.show()
    sys.exit(app.exec_())
