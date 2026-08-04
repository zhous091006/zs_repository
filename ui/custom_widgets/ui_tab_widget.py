from typing import Dict

from PyQt5 import sip
from PyQt5.QtCore import pyqtSignal, QSize, QEventLoop, Qt
from PyQt5.QtGui import QWheelEvent, QIcon
from PyQt5.QtWidgets import QFrame, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy, QStackedLayout, QWidget, QLayout, qApp

from lib.lib_linked_list import LibLinkedList
from lib.lib_type import LIB_IMAGE_DIR
from ui.custom_widgets.buttons.ui_font_icon_button import UiFontIconButton
from ui.custom_widgets.ui_scroll_frame import UiHorizontalScrollFrame
# from ui.lib.ui_func import ui_func_t

"""
                        UiTabWidget
    |————————————————————————————————————————————————|
    |  UiTab  |  UiTab  |  ...  |                    |  <-  UiTabBar
    |————————————————————————————————————————————————|
    |                                                |
    |                                                |
    |                                                |
    |————————————————————————————————————————————————|
"""


class UiTab(QPushButton):
    def __init__(self, text: str, icon: QIcon, parent):
        super().__init__(text, parent)

        self.setCursor(Qt.PointingHandCursor)

        if icon:
            self.setIcon(icon)

        self.close_btn = UiFontIconButton(UiFontIconButton.CLOSE, self)
        self.close_btn.setObjectName("CloseBtn")
        self.close_btn.setFixedSize(14, 14)

        self.h_layout = QHBoxLayout()
        self.h_layout.setContentsMargins(0, 0, 6, 0)
        self.h_layout.addStretch(1)
        self.h_layout.addWidget(self.close_btn)
        self.setLayout(self.h_layout)

        self.set_closeable(True)

    def set_closeable(self, enable):
        self.close_btn.setVisible(enable)
        # ui_func_t.set_property(self, name="closeable", value=enable)


class UiTabBar(UiHorizontalScrollFrame):
    sig_current_tab_changed = pyqtSignal(UiTab)
    sig_tab_removed = pyqtSignal(UiTab)

    def __init__(self, parent):
        super().__init__(parent)

        self.scroll_area.widget_helper.set_scroll_bar_spacing(0)
        self.scroll_area.widget_helper.set_scroll_bar_width(4)
        self.scroll_area.widget_helper.set_custom_scroll_bar_auto_hide(True)

        self.tab_list: LibLinkedList = LibLinkedList()
        self.active_tab = None

        self.setFixedHeight(28)

        self.__update_layout()

    def __update_layout(self):
        tabs_layout = QHBoxLayout()
        tabs_layout.setSpacing(0)
        tabs_layout.setContentsMargins(0, 0, 0, 0)
        tabs_layout.setSizeConstraint(QLayout.SetFixedSize)
        for node in self.tab_list.items():
            tabs_layout.addWidget(node.data)
        self.set_container_layout(tabs_layout)

    def __create_tab(self, text, icon: QIcon):
        tab = UiTab(text, icon, self)
        tab.setObjectName("TabButton")
        tab.setProperty("selected", False)
        tab.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        tab.setMinimumWidth(120)
        tab.setMinimumHeight(self.height())
        tab.pressed.connect(lambda: self.set_current_tab(tab))
        tab.close_btn.clicked.connect(lambda: self.remove_tab(tab))
        return tab

    def add_tab(self, text, icon: QIcon = None) -> UiTab:
        tab = self.__create_tab(text, icon)
        tab.raise_()
        self.tab_list.append_data(tab)
        self.__update_layout()
        self.scroll_to_tab(self.active_tab)
        self.update()
        qApp.processEvents(QEventLoop.ExcludeUserInputEvents)
        return tab

    def set_current_tab(self, tab: UiTab):
        if not self.tab_list.is_data_existed(tab):
            return False
        if self.active_tab == tab:
            return self.scroll_to_tab(tab)
        if isinstance(self.active_tab, UiTab):
            self.active_tab.setProperty("selected", False)
            self.active_tab.style().unpolish(self.active_tab)
            self.active_tab.style().polish(self.active_tab)
        self.active_tab = tab
        self.active_tab.setProperty("selected", True)
        self.active_tab.style().unpolish(self.active_tab)
        self.active_tab.style().polish(self.active_tab)
        self.sig_current_tab_changed.emit(self.active_tab)
        return self.scroll_to_tab(tab)

    def get_active_tab(self) -> [UiTab, None]:
        return self.active_tab

    def get_tab_index(self, tab: UiTab) -> int:
        i = 0
        for node in self.tab_list.items():
            if node.data == tab:
                return i
            i += 1
        return -1

    def get_tab_by_index(self, index: int) -> [UiTab, None]:
        i = 0
        for node in self.tab_list.items():
            if i == index:
                return node.data
            i += 1
        return None

    def set_active_tab_by_index(self, index: int) -> bool:
        return self.set_current_tab(self.get_tab_by_index(index))

    def set_tab_alert_state(self, index: int, state: bool):
        tab = self.get_tab_by_index(index)
        if tab:
            if state:
                tab.setIcon(QIcon(LIB_IMAGE_DIR + "\\rocket_18_12.svg"))
                tab.setIconSize(QSize(18, 12))
            else:
                tab.setIcon(QIcon())

    def set_tab_visible(self, index: int, visible: bool) -> None:
        tab = self.get_tab_by_index(index)
        if not isinstance(tab, UiTab) or visible == self.isVisible():
            return
        if visible:
            tab.setVisible(True)
        else:
            if self.get_active_tab() == tab:
                self.set_active_tab_by_index(index + 1) or self.set_active_tab_by_index(index - 1)
            tab.setVisible(False)

    def remove_tab(self, tab: UiTab):
        node = self.tab_list.get_node_by_data(tab)
        if self.tab_list.is_node_existed(node):
            if tab == self.active_tab:
                index = self.get_tab_index(tab)
                if index == 0:
                    self.set_current_tab(node.next.data)
                else:
                    self.set_current_tab(node.prev.data)
            self.tab_list.remove_data(tab)
            self.container.layout().removeWidget(tab)
            self.sig_tab_removed.emit(tab)
            tab.close()
            tab.deleteLater()
            if self.tab_list.size() == 0:
                self.active_tab = None

    def remove_tab_by_index(self, index):
        self.remove_tab(self.get_tab_by_index(index))

    def wheelEvent(self, event: QWheelEvent) -> None:
        if event.angleDelta().y() < 0:
            self.set_current_tab(self.tab_list.get_node_by_data(self.active_tab).next.data)
        else:
            self.set_current_tab(self.tab_list.get_node_by_data(self.active_tab).prev.data)

    def scroll_to_tab(self, tab: UiTab) -> bool:
        """
        滚动条滚动到指定的 Tab 位置
        :param tab:
        :return:
        """
        if not isinstance(tab, UiTab):
            return False
        widget_geometry = tab.geometry()
        self.scroll_area.widget_helper.locate_scroll_bar_h_range(begin=widget_geometry.left(), end=widget_geometry.right())
        return True


