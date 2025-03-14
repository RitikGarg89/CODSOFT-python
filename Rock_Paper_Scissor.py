import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt

class RockPaperScissorsGame(QWidget):
    def __init__(self):
        super().__init__()

        self.user_score = 0
        self.computer_score = 0

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Rock-Paper-Scissors")
        self.setGeometry(200, 200, 400, 300)

        # Dark Theme
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        self.setPalette(palette)

        # Labels
        self.label_title = QLabel("Rock-Paper-Scissors", self)
        self.label_title.setFont(QFont("Arial", 14, QFont.Bold))
        self.label_title.setAlignment(Qt.AlignCenter)

        self.label_result = QLabel("Choose Rock, Paper, or Scissors", self)
        self.label_result.setFont(QFont("Arial", 12))
        self.label_result.setAlignment(Qt.AlignCenter)

        self.label_score = QLabel(f"Score: You {self.user_score} - {self.computer_score} Computer", self)
        self.label_score.setFont(QFont("Arial", 12))
        self.label_score.setAlignment(Qt.AlignCenter)

        # Buttons
        self.rock_button = QPushButton("Rock")
        self.paper_button = QPushButton("Paper")
        self.scissors_button = QPushButton("Scissors")

        # Orange Button Styling
        button_style = """
            QPushButton {
                background-color: #FF8C00;  /* Orange color */
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #E07B00;  /* Darker orange on hover */
            }
        """

        self.rock_button.setStyleSheet(button_style)
        self.paper_button.setStyleSheet(button_style)
        self.scissors_button.setStyleSheet(button_style)

        self.rock_button.clicked.connect(lambda: self.play("Rock"))
        self.paper_button.clicked.connect(lambda: self.play("Paper"))
        self.scissors_button.clicked.connect(lambda: self.play("Scissors"))

        # Layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.label_title)
        vbox.addWidget(self.label_result)
        vbox.addWidget(self.label_score)

        hbox = QHBoxLayout()
        hbox.addWidget(self.rock_button)
        hbox.addWidget(self.paper_button)
        hbox.addWidget(self.scissors_button)

        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def play(self, user_choice):
        choices = ["Rock", "Paper", "Scissors"]
        computer_choice = random.choice(choices)

        # Determine Winner
        if user_choice == computer_choice:
            result_text = f"Tie! Both chose {user_choice}"
        elif (user_choice == "Rock" and computer_choice == "Scissors") or \
             (user_choice == "Scissors" and computer_choice == "Paper") or \
             (user_choice == "Paper" and computer_choice == "Rock"):
            self.user_score += 1
            result_text = f"You Win! {user_choice} beats {computer_choice}"
        else:
            self.computer_score += 1
            result_text = f"You Lose! {computer_choice} beats {user_choice}"

        # Update UI
        self.label_result.setText(result_text)
        self.label_score.setText(f"Score: You {self.user_score} - {self.computer_score} Computer")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = RockPaperScissorsGame()
    game.show()
    sys.exit(app.exec_())
