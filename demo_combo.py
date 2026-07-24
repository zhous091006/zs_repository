import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from ui.custom_widgets.ui_combo_box import UiComboBox


class DemoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UiComboBox 预览")
        self.resize(300, 200)

        layout = QVBoxLayout(self)

        lbl = QLabel("请选择一项：")
        layout.addWidget(lbl)

        self.combo = UiComboBox(self)
        self.combo.add_dict_items({
            "选项 A": "value_a",
            "选项 B": "value_b",
            "选项 C": "value_c",
        })
        layout.addWidget(self.combo)

        self.combo.activated.connect(self.on_selected)

    def on_selected(self, index):
        text = self.combo.itemText(index)
        data = self.combo.itemData(index)
        print(f"选中: {text}, 值: {data}")


app = QApplication(sys.argv)
win = DemoWindow()
win.show()
sys.exit(app.exec_())
