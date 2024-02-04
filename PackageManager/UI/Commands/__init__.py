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
from collections import defaultdict
__REGISTERED_COMMANDS = defaultdict(list)

RESOURCES_DIR = os.path.dirname(os.path.realpath(__file__)) + "/res/"

def REGISTER_COMMAND(packageName, toolClass):
    registeredToolNames = [tool.name() for tool in __REGISTERED_COMMANDS[packageName]]
    if toolClass.name() not in registeredToolNames:
        __REGISTERED_COMMANDS[packageName].append(toolClass)
        toolClass.packageName = packageName

def GET_COMMANDS():
    return __REGISTERED_COMMANDS