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

def scanOutlook():
    from win32com.client import constants
    from win32com.client.gencache import EnsureDispatch as Dispatch

    outlook = Dispatch("Outlook.Application")
    mapi = outlook.GetNamespace("MAPI")

    class Oli():
        def __init__(self, outlook_object):
            self._obj = outlook_object

        def items(self):
            array_size = self._obj.Count
            for item_index in xrange(1,array_size+1):
                yield (item_index, self._obj[item_index])

        def prop(self):
            return sorted( self._obj._prop_map_get_.keys() )

    for inx, folder in Oli(mapi.Folders).items():
        # iterate all Outlook folders (top level)
        print("-"*70)
        print(folder.Name)

        for inx,subfolder in Oli(folder.Folders).items():
            print("(%i)" % inx, subfolder.Name,"=> ", subfolder)