import sys, os
from PyQt5.QtCore import Qt, QMargins
from PyQt5.QtGui import QMouseEvent, QFontDatabase, QShowEvent
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QApplication, QPushButton
from ui.custom_widgets.ui_size_grip import UiSizeGrip
from ui.custom_widgets.ui_datetime_edit import UiDateTimeEdit
from ui.custom_widgets.ui_window_tools import UiWindowTopRightTool

EDGE_MARGIN = 5

class TestWindow(QMainWindow):
    normal_margins = QMargins(4, 4, 4, 4)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UiSizeGrip 测试窗口")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMouseTracking(True)
        # self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.resize(400, 300)
        self.setMinimumSize(200, 150)
        # self.setStyleSheet("background-color: #f0f0f0;")
        self.setContentsMargins(self.normal_margins.left(), self.normal_margins.top(),
                                self.normal_margins.right(), self.normal_margins.bottom())

        self.init_ui()
        self.init_size_grips()

    def init_ui(self):
        center = QWidget()
        layout = QVBoxLayout(center)
        layout.setAlignment(Qt.AlignCenter)

        winTool = UiWindowTopRightTool(self)
        layout.addWidget(winTool)

        close_btn = QPushButton("[×]", self)
        close_btn.setFixedHeight(30)
        close_btn.setFixedWidth(30)
        close_btn.clicked.connect(self.quit)
        layout.addWidget(close_btn)

        date_edit = UiDateTimeEdit(self)
        layout.addWidget(date_edit)

        label = QLabel("拖拽窗口边缘或角落来调整大小")
        label.setStyleSheet("font-size: 16px; color: #333;")
        layout.addWidget(label)

        self.setCentralWidget(center)

    def init_size_grips(self):
        margin = 4
        edge_list = [
            Qt.LeftEdge,
            Qt.TopEdge,
            Qt.RightEdge,
            Qt.BottomEdge,
            Qt.TopEdge | Qt.LeftEdge,
            Qt.TopEdge | Qt.RightEdge,
            Qt.BottomEdge | Qt.LeftEdge,
            Qt.BottomEdge | Qt.RightEdge,
        ]
        self.grips = []
        for edge in edge_list:
            grip = UiSizeGrip(edge, self)
            grip.setStyleSheet("background-color: transparent;")
            if edge in (Qt.LeftEdge, Qt.RightEdge):
                grip.setFixedWidth(margin)
            elif edge in (Qt.TopEdge, Qt.BottomEdge):
                grip.setFixedHeight(margin)
            else:
                grip.setFixedSize(margin, margin)
            grip.show()
            self.grips.append(grip)

        self.update_all_grips()

    def update_all_grips(self):
        for grip in self.grips:
            grip.update_size_grip_widget_geometry()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_all_grips()

    def getResizeRegion(self, pos):
        width = self.size().width()  # 获取当前窗口尺寸的宽度
        onLeft = pos.x() <= EDGE_MARGIN
        onRight = pos.x() >= width - EDGE_MARGIN
        print(onLeft, onRight)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        global_pos = event.globalPos()
        print(global_pos)
        self.getResizeRegion(global_pos)
        event.accept()

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        self._adjust_size_grip_widget_z_depth()

    def _adjust_size_grip_widget_z_depth(self):
        for grip in self.grips:
            grip.raise_()

    @staticmethod
    def quit():
        sys.exit()

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
    win = TestWindow()
    win.show()
    sys.exit(app.exec_())
