## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

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
# from PyFlow.Wizards.ClassWizard import ClassWizard
from PackageManager.Packages.PyFlow.Commands import RESOURCES_DIR
from PackageManager.Core.Common import Direction

from PySide6 import QtGui
from PySide6.QtWidgets import QFileDialog


class CommandBuilder(ShelfTool):

    def __init__(self):
        super(CommandBuilder, self).__init__()

    @staticmethod
    def toolTip():
        return "Command Builder"

    @staticmethod
    def getIcon():
        return QtGui.QIcon(RESOURCES_DIR + "new_file_icon.png")

    @staticmethod
    def name():
        return str("CommandBuilder")

    def do(self):
        ClassWizard.run
