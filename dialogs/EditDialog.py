from PyQt6.QtWidgets import (
    QDialog,
    QGridLayout,
    QComboBox,
    QLabel,
    QPushButton,
    QLineEdit,
    QMainWindow,
    QMessageBox
)
from utils.DatabaseConnection import DatabaseConnection
from utils.Validation import *


class EditDialog(QDialog):
    def __init__(self, main_window: QMainWindow):
        super().__init__()
        self.setWindowTitle("Edit Student Information")
        self.setFixedHeight(150)
        self.setFixedWidth(250)
        grid = QGridLayout()
        self.main_window = main_window

        # Take data from selected row
        index = main_window.table.currentRow()
        student_name = main_window.table.item(index, 1).text()
        course_name = main_window.table.item(index, 2).text()
        phone_number = main_window.table.item(index, 3).text()
        self.student_id = main_window.table.item(index, 0).text()

        # Create name widgets
        name_label = QLabel("Name")
        self.name_line_edit = QLineEdit(student_name)

        # Create course widgets
        course_label = QLabel("Course")
        self.course_combo = QComboBox()
        self.course_combo.addItems(main_window.load_course_data())
        self.course_combo.setCurrentText(course_name)

        # Create phone widgets
        phone_label = QLabel("Phone")
        self.phone_line_edit = QLineEdit(phone_number)

        # Create button widget
        submit_btn = QPushButton("Submit")
        submit_btn.clicked.connect(self.edit)

        # Add widgets to grid
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_line_edit, 0, 1)

        grid.addWidget(course_label, 1, 0)
        grid.addWidget(self.course_combo, 1, 1)

        grid.addWidget(phone_label, 2, 0)
        grid.addWidget(self.phone_line_edit, 2, 1)

        grid.addWidget(submit_btn, 3, 0, 1, 0)

        self.setLayout(grid)

    def edit(self):
        try:
            # Data
            name = self.name_line_edit.text().strip()
            course = self.course_combo.itemText(self.course_combo.currentIndex())
            number = self.phone_line_edit.text().strip()
            
            #Validating the data
            name_validation(name)
            phone_validation(number)

            # Update data in db
            with DatabaseConnection().connect() as db:
                cur = db.cursor()
                cur.execute(
                    f'UPDATE students SET name="{name.lower().title()}", course="{course}",mobile={number} WHERE id = {self.student_id}'
                )
                db.commit()
                cur.close()
            self.main_window.load_data()
            confirmation_widget = QMessageBox()
            confirmation_widget.setWindowTitle("Success")
            confirmation_widget.setText("The record was edited successfully!")
            confirmation_widget.exec()
            self.close()
        except NameValidaionException:
            error_widget = QMessageBox()
            error_widget.setWindowTitle("Error!")
            error_widget.setText(
                "Name should only consist of lower-/uppercase letters!"
            )
            error_widget.exec()
        except PhoneValidaionException:
            error_widget = QMessageBox()
            error_widget.setWindowTitle("Error!")
            error_widget.setText(
                "Phone number should look like: (+xx)xxxxxxxxx or xxxxxxxxx."
            )
            error_widget.exec()
