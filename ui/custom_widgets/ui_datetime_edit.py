from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QDateTimeEdit

# from ui.lib.ui_func import ui_func_t


class UiDateTimeEdit(QDateTimeEdit):
    def __init__(self, *args):
        super().__init__(*args)
        self.setFixedHeight(24)

    def enterEvent(self, event: QEvent) -> None:
        # if self.isEnabled() and not self.isReadOnly():
            # ui_func_t.set_border_shadow_effect(self, color=QColor("#888"), radius=10)
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        if not self.hasFocus():
            self.setGraphicsEffect(None)
        super().leaveEvent(event)

    def focusInEvent(self, event) -> None:
        # if self.isEnabled() and not self.isReadOnly():
            # ui_func_t.set_border_shadow_effect(self, color=QColor("#888"), radius=10)
        super().focusInEvent(event)

    def focusOutEvent(self, event) -> None:
        self.setGraphicsEffect(None)
        super().focusOutEvent(event)
