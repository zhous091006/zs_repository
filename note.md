```C++

//获取边缘区域
CustomWindow::ResizeRegion CustomWindow::getResizeRegion(const QPoint& pos)
{
        bool onLeft = pos.x() <= EDGE_MARGIN;
        bool onRight = pos.x() >= width() - EDGE_MARGIN;
        bool onTop = pos.y() <= EDGE_MARGIN;
        bool onButtom = pos.y() >= height() - EDGE_MARGIN;
        if (onTop && onLeft)return TopLeft;
        if (onTop && onRight)return TopRight;
        if (onButtom && onLeft)return BottomLeft;
        if (onButtom && onRight)return BottomRight;
        if (onTop)return Top;
        if (onButtom)return Bottom;
        if (onLeft)return Left;
        if (onRight)return Right;
        return NoEdge;
}

```

---

## UiSizeGrip 缩放窗口只能在四个角 vs 八个方向的问题

### 问题
`test_size_grip.py` 缩放窗口只能在四个角，而 `ui_dialog_base.py` 可以八个方向。

### 原因
**根本差异在 grip 控件的尺寸设置**：

- `test_size_grip.py`：所有 8 个 grip 全部 `setFixedSize(4, 4)`，四条边的 grip 只有 4x4 大小，只覆盖了四个角落区域。
- `ui_dialog_base.py`：边和角分开设置。四条边的 grip 只固定单边尺寸（`setFixedWidth` / `setFixedHeight`），另一边自由拉伸覆盖整条边；四个角的 grip 用 `setFixedSize(4, 4)`。

### 修复
```python
# 边：只固定单边，另一边自由拉伸
if edge in (Qt.LeftEdge, Qt.RightEdge):
    grip.setFixedWidth(margin)
elif edge in (Qt.TopEdge, Qt.BottomEdge):
    grip.setFixedHeight(margin)
else:
    grip.setFixedSize(margin, margin)
```

### setMouseTracking(True)
启用后，即使不按下鼠标按键，移动也会持续触发 `mouseMoveEvent`。不启用时，只有按下按键并移动才触发。

### 光标切换机制
`mouseMoveEvent` 里**没有**主动切换光标的代码。光标是在 `UiSizeGrip.__init__` 中根据 edge 一次性设置的：
```python
edge_cursor_dict = {
    Qt.LeftEdge: Qt.SizeHorCursor,
    Qt.TopEdge: Qt.SizeVerCursor,
    ...
}
self.setCursor(edge_cursor_dict.get(self._edge, Qt.ArrowCursor))
```
每个 grip 控件独立存在且设置了不同 cursor。当鼠标滑入不同 grip 区域时，QWidget 自动显示该控件对应的光标。

