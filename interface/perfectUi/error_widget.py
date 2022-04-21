from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QSize


class ErrorMessage(QMessageBox):
    def __init__(self):
        super(ErrorMessage, self).__init__()
        self.setMinimumSize(200, 90)

    def show_message(self, err_str):
        self.setText(f"Error: {err_str}")
        self.exec()
