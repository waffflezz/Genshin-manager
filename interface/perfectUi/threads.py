from PyQt5.QtCore import QThread, pyqtSignal
from api_response import realtime


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

    def __init__(self, parent=None):
        super(LoadExpedition, self).__init__(parent)

    def run(self):
        self.load_signal.emit(True)

        uid = 705359736
        rus = 'ru-ru'

        notes = realtime.grab_notes(uid, rus)

        self.notes_signal.emit(notes['info'])
        self.characters_signal.emit(notes['characters'])

        self.load_signal.emit(False)
