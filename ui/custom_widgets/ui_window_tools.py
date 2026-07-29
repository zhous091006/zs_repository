from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QFrame, QHBoxLayout

from ui.custom_widgets.buttons.ui_font_icon_button import UiFontIconButton

class UiWindowTopRightTool(QFrame):
    sig_show_minimized = pyqtSignal()
    sig_switch_show_max_normal = pyqtSignal()
    sig_close = pyqtSignal()
    sig_resized = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.__min_btn = UiFontIconButton(UiFontIconButton.WINDOW_MIN, self)
        self.__min_btn.setObjectName("MinBtn")
        self.__min_btn.setFixedSize(28, 28)
        self.__min_btn.setFocusPolicy(Qt.NoFocus)

        self.__max_btn = UiFontIconButton(UiFontIconButton.WINDOW_MAX, self)
        self.__max_btn.setObjectName("MaxBtn")
        self.__max_btn.setFixedSize(28, 28)
        self.__max_btn.setFocusPolicy(Qt.NoFocus)

        self.__close_btn = UiFontIconButton(UiFontIconButton.CLOSE, self)
        self.__close_btn.setObjectName("CloseBtn")
        self.__close_btn.setFixedSize(28, 28)
        self.__close_btn.setFocusPolicy(Qt.NoFocus)

        h_layout = QHBoxLayout()
        h_layout.setSpacing(0)
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.addWidget(self.__min_btn, 0, Qt.AlignTop)
        h_layout.addWidget(self.__max_btn, 0, Qt.AlignTop)
        h_layout.addWidget(self.__close_btn, 0, Qt.AlignTop)

        self.setLayout(h_layout)

        self.__init_connect()
        self.on_window_max_normal_state_changed()
        self.adjustSize()

    def __init_connect(self):
        self.__min_btn.clicked.connect(self.sig_show_minimized)
        self.__max_btn.clicked.connect(self.sig_switch_show_max_normal)
        self.__close_btn.clicked.connect(self.sig_close)

    def on_window_max_normal_state_changed(self):
        if self.window().isMaximized():
            self.__max_btn.set_icon(UiFontIconButton.WINDOW_NORMAL)
        else:
            self.__max_btn.set_icon(UiFontIconButton.WINDOW_MAX)
        self.__max_btn.style().unpolish(self.__max_btn)
        self.__max_btn.style().polish(self.__max_btn)

    def set_icon_size(self, width, height):
        self.__min_btn.setFixedSize(width, height)
        self.__max_btn.setFixedSize(width, height)
        self.__close_btn.setFixedSize(width, height)
        self.adjustSize()

    def set_min_btn_visible(self, visible: bool):
        self.__min_btn.setVisible(visible)
        self.adjustSize()

    def set_max_btn_visible(self, visible: bool):
        self.__max_btn.setVisible(visible)
        self.adjustSize()

    def set_close_btn_visible(self, visible: bool):
        self.__close_btn.setVisible(visible)
        self.adjustSize()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.sig_resized.emit()

