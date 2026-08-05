from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QTableWidget

from ui.custom_widgets.ui_abstract_scroll_area_helper import UiAbstractScrollAreaHelper


class UiTableWidget(QTableWidget):
    sig_resized = pyqtSignal(QSize)

    def __init__(self, parent):
        super().__init__(parent=parent)

        self.widget_helper = UiAbstractScrollAreaHelper(self)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        index = self.indexAt(event.pos())
        if not index.isValid():
            self.clearSelection()
            if self.selectionModel() is not None:
                self.selectionModel().clear()
        return super().mousePressEvent(event)
