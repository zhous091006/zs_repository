from PyQt5.QtCore import Qt
from PyQt5.QtGui import QResizeEvent, QFontMetrics, QShowEvent
from PyQt5.QtWidgets import QLabel


class UiLabel(QLabel):
    def __init__(self, *args):
        super().__init__(*args)
        self.raw_context = ""
        self.text_ellipsis_enable = False
        self.auto_scale_content = False
        self.prefer_font_size = 11
        if len(args) == 2:
            self.raw_context = args[0]

    def setText(self, text: str) -> None:
        self.raw_context = text
        self.__deal_text_scale()
        if Qt.mightBeRichText(self.raw_context):
            super().setText(self.raw_context)
        else:
            display_text = self.__deal_text_ellipsis(self.raw_context)
            if display_text != self.raw_context:
                self.setToolTip(self.raw_context)
            else:
                self.setToolTip("")
            super().setText(display_text)

    def clear(self) -> None:
        self.setText("")

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self.setText(self.raw_context)

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        self.setText(self.raw_context)

    def set_text_ellipsis_enabled(self, enable):
        self.text_ellipsis_enable = enable
        self.setText(self.raw_context)

    def set_auto_scale_content_enabled(self, enable):
        self.auto_scale_content = enable
        self.setText(self.raw_context)

    def __deal_text_scale(self):
        if self.auto_scale_content and self.raw_context and self.isVisible():
            font = self.font()
            font.setPixelSize(self.prefer_font_size)
            self.setFont(font)
            while True:
                font_size = font.pixelSize()
                fm = QFontMetrics(self.font())
                text_width = fm.width(self.raw_context)
                if text_width > self.width() and font_size > 1:
                    font.setPixelSize(font_size - 1)
                    self.setFont(font)
                else:
                    break

    def __deal_text_ellipsis(self, text: str) -> str:
        if self.text_ellipsis_enable:
            fontWidth = QFontMetrics(self.font())  # 得到每个字符的宽度
            return fontWidth.elidedText(text, Qt.ElideRight, self.width())  # 最大宽度150像素
        return text
