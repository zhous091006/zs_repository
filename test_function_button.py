import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout

from ui.custom_widgets.buttons.ui_function_button import UiFunctionButton


def main():
    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(400, 200)
    layout = QVBoxLayout(w)

    # 创建三个按钮，分别展示不同状态
    btn1 = UiFunctionButton("待执行", w)
    btn2 = UiFunctionButton("执行中", w)
    btn3 = UiFunctionButton("已完成", w)

    # 设置不同状态
    btn2.set_status(is_running=True)
    btn3.set_status(is_finished=True)

    layout.addWidget(btn1)
    layout.addWidget(btn2)
    layout.addWidget(btn3)

    # 点击切换状态
    def cycle_state(btn, original_text):
        if btn.is_running:
            btn.set_status(is_finished=True)
        elif btn.is_finished:
            btn.set_status()
        else:
            btn.set_status(is_running=True)

    btn1.clicked.connect(lambda: cycle_state(btn1, "待执行"))
    btn2.clicked.connect(lambda: cycle_state(btn2, "执行中"))
    btn3.clicked.connect(lambda: cycle_state(btn3, "已完成"))

    w.show()
    app.exec_()


if __name__ == "__main__":
    main()
