from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLineEdit, QMainWindow
from PyQt6.QtCore import Qt


class SearchDialog(QDialog):
    def __init__(self, main_window: QMainWindow) -> None:
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Search Student")
        self.setFixedHeight(150)
        self.setFixedWidth(250)

        # Creating layout
        layout = QVBoxLayout()

        # Create field for student name
        self.name_line_edit = QLineEdit()
        self.name_line_edit.setPlaceholderText("Name")

        # Create button for searching
        button = QPushButton("Search")
        button.clicked.connect(self.search_student)

        # Add widgets to layout
        layout.addWidget(self.name_line_edit)
        layout.addWidget(button)

        self.setLayout(layout)

    def search_student(self):
        s_text = self.name_line_edit.text()
        items = self.main_window.table.findItems(s_text, Qt.MatchFlag.MatchFixedString)
        for i in items:
            i.setSelected(True)
        self.close()
