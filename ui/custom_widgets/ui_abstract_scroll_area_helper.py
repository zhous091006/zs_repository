from typing import Tuple

from PyQt5.QtCore import QObject, Qt, QEvent
from PyQt5.QtWidgets import QAbstractScrollArea, QScrollBar, QScroller, QScrollerProperties, QAbstractItemView


class UiAbstractScrollAreaHelper(QObject):
    def __init__(self, parent: QAbstractScrollArea):
        super().__init__(parent)
        self.abstract_scroll_area = parent
        self.scroll_bar_spacing = 2
        self.scroll_bar_width = 6
        self.custom_scroll_bar_auto_hide_flag = False

        self.abstract_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.abstract_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scroll_bar_v = QScrollBar(Qt.Vertical, self.abstract_scroll_area)
        self.scroll_bar_h = QScrollBar(Qt.Horizontal, self.abstract_scroll_area)

        self.__init_custom_scroll_bar_attribute()
        self.__install_scroll_grab_gesture()

        self.abstract_scroll_area.installEventFilter(self)

    def set_scroll_bar_spacing(self, spacing: int):
        self.scroll_bar_spacing = spacing
        self.__adjust_custom_scroll_bar_geometry()

    def set_scroll_bar_width(self, width: int):
        """
        设置滚动条宽度（粗细）
        :param width:
        :return:
        """
        self.scroll_bar_width = width
        self.__adjust_custom_scroll_bar_geometry()

    def locate_scroll_bar_v_range(self, begin: int, end: int, padding: Tuple[int] = (0, 0)):
        """
        改变重置滚动条的位置，使得位于 begin、end 范围的控件能够完全显示在 viewport 上
        :param begin:
        :param end:
        :param padding: begin、end 两端的空距
        :return:
        """
        scroll_pos = self.scroll_bar_v.value()
        if begin < scroll_pos:
            self.scroll_bar_v.setValue(begin + padding[0])
        elif end > scroll_pos + self.abstract_scroll_area.viewport().height():
            self.scroll_bar_v.setValue(begin - (self.abstract_scroll_area.viewport().height() - (end - begin)) + padding[1])

    def locate_scroll_bar_h_range(self, begin: int, end: int, padding: Tuple[int] = (0, 0)):
        """
        改变水平滚动条的位置，使得位于 begin、end 范围的控件能够完全显示在 viewport 上
        :param begin:
        :param end:
        :param padding: begin、end 两端的空距
        :return:
        """
        scroll_pos = self.scroll_bar_h.value()
        if begin < scroll_pos:
            self.scroll_bar_h.setValue(begin + padding[0])
        elif end > scroll_pos + self.abstract_scroll_area.viewport().width():
            self.scroll_bar_h.setValue(begin - (self.abstract_scroll_area.viewport().width() - (end - begin)) + padding[1])

    def set_custom_scroll_bar_auto_hide(self, flag: bool):
        self.custom_scroll_bar_auto_hide_flag = flag
        self.__update_custom_scroll_bar_visible()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if watched == self.abstract_scroll_area:
            if event.type() in (QEvent.Enter, QEvent.Leave):
                if self.custom_scroll_bar_auto_hide_flag:
                    self.__update_custom_scroll_bar_visible()
            elif event.type() in (QEvent.Resize, QEvent.Show):
                self.__update_custom_scroll_bar_visible()
                self.__adjust_custom_scroll_bar_geometry()
        return super().eventFilter(watched, event)

    def __init_custom_scroll_bar_attribute(self):
        real_v_scroll_bar = self.abstract_scroll_area.verticalScrollBar()
        real_h_scroll_bar = self.abstract_scroll_area.horizontalScrollBar()

        self.scroll_bar_v.setRange(real_v_scroll_bar.minimum(), real_v_scroll_bar.maximum())
        self.scroll_bar_v.setValue(real_v_scroll_bar.value())
        real_v_scroll_bar.valueChanged.connect(self.scroll_bar_v.setValue)
        self.scroll_bar_v.valueChanged.connect(real_v_scroll_bar.setValue)
        real_v_scroll_bar.rangeChanged.connect(self.scroll_bar_v.setRange)
        self.scroll_bar_v.valueChanged.connect(self.__update_custom_scroll_bar_visible)
        self.scroll_bar_v.rangeChanged.connect(self.__update_custom_scroll_bar_visible)
        self.scroll_bar_v.raise_()
        self.scroll_bar_v.setPageStep(400)

        self.scroll_bar_h.setRange(real_h_scroll_bar.minimum(), real_h_scroll_bar.maximum())
        self.scroll_bar_h.setValue(real_h_scroll_bar.value())
        real_h_scroll_bar.valueChanged.connect(self.scroll_bar_h.setValue)
        self.scroll_bar_h.valueChanged.connect(real_h_scroll_bar.setValue)
        real_h_scroll_bar.rangeChanged.connect(self.scroll_bar_h.setRange)
        self.scroll_bar_h.valueChanged.connect(self.__update_custom_scroll_bar_visible)
        self.scroll_bar_h.rangeChanged.connect(self.__update_custom_scroll_bar_visible)
        self.scroll_bar_h.raise_()
        self.scroll_bar_h.setPageStep(400)

    def __adjust_custom_scroll_bar_geometry(self):
        """
        调整自定义滚动条大小、位置
        :return:
        """
        s_h_h = self.scroll_bar_width
        s_v_w = self.scroll_bar_width
        s_v_h = self.abstract_scroll_area.height() - 2 - s_h_h - self.scroll_bar_spacing if self.scroll_bar_h.maximum() > 0 else self.abstract_scroll_area.height() - 2
        s_h_w = self.abstract_scroll_area.width() - 2 - s_v_w - self.scroll_bar_spacing if self.scroll_bar_v.maximum() > 0 else self.abstract_scroll_area.width() - 2
        self.scroll_bar_v.setGeometry(self.abstract_scroll_area.width() - self.scroll_bar_width - self.scroll_bar_spacing, 1, self.scroll_bar_width, s_v_h)
        self.scroll_bar_h.setGeometry(1, self.abstract_scroll_area.height() - self.scroll_bar_width - self.scroll_bar_spacing, s_h_w, self.scroll_bar_width)
        self.scroll_bar_v.raise_()
        self.scroll_bar_h.raise_()

    def __update_custom_scroll_bar_visible(self) -> None:
        if self.custom_scroll_bar_auto_hide_flag:
            if self.abstract_scroll_area.underMouse():
                if self.scroll_bar_v.maximum() > 0:
                    self.scroll_bar_v.show()
                if self.scroll_bar_h.maximum() > 0:
                    self.scroll_bar_h.show()
            else:
                self.scroll_bar_v.hide()
                self.scroll_bar_h.hide()
        else:
            self.scroll_bar_v.setVisible(self.scroll_bar_v.maximum() > 0)
            self.scroll_bar_h.setVisible(self.scroll_bar_h.maximum() > 0)
        self.__adjust_custom_scroll_bar_geometry()

    def __install_scroll_grab_gesture(self):
        """
        安装抓取滚动视图工具
        :return:
        """
        if isinstance(self.abstract_scroll_area, QAbstractItemView):
            self.abstract_scroll_area.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
            self.abstract_scroll_area.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        scroller: QScroller = QScroller.scroller(self.abstract_scroll_area.viewport())
        scroller.grabGesture(self.abstract_scroll_area.viewport(), QScroller.LeftMouseButtonGesture)
        scroller_properties = QScrollerProperties()
        scroller_properties.setScrollMetric(QScrollerProperties.HorizontalOvershootPolicy, QScrollerProperties.OvershootAlwaysOff)
        scroller_properties.setScrollMetric(QScrollerProperties.VerticalOvershootPolicy, QScrollerProperties.OvershootAlwaysOff)
        scroller.setScrollerProperties(scroller_properties)
