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


from collections import defaultdict
__REGISTERED_DOCWINDOWS = defaultdict(list)

def REGISTER_DOCKWINDOW(packageName, dockWindowClass):
    registeredDockWindowNames = [tool.name() for tool in __REGISTERED_DOCWINDOWS[packageName]]
    if dockWindowClass.name() not in registeredDockWindowNames:
        __REGISTERED_DOCWINDOWS[packageName].append(dockWindowClass)
        dockWindowClass.packageName = packageName

def GET_COMMANDS():
    return __REGISTERED_DOCWINDOWS
