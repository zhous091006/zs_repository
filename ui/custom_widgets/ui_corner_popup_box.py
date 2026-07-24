import sys
from enum import IntEnum

from PyQt5.QtCore import QPropertyAnimation, QPoint, QTimer, Qt
from PyQt5.QtWidgets import QDesktopWidget, QDialog, QApplication, QLabel, QVBoxLayout, QPushButton, QHBoxLayout


class PopupBoxLevel(IntEnum):
    TEXT = 0
    INFO = 1
    WARNING = 2
    ERROR = 3


class UiCornerPopupBox(QDialog):
    def __init__(self, title: str, text: str, level: PopupBoxLevel, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.desktop = QDesktopWidget()
        self.animation = None
        self.drag_position = QPoint(0, 0)
        self.is_mouse_pressed = False

        self.title: str = title
        self.text: str = text
        self.level: PopupBoxLevel = level

        self.remainTimer = QTimer()
        self.remainTimer.setSingleShot(True)

        self.set_style_sheet()

        self.title_label = QLabel(self)
        self._init_title_color()

        self.close_btn = QPushButton("[×]", self)
        self.close_btn.setFixedHeight(20)

        self.h_layout = QHBoxLayout()
        self.h_layout.setSpacing(5)
        self.h_layout.setContentsMargins(0, 0, 0, 0)
        self.h_layout.addWidget(self.title_label)
        self.h_layout.addStretch(1)
        self.h_layout.addWidget(self.close_btn)

        self.label = QLabel(text, self)
        self.label.setWordWrap(True)

        self.v_layout = QVBoxLayout()
        self.v_layout.setContentsMargins(10, 5, 8, 8)
        self.v_layout.setSpacing(5)
        self.v_layout.addLayout(self.h_layout)
        self.v_layout.addWidget(self.label)
        self.setLayout(self.v_layout)

        self._init_connect()

        self.setMinimumSize(200, 100)
        self.setMaximumWidth(400)
        self.adjustSize()

        self.move((self.desktop.availableGeometry().width() - self.width()), self.desktop.availableGeometry().height())  # 初始化位置到右下角
        self.showAnimation()

    def _init_connect(self):
        self.remainTimer.timeout.connect(self.closeAnimation)
        self.close_btn.clicked.connect(self.quit)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_mouse_pressed = True
            self.drag_position = event.globalPos() - self.geometry().topLeft()
            self.remainTimer.stop()
            event.accept()

    def mouseMoveEvent(self, event):
        # 定义鼠标移动事件
        if event.buttons() == Qt.LeftButton and self.is_mouse_pressed and not self.isMaximized():
            self.move(event.globalPos() - self.drag_position)
            event.accept()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_mouse_pressed = False
            self.remainTimer.start(5000)
        super().mouseReleaseEvent(event)

    def _init_title_color(self):
        if self.level == PopupBoxLevel.TEXT:
            self.title = f"<span style=\" color:rgb(30,30,30); \">{self.title}</span>"
        elif self.level == PopupBoxLevel.INFO:
            self.title = f"<span style=\" color:#0082FF; \">{self.title}</span>"
        elif self.level == PopupBoxLevel.WARNING:
            self.title = f"<span style=\" color:#FF5E00;\">{self.title}</span>"
        elif self.level == PopupBoxLevel.ERROR:
            self.title = f"<span style=\" color:rgb(255,30,30); \">{self.title}</span>"
        self.title_label.setText(self.title)

    def set_style_sheet(self):
        self.setStyleSheet("UiCornerPopupBox{"
                           "border:1px solid #222;"
                           "background:#eee;"
                           "}"
                           "QLabel#Title{"
                           "background:#f00;"
                           "}"
                           "QPushButton{"
                           "background:transparent;"
                           "border:none;"
                           "}"
                           "QPushButton:hover{"
                           "color:#f00;"
                           "}")

    @staticmethod
    def popup(title: str, text: str, level: PopupBoxLevel = PopupBoxLevel.TEXT):
        """
        :param title:
        :param text:
        :param level: PopupBoxLevel.<TEXT/INFO/WARRING/ERROR>
        """
        app = QApplication(sys.argv)
        UiCornerPopupBox(title, text, level).show()
        app.exec_()

    def showAnimation(self):
        """弹出动画"""
        # 显示弹出框动画
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(200)
        self.animation.setStartValue(QPoint(self.x(), self.y()))
        self.animation.setEndValue(QPoint((self.desktop.availableGeometry().width() - self.width()),
                                          (self.desktop.availableGeometry().height() - self.height())))
        self.animation.start()
        self.remainTimer.start(5000)

    def closeAnimation(self):
        """关闭动画"""
        # 弹出框渐隐
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(1000)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()
        # 动画完成后清理
        self.animation.finished.connect(self.quit)

    @staticmethod
    def quit():
        return sys.exit()


if __name__ == '__main__':
    # pass
    UiCornerPopupBox.popup("标题", "内容", PopupBoxLevel.INFO)
