from math import sin, cos

from PyQt5.QtCore import Qt, QTimer, QDateTime, QRectF, QPointF
from PyQt5.QtGui import QColor, QConicalGradient, QPainterPath, QPainter
from PyQt5.QtWidgets import QFrame

from lib.lib_func import lib_func_t


class UiWaitingAnimationWidget(QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.setContentsMargins(2, 2, 2, 2)

        self.color = QColor("#0492FC")
        self.shape_width = 2
        self.speed = 200
        self.rotate = 90
        self.outer_circle_diameter = 0

        self.conical_gradient = QConicalGradient()
        self.conical_gradient.setColorAt(0, self.color)
        self.conical_gradient.setColorAt(0.9, Qt.transparent)

        self.concentric_circle_path = QPainterPath()
        self.leading_circle_path = QPainterPath()

        self.record_time = QDateTime.currentDateTime()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.__on_timeout)

    def set_color(self, color: QColor):
        self.color = color
        self.conical_gradient.setColorAt(0, self.color)

    def start(self):
        self.record_time = QDateTime.currentDateTime()
        self.rotate = 90
        self.update()
        self.timer.start(20)

    def stop(self):
        self.timer.stop()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        # 计算外圆直径
        l, t, r, b = self.getContentsMargins()
        self.outer_circle_diameter = min(self.width() - (l + r), self.height() - (r + b))

        outerCircleRect = QRectF(0, 0, self.outer_circle_diameter, self.outer_circle_diameter)
        outerCircleRect.moveCenter(QPointF(0, 0))

        innerCircleRect = outerCircleRect.adjusted(self.shape_width, self.shape_width, -self.shape_width, -self.shape_width)

        # 计算同心圆路径
        self.concentric_circle_path = QPainterPath()
        self.concentric_circle_path.addEllipse(outerCircleRect)

        innerCirclePath = QPainterPath()
        innerCirclePath.addEllipse(innerCircleRect)
        self.concentric_circle_path = self.concentric_circle_path.subtracted(innerCirclePath)

    def paintEvent(self, event) -> None:
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)

        # 绘制同心圆
        self.conical_gradient.setAngle(self.rotate)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.conical_gradient)
        painter.drawPath(self.concentric_circle_path)

        # 绘制领头圆
        r = self.outer_circle_diameter / 2 - 0.5 * self.shape_width
        p = QPointF(r * cos(lib_func_t.degrees_to_radians(self.rotate)), -r * sin(lib_func_t.degrees_to_radians(self.rotate)))
        painter.setBrush(self.color)
        painter.drawEllipse(p, self.shape_width / 2, self.shape_width / 2)

    def __on_timeout(self):
        currentTime = QDateTime.currentDateTime()
        ms = self.record_time.msecsTo(currentTime)
        self.record_time = currentTime
        self.rotate -= ms * self.speed / 1000
        self.rotate = (self.rotate + 360) if (self.rotate <= -270) else self.rotate
        self.update()
