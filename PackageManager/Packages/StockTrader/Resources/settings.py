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

import os

import platform

from QuantLib import *

#from sklearn import preprocessing
#from sklearn.ensemble import RandomForestClassifier
#from sklearn import neighbors
#from sklearn.ensemble import AdaBoostClassifier
#from sklearn.ensemble import GradientBoostingClassifier
#from sklearn.svm import SVC
#import operator

#from sklearn import *
#from dateutil import parser
#from backtest import Strategy, Portfolio

from matplotlib import *
use('Qt5Agg')
from matplotlib.finance import *


#from TreeViewAlchemy import *

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtSql import *
from PySide6.uic import *

basepath = os.path.dirname(os.path.abspath(__file__))
settingDatabase = "DSSettings.db"
settingTable = "tblProgramSettings"

from PackageManager.Packages.StockTrader.Database.dbBase import *

print("Loading on Platform:", platform.system())

if platform.system() == "Linux": LocalEngine = 'sqlite:////media/david/Template.db'
if platform.system() == "Windows": LocalEngine = 'sqlite:///D:Template.db'

if 1 == 1:
    engines = {
    "Template": create_engine(LocalEngine),
    "Stock": create_engine("mysql+pymysql://:@127.0.0.1:3306/Stock"),
    "LocalSettings": create_engine('sqlite:///DSSettings.db')
    }
else:
    engines = {
        "Template": create_engine(LocalEngine),
        "Phoebe": create_engine("mysql+pymysql://dlario@192.168.0.24:3306/Stock"),
                    #isolation_level="READ UNCOMMITTED"),,
        "LocalSettings": create_engine('sqlite:///DSSettings.db')
    }

#This is for MYSQL
engines["Stock"].execute("CREATE DATABASE IF NOT EXISTS Stock;")
engines["Stock"].execute("USE Stock")
#"Phoebe": create_engine('sqlite:///ActivityManager.db'),

# from dbTemplateTables import *
# from dbActivityTables import *

from PackageManager.Packages.StockTrader.Database.dbStockTrader import *

#TemplateBase.metadata.create_all(TemplateDatabase)
#MainBase.metadata.create_all(MainDatabase)

MainBase.metadata.create_all(engines["Stock"])

#Base.metadata.create_all(engines["Phoebe"])
MainBase.metadata.create_all(engines["LocalSettings"])

binds = {"LocalSettings": engines["LocalSettings"], "Stock": engines["Stock"]}

sessions = {
    "Template": scoped_session(sessionmaker(bind=engines["Template"], autocommit=True)),
    "Stock": scoped_session(sessionmaker(bind=engines["Stock"], autocommit=True)),
}

Session = scoped_session(sessionmaker(bind=engines["Stock"], autocommit=True))
session = Session()

#from frmStockMarket import *
