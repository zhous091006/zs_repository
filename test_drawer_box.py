import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QMessageBox, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from ui.custom_widgets.ui_drawer_box import UiDrawerBox


class ColorBlock(QWidget):
    """带颜色的方块，用于可视化演示"""
    COLOR_MAP = [
        "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4",
        "#FFEAA7", "#DDA0DD", "#98D8C8", "#F7DC6F",
        "#BB8FCE", "#85C1E9", "#F0B27A", "#82E0AA",
    ]

    def __init__(self, index, parent=None):
        super().__init__(parent)
        self.index = index
        color = self.COLOR_MAP[index % len(self.COLOR_MAP)]
        self.setStyleSheet(
            f"QLabel {{ background-color: {color}; "
            f"border-radius: 6px; min-height: 60px; }}"
        )

        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        label = QLabel(f"项目 {index + 1}  ({color})")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("", 11, QFont.Bold))
        label.setObjectName(f"block_{index}")
        label.setStyleSheet(
            f"QLabel {{ background-color: {color}; "
            f"border-radius: 6px; min-height: 60px; "
            f"color: #333; }}"
        )
        layout.addWidget(label)
        self.setLayout(layout)

    def sizeHint(self):
        from PyQt5.QtCore import QSize
        return QSize(300, 80)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UiDrawerBox 测试")
        self.resize(480, 520)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(12, 12, 12, 12)

        # 按钮操作区
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("追加项目")
        self.btn_insert = QPushButton("插入到头部")
        self.btn_remove = QPushButton("删除第一个")
        self.btn_clear = QPushButton("清空所有")
        self.lbl_count = QLabel("当前项目数: 0")
        self.lbl_count.setFont(QFont("", 10, QFont.Bold))

        for btn in (self.btn_add, self.btn_insert, self.btn_remove, self.btn_clear):
            btn.setFixedHeight(34)
            btn_layout.addWidget(btn)
        btn_layout.addWidget(self.lbl_count)
        main_layout.addLayout(btn_layout)

        # 抽屉容器
        self.drawer = UiDrawerBox(self)
        main_layout.addWidget(self.drawer)

        # 绑定信号
        self.counter = 0
        self.btn_add.clicked.connect(self.on_add)
        self.btn_insert.clicked.connect(self.on_insert)
        self.btn_remove.clicked.connect(self.on_remove)
        self.btn_clear.clicked.connect(self.on_clear)

    def on_add(self):
        w = ColorBlock(self.counter)
        self.drawer.append_item(w)
        self.counter += 1
        self.update_count()

    def on_insert(self):
        w = ColorBlock(self.counter)
        self.drawer.insert_item(0, w)
        self.counter += 1
        self.update_count()

    def on_remove(self):
        widgets = self.drawer.widgets
        if widgets:
            self.drawer.remove_item(widgets[0])
            self.update_count()

    def on_clear(self):
        widgets = list(self.drawer.widgets)
        for w in widgets:
            self.drawer.remove_item(w)
        self.update_count()

    def update_count(self):
        self.lbl_count.setText(f"当前项目数: {len(self.drawer.widgets)}")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
