from PySide6.QtWidgets import QInputDialog, QDialog
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

class InputDialog(QInputDialog):
    def __init__(self, inputdict, parent=None):
        super(InputDialog, self).__init__(parent=parent)

        try:
            self.setLabelText(f"{inputdict['label']}")
            self.setTextValue(f"{inputdict['default']}")
            self.setInputMode(QInputDialog.TextInput)
            self.setOkButtonText(f"{inputdict['button']}")
            self.setWindowTitle(f"{inputdict['title']}")
            self.setWindowIcon(QIcon(f"{inputdict['icon']}"))
            self.setCancelButtonText("Cancel")
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.setWindowModality(Qt.WindowModal)

        except KeyError as e:
            raise ValueError(f'Missing key in inputdict: {e}') from None

    def get_value(self):
        if self.exec_() == QInputDialog.Accepted:
            return self.textValue()
        else:
            return None
