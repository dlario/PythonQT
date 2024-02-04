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

# region Python Imports
import os
from datetime import *
#import sqlalchemy_utils
import re
import decimal
import pyodbc
# endregion

# region External Programs
from sqlalchemy import inspect, create_engine
from sqlalchemy import TypeDecorator
# endregion

# region PySide Imports
from PySide6.QtGui import QStandardItem, QStandardItemModel
from sqlalchemy.orm import scoped_session, sessionmaker

# endregion

# region Core Imports
from PackageManager.Core.Common import strToMyList, myListToStr
# endregion

# region Database Imports
from PackageManager.UI.Widgets import customTable
from PackageManager.Packages.ProgramBase.Database.dbMaster import *
from PackageManager.Packages.ProgramBase.Database.dbProgramBase import *
# endregion

# region Widgets

# endregion

# region Base Forms

# endregion

# region Import Tables

# endregion

# region Default Settings

# endregion

class MyFancyType(TypeDecorator):
    impl = Integer

    def process_literal_param(self, value, dialect):
        return "my_fancy_formatting(%s)" % value

class DatabaseController(object):

    def __init__(self, sessions):

        self.MasterTable = sessions.masterTable
        self.MasterBase = sessions.masterBase
        self.MasterSession = sessions.masterSession
        self.session = sessions

    def getallTagTableRef(self, TagString, TagTable):
        taglist = set(re.findall(r"[\(]" + str(TagTable) + "-[0-9]+\)", TagString, re.I))
        outputtagdata = []
        for tagitem in taglist:
            try:
                outputtagdata.append(self.getTagInfo(tagitem))
            except:
                pass
        return outputtagdata

    def getTagInfo(self, Tag):
        itemlist = Tag[1:-1].split("-")
        table_id = int(itemlist[0])
        item_id = int(itemlist[1])
        Value = [None, None, None, None]

        try:
            query1 = self.session.query(self.MasterTable).filter_by(id=int(table_id)).first()
            if query1:
                querybase = self.session.query(self.baseTable).filter_by(id=int(query1.Base)).first()
                querysession = self.session.query(self.sessionTable).filter_by(id=int(query1.Session)).first()

                tableclass = self.get_class_by_tablename(self.basedict[querybase.NameText],
                                                                        query1.TableName)
                columndict = self.get_fields_by_tablename(self.basedict[querybase.NameText],
                                                                         query1.TableName)

                '''tableclass = lario.DatabaseTools.get_class_by_tablename(self.basedict[self.activedatabase][query1.Base], query1.TableName)
                columndict = lario.DatabaseTools.get_fields_by_tablename(self.basedict[self.activedatabase][query1.Session], query1.TableName)'''

                if query1.DisplayColumn is not None:
                    ColumnClass = getattr(tableclass, query1.DisplayColumn)

                    query2 = self.sessiondict[querysession.NameText].query(ColumnClass).filter_by(id=item_id).first()

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
            TagList = strToMyList(self.MasterTable.Tags)
            TagList(filter((newTag).__ne__, x))

            TagString = self.myListToStr(TagList)

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

    def updateMasterTable(self):
        currentdatetime = datetime.datetime.now()

        for index, key in enumerate(self.engineDict[1]):
            inspector = inspect(self.engineDict[1][key])
            for TableName in inspector.get_table_names():

                # Load up the tables to the master table if its not there
                qryBase = self.session.query(self.baseTable).filter_by(NameText=key).first()
                if qryBase is None:
                    self.session.begin()
                    qryBase = self.baseTable(NameText=key)
                    self.session.add(qryBase)
                    self.session.commit()
                    self.session.flush()

                qrySession = self.session.query(SessionNames).filter_by(NameText=key).first()
                if qrySession is None:
                    self.session.begin()
                    qrySession = SessionNames(NameText=key)
                    self.session.add(qrySession)
                    self.session.commit()
                    self.session.flush()

                SelectedTable = self.get_class_by_tablename(self.baseDict[key], TableName)
                print(self.baseDict[key], TableName)

                qryMasterSession = self.session.query(MasterTable).filter_by(Base=qryBase.id) \
                    .filter_by(Session=qrySession.id) \
                    .filter_by(TableName=TableName).first()

                if qryMasterSession is None and SelectedTable is not None:  # and TableName != "lsttabletype": # and TableName != "Name" and TableName != "dataType":
                    TableTypeValue = None
                    DisplayColumn = None
                    DisplayQuery = None

                    if SelectedTable is not None:
                        for column in SelectedTable.__table__.columns:
                            '''masterField.key
                            masterField.type
                            masterField._data'''
                            if column.key == "NameText":
                                DisplayColumn = "NameText"
                                DisplayQuery = f"SELECT id, NameText FROM {TableName}"
                            if column.key == "Title":
                                DisplayColumn = "Title"
                                DisplayQuery = f"SELECT id, Title FROM {TableName}"
                            if column.key == "FullName":
                                DisplayColumn = "FullName"
                                DisplayQuery = f"SELECT id, FullName FROM {TableName}"

                    if TableName[:3] == "lst":
                        TableTypeValue = 5
                    if TableName[:3] == "att":
                        TableTypeValue = 2
                    if TableName[:3] == "btb":
                        TableTypeValue = 3

                    self.session.begin()
                    qryMasterSession = MasterTable(TableName=TableName,
                                                   Base=qryBase.id,
                                                   Session=qrySession.id,
                                                   DisplayColumn=DisplayColumn,
                                                   DisplayQuery=DisplayQuery,
                                                   TableType_id=TableTypeValue)
                    self.session.add(qryMasterSession)
                    self.session.commit()
                    self.session.flush()

                if qryMasterSession is not None and SelectedTable is not None:
                    self.session.begin()
                    if qryMasterSession.DisplayColumn is None and SelectedTable is not None:
                        for column in SelectedTable.__table__.columns:
                            if column.key == "NameText":
                                qryMasterSession.DisplayColumn = "NameText"
                                qryMasterSession.DisplayQuery = "SELECT id, NameText FROM %s" % (TableName)
                            if column.key == "Title":
                                qryMasterSession.DisplayColumn = "Title"
                                qryMasterSession.DisplayQuery = "SELECT id, Title FROM %s" % (TableName)
                            if column.key == "FullName":
                                qryMasterSession.DisplayColumn = "FullName"
                                qryMasterSession.DisplayQuery = "SELECT id, FullName FROM %s" % (TableName)

                    self.session.DateAccessed = currentdatetime
                    self.session.commit()
                    self.session.flush()

    def addUpdateRow(self, table1row, table2, ignored_columns=[]):
        copy = type(table1row)()
        for col in table1row.__table__.columns:
            if col.name not in ignored_columns:
                try:
                    copy.__setattr__(col.name, getattr(table1row, col.name))
                except Exception as e:
                    print(e)
                    continue
        return copy


    def loadDefaultData(self, package, defaultdata):
        from PackageManager.Packages.ProgramBase.Database import dbMaster
        from PackageManager.Packages.ProgramBase.Database import DefaultData

        for item, value in enumerate(defaultdata):
            table = defaultdata[value]["Table"]
            data = defaultdata[value]["NameText"]
            rows = self.session.query(table).count()
            if rows == 0:
                # The first record in tables should be the null record
                self.session.begin_nested()
                NewRecord = table(NameText="")
                self.session.add(NewRecord)
                self.session.commit()
                self.session.refresh(NewRecord)

            for record in data:
                # Add the default data
                query2 = (self.mainsession.query(dbMasterTables.Reference).
                          filter(dbMasterTables.Reference.Word == record).first())
                if query2 is None:
                    self.mainsession.begin_nested()
                    NewRecord2 = dbMasterTables.Reference(Word=record,
                                                          Language=1)
                    self.mainsession.add(NewRecord2)
                    self.mainsession.commit()
                    self.mainsession.refresh(NewRecord2)

                query = self.session.query(table).filter(table.NameText == record).first()
                if query is None:
                    self.session.begin_nested()
                    NewRecord = table(NameText=record, Name_id=query2.id)
                    self.session.add(NewRecord)
                    self.session.commit()
                    self.session.refresh(NewRecord)


    def syncDatabase(self, session, sourceTable, destinationTable):
        lastSyncDate = session.query(SyncLog).filter_by(sourceTable=sourceTable).filter_by(
            destinationTable=destinationTable).last()
        records = session.query(DataSyncStatements).filter(
            DataSyncStatements.id > lastSyncDate.SyncTableRowEnd)
        sourceTable = session.query(MasterTable).filter_by(id=sourceTable).first()
        sourceSession = session.query(SessionNames).filter_by(id=sourceTable.Session)
        destinationTable = session.query(MasterTable).filter_by(id=destinationTable).first()
        destinationSession = session.query(SessionNames).filter_by(id=destinationTable.Session)

        for record in records:
            if record.QueryType in ["Add", "Update"]:
                filterDict = record.JWhere
                for index, filterItemName in enumerate(filterDict):
                    tableRow = session.query(DataSyncStatements).filter(
                        getattr(sourceTable, filterItemName).in_(filterDict[filterItemName]))
                    self.MasterData.addUpdateRow(tableRow, destinationTable, ["id"])
            elif record.QueryType in ["Delete"]:
                pass

    def get_class_by_tablename(self, Base, table_fullname):
        """Return class reference mapped to table.
        http://stackoverflow.com/questions/11668355/sqlalchemy-get-model-from-table-name-this-may-imply-appending-some-function-to
        :param table_fullname: String with fullname of table.
        :return: Class reference or None.
        """
        for c in Base._decl_class_registry.values():
            if hasattr(c, '__table__') and c.__table__.fullname == table_fullname:
                #print(c.__table__.fullname, table_fullname)
                return c

    def get_fields_by_tableclass(self, tableclass):
        """Return class reference mapped to table."""
        inspector = inspect(tableclass)
        columndict = {m.name: m.type for m in inspector.columns}
        return columndict

    def get_fields_by_tablename(self, Base, table_fullname):
        """Return class reference mapped to table.
        http://stackoverflow.com/questions/11668355/sqlalchemy-get-model-from-table-name-this-may-imply-appending-some-function-to
        :param table_fullname: String with fullname of table.
        :return: Class reference or None.
        """
        for c in Base._decl_class_registry.values():

            try:
                if hasattr(c, '__table__'):
                    #print(c.__table__.fullname)
                    if c.__table__.fullname == table_fullname:
                        columndict = {m.name: m.type for m in c.__table__.columns}
                        return columndict
            except:
                pass

    def row2dictsql(self, querydata):
        columndata = querydata.column_descriptions
        fielddict = {}
        for key, value in enumerate(columndata):
            fielddict[value["name"]] = key

        return fielddict

    def row2dict(self, row, itemdata = {}):
        #http://stackoverflow.com/questions/1958219/convert-sqlalchemy-row-object-to-python-dict
        for column in row.__table__.columns:
            itemdata[column.name] = str(getattr(row, column.name))
        return itemdata

    def row2json(self, querydata):
        data = {}
        for c in inspect(querydata).mapper.column_attrs:
            value = getattr(querydata, c.key)
            # Convert datetime and date instances to string (ISO format)
            if isinstance(value, (datetime.datetime, datetime.date)):
                data[c.key] = value.isoformat()
            # Convert Decimal instances to float
            elif isinstance(value, decimal.Decimal):
                data[c.key] = float(value)
            # Include other values if they are not None
            elif value is not None:
                data[c.key] = value
        return data

    def getFieldName(self, session, Base, listName, id):
        FieldValue = None
        tableName = self.get_class_by_tablename(Base, listName.lower())
        if tableName is not None:
            if int(id) != -1:
                if listName == "reference":
                    tableName = self.get_class_by_tablename(Base, listName.lower())
                    LookupTable = session.query(tableName).filter(tableName.id == int(id)).first()

                    if LookupTable is not None:
                        FieldValue = LookupTable.Word
                        if FieldValue is not None:
                            pass#print("Record Found:", FieldValue)
                        else:
                            print("No Record Found")
                    else:
                        print("No Record Found")
                elif listName[:3] == "lst":
                    tableName = self.get_class_by_tablename(Base, listName.lower())
                    LookupTable = session.query(tableName.NameText).filter(tableName.id == int(id)).first()

                    FieldValue = LookupTable[0]

                    if FieldValue is not None:
                        pass#print("Record Found:", FieldValue)
                    else:
                        print("No Record Found")
        else:
            FieldValue = id
        return FieldValue

    def loadSingleTableCombo(self, session, Base, row, column, attrdict, tblTable):
        # Going to have to put this back in the main code till i figure out how to hook the on change
        # This little ditty is used to load data into a column of a table.
        # cursor = conn.cursor()

        referencetable = attrdict["ReferenceTable"]
        referenceList = attrdict["List"]
        attributelistValue = attrdict["AttributeValue"]

        if attributelistValue == "-" or attributelistValue is None: attributelistValue = 0

        if referenceList is not None and referenceList[:3] == "lst":
            tableName = self.get_class_by_tablename(Base, referenceList.lower())
            tableData = session.query(tableName).order_by(tableName.NameText)
            listDataModel2 = QStandardItemModel(0, 0)
            cmbboxindex = None
            for row2, record in enumerate(tableData):
                listDataModel2.setItem(row2, 0, QStandardItem("%i" % record.id))
                listDataModel2.setItem(row2, 1, QStandardItem(record.NameText))
                if record.Name_id is not None and record.Name_id != "":
                    referenceid = QStandardItem("%i" % record.Name_id)
                    listDataModel2.setItem(row2, 2, referenceid)
                # Add Value from wherever
                    # print(widgetData["List_id"], record.id,record.NameText, referenceid )

                if record.id == int(attributelistValue):
                    # print("Record Found", record.id, record.Name)
                    cmbboxindex = row2

            tblTable.openPersistentEditor(listDataModel2.index(row, column))

            c = customTable.TableComboModel(None, dataModel=listDataModel2, row=row, column=column)

            i = tblTable.model().index(row, column)
            tblTable.setIndexWidget(i, c)
            if cmbboxindex is not None: tblTable.indexWidget(i).setCurrentIndex(cmbboxindex)

            #c.currentIndexChanged2[dict].connect(self.on_tablecmbbox_ValueChanged)
        # This is the reference of a attribute table
        elif referencetable is not None:
            tableName = self.get_class_by_tablename(Base, referencetable.lower())
            # print("ReferenceList", referenceList)
            tableData = None
            if referencetable == "Reference":
                tableData = session.query(tableName).order_by(tableName.Word)
            elif referencetable == "Person":
                tableData = session.query(tableName).order_by(tableName.LastName)
            elif referencetable == "Company":
                tableData = session.query(tableName).order_by(tableName.NameText)

            listDataModel2 = QStandardItemModel(0, 0)
            cmbboxindex = None
            if tableData is not None:
                for row2, record in enumerate(tableData):
                    listDataModel2.setItem(row2, 0, QStandardItem("%i" % record.id))
                    if referencetable == "Reference":
                        listDataModel2.setItem(row2, 1, QStandardItem(record.Word))
                    elif referencetable == "Person":
                        if record.FirstName is not None:
                            FullName = str(record.FirstName) + " " + str(record.LastName)
                            listDataModel2.setItem(row2, 1, QStandardItem(FullName))


                    elif referencetable == "Company":
                        listDataModel2.setItem(row2, 1, QStandardItem(record.NameText))
                        # print(record.Name)
                        if record.Name_id is not None and record.Name_id != "":
                            referenceid = QStandardItem("%i" % record.Name_id)
                            listDataModel2.setItem(row2, 3, referenceid)
                        # Add Value from wherever
                            # print(widgetData["List_id"], record.id,record.NameText, referenceid )

                    if record.id == int(attributelistValue):
                        # print("Record Found", record.id, record.Name)
                        cmbboxindex = row2

            tblTable.openPersistentEditor(listDataModel2.index(row, column))

            c = customTable.TableComboModel(None, dataModel=listDataModel2, row=row, column=column)
            # print("Combobox Inserted",row, column)
            i = tblTable.model().index(row, column)
            tblTable.setIndexWidget(i, c)
            if cmbboxindex is not None: tblTable.indexWidget(i).setCurrentIndex(cmbboxindex)

            #c.currentIndexChanged2[dict].connect(self.on_tablecmbbox_ValueChanged)
        else:
            # print("Setting Text Value", attributelistValue)
            c = customTable.TableLineEditModel(None, row=row, column=column)
            i = tblTable.model().index(row, column)
            tblTable.setIndexWidget(i, c)

            #c.textChanged2[dict].connect(self.on_tabletextbox_ValueChanged)

            databaseIndex = tblTable.model().index(row, column)

            if attributelistValue is not None and tblTable.indexWidget(databaseIndex) is not None:
                tblTable.indexWidget(databaseIndex).setText(str(attributelistValue))
        tblTable.resizeColumnsToContents

    def createfielddict(FieldNames, FieldTypes, FieldOption = None):

        fielddict = {}
        for column, fielditems in enumerate(FieldNames):
            columndict = {}
            columndict["Title"] = fielditems
            columndict["DataType"] = FieldTypes[column]
            if FieldOption is not None: columndict["Options"] = FieldOption[column]
            fielddict[str(column)] = columndict
        return fielddict

