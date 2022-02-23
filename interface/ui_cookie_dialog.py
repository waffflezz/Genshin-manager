from PyQt5.QtWidgets import QDialog
import dialog


class CookieDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = dialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.setFixedSize(self.size().width(), self.size().height())

        self.ui.okButton.clicked.connect(self.close)
