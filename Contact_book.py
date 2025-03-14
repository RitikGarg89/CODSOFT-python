import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QTextEdit, QVBoxLayout, QHBoxLayout, QListWidget, QMessageBox
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt

CONTACTS_FILE = "contacts.json"

class ContactBook(QWidget):
    def __init__(self):
        super().__init__()
        self.contacts = self.load_contacts()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Contact Book")
        self.setGeometry(200, 200, 500, 400)

        # Dark Theme
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        self.setPalette(palette)

        # Labels
        self.label_title = QLabel("Contact Book", self)
        self.label_title.setFont(QFont("Arial", 16, QFont.Bold))
        self.label_title.setAlignment(Qt.AlignCenter)

        self.label_name = QLabel("Name:")
        self.label_phone = QLabel("Phone:")
        self.label_email = QLabel("Email:")
        self.label_address = QLabel("Address:")

        # Input Fields
        self.input_name = QLineEdit()
        self.input_phone = QLineEdit()
        self.input_email = QLineEdit()
        self.input_address = QTextEdit()
        self.contact_list = QListWidget()

        # Buttons
        self.add_button = QPushButton("Add Contact")
        self.update_button = QPushButton("Update Contact")
        self.delete_button = QPushButton("Delete Contact")
        self.search_button = QPushButton("Search Contact")

        # Orange Button Styling
        button_style = """
            QPushButton {
                background-color: #FF8C00;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #E07B00;
            }
        """
        self.add_button.setStyleSheet(button_style)
        self.update_button.setStyleSheet(button_style)
        self.delete_button.setStyleSheet(button_style)
        self.search_button.setStyleSheet(button_style)

        # Layouts
        vbox = QVBoxLayout()
        vbox.addWidget(self.label_title)
        vbox.addWidget(self.label_name)
        vbox.addWidget(self.input_name)
        vbox.addWidget(self.label_phone)
        vbox.addWidget(self.input_phone)
        vbox.addWidget(self.label_email)
        vbox.addWidget(self.input_email)
        vbox.addWidget(self.label_address)
        vbox.addWidget(self.input_address)

        hbox = QHBoxLayout()
        hbox.addWidget(self.add_button)
        hbox.addWidget(self.update_button)
        hbox.addWidget(self.delete_button)
        hbox.addWidget(self.search_button)
        
        vbox.addLayout(hbox)
        vbox.addWidget(self.contact_list)

        self.setLayout(vbox)

        # Load and Display Contacts
        self.load_contact_list()

        # Button Click Events
        self.add_button.clicked.connect(self.add_contact)
        self.update_button.clicked.connect(self.update_contact)
        self.delete_button.clicked.connect(self.delete_contact)
        self.search_button.clicked.connect(self.search_contact)
        self.contact_list.itemClicked.connect(self.fill_fields)

    def load_contacts(self):
        try:
            with open(CONTACTS_FILE, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_contacts(self):
        with open(CONTACTS_FILE, "w") as file:
            json.dump(self.contacts, file, indent=4)

    def load_contact_list(self):
        self.contact_list.clear()
        for name, details in self.contacts.items():
            self.contact_list.addItem(f"{name} - {details['phone']}")

    def add_contact(self):
        name = self.input_name.text().strip()
        phone = self.input_phone.text().strip()
        email = self.input_email.text().strip()
        address = self.input_address.toPlainText().strip()

        if not name or not phone:
            QMessageBox.warning(self, "Error", "Name and Phone are required!")
            return

        self.contacts[name] = {"phone": phone, "email": email, "address": address}
        self.save_contacts()
        self.load_contact_list()
        self.clear_fields()
        QMessageBox.information(self, "Success", "Contact Added!")

    def update_contact(self):
        name = self.input_name.text().strip()
        if name in self.contacts:
            self.contacts[name] = {
                "phone": self.input_phone.text().strip(),
                "email": self.input_email.text().strip(),
                "address": self.input_address.toPlainText().strip(),
            }
            self.save_contacts()
            self.load_contact_list()
            QMessageBox.information(self, "Success", "Contact Updated!")
        else:
            QMessageBox.warning(self, "Error", "Contact not found!")

    def delete_contact(self):
        name = self.input_name.text().strip()
        if name in self.contacts:
            del self.contacts[name]
            self.save_contacts()
            self.load_contact_list()
            self.clear_fields()
            QMessageBox.information(self, "Success", "Contact Deleted!")
        else:
            QMessageBox.warning(self, "Error", "Contact not found!")

    def search_contact(self):
        query = self.input_name.text().strip()
        self.contact_list.clear()
        found = False
        for name, details in self.contacts.items():
            if query.lower() in name.lower() or query in details["phone"]:
                self.contact_list.addItem(f"{name} - {details['phone']}")
                found = True
        if not found:
            QMessageBox.warning(self, "Not Found", "No contact found!")

    def fill_fields(self, item):
        selected_contact = item.text().split(" - ")[0]
        if selected_contact in self.contacts:
            self.input_name.setText(selected_contact)
            self.input_phone.setText(self.contacts[selected_contact]["phone"])
            self.input_email.setText(self.contacts[selected_contact]["email"])
            self.input_address.setPlainText(self.contacts[selected_contact]["address"])

    def clear_fields(self):
        self.input_name.clear()
        self.input_phone.clear()
        self.input_email.clear()
        self.input_address.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    contact_book = ContactBook()
    contact_book.show()
    sys.exit(app.exec_())
