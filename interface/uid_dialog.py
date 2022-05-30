from PyQt5.QtWidgets import QDialog
from . import uid_dialog_c


class UidDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = uid_dialog_c.Ui_Dialog()
        self.ui.setupUi(self)
        self.setFixedSize(self.size().width(), self.size().height())

        self.ui.uidButton.clicked.connect(self.save_uid)

    @staticmethod
    def get_uid():
        uid = None

        try:
            with open('C:\\ProgramData\\Genshin_manager\\uid.txt', "r") as f:
                uid = f.readline()
        except FileNotFoundError as e:
            print(e)
            with open('C:\\ProgramData\\Genshin_manager\\uid.txt', "w"):
                pass

        return uid

    def save_uid(self):
        with open('C:\\ProgramData\\Genshin_manager\\uid.txt', "w") as f:
            f.write(self.ui.uidEdit.text() + "\n")

        self.close()
