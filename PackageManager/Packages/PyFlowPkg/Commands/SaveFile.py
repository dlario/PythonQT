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

## August 8, 2019 - David James Lario - Created
## October 21, 2021 - David James Lario - Clean up file and pushed settings to the init file.

from PackageManager.UI.Commands.Command import ShelfTool

class SaveFile(ShelfTool):
    def __init__(self):
        super(SaveFile, self).__init__()

    @staticmethod
    def name():
        return str("SaveFile")

    def do(self):
        self.ProgramManagerInstance.save()
