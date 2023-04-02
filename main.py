from PyQt6.QtWidgets import (
    QApplication,
    QPushButton,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QToolBar,
    QStatusBar,
)
from utils.DatabaseConnection import DatabaseConnection
from dialogs import (
    AboutDialog,
    DeleteStudentDialog,
    DeleteStudentsDialog,
    EditDialog,
    InsertCourseDialog,
    InsertStudentDialog,
    SearchDialog,
)
from PyQt6.QtGui import QAction, QIcon
import sys


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
        add_student_action.triggered.connect(self.insert_student)
        file_menu_item.addAction(add_student_action)

        # Create 'add course' action
        add_course_action = QAction("Add Course", self)
        add_course_action.triggered.connect(self.insert_course)
        file_menu_item.addAction(add_course_action)

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
        self.table.selectionModel().selectionChanged.connect(self.cell_clicked)
        
    def load_data(self):
        self.table.setRowCount(0)
        with DatabaseConnection().connect() as db:
            cur = db.cursor()
            cur.execute("SELECT * FROM students")
            for row, data in enumerate(cur.fetchall()):
                self.table.insertRow(row)
                for col, col_data in enumerate(data):
                    self.table.setItem(row, col, QTableWidgetItem(str(col_data)))
            cur.close()

    def cell_clicked(self, selected, deselected):
        selected_cells = self.table.selectedIndexes()
        
        edit_btn = QPushButton("Edit Record")
        edit_btn.clicked.connect(self.edit)
        
        if len(selected_cells) == 1:
            del_btn = QPushButton("Delete Record")
            del_btn.clicked.connect(self.delete)
        else:
            del_btn = QPushButton("Delete Records")
            del_btn.clicked.connect(self.delete_multiple)

        # Remove old buttons
        for i in self.statusbar.findChildren(QPushButton):
            self.statusbar.removeWidget(i)

        self.statusbar.addWidget(edit_btn)
        self.statusbar.addWidget(del_btn)

    def load_course_data(self) -> tuple:
        with DatabaseConnection().connect() as db:
            cur = db.cursor()
            cur.execute("SELECT * FROM courses ORDER BY name ASC")
            courses = (x[1] for x in cur.fetchall())
            cur.close()
        return courses

    def insert_student(self):
        # Initialize Dialog
        dialog = InsertStudentDialog.InsertStudentDialog(self)
        dialog.exec()

    def insert_course(self):
        # Initialize Dialog
        dialog = InsertCourseDialog.InsertCourseDialog()
        dialog.exec()

    def search(self):
        # Initialize Dialog
        dialog = SearchDialog.SearchDialog(self)
        dialog.exec()

    def edit(self):
        dialog = EditDialog.EditDialog(self)
        dialog.exec()

    def delete(self):
        dialog = DeleteStudentDialog.DeleteStudentDialog(self)
        dialog.exec()
    
    def delete_multiple(self):
        dialog = DeleteStudentsDialog.DeleteStudentsDialog(self)
        dialog.exec()

    def about(self):
        dialog = AboutDialog.AboutDialog()
        dialog.exec()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
