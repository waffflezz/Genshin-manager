from PyQt5.QtCore import (
    QModelIndex, Qt, QRect, QSize, QPoint, QRectF
)
from PyQt5.QtWidgets import (
    QStyledItemDelegate, QStyleOptionViewItem
)
from PyQt5.QtGui import (
    QColor, QPainter, QFont, QLinearGradient, QBrush, QPixmap, QFontMetrics
)


class TestDelegate(QStyledItemDelegate):
    def __init__(self, parent=None) -> None:
        super(TestDelegate, self).__init__(parent)

        self.__margin = 5
        self.__font_size = 9
        self.__small_font_size = self.__font_size * 0.6

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

        painter.setBrush(QColor(199, 227, 232))
        painter.drawRect(origin_rect)

        painter.setPen(palette.shadow().color())
        painter.drawLine(origin_rect.bottomLeft(), origin_rect.bottomRight())
        painter.drawLine(origin_rect.left() + 97, origin_rect.top(),
                         origin_rect.left() + 97, origin_rect.bottom())
        painter.drawLine(origin_rect.left() + 394, origin_rect.top(),
                         origin_rect.left() + 394, origin_rect.bottom())

        painter.setFont(font)
        painter.setPen(palette.text().color())
        painter.drawText(origin_rect.left() + 30, origin_rect.center().y(), f'{data["amount"]}')
        painter.drawText(origin_rect.left() + 100, origin_rect.center().y(), f'{data["reason"]}')
        date, time = data["time"].split()
        painter.drawText(origin_rect.left() + 398, origin_rect.center().y(), date)
        painter.drawText(origin_rect.left() + 398, origin_rect.center().y() + 16, time)

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


# TODO: Доделать делегат
class CharactersDelegate(QStyledItemDelegate):
    def __init__(self, parent=None) -> None:
        super(CharactersDelegate, self).__init__(parent)

        self.__margin = 10
        self.__font_size = 10
        self.__small_font_size = self.__font_size * 0.8

    def paint(self, painter: QPainter, option: QStyleOptionViewItem,
              index: QModelIndex) -> None:
        _option = QStyleOptionViewItem(option)
        self.initStyleOption(_option, index)
        data = index.data(Qt.DisplayRole)

        origin_rect = QRect(_option.rect)
        content_rect = self._contentRectAdjusted(_option)

        palette = _option.palette
        font = QFont(_option.font)
        font.setPointSize(self.__font_size)
        font.setBold(True)

        painter.save()
        painter.setClipping(True)
        painter.setClipRect(origin_rect)

        painter.setRenderHint(painter.Antialiasing)
        painter.setBrush(QColor(199, 227, 232))
        painter.drawRoundedRect(content_rect, 15, 15)

        painter.setBrush(QColor(120, 193, 207))
        painter.drawLine(origin_rect.left() + 36, origin_rect.bottom(),
                         origin_rect.right() - 36, origin_rect.bottom())

        pix = QPixmap()
        pix.loadFromData(data['img'])
        pix = pix.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio,
                         Qt.TransformationMode.SmoothTransformation)
        painter.drawPixmap(content_rect.topLeft(), pix)

        painter.setFont(font)
        painter.setPen(palette.text().color())

        title_text, title_rect = self._sizes(font, data, _option)
        painter.drawText(
            title_rect.translated(content_rect.center()),
            title_text
        )

        painter.restore()

    def _textBox(self, font: QFont, data: str) -> QRectF:
        dy = font.pointSize() + self.__margin
        return QRectF(QFontMetrics(font).boundingRect(data).adjusted(0, dy, 0, dy))

    def _contentRectAdjusted(self, option: QStyleOptionViewItem) -> QRectF:
        return QRectF(option.rect).adjusted(
            self.__margin * 2, self.__margin,
            -self.__margin * 2, -self.__margin
        )

    def _sizes(self, font: QFont, data,
               option: QStyleOptionViewItem):
        _text = f'{data["time"]}'
        _text_rect = self._textBox(font, _text)
        _content_rect = self._contentRectAdjusted(option)
        if (dx := _content_rect.width() - _text_rect.width()) > 0:
            _text_rect.adjust(0, 0, dx, 0)
        return _text, _text_rect

    def sizeHint(self, option: QStyleOptionViewItem,
                 index: QModelIndex) -> QSize:
        _option = QStyleOptionViewItem(option)
        self.initStyleOption(_option, index)

        return QSize(135, 130)
