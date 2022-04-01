from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QSizePolicy, QLabel, QFrame
from PyQt5.QtWidgets import QHBoxLayout, QSpacerItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QSize, Qt, QThread, pyqtSignal
from sys import argv
from api_response import realtime, statistics
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

        self.add_new_menu("TRAVELER'S\nDIARIES", "exp_button", "url(:/16x16/icons/16x16/cil-code.png)")
        self.add_new_menu("PRIMOS\nSTATS", "primos_button", "url(:/16x16/icons/16x16/cil-code.png)")
        self.add_new_menu("RESIN\nSTATS", "resin_button", "url(:/16x16/icons/16x16/cil-code.png)")

        self.ui.stackedWidget.setCurrentWidget(self.ui.page)

        self.notes = LoadNotes()
        self.notes.signal.connect(self.add_wishes)
        self.notes.signal.connect(self.update_wishes)
        self.notes.load_signal.connect(self.loading)

        self.stats = statistics.StatisticsGetter("ru-ru")

        self.primos = LoadPrimos(self.stats)
        self.primos.signal.connect(self.add_primos)
        self.primos.load_signal.connect(self.loading)

        self.resin = LoadResin(self.stats)
        self.resin.signal.connect(self.add_resins)
        self.resin.load_signal.connect(self.loading)

        self.load_label = QLabel(self.ui.mainbody)
        self.load_label.setText("Загрузка")
        self.load_label.setObjectName("load_label")
        self.ui.verticalLayout_3.addWidget(self.load_label)
        self.load_label.hide()

        self.cookie_dialog = CookieDialog()
        self.cookie_dialog.show()

    # repeat code, fix it in future
    def add_primos(self, primos):
        for prim in primos:
            primos_info = QLabel(self.ui.scrollAreaWidgetContents_2)
            primos_text = ""
            for key, value in prim.items():
                primos_text += f"{key}: {value}\n"

            primos_info.setText(primos_text)

            self.ui.verticalLayout_8.addWidget(primos_info)

        self.ui.scrollAreaWidgetContents_2.show()

    def add_resins(self, resins):
        for resin in resins:
            resin_info = QLabel(self.ui.scrollAreaWidgetContents_3)
            resin_text = ""
            for key, value in resin.items():
                resin_text += f"{key}: {value}\n"

            resin_info.setText(resin_text)

            self.ui.verticalLayout_9.addWidget(resin_info)

        self.ui.scrollAreaWidgetContents_3.show()

    def buttons_events(self):
        button = self.sender()

        if button.objectName() == "exp_button":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page)
            self.reset_style("exp_button")
            button.setStyleSheet(select_menu(button.styleSheet()))

            self.notes.start()
        elif button.objectName() == "primos_button":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)
            self.reset_style("primos_button")
            button.setStyleSheet(select_menu(button.styleSheet()))

            self.primos.start()
        elif button.objectName() == "resin_button":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_5)
            self.reset_style("resin_button")
            button.setStyleSheet(select_menu(button.styleSheet()))

            self.resin.start()

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

        update_button = QPushButton(self.ui.scrollAreaWidgetContents)
        update_button.setObjectName("update_button")
        update_button.setText("Обновить")
        update_button.clicked.connect(self.notes.start)
        self.ui.scrollAreaLayout.addWidget(update_button)

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

    # QStatusBar
    def loading(self, is_load):
        if is_load:
            self.load_label.show()
        else:
            self.load_label.hide()


class LoadNotes(QThread):
    signal = pyqtSignal(list)
    load_signal = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__()

    def run(self):
        self.load_signal.emit(True)
        uid = 705359736
        rus = 'ru-ru'
        notes = realtime.grab_notes(uid, rus)
        self.signal.emit(notes)
        self.load_signal.emit(False)


class LoadPrimos(QThread):
    signal = pyqtSignal(object)
    load_signal = pyqtSignal(bool)

    def __init__(self, stats, parent=None):
        super().__init__()
        self.stats = stats

    def run(self):
        self.load_signal.emit(True)

        self.signal.emit(self.stats.get_next_page('primos'))

        self.load_signal.emit(False)


class LoadResin(QThread):
    signal = pyqtSignal(object)
    load_signal = pyqtSignal(bool)

    def __init__(self, stats, parent=None):
        super().__init__()
        self.stats = stats

    def run(self):
        self.load_signal.emit(True)

        self.signal.emit(self.stats.get_next_page('resin'))

        self.load_signal.emit(False)


if __name__ == '__main__':
    app = QApplication(argv)
    ex = MainWindow()
    ex.show()
    app.exec_()
    exit()
