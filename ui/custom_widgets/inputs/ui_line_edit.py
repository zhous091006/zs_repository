import os
import re
from typing import Dict, List

from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QLineEdit

# from cfg.cfg_if import cfg_if


class UiLineEdit(QLineEdit):
    CHECK_IP = "IP"
    CHECK_PORT = "PORT"
    CHECK_FILE = "FILE"
    CHECK_REAL_FILE = "REAL_FILE"
    CHECK_DIR = "DIR"
    CHECK_NUMBER = "NUMBER"
    CHECK_SERIAL_NUMBER = "SERIAL_NUMBER"

    def __init__(self, *args):
        super().__init__(*args)

        self.validity_check = None
        self.config_bind: Dict[str, List[str]] = {}  # 与配置文件绑定，文本改变后自动更新配置文件

        # self.setFixedHeight(26)
        self.textEdited.connect(self.on_text_edited)
        self.editingFinished.connect(self.on_editing_finished)
        self.textChanged.connect(self.on_text_changed)

        self.tmp_text_edited_status = False

    def setReadOnly(self, state: bool) -> None:
        super().setReadOnly(state)
        self.deal_validity_check()

    def is_empty(self):
        return self.text() == ""

    def on_text_edited(self):
        self.tmp_text_edited_status = True
        self.deal_validity_check()

    def on_text_changed(self):
        if not self.tmp_text_edited_status:
            self.deal_validity_check()
            self.deal_bound_configs()

    def on_editing_finished(self):
        if self.tmp_text_edited_status:
            self.deal_validity_check()
            self.deal_bound_configs()
        self.tmp_text_edited_status = False

    def bind_config(self, config_filepath: str, keys: List[str]):
        self.config_bind[config_filepath] = keys

    def set_validity_check(self, check_type: str):
        self.validity_check = check_type
        self.deal_validity_check()

    def deal_bound_configs(self):
        for config, keys in self.config_bind.items():
            pass
            # cfg_if.write_config(config, keys, self.text())

    def deal_validity_check(self):
        is_valid = True
        if self.validity_check == UiLineEdit.CHECK_IP:
            is_valid = self.is_ip_valid(self.text())
        elif self.validity_check == UiLineEdit.CHECK_PORT:
            is_valid = self.is_port_valid(self.text())
        elif self.validity_check == UiLineEdit.CHECK_FILE:
            is_valid = self.is_filepath_valid(self.text())
        elif self.validity_check == UiLineEdit.CHECK_REAL_FILE:
            is_valid = self.is_filepath_valid(self.text(), is_existed=True)
        elif self.validity_check == UiLineEdit.CHECK_DIR:
            is_valid = self.is_dir_valid(self.text())
        elif self.validity_check == UiLineEdit.CHECK_NUMBER:
            is_valid = self.is_number(self.text())
        elif self.validity_check == UiLineEdit.CHECK_SERIAL_NUMBER:
            is_valid = self.is_serial_number(self.text())
        # 这段代码用于‌在 PyQt/PySide 中动态修改控件属性后强制刷新 QSS 样式‌，解决 setProperty 变更不自动触发视觉更新的问题
        self.setProperty("valid", is_valid)
        self.style().unpolish(self)
        self.style().polish(self)

    def is_content_valid(self) -> bool:
        return self.property("valid")

    def enterEvent(self, event: QEvent) -> None:
        # if self.isEnabled() and not self.isReadOnly():
        #     ui_func_t.set_border_shadow_effect(self, color=QColor("#888"), radius=10)
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        # if not self.hasFocus():
        #     self.setGraphicsEffect(None)
        super().leaveEvent(event)

    def focusInEvent(self, event) -> None:
        # if self.isEnabled() and not self.isReadOnly():
        #     ui_func_t.set_border_shadow_effect(self, color=QColor("#888"), radius=10)
        super().focusInEvent(event)

    def focusOutEvent(self, event) -> None:
        # self.setGraphicsEffect(None)
        super().focusOutEvent(event)

    @classmethod
    def create_edit(cls, parent, text="", height=None, width=None):
        edit = cls(text, parent)
        if height:
            edit.setFixedHeight(height)
        if width:
            edit.setFixedWidth(width)
        return edit

    @staticmethod
    def is_serial_number(s: str) -> bool:
        """
        限定序列号为字母数字组合
        """
        return bool(re.match(r"^[0-9a-zA-Z-]*$", s))

    @staticmethod
    def is_number(s: str) -> bool:
        m = re.match(r"^[0-9][0-9]*$", s)
        if m:
            return True
        return False

    @staticmethod
    def is_ip_valid(ip: str) -> bool:
        is_empty = bool(ip == "")
        is_localhost = bool(ip == "localhost")
        is_ip = bool(re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ip))
        is_valid = not is_empty and (is_ip or is_localhost)
        return is_valid

    @staticmethod
    def is_port_valid(port: str) -> bool:
        m = re.match(r"^[0-9][0-9]*$", port)
        if m:
            port_val = int(port)
            return 0 <= port_val <= 65535
        return False

    @staticmethod
    def is_filepath_valid(filepath: str, is_existed=False) -> bool:
        """
        判断文件路径是否有效
        :param filepath: 文件路径
        :param is_existed: 是否需要为真实文件
        """
        if os.path.isdir(filepath):
            return False
        if is_existed:
            return os.path.exists(filepath)
        file_dir = os.path.dirname(filepath)
        if os.path.exists(file_dir):
            if os.path.basename(filepath):
                return True
        return False

    @staticmethod
    def is_dir_valid(dir_path: str) -> bool:
        return os.path.exists(dir_path)
