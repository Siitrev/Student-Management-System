from PyQt6.QtWidgets import (
    QDialog,
    QGridLayout,
    QComboBox,
    QLabel,
    QPushButton,
    QLineEdit,
    QMessageBox,
    QMainWindow,
)
from utils.DatabaseConnection import DatabaseConnection
from utils.Validation import *


class InsertStudentDialog(QDialog):
    def __init__(self, main_window: QMainWindow) -> None:
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Add Student")
        self.setFixedHeight(150)
        self.setFixedWidth(250)
        grid = QGridLayout()

        # Create name widgets
        name_label = QLabel("Name")
        self.name_line_edit = QLineEdit()

        # Create course widgets
        course_label = QLabel("Course")
        self.course_combo = QComboBox()
        self.course_combo.addItems(main_window.load_course_data())

        # Create phone widgets
        phone_label = QLabel("Phone")
        self.phone_line_edit = QLineEdit()

        # Create button widget
        submit_btn = QPushButton("Submit")
        submit_btn.clicked.connect(self.add_student)

        # Add widgets to grid
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_line_edit, 0, 1)

        grid.addWidget(course_label, 1, 0)
        grid.addWidget(self.course_combo, 1, 1)

        grid.addWidget(phone_label, 2, 0)
        grid.addWidget(self.phone_line_edit, 2, 1)

        grid.addWidget(submit_btn, 3, 0, 1, 0)

        self.setLayout(grid)

    def add_student(self):
        try:
            name = self.name_line_edit.text().strip()
            course = self.course_combo.itemText(self.course_combo.currentIndex())
            number = self.phone_line_edit.text().strip()
            
            # Validating the data
            name_validation(name)
            phone_validation(number)
            
            with DatabaseConnection().connect() as db:
                cur = db.cursor()
                cur.execute(
                    f'INSERT INTO students(name, course, mobile) VALUES ("{name.lower().title()}","{course}",{number})'
                )
                db.commit()
                cur.close()
            self.main_window.load_data()

            #Show confirmation message
            confirmation_widget = QMessageBox()
            confirmation_widget.setWindowTitle("Success")
            confirmation_widget.setText("The record was added successfully!")
            confirmation_widget.exec()
            
            #Show error message
        except NameValidaionException:
            error_widget = QMessageBox()
            error_widget.setWindowTitle("Error!")
            error_widget.setText(
                "Name should only consist of lower-/uppercase letters."
            )
            error_widget.exec()
        except PhoneValidaionException:
            error_widget = QMessageBox()
            error_widget.setWindowTitle("Error!")
            error_widget.setText(
                "Phone number should look like: (+xx)xxxxxxxxx or xxxxxxxxx."
            )
            error_widget.exec()
