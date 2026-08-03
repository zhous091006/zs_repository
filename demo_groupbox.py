import sys
import time
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout,
    QWidget, QLabel, QGroupBox, QHBoxLayout
)
from ui.custom_widgets.ui_group_box import UiGroupBox


class DemoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UiGroupBox 功能演示")
        self.resize(400, 300)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # 创建 UiGroupBox
        self.group_box = UiGroupBox(icon="", title="分组框标题")

        # 在 body_box 中添加内容
        body_layout = QVBoxLayout(self.group_box.body_box)
        body_layout.addWidget(QLabel("这是分组框的内容区域"))

        btn1 = QPushButton("按钮 1")
        btn2 = QPushButton("按钮 2")
        body_layout.addWidget(btn1)
        body_layout.addWidget(btn2)

        main_layout.addWidget(self.group_box)

        # 控制按钮
        ctrl_layout = QHBoxLayout()
        self.toggle_btn = QPushButton("模拟加载/完成")
        self.toggle_btn.clicked.connect(self.toggle_waiting)
        ctrl_layout.addWidget(self.toggle_btn)
        main_layout.addLayout(ctrl_layout)

        self.is_waiting = False

    def toggle_waiting(self):
        self.is_waiting = not self.is_waiting
        self.group_box.set_waiting_status(self.is_waiting)
        self.toggle_btn.setText("退出加载" if self.is_waiting else "模拟加载")


def main():
    app = QApplication(sys.argv)

    # 加载项目样式表
    qss_path = "resources/qss/custom.qss"
    try:
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print(f"未找到样式表 {qss_path}，将使用默认样式")

    window = DemoWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
