from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QPushButton,
    QSizePolicy, QLabel, QFrame,
    QHBoxLayout, QSpacerItem
)
from PyQt5.QtCore import (
    QPropertyAnimation, QEasingCurve, QSize,
    Qt, QThread, pyqtSignal
)

from models import PrimosModel, DailsModel
from widgets import TestDelegate, DailsDelegate
from error_widget import ErrorMessage
from threads import LoadPrimos, LoadResin, LoadDails, UpdateDb

from PyQt5.QtGui import QPixmap
from sys import argv
from api_response import realtime, statistics, is_cookie, cookie_path
from api_response.db_worker import DBaser
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

        # Класс управления базой данных
        self.db_manager = DBaser('C:\\Users\\leva\\PycharmProjects\\Genshin_manager\\databases')
        # self.db_manager.make_statistics_base()

        self.stats = statistics.StatisticsGetter("ru-ru")

        # Тред который обновляет базы данных
        self.dbs_updater = UpdateDb(self.stats)
        # self.dbs_updater.start()

        self.err_message = ErrorMessage()

        self.sidebar_animation = QPropertyAnimation(self.ui.sidebar_menu, b"minimumWidth")

        self.ui.sidebarButton.setMinimumSize(QSize(0, 60))
        self.ui.sidebarButton.clicked.connect(lambda: self.toggle_menu(200))

        self.add_new_menu("MAIN MENU", "main_menu", "url(:/16x16/icons/16x16/cil-code.png)")
        self.add_new_menu("TRAVELER'S\nDIARIES", "exp_button", "url(:/16x16/icons/16x16/cil-code.png)")
        self.add_new_menu("PRIMOS\nSTATS", "primos_button", "url(:/16x16/icons/16x16/cil-code.png)")
        self.add_new_menu("RESIN\nSTATS", "resin_button", "url(:/16x16/icons/16x16/cil-code.png)")

        self.ui.settingsButton.clicked.connect(self.buttons_events)
        self.ui.saveButton.clicked.connect(self.buttons_events)

        self.ui.stackedWidget.setCurrentWidget(self.ui.page)

        self.notes = LoadNotes()
        self.notes.signal.connect(self.add_wishes)
        self.notes.signal.connect(self.update_wishes)
        self.notes.load_signal.connect(self.loading)


        # Создаю модель и делегат для примогемов
        self.primos_model = PrimosModel(self.ui.primos_view)
        self.primos_model.err_signal.connect(self.err_message.show_message)
        self.test_delegate = TestDelegate(self.ui.primos_view)

        # Создаю модель и делегат для резины
        self.resin_model = PrimosModel(self.ui.resins_view)
        self.resin_model.err_signal.connect(self.err_message.show_message)
        self.resin_delegate = TestDelegate(self.ui.resins_view)

        # Создаю модель и делегат для ежедневных штук
        self.daily_model = DailsModel(self.ui.dails_view)
        self.daily_model.err_signal.connect(self.err_message.show_message)
        self.daily_delegate = DailsDelegate(self.ui.dails_view)

        # Подключаю к вьюшке примогемы
        self.ui.primos_view.setModel(self.primos_model)
        self.ui.primos_view.setItemDelegate(self.test_delegate)

        # Подключаю к вьюшке резину
        self.ui.resins_view.setModel(self.resin_model)
        self.ui.resins_view.setItemDelegate(self.resin_delegate)

        # Подключаю к вьюшке еждневные штуки
        self.ui.dails_view.setModel(self.daily_model)
        self.ui.dails_view.setItemDelegate(self.daily_delegate)

        self.primos = LoadPrimos(self.stats)
        self.primos.signal.connect(self.primos_model.add_primos)
        self.primos.load_signal.connect(self.loading)

        self.resin = LoadResin(self.stats)
        self.resin.signal.connect(self.resin_model.add_primos)
        self.resin.load_signal.connect(self.loading)

        self.dails = LoadDails(self.stats)
        self.dails.signal.connect(self.daily_model.add_dails)
        self.dails.load_signal.connect(self.loading)

        self.ui.settingsWarning.hide()

        self.cookie_dialog = CookieDialog()
        if is_cookie() is False:
            self.cookie_dialog.show()

        self.ui.stackedWidget.setCurrentWidget(self.ui.main_page)
        self.daily_model.add_dails(self.stats.get_dailys_page())

    def buttons_events(self):
        button = self.sender()

        if button.objectName() == "exp_button":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page)
            self.reset_style("exp_button")
            button.setStyleSheet(select_menu(button.styleSheet()))

            if is_cookie() is False:
                self.cookie_dialog.show()
                return
            self.notes.start()
        elif button.objectName() == "main_menu":
            self.ui.stackedWidget.setCurrentWidget(self.ui.main_page)
            self.reset_style("main_menu")
            button.setStyleSheet(select_menu(button.styleSheet()))

            self.dails.start()
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
        elif button.objectName() == "settingsButton":
            self.ui.stackedWidget.setCurrentWidget(self.ui.settings_page)
            self.reset_style("settingsButton")
            button.setStyleSheet(select_menu(button.styleSheet()))
        elif button.objectName() == "saveButton":
            with open(cookie_path, "w") as f:
                f.write(self.ui.ltoken.text() + "\n")
                f.write(self.ui.ltuid.text() + "\n")

            if not self.ui.ltoken.text() or not self.ui.ltuid.text() or is_cookie() is False:
                self.ui.settingsWarning.show()

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

    # TODO: передлать в модель с методом прогрузки в методе
    # TODO: добавить окошко с кнопкой, в который вводится uid и печатаются герои в экспедиции
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

    # TODO: сделать отдельным методом в моделе вишесев
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

    def loading(self, is_load):
        if is_load:
            self.statusBar().showMessage("LOADING")
        else:
            self.statusBar().clearMessage()


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


if __name__ == '__main__':
    app = QApplication(argv)
    ex = MainWindow()
    ex.show()
    app.exec_()

    exit()
