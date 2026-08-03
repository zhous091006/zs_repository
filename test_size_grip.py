from ctypes.wintypes import MSG
from typing import Tuple, Union, Dict

from PyQt5 import sip
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QRect, QMargins, QByteArray, QSize
from PyQt5.QtGui import QMouseEvent, QColor, QPaintEvent, QMovie, QPainter, QCursor, QResizeEvent, QShowEvent, QFontDatabase
from PyQt5.QtWidgets import QDialog, QFrame, QVBoxLayout, QLabel, QHBoxLayout, QSizePolicy, QGraphicsDropShadowEffect, QApplication, qApp, QPushButton
from win32con import WM_NCACTIVATE

from lib.lib_type import LIB_RESOURCE_DIR
from ui.custom_widgets.ui_size_grip import UiSizeGrip
from ui.custom_widgets.ui_window_tools import UiWindowTopRightTool

import os, sys, time

class TestWindow(QDialog):
    sig_window_max_normal_state_changed = pyqtSignal()
    sig_native_alert = pyqtSignal(bool)

    normal_margins = QMargins(4, 4, 4, 4)

    def __init__(self, title, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint
                            | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setContentsMargins(self.normal_margins.left(), self.normal_margins.top(),
                                self.normal_margins.right(), self.normal_margins.bottom())
        # self.setStyleSheet("background-color: #f0f0f0;")

        # 拖动坐标计算
        self.__drag_position = QPoint(0, 0)
        self.__record_geometry: QRect = QRect(0, 0, 0, 0)
        self.__is_mouse_pressed = False

        # 等待动画，暂时不实现
        self.__being_waiting_state = False
        self.__waiting_display = None

        # 主布局与中心布局
        self.__main_layout = QVBoxLayout()
        self.__central_layout = QVBoxLayout()

        # 中心窗口
        self.__central_widget = QFrame(self)
        self.__central_widget.setObjectName("CentralWidget")
        self.__central_widget.setMouseTracking(True)
        
        # 标题栏
        self.title_bar = UiDialogTitleBar("title", self)
        self.title_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # 主题窗口
        self.body_widget = QFrame(self)
        self.body_widget.setObjectName("BodyWidget")
        self.body_widget.setCursor(Qt.ArrowCursor)
        # 设置背景颜色
        self.body_widget.setAttribute(Qt.WA_StyledBackground, True)
        self.body_widget.setStyleSheet("background-color: brown")
        # 添加内容
        self.wait_btn = QPushButton("[×]", self)
        self.wait_btn.setFixedHeight(30)
        self.wait_btn.setFixedWidth(30)
        self.wait_btn.clicked.connect(self.show_wait)
        # 添加body_widget布局
        self.__body_layout = QVBoxLayout()
        self.__body_layout.addWidget(self.wait_btn)
        self.body_widget.setLayout(self.__body_layout)

        # 工具按钮
        self.top_right_tool = UiWindowTopRightTool(self)
        self.top_right_tool.set_icon_size(24, 24)

        # 拖拽控件
        self.is_size_grip_enabled = False
        self._size_grip_widget_dict: Dict[Qt.Edges, UiSizeGrip] = {}
        self.set_size_grip_enabled(True)

        self._init_central_ui()
        self._init_layout()
        self._init_shadow_effect()
        self._init_connect()

        self.resize(100, 100)


    def _init_central_ui(self):
        self.__main_layout = QVBoxLayout()
        self.__main_layout.setContentsMargins(0, 0, 0, 0)
        self.__main_layout.addWidget(self.__central_widget)
        self.setLayout(self.__main_layout)

    def _init_layout(self):
        self.__central_layout.setContentsMargins(0, 0, 0, 0)
        self.__central_layout.setSpacing(0)
        self.__central_layout.addWidget(self.title_bar)
        self.__central_layout.addWidget(self.body_widget)
        self.__central_widget.setLayout(self.__central_layout)

    def _init_connect(self):
        self.top_right_tool.sig_close.connect(self.close_window)
        self.top_right_tool.sig_show_minimized.connect(self.show_min_window)
        self.top_right_tool.sig_switch_show_max_normal.connect(self.switch_max_normal_window)
        self.top_right_tool.sig_resized.connect(self._adjust_window_top_right_tool_geometry)
        self.sig_window_max_normal_state_changed.connect(self.top_right_tool.on_window_max_normal_state_changed)

        self.title_bar.sig_switch_show_max_normal.connect(self.switch_max_normal_window)
        self.sig_native_alert.connect(self.__deal_native_alert)

    def __deal_native_alert(self, state: bool):
        self.__central_widget.setProperty("alert", state)
        self.__central_widget.style().unpolish(self.__central_widget)
        self.__central_widget.style().polish(self.__central_widget)
        self.title_bar.setProperty("alert", state)
        self.title_bar.style().unpolish(self.title_bar)
        self.title_bar.style().polish(self.title_bar)

    def set_size_grip_enabled(self, enable: bool):
        if self.is_size_grip_enabled != enable:
            self.is_size_grip_enabled = enable
            if self.is_size_grip_enabled:
                margin = 4
                self._size_grip_widget_dict[Qt.LeftEdge] = UiSizeGrip(Qt.LeftEdge, self)
                self._size_grip_widget_dict[Qt.LeftEdge].setFixedWidth(margin)
                self._size_grip_widget_dict[Qt.TopEdge] = UiSizeGrip(Qt.TopEdge, self)
                self._size_grip_widget_dict[Qt.TopEdge].setFixedHeight(margin)
                self._size_grip_widget_dict[Qt.RightEdge] = UiSizeGrip(Qt.RightEdge, self)
                self._size_grip_widget_dict[Qt.RightEdge].setFixedWidth(margin)
                self._size_grip_widget_dict[Qt.BottomEdge] = UiSizeGrip(Qt.BottomEdge, self)
                self._size_grip_widget_dict[Qt.BottomEdge].setFixedHeight(margin)
                self._size_grip_widget_dict[Qt.TopEdge | Qt.LeftEdge] = UiSizeGrip(Qt.TopEdge | Qt.LeftEdge, self)
                self._size_grip_widget_dict[Qt.TopEdge | Qt.LeftEdge].setFixedSize(margin, margin)
                self._size_grip_widget_dict[Qt.TopEdge | Qt.RightEdge] = UiSizeGrip(Qt.TopEdge | Qt.RightEdge, self)
                self._size_grip_widget_dict[Qt.TopEdge | Qt.RightEdge].setFixedSize(margin, margin)
                self._size_grip_widget_dict[Qt.BottomEdge | Qt.LeftEdge] = UiSizeGrip(Qt.BottomEdge | Qt.LeftEdge, self)
                self._size_grip_widget_dict[Qt.BottomEdge | Qt.LeftEdge].setFixedSize(margin, margin)
                self._size_grip_widget_dict[Qt.BottomEdge | Qt.RightEdge] = UiSizeGrip(Qt.BottomEdge | Qt.RightEdge, self)
                self._size_grip_widget_dict[Qt.BottomEdge | Qt.RightEdge].setFixedSize(margin, margin)
            else:
                for size_grip in self._size_grip_widget_dict.values():
                    size_grip.deleteLater()
                self._size_grip_widget_dict.clear()

    def _adjust_size_grip_widget_geometry(self):
        if self.is_size_grip_enabled:
            for edge, size_grip in self._size_grip_widget_dict.items():
                size_grip.update_size_grip_widget_geometry()

    def _adjust_window_top_right_tool_geometry(self):
        r = self.top_right_tool.rect()
        p = self.title_bar.mapTo(self, self.title_bar.rect().topRight())
        r.moveTopRight(p)
        self.top_right_tool.setGeometry(r)

    def _adjust_size_grip_widget_z_depth(self):
        if self.is_size_grip_enabled:
            for edge, size_grip in self._size_grip_widget_dict.items():
                size_grip.raise_()

    def _adjust_window_top_right_tool_z_depth(self):
        self.top_right_tool.raise_()

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self._adjust_size_grip_widget_geometry()
        self._adjust_window_top_right_tool_geometry()

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        self._adjust_size_grip_widget_z_depth()
        self._adjust_window_top_right_tool_z_depth()

    def mousePressEvent(self, event):
        """ 定义鼠标点击事件 """
        if self.test_window_flag(Qt.Popup) and not self.rect().contains(event.pos()):
            self.close_window()

        if event.button() == Qt.LeftButton:
            self.__is_mouse_pressed = True
            self.__drag_position = event.globalPos() - self.geometry().topLeft()
            self.__record_geometry = self.geometry()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        """ 定义鼠标移动事件 """
        if event.buttons() == Qt.LeftButton and self.__is_mouse_pressed and not self.isMaximized():
            self.move(event.globalPos() - self.__drag_position)
            event.accept()

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.__is_mouse_pressed = False
        super().mouseReleaseEvent(event)

    def nativeEvent(self, event_type: Union[QByteArray, bytes, bytearray], message: sip.voidptr) -> Tuple[bool, int]:
        msg = MSG.from_address(message.__int__())
        if msg.message == WM_NCACTIVATE:
            self.sig_native_alert.emit(bool(msg.wParam))
        return super().nativeEvent(event_type, message)

    def set_title(self, title: str):
        self.title_bar.title.setText(title)

    def set_title_bar_visible(self, visible: bool):
        self.title_bar.setVisible(visible)
        self.top_right_tool.setVisible(visible)

    def set_min_btn_visible(self, visible: bool):
        self.top_right_tool.set_min_btn_visible(visible)

    def set_max_btn_visible(self, visible: bool):
        self.top_right_tool.set_max_btn_visible(visible)

    def set_waiting_state(self, flag: bool):
        if self.__being_waiting_state != flag:
            self.__being_waiting_state = flag
            if self.__being_waiting_state:
                self.setCursor(QCursor(Qt.WaitCursor))
                self.__waiting_display = UiDialogWaitingDisplay(self)
                self.__waiting_display.run()
            else:
                self.setCursor(QCursor(Qt.ArrowCursor))
                if self.__waiting_display:
                    self.__waiting_display.quit()
                    self.__waiting_display = None

    def show_wait(self) -> None:
        self.set_waiting_state(True)
        time.sleep(5)
        self.set_waiting_state(False)

    def show_min_window(self) -> None:
        self.showMinimized()

    def show_max_window(self) -> None:
        if not self.isMaximized():
            self.setContentsMargins(0, 0, 0, 0)
            self.showMaximized()
        self.sig_window_max_normal_state_changed.emit()

    def switch_max_normal_window(self):
        if self.isMaximized():
            self.setContentsMargins(self.normal_margins.left(), self.normal_margins.top(),
                                    self.normal_margins.right(), self.normal_margins.bottom())
            self.showNormal()
        else:
            self.setContentsMargins(0, 0, 0, 0)
            self.showMaximized()
        self.sig_window_max_normal_state_changed.emit()

    def close_window(self):
        self.reject()

    def _init_shadow_effect(self):
        shadow = QGraphicsDropShadowEffect()
        # 设置阴影距离
        shadow.setOffset(0, 0)
        # 设置阴影颜色
        shadow.setColor(QColor("#606060"))
        # 设置阴影圆角
        shadow.setBlurRadius(8)
        # 给嵌套QWidget设置阴影
        self.__central_widget.setGraphicsEffect(shadow)

    def test_window_flag(self, win_flag) -> bool:
        return (int(self.windowFlags()) & win_flag) == win_flag

    def move_to_desktop_center(self):
        self.move(int((qApp.desktop().width() - self.width()) / 2),
                  int((qApp.desktop().height() - self.height()) / 2))

    def exec(self) -> int:
        ret = super().exec()
        self.deleteLater()
        return ret

# 两个类，标题栏+等待动画
class UiDialogTitleBar(QFrame):
    sig_show_minimized = pyqtSignal()
    sig_switch_show_max_normal = pyqtSignal()
    sig_close = pyqtSignal()

    def __init__(self, title: str, parent: TestWindow):
        super().__init__(parent)

        self.setCursor(Qt.ArrowCursor)

        self.parent_dialog: TestWindow = parent

        self.is_mouse_pressed = False
        self.drag_position = QPoint(0, 0)

        # 设置背景颜色
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: blue")

        self.title = QLabel(title, self)
        self.title.setObjectName("TitleName")
        self.title.setFixedHeight(26)
        self.title.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.title.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.h_layout = QHBoxLayout()
        self.h_layout.setSpacing(4)
        self.h_layout.setContentsMargins(4, 0, 0, 0)
        self.h_layout.addWidget(self.title)
        self.h_layout.addStretch(1)
        self.setLayout(self.h_layout)

    def mouseDoubleClickEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self.is_mouse_pressed = False
            self.sig_switch_show_max_normal.emit()
            event.accept()

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self.is_mouse_pressed = True
            self.drag_position = event.globalPos() - self.window().frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.is_mouse_pressed:
            if self.window().isMaximized():
                w = self.window()
                max_width = w.width()
                normal_width = w.normalGeometry().width()
                scale = event.x() / max_width
                normal_delta_x = normal_width * scale

                normal_rect = self.window().normalGeometry()
                normal_rect.moveLeft(int(event.globalX() - normal_delta_x))
                normal_rect.moveTop(int(event.globalY() - event.y() - self.parent_dialog.normal_margins.top()))

                self.drag_position = self.drag_position + self.window().frameGeometry().topLeft() - normal_rect.topLeft()
                self.sig_switch_show_max_normal.emit()

            self.window().move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_mouse_pressed = False
        super().mouseReleaseEvent(event)

    def minimumSizeHint(self) -> QSize:
        s = super().minimumSizeHint()
        s.setWidth(self.h_layout.sizeHint().width() + self.parent_dialog.top_right_tool.sizeHint().width())
        return s


class UiDialogWaitingDisplay(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet("font-size:12px; color:#333; padding:0px 0px 0px 0px;")
        self.movie = QMovie(LIB_RESOURCE_DIR + "\\images\\waiting.gif")

        self.gifLabel = QLabel(self)
        self.gifLabel.setFixedSize(40, 40)
        self.gifLabel.setAlignment(Qt.AlignCenter)

        self.gifLabel.setMovie(self.movie)

        vLayout = QVBoxLayout()
        vLayout.setSpacing(0)
        vLayout.addStretch(1)
        vLayout.addWidget(self.gifLabel, 0, Qt.AlignHCenter)
        vLayout.addWidget(QLabel("Waiting...", self), 0, Qt.AlignHCenter)
        vLayout.addStretch(1)

        self.setLayout(vLayout)

    def run(self):
        self.movie.start()
        self.setGeometry(self.window().rect())
        self.show()
        self.raise_()

    def quit(self):
        self.hide()
        self.movie.stop()
        self.deleteLater()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        parentMargins = self.parent().contentsMargins()
        painter.setBrush(QColor(100, 100, 100, 40))
        painter.drawRect(self.rect().adjusted(parentMargins.left() + 1, parentMargins.top() + 1,
                                              -parentMargins.right() - 1, -parentMargins.bottom() - 1))

        gifRect = QRect(0, 0, 70, 70)
        gifRect.moveCenter(self.rect().adjusted(1, 1, -2, -2).center())
        gifRect.adjust(0, -2, 0, -2)

        painter.setBrush(QColor("#fafafa"))
        painter.drawRoundedRect(gifRect, 4, 4)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 注册 fontello 字体
    font_db = QFontDatabase()
    font_path = os.path.abspath("resources/fonts/fontello.ttf")
    font_db.addApplicationFont(font_path)

    # 加载样式表（包含 UiFontIconButton 的 fontello 字体设置）
    qss_path = os.path.abspath("resources/qss/custom.qss")
    with open(qss_path, "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())
    win = TestWindow("test")
    win.show()
    sys.exit(app.exec_())
