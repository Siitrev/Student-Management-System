from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QWidget,
    QLineEdit,
    QPushButton,
    QMainWindow,
    QTableWidget
)
from PyQt6.QtGui import QAction, QIcon
import sys


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu_item = self.menuBar().addMenu("&File")
        about_menu_item = self.menuBar().addMenu("&Help")

        add_student_action = QAction("Add Student", self)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        about_menu_item.addAction(about_action)
        
        # tool_bar = self.addToolBar("Toolbar")
        # plus_icon = QIcon("plus.webp")
        # tool_bar.addAction(icon=plus_icon,text="Add Student")


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
