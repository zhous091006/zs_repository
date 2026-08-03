import sys
import os

# 将项目根目录加入路径，确保能导入 ui 模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from ui.custom_widgets.ui_message_box import UiMessageBox


class DemoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UiMessageBox 功能演示")
        self.resize(400, 350)

        main = QVBoxLayout(self)

        btn_info = QPushButton("信息提示 (information)")
        btn_info.clicked.connect(self.on_info)
        main.addWidget(btn_info)

        btn_tip = QPushButton("提示信息 (tip)")
        btn_tip.clicked.connect(self.on_tip)
        main.addWidget(btn_tip)

        btn_question = QPushButton("询问框 (question)")
        btn_question.clicked.connect(self.on_question)
        main.addWidget(btn_question)

        btn_warning = QPushButton("警告框 (warning)")
        btn_warning.clicked.connect(self.on_warning)
        main.addWidget(btn_warning)

        btn_error = QPushButton("错误提示 (error)")
        btn_error.clicked.connect(self.on_error)
        main.addWidget(btn_error)

        btn_custom = QPushButton("自定义按钮 (custom_message)")
        btn_custom.clicked.connect(self.on_custom)
        main.addWidget(btn_custom)

        main.addStretch()

    def on_info(self):
        UiMessageBox.information("信息", "这是一条信息提示", parent=self)

    def on_tip(self):
        ret = UiMessageBox.tip("提示", "是否继续执行操作？", parent=self)
        print(f"tip 返回值: {ret}")

    def on_question(self):
        ret = UiMessageBox.question("询问", "确定要执行此操作吗？", parent=self)
        print(f"question 返回值: {ret}")

    def on_warning(self):
        ret = UiMessageBox.warning("警告", "此操作不可撤销，是否继续？", parent=self)
        print(f"warning 返回值: {ret}")

    def on_error(self):
        UiMessageBox.error("错误", "操作失败：文件未找到", parent=self)

    def on_custom(self):
        btn = UiMessageBox.custom_message(
            level=UiMessageBox.LEVEL_QUESTION,
            title="请选择",
            text="请选择要执行的操作：",
            roles=["导入数据", "导出数据", "取消"],
            parent=self
        )
        print(f"custom_message 返回值: {btn}")


def main():
    app = QApplication(sys.argv)

    # 加载项目样式表
    qss_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "qss", "custom.qss")
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
