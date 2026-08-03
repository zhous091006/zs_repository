from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtWidgets import QListWidget

from ui.custom_widgets.ui_abstract_scroll_area_helper import UiAbstractScrollAreaHelper


class UiListWidget(QListWidget):
    sig_resized = pyqtSignal(QSize)

    def __init__(self, parent):
        super().__init__(parent=parent)

        self.widget_helper = UiAbstractScrollAreaHelper(self)
