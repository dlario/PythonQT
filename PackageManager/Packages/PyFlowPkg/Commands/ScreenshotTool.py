## Copyright 2020 David Lario

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.



from PackageManager.UI.Commands.Command import ShelfTool
from PackageManager.Packages.PyFlow.Commands import RESOURCES_DIR
from PyFlow.UI.ContextMenuDataBuilder import ContextMenuDataBuilder

from PySide6 import QtGui
from PySide6.QtWidgets import QFileDialog


class ScreenshotTool(ShelfTool):
    """docstring for ScreenshotTool."""
    def __init__(self):
        super(ScreenshotTool, self).__init__()
        self.format = "PNG"

    def saveState(self, settings):
        super(ScreenshotTool, self).saveState(settings)
        settings.setValue("format", self.format)

    def restoreState(self, settings):
        super(ScreenshotTool, self).restoreState(settings)
        formatValue = settings.value("format")
        if formatValue is not None:
            self.format = formatValue
        else:
            self.format = "PNG"

    def onSetFormat(self, fmt):
        self.format = fmt

    def contextMenuBuilder(self):
        builder = ContextMenuDataBuilder()
        builder.addEntry("Save to PNG", "PNG", lambda: self.onSetFormat("PNG"))
        builder.addEntry("Save to JPG", "JPG", lambda: self.onSetFormat("JPG"))
        return builder

    @staticmethod
    def toolTip():
        return "Takes screenshot of visible area of canvas and\nsaves image to file"

    @staticmethod
    def getIcon():
        return QtGui.QIcon(RESOURCES_DIR + "screenshot_icon.png")

    @staticmethod
    def name():
        return str("ScreenshotTool")

    def do(self):
        print("ScreenshotTool")
