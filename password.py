from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QSlider, QCheckBox, QHBoxLayout, QLineEdit
from PyQt5.QtGui import QFont, QClipboard
from PyQt5.QtCore import Qt
import sys, random, string

class IOSPasswordGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Password Generator")
        self.setGeometry(100, 100, 350, 500)
        self.setStyleSheet("background-color: #1C1C1E; color: white;")
        
        layout = QVBoxLayout()
        
        self.password_container = QHBoxLayout()
        
        self.password_input = QLineEdit(self)
        self.password_input.setFont(QFont("Arial", 16))
        self.password_input.setAlignment(Qt.AlignCenter)
        self.password_input.setStyleSheet("background: #2C2C2E; padding: 20px; border-radius: 10px; color: white; font-size: 24px; min-height: 60px; min-width: 250px;")
        self.password_input.setReadOnly(True)
        
        self.copy_button = QPushButton("Copy", self)
        self.copy_button.setFont(QFont("Arial", 14))
        self.copy_button.setStyleSheet("background: #007AFF; color: white; padding: 10px; border-radius: 10px;")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        
        self.password_container.addWidget(self.password_input)
        self.password_container.addWidget(self.copy_button)
        
        layout.addLayout(self.password_container)
        
        self.length_label = QLabel("Password Length: 8", self)
        self.length_label.setFont(QFont("Arial", 14))
        self.length_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.length_label)
        
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(4)
        self.slider.setMaximum(20)
        self.slider.setValue(8)
        self.slider.setStyleSheet("QSlider::groove:horizontal { background: #3A3A3C; height: 8px; }" 
                                  "QSlider::handle:horizontal { background: #FF9500; width: 18px; border-radius: 9px; }")
        self.slider.valueChanged.connect(self.update_length_label)
        layout.addWidget(self.slider)
        
        self.uppercase_checkbox = QCheckBox("Include Uppercase Letters", self)
        self.uppercase_checkbox.setFont(QFont("Arial", 12))
        layout.addWidget(self.uppercase_checkbox)
        
        self.numbers_checkbox = QCheckBox("Include Numbers", self)
        self.numbers_checkbox.setFont(QFont("Arial", 12))
        layout.addWidget(self.numbers_checkbox)
        
        self.symbols_checkbox = QCheckBox("Include Symbols", self)
        self.symbols_checkbox.setFont(QFont("Arial", 12))
        layout.addWidget(self.symbols_checkbox)
        
        self.button = QPushButton("Generate Password", self)
        self.button.setFont(QFont("Arial", 14))
        self.button.setStyleSheet("background: #FF9500; color: white; padding: 10px; border-radius: 10px;")
        self.button.clicked.connect(self.generate_password)
        layout.addWidget(self.button)
        
        self.setLayout(layout)
    
    def update_length_label(self, value):
        self.length_label.setText(f"Password Length: {value}")
    
    def generate_password(self):
        length = self.slider.value()
        chars = string.ascii_lowercase
        if self.uppercase_checkbox.isChecked():
            chars += string.ascii_uppercase
        if self.numbers_checkbox.isChecked():
            chars += string.digits
        if self.symbols_checkbox.isChecked():
            chars += string.punctuation
        
        password = ''.join(random.choice(chars) for _ in range(length))
        self.password_input.setText(password)
    
    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.password_input.text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IOSPasswordGenerator()
    window.show()
    sys.exit(app.exec_())