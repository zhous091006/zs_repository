import sys
import math
from lib.lib_func import lib_func_t

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame
)

from ui.custom_widgets.ui_waiting_animation_widget import UiWaitingAnimationWidget


class TestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UiWaitingAnimationWidget 测试")
        self.resize(400, 500)

        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        # --- 颜色测试区 ---
        self._build_color_section(layout)

        layout.addStretch()

    def _build_color_section(self, layout):
        title = QLabel("不同颜色与尺寸")
        title.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 4px;")
        layout.addWidget(title)

        colors = [
            ("#0492FC", "默认蓝色"),
            ("#0f0",     "绿色"),
            ("#ff4444",  "红色"),
            ("#ffaa00",  "橙色"),
            ("#aa44ff",  "紫色"),
        ]

        sizes = [
            (16, 16,  "16x16"),
            (32, 32,  "32x32"),
            (48, 48,  "48x48"),
            (64, 64,  "64x64"),
        ]

        # 按颜色分组
        for color_hex, color_name in colors:
            row = QHBoxLayout()
            row.setSpacing(12)

            label = QLabel(color_name)
            label.setFixedWidth(60)
            row.addWidget(label)

            for w, h, _ in sizes:
                # 容器提供深色背景
                container = QFrame()
                container.setFixedSize(w + 4, h + 4)
                container.setStyleSheet("background-color: #1a1a2e; border-radius: 4px;")

                anim = UiWaitingAnimationWidget(container)
                anim.setFixedSize(w, h)
                anim.move(2, 2)
                anim.set_color(QColor(color_hex))
                anim.start()

                row.addWidget(container)

            layout.addLayout(row)

        # 按钮控制区
        btn_row = QHBoxLayout()

        btn_start = QPushButton("全部开始")
        btn_start.clicked.connect(self._start_all)
        btn_row.addWidget(btn_start)

        btn_stop = QPushButton("全部停止")
        btn_stop.clicked.connect(self._stop_all)
        btn_row.addWidget(btn_stop)

        layout.addLayout(btn_row)

        # 保存所有动画引用
        self._collect_animations()

    def _collect_animations(self):
        self._animations = []
        for child in self.findChildren(UiWaitingAnimationWidget):
            self._animations.append(child)

    def _start_all(self):
        for anim in self._animations:
            anim.start()

    def _stop_all(self):
        for anim in self._animations:
            anim.stop()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = TestWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
