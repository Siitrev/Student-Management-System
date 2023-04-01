from PyQt6.QtWidgets import QMessageBox


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
