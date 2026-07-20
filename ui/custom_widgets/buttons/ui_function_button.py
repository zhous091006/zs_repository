from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QSizePolicy

from lib.lib_type import LIB_IMAGE_DIR
from ui.custom_widgets.buttons.ui_push_button import UiPushButton
from ui.custom_widgets.ui_waiting_animation_widget import UiWaitingAnimationWidget


class UiFunctionButton(UiPushButton):
    def __init__(self, text, parent):
        super().__init__(text, parent)
        self.original_text = text
        self.is_running = False
        self.is_finished = False
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.__animation = UiWaitingAnimationWidget(self)
        self.__animation.setFixedSize(16, 16)
        self.__animation.set_color(QColor("#0f0"))
        self.update_ui()

    def set_status(self, is_running=False, is_finished=False):
        self.is_running = is_running
        self.is_finished = is_finished
        self.update_ui()

    def update_ui(self):
        self.setIcon(QIcon())
        self.__animation.stop()
        self.__animation.hide()
        if self.is_running:
            self.setText(f"{self.original_text}")
            self.__animation.start()
            self.__animation.show()
        elif self.is_finished:
            self.setIcon(QIcon(LIB_IMAGE_DIR + "\\ok.svg"))
            self.setText(f"{self.original_text}")
        else:
            self.setText(self.original_text)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        r = self.__animation.rect()
        r.moveCenter(self.rect().center())
        r.moveLeft(self.rect().left() + 8)
        self.__animation.setGeometry(r)
