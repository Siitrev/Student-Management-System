from PyQt6.QtWidgets import (
    QDialog,
    QGridLayout,
    QLabel,
    QPushButton,
    QMessageBox,
    QMainWindow,
)
from PyQt6.QtCore import Qt
from utils.DatabaseConnection import DatabaseConnection


class DeleteStudentsDialog(QDialog):
    def __init__(self, main_window: QMainWindow) -> None:
        super().__init__()
        self.setFixedHeight(100)
        self.setFixedWidth(300)
        self.main_window = main_window
        grid = QGridLayout()

        # Take current students id
        indexes = main_window.table.selectedIndexes()
        self.students_ids = set()
        for i in indexes:
            self.students_ids.add(main_window.table.item(i.row(), 0).text())    

        # Create label
        info_label = QLabel("Are you sure you want to delete this records?")

        # Create buttons
        confirm_button = QPushButton("Yes")
        confirm_button.clicked.connect(self.delete)

        dismiss_button = QPushButton("No")
        dismiss_button.clicked.connect(self.close)

        # Add widgets to layout
        grid.addWidget(info_label, 0, 0, 1, 0, Qt.AlignmentFlag.AlignCenter)

        grid.addWidget(confirm_button, 1, 0)
        grid.addWidget(dismiss_button, 1, 1)

        self.setLayout(grid)

    def delete(self):
        # Delete row from db
        with DatabaseConnection().connect() as db:
            for i in self.students_ids:
                cur = db.cursor()
                cur.execute(f"DELETE FROM students WHERE id = {i}")
                db.commit()
                cur.close()
        self.main_window.load_data()
        self.close()

        # Show confirmation message
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The records were deleted successfully!")
        confirmation_widget.exec()
