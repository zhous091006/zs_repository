from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QDialogButtonBox, QSizePolicy, qApp, QHBoxLayout, QFrame

# from lib.lib_translation import tr
from ui.custom_widgets.ui_dialog_base import UiDialogBase
from ui.custom_widgets.buttons.ui_push_button import UiPushButton


class UiMessageBox(UiDialogBase):
    LEVEL_INFO = "information"
    LEVEL_TIPS = "tip"
    LEVEL_QUESTION = "question"
    LEVEL_WARNING = "warning"
    LEVEL_ERROR = "error"

    ACCEPT_ROLE = QDialogButtonBox.AcceptRole
    REJECT_ROLE = QDialogButtonBox.RejectRole
    YES_ROLE = QDialogButtonBox.YesRole
    NO_ROLE = QDialogButtonBox.NoRole
    NULL_ROLE = QDialogButtonBox.InvalidRole

    def __init__(self, title, text, roles: list, default_role, parent=None, is_custom_roles_mode: bool = False):
        super().__init__(title, parent)

        self.roles = roles
        self.is_custom_roles_mode = is_custom_roles_mode
        self.clicked_button = None

        self.setMinimumSize(320, 180)
        self.set_min_btn_visible(False)
        self.set_max_btn_visible(False)
        self.set_close_btn_visible(False)

        self.icon_label = QLabel(self)
        self.icon_label.setObjectName("Icon")
        self.icon_label.setFixedWidth(32)
        self.icon_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.tips_label = QLabel(text, self)
        self.tips_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.tips_label.setWordWrap(True)

        h_layout1 = QHBoxLayout()
        h_layout1.setContentsMargins(6, 6, 6, 6)
        h_layout1.setSpacing(12)
        h_layout1.addWidget(self.icon_label)
        h_layout1.addWidget(self.tips_label)

        self.btn_box = QDialogButtonBox(self)
        # self.btn_box.setFixedHeight(36)
        self.btn_box.setContentsMargins(6, 6, 6, 6)
        self._add_buttons(roles)

        self.button_area = QFrame(self)
        self.button_area.setObjectName("ButtonArea")
        h_layout2 = QHBoxLayout()
        h_layout2.setContentsMargins(0, 0, 0, 0)
        h_layout2.addWidget(self.btn_box)
        self.button_area.setLayout(h_layout2)

        v_layout = QVBoxLayout()
        v_layout.setContentsMargins(1, 0, 1, 1)
        v_layout.setSpacing(20)
        v_layout.addLayout(h_layout1)
        v_layout.addWidget(self.button_area)

        self.body_widget.setLayout(v_layout)

        self.btn_box.clicked.connect(self.on_btn_clicked)
        self._set_default_btn(default_role)
        self.adjustSize()

        qApp.alert(self)

    def polish_level_style(self, level: str):
        self.icon_label.setProperty("level", level)
        self.style().unpolish(self.icon_label)
        self.style().polish(self.icon_label)
        self.body_widget.setProperty("level", level)
        self.style().unpolish(self.body_widget)
        self.style().polish(self.body_widget)

    def on_btn_clicked(self, btn):
        if self.is_custom_roles_mode:
            self.clicked_button = btn
            self.close()
        else:
            self.done(self.btn_box.buttonRole(btn))

    def reject(self) -> None:
        self.done(self.REJECT_ROLE)

    def _add_buttons(self, roles: list):
        if self.is_custom_roles_mode:
            for role in roles:
                btn = UiPushButton(role, self)
                btn.setMinimumWidth(80)
                self.btn_box.addButton(btn, 0)
        else:
            text_dict = {QDialogButtonBox.AcceptRole: "&OK",
                         QDialogButtonBox.RejectRole: "&Cancel",
                         QDialogButtonBox.YesRole: "&Yes",
                         QDialogButtonBox.NoRole: "&No"}
            for i in roles:
                btn = UiPushButton(text_dict.get(i), self)
                btn.setFixedWidth(80)
                self.btn_box.addButton(btn, i)

    def _set_default_btn(self, role):
        btn = self._get_btn_by_role(role)
        if btn:
            btn.setFocus()

    def _get_btn_by_role(self, role) -> [UiPushButton, None]:
        if isinstance(role, int):
            for btn in self.btn_box.buttons():
                if self.btn_box.buttonRole(btn) == role:
                    return btn
        elif isinstance(role, str):
            for btn in self.btn_box.buttons():
                if btn.text() == role:
                    return btn
        return None

    def keyPressEvent(self, event: QKeyEvent) -> None:
        key = event.key()
        btn = None
        if key == Qt.Key_O:
            btn = self._get_btn_by_role(UiMessageBox.ACCEPT_ROLE)
        elif key == Qt.Key_C:
            btn = self._get_btn_by_role(UiMessageBox.REJECT_ROLE)
        elif key == Qt.Key_Y:
            btn = self._get_btn_by_role(UiMessageBox.YES_ROLE)
        elif key == Qt.Key_N:
            btn = self._get_btn_by_role(UiMessageBox.NO_ROLE)
        if btn:
            btn.clicked.emit(True)
        super().keyPressEvent(event)

    def showEvent(self, event) -> None:
        qApp.alert(self)
        super().showEvent(event)

    @staticmethod
    def information(title="Information", text="", parent=None):
        # title = tr(title)
        dialog = UiMessageBox(title, text, [UiMessageBox.ACCEPT_ROLE], UiMessageBox.ACCEPT_ROLE, parent)
        dialog.polish_level_style("information")
        dialog.exec()

    @staticmethod
    def tip(title="Tips", text="", roles: list = None, default_role=NULL_ROLE, parent=None) -> bool:
        # title = tr(title)
        if roles is None:
            roles = [UiMessageBox.ACCEPT_ROLE, UiMessageBox.REJECT_ROLE]
        dialog = UiMessageBox(title, text, roles, default_role, parent)
        dialog.polish_level_style("information")
        ret = dialog.exec()
        if ret in [UiMessageBox.ACCEPT_ROLE, UiMessageBox.YES_ROLE]:
            return True
        return False

    @staticmethod
    def question(title="Question", text="", roles: list = None, default_role=NULL_ROLE, parent=None) -> bool:
        # title = tr(title)
        if roles is None:
            roles = [UiMessageBox.ACCEPT_ROLE, UiMessageBox.REJECT_ROLE]
        dialog = UiMessageBox(title, text, roles, default_role, parent)
        dialog.polish_level_style("question")
        ret = dialog.exec()
        if ret in [UiMessageBox.ACCEPT_ROLE, UiMessageBox.YES_ROLE]:
            return True
        return False

    @staticmethod
    def warning(title="Warning", text="", roles: list = None, default_role=NULL_ROLE, parent=None) -> bool:
        # title = tr(title)
        if roles is None:
            roles = [UiMessageBox.YES_ROLE, UiMessageBox.NO_ROLE]
        dialog = UiMessageBox(title, text, roles, default_role, parent)
        dialog.polish_level_style("warning")
        ret = dialog.exec()
        if ret in [UiMessageBox.ACCEPT_ROLE, UiMessageBox.YES_ROLE]:
            return True
        return False

    @staticmethod
    def error(title="Error", text="", parent=None):
        # title = tr(title)
        dialog = UiMessageBox(title, text, [UiMessageBox.ACCEPT_ROLE], UiMessageBox.ACCEPT_ROLE, parent)
        dialog.polish_level_style("error")
        dialog.exec()

    @staticmethod
    def custom_message(level=LEVEL_QUESTION, title="Question", text="", roles: List[str] = None, default_role=None, parent=None) -> str:
        # title = tr(title)
        if roles is None:
            roles = []
        dialog = UiMessageBox(title, text, roles, default_role, parent, True)
        dialog.polish_level_style(level)
        dialog.exec()
        if isinstance(dialog.clicked_button, UiPushButton):
            return dialog.clicked_button.text()
        return ""
