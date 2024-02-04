## Copyright 2023 David James Lario

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
## 2023-07-10 - David James Lario - Created

from cycler import *
from PyFlow.Core import FunctionLibraryBase
from PyFlow.Core import (
    FunctionLibraryBase,
    IMPLEMENT_NODE)
from PyFlow import getHashableDataTypes
from PyFlow.Core.Common import *
from PackageManager.Core.PathsRegistry import PathsRegistry

class cycler(FunctionLibraryBase):
#doc string

    def __init__(self, packageName):
        super(cycler, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Cycler_by_key (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Cycler.by_key(self)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Cycler_change_key (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 old=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 new=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Cycler.change_key(self, old, new)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Cycler_concat (left=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 right=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Cycler.concat(left, right)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Cycler_simplify (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Cycler.simplify(self)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def concat (left=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 right=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return concat(left, right)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def cycler (args=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 kwargs=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return cycler(args, kwargs)
