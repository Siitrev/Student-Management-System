from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QMessageBox,
)
from utils.DatabaseConnection import DatabaseConnection
import sqlite3


class InsertCourseDialog(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Add Course")
        self.setFixedHeight(150)
        self.setFixedWidth(250)
        
        # Create layout
        grid = QVBoxLayout()
        
        # Create edit line 
        self.course_line_edit = QLineEdit()
        self.course_line_edit.setPlaceholderText("Course name")
        
        # Create button
        button = QPushButton("Submit")
        button.clicked.connect(self.add_course)
        
        # Add widgets to layout
        grid.addWidget(self.course_line_edit)
        grid.addWidget(button)
        
        self.setLayout(grid)
        
    def add_course(self): 
        course = self.course_line_edit.text()
        try:
            with DatabaseConnection().connect() as db:
                cur = db.cursor()
                cur.execute(
                    f'INSERT INTO courses(name) VALUES ("{course}")'
                )
                db.commit()
                cur.close()
            confirmation_widget = QMessageBox()
            confirmation_widget.setWindowTitle("Success")
            confirmation_widget.setText("The record was added successfully!")
            confirmation_widget.exec()      
        except sqlite3.IntegrityError:
            confirmation_widget = QMessageBox()
            confirmation_widget.setWindowTitle("Error!")
            confirmation_widget.setText("The record has already been added into database!")
            confirmation_widget.exec()     
        
        
