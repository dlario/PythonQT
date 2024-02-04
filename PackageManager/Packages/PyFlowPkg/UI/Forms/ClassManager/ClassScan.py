import os
import sys
import shutil
import pyclbr

from PyFlow import Wizards
from PyFlow import Packages

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6.QtWidgets import *

def scanfolder(filelocation, folderlist):
    packageRoot = Packages.__path__[0]
    templatesRoot = os.path.join(packageRoot, "../../../../PyFlow/UI/Forms/PackageWizard/Templates")
    packageRoot = QFileDialog.getExistingDirectory(None, "Choose folder", "Choose folder",
                                                   QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)

    defaultfolderlist = ["Exporters", "Factories", "FunctionLibraries", "Nodes", "Pins", "PrefsWidgets", "Tools", "UI"]
    folderdict = {i: [] for i in defaultfolderlist}

    fullpathname = ""
    for path, dirs, files in os.walk(packageRoot):
        for filename in files:
            print(path, dirs, files)
            module_info = pyclbr.readmodule(filename)
            print(module_info)
            for item in module_info.values():
                print(item.name)

