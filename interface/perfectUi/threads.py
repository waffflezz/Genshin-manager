from PyQt5.QtCore import QThread, pyqtSignal


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


class LoadDails(QThread):
    signal = pyqtSignal(object)
    load_signal = pyqtSignal(bool)

    def __init__(self, stats, parent=None):
        super().__init__()
        self.stats = stats

    def run(self):
        self.load_signal.emit(True)

        self.signal.emit(self.stats.get_dailys_page(is_pic=True))

        self.load_signal.emit(False)


class UpdateDb(QThread):
    load_signal = pyqtSignal(bool)

    def __init__(self, stats, parent=None):
        super(UpdateDb, self).__init__()
        self.stats = stats

    def run(self) -> None:
        self.load_signal.emit(True)

        self.stats.update_dbs()

        self.load_signal.emit(False)

