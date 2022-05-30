from PyQt5.QtWidgets import QDialog
from api_response import is_cookie
from . import dialog


class CookieDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = dialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.setFixedSize(self.size().width(), self.size().height())

        self.ui.label.hide()

        self.ui.okButton.clicked.connect(self.save_cookie)

    @staticmethod
    def get_lt():
        ltoken, ltuid = None, None


        try:
            with open('C:\\ProgramData\\Genshin_manager\\cookie.txt', "r") as f:
                ltoken = f.readline()
                ltuid = f.readline()
        except FileNotFoundError as e:
            print(e)
            with open('C:\\ProgramData\\Genshin_manager\\uid.txt', "w"):
                pass

        return ltoken, ltuid

    def save_cookie(self):
        with open('C:\\ProgramData\\Genshin_manager\\cookie.txt', "w") as f:
            f.write(self.ui.ltokenEdit.text() + "\n")
            f.write(self.ui.ltuidEdit.text() + "\n")

        if not self.ui.ltuidEdit.text() or not self.ui.ltokenEdit.text() or is_cookie() is False:
            self.ui.label.show()
            return

        self.close()
