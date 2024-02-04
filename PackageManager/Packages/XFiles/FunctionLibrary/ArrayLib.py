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


from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.Common import *


class ArrayLib(FunctionLibraryBase):
    '''doc string for ArrayLib'''
    def __init__(self, packageName):
        super(ArrayLib, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyPin', [], {PinSpecifires.CONSTRAINT: '1'}), meta={NodeMeta.CATEGORY: 'Array', NodeMeta.KEYWORDS: []})
    def extendArray(lhs=('AnyPin', [], {PinSpecifires.CONSTRAINT: '1', PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported | PinOptions.AllowAny}),
                    rhs=('AnyPin', [], {PinSpecifires.CONSTRAINT: '1', PinSpecifires.ENABLED_OPTIONS: PinOptions.ArraySupported | PinOptions.AllowAny})):
        """Extend the list by appending all the items from the iterable."""
        lhs.extend(rhs)
        return lhs