import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout

from ui.custom_widgets.buttons.ui_push_button import UiPushButton

app = QApplication(sys.argv)

w = QWidget()
w.resize(300, 200)
layout = QVBoxLayout(w)

btn = UiPushButton("点击我", w)
btn.clicked.connect(lambda: print("按钮被点击"))

btn2 = UiPushButton.create_icon_button(text="﹣", object_name="Icon", width=20, height=20, parent=w)
btn2.clicked.connect(lambda: print("按钮2被点击"))

layout.addWidget(btn)
layout.addWidget(btn2)

w.show()
app.exec_()
