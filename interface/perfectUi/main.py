from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QSizePolicy, QLabel, QFrame
from PyQt5.QtWidgets import QHBoxLayout, QSpacerItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QSize, Qt, QThread, pyqtSignal
from sys import argv
from api_response import realtime
from interface.ui_cookie_dialog import CookieDialog
from styles import style_bt_standard
import ui


def select_menu(get_style):
    select = get_style + "QPushButton { border-right: 7px solid rgb(44, 49, 60); }"
    return select


def deselect_menu(get_style):
    deselect = get_style.replace("QPushButton { border-right: 7px solid rgb(44, 49, 60); }", "")
    return deselect


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self)

        self.sidebar_animation = QPropertyAnimation(self.ui.sidebar_menu, b"minimumWidth")

        self.ui.sidebarButton.setMinimumSize(QSize(0, 60))
        self.ui.sidebarButton.clicked.connect(lambda: self.toggle_menu(200))

        self.add_new_menu("HOME", "home_button", "url(:/16x16/icons/16x16/cil-code.png)")
        self.add_new_menu("SAMOLET", "samolet_button", "url(:/16x16/icons/16x16/cil-airplane-mode.png)")

        self.ui.stackedWidget.setCurrentWidget(self.ui.page)

        self.test = LoadNotes()
        self.test.signal.connect(self.add_wishes)
        self.test.signal.connect(self.update_wishes)

        self.cookie_dialog = CookieDialog()
        self.cookie_dialog.show()

    def buttons_events(self):
        button = self.sender()

        if button.objectName() == "home_button":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page)
            self.reset_style("home_button")
            button.setStyleSheet(select_menu(button.styleSheet()))

            self.test.start()
        if button.objectName() == "samolet_button":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)
            self.reset_style("samolet_button")
            button.setStyleSheet(select_menu(button.styleSheet()))

    def toggle_menu(self, max_width):
        width = self.ui.sidebar_menu.width()
        max_extend = max_width
        standard = 60

        if width == standard:
            width_extended = max_extend
        else:
            width_extended = standard

        self.sidebar_animation.setDuration(300)
        self.sidebar_animation.setStartValue(width)
        self.sidebar_animation.setEndValue(width_extended)
        self.sidebar_animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.sidebar_animation.start()

    def add_new_menu(self, name, obj_name, icon):
        button = QPushButton(self)
        button.setObjectName(obj_name)
        size_policy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        size_policy3.setHorizontalStretch(0)
        size_policy3.setVerticalStretch(0)
        size_policy3.setHeightForWidth(button.sizePolicy().hasHeightForWidth())
        button.setSizePolicy(size_policy3)
        button.setMinimumSize(QSize(0, 60))
        button.setLayoutDirection(Qt.LeftToRight)
        button.setStyleSheet(style_bt_standard.replace('ICON_REPLACE', icon))
        button.setText(name)
        button.setToolTip(name)
        button.clicked.connect(self.buttons_events)
        self.ui.verticalLayout_4.addWidget(button)

    def reset_style(self, widget):
        for button in self.ui.sidebar_menu.findChildren(QPushButton):
            if button.objectName() != widget and button.objectName() != "sidebarButton":
                button.setStyleSheet(deselect_menu(button.styleSheet()))

    def add_wishes(self, notes):
        if len(self.ui.scrollAreaWidgetContents.children()) > 1:
            return

        expedition_info = QLabel(self.ui.scrollAreaWidgetContents)
        expedition_info.setObjectName('wishes_info')
        expedition_info.setText("".join(i + "\n" for i in notes[:5]))
        self.ui.scrollAreaLayout.addWidget(expedition_info)

        for i, note in enumerate(notes[5:]):
            frame = QFrame(self.ui.scrollAreaWidgetContents)

            pix = QPixmap()
            pix.loadFromData(b"".join(note[:-1]))
            hero_pix = QLabel(frame)
            hero_pix.setObjectName(f"hero_pix_{i}")
            hero_pix.setPixmap(pix)

            expedition_time = QLabel(frame)
            expedition_time.setObjectName(f"heroes_time_{i}")
            expedition_time.setText(note[-1])

            v_layout = QHBoxLayout(frame)
            v_layout.addWidget(hero_pix)
            v_layout.addWidget(expedition_time)

            self.ui.scrollAreaLayout.addWidget(frame)
            spacer_item = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            v_layout.addItem(spacer_item)

        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.ui.scrollAreaLayout.addItem(spacer_item)
        self.ui.scrollAreaWidgetContents.show()

    def update_wishes(self, notes):
        expedition_info = self.ui.scrollAreaWidgetContents.findChild(QLabel, "wishes_info")
        expedition_info.setText("".join(i + "\n" for i in notes[:5]))

        for i, note in enumerate(notes[5:]):
            pix = QPixmap()
            pix.loadFromData(b"".join(note[:-1]))
            hero_pix = self.ui.scrollAreaWidgetContents.findChild(QLabel, f"hero_pix_{i}")
            hero_pix.setPixmap(pix)

            expedition_time = self.ui.scrollAreaWidgetContents.findChild(QLabel, f"heroes_time_{i}")
            expedition_time.setText(note[-1])


class LoadNotes(QThread):
    signal = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__()

    def run(self):
        uid = 705359736
        rus = 'ru-ru'
        notes = realtime.grab_notes(uid, rus)
        self.signal.emit(notes)


if __name__ == '__main__':
    app = QApplication(argv)
    ex = MainWindow()
    ex.show()
    app.exec_()
    exit()
