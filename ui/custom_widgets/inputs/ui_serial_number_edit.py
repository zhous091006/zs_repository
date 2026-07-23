from PyQt5.QtCore import Qt

from ui.custom_widgets.inputs.ui_line_edit import UiLineEdit


class UiSerialNumberEdit(UiLineEdit):
    def __init__(self, *args):
        super().__init__(*args)

        self.setAttribute(Qt.WA_InputMethodEnabled, False)
        self.set_validity_check(UiLineEdit.CHECK_SERIAL_NUMBER)

    def set_read_only(self, state: bool):
        self.setReadOnly(state)
        self.setAttribute(Qt.WA_InputMethodEnabled, False)  # 设置只读状态后需要重新设置输入方法模式
