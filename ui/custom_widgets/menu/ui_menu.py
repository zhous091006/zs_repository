from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMenu, QGraphicsDropShadowEffect


class UiMenu(QMenu):
    def __init__(self, *args):
        super().__init__(*args)
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.setWindowFlag(Qt.NoDropShadowWindowHint, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.set_shadow_style(x_offset=2, y_offset=2, color=QColor("#ccc"), blur_radius=8)

    def sizeHint(self) -> QSize:
        return super().sizeHint() + QSize(4, 4)

    def set_shadow_style(self, x_offset: int, y_offset: int, color: QColor, blur_radius: int) -> None:
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setOffset(x_offset, y_offset)
        shadow.setColor(color)
        shadow.setBlurRadius(blur_radius)

        self.setGraphicsEffect(shadow)
