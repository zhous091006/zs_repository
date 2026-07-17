import sys,os
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout
from ui.custom_widgets.buttons.ui_font_icon_button import UiFontIconButton
from PyQt5.QtGui import QFontDatabase

app = QApplication(sys.argv)
# 注册 fontello 字体
font_db = QFontDatabase()
font_path = os.path.abspath("resources/fonts/fontello.ttf")
print(f"路径: {font_path}")
print(f"存在: {os.path.exists(font_path)}")
font_db.addApplicationFont(font_path)

# 加载样式表（包含 UiFontIconButton 的 fontello 字体设置）
qss_path = os.path.abspath("resources/qss/custom.qss")
with open(qss_path, "r", encoding="utf-8") as f:
    app.setStyleSheet(f.read())

w = QWidget()
layout = QHBoxLayout(w)

btn1 = UiFontIconButton(UiFontIconButton.PLAY, w)
btn2 = UiFontIconButton(UiFontIconButton.PAUSE, w)
btn3 = UiFontIconButton(UiFontIconButton.CLOSE, w)
# btn3.set_foot_icon(UiFontIconButton.PLAY)  # 右下角小红标


btn1.clicked.connect(lambda: print("播放"))
btn2.clicked.connect(lambda: print("暂停"))
btn3.clicked.connect(lambda: print("关闭"))

layout.addWidget(btn1)
layout.addWidget(btn2)
layout.addWidget(btn3)

w.show()
app.exec_()
