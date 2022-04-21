from PyQt5.QtWidgets import QDialog
from api_response import cookie_path, is_cookie
from . import dialog


class CookieDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = dialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.setFixedSize(self.size().width(), self.size().height())

        self.ui.label.hide()

        self.ui.okButton.clicked.connect(self.save_cookie)

    def save_cookie(self):
        with open(cookie_path, "w") as f:
            f.write(self.ui.ltokenEdit.text() + "\n")
            f.write(self.ui.ltuidEdit.text() + "\n")

        if not self.ui.ltuidEdit.text() or not self.ui.ltokenEdit.text() or is_cookie() is False:
            self.ui.label.show()
            return

        self.close()
