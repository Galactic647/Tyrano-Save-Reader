from PySide2.QtWidgets import QTreeWidget, QStyledItemDelegate

from typing import Union


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
    