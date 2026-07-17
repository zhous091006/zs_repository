from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtWidgets import QPushButton

class UiFontIconButton(QPushButton):
    ADD = 0xe813
    CLOSE = 0xe801
    THREE_DOTS = 0xe800
    DELETE = 0xe803
    SETTING = 0xe803
    MESSAGE = 0xe80b
    PLAY = 0xe808
    PAUSE = 0xe805
    RESUME = 0xe80a
    STOP = 0xe806
    CONNECT = 0xe800
    OPEN_FOLDER = 0xe807
    WINDOW_MIN = 0xe802
    WINDOW_MAX = 0xe809
    WINDOW_NORMAL = 0xe804
    LOCATE = 0xe80b

    def __init__(self, icon_code, parent):
        super().__init__(chr(icon_code), parent)
        self.setFixedSize(20, 20)
        self.foot_icon = None

    def set_icon(self, icon_code):
        self.setText(chr(icon_code))
    
    def set_foot_icon(self, icon_code):
        if icon_code:
            self.foot_icon = chr(icon_code)
        else:
            self.foot_icon = icon_code
        self.update()
    
    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        if self.foot_icon:
            painter = QPainter(self)
            font = QFont('fontello')
            font.setPixelSize(4)
            painter.setFont(font)
            painter.setPen(Qt.red)
            painter.drawText(self.rect().adjusted(0, 0, -2, -2), Qt.AlignRight | Qt.AlignBottom, self.foot_icon)
