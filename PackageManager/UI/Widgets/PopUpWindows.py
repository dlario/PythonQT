import os

from PySide6.QtGui import QPixmap, QIcon, QIntValidator
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QListWidget, QPushButton, QTextEdit, QLineEdit, \
    QAbstractItemView, QHBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QInputDialog, QComboBox, QDialogButtonBox, \
    QFormLayout, QCheckBox
from PIL import Image
from wandb.integration.openai import openai


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

class ListSelectionDialog(QDialog):
    def __init__(self, inputdict, options, parent=None):
        super().__init__(parent)

        try:
            self.setWindowTitle(f"{inputdict['title']}")
            self.setWindowIcon(QIcon(f"{inputdict['icon']}"))
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.setWindowModality(Qt.WindowModal)

        except KeyError as e:
            raise ValueError(f'Missing key in inputdict: {e}') from None

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.list_widget = QListWidget()
        for option in options:
            self.list_widget.addItem(option)
        self.layout.addWidget(self.list_widget)


        # Connect the list widget's itemSelectionChanged signal to update the line edit
        self.list_widget.itemSelectionChanged.connect(self.update_text_edit)

        # Create a QLineEdit widget to display the selected item
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(False)
        self.layout.addWidget(self.text_edit)

        self.ok_button = QPushButton('OK')
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)

        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.reject)
        self.layout.addWidget(self.cancel_button)

    def update_text_edit(self):
        self.text_edit.setText(self.list_widget.currentItem().text())

    def selected_item(self):
        return self.text_edit.toPlainText()


class ListItemSelectionDialog(QDialog):
    def __init__(self, inputdict, options, parent=None):
        super().__init__(parent)
        try:
            self.setWindowTitle(f"{inputdict['title']}")
            self.setWindowIcon(QIcon(f"{inputdict['icon']}"))
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.setWindowModality(Qt.WindowModal)

        except KeyError as e:
            raise ValueError(f'Missing key in inputdict: {e}') from None

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.list_widget = QListWidget()
        for option in options:
            self.list_widget.addItem(option)
        self.layout.addWidget(self.list_widget)

        # Set selection mode to allow multiple selections
        self.list_widget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.list_widget.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

        # Connect the list widget's itemSelectionChanged signal to update the text edit
        self.list_widget.itemSelectionChanged.connect(self.update_text_edit)

        # Create a QTextEdit widget to display the selected items
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.layout.addWidget(self.text_edit)

        # Create a QLineEdit widget and a QPushButton for adding new items
        self.add_item_layout = QHBoxLayout()
        self.new_item_edit = QLineEdit()
        self.add_item_layout.addWidget(self.new_item_edit)
        self.add_item_button = QPushButton('Add')
        self.add_item_button.clicked.connect(self.add_item)
        self.add_item_layout.addWidget(self.add_item_button)
        self.layout.addLayout(self.add_item_layout)

        self.ok_button = QPushButton('OK')
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)

        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.reject)
        self.layout.addWidget(self.cancel_button)

    def add_item(self):
        new_item_text = self.new_item_edit.text()
        if new_item_text:  # Add the new item only if the text is not empty
            self.list_widget.addItem(new_item_text)
            self.new_item_edit.clear()

    def update_text_edit(self):
        selected_items = [item.text() for item in self.list_widget.selectedItems()]
        self.text_edit.setText('\n'.join(selected_items))

    def selected_items(self):
        return [item.text() for item in self.list_widget.selectedItems()]


class ListItemSelectionDialogGPT(QDialog):
    def __init__(self, inputdict, options, parent=None):
        super().__init__(parent)
        try:
            self.setWindowTitle(f"{inputdict['title']}")
            self.setWindowIcon(QIcon(f"{inputdict['icon']}"))
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.setWindowModality(Qt.WindowModal)

        except KeyError as e:
            raise ValueError(f'Missing key in inputdict: {e}') from None

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create an input field for the prompt
        self.prompt_edit = QLineEdit()
        self.layout.addWidget(QLabel("ChatGPT Prompt:"))
        self.layout.addWidget(self.prompt_edit)

        # Create two input fields for the integers
        self.int_edit1 = QLineEdit()
        self.int_edit1.setValidator(QIntValidator())
        self.int_edit2 = QLineEdit()
        self.int_edit2.setValidator(QIntValidator())

        self.layout.addWidget(QLabel("Integer 1:"))
        self.layout.addWidget(self.int_edit1)
        self.layout.addWidget(QLabel("Integer 2:"))
        self.layout.addWidget(self.int_edit2)

        # Create a refresh button
        self.refresh_button = QPushButton('Refresh')
        self.refresh_button.clicked.connect(self.refresh)
        self.layout.addWidget(self.refresh_button)

        self.list_widget = QListWidget()
        for option in options:
            self.list_widget.addItem(option)
        self.layout.addWidget(self.list_widget)

        # Set selection mode to allow multiple selections
        self.list_widget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        # Connect the list widget's itemSelectionChanged signal to update the text edit
        self.list_widget.itemSelectionChanged.connect(self.update_text_edit)

        # Create a QTextEdit widget to display the selected items
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(False)
        self.layout.addWidget(self.text_edit)

        # Create a QLineEdit widget and a QPushButton for adding new items
        self.add_item_layout = QHBoxLayout()
        self.new_item_edit = QLineEdit()
        self.add_item_layout.addWidget(self.new_item_edit)
        self.add_item_button = QPushButton('Add')
        self.add_item_button.clicked.connect(self.add_item)
        self.add_item_layout.addWidget(self.add_item_button)
        self.layout.addLayout(self.add_item_layout)

        self.ok_button = QPushButton('OK')
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)

        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.reject)
        self.layout.addWidget(self.cancel_button)

    def refresh(self):
        PROMPT = self.prompt_edit.text()
        int1 = int(self.int_edit1.text()) if self.int_edit1.text() else None
        int2 = int(self.int_edit2.text()) if self.int_edit2.text() else None

        # Implement or call your comp method here
        self.comp(PROMPT, int1, int2)

    def comp(self, PROMPT, int1, int2):
        # Implement your method here
        pass

    def add_item(self):
        new_item_text = self.new_item_edit.text()
        if new_item_text:  # Add the new item only if the text is not empty
            self.list_widget.addItem(new_item_text)
            self.new_item_edit.clear()

    def update_text_edit(self):
        selected_items = [item.text() for item in self.list_widget.selectedItems()]
        self.text_edit.setText('\n'.join(selected_items))

    def selected_items(self):
        return [item.text() for item in self.list_widget.selectedItems()]

    def comp(self, PROMPT, MaxToken=50, outputs=3):
        # using OpenAI's Completion module that helps execute
        # any tasks involving text
        response = openai.Completion.create(
            # model name used here is text-davinci-003
            # there are many other models available under the
            # umbrella of GPT-3
            model="text-davinci-003",
            # passing the user input
            prompt=PROMPT,
            # generated output can have "max_tokens" number of tokens
            max_tokens=MaxToken,
            # number of outputs generated in one call
            n=outputs
        )
        # creating a list to store all the outputs
        output = list()
        for k in response['choices']:
            output.append(k['text'].strip())
        return output

