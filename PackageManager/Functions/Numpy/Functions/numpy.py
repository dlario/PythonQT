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

from numpy import *
from PyFlow.Core import FunctionLibraryBase
from PyFlow.Core import (
    FunctionLibraryBase,
    IMPLEMENT_NODE)
from PyFlow import getHashableDataTypes
from PyFlow.Core.Common import *
from PackageManager.Core.PathsRegistry import PathsRegistry

class test_isfile(FunctionLibraryBase):
#doc string

    def __init__(self, packageName):
        super(test_isfile, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_absolute (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.absolute(self)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_as_posix (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.as_posix(self)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_as_uri (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.as_uri(self)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_chmod (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 mode=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 follow_symlinks=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.chmod(self, mode, follow_symlinks)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path.cwd():
        return Path.cwd()

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_exists (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.exists(self)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_expanduser (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.expanduser(self)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_glob (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 pattern=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.glob(self, pattern)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_group (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.group(self)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_hardlink_to (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 target=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.hardlink_to(self, target)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path.home():
        return Path.home()

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_is_absolute (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.is_absolute(self)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_is_block_device (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.is_block_device(self)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_is_char_device (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.is_char_device(self)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_is_dir (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.is_dir(self)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_is_fifo (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.is_fifo(self)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_is_file (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.is_file(self)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_is_mount (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.is_mount(self)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_is_relative_to (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 other=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.is_relative_to(self, other)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_is_reserved (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.is_reserved(self)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_is_socket (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.is_socket(self)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_is_symlink (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.is_symlink(self)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_iterdir (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.iterdir(self)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_joinpath (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 args=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.joinpath(self, args)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_lchmod (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 mode=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.lchmod(self, mode)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_link_to (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 target=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.link_to(self, target)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_lstat (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.lstat(self)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_match (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 path_pattern=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.match(self, path_pattern)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_mkdir (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 mode=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 parents=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 exist_ok=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.mkdir(self, mode, parents, exist_ok)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_open (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 mode=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 buffering=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 encoding=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 errors=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 newline=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.open(self, mode, buffering, encoding, errors, newline)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_owner (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.owner(self)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_read_bytes (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.read_bytes(self)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_read_text (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 encoding=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 errors=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.read_text(self, encoding, errors)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_readlink (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.readlink(self)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_relative_to (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 other=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.relative_to(self, other)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_rename (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 target=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.rename(self, target)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_replace (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 target=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.replace(self, target)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_resolve (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 strict=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.resolve(self, strict)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_rglob (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 pattern=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.rglob(self, pattern)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_rmdir (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.rmdir(self)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_samefile (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 other_path=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.samefile(self, other_path)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_stat (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 follow_symlinks=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.stat(self, follow_symlinks)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_symlink_to (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 target=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 target_is_directory=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.symlink_to(self, target, target_is_directory)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_touch (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 mode=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 exist_ok=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.touch(self, mode, exist_ok)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_unlink (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 missing_ok=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.unlink(self, missing_ok)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_with_name (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 name=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.with_name(self, name)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_with_stem (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 stem=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.with_stem(self, stem)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_with_suffix (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 suffix=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.with_suffix(self, suffix)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_write_bytes (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 data=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.write_bytes(self, data)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def Path_write_text (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 data=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 encoding=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 errors=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 newline=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return Path.write_text(self, data, encoding, errors, newline)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def TestIsFile_test_isfile (self=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return TestIsFile.test_isfile(self)

    @staticmethod
    @IMPLEMENT_NODE(returns=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                    meta={NodeMeta.CATEGORY: '{category}', NodeMeta.KEYWORDS: ['T', 'E', 'S'], NodeMeta.CACHE_ENABLED: False})
    def assert_ (val=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']}), 
                 msg=('AnyType', None, {PinSpecifires.SUPPORTED_DATA_TYPES: ['AnyType']})):
        return assert_(val, msg)
