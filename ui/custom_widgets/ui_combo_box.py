from PyQt5.QtCore import QObject, QModelIndex, Qt, QSize, QPoint
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QStyledItemDelegate, QComboBox, QStyleOptionViewItem, QAbstractItemView, QStyleOption, QListView


class UiComboBox(QComboBox):
    def __init__(self, parent: QObject):
        super().__init__(parent)
        delegate = UiComboBoxDelegateStyled(self, self)
        self.setView(QListView(self))
        self.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        # self.view().window().setAttribute(Qt.WA_TranslucentBackground)
        self.setItemDelegate(delegate)

    def add_dict_items(self, items: dict):
        for key, value in items.items():
            self.addItem(key, value)


class UiComboBoxDelegateStyled(QStyledItemDelegate):
    def __init__(self, parent: QObject, cmb: QComboBox):
        super().__init__(parent=parent)
        self.combobox = cmb

    @staticmethod
    def is_separator(index: QModelIndex) -> bool:
        description_role = index.data(Qt.AccessibleDescriptionRole)
        return description_role == "separator"

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        if self.is_separator(index):
            rect = option.rect
            if isinstance(option.widget, QAbstractItemView):
                rect.setWidth(option.widget.viewport().width())
            opt = QStyleOption()
            opt.rect = rect

            # 从样式表取样式，不完善
            # self.combobox.style().drawPrimitive(QStyle.PE_IndicatorToolBarSeparator, opt, painter, self.combobox)

            pt1 = QPoint(rect.left() + 4, rect.top() + int(rect.height() / 2))
            pt2 = QPoint(rect.right() - 4, pt1.y())
            painter.save()
            painter.setPen(QColor("#888"))
            painter.drawLine(pt1, pt2)
            painter.restore()
        else:
            super().paint(painter, option, index)

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        if self.is_separator(index):
            pm = 8
            return QSize(pm, pm)
        return super().sizeHint(option, index)