class IconSelectionDialog(QDialog):
    def __init__(self, inputdict, directory, parent=None):
        super().__init__(parent)
        try:
            self.setWindowTitle(f"{inputdict['title']}")
            self.setWindowIcon(QIcon(f"{inputdict['icon']}"))
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.setWindowModality(Qt.WindowModal)

        except KeyError as e:
            raise ValueError(f'Missing key in inputdict: {e}') from None

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.icon_table = QTableWidget()
        self.icon_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.layout.addWidget(self.icon_table)

        self.selected_icon_label = QLabel()
        self.layout.addWidget(self.selected_icon_label)

        self.ok_button = QPushButton('OK')
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)

        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.reject)
        self.layout.addWidget(self.cancel_button)

        self.load_icons(directory)

        self.icon_table.itemSelectionChanged.connect(self.update_selected_icon)

    def load_icons(self, directory):
        # Get all image files in the directory
        image_files = [f for f in os.listdir(directory) if f.endswith(('.png', '.jpg', '.jpeg'))]
        # Set the number of rows and columns
        self.icon_table.setRowCount(len(image_files))
        self.icon_table.setColumnCount(1)
        # Add each image file as an item in the table
        for i, image_file in enumerate(image_files):
            pixmap = QPixmap(os.path.join(directory, image_file))
            pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio)
            item = QTableWidgetItem()
            item.setData(Qt.DecorationRole, pixmap)
            self.icon_table.setItem(i, 0, item)

    def update_selected_icon(self):
        selected_items = self.icon_table.selectedItems()
        if selected_items:
            pixmap = selected_items[0].data(Qt.DecorationRole)
            self.selected_icon_label.setPixmap(pixmap)

    def selected_icon(self):
        selected_items = self.icon_table.selectedItems()
        if selected_items:
            return selected_items[0].data(Qt.DecorationRole)
        else:
            return None

class RibbonBarDialog(QDialog):
    def __init__(self, bars, bar_name, sections, section_name, elements, element_name, parent=None):
        super(RibbonBarDialog, self).__init__(parent)

        self.setWindowTitle('Create Ribbon Bar Element')

        # Bar name input
        self.bar_name_label = QLabel('Bar Name:')
        self.bar_combo = QComboBox()
        self.bar_combo.setEditable(True)
        self.bar_combo.addItems(bars) # Add predefined sections
        self.bar_combo.setEditText(bar_name)

        # Section input (ComboBox with predefined options)
        self.section_label = QLabel('Section:')
        self.section_combo = QComboBox()
        self.section_combo.setEditable(True)
        self.section_combo.addItems(sections) # Add predefined sections
        self.section_combo.setEditText(section_name)

        # Another ComboBox with predefined options
        self.element_label = QLabel('Element:')
        self.element_combo = QComboBox()
        self.element_combo.addItems(elements) # Add predefined elements
        self.element_combo.setEditText(element_name)

        # OK and Cancel buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # Checkboxes for "Main" and "Instance"
        self.main_checkbox = QCheckBox('Main')
        self.instance_checkbox = QCheckBox('Instance')

        # Layout
        self.layout = QFormLayout()
        self.layout.addRow(self.bar_name_label, self.bar_combo)
        self.layout.addRow(self.section_label, self.section_combo)
        self.layout.addRow(self.element_label, self.element_combo)
        self.layout.addRow(self.main_checkbox)
        self.layout.addRow(self.instance_checkbox)
        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)

    def get_inputs(self):
        return (
            self.bar_combo.currentText(),
            self.section_combo.currentText(),
            self.element_combo.currentText(),
            self.main_checkbox.isChecked(),
            self.instance_checkbox.isChecked()
        )