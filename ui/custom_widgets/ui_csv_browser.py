import datetime
import os
import re
from copy import deepcopy
from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextOption, QKeyEvent
from PyQt5.QtWidgets import QTextBrowser, QScroller, QScrollerProperties

from lib.lib_func import lib_func_t
from lib.lib_type import LIB_CSS_DIR

color_list = ["#1976D2", "#F37600", "#00C853", "#B487FF", "#F8AE68",
              "#1B5E20", "#FF5722", "#5E35B1", "#d258be", "#827717"]


class RowData:
    BLANK = "blank"
    NOTES = "notes"
    TITLES = "titles"
    DATA = "data"

    __slots__ = 'data', 'type', 'class_list'

    def __init__(self, data: List[str], data_type=None):
        self.data = data
        if data_type:
            self.type = data_type
        else:
            if len(data) == 0:
                self.type = self.BLANK
            else:
                if data[0].startswith("!"):
                    self.type = self.NOTES
                elif data[0].startswith("#"):
                    self.type = self.TITLES
                else:
                    self.type = self.DATA
        self.class_list = ""


class UiCsvBrowser(QTextBrowser):
    def __init__(self, parent):
        super().__init__(parent)

        self.raw_data: List[RowData] = []
        self.equal_width_data: List[RowData] = []
        self.format_data: List[RowData] = []
        self.be_formatted = False
        self.selected_lines: List[int] = []
        self.ctrl_pressed = False

        self.setWordWrapMode(QTextOption.NoWrap)
        self.__install_scroll_grab_gesture()

        self.cursorPositionChanged.connect(self.on_text_cursor_pos_changed)

    def on_text_cursor_pos_changed(self):
        if not self.be_formatted:
            return
        tc = self.textCursor()
        ty = tc.block().layout()
        line_num = ty.lineForTextPosition(tc.positionInBlock()).lineNumber() + tc.block().firstLineNumber()
        if self.ctrl_pressed:
            if line_num in self.selected_lines:
                self.selected_lines.remove(line_num)
            else:
                self.selected_lines.append(line_num)
        else:
            self.selected_lines = [line_num]
        v_scroll_bar_value = self.verticalScrollBar().value()
        h_scroll_bar_value = self.horizontalScrollBar().value()
        self.cursorPositionChanged.disconnect(self.on_text_cursor_pos_changed)
        self.setUpdatesEnabled(False)
        self.setHtml(self.render_data())
        self.setUpdatesEnabled(True)
        self.cursorPositionChanged.connect(self.on_text_cursor_pos_changed)
        self.verticalScrollBar().setValue(v_scroll_bar_value)
        self.horizontalScrollBar().setValue(h_scroll_bar_value)

    def read_file(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            raw_data_str = f.read()
        self.read_content(raw_data_str)

    def read_content(self, content: str):
        if not isinstance(content, str):
            return

        self.raw_data.clear()
        row_list = content.strip().split("\n")

        for row_data in row_list:
            item_list = lib_func_t.parse_csv_line_text(row_data)
            self.raw_data.append(RowData(item_list))

        if self.be_formatted:
            self.convert_raw_data_to_equal_width()
            self.convert_equal_width_data_to_format()

        self.setUpdatesEnabled(False)
        self.setHtml(self.render_data())
        self.setUpdatesEnabled(True)

    def convert_raw_data_to_equal_width(self):
        self.equal_width_data = deepcopy(self.raw_data)

        ignored_rows = []

        # 获取最大列数
        max_col_counts = 0
        for i in range(len(self.equal_width_data)):
            row = self.equal_width_data[i].data
            length = len(row)
            if length == 0 or row[0].startswith("!"):
                ignored_rows.append(i)
            max_col_counts = length if (length > max_col_counts) else max_col_counts

        # 获取每一列的最大字符串长度行，并同化长度至其他行
        for i in range(max_col_counts):
            max_str_len = 0
            for r in range(len(self.equal_width_data)):  # 找出最长的字符串
                row_data = self.equal_width_data[r].data
                if r not in ignored_rows and len(row_data) > i:
                    str_len = len(row_data[i])
                    max_str_len = str_len if (str_len > max_str_len) else max_str_len
            max_str_len += 1
            for r in range(len(self.equal_width_data)):  # 填充其他字符串
                row_data = self.equal_width_data[r].data
                if r not in ignored_rows and len(row_data) > i:
                    item = row_data[i]
                    if item.startswith("#"):
                        self.equal_width_data[r].data[i] = "#" + " " * (max_str_len - len(item)) + item[1:]
                    elif item:
                        self.equal_width_data[r].data[i] = " " * (max_str_len - len(item)) + item

    def convert_equal_width_data_to_format(self):
        self.format_data.clear()
        for row_data in self.equal_width_data:
            if row_data.type == RowData.NOTES:  # 注释
                self.format_data.append(RowData([UiCsvBrowser.get_span(", ".join(row_data.data))], data_type=row_data.type))
                continue

            is_titles = row_data.type == RowData.TITLES  # 标题
            is_failed = self.check_is_failed(row_data)

            html_data_list = []
            if is_titles:
                for data in row_data.data:
                    html_data_list.append(UiCsvBrowser.get_span(data))
            elif is_failed:
                for data in row_data.data:
                    html_data_list.append(UiCsvBrowser.get_span(data))
            else:
                for i, data in enumerate(row_data.data):
                    html_data_list.append(UiCsvBrowser.get_span(data, class_name=f'c{i % 10}'))

            if len(row_data.data) != 0:
                if len(row_data.data) == 1 and row_data.data[0] == "":
                    s = ""
                else:
                    s = "|" + "|".join(html_data_list) + "|"
            else:
                s = ""
            self.format_data.append(RowData([s], data_type=row_data.type))

    def render_data(self):
        final_data_list = []
        if self.be_formatted:
            for row_data in self.format_data:
                class_name = ['r-data', 'underline']
                if row_data.type == RowData.NOTES:
                    class_name.append('r-notes')
                elif row_data.type == RowData.TITLES:
                    class_name.append('r-title')
                elif row_data.type == RowData.DATA:
                    if self.check_is_failed(row_data):
                        class_name.append('fail')
                        if self.check_is_selected(row_data):
                            class_name.append('selected')
                    elif self.format_data.index(row_data) in self.selected_lines:
                        class_name.append('selected')
                    else:
                        pass
                class_name = ' '.join(class_name)
                if class_name:
                    s = f"<span class='{class_name}'>" + "|".join(row_data.data) + "</span><br>"
                else:
                    s = f"<span>" + "|".join(row_data.data) + "</span><br>"
                final_data_list.append(s)
            final_data_str = "\n".join(final_data_list)
        else:
            _get_span_func = self.get_span
            for row_data in self.raw_data:
                html_data_list = []
                for i, text in enumerate(row_data.data):
                    html_data_list.append(_get_span_func(text, class_name=f"item c{i % 10}"))
                s = ",".join(html_data_list) + "<br>"
                final_data_list.append(s)
            _lines = '\n'.join(final_data_list)
            final_data_str = f"<p style='color:#666'>{_lines}</p>"

        css_file_path = os.path.abspath(LIB_CSS_DIR + f"/csv_viewer/style.css")
        css_file_path = os.path.relpath(css_file_path, os.curdir)
        html = f'''<!DOCTYPE><html><head><link rel="stylesheet" type="text/css" href="{css_file_path}"></head><body>{final_data_str}</body></html>'''
        with open("./xxx.html", "w") as f:
            f.write(html)

        return html

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Control:
            self.ctrl_pressed = True
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Control:
            self.ctrl_pressed = False
        super().keyPressEvent(event)

    @staticmethod
    def get_span(text: str, class_name: str = ""):
        text = text.replace(" ", "&nbsp;")
        _class_attr = f" class='{class_name}'" if class_name else ""
        span_text = f"<span{_class_attr}>{text}</span>"
        return span_text

    @staticmethod
    def check_is_failed(row_data: RowData):
        return re.findall(r"FAIL", "".join(row_data.data), flags=re.I)

    def check_is_selected(self, row_data: RowData):
        return self.format_data.index(row_data) in self.selected_lines

    @staticmethod
    def __get_item_value(data: List[RowData], row, column):
        if len(data) < row or len(data[row].data) < column:
            return None
        return data[row].data[column]

    @staticmethod
    def __set_item_value(data: List[RowData], row, column, value):
        if len(data) >= row and len(data[row].data) >= column:
            data[row].data[column] = value

    def __install_scroll_grab_gesture(self):
        scroller: QScroller = QScroller.scroller(self.viewport())
        scroller.grabGesture(self.viewport(), QScroller.LeftMouseButtonGesture)
        scroller_properties = QScrollerProperties()
        scroller_properties.setScrollMetric(QScrollerProperties.HorizontalOvershootPolicy,
                                            QScrollerProperties.OvershootAlwaysOff)
        scroller_properties.setScrollMetric(QScrollerProperties.VerticalOvershootPolicy,
                                            QScrollerProperties.OvershootAlwaysOff)
        scroller.setScrollerProperties(scroller_properties)
