from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QWidget

from lib.lib_unicode import LibUnicode


class UiPushButton(QPushButton):
    def __init__(self, text, parent):
        super().__init__(text, parent)
        self.border_shadow_effect_enable = True
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(24)

    def set_icon(self, icon: QIcon, size: QSize):
        self.setIcon(icon)
        self.setIconSize(size)

    @staticmethod
    def create_icon_button(text: [str, LibUnicode], parent: QWidget, object_name: str, width: int = None, height: int = None) -> "UiPushButton":
        if isinstance(text, LibUnicode):
            text = text.value
        btn = UiPushButton(text, parent)
        btn.setObjectName(object_name)
        btn.border_shadow_effect_enable = False
        if width is not None:
            btn.setFixedWidth(width)
        if height is not None:
            btn.setFixedHeight(height)
        return btn
