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
import re
import json
import decimal
import datetime
import pkgutil

'''import customDelegates
#import GeneratePDF
import customTree
import customTable
import ProgramSettings
import DatabaseConnect
import DatabaseTools'''

# import TreeViewAlchemy
from PySide6.QtWidgets import *
from PySide6.QtGui import *

# from PySide6.QtWebEngineWidgets import QWebEngineView

basepath = os.path.dirname(os.path.abspath(__file__))
settingDatabase = "DSSettings.db"
settingTable = "tblProgramSettings"
from sshtunnel import SSHTunnelForwarder

# import openpyxl

# import sqlalchemy_utils
# from qtalchemy.dialogs import *
# from qtalchemy.widgets import *

from PackageManager.Core.Database import DatabaseTools
from PackageManager.Core.Common import myListToStr, strToMyList

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy_filters import apply_filters

from collections import defaultdict

PACKAGES = defaultdict(list)
PACKAGE_PATHS = {}

from PackageManager import Packages
from PackageManager.Packages.ProgramBase.Database.dbMaster import SessionInformation, SyncJournal, MasterTable, DataBaseType
from PackageManager.Packages.ProgramBase.Database.dbGeography import *


class SQLJournal(object):
    def __init__(self):
        self.StatusDict = {}
        self.TagList = []  # This will help with the sync process
        self.source_tag = None
        self.action = None
        self.recordModel = None
        self.recordDict = {}
        self.Record = None
        self.Table = None

    def addRecord(self, recordModel):
        self.recordModel = recordModel
        self.recordDict = self.model_to_dict(recordModel)

    def passTransaction(self, location_id, table_id, recordmodel_id, action, source_tag):
        self.StatusDict[location_id] = {"location_id": location_id, "table_id": table_id, "record_id": recordmodel_id,
                                        "Action": action, "Status": 2, "source_id": source_tag,
                                        "TransactionTime": datetime.datetime.now().isoformat()}

        tag = f"({location_id}-{table_id}-{recordmodel_id})"
        self.TagList.append(tag)

    def failTransaction(self, location_id, table_id, recordmodel_id, action, source_id):
        self.StatusDict[location_id] = {"location_id": location_id, "table_id": table_id, "record_id": recordmodel_id,
                                        "Action": action, "Status": 3, "source_id": source_tag,
                                        "TransactionTime": datetime.datetime.now().isoformat()}

    def postponeTransaction(self, location_id, table_id, recordmodel_id, action, source_id):
        self.StatusDict[location_id] = {"location_id": location_id, "table_id": source_tag, "record_id": recordmodel_id,
                                        "Action": action, "Status": 4,
                                     "source_id": source_id, "TransactionTime": datetime.datetime.now().isoformat()}

    def saveandclose(self, mastersession):
        self.saveTransaction(mastersession)
        self.__del__()

    def saveTransaction(self, session):
        JSONRecord = json.dumps(self.recordDict, indent=4)
        JSONStatus = json.dumps(self.StatusDict, indent=4)

        JSONTag = json.dumps(self.TagList, indent=4)

        session.begin_nested()
        newrecord = SyncJournal(action=self.action,
                                source=self.source_tag,
                                recordJson=JSONRecord,
                                syncStatus=JSONStatus,
                                tagJSON=JSONTag)
        session.add(newrecord)
        session.commit()
        session.refresh(newrecord)
        session.close()

    def __del__(self):
        return "destroyed"

    def model_to_dict(self, model):
        returndict = {}
        for modelitem in inspect(model).mapper.column_attrs:
            if getattr(model, modelitem.key) is not None:
                returndict[modelitem.key] = getattr(model, modelitem.key)


