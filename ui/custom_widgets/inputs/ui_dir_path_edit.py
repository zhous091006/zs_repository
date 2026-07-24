from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFileDialog

from lib.lib_func import lib_func_t
# from lib.lib_translation import tr
from ui.custom_widgets.buttons.ui_push_button import UiPushButton
from ui.custom_widgets.inputs.ui_line_edit import UiLineEdit


class UiDirPathEdit(QWidget):
    def __init__(self, caption, parent):
        """

        :param caption: 关键词
        :param parent:
        """
        super().__init__(parent)
        self.caption = caption

        self.file_path_edit = UiLineEdit(self)
        self.file_path_edit.setAttribute(Qt.WA_InputMethodEnabled, False)
        self.file_path_edit.set_validity_check(UiLineEdit.CHECK_DIR)

        # self.file_path_select_btn = UiPushButton(tr("Select..."), self)
        self.file_path_select_btn = UiPushButton(tr("Select..."), self)
        self.file_path_select_btn.setMinimumWidth(100)

        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.setSpacing(4)
        h_layout.addWidget(self.file_path_edit)
        h_layout.addWidget(self.file_path_select_btn)

        self.setLayout(h_layout)

        self.__init_connect()

    def __init_connect(self):
        self.file_path_select_btn.clicked.connect(self.open_select_dir_dialog)

    def open_select_dir_dialog(self):
        open_dir = self.file_path_edit.text()
        if not lib_func_t.is_path_existed(open_dir):
            open_dir = lib_func_t.get_desktop_path()
        dir_path = QFileDialog.getExistingDirectory(self, self.caption, open_dir)
        if dir_path:
            self.file_path_edit.setText(dir_path)

    def text(self) -> str:
        return self.file_path_edit.text()

    def set_text(self, text):
        self.file_path_edit.setText(text)

    def set_input_read_only(self, state):
        self.file_path_edit.setReadOnly(state)
