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


import os
import json

from PySide6 import QtCore, QtGui

from PackageManager.Core.Common import *
from PackageManager.Input import InputAction, InputManager, InputActionType


@SingletonDecorator
class ConfigManager(object):
    """Responsible for registering configuration files, reading/writing values to registered config files by aliases, providing QSettings from registered aliases."""

    CONFIGS_STORAGE = {}

    CONFIGS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "Configs")
    INPUT_CONFIG_PATH = os.path.join(CONFIGS_DIR, "input.json")

    def __init__(self, *args, **kwargs):
        self.registerConfigFile("PREFS", os.path.join(self.CONFIGS_DIR, "prefs.ini"))
        self.registerConfigFile("APP_STATE", os.path.join(self.CONFIGS_DIR, "config.ini"))

        if not os.path.exists(self.INPUT_CONFIG_PATH):
            self.createDefaultInput()
            data = InputManager().serialize()
            if not os.path.exists(os.path.dirname(self.INPUT_CONFIG_PATH)):
                os.makedirs(os.path.dirname(self.INPUT_CONFIG_PATH))
            with open(self.INPUT_CONFIG_PATH, "w") as f:
                json.dump(data, f)
        else:
            with open(self.INPUT_CONFIG_PATH, "r") as f:
                data = json.load(f)
                InputManager().loadFromData(data)

    @staticmethod
    def shouldRedirectOutput():
        return ConfigManager().getPrefsValue("PREFS", "General/RedirectOutput") == "true"

    def registerConfigFile(self, alias, absPath):
        if alias not in self.CONFIGS_STORAGE:
            self.CONFIGS_STORAGE[alias] = absPath
            return True
        return False

    def getSettings(self, alias):
        if alias in self.CONFIGS_STORAGE:
            settings = QtCore.QSettings(self.CONFIGS_STORAGE[alias], QtCore.QSettings.IniFormat)
            return settings

    def getPrefsValue(self, configAlias, valueKey):
        settings = self.getSettings(configAlias)
        if settings:
            if settings.contains(valueKey):
                return settings.value(valueKey)

    def createDefaultInput(self):
        InputManager().registerAction(InputAction(name="App.NewFile", actionType=InputActionType.Keyboard, group="IO", key=QtCore.Qt.Key_N, modifiers=QtCore.Qt.ControlModifier))
        InputManager().registerAction(InputAction(name="App.Save", actionType=InputActionType.Keyboard, group="IO", key=QtCore.Qt.Key_S, modifiers=QtCore.Qt.ControlModifier))
        InputManager().registerAction(InputAction(name="App.SaveAs", actionType=InputActionType.Keyboard, group="IO", key=QtCore.Qt.Key_S, modifiers=QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier))
        InputManager().registerAction(InputAction(name="App.Load", actionType=InputActionType.Keyboard, group="IO", key=QtCore.Qt.Key_O, modifiers=QtCore.Qt.ControlModifier))
