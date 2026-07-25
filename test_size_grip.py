import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QApplication
from ui.custom_widgets.ui_size_grip import UiSizeGrip


class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UiSizeGrip 测试窗口")
        self.resize(400, 300)
        self.setMinimumSize(200, 150)
        self.setStyleSheet("background-color: #f0f0f0;")

        self.init_ui()
        self.init_size_grips()

    def init_ui(self):
        center = QWidget()
        layout = QVBoxLayout(center)
        layout.setAlignment(Qt.AlignCenter)

        label = QLabel("拖拽窗口边缘或角落来调整大小")
        label.setStyleSheet("font-size: 16px; color: #333;")
        layout.addWidget(label)

        self.setCentralWidget(center)

    def init_size_grips(self):
        self.grip_size = 16
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
            grip.setFixedSize(self.grip_size, self.grip_size)
            grip.setStyleSheet("background-color: transparent;")
            grip.show()
            self.grips.append(grip)

        self.update_all_grips()

    def update_all_grips(self):
        for grip in self.grips:
            grip.update_size_grip_widget_geometry()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_all_grips()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = TestWindow()
    win.show()
    sys.exit(app.exec_())
