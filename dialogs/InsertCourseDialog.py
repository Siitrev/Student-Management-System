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


class InsertCourseDialog(QDialog):
    def __init__(self, main_window: QMainWindow) -> None:
        super().__init__()
        self.main_window = main_window
