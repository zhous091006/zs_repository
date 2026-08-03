from PyQt5.QtCore import QEvent, pyqtSignal, QSize, QTimer, QPoint
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QScrollArea, qApp

from ui.custom_widgets.ui_abstract_scroll_area_helper import UiAbstractScrollAreaHelper


class UiScrollArea(QScrollArea):
    sig_resized = pyqtSignal(QSize)

    def __init__(self, parent):
        super().__init__(parent)

        self.widget_helper = UiAbstractScrollAreaHelper(self)

    @staticmethod
    def __fake_mouse_move():
        pos = QCursor.pos()
        # slightly move the mouse
        QCursor.setPos(pos + QPoint(0, 1))
        # ensure that the application correctly processes the mouse movement
        qApp.processEvents()
        # restore the previous position
        QCursor.setPos(pos)

    def viewportEvent(self, event: QEvent) -> bool:
        if event.type() == QEvent.Wheel:
            # let the viewport handle the event correctly, *then* move the mouse
            QTimer.singleShot(0, self.__fake_mouse_move)
        return super().viewportEvent(event)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.sig_resized.emit(self.size())
