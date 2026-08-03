from PyQt5 import sip
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLayout

from ui.custom_widgets.ui_scroll_area import UiScrollArea


class UiHorizontalScrollFrame(QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.container = QFrame(self)
        self.container.setObjectName("Container")

        self.scroll_area = UiScrollArea(self)
        self.scroll_area.setWidget(self.container)

        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.addWidget(self.scroll_area)
        self.setLayout(h_layout)

    def set_container_layout(self, layout):
        if isinstance(self.container.layout(), QLayout):
            sip.delete(self.container.layout())
        self.container.setLayout(layout)
        self.container.adjustSize()
        self.scroll_area.setWidget(self.container)
        self.update_size()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.update_size()

    def update_size(self):
        viewport_height = self.scroll_area.viewport().height()
        self.container.setFixedHeight(viewport_height)


class UiVerticalScrollFrame(QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.container = QFrame(self)
        self.container.setObjectName("Container")

        self.scroll_area = UiScrollArea(self)
        self.scroll_area.setWidget(self.container)

        v_layout = QVBoxLayout()
        v_layout.setContentsMargins(0, 0, 0, 0)
        v_layout.addWidget(self.scroll_area)
        self.setLayout(v_layout)

    def set_container_layout(self, layout):
        self.container.setLayout(layout)
        self.container.adjustSize()
        self.scroll_area.setWidget(self.container)
        self.update_size()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.update_size()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self.update_size()

    def update_size(self):
        viewport_width = self.scroll_area.viewport().width()
        self.container.setFixedWidth(viewport_width)
