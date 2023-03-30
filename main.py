from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QDialog,
    QComboBox,
    QVBoxLayout,
    QToolBar,
    QStatusBar,
    QMessageBox
)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
import sys, sqlite3


class DatabaseConnection:
    def __init__(self, database_file="database.db"):
        self.database_file = database_file

    # Estblish database connection
    def connect(self):
        return sqlite3.connect(self.database_file)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Student Management System")

        # Create menu bar items
        file_menu_item = self.menuBar().addMenu("&File")
        edit_menu_item = self.menuBar().addMenu("&Edit")
        help_menu_item = self.menuBar().addMenu("&Help")

        # Create action that adds student
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        # Add 'about' action
        about_action = QAction("About", self)
        about_action.triggered.connect(self.about)
        help_menu_item.addAction(about_action)

        # Create 'search' action
        search_action = QAction(QIcon("icons/search.png"), "Search", self)
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

        # Create toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # Create status bar and add status bar elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)

        

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

    def cell_clicked(self):
        edit_btn = QPushButton("Edit Record")
        edit_btn.clicked.connect(self.edit)
        
        del_btn = QPushButton("Delete Record")
        del_btn.clicked.connect(self.delete)
        
        
        for i in self.statusbar.findChildren(QPushButton):
            self.statusbar.removeWidget(i)
        
        self.statusbar.addWidget(edit_btn)
        self.statusbar.addWidget(del_btn)
    
    def load_course_data(self) -> tuple:
        with sqlite3.connect("database.db") as db:
            cur = db.cursor()
            cur.execute("SELECT * FROM courses ORDER BY name ASC")
            courses = (x[1] for x in cur.fetchall())
            cur.close()
        return courses
        
    def insert(self):
        # Initialize Dialog
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        # Initialize Dialog
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()
    
    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self) -> None:
        super().__init__()
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
        name = self.name_line_edit.text()
        course = self.course_combo.itemText(self.course_combo.currentIndex())
        number = self.phone_line_edit.text()
        with DatabaseConnection().connect() as db:
            cur = db.cursor()
            cur.execute(
                f'INSERT INTO students(name, course, mobile) VALUES ("{name}","{course}",{number})'
            )
            db.commit()
            cur.close()
        main_window.load_data()
        
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The record was added successfully!")
        confirmation_widget.exec()


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
        items = main_window.table.findItems(s_text, Qt.MatchFlag.MatchFixedString)
        for i in items:
            i.setSelected(True)
        self.close()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Student Information")
        self.setFixedHeight(150)
        self.setFixedWidth(250)
        grid = QGridLayout()

        # Take data from selected row
        index = main_window.table.currentRow()
        student_name = main_window.table.item(index,1).text()
        course_name = main_window.table.item(index,2).text()
        phone_number = main_window.table.item(index,3).text()
        self.student_id = main_window.table.item(index,0).text()
        
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
        # Data for overwrite
        name = self.name_line_edit.text()
        course = self.course_combo.itemText(self.course_combo.currentIndex())
        number = self.phone_line_edit.text()
        
        # Update data in db
        with DatabaseConnection().connect() as db:
            cur = db.cursor()
            cur.execute(
                f'UPDATE students SET name="{name}", course="{course}",mobile={number} WHERE id = {self.student_id}'
            )
            db.commit()
            cur.close()
        main_window.load_data()
        self.close()


class DeleteDialog(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setFixedHeight(100)
        self.setFixedWidth(300)
        
        grid = QGridLayout()
        
        # Take current student id
        index = main_window.table.currentRow()
        self.student_id = main_window.table.item(index,0).text()
        
        #Create label
        info_label = QLabel("Are you sure you want to delete this record?")
        
        # Create buttons
        confirm_button = QPushButton("Yes")
        confirm_button.clicked.connect(self.delete)
        
        dismiss_button = QPushButton("No")
        dismiss_button.clicked.connect(self.close)
        
        # Add widgets to layout
        grid.addWidget(info_label, 0, 0,1,0,Qt.AlignmentFlag.AlignCenter)
        
        grid.addWidget(confirm_button, 1, 0)
        grid.addWidget(dismiss_button, 1, 1)
        
        self.setLayout(grid)
    
    def delete(self):
        # Delete row from db
        with DatabaseConnection().connect() as db:
            cur = db.cursor()
            cur.execute(
                f'DELETE FROM students WHERE id = {self.student_id}'
            )
            db.commit()
            cur.close()
        main_window.load_data()
        self.close()
        
        # Show confirmation message
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The record was deleted successfully!")
        confirmation_widget.exec()
        

class AboutDialog(QMessageBox):
    def __init__(self) -> None:
        super().__init__()
        content = """
        This app was created during an Udemy course. It allows the user to manipulate
        the data inside the 'students' database. Some of the funcionalities are from that
        course and other are added by me.
        Feel free to modify and reuse this app!
        """
        self.setText(content)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
