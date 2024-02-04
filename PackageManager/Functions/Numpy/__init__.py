'''Numpy
'''
PACKAGE_NAME = 'Numpy'
# [Class Imports]
from collections import OrderedDict
from PackageManager.UI.UIInterfaces import IPackage
from PackageManager.Packages.Numpy.Commands import RESOURCES_DIR
# [FunctionLibrary]
# [numpy Package]
class Numpy (IPackage):
    """numpy  package
    """

    def __init__(self, Parent):
        super(Numpy , self).__init__()

    @staticmethod
    def GetPinClasses():
        return _PINS

    @staticmethod
    def GetIcon():
        return RESOURCES_DIR + "ProgramLogo.png"