class SQLSession(object):
    def __init__(self, instanceName, defaultpaths=[]):
        super(SQLSession, self).__init__()
        self.instanceName = instanceName
        self.base = None
        self.engine = None
        self.session = None
        self.scopedSession = None

        self.TABLE_PATHS = {}
        self.TABLELOCATIONS = []
        self.packageTables = {}
        self.packageBases = {}
        self.REGISTERED_BASES = {}

        # self.PackagePaths = Packages.__path__
        # self.autocommit = True

    def GET_PACKAGE_TABLE(self, tableName):
        return self.REGISTERED_TABLES[tableName]

    def GET_PACKAGE_TABLES(self):
        return self.REGISTERED_TABLES

    def addTablePaths(self, additionalTableLocations=[]):
        def ensureTablePath(inPath):
            for subFolder in os.listdir(inPath):
                subFolderPath = os.path.join(inPath, subFolder)
                if os.path.isdir(subFolderPath):
                    if "ProgramBase" in os.listdir(subFolderPath):
                        subFolderPath = os.path.join(subFolderPath, "ProgramBase", "Packages")
                        if os.path.exists(subFolderPath):
                            return subFolderPath
            return inPath

        def recurseTablePaths(inPath):
            paths = []
            for subFolder in os.listdir(inPath):
                subFolderPath = os.path.join(inPath, subFolder)
                if os.path.isdir(subFolderPath):
                    if "PackageManager" in os.listdir(subFolderPath):
                        subFolderPath = os.path.join(subFolderPath, "PackageManager", "Packages")
                        if os.path.exists(subFolderPath):
                            paths.append(subFolderPath)
            return paths

        # check for additional package locations
        if "PackageManager_TABLE_PATHS" in os.environ:
            delim = ';'
            pathsString = os.environ["PackageManager_TABLE_PATHS"]
            # remove delimeters from right
            pathsString = pathsString.rstrip(delim)
            for packagesRoot in pathsString.split(delim):
                if os.path.exists(packagesRoot):
                    paths = recurseTablePaths(packagesRoot)
                    self.PackagePaths.extend(paths)

        for packagePathId in range(len(additionalTableLocations)):
            tablePath = additionalTableLocations[packagePathId]
            tablePath = ensureTablePath(tablePath)
            additionalTableLocations[packagePathId] = tablePath

        self.PackagePaths.extend(additionalTableLocations)

        for importer, modname, ispkg in pkgutil.iter_modules(self.PackagePaths):
            try:
                if ispkg:
                    print("loads: " + modname)
                    mod = importer.find_module(modname).load_module(modname)
                    # mod = importlib.import_module(modname) #This way can be used too
                    package = getattr(mod, modname)(None)
                    a = package
                    self.REGISTERED_TABLES[modname] = package
                    '''__PACKAGE_PATHS[modname] = os.path.normpath(mod.__path__[0])'''
            except Exception as e:
                QMessageBox.critical(None, str("Fatal error"), "Error On Module %s :\n%s" % (modname, str(e)))
                continue
        a = package
        '''def PreferenceWindow(self):
            for name, package in self.GET_PACKAGES().items():
               prefsWidgets = package.PrefsWidgets()
               if prefsWidgets is not None:
                   for categoryName, widgetClass in prefsWidgets.items():
                       PreferencesWindow().addCategory(categoryName, widgetClass())
                   PreferencesWindow().selectByName("General")'''

    def loadTables(self, packagename, Parent=None):
        # loads package to memory\
        # Creates the command register to build the menus
        self.PackagePaths = Packages.__path__
        for importer, modname, ispkg in pkgutil.iter_modules(self.PackagePaths):
            try:
                if ispkg:
                    print("Tables: " + modname)
                    mod = importer.find_module(modname).load_module(modname)
                    # mod = importlib.import_module(modname) #This way can be used too
                    package = getattr(mod, modname)(Parent)
                    PACKAGES[modname] = package
                    PACKAGE_PATHS[modname] = os.path.normpath(mod.__path__[0])
            except Exception as e:
                QMessageBox.critical(None, str("Fatal error"), "Error On Module %s :\n%s" % (modname, str(e)))
                continue

        self.REGISTERED_BASES = PACKAGES[packagename].GetBases().items()

        tableItems = PACKAGES[packagename].GetTables()
        if packagename not in self.packageTables:
            self.packageTables[packagename] = {}
        for counter, tableName in enumerate(tableItems):
            if tableName not in self.packageTables:
                self.packageTables[packagename][tableName] = tableItems[tableName]

    def createSession(self, base, dbtype, user, password, host, port, dbname, key=None, sshTunnel=None):
        if dbtype == "excel":
            pass
        else:
            if sshTunnel is not None:
                server = SSHTunnelForwarder(
                    sshTunnel,
                    ssh_pkey=key,
                    ssh_password=password,
                    ssh_username=user,
                    remote_bind_address=(host, port))  # '127.0.0.1', 3306))
                server.start()
                self.engine = create_engine('%s://%s:%s@%s:%s/%s' % (dbtype, user, password, host, server.local_bind_port))

            elif dbtype == "mysql+pymysql":
                self.engine = create_engine(f"{dbtype}://{user}:{password}@{host}:{port}/{dbname}")
            elif dbtype == "sqlite":
                self.engine = create_engine(f'sqlite:///{host}')

            for name, baseClass in self.REGISTERED_BASES:
                if name == base:
                    baseClass.metadata.create_all(self.engine)

            self.scopedSession = scoped_session(sessionmaker(bind=self.engine))
            self.session = self.scopedSession()


