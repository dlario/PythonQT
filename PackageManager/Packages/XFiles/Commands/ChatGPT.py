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


from PackageManager.UI.Commands.Command import ShelfTool
from PackageManager.Packages.XFiles.UI.Forms.frmChatGPT import ChatGPT as loadedForm

class ChatGPT(ShelfTool):
    def __init__(self):
        super(ChatGPT, self).__init__()

    @staticmethod
    def name():
        return str("ChatGPT")

    @staticmethod
    def category():
        return None

    @staticmethod
    def keywords():
        return None

    def do(self):
        self.ProgramManagerInstance.instance.newFileFromUi(loadedForm(self.ProgramManagerInstance,
                                                                      self.ProgramManagerInstance))
