from typing import List

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QFrame, QWidget, QVBoxLayout, QLayout

from ui.custom_widgets.ui_scroll_area import UiScrollArea


class UiDrawerBox(QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.widgets: List[QWidget] = []

        self.v_layout = QVBoxLayout()
        self.v_layout.setSpacing(0)
        self.v_layout.setContentsMargins(0, 0, 0, 0)
        self.v_layout.setSizeConstraint(QLayout.SetFixedSize)

        self.container = QFrame(self)
        self.container.setObjectName("Container")
        self.container.setLayout(self.v_layout)

        self.scroll_area = UiScrollArea(self)
        self.scroll_area.setWidget(self.container)

        v_layout = QVBoxLayout()
        v_layout.setContentsMargins(0, 0, 0, 0)
        v_layout.addWidget(self.scroll_area)
        self.setLayout(v_layout)

    def append_item(self, w: QWidget):
        if isinstance(w, QWidget):
            self.widgets.append(w)
            wrap_item = UiDrawerItem(w, self)
            self.v_layout.addWidget(wrap_item)
            self.container.setLayout(self.v_layout)
            self.container.adjustSize()
            self.scroll_area.setWidget(self.container)
            self.update_size()

    def insert_item(self, index, w: QWidget):
        if isinstance(w, QWidget):
            self.widgets.insert(index, w)
            wrap_item = UiDrawerItem(w, self)
            self.v_layout.insertWidget(index, wrap_item)
            self.container.setLayout(self.v_layout)
            self.container.adjustSize()
            self.scroll_area.setWidget(self.container)
            self.update_size()

    def remove_item(self, w: QWidget):
        if w in self.widgets:
            wrap_item = self.wrap_widget(w)
            if isinstance(wrap_item, UiDrawerItem) and wrap_item.w == w:
                self.v_layout.removeWidget(wrap_item)
                self.widgets.remove(w)
                w.setParent(None)
                wrap_item.deleteLater()
                self.container.setLayout(self.v_layout)
                self.container.adjustSize()
                self.scroll_area.setWidget(self.container)
                self.update_size()

    def wrap_widget(self, w: QWidget):
        i = self.widgets.index(w)
        wrap_widget = self.v_layout.itemAt(i).widget()
        return wrap_widget

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.update_size()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self.update_size()

    def update_size(self):
        viewport_width = self.scroll_area.viewport().width()
        self.container.setFixedWidth(viewport_width)
        for i in range(self.v_layout.count()):
            self.v_layout.itemAt(i).widget().set_fixed_width(viewport_width)


class UiDrawerItem(QWidget):
    def __init__(self, w, parent):
        super().__init__(parent)
        self.w = w
        self.width_hint = 10
        self.v_layout = QVBoxLayout()
        self.v_layout.setContentsMargins(0, 0, 0, 0)
        self.v_layout.addWidget(w)
        self.setLayout(self.v_layout)

    def set_fixed_width(self, width):
        self.width_hint = width
        self.setFixedWidth(width)

    def sizeHint(self) -> QSize:
        s = super().sizeHint()
        s.setWidth(self.width_hint)
        return s

    def minimumSizeHint(self) -> QSize:
        s = super().minimumSizeHint()
        s.setWidth(self.width_hint)
        return s
