from typing import Dict

from PyQt5.QtCore import Qt, QRect, QPoint, QMargins, pyqtSignal, QSize
from PyQt5.QtGui import QMouseEvent, QColor, QResizeEvent, QPixmap, QShowEvent, QBitmap, QPainter
from PyQt5.QtWidgets import QMainWindow, QFrame, QLabel, QHBoxLayout, QGraphicsDropShadowEffect, QVBoxLayout, qApp, QMenuBar, QWidget

from lib.lib_type import LIB_RESOURCE_DIR
from ui.custom_widgets.ui_size_grip import UiSizeGrip
from ui.custom_widgets.ui_window_tools import UiWindowTopRightTool

from ui.dialogs.ui_dialog_about import UiDialogAbout
from ui.custom_widgets.menu.ui_menu import UiMenu


class UiCustomMainWindow(QMainWindow):
    sig_window_max_normal_state_changed = pyqtSignal()
    normal_margins = QMargins(4, 4, 4, 4)

    def __init__(self):
        super().__init__(parent=None, flags=Qt.Window)

        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint
                            | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setContentsMargins(self.normal_margins.left(), self.normal_margins.top(),
                                self.normal_margins.right(), self.normal_margins.bottom())

        self.__record_geometry: QRect = QRect(0, 0, 0, 0)
        self.__record_mouse_pos_edge = 0
        self.__drag_position = QPoint(0, 0)
        self.__is_mouse_pressed = False

        self.__container_widget = QFrame(self)
        self.__container_widget.setObjectName("ContainerWidget")
        self.__container_widget.setCursor(Qt.ArrowCursor)
        self.__set_border_shadow_effect(self.__container_widget)

        #
        self.central_widget = QFrame()
        self.central_widget.setObjectName("CentralWidget")
        self.central_widget.setMouseTracking(True)
        self.central_widget.setCursor(Qt.ArrowCursor)
        self.central_widget.setVisible(False)

        #
        self.top_right_tool = UiWindowTopRightTool(self)

        #
        self.m_layout = QVBoxLayout()
        self.m_layout.setContentsMargins(0, 0, 0, 0)
        self.m_layout.setSpacing(0)
        # self.m_layout.addWidget(self.top_bar)
        # self.m_layout.addWidget(self.central_widget)

        self.__container_widget.setLayout(self.m_layout)

        self.is_size_grip_enabled = False
        self._size_grip_widget_dict: Dict[Qt.Edges, UiSizeGrip] = {}
        self.set_size_grip_enabled(True)

        #
        self.top_bar = UiCustomMainWindowTopBar(self)
        self.setMenuBar(self.top_bar)

        # 新增Menu测试
        '''Help Menu'''
        help_menu = UiMenu(("Help") + " (&H)", self.top_bar)
        help_menu.addAction(("About..."), self.show_help_dialog)

        self.top_bar.addMenu(help_menu)

        self.__init_connect()

    def __init_connect(self) -> None:
        self.top_right_tool.sig_close.connect(self.quit_app)
        self.top_right_tool.sig_show_minimized.connect(self.show_min_window)
        self.top_right_tool.sig_switch_show_max_normal.connect(self.switch_max_normal_window)
        self.sig_window_max_normal_state_changed.connect(self.top_right_tool.on_window_max_normal_state_changed)
        self.top_bar.sig_switch_show_max_normal.connect(self.switch_max_normal_window)

    def show_help_dialog(self):
        ui_about = UiDialogAbout(self)
        ui_about.exec()

    def set_size_grip_enabled(self, enable: bool) -> None:
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

    def _adjust_size_grip_widget_geometry(self) -> None:
        if self.is_size_grip_enabled:
            for edge, size_grip in self._size_grip_widget_dict.items():
                size_grip.update_size_grip_widget_geometry()

    def _adjust_window_top_right_tool_geometry(self) -> None:
        r = self.top_right_tool.rect()
        r.moveTopRight(self.__container_widget.geometry().topRight())
        self.top_right_tool.setGeometry(r)

    def _adjust_size_grip_widget_z_depth(self) -> None:
        if self.is_size_grip_enabled:
            for edge, size_grip in self._size_grip_widget_dict.items():
                size_grip.raise_()

    def _adjust_window_top_right_tool_z_depth(self) -> None:
        self.top_right_tool.raise_()

    def minimumSizeHint(self) -> QSize:
        return self.__container_widget.minimumSizeHint() + QSize(self.normal_margins.top(), self.normal_margins.top())

    def sizeHint(self) -> QSize:
        return self.__container_widget.sizeHint() + QSize(self.normal_margins.top(), self.normal_margins.top())

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        if self.isMaximized():
            margin_spacing = 0
        else:
            margin_spacing = self.normal_margins.top()
        self.__container_widget.setGeometry(self.rect().adjusted(margin_spacing, margin_spacing, -margin_spacing, -margin_spacing))
        self._adjust_size_grip_widget_geometry()
        self._adjust_window_top_right_tool_geometry()
        # self.__update_container_widget_mask()

    def showEvent(self, event: QShowEvent) -> None:
        self.setMinimumSize(800, 800)
        super().showEvent(event)
        self._adjust_size_grip_widget_z_depth()
        self._adjust_window_top_right_tool_z_depth()

    def mousePressEvent(self, event) -> None:
        """ 定义鼠标点击事件 """
        if event.button() == Qt.LeftButton:
            self.__is_mouse_pressed = True
            self.__record_mouse_pos_edge = self.__get_mouse_pos_edge(event.pos())
            self.__drag_position = event.globalPos() - self.geometry().topLeft()
            self.__record_geometry = self.geometry()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """ 定义鼠标移动事件 """
        if not self.__is_mouse_pressed:
            self.__record_mouse_pos_edge = self.__get_mouse_pos_edge(event.pos())

        if self.__record_mouse_pos_edge == 0 and event.buttons() == Qt.LeftButton and self.__is_mouse_pressed and not self.isMaximized():
            self.move(event.globalPos() - self.__drag_position)
            event.accept()

        # self.__deal_mouse_hover_cursor()
        # self.__deal_mouse_move_resize(event)

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self.__is_mouse_pressed = False
        super().mouseReleaseEvent(event)

    def __update_container_widget_mask(self) -> None:
        bmp = QBitmap(self.__container_widget.size())
        bmp.clear()

        painter = QPainter(bmp)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(Qt.black))
        painter.drawRoundedRect(self.__container_widget.rect(), 8.0, 8.0, Qt.AbsoluteSize)
        self.__container_widget.setMask(bmp)

    def __get_mouse_pos_edge(self, pos: QPoint) -> int:
        x = pos.x()
        y = pos.y()
        w = self.width()
        h = self.height()
        margins: QMargins = self.contentsMargins()

        if 0 < y < margins.top():
            if 0 < x < margins.left():
                return Qt.TopEdge | Qt.LeftEdge
            if 0 < x < w - margins.right():
                return Qt.TopEdge
            if w - margins.right() < x < w:
                return Qt.TopEdge | Qt.RightEdge
        elif margins.top() < y < h - margins.bottom():
            if 0 < x < margins.left():
                return Qt.LeftEdge
            if w - margins.right() < x < w:
                return Qt.RightEdge
        elif h - margins.bottom() < y < h:
            if 0 < x < margins.left():
                return Qt.BottomEdge | Qt.LeftEdge
            if 0 < x < w - margins.right():
                return Qt.BottomEdge
            if w - margins.right() < x < w:
                return Qt.BottomEdge | Qt.RightEdge

        return 0

    def show_min_window(self) -> None:
        self.showMinimized()

    def show_max_window(self) -> None:
        if not self.isMaximized():
            self.setContentsMargins(0, 0, 0, 0)
            self.showMaximized()
        self.sig_window_max_normal_state_changed.emit()

    def show_normal_window(self) -> None:
        if self.isMaximized() or self.isMinimized():
            self.setContentsMargins(self.normal_margins.left(), self.normal_margins.top(),
                                    self.normal_margins.right(), self.normal_margins.bottom())
            self.showNormal()

    def switch_max_normal_window(self) -> None:
        if self.isMaximized():
            self.show_normal_window()
        else:
            self.show_max_window()

    def quit_app(self) -> None:
        """
        关闭主窗口，并退出 APP
        :return:
        """
        if self.close():
            qApp.quit()

    def move_to_desktop_center(self) -> None:
        r = qApp.desktop().availableGeometry()
        self.move(int((r.width() - self.width()) / 2),
                  int((r.height() - self.height()) / 2))

    @staticmethod
    def __set_border_shadow_effect(widget) -> None:
        shadow = QGraphicsDropShadowEffect()
        # 设置阴影距离
        shadow.setOffset(0, 0)
        # 设置阴影颜色
        shadow.setColor(QColor("#000"))
        # 设置阴影圆角
        shadow.setBlurRadius(8)
        # 给嵌套QWidget设置阴影
        widget.setGraphicsEffect(shadow)


