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

from PackageManager.Packages.ProgramBase.Database.dbProgramBase import *
from PackageManager.Packages.ProgramBase.Database.dbGeography import *
from PackageManager.Packages.ProgramBase.Database.dbMaster import *
from PackageManager.Packages.ProgramBase.Database.dbUnits import *

def defaultData():
    defaultNameTextData = {"TableSelectionType": {"Table": TableSelectionType, "Data": ["Single", "Multiple"]},
                           "DataType": {"Table": DataType,
                                        "Data": ["Text", "Number", "Date", "Boolean", "Currency", "Percentage", "Time",
                                                 "Image",
                                                 "File"]},
                           "UnitType": {"Table": UnitType,
                                        "Data": ["Length", "Area", "Volume", "Mass", "Time", "Speed", "Temperature",
                                                 "Energy",
                                                 "Power",
                                                 "Force", "Pressure", "Frequency", "Voltage", "Current", "Resistance",
                                                 "Capacitance",
                                                 "Inductance", "Charge", "Magnetic Flux", "Magnetic Flux Density",
                                                 "Illuminance",
                                                 "Luminous Flux", "Luminous Intensity", "Angle", "Solid Angle"]},
                           "Unit": {"Table": Unit, "Data": ["Text", "Number", "Date", "Boolean", ]},
                           "Country": {"Table": Country, "Data": ["Canada", "United States"]},
                           "City": {"Table": City, "Data": ["Silver Valley", "Grande Prairie"]},
                           "AoGType": {"Table": AoGType, "Data": ["National", "Provincial", "Local"]},
                           "Municipality": {"Table": Municipality, "Data": []},
                           "DatabaseActions":{"Table": DatabaseAction, "Data": ["Add Record", "Remove Record", "Update Record"]}}
    return defaultNameTextData
