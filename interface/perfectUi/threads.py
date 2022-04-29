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


class LoadExpedition(QThread):
    notes_signal = pyqtSignal(object)
    characters_signal = pyqtSignal(object)
    load_signal = pyqtSignal(bool)

    def __init__(self, exp, parent=None):
        super(LoadExpedition, self).__init__(parent)
        self.exp = exp

    def run(self):
        self.load_signal.emit(True)

        self.notes_signal.emit(self.exp['info'])
        self.characters_signal.emit(self.exp['characters'])

        self.load_signal.emit(False)
