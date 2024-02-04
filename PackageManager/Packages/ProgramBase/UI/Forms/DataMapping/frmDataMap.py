## Copyright 2023 David Lario
__author__ = 'David Lario'
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.

## Revision History
## October 27, 2023 - David James Lario - Created

import os
import sys

basepath = os.path.dirname(os.path.abspath(__file__))
settingDatabase = "DSSettings.db"
settingTable = "tblProgramSettings"

from sqlalchemy import and_, extract
from sqlalchemy.orm import aliased
from sqlalchemy.orm import Query

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (QApplication, QFileDialog, QMdiSubWindow, QMessageBox)


class DataMap(QMdiSubWindow):
    def __init__(self, main, parent):
        super(DataMap, self).__init__()
        #.initDatabase()
        self.PackageName = "ProgramBase"
        self.main = main
        loader = QUiLoader()
        uiFile = os.path.join(basepath, 'frmDataMap.ui')
        self.ui = loader.load(uiFile, self)