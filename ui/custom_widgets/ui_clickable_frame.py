from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QFrame


class UiClickableFrame(QFrame):
    sig_clicked = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.__is_mouse_pressed = False

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton:
            self.__is_mouse_pressed = True
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.__is_mouse_pressed:
            self.sig_clicked.emit()
        super().mouseReleaseEvent(event)
        self.__is_mouse_pressed = False
