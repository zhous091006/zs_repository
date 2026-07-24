from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFileDialog

from lib.lib_func import lib_func_t
# from lib.lib_translation import tr
from ui.custom_widgets.buttons.ui_push_button import UiPushButton
from ui.custom_widgets.inputs.ui_line_edit import UiLineEdit


class UiFilePathEdit(QWidget):
    def __init__(self, caption, file_filter, is_real_file: bool, parent):
        """
        文件路径编辑框
        :param caption: 关键词
        :param file_filter: 文件过滤（‘;;’分隔不同文件类型） e.g. "Images (*.png *.xpm *.jpg);;Text files (*.txt);;XML files (*.xml)"
        :param parent:
        """
        super().__init__(parent)
        self.caption = caption
        self.file_filter = file_filter
        self.is_real_file = is_real_file

        self.file_path_edit = UiLineEdit(self)
        self.file_path_edit.setAttribute(Qt.WA_InputMethodEnabled, False)

        if self.is_real_file:
            self.file_path_edit.set_validity_check(UiLineEdit.CHECK_REAL_FILE)
        else:
            self.file_path_edit.set_validity_check(UiLineEdit.CHECK_FILE)

        # self.file_path_select_btn = UiPushButton(tr("Select..."), self)
        self.file_path_select_btn = UiPushButton(("Select..."), self)
        self.file_path_select_btn.setMinimumWidth(100)

        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.setSpacing(4)
        h_layout.addWidget(self.file_path_edit)
        h_layout.addWidget(self.file_path_select_btn)

        self.setLayout(h_layout)

        self.__init_connect()

    def __init_connect(self):
        self.file_path_select_btn.clicked.connect(self.open_select_file_dialog)

    def open_select_file_dialog(self):
        open_dir = lib_func_t.get_file_dir(self.file_path_edit.text())
        if not lib_func_t.is_path_existed(open_dir):
            open_dir = lib_func_t.get_desktop_path()
        filepath, file_filter = QFileDialog.getOpenFileName(self, self.caption, open_dir, self.file_filter)
        self.file_path_edit.setText(filepath)

    def text(self) -> str:
        return self.file_path_edit.text()

    def set_text(self, text):
        self.file_path_edit.setText(text)

    def set_input_read_only(self, state):
        self.file_path_edit.setReadOnly(state)
