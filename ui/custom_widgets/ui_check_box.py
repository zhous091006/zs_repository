from PyQt5.QtWidgets import QCheckBox


class UiCheckBox(QCheckBox):
    def __init__(self, *args):
        super().__init__(*args)
        self.setFixedHeight(26)
