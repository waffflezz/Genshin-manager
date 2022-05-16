import datetime
import time

from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QPushButton,
    QSizePolicy, QLabel, QFrame,
    QHBoxLayout, QSpacerItem
)
from PyQt5.QtCore import (
    QPropertyAnimation, QEasingCurve, QSize,
    Qt, QThread, pyqtSignal
)
from threads import (
    LoadPrimos, LoadResin, LoadDails,
    LoadExpedition
)

from models import PrimosModel, DailsModel, CharactersModel
from widgets import TestDelegate, DailsDelegate, CharactersDelegate
from error_widget import ErrorMessage

from sys import argv
from api_response import realtime, statistics, is_cookie, set_cookie
from api_response.db_worker import DBaser
from interface.ui_cookie_dialog import CookieDialog
from styles import style_bt_standard
import ui

import pyqtgraph as pg
import numpy as np


def select_menu(get_style):
    select = get_style + "QPushButton { border-right: 7px solid rgb(73, 117, 125); }"
    return select


def deselect_menu(get_style):
    deselect = get_style.replace("QPushButton { border-right: 7px solid rgb(73, 117, 125); }", "")
    return deselect


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        set_cookie()

        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self)

        # Класс управления базой данных
        self.db_manager = DBaser('C:\\ProgramData\\Genshin_manager\\databases\\')
        self.db_manager.make_statistics_base()

        self.stats = statistics.StatisticsGetter("ru-ru")
        self.analyzer = statistics.StatisticsAnalyzer('C:\\ProgramData\\Genshin_manager\\databases\\')
        # self.stats.update_dbs()

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
        self.ui.upd_realtime_button.clicked.connect(self.buttons_events)

        self.ui.stackedWidget.setCurrentWidget(self.ui.page)

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

        # Создаю модель и делегат для героев в экспедиции
        self.chars_model = CharactersModel(self.ui.characters_view)
        self.chars_delegate = CharactersDelegate(self.ui.characters_view)

        # Подключаю к вьюшке примогемы
        self.ui.primos_view.setModel(self.primos_model)
        self.ui.primos_view.setItemDelegate(self.test_delegate)

        # Подключаю к вьюшке резину
        self.ui.resins_view.setModel(self.resin_model)
        self.ui.resins_view.setItemDelegate(self.resin_delegate)

        # Подключаю к вьюшке еждневные штуки
        self.ui.dails_view.setModel(self.daily_model)
        self.ui.dails_view.setItemDelegate(self.daily_delegate)

        # Подключаю к вьющке героев из экспедиции
        self.ui.characters_view.setModel(self.chars_model)
        self.ui.characters_view.setItemDelegate(self.chars_delegate)

        # QThreads для загрузки данных
        self.primos = LoadPrimos(self.stats)
        self.primos.signal.connect(self.primos_model.add_primos)
        self.primos.load_signal.connect(self.loading)

        self.resin = LoadResin(self.stats)
        self.resin.signal.connect(self.resin_model.add_primos)
        self.resin.load_signal.connect(self.loading)

        self.dails = LoadDails(self.stats)
        self.dails.signal.connect(self.daily_model.add_dails)
        self.dails.load_signal.connect(self.loading)

        self.expedition = LoadExpedition()
        self.expedition.notes_signal.connect(self.add_notes)
        self.expedition.characters_signal.connect(self.chars_model.add_characters)
        self.expedition.load_signal.connect(self.loading)

        self.ui.settingsWarning.hide()

        self.cookie_dialog = CookieDialog()
        if is_cookie() is False:
            self.cookie_dialog.show()

        self.ui.stackedWidget.setCurrentWidget(self.ui.main_page)
        self.daily_model.add_dails(self.stats.get_dailys_page())

        self.graph_pen = pg.mkPen(color=(255, 0, 0), width=2)

        axis = pg.DateAxisItem()
        self.ui.prim_graphic_1.setAxisItems({'bottom': axis})
        self.ui.prim_graphic_1.setBackground((199, 227, 232))
        self.ui.prim_graphic_1.setTitle("Primos per month")

        self.ui.prim_graphic_2.setBackground((199, 227, 232))
        self.ui.prim_graphic_2.setTitle("Primos top")

    def buttons_events(self):
        button = self.sender()

        if button.objectName() == "exp_button":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page)
            self.reset_style("exp_button")
            button.setStyleSheet(select_menu(button.styleSheet()))

            if is_cookie() is False:
                self.cookie_dialog.show()
                return
            self.expedition.start()
        elif button.objectName() == "main_menu":
            self.ui.stackedWidget.setCurrentWidget(self.ui.main_page)
            self.reset_style("main_menu")
            button.setStyleSheet(select_menu(button.styleSheet()))

            self.dails.start()
        elif button.objectName() == "primos_button":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)
            self.reset_style("primos_button")
            button.setStyleSheet(select_menu(button.styleSheet()))

            self.ui.prim_graphic_1.clear()
            self.ui.prim_graphic_2.clear()

            self.ui.prim_graphic_1.plot(x=np.array([time.mktime(datetime.date(i[0], i[1], 1).timetuple()) for i in self.analyzer.get_primos_per_month().keys()]),
                                        y=np.array([i for i in self.analyzer.get_primos_per_month().values()]),
                                        pen=self.graph_pen)

            self.ui.prim_graphic_2.plot(x=np.array([i + 1 for i in range(len(self.analyzer.get_primos_top()))]),
                                        y=np.array([i['amount'] for i in self.analyzer.get_primos_top()]),
                                        pen=self.graph_pen)

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
            with open('C:\\ProgramData\\Genshin_manager\\cookie.txt', "w") as f:
                f.write(self.ui.ltoken.text() + "\n")
                f.write(self.ui.ltuid.text() + "\n")

            if not self.ui.ltoken.text() or not self.ui.ltuid.text() or is_cookie() is False:
                self.ui.settingsWarning.show()
        elif button.objectName() == "upd_realtime_button":
            if is_cookie() is False:
                self.cookie_dialog.show()
                return
            self.expedition.start()

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

    def reset_models(self):
        self.primos_model.clear()
        self.resin_model.clear()
        self.daily_model.clear()
        self.chars_model.clear()

    def reset_style(self, widget):
        for button in self.ui.sidebar_menu.findChildren(QPushButton):
            if button.objectName() != widget and button.objectName() != "sidebarButton":
                button.setStyleSheet(deselect_menu(button.styleSheet()))

    def add_notes(self, notes):
        self.ui.info_1.setText(notes['dailik'].replace('\\', '/'))
        self.ui.info_2.setText(notes['reward'])
        self.ui.info_3.setText(notes['bosses'].replace('\\', '/'))
        self.ui.info_4.setText(notes['resin']['amount'].replace('\\', '/')[:-1])
        self.ui.info_5.setText(notes['resin']['time'])
        self.ui.info_6.setText(notes['expedition'].replace('\\', '/'))

    def loading(self, is_load):
        if is_load:
            self.statusBar().showMessage("LOADING")
        else:
            self.statusBar().clearMessage()


if __name__ == '__main__':
    app = QApplication(argv)
    ex = MainWindow()
    ex.show()
    app.exec_()

    exit()
