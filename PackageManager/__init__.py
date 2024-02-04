## Copyright 2023 David Lario
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


"""Common utils working with packags.
"""

# this line adds extension-packages not installed inside the PackageManager directory
__path__ = __import__('pkgutil').extend_path(__path__, __name__)

import importlib
import pkgutil
import collections
from copy import copy
import os
import json

from PackageManager.Packages import *


__all__ = [
    "INITIALIZE",
    "GET_PACKAGES",
    "GET_PACKAGE_CHECKED",
    "GET_DEFAULT_PATHS"
]

__PACKAGES = {}
__PACKAGE_PATHS = {}
__HASHABLE_TYPES = []


__DATABASES = {}

def GET_PACKAGES():
    return __PACKAGES

def GET_DATABASES():
    return __DATABASES

def GET_PACKAGE_PATH(packageName):
    if packageName in __PACKAGE_PATHS:
        return __PACKAGE_PATHS[packageName]

def GET_PACKAGE_CHECKED(package_name):
    assert package_name in __PACKAGES
    return __PACKAGES[package_name]

def GET_DEFAULT_PATHS():
    return Packages.__path__

def INITIALIZE(additionalPackageLocations=[], Parent=None):
    from PackageManager.UI.Commands import REGISTER_COMMAND
    from PackageManager.UI.Widgets.InputWidgets import REGISTER_UI_INPUT_WIDGET_PIN_FACTORY
    from PackageManager import ConfigManager
    from PySide6.QtWidgets import QMessageBox

    packagePaths = Packages.__path__

    def ensurePackagePath(inPath):
        for subFolder in os.listdir(inPath):
            subFolderPath = os.path.join(inPath, subFolder)
            if os.path.isdir(subFolderPath):
                if "PackageManager" in os.listdir(subFolderPath):
                    subFolderPath = os.path.join(subFolderPath, "PackageManager", "Packages")
                    if os.path.exists(subFolderPath):
                        return subFolderPath
        return inPath

    def recursePackagePaths(inPath):
        paths = []
        for subFolder in os.listdir(inPath):
            subFolderPath = os.path.join(inPath, subFolder)
            if os.path.isdir(subFolderPath):
                if "PackageManager" in os.listdir(subFolderPath):
                    subFolderPath = os.path.join(subFolderPath, "PackageManager", "Packages")
                    if os.path.exists(subFolderPath):
                        paths.append(subFolderPath)
        return paths

    # check for additional package locations
    if "PackageManager_PACKAGES_PATHS" in os.environ:
        delim = ';'
        pathsString = os.environ["PackageManager_PACKAGES_PATHS"]
        # remove delimeters from right
        pathsString = pathsString.rstrip(delim)
        for packagesRoot in pathsString.split(delim):
            if os.path.exists(packagesRoot):
                paths = recursePackagePaths(packagesRoot)
                packagePaths.extend(paths)

    for packagePathId in range(len(additionalPackageLocations)):
        packagePath = additionalPackageLocations[packagePathId]
        packagePath = ensurePackagePath(packagePath)
        additionalPackageLocations[packagePathId] = packagePath

    packagePaths.extend(additionalPackageLocations)

    for importer, modname, ispkg in pkgutil.iter_modules(packagePaths):
        try:
            if ispkg:
                print("Tables: " + modname)
                mod = importer.find_module(modname).load_module(modname)
                #mod = importlib.import_module(modname) #This way can be used too
                package = getattr(mod, modname)(Parent)
                __PACKAGES[modname] = package
                __PACKAGE_PATHS[modname] = os.path.normpath(mod.__path__[0])
        except Exception as e:
            QMessageBox.critical(None, str("Fatal error"), "Error On Module %s :\n%s" % (modname, str(e)))
            continue


    for name, package in __PACKAGES.items():
        packageName = package.__class__.__name__

        for toolClass in package.GetCommandClasses().values():
            REGISTER_COMMAND(packageName, toolClass)

        '''for sessionClass in package.GetCommandClasses.values():
            REGISTER_SESSION(session)'''