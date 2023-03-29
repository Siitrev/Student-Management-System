from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QWidget,
    QLineEdit,
    QPushButton,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QDialog,
    QComboBox,
    QVBoxLayout
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
import sys, sqlite3


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Student Management System")

        # Create menu bar items
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # Create action that adds student
        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        # Add 'about' action
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        
        # Create 'search' action
        search_action = QAction("Search",self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)

        # Set table properties
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.verticalHeader().setVisible(False)
        self.table.setHorizontalHeaderLabels(("id", "Name", "Course", "Mobile"))
        self.setCentralWidget(self.table)
        self.load_data()
        self.setFixedWidth(self.table.width())
        self.setFixedWidth(self.table.height())

    def load_data(self):
        self.table.setRowCount(0)
        with sqlite3.connect("database.db") as db:
            cur = db.cursor()
            cur.execute("SELECT * FROM students")
            for row, data in enumerate(cur.fetchall()):
                self.table.insertRow(row)
                for col, col_data in enumerate(data):
                    self.table.setItem(row, col, QTableWidgetItem(str(col_data)))
            cur.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()
        
    def search(self):
        dialog = SearchDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setFixedHeight(150)
        self.setFixedWidth(250)
        grid = QGridLayout()

        # Create name widgets
        name_label = QLabel("Name")
        self.name_line_edit = QLineEdit()

        # Create course widgets
        course_label = QLabel("Course")
        self.course_combo = QComboBox()
        self.course_combo.addItems(self.load_course_data())

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

    def load_course_data(self) -> tuple:
        with sqlite3.connect("database.db") as db:
            cur = db.cursor()
            cur.execute("SELECT * FROM courses ORDER BY name ASC")
            courses = (x[1] for x in cur.fetchall())
            cur.close()
        return courses

    def add_student(self):
        name = self.name_line_edit.text()
        course = self.course_combo.itemText(self.course_combo.currentIndex())
        number = int(self.phone_line_edit.text())
        with sqlite3.connect("database.db") as db:
            cur = db.cursor()
            cur.execute(
                f'INSERT INTO students(name, course, mobile) VALUES ("{name}","{course}",{number})'
            )
            db.commit()
            cur.close()
        main_window.load_data()


class SearchDialog(QDialog):
    def __init__(self) -> None:
        super().__init__()
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
        items = main_window.table.findItems(s_text,Qt.MatchFlag.MatchFixedString)
        for i in items:
            i.setSelected(True)
        self.close()



app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
