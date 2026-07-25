from copy import copy

from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QWidget


class UiSizeGrip(QWidget):
    def __init__(self, edge: Qt.Edge, parent: QWidget):
        super().__init__(parent)
        self._edge = edge
        self._is_mouse_pressed = False
        self._mouse_pressed_pos: QPoint = QPoint()
        self._record_geometry: QRect = QRect()

        self.setMouseTracking(True)

        edge_cursor_dict = {
            Qt.LeftEdge: Qt.SizeHorCursor,
            Qt.TopEdge: Qt.SizeVerCursor,
            Qt.RightEdge: Qt.SizeHorCursor,
            Qt.BottomEdge: Qt.SizeVerCursor,
            Qt.TopEdge | Qt.LeftEdge: Qt.SizeFDiagCursor,
            Qt.TopEdge | Qt.RightEdge: Qt.SizeBDiagCursor,
            Qt.BottomEdge | Qt.LeftEdge: Qt.SizeBDiagCursor,
            Qt.BottomEdge | Qt.RightEdge: Qt.SizeFDiagCursor,
        }

        self.setCursor(edge_cursor_dict.get(self._edge, Qt.ArrowCursor))

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self._is_mouse_pressed = True
        if event.button() == Qt.LeftButton:
            self._mouse_pressed_pos = event.globalPos()
            if self.parentWidget() is not None:
                self._record_geometry = self.parentWidget().geometry()
                event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        parent_widget = self.parentWidget()

        if not self._is_mouse_pressed or event.buttons() != Qt.LeftButton or self.isMaximized() or self._edge == 0 or parent_widget is None:
            return

        resized_geometry = copy(self._record_geometry)
        global_pos = event.globalPos()

        if self._edge == (Qt.TopEdge | Qt.LeftEdge):
            resized_geometry.setTopLeft(self._record_geometry.topLeft() + global_pos - self._mouse_pressed_pos)
        elif self._edge == Qt.TopEdge:
            resized_geometry.setTop(self._record_geometry.top() + global_pos.y() - self._mouse_pressed_pos.y())
        elif self._edge == (Qt.TopEdge | Qt.RightEdge):
            resized_geometry.setTopRight(self._record_geometry.topRight() + global_pos - self._mouse_pressed_pos)
        elif self._edge == Qt.LeftEdge:
            resized_geometry.setLeft(self._record_geometry.left() + global_pos.x() - self._mouse_pressed_pos.x())
        elif self._edge == Qt.RightEdge:
            resized_geometry.setRight(self._record_geometry.right() + global_pos.x() - self._mouse_pressed_pos.x())
        elif self._edge == (Qt.BottomEdge | Qt.LeftEdge):
            resized_geometry.setBottomLeft(self._record_geometry.bottomLeft() + global_pos - self._mouse_pressed_pos)
        elif self._edge == Qt.BottomEdge:
            resized_geometry.setBottom(self._record_geometry.bottom() + global_pos.y() - self._mouse_pressed_pos.y())
        elif self._edge == (Qt.BottomEdge | Qt.RightEdge):
            resized_geometry.setBottomRight(self._record_geometry.bottomRight() + global_pos - self._mouse_pressed_pos)

        if resized_geometry.width() < parent_widget.minimumWidth():
            if self._edge & Qt.LeftEdge:
                resized_geometry.setLeft(resized_geometry.right() - parent_widget.minimumWidth())
            elif self._edge & Qt.RightEdge:
                resized_geometry.setRight(resized_geometry.left() + parent_widget.minimumWidth())
            else:
                resized_geometry.setWidth(parent_widget.minimumWidth())

        if resized_geometry.height() < parent_widget.minimumHeight():
            if self._edge & Qt.TopEdge:
                resized_geometry.setTop(resized_geometry.bottom() - parent_widget.minimumHeight())
            elif self._edge & Qt.BottomEdge:
                resized_geometry.setBottom(resized_geometry.top() + parent_widget.minimumHeight())
            else:
                resized_geometry.setHeight(parent_widget.minimumHeight())

        parent_widget.setGeometry(resized_geometry)
        event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self._is_mouse_pressed = False
        self._mouse_pressed_pos = QPoint()
        self._record_geometry = QRect()
        event.accept()

    def update_size_grip_widget_geometry(self):
        parent_rect = self.parentWidget().rect()
        r = self.geometry()
        if self._edge == Qt.LeftEdge:
            r.setHeight(parent_rect.height())
            r.moveTopLeft(parent_rect.topLeft())
        elif self._edge == Qt.TopEdge:
            r.setWidth(parent_rect.width())
            r.moveTopLeft(parent_rect.topLeft())
        elif self._edge == Qt.RightEdge:
            r.setHeight(parent_rect.height())
            r.moveTopRight(parent_rect.topRight())
        elif self._edge == Qt.BottomEdge:
            r.setWidth(parent_rect.width())
            r.moveBottomLeft(parent_rect.bottomLeft())
        elif self._edge == (Qt.TopEdge | Qt.LeftEdge):
            r.moveTopLeft(parent_rect.topLeft())
        elif self._edge == Qt.TopEdge | Qt.RightEdge:
            r.moveTopRight(parent_rect.topRight())
        elif self._edge == (Qt.BottomEdge | Qt.LeftEdge):
            r.moveBottomLeft(parent_rect.bottomLeft())
        elif self._edge == (Qt.BottomEdge | Qt.RightEdge):
            r.moveBottomRight(parent_rect.bottomRight())
        self.setGeometry(r)
