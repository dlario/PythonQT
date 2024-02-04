'''Cycler
'''
PACKAGE_NAME = 'Cycler'
# [Class Imports]
from collections import OrderedDict
from PackageManager.UI.UIInterfaces import IPackage
from PackageManager.Packages.Cycler.Commands import RESOURCES_DIR
# [FunctionLibrary]
# [cycler Package]
class Cycler (IPackage):
    """cycler  package
    """

    def __init__(self, Parent):
        super(Cycler , self).__init__()

    @staticmethod
    def GetPinClasses():
        return _PINS

    @staticmethod
    def GetIcon():
        return RESOURCES_DIR + "ProgramLogo.png"