class UiTabWidget(QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.tab_page_dict: Dict[UiTab, QWidget] = {}

        self.tab_bar = UiTabBar(self)
        self.tab_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.body = QFrame(self)
        self.body.setObjectName("Body")
        self.body.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        v_layout = QVBoxLayout()
        v_layout.setSpacing(0)
        v_layout.setContentsMargins(0, 0, 0, 0)
        v_layout.addWidget(self.tab_bar)
        v_layout.addWidget(self.body)

        self.setLayout(v_layout)

        self.__init_connect()
        self.__update_layout()

    def __update_layout(self):
        if isinstance(self.body.layout(), QLayout):
            sip.delete(self.body.layout())
        s_layout = QStackedLayout()
        for node in self.tab_bar.tab_list.items():
            s_layout.addWidget(self.tab_page_dict[node.data])
        self.body.setLayout(s_layout)
        self.adjustSize()

    def __init_connect(self):
        self.tab_bar.sig_current_tab_changed.connect(self.__update_current_page)
        self.tab_bar.sig_tab_removed.connect(self.__on_tab_removed)

    def append_tab(self, page: QWidget, label: str, icon: QIcon = None) -> int:
        tab = self.tab_bar.add_tab(label, icon)
        self.tab_page_dict[tab] = page
        self.__update_layout()
        self.tab_bar.set_current_tab(tab)
        return self.tab_bar.tab_list.size() - 1

    def remove_tab(self, index):
        self.tab_bar.remove_tab_by_index(index)

    def set_tab_visible(self, index: int, visible: bool) -> None:
        self.tab_bar.set_tab_visible(index, visible)

    def set_tab_closeable(self, index, enable):
        tab = self.tab_bar.get_tab_by_index(index)
        if isinstance(tab, UiTab):
            tab.set_closeable(enable)

    def set_current_tab(self, index: int) -> bool:
        return self.tab_bar.set_active_tab_by_index(index)

    def get_active_index(self):
        return self.tab_bar.get_tab_index(self.tab_bar.get_active_tab())

    def get_page_by_index(self, index: int) -> QWidget:
        return self.tab_page_dict.get(self.tab_bar.get_tab_by_index(index), None)

    def set_tab_alert_state(self, argv, state: bool):
        if isinstance(argv, int):
            self.tab_bar.set_tab_alert_state(argv, state)
        elif isinstance(argv, QWidget):
            self.tab_bar.set_tab_alert_state(self.get_widget_index(argv), state)

    def get_widget_index(self, widget: QWidget):
        return self.body.layout().indexOf(widget)

    def __update_current_page(self):
        active_tab = self.tab_bar.get_active_tab()
        if active_tab is not None:
            self.body.layout().setCurrentWidget(self.tab_page_dict[active_tab])

    def __on_tab_removed(self, tab: UiTab):
        page = self.tab_page_dict[tab]
        self.body.layout().removeWidget(page)
        page.close()
        page.deleteLater()
        self.tab_page_dict.pop(tab)