class DatabaseConnection(object):
    def __init__(self, connectionDict):
        super(DatabaseConnection, self).__init__()

        if connectionDict:
            self.connectionname = connectionDict["connectionName"]
            if "dialect" in connectionDict: self.dialect = connectionDict["dialect"]
            if "location" in connectionDict: self.location = connectionDict["location"]  # "104.248.176.241"
            self.port = ""
            self.login = ""
            self.password = ""

            if "port" in connectionDict: self.port = connectionDict["port"]
            if "login" in connectionDict: self.login = connectionDict["login"]
            if "password" in connectionDict: self.password = connectionDict["password"]

            self.ssh_pkey = None
            self.ssh_password = None
            self.ssh_username = None
            self.remote_bind_address = None
            self.remote_bind_address_port = None

            if "ssh_pkey" in connectionDict: self.ssh_pkey = connectionDict["ssh_pkey"]
            if "ssh_password" in connectionDict: self.ssh_password = connectionDict["ssh_password"]
            if "ssh_username" in connectionDict: self.ssh_username = connectionDict["ssh_username"]
            if "remote_bind_address" in connectionDict: self.remote_bind_address = connectionDict["remote_bind_address"]
            if "remote_bind_address_port" in connectionDict: self.remote_bind_address_port = connectionDict[
                "remote_bind_address_port"]

        self.base = None
        self.connection = None
        self.schemaDict = {}
        self.schemaClassDict = {}
        self.engine = {}
        self.session = {}
        self.sessiontables = {}

    def sqlAttackCheck(self, phrase):
        # A checker to determine is a SQLAttack is being attempted
        a = 0
        b = 0

        a = phrase.find("Select")
        a = + phrase.find("SELECT")

        b = phrase.find("from")
        b = + phrase.find("FROM")

        if a == 0 and b == 0:
            return True
        else:
            print("Injection Detected")
            return False

    def createTableName(phrase):
        words = phrase.split()
        newPhrase = None
        for count, word in enumerate(words):
            if count == 0:
                newPhrase = word.lower()
            else:
                newPhrase += word.title()
        return newPhrase

    def dbConnect(databasefile):
        # print(databasefile)
        if databasefile != None:

            if databasefile != ":memory:":
                fileType = databasefile.split('.')[1]
            else:
                fileType = "db"

            # print(fileType)
            if fileType == "mdb" or fileType == "accdb":
                sources = pyodbc.dataSources()
                dsns = sources.keys()
                sl = []
                for dsn in dsns:
                    sl.append('%s [%s]' % (dsn, sources[dsn]))
                database = accessDatabase(databasefile)
                conn = pyodbc.connect('Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + str(databasefile))

            elif fileType == "sqlite3" or fileType == "db" or fileType == "db3":
                database = sqliteDatabase(databasefile)
                conn = sqlite3.connect(databasefile, timeout=1)

            # conn = database.getConn()
            return conn

    def getTablesInfo(self):
        self.tableNames = []
        c = self.connSQLite.cursor()

        c.execute("SELECT name FROM sqlite_master WHERE type = \"table\"")
        tableList = c.fetchall()

        for tableName in tableList:
            # print(str(tableName)[2:-3])
            self.tableNames.append(str(tableName)[2:-3])

        return self.tableNames

    def getColumnsInfo(self, tablename):
        c = self.connSQLite.cursor()

        # Retrieve column information
        # Every column will be represented by a tuple with the following attributes:
        # (id, name, type, notnull, default_value, primary_key)

        c.execute('PRAGMA TABLE_INFO({})'.format(tablename))

        # collect names in a list
        names = [tup[1] for tup in c.fetchall()]
        # e.g., ['id', 'date', 'time', 'date_time']
        # Closing the connection to the database file
        return (names)

    def sshConnection(self):
        self.ssh_pkey = self.ssh_pkey  # "D:\Dropbox (Personal)\David Lario - Office\Engima Design Solutions\.ssh\id_rsa"
        self.ssh_password = self.ssh_password
        self.ssh_username = self.ssh_username
        self.remote_bind_address = self.remote_bind_address  # '127.0.0.1'
        self.remote_bind_address_port = self.remote_bind_address_port  # 3306

    def loadTables(self, session):
        '''for name, obj in inspect.getmembers(className):
            if inspect.isclass(obj):
                self.tables[name] = obj'''
        tables = {}
        for c in self.base._decl_class_registry.values():
            try:
                if hasattr(c, '__table__'):
                    tables[c.__table__.fullname] = c
            except:
                pass

        self.sessiontables[session] = tables

    def loadTable(self, TableName):

        for name, obj in inspect.getmembers(sys.modules[__name__]):
            if inspect.isclass(obj):
                self.tables[name] = obj

    def loadSession(self, name):
        self.session[name] = scoped_session(sessionmaker(bind=self.engine[name], autocommit=True))

    def getSessions(self):
        return self.session

    def getBase(self):
        return self.base

    def getSessionTables(self, session):
        return self.sessiontables[session]

    # Dont moves these after creating the engine.  New Tables wont be recognized
    def startSSH(self):
        self.server = SSHTunnelForwarder(self.location,
                                         ssh_pkey=self.ssh_pkey,
                                         ssh_password=self.ssh_password,
                                         ssh_username=self.ssh_username,
                                         remote_bind_address=(self.remote_bind_address, self.remote_bind_address_port))
        self.server.start()

    def addSchema(self, schemaDict):
        name = schemaDict["name"]
        schemaName = schemaDict["schemaName"]
        schemaClassName = schemaDict["class"]
        schemaBaseClass = schemaDict["base"]
        self.base = schemaBaseClass
        # self.loadBase()
        self.loadTables(name)

        if self.ssh_pkey:
            self.startSSH()
            self.port = self.server.local_bind_port

        if self.login:
            enginestring = '%s://%s:%s@%s:%s/%s' % (
            str(self.dialect), str(self.login), str(self.password), str(self.location), str(self.port), str(schemaName))

            self.engine[name] = create_engine(enginestring)

            schemaBaseClass.metadata.create_all(self.engine[name])

        else:
            databasepath = self.location
            enginestring = '%s:///%s' % (self.dialect, databasepath)

            file_exists = os.path.isfile(databasepath)
            # todo: create settings database from template

            if not file_exists:
                try:
                    os.makedirs(os.path.dirname(self.location), exist_ok=True)
                except:
                    pass  # path already created

            self.engine[name] = create_engine(enginestring)

            schemaBaseClass.metadata.create_all(self.engine[name])

        self.loadSession(name)

    def closeConnection(self):
        self.session.close()