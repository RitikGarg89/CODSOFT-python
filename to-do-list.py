import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, 
    QListWidget, QLabel, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

TASKS_FILE = "tasks.json"

class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To-Do List")
        self.setGeometry(200, 200, 400, 550)
        self.setStyleSheet("background-color: #2b2b2b; color: white;")

        self.layout = QVBoxLayout()

        # Heading Label
        self.heading = QLabel("📝 To-Do List")
        self.heading.setFont(QFont("Arial", 16, QFont.Bold))
        self.heading.setAlignment(Qt.AlignCenter)
        self.heading.setStyleSheet("padding: 10px; color: #ffcc00;")
        self.layout.addWidget(self.heading)

        # Task input field
        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("Enter a new task...")
        self.task_input.setFont(QFont("Arial", 12))
        self.task_input.setStyleSheet(
            "background: #3c3f41; color: white; padding: 8px; border-radius: 5px; border: 1px solid #555;"
        )
        self.layout.addWidget(self.task_input)

        # Add Task Button
        self.add_button = QPushButton("➕ Add Task", self)
        self.add_button.clicked.connect(self.add_task)
        self.style_button(self.add_button)
        self.layout.addWidget(self.add_button)

        # Mark Completed Button
        self.complete_button = QPushButton("✅ Mark Completed", self)
        self.complete_button.clicked.connect(self.mark_completed)
        self.style_button(self.complete_button)
        self.layout.addWidget(self.complete_button)

        # Delete Task Button
        self.delete_button = QPushButton("🗑 Delete Task", self)
        self.delete_button.clicked.connect(self.delete_task)
        self.style_button(self.delete_button)
        self.layout.addWidget(self.delete_button)

        # Mark All Completed Button
        self.mark_all_button = QPushButton("✅ Mark All Completed", self)
        self.mark_all_button.clicked.connect(self.mark_all_completed)
        self.style_button(self.mark_all_button)
        self.layout.addWidget(self.mark_all_button)

        # Delete All Completed Button
        self.delete_all_completed_button = QPushButton("🗑 Delete All Completed", self)
        self.delete_all_completed_button.clicked.connect(self.delete_all_completed)
        self.style_button(self.delete_all_completed_button)
        self.layout.addWidget(self.delete_all_completed_button)

        # Task List
        self.task_list = QListWidget(self)
        self.task_list.setFont(QFont("Arial", 12))
        self.task_list.setStyleSheet(
            "background: #3c3f41; color: white; padding: 8px; border-radius: 5px; border: 1px solid #555;"
        )
        self.layout.addWidget(self.task_list)

        self.setLayout(self.layout)

        self.tasks = self.load_tasks()
        self.update_task_list()

    def style_button(self, button):
        button.setFont(QFont("Arial", 11))
        button.setStyleSheet("""
            QPushButton {
                background-color: #555; 
                color: white; 
                padding: 10px;
                border-radius: 8px;
                border: 1px solid #777;
            }
            QPushButton:hover {
                background-color: #777;
            }
        """)

    def load_tasks(self):
        try:
            with open(TASKS_FILE, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_tasks(self):
        with open(TASKS_FILE, "w") as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self):
        task = self.task_input.text().strip()
        if task:
            self.tasks.append({"task": task, "completed": False})
            self.save_tasks()
            self.update_task_list()
            self.task_input.clear()
        else:
            QMessageBox.warning(self, "Warning", "Task cannot be empty!")

    def mark_completed(self):
        selected = self.task_list.currentRow()
        if selected >= 0:
            self.tasks[selected]["completed"] = True
            self.save_tasks()
            self.update_task_list()
        else:
            QMessageBox.warning(self, "Warning", "No task selected!")

    def delete_task(self):
        selected = self.task_list.currentRow()
        if selected >= 0:
            del self.tasks[selected]
            self.save_tasks()
            self.update_task_list()
        else:
            QMessageBox.warning(self, "Warning", "No task selected!")

    def mark_all_completed(self):
        if self.tasks:
            for task in self.tasks:
                task["completed"] = True
            self.save_tasks()
            self.update_task_list()
        else:
            QMessageBox.warning(self, "Warning", "No tasks available!")

    def delete_all_completed(self):
        if any(task["completed"] for task in self.tasks):
            self.tasks = [task for task in self.tasks if not task["completed"]]
            self.save_tasks()
            self.update_task_list()
        else:
            QMessageBox.warning(self, "Warning", "No completed tasks to delete!")

    def update_task_list(self):
        self.task_list.clear()
        for task in self.tasks:
            status = "✅" if task["completed"] else "❌"
            self.task_list.addItem(f"{status} {task['task']}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToDoApp()
    window.show()
    sys.exit(app.exec_())
