import sys
from PySide6.QtWidgets import QApplication, QTreeView, QTreeWidgetItem
from PySide6.QtGui import QStandardItemModel, QStandardItem

def addTreeViewItem(item, value):
    item.setRowCount(0)
    if type(value) is dict:
        for key, val in sorted(value.items()):
            child_item = QStandardItem(str(key))
            item.appendRow([child_item, QStandardItem(str(val))])
            addTreeViewItem(child_item, val)
    elif type(value) is list:
        for val in value:
            child_item = QStandardItem()
            item.appendRow([child_item, QStandardItem(str(val))])
            addTreeViewItem(child_item, val)

def dict2TreeView(model, data):
    model.setHorizontalHeaderLabels(['Key', 'Value'])
    root_item = model.invisibleRootItem()
    addTreeViewItem(root_item, data)


def addTreeWidgetItem(item, value, depth, max_depth):
    if depth >= max_depth:
        return

    if depth < 2:
        item.setExpanded(True)
    else:
        item.setExpanded(False)

    if type(value) is dict:
        for key, val in sorted(value.items()):
            child = QTreeWidgetItem()
            child.setText(0, str(key))
            item.addChild(child)
            addTreeWidgetItem(child, val, depth + 1, max_depth)
    elif type(value) is list:
        for val in value:
            child = QTreeWidgetItem()
            item.addChild(child)
            if type(val) is dict:
                child.setText(0, '[dict]')
                addTreeWidgetItem(child, val, depth + 1, max_depth)
            elif type(val) is list:
                child.setText(0, '[list]')
                addTreeWidgetItem(child, val, depth + 1, max_depth)
            else:
                child.setText(0, str(val))
    else:
        child = QTreeWidgetItem()
        child.setText(0, str(value))
        item.addChild(child)


def dict2TreeWidget(widget, value, max_depth=3):
    widget.clear()
    addTreeWidgetItem(widget.invisibleRootItem(), value, 0, max_depth)


def treewidgetpath(selected_item):
    if selected_item:
        item = selected_item
        path = [item.text(0)]
        while item.parent() is not None:
            item = item.parent()
            path.insert(0, item.text(0))
    return path