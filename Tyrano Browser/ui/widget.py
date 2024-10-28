from PySide2.QtWidgets import QTreeWidget, QStyledItemDelegate, QStyle
from PySide2.QtGui import QBrush, QColor, QPen
from PySide2.QtCore import Qt, QRect

from typing import Union


class CustomCheckboxDelegate(QStyledItemDelegate):
    def __init__(self, size, parent=None) -> None:
        super(CustomCheckboxDelegate, self).__init__(parent)

        self.size = size

    def paint(self, painter, option, index):
        if not index.column() and index.data(Qt.CheckStateRole) is not None:
            if option.state & QStyle.State_MouseOver:
                if option.state & QStyle.State_Selected:
                    painter.fillRect(option.rect, QBrush(QColor(64, 64, 64)))
                else:
                    painter.fillRect(option.rect, QBrush(QColor(48, 48, 48)))
            elif option.state & QStyle.State_Selected:
                if option.state & QStyle.State_HasFocus:
                    painter.fillRect(option.rect, QBrush(QColor(64, 64, 64)))
                else:
                    painter.fillRect(option.rect, QBrush(QColor(48, 48, 48)))
            else:
                painter.fillRect(option.rect, option.palette.base())

            state = index.data(Qt.CheckStateRole)
            pos = (
                option.rect.x(),
                option.rect.center().y() - self.size // 2
            )
            rect = QRect(*pos, self.size, self.size)

            if state == Qt.Checked:
                if option.state & QStyle.State_MouseOver:
                    pen = QPen(QColor(255, 255, 255), 1)
                    brush = QBrush(QColor(0, 224, 0))
                else:
                    pen = QPen(QColor(224, 224, 224), 1)
                    brush = QBrush(QColor(0, 224, 0))
            else:
                if option.state & QStyle.State_MouseOver:
                    pen = QPen(QColor(192, 192, 192), 1)
                    brush = QBrush(QColor(32, 32, 32))
                else:
                    pen = QPen(QColor(160, 160, 160), 1)
                    brush = QBrush(QColor(32, 32, 32))

            painter.setPen(pen)
            painter.setBrush(brush)
            painter.drawRect(rect)
            text_rect = option.rect.adjusted(30, 0, 0, 0)
            painter.setPen(QColor(255, 255, 255))
            painter.drawText(text_rect, Qt.AlignVCenter, index.data(Qt.DisplayRole))
        else:
            super().paint(painter, option, index)
    
    def createEditor(self, parent, option, index):
        return None

class NoEditDelegate(QStyledItemDelegate):
    def __init__(self, parent) -> None:
        super(NoEditDelegate, self).__init__(parent=parent)

    def createEditor(self, parent, option, index):
        return None

class CustomEditTreeWidget(QTreeWidget):
    def __init__(self, non_editable_columns: Union[list, tuple], parent=None) -> None:
        super(CustomEditTreeWidget, self).__init__(parent=parent)

        for i in non_editable_columns:
            self.setItemDelegateForColumn(i, NoEditDelegate(self))

class TemplateTreeWidget(QTreeWidget):
    def __init__(self, parent=None) -> None:
        super(TemplateTreeWidget, self).__init__(parent=parent)

    def dropEvent(self, event):
        super().dropEvent(event)
        self.itemChanged.emit(self.currentItem(), 1)

    def takeTopLevelItem(self, index):
        item = super().takeTopLevelItem(index)
        self.itemChanged.emit(item, 1)
        return item
    
    def removeChildItem(self, parent, item):
        parent.removeChild(item)
        self.itemChanged.emit(item, 1)
    