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

from PackageManager.Core.Common import *

@SingletonDecorator
class PathsRegistry(object):
    """Holds paths to nodes and pins. Can rebuild paths and return entities by paths."""
    def __init__(self):
        self._data = {}

    def rebuild(self):
        man = GraphManagerSingleton().get()
        allNodes = man.getAllNodes()
        self._data.clear()
        for node in allNodes:
            self._data[node.path()] = node
            for pin in node.pins:
                self._data[pin.path()] = pin

    def getAllPaths(self):
        return list(self._data)

    def contains(self, path):
        return path in self._data

    # def resolvePath(self, base, path):
    #     temp = os.path.normpath(os.path.join(base, path))
    #     res = "/".join(temp.split(os.sep))

    def getEntity(self, path):
        if self.contains(path):
            return self._data[path]
        return None
