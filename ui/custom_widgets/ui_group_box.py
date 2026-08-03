from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGroupBox, QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout


class UiGroupBox(QFrame):
    def __init__(self, icon: str = "", title: str = "", parent: QWidget = None):
        super().__init__(parent)

        self.waiting_mask = QWidget(self)
        self.waiting_mask.setCursor(Qt.WaitCursor)
        self.waiting_mask.setVisible(False)

        ''' title bar '''
        self.title_bar = QFrame(self)
        self.title_bar.setObjectName("TitleBar")
        self.title_bar.setFixedHeight(28)
        self.title_bar_layout = QHBoxLayout()

        self.title_icon = QLabel(self.title_bar)
        if icon:
            self.title_icon.setFixedSize(12, 12)
            self.title_icon.setPixmap(QPixmap(icon))
        else:
            self.title_icon.hide()
        self.title_label = QLabel(title, self.title_bar)

        ''' body box '''
        self.body_box = QGroupBox(self)
        self.body_box.setObjectName("Body")

        ''' init layout '''
        self._init_title_bar_layout()
        self._main_init_layout()
        self.setMinimumSize(100, 40)

    def set_waiting_status(self, state: bool):
        if state:
            for child in self.children():
                if isinstance(child, QWidget):
                    child.setEnabled(False)
            self.waiting_mask.setEnabled(True)
            self.waiting_mask.setVisible(True)
            self.waiting_mask.raise_()
        else:
            for child in self.children():
                if isinstance(child, QWidget):
                    child.setEnabled(True)
            self.waiting_mask.setVisible(False)

    def _init_title_bar_layout(self):
        self.title_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.title_bar_layout.setSpacing(4)
        self.title_bar_layout.addSpacing(4)
        self.title_bar_layout.addWidget(self.title_icon)
        self.title_bar_layout.addWidget(self.title_label)
        self.title_bar_layout.addStretch(1)
        self.title_bar.setLayout(self.title_bar_layout)

    def _main_init_layout(self):
        v_layout = QVBoxLayout()
        v_layout.setContentsMargins(0, 0, 0, 0)
        v_layout.setSpacing(0)
        v_layout.addWidget(self.title_bar)
        v_layout.addWidget(self.body_box)
        self.setLayout(v_layout)

    def resizeEvent(self, event) -> None:
        self.waiting_mask.setGeometry(self.rect())
        super().resizeEvent(event)
