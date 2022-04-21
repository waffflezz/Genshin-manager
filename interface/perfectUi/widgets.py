from PyQt5.QtCore import (
    QModelIndex, Qt, QRect, QSize, QPoint
)
from PyQt5.QtWidgets import (
    QStyledItemDelegate, QStyleOptionViewItem
)
from PyQt5.QtGui import (
    QColor, QPainter, QFont, QLinearGradient, QBrush, QPixmap
)


class TestDelegate(QStyledItemDelegate):
    def __init__(self, parent=None) -> None:
        super(TestDelegate, self).__init__(parent)

        self.__margin = 5
        self.__font_size = 15
        self.__small_font_size = self.__font_size * 0.8

    def paint(self, painter: QPainter, option: QStyleOptionViewItem,
              index: QModelIndex) -> None:
        _option = QStyleOptionViewItem(option)
        self.initStyleOption(_option, index)
        data = index.data(Qt.DisplayRole)

        origin_rect = QRect(_option.rect)

        palette = _option.palette
        font = QFont(_option.font)
        font.setPointSize(self.__font_size)
        font.setBold(True)

        painter.save()
        painter.setClipping(True)
        painter.setClipRect(origin_rect)

        grad = QLinearGradient(origin_rect.topLeft(), origin_rect.bottomRight())
        grad.setColorAt(0, QColor('#85004B'))
        grad.setColorAt(1, QColor('#4380D3'))

        painter.fillRect(origin_rect, QBrush(grad))

        painter.setPen(palette.shadow().color())
        painter.drawLine(origin_rect.bottomLeft(), origin_rect.bottomRight())
        painter.drawLine(origin_rect.left() + 150, origin_rect.top(),
                         origin_rect.left() + 150, origin_rect.bottom())
        painter.drawLine(origin_rect.left() + 580, origin_rect.top(),
                         origin_rect.left() + 580, origin_rect.bottom())

        painter.setFont(font)
        painter.setPen(palette.text().color())
        painter.drawText(origin_rect.left() + 10, origin_rect.center().y(), f'Кол-во: {data["amount"]}')
        painter.drawText(origin_rect.left() + 590, origin_rect.center().y() - 10, f'Время:')
        painter.drawText(origin_rect.left() + 590, origin_rect.center().y() + 10, f'{data["time"]}')
        painter.drawText(origin_rect.left() + 160, origin_rect.center().y() - 10, f'Получено за:')
        painter.drawText(origin_rect.left() + 160, origin_rect.center().y() + 10, f'{data["reason"]}')

        painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem,
                 index: QModelIndex) -> QSize:
        _option = QStyleOptionViewItem(option)
        self.initStyleOption(_option, index)

        return QSize(135, 80)


class DailsDelegate(QStyledItemDelegate):
    def __init__(self, parent=None) -> None:
        super(DailsDelegate, self).__init__(parent)

        self.__margin = 5
        self.__font_size = 15
        self.__small_font_size = self.__font_size * 0.6

    def paint(self, painter: QPainter, option: QStyleOptionViewItem,
              index: QModelIndex) -> None:
        _option = QStyleOptionViewItem(option)
        self.initStyleOption(_option, index)
        data = index.data(Qt.DisplayRole)

        origin_rect = QRect(_option.rect)

        palette = _option.palette
        font = QFont(_option.font)

        painter.save()
        painter.setClipping(True)
        painter.setClipRect(origin_rect)

        painter.drawLine(origin_rect.bottomLeft(), origin_rect.bottomRight())

        pix = QPixmap()
        pix.loadFromData(data["img"])
        pix = pix.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio,
                         Qt.TransformationMode.SmoothTransformation)
        painter.drawPixmap(QPoint(origin_rect.left(), origin_rect.center().y() - 20), pix)

        font.setBold(False)
        font.setPointSizeF(self.__small_font_size)
        painter.setFont(font)

        painter.drawText(origin_rect.left() + 60, origin_rect.center().y() - 16, f'Название: {data["name"]}')
        painter.drawText(origin_rect.left() + 60, origin_rect.center().y(), f'Кол-во: {data["count"]}')
        painter.drawText(origin_rect.left() + 60, origin_rect.center().y() + 16, f'Дата: {data["date"]}')

        painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem,
                 index: QModelIndex) -> QSize:
        _option = QStyleOptionViewItem(option)
        self.initStyleOption(_option, index)

        return QSize(135, 80)