class UiCustomMainWindowTopBar(QMenuBar):
    sig_show_minimized = pyqtSignal()
    sig_switch_show_max_normal = pyqtSignal()
    sig_close = pyqtSignal()

    def __init__(self, parent: QMainWindow):
        super().__init__(parent)

        self.setCursor(Qt.ArrowCursor)

        self.__is_mouse_pressed = False
        self.__drag_position = QPoint(0, 0)

        self.__left_bar = QWidget(self)

        self.__app_logo = QLabel(self)
        self.__app_logo.setObjectName("AppLogo")
        self.__app_logo.setPixmap(QPixmap(LIB_RESOURCE_DIR + "\\images\\app_logo.svg").scaled(24, 24))

        self.__app_logo.setFixedSize(24, 24)

        h_layout = QHBoxLayout()
        h_layout.setSpacing(4)
        h_layout.setContentsMargins(2, 0, 0, 0)
        h_layout.addWidget(self.__app_logo)

        self.__left_bar.setLayout(h_layout)
        self.__left_bar.adjustSize()

        self.__init_connect()

    def __init_connect(self) -> None:
        pass

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.__left_bar.setFixedHeight(self.height())
        self.__left_bar.move(0, 0)

    def mouseDoubleClickEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self.__is_mouse_pressed = False
            if not self.actionAt(event.pos()):
                self.sig_switch_show_max_normal.emit()
            event.accept()
        # super().mouseDoubleClickEvent(event)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton and not self.actionAt(event.pos()):
            self.__is_mouse_pressed = True
            self.__drag_position = event.globalPos() - self.window().frameGeometry().topLeft()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """定义鼠标移动事件"""
        if event.buttons() == Qt.LeftButton and self.__is_mouse_pressed:
            w = self.window()
            if w.isMaximized():
                max_width = w.width()
                normal_width = w.normalGeometry().width()
                scale = event.x() / max_width
                normal_delta_x = normal_width * scale

                normal_rect = w.normalGeometry()
                normal_rect.moveLeft(int(event.globalX() - normal_delta_x))
                normal_rect.moveTop(int(event.globalY() - event.y() - 2 * w.normal_margins.top()))

                self.__drag_position = self.__drag_position + w.frameGeometry().topLeft() - normal_rect.topLeft()
                self.sig_switch_show_max_normal.emit()

            w.move(event.globalPos() - self.__drag_position)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self.__is_mouse_pressed = False
        super().mouseReleaseEvent(event)