class Register(object):
    def __init__(self, main):
        self.sqlDict = {}
        self.main = main
        self.packageTables = defaultdict(list)
        self.preferenceWindow = {}
        self.scopedSessionDict = {}
        self.engineDict = {}
        self.baseDict = {}
        self.sessionDict = {}
        self.instanceSesssionDict = {}
        self.locationList = []
        self.packageTableDict = main.packageRegister.packageInstanceTables
        self.packageBaseDict = main.packageRegister.packageInstanceBase

        self.masterBase = None
        self.masterSession = None
        self.masterTable = MasterTable
        self.FieldTable = None

        self.masterTableID = None
        self.syncDict = {}

        self.databaseController = DatabaseTools.DatabaseController(self)

    def registarInstance(self, connectionDict):
        # "Base, Session, DatabaseType, Login, Password, Address, Port, Schema, Key, SSHTunnel"
        self.connectionDict = connectionDict
        self.sqlDict[connectionDict["Session"]] = SQLSession(connectionDict["Session"])
        self.syncDict[connectionDict["Session"]] = connectionDict["SyncType"]
        self.locationList.append(connectionDict["Session"])
        '''self.sessionDict[packageName] = SQLSession(packageName).session
        self.baseDict[packageName] = SQLSession(packageName).base
        self.engineDict[packageName] = SQLSession(packageName).engine'''

    def createMasterTableidDict(self, Location):
        queryrecord = self.masterSession.query(MasterTable).all()
        self.masterTableID = {}
        for name, session in self.sqlDict.items():
            self.masterTableID[name] = {}

        for record in queryrecord:
            SyncTags = record.SyncTags
            if SyncTags is not None:
                synclist = self.StringToList(SyncTags)
                for tag in synclist:
                    itemlist = tag[1:-1].split("-")
                    location_id = int(itemlist[0])
                    table_id = int(itemlist[1])
                    record_id = int(itemlist[2])
                    queryLocationx = self.masterSession.query(SessionInformation).filter_by(id=location_id).first()
                    self.masterTableID[queryLocationx.SessionName][record.TableName] = record_id

            self.masterTableID[record.TableName] = record.id
            self.masterTableID[Location][record.TableName] = record.id

    def registarPackage(self, instanceName, packageName, TableDict):
        self.sqlDict[instanceName].packageTables[packageName] = TableDict

    def registarinstancesession(self, instance_id, sesssionname, session):
        # This allows for instance to change their session references in realtime.
        self.instanceSesssionDict[instance_id] = {"SessionName": sesssionname, "Session": session}

    def connectDatabase(self, Location):
        self.sqlDict[Location].createSession(self.connectionDict["Base"],
                                              self.connectionDict["DatabaseType"],
                                              self.connectionDict["Login"],
                                              self.connectionDict["Password"],
                                              self.connectionDict["Address"],
                                              self.connectionDict["Port"],
                                              self.connectionDict["Schema"],
                                              self.connectionDict["Key"],
                                              self.connectionDict["SSHTunnel"])

    def changeinstancesession(self, instance_id, sesssionname, session):
        self.instanceSesssionDict[instance_id][sessionname]

    def updateDatabaseController(self, packagename):
        self.updateMasterTable(packagename)

    def getPackageTable(self, packageName, tableName):
        return self.packageTableDict[packageName][tableName]

    def getTableID(self, tableDict):
        #Add some values of what you know and if it returns one record then you are good.
        # If it returns more than one then you need to add more values.
        # If it returns none then it will add new record.

        filtered_query = self.masterSession.query(MasterTable)
        for field, value in tableDict.items():
            if value is not None:
                filter_spec = [{'field': field, 'op': '==', 'value': value}]
                filtered_query = apply_filters(filtered_query, filter_spec)

        if filtered_query.count() == 1:
            return filtered_query.first().id

        if filtered_query.count() > 1:
            print("Multiple records found")
            return None

        if filtered_query.count() == 0:
            self.masterSession.begin_nested()
            newrecord = MasterTable()
            noneNullRecords = 0
            for field, value in tableDict.items():
                if value is not None and len(value):
                    noneNullRecords += 1
                    print(field, value)
                    setattr(newrecord, field, value)

            if noneNullRecords > 1:
                self.masterSession.add(newrecord)
                self.masterSession.commit()
                #self.sqlDict["Master"].session.close()
                return newrecord.id
            else:
                print("Not enough information to create a new record")
                return None

    def setSessions(self, sessions, Location):
        for key, value in enumerate(sessions):
            sessions[value] = self.sqlDict[Location].session
        return sessions

    def saveSession(self, packageName, connectiondict):
        # SessionName, DatabaseType, Address, Port, Login, Password, Schema, LBP, databaselist
        querydict = {}
        sessionLocations = []
        recordDict = {}

        for Location, dictValues in connectiondict.items():
            recordDatabaseType = self.addGetAddListItem(self.locationList, packageName,
                                                        DataBaseType, dictValues["DatabaseType"])
            for Location2 in self.locationList:
                session = self.sqlDict[Location2].session
                recordquery = session.query(SessionInformation).filter_by(
                    SessionName=dictValues["Session"],
                    DatabaseType=recordDatabaseType[Location],
                    Address=dictValues["Address"]).first()

                if recordquery is not None:
                    recordDict[Location2] = recordquery.id
                else:
                    sessionLocations.append(Location2)

            for Location2 in sessionLocations:
                #todo: get the packagename from the sessionlocations
                recordDatabaseType = self.addGetAddListItem(self.locationList, "PackageManager",
                                                            DataBaseType, dictValues["DatabaseType"])

                querydict[Location2] = SessionInformation(SessionName=dictValues["Session"],
                                                         DatabaseType=recordDatabaseType[Location],
                                                         Address=dictValues["Address"],
                                                         Port=dictValues["Port"],
                                                         Login=dictValues["Login"],
                                                         Password=dictValues["Password"],
                                                         Schema=dictValues["Schema"])
            if sessionLocations != []:
                recordDict = self.createRecord("PackageManager", SessionInformation,
                                                           querydict,
                                                           sessionLocations,
                                                           recordDict)
        return recordDict

        '''#SSHTunnelForwarder
        id = Column(Integer, primary_key=True)
        Address = Column(String(255))
        Port = Column(Integer)
        Login = Column(String(255))
        Password = Column(String(255))'''

    def createRecord(self, packagename, tableClass, RecordClass, sessionlocations, sourceTag, record_idDict=None):
        if record_idDict is None:
            record_idDict = {}
        syncItem = SQLJournal()
        syncItem.Table = tableClass
        syncItem.Table_id = self.getTableID(packagename, tableClass.__name__)
        taglist = []

        for Location in sessionlocations:
            session = self.sqlDict[Location].session
            record_idDict[Location] = None
            queryLocation = self.masterSession.query(SessionInformation).filter_by(SessionName=Location).first()

            if self.syncDict[Location] == "ASAP":
                try:
                    session.begin_nested()
                    rows = session.query(tableClass).count()
                    if rows == 0:
                        NullFirstRecord = tableClass()
                        session.add(NullFirstRecord)
                        session.commit()

                    session.add(RecordClass[Location])
                    syncItem.recordDict = self.model_to_dict(RecordClass[Location])
                    session.commit()
                    record_idDict[Location] = RecordClass[Location].id
                    syncItem.passTransaction(Location, syncItem.Table_id, RecordClass[Location].id, "Add Record", sourceTag)
                    taglist.append(f"({queryLocation}-{syncItem.Table_id}-{RecordClass[Location].id})")
                except:
                    session.rollback()
                    syncItem.failTransaction(Location, syncItem.Table_id, None, "Add Record", sourceTag)
                finally:
                    session.close()
            else:
                syncItem.postponeTransaction(Location, syncItem.Table_id, None, "Add Record", sourceTag)

        # add the synctags to the records so they can talk to each other
        for Location in sessionlocations:
            if record_idDict[Location] is not None:
                session = self.sqlDict[Location].session
                try:
                    queryrecord = session.query(tableClass).filter_by(id=record_idDict[Location]).first()
                    queryrecord.SyncTags = myListToStr(taglist)
                    session.commit()
                finally:
                    session.close()

        syncItem.saveandclose(self.masterSession)

        return record_idDict

    def getRecordID(self, Location, TableClass, FieldName, FieldValue):
        searchrecord = self.sqlDict[Location].session.query(TableClass)
        fkfilter3 = [{'field': FieldName, 'op': '==', 'value': FieldValue}]
        searchrecord = apply_filters(searchrecord, fkfilter3)

        if searchrecord.count() == 0:
            self.sqlDict["Location1"].session.begin_nested()
            searchrecord = TableClass()
            setattr(searchrecord, FieldName, FieldValue)
            self.sqlDict["Location1"].session.add(searchrecord)
            self.sqlDict["Location1"].session.commit()
        else:
            searchrecord = searchrecord.first()
        return searchrecord.id

    def findRecord(self, sessionName, packagename, tableClass, RecordClass, sessionlist, sessionlocations):
        record_idDict = {}

        for Location in sessionlocations[sessionName]:
            session = self.sqlDict[Location].session
            try:
                session.begin_nested()

                record_idDict[Location] = RecordClass[Location].id
            finally:
                session.close()

        return record_idDict

    def model_to_dict(self, model):
        returndict = {}
        for modelitem in inspect(model).mapper.column_attrs:
            if getattr(model, modelitem.key) is not None:
                value = getattr(model, modelitem.key)
                # Convert datetime and date instances to string (ISO format)
                if isinstance(value, (datetime.datetime, datetime.date)):
                    returndict[modelitem.key] = value.isoformat()
                # Convert Decimal instances to float
                elif isinstance(value, decimal.Decimal):
                    returndict[modelitem.key] = float(value)
                # Include other values if they are not None
                elif value is not None:
                    returndict[modelitem.key] = value
        return returndict

    def addGetAddListItem(self, databaselist, packageName, tableClass, value):

        querydict = {}
        sessionLocations = []
        recordDict = {}

        for Location in databaselist:
            recordquery = self.sqlDict[Location].session.query(
                tableClass).filter_by(NameText=value).first()

            if recordquery is not None:
                recordDict[Location] = recordquery.id
            else:
                sessionLocations.append(Location)

        # todo this would be also be a good spot to put a gpt assessment of similar names.
        for Location in databaselist:
            querydict[Location] = tableClass(NameText=value)
        if sessionLocations != []:
            recordDict = self.createRecord(packageName, tableClass,
                                                       querydict,
                                                       sessionLocations,
                                                       recordDict)
        return recordDict

    def addGetAddAOGItem(self, databaselist, packageName, aogtype, parent_id, value):
        table_id = None
        record_id = None

        if aogtype == "Country":
            table_id = self.getTableID({"Package": packageName, "ClassName": "Country", "DataSourceFormat": "SQL"})
            record_id = self.addGetAddListItem(databaselist, packageName, Country, value)
        elif aogtype == "City":
            table_id = self.getTableID({"Package": packageName, "ClassName": "City", "DataSourceFormat": "SQL"})
            record_id = self.addGetAddListItem(databaselist, packageName, City, value)
        elif aogtype == "Municipality":
            table_id = self.getTableID({"Package": packageName, "ClassName": "Municipality", "DataSourceFormat": "SQL"})
            record_id = self.addGetAddListItem(databaselist, packageName, Municipality, value)

        querydict = {}
        recordDict = {}
        sessionLocations = []
        if table_id is not None and record_id is not None:
            for Location in databaselist:
                recordquery = self.sqlDict[Location].session.query(
                    AreaOfGovernance).filter_by(Table_id=table_id,
                                                Record_id=record_id,
                                                Parent_id=parent_id).first()

                if recordquery is not None:
                    recordDict[Location] = recordquery.id
                else:
                    sessionLocations.append(Location)

            # todo this would be also be a good spot to put a gpt assessment of similar names.
            for Location in databaselist:
                querydict[Location] = AreaOfGovernance(Table_id=table_id,
                                                       Record_id=record_id,
                                                       Parent_id=parent_id)

            recordDict = self.createRecord(self.packageName, AreaOfGovernance,
                                           querydict,
                                           sessionLocations,
                                           recordDict)
        else:
            for Location in databaselist:
                recordDict[Location] = 1
        return recordDict

    def updateMasterTable(self, packagemame):
        currentdatetime = datetime.datetime.now()

        # inspector = inspect(packagesession.bind.engine)
        # for TableName in inspector.get_table_names():
        for key, ClassName in enumerate(self.packageTableDict[packagemame]):
            SelectedTable = self.packageTableDict[packagemame][ClassName]
            TableName = SelectedTable.__tablename__

            TableTypeValue = 1
            if TableName[:3] == "lst":
                TableTypeValue = 5
            if TableName[:3] == "att":
                TableTypeValue = 2
            if TableName[:3] == "btb":
                TableTypeValue = 3

            self.masterSession.begin()
            masterRecord = MasterTable(TableType_id=TableTypeValue,
                                       Package=packagemame,
                                       File="",
                                       ClassName=SelectedTable.__tablename__,
                                       TableName=TableName)

            for column in SelectedTable.__table__.columns:
                if column.key == "NameText":
                    masterRecord.DisplayColumn = "NameText"
                    masterRecord.DisplayQuery = f"SELECT id, NameText FROM {TableName}"
                if column.key == "Title":
                    masterRecord.DisplayColumn = "Title"
                    masterRecord.DisplayQuery = f"SELECT id, Title FROM {TableName}"
                if column.key == "FullName":
                    masterRecord.DisplayColumn = "FullName"
                    masterRecord.DisplayQuery = f"SELECT id, FullName FROM {TableName}"

            self.masterSession.add(masterRecord)
            self.masterSession.commit()
            self.masterSession.close()

    def getallTagTableRef(self, TagString, TagTable):
        taglist = set(re.findall(r"[\(]" + str(TagTable) + "-[0-9]+\)", TagString, re.I))
        outputtagdata = []
        for tagitem in taglist:
            try:
                outputtagdata.append(self.getTagInfo(tagitem))
            except:
                pass
        return outputtagdata

    def getTagInfo(self, packageName, location, Tag):
        itemlist = Tag[1:-1].split("-")
        table_id = int(itemlist[0])
        item_id = int(itemlist[1])
        Value = [None, None, None, None]

        self.masterTable = MasterTable
        self.FieldTable = None

        try:
            query1 = self.masterSession.query(self.masterTable).filter_by(id=int(table_id)).first()
            tableClass = self.getPackageTable(packageName, query1.ClassName)

            if query1.DisplayColumn is not None:
                ColumnClass = getattr(tableClass, query1.DisplayColumn)

                query2 = self.sqlDict[packageName].session.query(ColumnClass).filter_by(id=item_id).first()

                if query2:
                    Value[0] = query1.TableName
                    Value[1] = query2[0]
                    Value[2] = table_id
                    Value[3] = item_id
            else:
                Value[0] = query1.TableName
                Value[1] = item_id
                Value[2] = table_id
                Value[3] = item_id
        except:
            pass

        return Value

    def addTags(self, mastertable_id, newTag):
        # Used for filter favorite tags, but could be also used to determine type of table (ie list, primary, treeview)
        query1 = self.sessiondict["Master"].query(self.MasterTable).filter_by(id=int(mastertable_id)).first()
        if query1:
            TagList = strToMyList(query1.Tags)
            if newTag not in TagList:
                TagList.append(newTag)

            TagString = myListToStr(TagList)

            self.sessiondict["Master"].begin()
            query1.Tags = TagString
            self.sessiondict["Master"].commit()
            self.sessiondict["Master"].flush()

    def removeTags(self, mastertable_id, newTag):
        # Used for filter favorite tags, but could be also used to determine type of table (ie list, primary, treeview)
        query1 = self.sessiondict["Master"].query(self.MasterTable).filter_by(id=int(mastertable_id)).first()
        if query1:
            TagList = DatabaseTools.strToMyList(self.MasterTable.Tags)
            TagList(filter((newTag).__ne__, x))

            TagString = DatabaseTools.myListToStr(TagList)

            self.sessiondict["Master"].begin()
            self.MasterTable.Tags = TagString
            self.sessiondict["Master"].commit()
            self.sessiondict["Master"].flush()

    def displayTableData(self, mastertable_id, displayquery):

        query1 = self.sessiondict["Master"].query(self.MasterTable).filter_by(id=int(mastertable_id)).first()
        query2 = self.sessiondict["Master"].query(self.sessionTable).filter_by(id=int(query1.Session)).first()

        selectedTableModel = QStandardItemModel(0, 2)
        conn = self.sessiondict["Master"].connection()
        try:
            conn2 = self.sessiondict[query2.NameText].connection()

            if displayquery is not None:
                records = conn2.execute(displayquery).fetchall()

                if records != []:
                    for row, ItemName in enumerate(records):
                        Descriptor_id = QStandardItem("%i" % ItemName[0])
                        Descriptor_Name = QStandardItem(ItemName[1])
                        table_id = QStandardItem("%i" % int(mastertable_id))

                        selectedTableModel.setItem(row, 0, Descriptor_id)
                        selectedTableModel.setItem(row, 1, Descriptor_Name)
                        selectedTableModel.setItem(row, 2, table_id)
                conn2.close()
                conn.close()
                return selectedTableModel

            else:
                print("No Records to Display")
                return None

        except:
            return None
