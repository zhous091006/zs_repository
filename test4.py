import sys, os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent, QFontDatabase
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QApplication, QPushButton

from ui.custom_widgets.ui_dialog_base import UiDialogBase

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
    win = UiDialogBase("test")
    win.show()
    sys.exit(app.exec_())
