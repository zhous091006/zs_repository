from PyQt5.QtWidgets import QSpinBox


class UiSpinBox(QSpinBox):
    def __init__(self, *args):
        super().__init__(*args)
        self.setFixedHeight(26)
