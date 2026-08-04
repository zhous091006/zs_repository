from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFrame, QStackedLayout, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy

from lib.lib_type import LIB_IMAGE_DIR
from ui.custom_widgets.buttons.ui_tool_button import UiToolButton


class UiStackedItemPageHeader(QFrame):
    def __init__(self, title, parent):
        super().__init__(parent)
        self.return_btn = UiToolButton(self)
        self.return_btn.setObjectName("Style2")
        self.return_btn.set_icon(QIcon(LIB_IMAGE_DIR + "\\back_32.svg"), QSize(12, 12))
        self.return_btn.setFixedSize(20, 20)
        self.return_btn.set_shadow_enabled(False)
        self.title_label = QLabel(title, self)

        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(4, 4, 4, 4)
        h_layout.setSpacing(0)
        h_layout.addWidget(self.return_btn)
        h_layout.addStretch(1)
        h_layout.addWidget(self.title_label)
        h_layout.addStretch(1)
        h_layout.addSpacing(20)

        self.setLayout(h_layout)

        # ui_func_t.set_border_shadow_effect(self, offset_y=2, color=QColor("#e5e5e5"))


class UiStackedItemPage(QFrame):
    sig_close = pyqtSignal()

    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.header = UiStackedItemPageHeader(title, self)
        self.header.return_btn.clicked.connect(self.close_page)
        self.body = QFrame(self)
        self.body.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        v_layout = QVBoxLayout()
        v_layout.setContentsMargins(0, 0, 0, 0)
        v_layout.setSpacing(0)
        v_layout.addWidget(self.header)
        v_layout.addWidget(self.body)
        self.setLayout(v_layout)

    def open_page(self, page):
        assert isinstance(self.parent(), UiStackedPageContainer)
        self.parent().add_page(page)

    def close_page(self):
        self.close()

    def closeEvent(self, event) -> None:
        super().closeEvent(event)
        self.sig_close.emit()


class UiStackedPageContainer(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.page_index_map = {}
        self.stacked_layout = QStackedLayout()
        self.setLayout(self.stacked_layout)

    def add_page(self, page: UiStackedItemPage):
        assert isinstance(page, UiStackedItemPage)
        page.setParent(self)
        page.sig_close.connect(lambda: self.del_page(page))
        index = self.stacked_layout.addWidget(page)
        self.page_index_map[page] = index
        self.stacked_layout.setCurrentIndex(index)

    def del_page(self, page: UiStackedItemPage):
        assert isinstance(page, UiStackedItemPage)
        self.stacked_layout.removeWidget(page)
        self.page_index_map.pop(page)
        page.deleteLater()
