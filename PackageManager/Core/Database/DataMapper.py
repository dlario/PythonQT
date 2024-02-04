from datetime import datetime
import pandas as pd
import numpy as np
import os
import sys
import xlwings as xw
from alive_progress import alive_bar
from sqlalchemy_filters import apply_filters
import json
import re

from PackageManager.Packages.ProgramBase.Database.dbMaster import MasterTable
from PackageManager.Packages.ProgramBase.Database.dbMaster import FieldTable
from PackageManager.Packages.ProgramBase.Database.dbMaster import DataBaseType
from PackageManager.Packages.ProgramBase.Database.dbMaster import DataType
from PackageManager.Packages.ProgramBase.Database.dbMaster import DataMap
#from PackageManager.Packages.ProgramBase.Database.dbMaster import DataMapKey
from PackageManager.Packages.ProgramBase.Database.dbMaster import SessionInformation
from PackageManager.Packages.ProgramBase.Database.dbMaster import ExcelTable

class DataMapper(object):
    def __init__(self, sqlRegister):

        self.sqlRegister = sqlRegister
        self.itemdict = {}
        self.fkdict = {}

        filepaths = {}
        filepaths["Person"] = r"C:/Users/d_lar/OneDrive/Enigma Design Solutions/Projects/EDS - Project List2.xlsm"

        self.datamaporder = []
        self.errorlog = []

        self.liveBar ='bubbles'
        self.liveSpinner = 'notes2'

        self.tableList = ["Work Order Items", "Invoice"]
        self.loadDataMapItems()

        self.dataConnection = {}
        excelfilepath = r"C:/Users/d_lar/OneDrive/Enigma Design Solutions/Projects/EDS - Project List.xlsm"
        self.loadExcelDataBase()
        self.loadSQLDataBase("MainServer", "MySQL")

        self.sourceDatabase = "ExcelProjectList"
        self.sourceDataConnection = os.path.basename(excelfilepath)

    def setDataMappingOrder(self, dataMappingorder):
        self.datamappingorder = dataMappingorder

    def loadSQLDataBase(self, SourceName, DatabaseType2):
        if SourceName not in self.dataConnection:
            self.dataConnection[SourceName] = {}
            itemlist = self.LoadSQLConnection()
            self.dataConnection[SourceName]["DataType"] = DatabaseType2
            self.dataConnection[SourceName]["ItemList"] = {}
            for item in self.tableList:
                self.dataConnection[SourceName]["ItemList"][item] = itemlist[item]
        else:
            print("Name Already Exists")
    def loadExcelDataBase(self):
        itemlist = self.loadExcelConnection()

        for itemname, itemdict in itemlist.items():
            excelfilepath = itemlist[itemname]["WorkBook"]
            SourceName = os.path.basename(excelfilepath)

            dataConnection = {}
            dataConnection["DatabaseType"] = "Excel"
            dataConnection["NameText"] = itemname
            dataConnection["Package"] = {}
            dataConnection["File"] = itemdict["WorkBook"]
            dataConnection["DataSourceFormat"] = itemdict["Format"]
            dataConnection["ClassName"] = {}
            dataConnection["TableName"] = itemdict["TableName"]
            dataConnection["DisplayColumn"] = {}
            dataConnection["Description"] = {}
            dataConnection["PrimaryKey"] = itemdict["PrimaryKey"]
            dataConnection["Tags"] = {}
            dataConnection["Active"] = True

            dataConnection["HeaderRow"] = itemdict["HeaderRow"]
            dataConnection["StartColumn"] = itemdict["StartColumn"]
            dataConnection["StartRow"] = itemdict["StartRow"]
            dataConnection["PrimaryColumn"] = itemdict["PrimaryColumn"]

        #Add Connection Datato SQL
            connectionrecord = (self.sqlRegister.sqlDict["Location1"].session.query(SessionInformation)
                     .filter(SessionInformation.SessionName == SourceName)
                     .filter(SessionInformation.DatabaseType == 4))
            if connectionrecord.count() == 0:
                self.sqlRegister.sqlDict["Location1"].session.begin_nested()
                connectionrecord = SessionInformation()
                connectionrecord.SessionName = SourceName
                connectionrecord.DataBaseType = 4 #Excel
                connectionrecord.Address = dataConnection["File"]
                connectionrecord.Login = ""
                connectionrecord.Password = ""
                self.sqlRegister.sqlDict["Location1"].session.add(connectionrecord)
                self.sqlRegister.sqlDict["Location1"].session.commit()

        #Add Table to MasterTable
            tableDict = {"TableName": itemdict["TableName"], "File": dataConnection["File"], "PrimaryKey": itemdict["PrimaryKey"]}
            tableDict["TableRecord_id"] = self.getcreateTableRecord(tableDict)

        # Field Items
            fieldItems = self.DataMapItems()
            fieldrecorddict = {}
            fieldrecorddict[dataConnection["TableName"]] = {}

            for fielditem, fielddict in fieldItems[itemname]["DataMap"].items():
                if "DataField" not in fielddict["Excel"]:
                    fielddict["Excel"]["DataField"] = None

                fieldrecorddict[dataConnection["TableName"]][fielditem] = {}
                fieldrecorddict[dataConnection["TableName"]][fielditem]["Table_id"] = tableDict["TableRecord_id"]
                fieldrecorddict[dataConnection["TableName"]][fielditem]["TableName"] = dataConnection["TableName"]
                fieldrecorddict[dataConnection["TableName"]][fielditem]["DataField"] = fielddict["Excel"]["DataField"]
                fieldrecorddict[dataConnection["TableName"]][fielditem]["DataColumn"] = fielddict["Excel"]["DataColumn"]
                fieldrecorddict[dataConnection["TableName"]][fielditem]["DataType"] = fielddict["Excel"]["DataType"]

                tableDict2 =tableDict.copy()
                if "FKSheet" in fielddict["Excel"]:
                    fieldrecorddict[dataConnection["TableName"]][fielditem]["FKSheet"] = fielddict["Excel"]["FKSheet"]
                if "FKField" in fielddict["Excel"]:
                    fieldrecorddict[dataConnection["TableName"]][fielditem]["FKField"] = fielddict["Excel"]["FKField"]
                fieldrecorddict[dataConnection["TableName"]][fielditem]["Active"] = True

                if "FKTable" in fielddict["Excel"]:
                    if dataConnection["TableName"] not in fieldrecorddict:
                        fieldrecorddict[dataConnection["TableName"]] = {}
                    tableDict2["TableName"] = fieldrecorddict[dataConnection["TableName"]][fielditem]["FKTable"] = fielddict["Excel"]["FKTable"]
                    tableDict2["Table_id"] = fieldrecorddict[dataConnection["TableName"]][fielditem]["FKTable_id"] = self.getcreateTableRecord(tableDict2)

                if "Key" in fielddict["Excel"]:
                    fieldrecorddict = self.loadKey(tableDict2, fielditem, fieldrecorddict, fielddict["Excel"]["Key"])

                if "City" in fielditem:
                    pass

                record_id = self.getcreateFieldRecord(tableDict, fielditem, fieldrecorddict)

    def loadKey(self, tableDict, keyitem, fieldrecorddict, keydict):
        #The key
        tabledict2 = tableDict.copy()
        if "FKTable" in keydict:
            if keydict["FKTable"] not in fieldrecorddict:
                fieldrecorddict[keydict["FKTable"]] = {}
            tabledict2["TableName"] = fieldrecorddict[keydict["FKTable"]][keyitem]["FKTable"] = keydict["FKTable"]
            tabledict2["Table_id"] = fieldrecorddict[keydict["FKTable"]][keyitem]["FKTable_id"] = self.getcreateTableRecord(tabledict2)
        if "FKSheet" in keydict:
            tabledict2["FKSheet"] = keydict["FKSheet"]
        if "FKField" in keydict:
            tabledict2["FKField"] = keydict["FKField"]
        if "FKFile" in keydict:
            tabledict2["FKFile"] = keydict["FKFile"]

        if "Key" in keydict:
            if keydict["Key"] is not None:
                fieldrecorddict = self.loadKey(tableDict, keyitem, fieldrecorddict, keydict["Key"])

        for keyitem2, fielddict in keydict.items():
            if "Company Name" in keyitem2:
                pass
            if "First Name" in keyitem2:
                pass
            if "Legal Name" in keyitem2:
                pass

            field = keyitem2
            tabledict3 = tabledict2.copy()
            if tabledict2["TableName"] not in fieldrecorddict:
                fieldrecorddict[tabledict2["TableName"]] = {}

            if "FKTable" in fielddict:
                if keydict["FKTable"] not in fieldrecorddict:
                    fieldrecorddict[keydict["FKTable"]] = {}
                    tabledict3["TableName"] = keydict["FKTable"]
                    tabledict3["Table_id"] = self.getcreateTableRecord(tabledict3)

            if "FKField" in fielddict:
                field = fielddict["FKField"]

            if "FKTable" in fielddict:
                if keydict["FKTable"] not in fieldrecorddict:
                    fieldrecorddict[keydict["FKTable"]] = {}
                if field not in fieldrecorddict[tabledict2["TableName"]]:
                    fieldrecorddict[tabledict2["TableName"]][field] = {}

                tabledict3["TableName"] = fieldrecorddict[tabledict2["TableName"]][field]["FKTable"] = fielddict["FKTable"]
                tabledict3["Table_id"] = fieldrecorddict[tabledict2["TableName"]][field]["FKTable_id"] = self.getcreateTableRecord(tabledict3)

            if "FKSheet" in fielddict:
                fieldrecorddict[tabledict2["TableName"]][field]["FKSheet"] = fielddict["FKSheet"]

            if "FKField" in fielddict:
                field = fielddict["FKField"]
            if field not in fieldrecorddict[tabledict2["TableName"]]:
                fieldrecorddict[tabledict2["TableName"]][field] = {}
            fieldrecorddict[tabledict2["TableName"]][field]["FKField"] = field


            if "DataType" in fielddict:
                fieldrecorddict[tabledict2["TableName"]][field]["DataType"] = fielddict["DataType"]
            else:
                pass

            if "City" == field:
                pass

            fieldrecorddict[tabledict2["TableName"]][field]["Active"] = True

            record_id = self.getcreateFieldRecord(tabledict2, field, fieldrecorddict)
        return fieldrecorddict

    def getcreateTableRecord(self, tableDict):
        #Add Table to MasterTable
            tablerecord = (self.sqlRegister.sqlDict["Location1"].session.query(MasterTable)
                           .filter(MasterTable.DataSourceFormat == "Excel")
                           .filter(MasterTable.NameText == tableDict["TableName"])
                           .filter(MasterTable.TableName == tableDict["TableName"]))
            if tablerecord.count() == 0:
                self.sqlRegister.sqlDict["Location1"].session.begin_nested()
                tablerecord = MasterTable()
                tablerecord.TableType_id = 1
                tablerecord.NameText = tableDict["TableName"]
                tablerecord.Package = "Excel"
                FileName = os.path.basename(tableDict["File"])
                tablerecord.File = FileName
                tablerecord.DataSourceFormat = "Excel"
                tablerecord.ClassName = tableDict["TableName"]
                tablerecord.TableName = tableDict["TableName"]
                tablerecord.PrimaryKey = tableDict["PrimaryKey"]
                self.sqlRegister.sqlDict["Location1"].session.add(tablerecord)
                self.sqlRegister.sqlDict["Location1"].session.commit()
            else:
                tablerecord = tablerecord.first()

            return tablerecord.id
    def getcreateFieldRecord(self, tableDict, fielditem, fieldrecorddict):
        table_id = tableDict["TableRecord_id"]
        tableName = tableDict["TableName"]

        if fieldrecorddict is not None:
            fieldrecord = (self.sqlRegister.sqlDict["Location1"].session.query(FieldTable)
                           .filter(FieldTable.Table_id == table_id)
                           .filter(FieldTable.NameText == fielditem))

            if "DataType" not in fieldrecorddict[tableName][fielditem]:
                pass

            datatype_id = self.sqlRegister.getRecordID("Location1", DataType,
                                                       "NameText", fieldrecorddict[tableName][fielditem]["DataType"])

            if fieldrecord.count() == 0:
                self.sqlRegister.sqlDict["Location1"].session.begin_nested()
                fieldrecord = FieldTable()
                #"DataField": "COMPONENT", "DataType": "int", "DataColumn": None, "Active": True
                #fieldrecord.TableType_id = tableRecord.id
                fieldrecord.Table_id = table_id
                fieldrecord.NameText = fielditem
                fieldrecord.Package = "ProgramBase"
                fieldrecord.DataType_id = datatype_id
                fieldrecord.DataType_Value = fieldrecorddict[tableName][fielditem]["DataType"]
                fieldrecord.PrimaryKey = None
                fieldrecord.NotNull = None
                fieldrecord.Unique = None
                fieldrecord.Binary = None
                fieldrecord.ZeroFill = None
                fieldrecord.GeneratedColumn = None
                fieldrecord.DefaultExpression = None
                fieldrecord.Description = None
                if "FKTable_id" in fieldrecorddict[tableName][fielditem]:
                    fieldrecord.ForeignKey = fieldrecorddict[tableName][fielditem]["FKTable_id"]
                fieldrecord.Tags = None
                fieldrecord.Active = True
                self.sqlRegister.sqlDict["Location1"].session.add(fieldrecord)
                self.sqlRegister.sqlDict["Location1"].session.commit()
            else:
                fieldrecord = fieldrecord.first()
            return fieldrecord.id
    def loadDataItems(self, SourceName, dataMapDict=None, itemName=None, parent_id=None, ):
        a = self.dataConnection[SourceName]["ItemList"]

        for item, itemdict in dataMapDict.items():
            recorddict = {}
            for item2, itemdict2 in itemdict["DataMap"].items():
                if "WorkBook" in itemdict2:
                    recorddict["WorkBook"] = itemdict2["WorkBook"]
                else:
                    recorddict["WorkBook"] = self.dataConnection[SourceName]["ItemList"][item]["WorkBook"]
                    
                if "Sheet" in itemdict2:
                    recorddict["Sheet"] = itemdict2["Sheet"]
                else:
                    recorddict["Sheet"] = self.dataConnection[SourceName]["ItemList"][item]["Sheet"]

                if "Table" in itemdict2:
                    recorddict["Table"] = itemdict2["Table"]
                else:
                    recorddict["Table"] = self.dataConnection[SourceName]["ItemList"][item]["TableName"]

                if "PrimaryKey" in itemdict2:
                    recorddict["PrimaryKey"] = itemdict2["PrimaryKey"]
                else:
                    recorddict["PrimaryKey"] = self.dataConnection[SourceName]["ItemList"][item]["PrimaryKey"]

                if "HeaderRow" in itemdict2:
                    recorddict["HeaderRow"] = itemdict2["HeaderRow"]
                else:
                    recorddict["HeaderRow"] = self.dataConnection[SourceName]["ItemList"][item]["HeaderRow"]

                if "StartRow" in itemdict2:
                    recorddict["StartRow"] = itemdict2["StartRow"]
                else:
                    recorddict["StartRow"] = self.dataConnection[SourceName]["ItemList"][item]["StartRow"]

                if "StartColumn" in itemdict2:
                    recorddict["StartColumn"] = itemdict2["StartColumn"]
                else:
                    recorddict["StartColumn"] = self.dataConnection[SourceName]["ItemList"][item]["StartColumn"]

                if "DataField" in itemdict2["Excel"] or "Value" in itemdict2["Excel"]:
                    query = (self.sqlRegister.sqlDict["Location1"].session.query(DataMap)
                             .filter(DataMap.Name == item)
                             .filter(DataMap.Sheet == recorddict["Sheet"])
                             .filter(DataMap.Table == recorddict["TableName"]))

                    if query.count() == 0:
                        self.sqlRegister.sqlDict["Location1"].session.begin_nested()
                        newrecord = DataMap()
                        newrecord.DataBaseType = 3 #Excel
                        if parent_id is not None:
                            newrecord.Parent_id = parent_id
                            newrecord.Name = itemName
                        else:
                            newrecord.Name = item

                        if "Name" in itemdict2: newrecord.Name = itemdict2["Name"]
                        if "DataField" in itemdict2: newrecord.DataField = itemdict2["DataField"]
                        if "DataColumn" in itemdict2: newrecord.DataColumn = itemdict2["DataColumn"]
                        if "DataType" in itemdict2: newrecord.DataType = itemdict2["DataType"]
                        if "FKSheet" in itemdict2: newrecord.FKSheet = itemdict2["FKSheet"]
                        if "FKTable" in itemdict2: newrecord.FKTable = itemdict2["FKTable"]
                        if "FKField" in itemdict2: newrecord.FKField = itemdict2["FKField"]
                        if "Active" in itemdict2: newrecord.WorkBook = itemdict2["Active"]
                        if "Key" in itemdict2:
                            for keyname, keydict in itemdict2["Key"].items():
                                self.loadDataItems(keyname, newrecord.id, keydict)
    def loadDataMapItems(self):
        self.dataMapItems = self.DataMapItems()

    def initDataMapItem(self, Index, fieldName):
        lastmodified = datetime.now()
        if fieldName not in self.datadict:
            self.datadict[Index][fieldName] = {}
        for Location, value in self.dataConnection.items():
            if Location not in self.datadict:
                self.datadict[Index][fieldName][Location] = {"id": None, "Value": None, "DataType": None, "Unique": {}, "tagList": [], "LastModified": lastmodified}

    def syncDataItem(self, DataMapItem):
        itemdict = self.dataMapItems[DataMapItem]
        if "AdditionalEntries" in itemdict:
            additionalData = itemdict["AdditionalEntries"]
        else:
            additionalData = {"None": []}

        for Subset, SubsetDict in additionalData.items():
            self.datadict = {}
            self.rowStatus = {}
            print("SubSet: ", Subset)
            for Destination, value2 in self.dataConnection.items():
                if self.sourceDatabase == Destination:
                    if value2["DataType"] == "Excel":
                        print("Loading Excel File: ", DataMapItem)
                        print("SubSet: ", Subset)
                        self.readExcel(self.sourceDatabase, DataMapItem, SubsetDict)
                else:
                    print("Writting File: ", DataMapItem)
                    print("SubSet: ", Subset)
                    #self.writeSQL(self.sourceDatabase, Destination, DataMapItem, SubsetDict)

    def readExcel(self, Source, DataMapItem, SubsetDict=None):
        # filepaths is a dictionary that can pull from mulitples excel files at the same time incase
        # the table is linked to multiple excel files.
        # self.dataMap is the dictionary that contains the data map information.
        # self. datamappingorder is the list of entries if it is none then it is all the self.dataMap entries
        # if self. datamappingorder is not none then it is a list of the entries to be pulled.


        pandastable = {}
        itemdict = self.dataMapItem[DataMapItem]
        # print("point1")
        # Read Source
        package = itemdict["Package"]

        sourceDataFormat = self.dataConnection[Source]["ItemList"][DataMapItem]["Format"]
        sourceTable = self.dataConnection[Source]["ItemList"][DataMapItem]["TableName"]

        sourceTable_id = self.sqlRegister.getTableID({"Package": package, "TableName": sourceTable, "DataSourceFormat": sourceDataFormat})

        for updateitem in SubsetDict:
            if updateitem["DataSource"] == sourceDataFormat:
                if "KeyField" in updateitem:
                    itemdict["DataMap"][updateitem["DataField"]][updateitem["DataSource"]]["Key"][updateitem["KeyField"]][updateitem["ItemName"]] = updateitem["Value"]
                else:
                    itemdict["DataMap"][updateitem["DataField"]][updateitem["DataSource"]][updateitem["ItemName"]] = updateitem["ItemValue"]
                if "Active" in updateitem:
                    itemdict["DataMap"][updateitem["DataField"]][updateitem["DataSource"]]["Active"] = updateitem["Active"]
                else:
                    itemdict["DataMap"][updateitem["DataField"]][updateitem["DataSource"]]["Active"] = True

        if "UniqueFields" in itemdict:
            uniqueFields = itemdict["UniqueFields"]
        sheet = self.dataConnection[Source]["ItemList"][DataMapItem]["Sheet"]

        sht = self.dataConnection[Source]["WorkBooks"][self.sourceDataConnection].sheets[sheet]  # select the first sheet
        table = sht.api.ListObjects(sourceTable)  # select the first table in the sheet
        table_range = table.Range
        rowcount = table_range.Rows.Count - 1
        df11 = sht['A1'].options(pd.Series, expand='table', header=True).value
        df11 = df11.where(pd.notna(df11), None)

        with (alive_bar(int(rowcount), bar=self.liveBar, spinner=self.liveSpinner, force_tty=True) as bar):
            for index, record in df11.iterrows():
                if "LAST MODIFIED" in itemdict["DataMap"]:
                    fieldname = itemdict["DataMap"]["LAST MODIFIED"][sourceDataFormat]["DataField"]
                    lastmodified = record[fieldname]
                else:
                    lastmodified = None
                self.datadict[int(index)] = {}
                self.rowStatus[int(index)] = {}
                if Source not in self.rowStatus[int(index)]:
                    self.rowStatus[int(index)][Source] = {}

                for fieldName, fieldProperties in itemdict["DataMap"].items():
                    self.initDataMapItem(int(index), fieldName)

                    if sourceDataFormat in fieldProperties:
                        if fieldProperties[sourceDataFormat]["Active"]:  # Some properties are sometimes calculated and dont exist.
                            if "DataType" in fieldProperties[sourceDataFormat]:
                                self.datadict[int(index)][fieldName][Source]["DataType"] = fieldProperties[sourceDataFormat]["DataType"]

                            if "book" in fieldProperties[sourceDataFormat]:
                                workbookName = fieldProperties[sourceDataFormat]["Name"]
                                fkbook = fieldProperties[sourceDataFormat]["Path"]
                                if workbookName not in self.dataConnection[Source]["WorkBooks"]:
                                    self.dataConnection[Source]["WorkBooks"][workbookName] = xw.Book(fkbook)

                            # Can handle one field having multiple values, might be able to do multiple fields but no depth.
                            if fieldProperties[sourceDataFormat]["DataType"] is not None:
                                if "List" in fieldProperties[sourceDataFormat]["DataType"]:
                                    listitemfield = self.dataConnection[Source]["ItemList"][DataMapItem]["ListItems"]
                                    listitemcsvvalues = record[listitemfield]
                                    listitemlist = listitemcsvvalues.split(",")
                                else:
                                    listitemfield = None
                                    listitemlist = [None]

                            # If the field is a csv field
                            for listitemfieldvalue in listitemlist:
                                # print("point4")
                                if "Value" in fieldProperties[sourceDataFormat]:
                                    sourcefieldvalue = fieldProperties[sourceDataFormat]["Value"]
                                    if "DataField" in fieldProperties[sourceDataFormat]:
                                        sourcefieldname = fieldProperties[sourceDataFormat]["DataField"]

                                if "DataField" in fieldProperties[sourceDataFormat] and "Value" not in fieldProperties[sourceDataFormat]:
                                    sourcefieldname = fieldProperties[sourceDataFormat]["DataField"]
                                    if sourcefieldname == listitemfield:
                                        sourcefieldvalue = listitemfieldvalue
                                    else:
                                        sourcefieldvalue = record[sourcefieldname]
                                        if "Format" in fieldProperties[sourceDataFormat]:
                                            if fieldProperties[sourceDataFormat]["DataType"] == "date":
                                                try:
                                                    sourcefieldvalue = datetime.datetime.strptime(sourcefieldvalue, fieldProperties[sourceDataFormat]["Format"]).date()
                                                except:
                                                    pass
                                self.datadict[int(index)][fieldName][Source]["Value"] = sourcefieldvalue

                                # If there is a Foreign key then there will be an id number to lookup
                                recordFound = False
                                filtered_df = None
                                if "FKField" in fieldProperties[sourceDataFormat]:
                                    if fieldProperties[sourceDataFormat]["FKSheet"] not in pandastable:
                                        fksht1 = self.dataConnection[Source]["WorkBooks"][workbookName].sheets[fieldProperties[sourceDataFormat]["FKSheet"]]  # select the first sheet
                                        df2 = fksht1['A1'].options(pd.Series, expand='table', header=True).value
                                        pandastable[fieldProperties[sourceDataFormat]["FKSheet"]] = df2
                                    else:
                                        df2 = pandastable[fieldProperties[sourceDataFormat]["FKSheet"]]
                                    df2 = df2.where(pd.notna(df2), None)
                                    sourceFKTable_id = self.sqlRegister.getTableID({"Package": package, "TableName": fieldProperties[sourceDataFormat]["FKTable"], "DataSourceFormat": sourceDataFormat})

                                    fieldvalue = fieldProperties[sourceDataFormat]["FKField"]
                                    filtered_df = df2.loc[df2[fieldvalue] == sourcefieldvalue]
                                    if not filtered_df.empty:
                                        self.datadict[int(index)][fieldName][Source]["id"] = int(filtered_df.iloc[0].name)
                                    else:
                                        self.datadict[int(index)][fieldName][Source]["id"] = None

                                if recordFound:
                                    PrimarySourceKey = -1
                                    if "PrimaryKey" in self.dataConnection[Source]["ItemList"][DataMapItem]:
                                        fkid = self.dataConnection[Source]["ItemList"][DataMapItem]["PrimaryKey"]
                                        if fkid in df2.columns:
                                            PrimarySourceKey = filtered_df.iloc[0][fkid]
                                        else:
                                            PrimarySourceKey = int(index)

                                    elif "PrimaryColumn" in self.dataConnection[Source]["ItemList"][DataMapItem]:
                                        primarycolumn = self.dataConnection[Source]["ItemList"][DataMapItem]["PrimaryColumn"]
                                        # PrimarySourceKey = fkrow2[primarycolumn]
                                        PrimarySourceKey = int(filtered_df.iloc[0].name)

                                    if PrimarySourceKey != -1:
                                        self.datadict[int(index)][fieldName][Source]["tagList"] = [f'({sourceTable_id}-{PrimarySourceKey})']

                                keyValueDict = {}
                                if "Key" in fieldProperties[sourceDataFormat]:
                                    for keyname, keydict in fieldProperties[sourceDataFormat]["Key"].items():
                                        keyValueDict[keyname] = {"DataField": None, "Value": None, "TableID": None, "RecordID": None}
                                        # print("point5")
                                        field = None
                                        if sourceDataFormat == "Excel":
                                            recordid = -1
                                            tableid = -1

                                            if "Value" in keydict:
                                                keyfieldvalue = keydict["Value"]  # field = keydict["DataField"]

                                            if "FKField" in keydict and not filtered_df.empty:
                                                keyfieldvalue = filtered_df.iloc[0][keydict["FKField"]]
                                                field = keydict["FKField"]
                                                recordid = int(filtered_df.iloc[0].name)
                                                if recordid != "":
                                                    try:
                                                        recordid = int(recordid)
                                                    except:
                                                        pass
                                                else:
                                                    recordid = -1
                                                tableid = sourceFKTable_id

                                            if "DataField" in keydict:
                                                keyfieldvalue = record[keydict["DataField"]]
                                                field = keydict["DataField"]

                                            keyValueDict[keyname] = {"DataField": field, "Value": keyfieldvalue, "TableID": None, "RecordID": None}
                                            if isinstance(self.datadict[int(index)][fieldName][Source]["Value"], int):
                                                if self.datadict[int(index)][fieldName][Source]["Value"] is not None:
                                                    if len(self.datadict[int(index)][fieldName][Source]["Value"]):
                                                        sourcefieldvalue = self.datadict[int(index)][fieldName][Source]["Value"]
                                                        unqDict = {}
                                                        ufieldName = fieldName  # sourcefieldname
                                                        ufieldvalue = sourcefieldvalue
                                                        unqDict[ufieldName] = {"DataField": ufieldName, "Value": ufieldvalue, "TableID": tableid, "RecordID": recordid}
                                                        self.datadict[int(index)][fieldName][Source]["Unique"] = unqDict
                                                        keyValueDict[keyname] = {"DataField": field, "Value": keyfieldvalue, "TableID": tableid, "RecordID": recordid}

                                            if "FKTable" in keydict:
                                                # fksht = workbooks[workbookName].sheets[keydict["Sheet"]]  # select the first sheet
                                                fktable = fksht1.api.ListObjects(keydict["FKTable"])
                                                fkfield = keydict["FKField"]

                                                if keydict["FKTable"] not in pandastable:
                                                    fksht1 = self.dataConnection[Source]["WorkBooks"][workbookName].sheets[keydict["FKTable"]]  # select the first sheet
                                                    df3 = fktable['A1'].options(pd.Series, expand='table', header=True).value
                                                    pandastable[keydict["FKTable"]] = df3
                                                else:
                                                    df3 = pandastable[keydict["FKTable"]]
                                                df3 = df3.where(pd.notna(df3), None)

                                                sourceFKTable_id = self.sqlRegister.getTableID(
                                                    {"Package": package, "TableName": fieldProperties[sourceDataFormat]["FKTable"], "DataSourceFormat": sourceDataFormat})

                                                filtered_df3 = df3.loc[df3[fieldvalue] == sourcefieldvalue]
                                                if not filtered_df3.empty:
                                                    if self.datadict[int(index)][fieldName][Source]["Key"][keyname]["Value"] == filtered_df.iloc[0][fkfield]:
                                                        # sourcefkid = record["ID").Index).Text
                                                        table_id = self.sqlRegister.getTableID({"Package": package, "TableName": fktable, "DataSourceFormat": "Excel"})
                                                        field_id = filtered_df.iloc[0].name
                                                        self.datadict[int(index)][fieldName][Source]["tagList"].append([f'({table_id}-{field_id})'])
                                                        keyfieldvalue = filtered_df.iloc[0][ufieldName]

                                self.datadict[int(index)][fieldName][Source]["Unique"] = keyValueDict
                self.rowStatus[int(index)][Source]["Status"] = self.recordVerification(itemdict, Source, index)
                bar()


    def readSQL(self, filepath, sheetname, table):
        pass

    def recordVerification(self, itemdict, Source, Index):
        # Check for Duplicates in unique fields
        uniqueDict = {}
        nonnullrecord = True
        sourcefieldvalue = None

        if "UniqueFields" in itemdict:
            uniqueFieldGroups = itemdict["UniqueFields"]
        else:
            uniqueFieldGroups = [[]]

        for uniqueFields in uniqueFieldGroups:
            # print("point7")
            for fieldcheck in uniqueFields:
                uniqueDict[fieldcheck] = {"Source": None, "Destination": None}
                if "Value" in self.datadict[Index][fieldcheck][Source]:
                    sourcefieldvalue = self.datadict[Index][fieldcheck][Source]["Value"]  # sourcefieldname = itemdict["DataMap"][fieldcheck][Source]["FKField"]

                    if isinstance(sourcefieldvalue, str):
                        if sourcefieldvalue is None:
                            nonnullrecord = False
                        elif len(sourcefieldvalue) == 0:
                            nonnullrecord = False

                uniqueDict[fieldcheck]["Source"] = sourcefieldvalue
        return nonnullrecord

    def writeExcel(self, filepath, sheetname, table):
        pass

    def writeSQL(self, Source, Destination, DataMapItem, additionalitem=None):
        # Determines values for all foreign keys.  This is done before the record is created.
        # Checks to see if record is duplicate of existing.
        # Future. Does Record compares to see if the record is different from the existing records.
        itemdict = self.dataMapItems[DataMapItem]
        destinationTable = self.dataConnection[Destination]["ItemList"][DataMapItem]["TableName"]
        destinationDataFormat = self.dataConnection[Destination]["ItemList"][DataMapItem]["Format"]
        package = itemdict["Package"]

        if "UniqueFields" in itemdict:
            uniqueFieldGroups = itemdict["UniqueFields"]
        else:
            uniqueFieldGroups = [[]]

        destinationTable_id = self.sqlRegister.getTableID({"Package": package, "TableName": destinationTable, "DataSourceFormat": destinationDataFormat})

        if additionalitem:
            additionalData = itemdict["AdditionalEntries"]
        else:
            additionalData = {"None": []}

        for name, additionalitem in additionalData.items():
            for updateitem in additionalitem:
                if updateitem["DataSource"] == destinationDataFormat:
                    if "KeyField" in updateitem:
                        itemdict["DataMap"][updateitem["DataField"]][destinationDataFormat]["Key"][updateitem["KeyField"]][updateitem["ItemName"]] = updateitem["ItemValue"]
                    else:
                        itemdict["DataMap"][updateitem["DataField"]][destinationDataFormat][updateitem["ItemName"]] = updateitem["ItemValue"]
                    if "Active" in updateitem:
                        itemdict["DataMap"][updateitem["DataField"]][destinationDataFormat]["Active"] = updateitem["Active"]
                    else:
                        itemdict["DataMap"][updateitem["DataField"]][destinationDataFormat]["Active"] = True


            with (alive_bar(int(len(self.datadict)), bar=self.liveBar, spinner=self.liveSpinner, force_tty=True) as bar):
                for index, record in self.datadict.items():
                    if self.rowStatus[index][self.sourceDatabase]["Status"]:
                        for fieldName, fieldProperties in itemdict["DataMap"].items():

                            # print("point8")
                            if fieldName in ["DATE", "CLIENT CONTACT", "PROJECT CONTACT", "CONSIGNEE", "OWNER"]:
                                pass
                            if destinationDataFormat in fieldProperties:
                                if fieldProperties[destinationDataFormat]["Active"]:
                                    field = fieldProperties[destinationDataFormat]["DataField"]
                                    if fieldName in record:
                                        if "Value" in record[fieldName][Source]:
                                            fieldvalue = sourcefieldvalue = record[fieldName][Source]["Value"]
                                        else:
                                            fieldvalue = sourcefieldvalue = None
                                    else:
                                        fieldvalue = sourcefieldvalue = None

                                    record[fieldName][Destination]["DataField"] = field
                                    record[fieldName][Destination]["Value"] = fieldvalue
                                    record[fieldName][Destination]["DataType"] = fieldProperties[destinationDataFormat]["DataType"]

                                    if Source in fieldProperties:
                                        if "Format" in fieldProperties[destinationDataFormat]:
                                            record[fieldName][Source]["Format"] = fieldProperties[destinationDataFormat]["Format"]

                                    if fieldvalue == "":
                                        fieldvalue = None

                                    if "FKTable" in fieldProperties[destinationDataFormat]:
                                        FKTable1 = fieldProperties[destinationDataFormat]["FKTable"]
                                    if "FKField" in fieldProperties[destinationDataFormat]:
                                        FKField1 = fieldProperties[destinationDataFormat]["FKField"]
                                    if "Package" in fieldProperties[destinationDataFormat]:
                                        FKPackage1 = fieldProperties[destinationDataFormat]["Package"]

                                    # table_id = self.sqlRegister.getTableID({"Package": package, "TableName": FKTable1, "DataSourceFormat": "SQL"})

                                    # check to see if table exists if not create first row as empty record
                                    if package not in self.fkdict:
                                        self.fkdict[package] = {}
                                    if destinationTable not in self.fkdict[package]:
                                        self.fkdict[package][destinationTable] = self.sqlRegister.sqlDict["Location1"].session.query(self.sqlRegister.packageTableDict[package][destinationTable])
                                    testquery = self.fkdict[package][destinationTable].first()

                                    if testquery is None:
                                        self.sqlRegister.sqlDict["Location1"].session.begin_nested()
                                        newrecord = self.sqlRegister.packageTableDict[package][destinationTable]()
                                        self.sqlRegister.sqlDict["Location1"].session.add(newrecord)
                                        self.sqlRegister.sqlDict["Location1"].session.commit()

                                    unqDict = {}
                                    keyValueDict2 = {}
                                    # If there are keys then find them first
                                    if "Key" in fieldProperties[destinationDataFormat]:
                                        for keyname, fkkeydict in fieldProperties[destinationDataFormat]["Key"].items():
                                            if "Key" in fkkeydict:
                                                for keyname2, fkkeydict2 in fkkeydict["Key"].items():
                                                    # print("point9")
                                                    # Non-Simple Foreign Keys or foreign relationships without a key
                                                    if "FKField" in fkkeydict2:
                                                        try:
                                                            FKFieldFK2 = fkkeydict2["FKField"]
                                                            FKTable2 = fkkeydict2["FKTable"]
                                                            FKTableField2 = fkkeydict2["FKField"]
                                                            FKPackage2 = fkkeydict2["Package"]
                                                            if "Value" in fkkeydict2:
                                                                fkvalue2 = fkkeydict2["Value"]
                                                            else:
                                                                if "Value" in fieldProperties[destinationDataFormat]["Key"][keyname2]:
                                                                    fkvalue2 = fieldProperties[destinationDataFormat]["Key"][keyname2]["Value"]
                                                                else:
                                                                    fkvalue2 = record[fieldName][Source]["Value"]

                                                            if "Unique" in record[fieldName][Source]:
                                                                if keyname2 in record[fieldName][Source]["Unique"]:
                                                                    fkvalue2 = record[fieldName][Source]["Unique"][keyname2]["Value"]

                                                            table_id2 = self.sqlRegister.getTableID({"Package": package, "TableName": FKTable2, "DataSourceFormat": "SQL"})
                                                            # Test if the FK value is in the system
                                                            if FKPackage2 not in self.fkdict:
                                                                self.fkdict[FKPackage2] = {}
                                                            if FKTable2 not in self.fkdict[FKPackage2]:
                                                                self.fkdict[FKPackage2][FKTable2] = self.sqlRegister.sqlDict["Location1"].session.query(
                                                                    self.sqlRegister.packageTableDict[FKPackage2][FKTable2])

                                                            fkquery2 = self.fkdict[FKPackage2][FKTable2]
                                                            fkquerycount1 = fkquery2.count()
                                                            fkfilter2 = [{'field': FKFieldFK2, 'op': '==', 'value': fkvalue2}]
                                                            fkquery2 = apply_filters(fkquery2, fkfilter2)
                                                            fkquerycount2 = fkquery2.count()

                                                            if fkquerycount1 == 0:
                                                                # Create Blank Entry
                                                                self.sqlRegister.sqlDict["Location1"].session.begin_nested()
                                                                newfkrecord = self.sqlRegister.packageTableDict[FKPackage2][FKTable2]()
                                                                self.sqlRegister.sqlDict["Location1"].session.add(newfkrecord)
                                                                self.sqlRegister.sqlDict["Location1"].session.commit()

                                                            if fkquerycount2 == 0:
                                                                if fkvalue2 is not None and len(fkvalue2) != 0 and fkvalue2 != "":
                                                                    # Create New Record
                                                                    self.sqlRegister.sqlDict["Location1"].session.begin_nested()
                                                                    newfkrecord = self.sqlRegister.packageTableDict[FKPackage2][FKTable2]()
                                                                    setattr(newfkrecord, fkkeydict2["FKField"], fkvalue2)
                                                                    self.sqlRegister.sqlDict["Location1"].session.add(newfkrecord)
                                                                    self.sqlRegister.sqlDict["Location1"].session.commit()
                                                                    recordid = newfkrecord.id
                                                                else:
                                                                    recordid = None
                                                            else:
                                                                recordid = fkquery2.first().id

                                                            keyValueDict2[keyname2] = {"DataField": fkkeydict2["DataField"], "FKField": FKFieldFK2, "Value": fkvalue2, "TableID": table_id2, "RecordID": recordid}
                                                            if "KeyType" in fkkeydict2:
                                                                if fkkeydict2["KeyType"] != "Reference":
                                                                    unqDict[keyname2] = {"DataField": fkkeydict2["DataField"], "FKField": FKFieldFK2, "Value": recordid, "TableID": table_id2, "RecordID": recordid}
                                                            else:
                                                                unqDict[keyname2] = {"DataField": fkkeydict2["DataField"], "FKField": FKFieldFK2, "Value": recordid, "TableID": table_id2, "RecordID": recordid}
                                                        except:
                                                            pass

                                                    else:
                                                        tableid = -1
                                                        try:
                                                            a = record[fieldName][Source]["Unique"][keyname]["Value"]
                                                        except:
                                                            pass

                                                        keyValueDict2[keyname2] = {"DataField": fkkeydict2["DataField"], "FKField": FKFieldFK2, "Value": fkvalue2, "TableID": table_id2, "RecordID": recordid}
                                                        if "KeyType" in fkkeydict2:
                                                            if fkkeydict2["KeyType"] != "Reference":
                                                                unqDict[keyname2] = {"DataField": fkkeydict2["DataField"], "FKField": FKFieldFK2, "Value": recordid, "TableID": table_id2, "RecordID": recordid}
                                                        else:
                                                            unqDict[keyname2] = {"DataField": fkkeydict2["DataField"], "FKField": FKFieldFK2, "Value": recordid, "TableID": table_id2, "RecordID": recordid}

                                            # print("point9")
                                            # Non-Simple Foreign Keys or foreign relationships without a key
                                            if "FKField" in fkkeydict:
                                                try:
                                                    FKFieldFK2 = fkkeydict["FKField"]
                                                    FKTable2 = fkkeydict["FKTable"]
                                                    FKTableField2 = fkkeydict["FKField"]
                                                    FKPackage2 = fkkeydict["Package"]
                                                    fkvalue = record[fieldName][Source]["Value"]
                                                    if "Unique" in record[fieldName][Source]:
                                                        if keyname in record[fieldName][Source]["Unique"]:
                                                            fkvalue = record[fieldName][Source]["Unique"][keyname]["Value"]

                                                    table_id = self.sqlRegister.getTableID({"Package": package, "TableName": FKTable2, "DataSourceFormat": "SQL"})
                                                    # Test if the FK value is in the system
                                                    if FKPackage2 not in self.fkdict:
                                                        self.fkdict[FKPackage2] = {}
                                                    if FKTable2 not in self.fkdict[FKPackage2]:
                                                        self.fkdict[FKPackage2][FKTable2] = self.sqlRegister.sqlDict["Location1"].session.query(self.sqlRegister.packageTableDict[FKPackage2][FKTable2])

                                                    fkquery2 = self.fkdict[FKPackage2][FKTable2]
                                                    fkquerycount1 = fkquery2.count()
                                                    fkfilter2 = [{'field': FKFieldFK2, 'op': '==', 'value': fkvalue}]
                                                    fkquery2 = apply_filters(fkquery2, fkfilter2)
                                                    fkquerycount2 = fkquery2.count()

                                                    if fkquerycount1 == 0:
                                                        # Create Blank Entry
                                                        self.sqlRegister.sqlDict["Location1"].session.begin_nested()
                                                        newfkrecord = self.sqlRegister.packageTableDict[FKPackage2][FKTable2]()
                                                        self.sqlRegister.sqlDict["Location1"].session.add(newfkrecord)
                                                        self.sqlRegister.sqlDict["Location1"].session.commit()

                                                    if fkquerycount2 == 0:
                                                        if fkvalue is not None and len(fkvalue) != 0 and fkvalue != "":
                                                            # Create New Record
                                                            self.sqlRegister.sqlDict["Location1"].session.begin_nested()
                                                            newfkrecord = self.sqlRegister.packageTableDict[FKPackage2][FKTable2]()
                                                            setattr(newfkrecord, fkkeydict["FKField"], fkvalue)
                                                            for keyname, keydict in keyValueDict2.items():
                                                                if keydict["Value"] is not None and keydict["Value"] != "":
                                                                    value = keydict["Value"]
                                                                    if "RecordID" in keydict:
                                                                        if keydict["RecordID"] is not None:
                                                                            value = keydict["RecordID"]

                                                                    setattr(newfkrecord, keydict["DataField"], value)
                                                            self.sqlRegister.sqlDict["Location1"].session.add(newfkrecord)
                                                            self.sqlRegister.sqlDict["Location1"].session.commit()
                                                            recordid = newfkrecord.id
                                                        else:
                                                            recordid = None
                                                    else:
                                                        recordid = fkquery2.first().id

                                                    tableid = -1
                                                    keyValueDict2[keyname] = {"DataField": fkkeydict["DataField"], "FKField": FKFieldFK2, "Value": fkvalue, "TableID": tableid, "RecordID": recordid}

                                                    if "KeyType" in fkkeydict:
                                                        if fkkeydict["KeyType"] != "Reference":
                                                            unqDict[keyname] = {"DataField": field, "FKField": FKFieldFK2, "Value": recordid, "TableID": tableid, "RecordID": recordid}
                                                    else:
                                                        unqDict[keyname] = {"DataField": field, "FKField": FKFieldFK2, "Value": recordid, "TableID": tableid, "RecordID": recordid}
                                                except:
                                                    pass
                                            else:
                                                tableid = -1
                                                listDict = {}
                                                Value = record[fieldName][Source]["Unique"][keyname]["Value"]
                                                if "list" in fkkeydict["DataType"]:
                                                    if fkkeydict["DataField"] in listDict:
                                                        listDict[fkkeydict["DataField"]].append(Value)
                                                    else:
                                                        listDict[fkkeydict["DataField"]] = [Value]

                                                keyValueDict2[keyname] = {"DataField": fkkeydict["DataField"], "FKField": None, "Value": record[fieldName][Source]["Unique"][keyname]["Value"], "TableID": tableid,
                                                                          "RecordID": None}
                                                if "KeyType" in fkkeydict:
                                                    if fkkeydict2["KeyType"] != "Reference":
                                                        unqDict[keyname] = {"DataField": fkkeydict["DataField"], "FKField": None, "Value": record[fieldName][Source]["Unique"][keyname]["Value"], "TableID": tableid,
                                                                            "RecordID": None}
                                                else:
                                                    unqDict[keyname] = {"DataField": fkkeydict["DataField"], "FKField": None, "Value": record[fieldName][Source]["Unique"][keyname]["Value"], "TableID": tableid,
                                                                        "RecordID": None}

                                        record[fieldName][Destination]["Unique"] = unqDict
                                        # dictfield = record[fieldName][Destination]["DataField"]

                                        if keyValueDict2 != {}:
                                            if field not in keyValueDict2:
                                                # keyvalue = keyValueDict2[next(iter(keyValueDict2))]

                                                if FKPackage1 not in self.fkdict:
                                                    self.fkdict[FKPackage1] = {}
                                                if FKTable2 not in self.fkdict[FKPackage1]:
                                                    self.fkdict[FKPackage1][FKTable1] = self.sqlRegister.sqlDict["Location1"].session.query(self.sqlRegister.packageTableDict[FKPackage1][FKTable1])

                                                testquery2 = self.fkdict[FKPackage1][FKTable1]
                                                for keyname, keydict3 in keyValueDict2.items():
                                                    keyType = "ForeignKey"
                                                    if "KeyType" in fkkeydict:
                                                        if fkkeydict["KeyType"] == "Reference":
                                                            keyType = "Reference"

                                                    if keyType == "ForeignKey":
                                                        if keyValueDict2[keyname]["FKField"] is None:
                                                            fkfilter3 = [{'field': keydict3["DataField"], 'op': '==', 'value': keydict3["Value"]}]
                                                            testquery2 = apply_filters(testquery2, fkfilter3)
                                                        else:
                                                            if "RecordID" in keydict3:
                                                                if keydict3["RecordID"] is not None:
                                                                    # ToDo... I keep switching this
                                                                    fkfilter3 = [{'field': keydict3["DataField"], 'op': '==', 'value': keydict3["RecordID"]}]
                                                                    testquery2 = apply_filters(testquery2, fkfilter3)
                                                                else:
                                                                    fkfilter3 = [{'field': keydict3["DataField"], 'op': '==', 'value': keydict3["Value"]}]
                                                                    testquery2 = apply_filters(testquery2, fkfilter3)
                                                            else:
                                                                fkfilter3 = [{'field': keydict3["DataField"], 'op': '==', 'value': keydict3["Value"]}]
                                                                testquery2 = apply_filters(testquery2, fkfilter3)
                                                result = testquery2.first()
                                                fkquerycount2 = testquery2.count()
                                                createRecord = True
                                                if fkquerycount2 == 0:
                                                    newfkrecord = self.sqlRegister.packageTableDict[FKPackage1][FKTable1]()
                                                    for keyname, keydict4 in keyValueDict2.items():
                                                        if keydict4["Value"] is not None and keydict4["Value"] != "":
                                                            if "RecordID" in keydict4:
                                                                if keydict4["RecordID"] is not None:
                                                                    setattr(newfkrecord, fkkeydict["DataField"], keydict4["RecordID"])
                                                            else:
                                                                setattr(newfkrecord, fkkeydict["DataField"], keydict4["Value"])
                                                        else:
                                                            createRecord = False
                                                    if createRecord == True:
                                                        self.sqlRegister.sqlDict["Location1"].session.add(newfkrecord)
                                                        self.sqlRegister.sqlDict["Location1"].session.commit()
                                                        record[fieldName][Destination]["id"] = newfkrecord.id
                                                    else:
                                                        record[fieldName][Destination]["id"] = None
                                                else:
                                                    record[fieldName][Destination]["id"] = result.id
                                            else:
                                                record[fieldName][Destination]["id"] = unqDict[keyname]["RecordID"]

                        # Checking record on unique values
                        if package not in self.fkdict:
                            self.fkdict[package] = {}
                        if destinationTable not in self.fkdict[package]:
                            self.fkdict[package][destinationTable] = self.sqlRegister.sqlDict["Location1"].session.query(self.sqlRegister.packageTableDict[package][destinationTable])
                        filtered_query = self.fkdict[package][destinationTable].first()

                        uniqueValues = []
                        for uniqueFields in uniqueFieldGroups[0]:
                            FieldName = record[uniqueFields][Destination]["DataField"]

                            FieldValue = record[uniqueFields][Destination]["Value"]
                            if isinstance(FieldValue, float):
                                if np.isnan(FieldValue):
                                    FieldValue = None

                            if "id" in record[uniqueFields][Destination]:
                                if record[uniqueFields][Destination]["id"] is not None:
                                    FieldValue = record[uniqueFields][Destination]["id"]

                            uniqueValues.append(FieldValue)
                            filter_spec = [{'field': FieldName, 'op': '==', 'value': FieldValue}]
                            filtered_query = apply_filters(filtered_query, filter_spec)
                        result = filtered_query.count()

                        recordTable = self.dataConnection[Destination]["ItemList"][DataMapItem]["Table"]
                        recordPackage = itemdict["Package"]

                        # Create Record if it does not exist
                        if result == 0 and None not in uniqueValues:
                            self.sqlRegister.sqlDict["Location1"].session.begin_nested()
                            newfkrecord = self.sqlRegister.packageTableDict[recordPackage][recordTable]()
                            for fieldName2, fieldProperties2 in record.items():
                                if Destination in fieldProperties2:
                                    if fieldProperties[destinationDataFormat]["Active"]:
                                        if fieldName2 in ["DATE", "CLIENT CONTACT", "PROJECT CONTACT", "CONSIGNEE", "OWNER"]:
                                            pass
                                        if "Value" in fieldProperties2[Destination]:
                                            Field = fieldProperties2[Destination]["DataField"]
                                            Value = FieldValue = fieldProperties2[Destination]["Value"]

                                            if isinstance(FieldValue, str):
                                                if FieldValue[0] == "=":
                                                    for var in re.findall(r'\{(.*?)}', FieldValue):
                                                        if var in record[fieldName]:
                                                            DictValue = record[var][Source]["Value"]
                                                            # Replace the variable name with its value
                                                            expression = FieldValue.replace(f'{{{var}}}', str(DictValue))
                                                        else:
                                                            raise ValueError(f"Variable '{var}' not found in dictionary")
                                                    Value = eval(expression)
                                                else:
                                                    Value = FieldValue

                                        elif "DataField" in fieldProperties2[Destination]:
                                            Field = fieldProperties2[Destination]["DataField"]
                                            Value = fieldProperties2[Destination]["Value"]

                                            # SQL Doesnt Like Nan Bread
                                            if isinstance(Value, float):
                                                if np.isnan(Value):
                                                    Value = None

                                            if fieldProperties2[Destination]["DataType"] == "date":
                                                try:
                                                    Value = Value.toPyDateTime()
                                                    if "Format" in fieldProperties[destinationDataFormat]:
                                                        Value = datetime.strptime(Value, fieldProperties[destinationDataFormat]["Format"]).date()
                                                except:
                                                    pass
                                            if fieldProperties2[Destination]["DataType"] == "int" and isinstance(Value, str):
                                                # When i can find the value so i default it to 1
                                                Value = 1

                                        if fieldProperties2[Destination]["id"] is not None:
                                            ID = fieldProperties2[Destination]["id"]
                                            if ID is not None:
                                                Value = ID

                                        setattr(newfkrecord, Field, Value)

                            self.sqlRegister.sqlDict["Location1"].session.add(newfkrecord)
                            self.sqlRegister.sqlDict["Location1"].session.commit()
                            FKValue2 = newfkrecord.id  # update this to create a new record
                        else:
                            pass  # Check compare all fields to see which one is updated the best
                        bar()
    def LoadSQLConnection(self):
        tblExcelBook = {}
        tblExcelBook["Project List"] = {"Format": "SQL", "TableName": "Project", "PrimaryKey": "id"}
        tblExcelBook["Tracking"] = {"Format": "SQL", "TableName": "Equipment", "PrimaryKey": "id", "DataType": "int"}
        tblExcelBook["Equipment"] = {"Format": "SQL", "TableName": "Equipment", "PrimaryKey": "id"}
        tblExcelBook["ProjectEquipment"] = {"Format": "SQL", "TableName": "ProjectEquipment", "PrimaryKey": "id"}
        tblExcelBook["OwnerEquipment"] = {"Format": "SQL", "TableName": "Equipment", "PrimaryKey": "id"}
        tblExcelBook["Company"] = {"Format": "SQL", "TableName": "Company", "PrimaryKey": "id"}
        tblExcelBook["Person"] = {"Format": "SQL", "TableName": "Person", "PrimaryKey": "id"}
        tblExcelBook["PersonAffiliation"] = {"Format": "SQL", "TableName": "PersonAffiliation", "PrimaryKey": "id"}
        tblExcelBook["PersonContact"] = {"Format": "SQL", "TableName": "PersonContact", "PrimaryKey": "id"}
        tblExcelBook["Training"] = {"Format": "SQL", "TableName": "Project", "PrimaryKey": "id"}
        tblExcelBook["Inspection"] = {"Format": "SQL", "TableName": "Project", "PrimaryKey": "id"}
        tblExcelBook["Work Order"] = {"Format": "SQL", "TableName": "WorkOrder", "PrimaryKey": "id"}
        tblExcelBook["Work Order Items"] = {"Format": "SQL", "TableName": "WorkOrderItem", "PrimaryKey": "id"}
        tblExcelBook["Invoice"] = {"Format": "SQL", "TableName": "Project", "PrimaryKey": "id"}
        tblExcelBook["RateSheet"] = {"Format": "SQL", "TableName": "Project", "PrimaryKey": "id"}
        return tblExcelBook

    def loadExcelConnection(self):
        tblExcelBook = {}
        tblExcelBook["Project List"] = {"Format": "Excel",
                                        "WorkBook": r"C:/Users/d_lar/OneDrive/Enigma Design Solutions/Projects/EDS - Project List.xlsm",
                                        "Sheet": "Project List", "TableName": "tbl_ProjectList", "PrimaryKey": "ID",
                                        "HeaderRow": 1, "StartColumn": 1, "StartRow": 2,  "PrimaryColumn": 1}

        tblExcelBook["Tracking"] = {"Format": "Excel",
                                    "WorkBook": r"C:/Users/d_lar/OneDrive/Enigma Design Solutions/Projects/EDS - Project List.xlsm",
                                    "Sheet": "Project List", "TableName": "tbl_ProjectList", "PrimaryKey": "ID", "DataType": "int",
                                    "HeaderRow": -1, "StartColumn": 1, "StartRow": -1, "PrimaryColumn": 1}

        tblExcelBook["Equipment"] = {"Format": "Excel",
                                     "WorkBook": r"C:/Users/d_lar/OneDrive/Enigma Design Solutions/Projects/EDS - Project List.xlsm",
                                     "Sheet": "Project List", "TableName": "tbl_ProjectList", "PrimaryKey": "ID",
                                     "HeaderRow": -1, "StartColumn": 1, "StartRow": -1, "PrimaryColumn": -1}

        tblExcelBook["ProjectEquipment"] = {"Format": "Excel",
                                            "WorkBook": r"C:/Users/d_lar/OneDrive/Enigma Design Solutions/Projects/EDS - Project List.xlsm",
                                            "Sheet": "Project List", "TableName": "tbl_ProjectList",
                                            "PrimaryKey": "ID", "HeaderRow": -1, "StartColumn": 1, "StartRow": -1, "PrimaryColumn": -1}

        tblExcelBook["OwnerEquipment"] = {"Format": "Excel",
                                          "WorkBook": r"C:/Users/d_lar/OneDrive/Enigma Design Solutions/Projects/EDS - Project List.xlsm",
                                          "Sheet": "Project List", "TableName": "tbl_ProjectList", "PrimaryKey": "ID",
                                          "HeaderRow": -1, "StartColumn": 1, "StartRow": -1, "PrimaryColumn": -1}

        tblExcelBook["Company"] = {"Format": "Excel",
                                   "WorkBook": r"C:/Users/d_lar/OneDrive/Enigma Design Solutions/Projects/EDS - Project List.xlsm",
                                   "Sheet": "Client Information", "TableName": "tbl_ClientList", "PrimaryKey": "ID",
                                   "HeaderRow": 1, "StartColumn": 1, "StartRow": 2, "PrimaryColumn": 1}

        tblExcelBook["Person"] = {"Format": "Excel",
                                  "WorkBook": r"C:/Users/d_lar/OneDrive/Enigma Design Solutions/Projects/EDS - Project List.xlsm",
                                  "Sheet": "Contact Information", "TableName": "tbl_ContactList", "PrimaryKey": "ID",
                                  "HeaderRow": 1, "StartColumn": 1, "StartRow": 2, "PrimaryColumn": 1}

        tblExcelBook["PersonAffiliation"] = {"Format": "Excel",
                                             "WorkBook": r"C:/Users/d_lar/OneDrive/Enigma Design Solutions/Projects/EDS - Project List.xlsm",
                                             "Sheet": "Contact Information", "TableName": "tbl_ContactList", "PrimaryKey": "ID",
                                             "HeaderRow": 1, "StartColumn": 1, "StartRow": 2, "PrimaryColumn": 1}

        tblExcelBook["PersonContact"] = {"Format": "Excel",
                                         "WorkBook": r"C:/Users/d_lar/OneDrive/Enigma Design Solutions/Projects/EDS - Project List.xlsm",
                                         "Sheet": "Contact Information", "TableName": "tbl_ContactList", "PrimaryKey": "ID",
                                         "HeaderRow": 1, "StartColumn": 1, "StartRow": 2, "PrimaryColumn": 1}

        tblExcelBook["Training"] = {"Format": "Excel",
                                    "WorkBook": r"C:/Users/d_lar/OneDrive/Enigma Design Solutions/Projects/EDS - Project List.xlsm",
                                    "Sheet": "Contact Information", "TableName": "tbl_ContactList", "PrimaryKey": "ID",
                                    "HeaderRow": 1, "StartColumn": 1, "StartRow": 2, "PrimaryColumn": 1}

        tblExcelBook["Inspection"] = {"Format": "Excel",
                                      "WorkBook": r"C:/Users/d_lar/OneDrive/Enigma Design Solutions/Projects/EDS - Project List.xlsm",
                                      "Sheet": "Project List", "TableName": "tbl_ProjectList", "PrimaryKey": "ID",
                                      "HeaderRow": 1, "StartColumn": 1, "StartRow": 2, "PrimaryColumn": 1}

        tblExcelBook["Work Order"] = {"Format": "Excel", "WorkBook": r"C:/Users/d_lar/OneDrive/Enigma Design Solutions/Projects/EDS - Project List.xlsm",
                                      "Sheet": "Project List", "TableName": "tbl_ProjectList", "PrimaryKey": "ID",
                                      "HeaderRow": 1, "StartColumn": 1, "StartRow": 2, "PrimaryColumn": 1}

        tblExcelBook["Work Order Items"] = {"Format": "Excel",
                                            "WorkBook": r"C:/Users/d_lar/OneDrive/Enigma Design Solutions/Projects/EDS - Project List.xlsm",
                                            "Sheet": "Project List", "TableName": "tbl_ProjectList", "PrimaryKey": "ID",
                                            "HeaderRow": 1, "StartColumn": 1, "StartRow": 2, "PrimaryColumn": 1}

        tblExcelBook["Invoice"] = {"Format": "Excel",
                                   "WorkBook": r"C:/Users/d_lar/OneDrive/Enigma Design Solutions/Projects/EDS - Project List.xlsm",
                                   "FKSheet": "Ageing Report", "TableName": "tbl_Invoice", "PrimaryKey": "ID",
                                   "HeaderRow": 1, "StartColumn": 1, "StartRow": 2, "PrimaryColumn": 1}

        tblExcelBook["RateSheet"] = {"Format": "Excel",
                                     "WorkBook": r"C:/Users/d_lar/OneDrive/Enigma Design Solutions/Projects/EDS - Project List.xlsm",
                                     "Sheet": "Rate Sheet", "TableName": "tbl_RateSheet", "PrimaryKey": "ID",
                                     "HeaderRow": 11, "StartColumn": 1, "StartRow": 12, "PrimaryColumn": 1}
        return tblExcelBook
    def DataMapItems(self):
        tblExcelBook = {}
        tblProjectList = {}
        # tblProjectList["ID"] = {"Excel": {"DataField": "ID", "DataType": "int", "DataColumn": None},
        #                        "SQL": {"DataField": "id", "PrimaryKey": True}}
        tblProjectList["DATE"] = {"Excel": {"DataField": "DATE", "Format": "%B %d, %Y", "DataColumn": None, "DataType": "date", "Active": True},
                                  "SQL": {"DataField": "Start_Date", "Format": "%B %d, %Y", "DataType": "date", "Active": True}}

        tblProjectList["PROJECT NUMBER"] = {"Excel": {"DataField": "PROJECT NUMBER", "DataColumn": None, "DataType": "str", "Active": True},
                                            "SQL": {"DataField": "ProjectNumber", "DataType": "str", "Active": True}}

        tblProjectList["SUB PROJECT NUMBER"] = {
            "Excel": {"DataField": "SUB PROJECT NUMBER", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "SubProjectNumber", "DataType": "str", "Active": True}}

        tblProjectList["PROJECT TITLE"] = {"Excel": {"DataField": "PROJECT TITLE", "DataColumn": None, "DataType": "str", "Active": True},
                                           "SQL": {"DataField": "ProjectTitle", "DataType": "str", "Active": True}}
        # tblProjectList["STATUS"] = {"DataType": "str", "DataColumn": "F", "Key": "ProjectStatus"}, "SQL": {"DataField": "Status"}}
        tblProjectList["CONSIGNEE"] = {
            "Excel": {"DataField": "CONSIGNEE", "DataColumn": None, "FKValue": "{Company Name} ({City})", "DataType": "str", "Active": True,
                      "FKSheet": "Client Information", "FKTable": "tbl_ClientList", "FKField": "Project List Name",
                      "Key": {"Company Name": {"FKField": "Legal Name", "DataType": "str"},
                              "City": {"FKField": "Physical City", "DataType": "str"}}},
            "SQL": {"DataField": "Owner", "DataType": "int", "Active": True,
                       "Package": "ProjectList", "FKTable": "Company", "FKField": "id",
                       "Key": {"Company Name": {"DataField": "LegalName", "DataType": "str"},
                               "City": {"DataField": "PhysicalCity", "DataType": "int",
                                        "Package": "ProgramBase", "FKTable": "City", "FKField": "NameText"}}}}

        tblProjectList["OWNER"] = {
            "Excel": {"DataField": "OWNER", "DataColumn": None, "FKValue": "{Company Name} ({City})", "DataType": "str", "Active": True,
                      "FKSheet": "Client Information", "FKTable": "tbl_ClientList", "FKField": "Project List Name",
                      "Key": {"Company Name": {"FKField": "Legal Name", "DataType": "str"},
                              "City": {"FKField": "Physical City", "DataType": "str"}}},
            "SQL": {"DataField": "Owner", "DataType": "int", "Active": True,
                       "Package": "ProjectList", "FKTable": "Company", "FKField": "id",
                       "Key": {"Company Name": {"DataField": "LegalName", "DataType": "str"},
                               "City": {"DataField": "PhysicalCity", "DataType": "int",
                                        "Package": "ProgramBase", "FKTable": "City", "FKField": "NameText"}}}}

        tblProjectList["CLIENT CONTACT"] = {
            "Excel": {"DataField": "CLIENT CONTACT", "DataColumn": None, "FKValue": "{First Name} {Last Name}", "DataType": "str", "Active": True,
                      "FKSheet": "Contact Information", "FKTable": "tbl_ContactList", "FKField": "COMMON NAME",
                      "Key": {"First Name": {"FKField": "FIRST NAME", "DataType": "str"},
                              "Last Name": {"FKField": "LAST NAME", "DataType": "str"}}},
            "SQL": {"DataField": "ClientContact", "DataType": "int",
                       "Package": "ProjectList", "FKTable": "Person", "FKField": "id",
                       "Key": {"First Name": {"DataField": "FirstName", "DataType": "str"},
                               "Last Name": {"DataField": "LastName", "DataType": "str"}}}}

        tblProjectList["PROJECT CONTACT"] = {
            "Excel": {"DataField": "SUPERVISOR", "DataColumn": None, "FKValue": "{First Name} {Last Name}", "DataType": "str", "Active": True,
                      "FKSheet": "Contact Information", "FKTable": "tbl_ContactList", "FKField": "COMMON NAME",
                      "Key": {"First Name": {"FKField": "FIRST NAME", "DataType": "str"},
                              "Last Name": {"FKField": "LAST NAME", "DataType": "str"}}},
            "SQL": {"DataField": "ClientContact", "DataType": "int",
                       "Package": "ProjectList", "FKTable": "Person", "FKField": "id",
                       "Key": {"First Name": {"DataField": "FirstName", "DataType": "str"},
                               "Last Name": {"DataField": "LastName", "DataType": "str"}}}}

        tblProjectList["ENGINEER"] = {
            "Excel": {"DataField": "ENGINEER", "DataColumn": None, "FKValue": "{First Name} {Last Name}", "DataType": "str", "Active": True,
                      "FKSheet": "Contact Information", "FKTable": "tbl_ContactList", "FKField": "COMMON NAME",
                      "Key": {"First Name": {"FKField": "FIRST NAME", "DataType": "str"},
                              "Last Name": {"FKField": "LAST NAME", "DataType": "str"}}},
            "SQL": {"DataField": "ClientContact", "DataType": "int", "Active": True,
                       "Package": "ProjectList", "FKTable": "Person", "FKField": "id",
                       "Key": {"First Name": {"DataField": "FirstName", "DataType": "str"},
                               "Last Name": {"DataField": "LastName", "DataType": "str"}}}}

        tblProjectList["INSPECTOR"] = {
            "Excel": {"DataField": "INSPECTOR", "DataColumn": None, "FKValue": "{First Name} {Last Name}", "DataType": "str", "Active": True,
                      "FKSheet": "Contact Information", "FKTable": "tbl_ContactList", "FKField": "COMMON NAME",
                      "Key": {"First Name": {"FKField": "FIRST NAME", "DataType": "str"},
                              "Last Name": {"FKField": "LAST NAME", "DataType": "str"}}},
            "SQL": {"DataField": "ClientContact", "DataType": "int", "Active": True,
                       "Package": "ProjectList", "FKTable": "Person", "FKField": "id",
                       "Key": {"First Name": {"DataField": "FirstName", "DataType": "str"},
                               "Last Name": {"DataField": "LastName", "DataType": "str"}}}}

        tblProjectList["LOCATION"] = {
            "Excel": {"DataField": "LOCATION", "DataColumn": None, "DataType": "str", "Active": True,
                      "Key": {"City": {"DataField": "LOCATION", "DataType": "str"}}},
            "SQL": {"DataField": "Location", "Package": "ProgramBase", "FKTable": "City",
                       "FKValue": "id", "DataType": "int", "Active": True,
                       "Key": {"City": {"DataField": "NameText", "DataType": "str"}}}}

        tblProjectList["PURCHASE ORDER"] = {
            "Excel": {"DataField": "PURCHASE ORDER", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "PurchaseOrder", "DataType": "str", "Active": True}}

        tblProjectList["YEAR"] = {
            "Excel": {"DataField": "YEAR", "DataType": "int", "DataColumn": None, "Active": True},
            "SQL": {"DataField": "Year", "DataType": "int", "Active": True}}

        tblProjectList["MONTH"] = {
            "Excel": {"DataField": "MONTH", "DataType": "int", "DataColumn": None, "Active": True},
            "SQL": {"DataField": None, "DataType": None, "Active": False}}

        tblExcelBook["Project List"] = {"Package": "ProjectList", "DataMap": tblProjectList,
                                        "UniqueFields": [["PROJECT NUMBER"]]}

        # This belongs to a more complicated task tree
        tblTask = {}
        tblTask["ASSESSMENT"] = {
            "Excel": {"DataField": "ASSESSMENT", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "Assessment", "Active": True,
                    "Key": {"Package": "ProjectList", "Table": "Journal", "Category": "Assessment"}}}

        tblTask["DRAWINGS"] = {
            "Excel": {"DataField": "DRAWINGS", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "Drawings", "Active": True,
                    "Key": {"Package": "ProjectList", "Table": "Journal", "Category": "Assessment"}}}

        tblTask["EQUIPMENT INSPECTION"] = {
            "Excel": {"DataField": "EQUIPMENT INSPECTION", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "EquipmentInspection", "Active": True,
                    "Key": {"Package": "ProjectList", "Table": "Journal", "Category": "Assessment"}}}

        tblTask["INSPECTION CERTIFICATE"] = {
            "Excel": {"DataField": "INSPECTION CERTIFICATE", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "InspectionCertificate", "Active": True,
                    "Key": {"Package": "ProjectList", "Table": "Journal", "Category": "Assessment"}}}

        tblTask["LAMINATE CERTIFICATE"] = {
            "Excel": {"DataField": "LAMINATE CERTIFICATE", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "LaminateCertificate", "Active": True,
                    "Key": {"Package": "ProjectList", "Table": "Journal", "Category": "Assessment"}}}

        tblTask["REPAIRS"] = {
            "Excel": {"DataField": "REPAIRS", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "Repairs", "Active": True,
                    "Key": {"Package": "ProjectList", "Table": "Journal", "Category": "Assessment"}}}

        tblTask["LOAD TEST"] = {
            "Excel": {"DataField": "LOAD TEST", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "Load Test", "Active": True,
                    "Key": {"Package": "ProjectList", "Table": "Journal", "Category": "Assessment"}}}

        tblTask["FEA ANALYSIS"] = {
            "Excel": {"DataField": "FEA ANALYSIS", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "Load Test", "Active": True,
                    "Key": {"Package": "ProjectList", "Table": "Journal", "Category": "Assessment"}}}

        tblTask["ENGINEERING CERT"] = {
            "Excel": {"DataField": "ENGINEERING CERT", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "Load Test", "Active": True,
                    "Key": {"Package": "ProjectList", "Table": "Journal", "Category": "Assessment"}}}

        tblTask["PO STATUS"] = {
            "Excel": {"DataField": "PO STATUS", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "Contact", "DataType": "int", "Active": True}}

        tblTask["ADMINISTRATION"] = {
            "Excel": {"DataField": "ADMINISTRATION", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "Contact", "DataType": "int", "Active": True,
                    "Key": {"Package": "ProjectList", "Table": "Journal", "Category": "Assessment"}}}

        tblTask["INVOICING"] = {
            "Excel": {"DataField": "INVOICING", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "Load Test", "DataType": "int", "Active": True,
                    "Key": {"Package": "ProjectList", "Table": "Journal", "Category": "Assessment"}}}

        tblExcelBook["Tracking"] = {"Package": "ProjectList", "DataMap": tblTask, "UniqueFields": [["MANUFACTURER", "MODEL", "SERIAL"]]}

        tblEquipment = {}
        tblEquipment["EQUIPMENT CATEGORY"] = {
            "Excel": {"DataField": "EQUIPMENT CATEGORY", "DataColumn": None, "DataType": "str", "Active": True,
                      "Key": {"EquipmentItem": {"DataField": "EQUIPMENT CATEGORY", "DataType": "str"}}},
            "SQL": {"DataField": "Category", "DataType": "int", "Active": True,
                    "Package": "ProjectList", "FKTable": "EquipmentItem", "FKField": "NameText",
                    "Key": {"EquipmentItem": {"DataField": "Category", "DataType": "int",
                                              "Package": "ProjectList", "FKTable": "EquipmentItem", "FKField": "NameText"}}}}

        tblEquipment["EQUIPMENT TYPE"] = {
            "Excel": {"DataField": "EQUIPMENT TYPE", "DataColumn": None, "DataType": "str", "Active": True,
                      "Key": {"EquipmentType": {"DataField": "EQUIPMENT CATEGORY", "DataType": "str"}}},
            "SQL": {"DataField": "EquipmentType", "DataType": "int", "Active": True,
                    "Package": "ProjectList", "FKTable": "EquipmentItem", "FKField": "NameText",
                    "Key": {"EquipmentType": {"DataField": "EquipmentType", "DataType": "int",
                                              "Package": "ProjectList", "FKTable": "EquipmentItem", "FKField": "NameText"}}}}

        tblEquipment["SUB ASSEMBLY"] = {
            "Excel": {"DataField": "SUB ASSEMBLY", "DataColumn": None, "DataType": "str", "Active": True,
                      "Key": {"SubAssembly": {"DataField": "EQUIPMENT CATEGORY", "DataType": "str"}}},
            "SQL": {"DataField": "SubAssembly", "DataType": "int", "Active": True,
                    "Package": "ProjectList", "FKTable": "EquipmentItem", "FKField": "NameText",
                    "Key": {"SubAssembly": {"DataField": "SubAssembly", "DataType": "int",
                                            "Package": "ProjectList", "FKTable": "EquipmentItem", "FKField": "NameText"}}}}

        tblEquipment["COMPONENT"] = {
            "Excel": {"DataField": "COMPONENT", "DataType": "int", "DataColumn": None, "Active": True,
                      "Key": {"Component": {"DataField": "EQUIPMENT CATEGORY", "DataType": "str"}}},
            "SQL": {"DataField": "Component", "DataType": "int", "Active": True,
                    "Package": "ProjectList", "FKTable": "EquipmentItem", "FKField": "NameText",
                    "Key": {"Component": {"DataField": "Component", "DataType": "int",
                                          "Package": "ProjectList", "FKTable": "EquipmentItem", "FKField": "NameText"}}}}

        # todo these two will be combined in the future to a single statement
        tblEquipment["MANUFACTURER"] = {
            "Excel": {"DataField": "MANUFACTURER", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "Manufacturer", "DataType": "str", "Active": True}}

        tblEquipment["MANUFACTURER_ID"] = {
            "Excel": {"DataField": "MANUFACTURER", "DataColumn": None, "FKValue": "{Company Name} ({City})", "DataType": "str", "Active": True,
                      "FKSheet": "Client Information", "FKTable": "tbl_ClientList", "FKField": "Project List Name",
                      "Key": {"Company Name": {"FKField": "Legal Name", "DataType": "str"},
                              "City": {"FKField": "Physical City", "DataType": "str"}}},
            "SQL": {"DataField": "Manufacturer_id", "DataType": "int", "Active": True,
                    "Package": "ProjectList", "FKTable": "Company", "FKField": "id",
                    "Key": {"Company Name": {"DataField": "LegalName", "DataType": "str"},
                               "City": {"DataField": "PhysicalCity", "DataType": "int",
                                        "Package": "ProgramBase", "FKTable": "City", "FKField": "NameText"}}}}

        tblEquipment["MODEL"] = {"Excel": {"DataField": "MODEL", "DataColumn": None, "DataType": "str", "Active": True},
                                 "SQL": {"DataField": "Model", "DataType": "str", "Active": True}}
        tblEquipment["SERIAL"] = {"Excel": {"DataField": "SERIAL", "DataColumn": None, "DataType": "str", "Active": True},
                                  "SQL": {"DataField": "Serial", "DataType": "str", "Active": True}}
        tblEquipment["UNIT"] = {"Excel": {"DataField": "UNIT", "DataColumn": None, "DataType": "str", "Active": True},
                                "SQL": {"DataField": "Unit", "DataType": "str", "Active": True}}

        # I put -1 in for values because this table exists only inside another table and is not a standalone table of unique values
        tblExcelBook["Equipment"] = {"Package": "ProjectList", "DataMap": tblEquipment,
                                     "UniqueFields": [["MANUFACTURER", "MODEL", "SERIAL"]]}

        tblProjectEquipment = {}
        tblEquipment["Project"] = {
            "Excel": {"DataField": "PROJECT NUMBER", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "Project Number", "Package": "ProgramBase", "FKTable": "Country", "FKField": "NameText", "DataType": "int",
                    "Key": {"Project Number": {"DataField": "project_id", "DataType": "int", "Active": True,
                                                  "Package": "ProgramBase", "FKTable": "Project", "FKField": "ProjectNumber"}}}}

        tblProjectEquipment["EQUIPMENT"] = {
            "Excel": {"DataField": "Equipment", "DataColumn": None, "DataType": "str", "Active": True,
                      "Key": {"Manufacturer": {"DataField": "MANUFACTURER", "DataType": "str"},
                              "Model": {"DataField": "MODEL", "DataType": "str"},
                              "Serial": {"DataField": "SERIAL", "DataType": "str"}}},
            "SQL": {"DataField": "Equipment", "DataType": "int", "Active": True, "Package": "ProjectList",
                    "FKTable": "Equipment", "FKField": "id",
                    "Key": {"Manufacturer": {"DataField": "Manufacturer", "DataType": "str", "Package": "ProjectList", "FKTable": "Equipment", "FKField": "Manufacturer"},
                               "Model": {"DataField": "Model", "DataType": "str", "Package": "ProjectList", "FKTable": "Equipment", "FKField": "Model"},
                               "Serial": {"DataField": "Serial", "DataType": "str", "Package": "ProjectList", "FKTable": "Equipment", "FKField": "Serial"}}}}

        tblExcelBook["ProjectEquipment"] = {"Package": "ProjectList", "DataMap": tblProjectEquipment}

        tblOwnerEquipment = {}
        tblOwnerEquipment["OWNER"] = {
            "Excel": {"DataField": "OWNER", "DataColumn": None, "FKValue": "{Company Name} ({City})", "DataType": "str", "Active": True,
                      "FKSheet": "Client Information", "FKTable": "tbl_ClientList", "FKField": "Project List Name",
                      "Key": {"Company Name": {"FKField": "Legal Name", "DataType": "str"},
                              "City": {"FKField": "Physical City", "DataType": "str"}}},
            "SQL": {"DataField": "Manufacturer_id", "DataType": "int", "Active": True, "Package": "ProjectList", "FKTable": "Company", "FKField": "id",
                    "Key": {"Company Name": {"DataField": "LegalName", "DataType": "str"},
                               "City": {"DataField": "PhysicalCity", "DataType": "int", "Package": "ProgramBase", "FKTable": "City", "FKField": "NameText"}}}}

        tblOwnerEquipment["EQUIPMENT"] = {
            "Excel": {"DataField": "Equipment", "DataColumn": None, "DataType": "str", "Active": True,
                      "Key": {"Manufacturer": {"DataField": "MANUFACTURER", "DataType": "str"},
                              "Model": {"DataField": "MODEL", "DataType": "str"},
                              "Serial": {"DataField": "SERIAL", "DataType": "str"}}},
            "SQL": {"DataField": "Equipment", "DataType": "int", "Active": True, "Package": "ProjectList",
                    "FKTable": "Equipment", "FKField": "id",
                    "Key": {"Manufacturer": {"DataField": "Manufacturer", "DataType": "str", "Package": "ProjectList", "FKTable": "Equipment", "FKField": "Manufacturer"},
                               "Model": {"DataField": "Model", "DataType": "str", "Package": "ProjectList", "FKTable": "Equipment", "FKField": "Model"},
                               "Serial": {"DataField": "Serial", "DataType": "str", "Package": "ProjectList", "FKTable": "Equipment", "FKField": "Serial"}}}}

        tblExcelBook["OwnerEquipment"] = {"Package": "ProjectList", "DataMap": tblOwnerEquipment}

        tblCompany = {}
        tblCompany["PROJECT LIST NAME"] = {
            "Excel": {"DataField": "Project List Name", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "Title", "DataType": "str", "Active": True}}

        tblCompany["LEGAL NAME"] = {
            "Excel": {"DataField": "Legal Name", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "LegalName", "DataType": "str", "Active": True}}

        tblCompany["COMBINED"] = {
            "Excel": {"DataField": "Combined", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "CommonName", "DataType": "str", "Active": True}}

        # tblCompany["PROJECT LIST NAME"] = {"Excel": {"DataField": "PROJECT LIST NAME", "DataColumn": None, "DataType": "str"}, "SQL": {"DataField": "Capacity"}}
        # tblCompany["RELATIONSHIP"] = {"Excel": {"DataField": "RELATIONSHIP", "DataColumn": None, "DataType": "str"}, "SQL": {"DataField": "Capacity"}}
        tblCompany["PHYSICAL STREET"] = {
            "Excel": {"DataField": "Physical Street", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "PhysicalStreet", "DataType": "str", "Active": True}}

        tblCompany["PHYSICAL CITY"] = {
            "Excel": {"DataField": "Physical City", "DataColumn": None, "PrimaryKey": "ID",
                      "FKSheet": "Client Information", "FKTable": "tbl_ClientList", "DataType": "str", "Active": True},
            "SQL": {"DataField": "PhysicalCity", "Package": "ProgramBase", "FKTable": "City", "FKField": "NameText", "DataType": "int",
                       "Key": {"City": {"DataField": "PhysicalCity", "DataType": "int", "Active": True,
                                        "Package": "ProgramBase", "FKTable": "City", "FKField": "NameText"}}}}

        tblCompany["PHYSICAL PROVINCE"] = {
            "Excel": {"DataField": "Physical Province", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "PhysicalProvince", "Package": "ProgramBase", "FKTable": "Province", "FKField": "NameText", "DataType": "int",
                       "Key": {"Province": {"DataField": "PhysicalProvince", "DataType": "int", "Active": True,
                                            "Package": "ProgramBase", "FKTable": "Province", "FKField": "NameText"}}}}

        tblCompany["PHYSICAL COUNTRY"] = {
            "Excel": {"DataField": "Physical Country", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "PhysicalCountry", "Package": "ProgramBase", "FKTable": "Country", "FKField": "NameText", "DataType": "int",
                       "Key": {"Country": {"DataField": "PhysicalCountry", "DataType": "int", "Active": True,
                                           "Package": "ProgramBase", "FKTable": "Country", "FKField": "NameText"}}}}

        tblCompany["MAILING CITY"] = {
            "Excel": {"DataField": "Mailing City", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "MailingCity", "Package": "ProgramBase", "FKTable": "City", "FKField": "NameText", "DataType": "int",
                       "Key": {"City": {"DataField": "PhysicalCity", "DataType": "int", "Active": True,
                                        "Package": "ProgramBase", "FKTable": "City", "FKField": "NameText"}}}}

        tblCompany["MAILING PROVINCE"] = {
            "Excel": {"DataField": "Mailing Province", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "MailingProvince", "Package": "ProgramBase", "FKTable": "Province", "FKField": "NameText", "DataType": "int",
                       "Key": {"Province": {"DataField": "PhysicalProvince", "DataType": "int", "Active": True,
                                            "Package": "ProgramBase", "FKTable": "Province", "FKField": "NameText"}}}}

        tblCompany["MAILING COUNTRY"] = {
            "Excel": {"DataField": "Mailing Country", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "MailingCountry", "Package": "ProgramBase", "FKTable": "Country", "FKField": "NameText", "DataType": "int",
                       "Key": {"Country": {"DataField": "MailingCountry", "DataType": "int", "Active": True,
                                           "Package": "ProgramBase", "FKTable": "Country", "FKField": "NameText"}}}}

        tblCompany["MAILING POSTAL CODE"] = {
            "Excel": {"DataField": "Mailing Postal Code", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "MailingPostalCode", "Package": "ProgramBase", "FKTable": "PostalCode", "FKField": "NameText", "DataType": "int",
                       "Key": {"City": {"DataField": "MailingPostalCode", "DataType": "int", "Active": True,
                                        "Package": "ProgramBase", "FKTable": "PostalCode", "FKField": "NameText"}}}}

        tblCompany["PO BOX"] = {
            "Excel": {"DataField": "PO Box", "DataType": "str", "Active": True, "DataColumn": "N"},
            "SQL": {"DataField": "MailingBoxNumber", "DataType": "str", "Active": True}}

        tblCompany["PO BOX LOCATION"] = {
            "Excel": {"DataField": "PO Box Location", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "MailingBoxLocation", "DataType": "str", "Active": True}}

        tblCompany["INVOICE STREET"] = {
            "Excel": {"DataField": "Invoice Street", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "InvoiceStreet", "DataType": "str", "Active": True}}

        tblCompany["INVOICE PO BOX"] = {
            "Excel": {"DataField": "Invoice PO Box", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "InvoiceBoxNumber", "DataType": "str", "Active": True}}

        tblCompany["INVOICE PO BOX LOCATION"] = {
            "Excel": {"DataField": "Invoice PO Box Location", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "InvoiceBoxLocation", "DataType": "str", "Active": True}}

        tblCompany["INVOICE CITY"] = {
            "Excel": {"DataField": "Invoice City", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "InvoiceCity", "Package": "ProgramBase", "FKTable": "City", "FKField": "NameText", "DataType": "int", "Active": True,
                    "Key": {"City": {"DataField": "InvoiceCity", "DataType": "int",
                                        "Package": "ProgramBase", "FKTable": "City", "FKField": "NameText"}}}}

        tblCompany["INVOICE PROVINCE"] = {
            "Excel": {"DataField": "Invoice Province", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "InvoiceProvince", "Package": "ProgramBase", "FKTable": "Province", "FKField": "NameText", "DataType": "int", "Active": True,
                    "Key": {"Province": {"DataField": "InvoiceProvince", "DataType": "int",
                                            "Package": "ProgramBase", "FKTable": "Province", "FKField": "NameText"}}}}

        tblCompany["INVOICE COUNTRY"] = {
            "Excel": {"DataField": "Invoice Country", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "InvoiceCountry", "Package": "ProgramBase", "FKTable": "Country", "FKField": "NameText", "DataType": "int", "Active": True,
                    "Key": {"Country": {"DataField": "PhysicalCountry", "DataType": "int",
                                           "Package": "ProgramBase", "FKTable": "Country", "FKField": "NameText"}}}}

        tblCompany["INVOICE POSTAL CODE"] = {
            "Excel": {"DataField": "Invoice Postal Code", "DataColumn": None, "DataType": "str", "Active": True,
                      "Key": {"PostalCode": {"DataField": "Invoice Postal Code", "DataType": "str"}}},
            "SQL": {"DataField": "InvoicePostalCode", "Package": "ProgramBase",
                    "FKTable": "PostalCode", "FKField": "NameText", "DataType": "int", "Active": True,
                    "Key": {"PostalCode": {"DataField": "InvoicePostalCode", "DataType": "int",
                                           "Package": "ProgramBase", "FKTable": "PostalCode", "FKField": "NameText"}}}}

        tblCompany["INVOICE EMAIL"] = {
            "Excel": {"DataField": "Invoice Email", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "InvoiceEmail", "DataType": "str", "Active": True}}
        tblCompany["WEBSITE"] = {
            "Excel": {"DataField": "Website", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "WebAddress", "DataType": "str", "Active": True}}
        tblCompany["GST NUMBER"] = {
            "Excel": {"DataField": "GST Number", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "GSTNumber", "DataType": "str", "Active": True}}
        tblCompany["CWB NUMBER"] = {
            "Excel": {"DataField": "CWB Number", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "CWBNumber", "DataType": "str", "Active": True}}
        tblCompany["WCB NUMBER"] = {
            "Excel": {"DataField": "WBC Number", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "WCBNumber", "DataType": "str", "Active": True}}

        tblExcelBook["Company"] = {"Package": "ProjectList", "DataMap": tblCompany,
                                   "UniqueFields": [["LEGAL NAME", "PHYSICAL CITY"]]}

        tblPerson = {}
        tblPerson["SURNAME"] = {"Excel": {"DataField": "SURNAME", "DataColumn": None, "DataType": "str", "Active": True},
                                "SQL": {"DataField": "Prefix", "DataType": "str", "Active": True}}
        tblPerson["FIRST NAME"] = {"Excel": {"DataField": "FIRST NAME", "DataColumn": None, "DataType": "str", "Active": True},
                                   "SQL": {"DataField": "FirstName", "DataType": "str", "Active": True}}
        tblPerson["MIDDLE NAME"] = {"Excel": {"DataField": "MIDDLE NAME", "DataColumn": None, "DataType": "str", "Active": True},
                                    "SQL": {"DataField": "MiddleName", "DataType": "str", "Active": True}}
        tblPerson["LAST NAME"] = {"Excel": {"DataField": "LAST NAME", "DataColumn": None, "DataType": "str", "Active": True},
                                  "SQL": {"DataField": "LastName", "DataType": "str", "Active": True}}
        tblPerson["NAME TITLE"] = {"Excel": {"DataField": "NAME TITLE", "DataColumn": None, "DataType": "str", "Active": True},
                                   "SQL": {"DataField": "Suffix", "DataType": "str", "Active": True}}
        tblPerson["COMMON NAME"] = {"Excel": {"DataField": "COMMON NAME", "DataColumn": None, "DataType": "str", "Active": True},
                                    "SQL": {"DataField": "Common Name", "DataType": "str", "Active": True}}
        tblPerson["DISPLAY NAME"] = {"Excel": {"DataField": "DISPLAY NAME", "DataColumn": None, "DataType": "str", "Active": True},
                                     "SQL": {"DataField": "Display Name", "DataType": "str", "Active": True}}

        tblPerson["INITIALS"] = {"Excel": {"DataField": "INITIALS", "DataType": "str", "Active": True , "DataColumn": "H",
                                           "Format": "{First Name}[1]{Middle Name}[1]{Last Name}[1]"}}

        tblExcelBook["Person"] = {"Package": "ProjectList", "Format": "Excel", "DataMap": tblPerson,
                                  "UniqueFields": [["FIRST NAME", "LAST NAME"]]}

        # Person Affiliation
        tblPersonAffiliation = {}

        tblPersonAffiliation["PERSON"] = {
            "Excel": {"DataField": "COMMON NAME","DataColumn": None, "FKValue": "{First Name} {Last Name}", "DataType": "str", "Active": True,
                      "FKSheet": "Contact Information", "FKTable": "tbl_ContactList", "FKField": "COMMON NAME",
                      "Key": {"First Name": {"DataField": "FIRST NAME", "DataType": "str"},
                              "Last Name": {"DataField": "LAST NAME", "DataType": "str"}}},
            "SQL": {"DataField": "Person_id", "DataType": "int", "Active": True,
                       "Package": "ProjectList", "FKTable": "Person", "FKField": "id",
                       "Key": {"First Name": {"DataField": "FirstName", "DataType": "str"},
                               "Last Name": {"DataField": "LastName", "DataType": "str"}}}}

        tblPersonAffiliation["Affiliation ID"] = {
            "Excel": {"DataField": "Employee Number", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "Affiliation_id", "DataType": "str", "Active": True}}

        tblPersonAffiliation["ASSOCIATION"] = {
            "Excel": {"DataField": "ASSOCIATION", "DataColumn": None, "FKValue": "{Company Name} ({City})", "DataType": "str", "Active": True,
                      "FKSheet": "Client Information", "FKTable": "tbl_ClientList", "FKField": "Project List Name",
                      "Key": {"Company Name": {"FKField": "Legal Name", "DataType": "str"},
                              "City": {"FKField": "Physical City", "DataType": "str"}}},
            "SQL": {"DataField": "Association", "DataType": "int", "Active": True,
                       "Package": "ProjectList", "FKTable": "Company", "FKField": "id",
                       "Key": {"Company Name": {"DataField": "LegalName", "DataType": "str"},
                               "City": {"DataField": "PhysicalCity", "DataType": "int",
                                        "Package": "ProgramBase", "FKTable": "City", "FKField": "NameText"}}}}

        tblPersonAffiliation["POSITION"] = {
            "Excel": {"DataField": "TITLE",  "DataColumn": None, "DataType": "list", "Active": True,
                      "Key": {"Position": {"DataField": "TITLE", "DataType": "str"}}},
            "SQL": {"DataField": "Position", "DataType": "int", "Active": True,
                       "Package": "ProjectList", "FKTable": "ActivityRole", "FKField": "NameText",
                       "Key": {"Position": {"DataField": "Position", "DataType": "int",
                                            "Package": "ProjectList", "FKTable": "ActivityRole", "FKField": "NameText"}}}}

        tblPersonAffiliation["TERM START"] = {"Excel": {"DataField": "LAST MODIFIED", "DataType": "date", "DataColumn": None},
                                              "SQL": {"DataField": "Start_Date", "DataType": "date",
                                                         "Format": "%B %d, %Y"}}

        alternateentries = {}
        alternateentries["Company"] = []
        alternateentries["Company"].append({"DataField": "Affiliation ID", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "Employee Number", "Active": True})
        alternateentries["Company"].append({"DataField": "ASSOCIATION", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "COMPANY", "Active": True})
        alternateentries["Company"].append({"DataField": "POSITION", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "TITLE", "Active": True})

        alternateentries["CGSB"] = []
        alternateentries["CGSB"].append({"DataField": "Affiliation ID", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "CGSB Number", "Active": True})
        alternateentries["CGSB"].append({"DataField": "ASSOCIATION", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "CGSB", "Active": True})
        alternateentries["CGSB"].append({"DataField": "POSITION", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "CGSB Inspector", "Active": True})

        alternateentries["CWB"] = []
        alternateentries["CWB"].append({"DataField": "Affiliation ID", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "CWB Number", "Active": True})
        alternateentries["CWB"].append({"DataField": "ASSOCIATION", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "CWB", "Active": True})
        alternateentries["CWB"].append({"DataField": "POSITION", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "CWB Inspector", "Active": True})

        alternateentries["JourneymanWelder"] = []
        alternateentries["JourneymanWelder"].append({"DataField": "Affiliation ID", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "Journey Number", "Active": True})
        alternateentries["JourneymanWelder"].append({"DataField": "ASSOCIATION", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "Welding", "Active": True})
        alternateentries["JourneymanWelder"].append({"DataField": "POSITION", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "Welder", "Active": True})

        alternateentries["Engineer - AB"] = []
        alternateentries["Engineer - AB"].append({"DataField": "Affiliation ID", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "APEGA ID", "Active": True})
        alternateentries["Engineer - AB"].append({"DataField": "ASSOCIATION", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "APEGA (Edmonton)", "Active": True})
        alternateentries["Engineer - AB"].append({"DataField": "POSITION", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "APEGA Designation", "Active": True})

        alternateentries["Engineer - BC"] = []
        alternateentries["Engineer - BC"].append({"DataField": "Affiliation ID", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "PEGBC ID", "Active": True})
        alternateentries["Engineer - BC"].append({"DataField": "ASSOCIATION", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "PEGBC (Vancouver)", "Active": True})
        alternateentries["Engineer - BC"].append({"DataField": "POSITION", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "PEGBC Designation", "Active": True})

        alternateentries["Engineer - Sask"] = []
        alternateentries["Engineer - Sask"].append({"DataField": "Affiliation ID", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "PEGSASK ID", "Active": True})
        alternateentries["Engineer - Sask"].append({"DataField": "ASSOCIATION", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "PEGSASK (Regina)", "Active": True})
        alternateentries["Engineer - Sask"].append({"DataField": "POSITION", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "PEGSASK Designation", "Active": True})

        tblExcelBook["PersonAffiliation"] = {"Package": "ProjectList", "DataMap": tblPersonAffiliation,
                                             "AdditionalEntries": alternateentries,
                                             "UniqueFields": [["PERSON", "ASSOCIATION"]],
                                             "ListFields": ["POSITION"]}

        # Person Contact
        tblContactDirectory = {}
        tblContactDirectory["PERSON"] = {
            "Excel": {"DataField": "COMMON NAME", "DataColumn": None, "FKValue": "{First Name} {Last Name}", "DataType": "str", "Active": True,
                      "FKSheet": "Contact Information", "FKTable": "tbl_ContactList", "FKField": "COMMON NAME",
                      "Key": {"First Name": {"FKField": "FIRST NAME", "DataType": "str"},
                              "Last Name": {"FKField": "LAST NAME", "DataType": "str"}}},
            "SQL": {"DataField": "Person_id", "DataType": "int", "Active": True,
                    "Package": "ProjectList", "FKTable": "Person", "FKField": "id",
                    "Key": {"First Name": {"DataField": "FirstName", "DataType": "str"},
                            "Last Name": {"DataField": "LastName", "DataType": "str"}}}}

        tblContactDirectory["CONTACT TYPE"] = {
            "Excel": {"DataField": "CONTACT TYPE", "Value": "Email", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "ContactType", "DataType": "int", "Active": True,
                    "Package": "ProjectList", "FKTable": "ContactType", "FKField": "id",
                    "Key": {"ContactType": {"DataField": "Email", "DataType": "int",
                                            "Package": "ProjectList", "FKTable": "ContactType", "FKField": "NameText"}}}}

        tblContactDirectory["CONTACT ID"] = {"Excel": {"DataField": "EMAIL", "DataColumn": None, "DataType": "str", "Active": True},
                                             "SQL": {"DataField": "Contact_id", "DataType": "str", "Active": True}}

        tblContactDirectory["CONTACT NAME"] = {"Excel": {"DataField": "COMMON NAME", "DataColumn": None, "DataType": "str", "Active": True},
                                               "SQL": {"DataField": "Contact_Name", "DataType": "str", "Active": True}}

        tblContactDirectory["ACTIVE DATE"] = {
            "Excel": {"DataField": "StartDate", "Value": "currentDateTime", "DataType": "date", "DataColumn": None, "Active": True},
            "SQL": {"DataField": "Start_Date", "DataType": "date", "Format": "%B %d, %Y", "Active": True}}

        tblContactDirectory["ACTIVE"] = {
            "Excel": {"DataField": "Active", "Value": True, "DataType": "boolean", "DataColumn": None, "Active": True},
            "SQL": {"DataField": "Active", "DataType": "boolean", "Active": True}}

        tblContactDirectory["PREFERRED"] = {
            "Excel": {"DataField": "Preferred", "Value": True, "DataType": "boolean", "DataColumn": None, "Active": True},
            "SQL": {"DataField": "Preferred", "DataType": "boolean", "Active": True}}

        # tblContactDirectory["INACTIVE DATE"] = {"Excel": {"DataField": "DATE", "DataType": "date", "DataColumn": None},
        #                          "SQL": {"DataField": "Start_Date", "DataType": "date", "Format": "%B %d, %Y"}}

        alternateentries2 = {}
        alternateentries2["Email"] = []
        alternateentries2["Email"].append({"DataField": "CONTACT TYPE", "DataSource": "Excel", "ItemName": "Value", "ItemValue": "Email", "Active": True})
        alternateentries2["Email"].append({"DataField": "CONTACT TYPE", "DataSource": "SQL", "KeyField": "ContactType", "ItemName": "DataField", "ItemValue": "Email", "Active": True})
        alternateentries2["Email"].append({"DataField": "CONTACT ID", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "EMAIL", "Active": True})
        #alternateentries2["Email"].append({"DataField": "CONTACT ID", "DataSource": "SQL", "KeyField": "Contact_id", "ItemName": "Value", "ItemValue": "EMAIL"})

        alternateentries2["Mobile"] = []
        alternateentries2["Mobile"].append({"DataField": "CONTACT TYPE", "DataSource": "Excel", "ItemName": "Value", "ItemValue": "Mobile Phone", "Active": True})
        alternateentries2["Mobile"].append({"DataField": "CONTACT TYPE", "DataSource": "SQL", "KeyField": "ContactType", "ItemName": "DataField", "ItemValue": "Mobile Phone", "Active": True})
        alternateentries2["Mobile"].append({"DataField": "CONTACT ID", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "MOBILE PHONE", "Active": True})
        #alternateentries2["Mobile"].append({"DataField": "CONTACT ID", "DataSource": "SQL", "KeyField": "Contact_id", "ItemName": "Value", "ItemValue": "Mobile Phone"})


        tblExcelBook["PersonContact"] = {"Package": "ProjectList", "DataMap": tblContactDirectory,
                                         "AdditionalEntries": alternateentries2,
                                         "UniqueFields": [["PERSON", "CONTACT TYPE", "CONTACT ID"]]}

        # Training
        tblTraining = {}
        tblTraining["PERSON"] = {
            "Excel": {"DataField": "COMMON NAME", "DataColumn": None, "FKValue": "{First Name} {Last Name}", "DataType": "str", "Active": True,
                      "FKSheet": "Contact Information", "FKTable": "tbl_ContactList", "FKField": "COMMON NAME",
                      "Key": {"First Name": {"DataField": "First Name", "DataType": "str"},
                              "Last Name": {"DataField": "Last Name", "DataType": "str"}}},
            "SQL": {"DataField": "ClientContact", "DataType": "int", "Active": True,
                    "Package": "ProjectList", "FKTable": "Person", "FKField": "id",
                    "Key": {"First Name": {"DataField": "FirstName", "DataType": "str"},
                            "Last Name": {"DataField": "LastName", "DataType": "str"}}}}

        tblTraining["INSTITUTION"] = {
            "Excel": {"DataField": "COMMON NAME", "DataColumn": None, "FKValue": "{Company Name} ({City})", "DataType": "str", "Active": True, "Sheet": "Client Information", "FKTable": "tbl_ClientList", "FKField": "Project List Name",
                      "Key": {
                          "Company Name": {"DataField": "Legal Name", "DataType": "str"},
                          "City": {"DataField": "Physical City", "DataType": "str"}}},
            "SQL": {"DataField": "Owner", "DataType": "int", "Active": True,
                    "Package": "ProjectList", "FKTable": "Company", "FKField": "id",
                    "Key": {"Company Name": {"DataField": "LegalName", "DataType": "str"},
                            "City": {"DataField": "PhysicalCity", "DataType": "int", "Package": "ProgramBase", "FKTable": "City",
                                        "FKField": "NameText"}}}}

        tblTraining["PROFESSIONAL TITLE"] = {
            "Excel": {"DataField": "PROFESSIONAL TITLE", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "Owner", "DataType": "int", "Active": True,
                    "Package": "ProjectList", "FKTable": "Company", "FKField": "id",
                    "Key": {"Company Name": {"DataField": "LegalName", "DataType": "str"},
                            "City": {"DataField": "PhysicalCity", "DataType": "int", "Package": "ProgramBase", "FKTable": "City",
                                    "FKField": "NameText"}}}}

        tblTraining["Inspection Credential"] = {
            "Excel": {"DataField": "Inspection Credential", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "Capacity", "Active": True}}

        alternateentries = {}
        alternateentries["CGSB MPI"] = []
        alternateentries["CGSB MPI"].append({"DataField": "TrainingInstitute", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "CGSB", "Active": True})
        alternateentries["CGSB MPI"].append({"DataField": "Course", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "CGSB Magentic Partical Inspection", "Active": True})
        alternateentries["CGSB MPI"].append({"DataField": "Level", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "CGSB Number", "Active": True})

        alternateentries["CGSB LPI"] = []
        alternateentries["CGSB LPI"].append({"DataField": "TrainingInstitute", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "CGSB Number", "Active": True})
        alternateentries["CGSB LPI"].append({"DataField": "Course", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "CGSB Number", "Active": True})
        alternateentries["CGSB LPI"].append({"DataField": "Level", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "CGSB Number", "Active": True})

        alternateentries["CGSB UT"] = []
        alternateentries["CGSB UT"].append({"DataField": "TrainingInstitute", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "CGSB Number", "Active": True})
        alternateentries["CGSB UT"].append({"DataField": "Course", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "CGSB Number", "Active": True})
        alternateentries["CGSB UT"].append({"DataField": "Level", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "CGSB Number", "Active": True})

        alternateentries["CWB VISUAL"] = []
        alternateentries["CWB VISUAL"].append({"DataField": "TrainingInstitute", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "CGSB Number", "Active": True})
        alternateentries["CWB VISUAL"].append({"DataField": "Course", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "CGSB Number", "Active": True})
        alternateentries["CWB VISUAL"].append({"DataField": "Level", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "CGSB Number", "Active": True})

        alternateentries["P.Eng. AB"] = []
        alternateentries["P.Eng. AB"].append({"DataField": "TrainingInstitute", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "CGSB Number", "Active": True})
        alternateentries["P.Eng. AB"].append({"DataField": "Course", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "CGSB Number", "Active": True})

        alternateentries["P.Eng. BC"] = []
        alternateentries["P.Eng. BC"].append({"DataField": "TrainingInstitute", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "CGSB Number", "Active": True})
        alternateentries["P.Eng. BC"].append({"DataField": "Course", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "CGSB Number", "Active": True})


        tblExcelBook["Training"] = {"Package": "ProjectList", "DataMap": tblTraining, "UniqueFields": [[]]}

        tblInspection = {}
        tblInspection["CERT PERIOD"] = {
            "Excel": {"DataField": "CERT PERIOD", "DataType": "int", "DataColumn": None, "Active": True},
            "SQL": {"DataField": "Equipment", "DataType": "int", "DataColumn": None, "Active": True}}

        tblInspection["DAYS TO EXPIRY"] = {
            "Excel": {"DataField": "DATS TO EXPIRY", "DataType": "int", "DataColumn": "AM",
                      "Formula": "=EDATE([@DATE],[@[CERT PERIOD]])-NOW()", "Format": "DDMMYYYY", "Active": True},
            "SQL": {"DataField": "Equipment", "DataType": "int", "DataColumn": None, "Active": True}}

        tblExcelBook["Inspection"] = {"Package": "ProjectList", "DataMap": tblInspection, "UniqueFields": [[]]}

        tblWorkOrder = {}

        tblWorkOrder["Project"] = {
            "Excel": {"DataField": "PROJECT NUMBER", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "Project_id", "Package": "ProjectList", "FKTable": "Project", "FKField": "Project Number", "DataType": "int", "Active": True,
                    "Key": {"Project Number": {"DataField": "Project_id", "DataType": "int",
                                               "Package": "ProjectList", "FKTable": "Project", "FKField": "ProjectNumber"}}}}

        tblWorkOrder["Work Order"] = {
            "Excel": {"DataField": "PROJECT NUMBER", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "WorkOrder", "DataType": "str", "Active": True, "Package": "ProjectList"}}

        tblWorkOrder["IssuedBy"] = {
            "Excel": {"DataField": "SUPERVISOR", "DataColumn": None, "FKValue": "{First Name} {Last Name}", "DataType": "str", "Active": True,
                      "FKSheet": "Contact Information", "FKTable": "tbl_ContactList", "FKField": "COMMON NAME",
                      "Key": {"First Name": {"FKField": "FIRST NAME", "DataType": "str"},
                              "Last Name": {"FKField": "LAST NAME", "DataType": "str"}}},
            "SQL": {"DataField": "IssuedBy", "DataType": "int", "Active": True,
                       "Package": "ProjectList", "FKTable": "Person", "FKField": "id",
                       "Key": {"First Name": {"DataField": "FirstName", "DataType": "str"},
                               "Last Name": {"DataField": "LastName", "DataType": "str"}}}}

        tblWorkOrder["IssuedTo"] = {
            "Excel": {"DataField": "CLIENT CONTACT", "DataColumn": None, "FKValue": "{First Name} {Last Name}", "DataType": "str", "Active": True,
                      "FKSheet": "Contact Information", "FKTable": "tbl_ContactList", "FKField": "COMMON NAME",
                      "Key": {"First Name": {"FKField": "FIRST NAME", "DataType": "str"},
                              "Last Name": {"FKField": "LAST NAME", "DataType": "str"}}},
            "SQL": {"DataField": "IssuedTo", "DataType": "int", "Active": True,
                       "Package": "ProjectList", "FKTable": "Person", "FKField": "id",
                       "Key": {"First Name": {"DataField": "FirstName", "DataType": "str"},
                               "Last Name": {"DataField": "LastName", "DataType": "str"}}}}

        tblWorkOrder["Work Description"] = {
            "Excel": {"DataField": "PROJECT TITLE", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "WorkDescription", "DataType": "str", "Active": True}}

        tblWorkOrder["Location"] = {
            "Excel": {"DataField": "LOCATION", "DataColumn": None, "DataType": "str", "Active": True,
                      "Key": {"Location": {"DataField": "LOCATION", "DataType": "str"}}},
            "SQL": {"DataField": "WorkLocation", "DataType": "int", "Active": True,
                       "Package": "ProgramBase", "FKTable": "City", "FKField": "NameText",
                       "Key": {"Location": {"DataField": "WorkLocation", "DataType": "int",
                                            "Package": "ProgramBase", "FKTable": "City", "FKField": "NameText"}}}}

        tblWorkOrder["Work Order Status"] = {
            "Excel": {"DataField": "STATUS", "DataColumn": None, "DataType": "str", "Active": True,
                      "Key": {"WorkOrderStatus": {"DataField": "STATUS", "DataType": "str"}}},
            "SQL": {"DataField": "WorkOrderStatus", "Package": "ProjectList",
                       "FKTable": "ProjectStatus", "FKField": "NameText", "DataType": "int", "Active": True,
                       "Key": {"Status": {"DataField": "WorkOrderStatus", "DataType": "int",
                                          "Package": "ProjectList", "FKTable": "ProjectStatus", "FKField": "NameText"}}}}

        tblExcelBook["Work Order"] = {"Package": "ProjectList", "DataMap": tblWorkOrder,
                                      "UniqueFields": [["Work Order"]]}

        tblWorkOrderItems = {}
        tblWorkOrderItems["Work Order"] = {
            "Excel": {"DataField": "PROJECT NUMBER", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "WorkOrder_id", "Package": "ProjectList", "FKTable": "Project", "FKField": "ProjectNumber", "DataType": "int", "Active": True,
                       "Key": {"WorkOrder_id": {"DataField": "WorkOrder_id", "DataType": "int",
                                                "Package": "ProjectList", "FKTable": "Project", "FKField": "ProjectNumber"}}}}

        tblContactDirectory["Item Date"] = {
            "Excel": {"DataField": "StartDate", "DataType": "date", "DataColumn": None, "Active": True},
            "SQL": {"DataField": "ItemDate", "DataType": "date", "Format": "%B %d, %Y", "Active": True}}

        tblWorkOrderItems["Item Description"] = {
            "Excel": {"Value": "Travel Distance Rate", "DataColumn": None, "DataType": "str", "Active": True},
            "SQL": {"DataField": "ItemDescription", "DataType": "str", "Active": True}}

        tblWorkOrderItems["Item Quantity"] = {
            "Excel": {"DataField": "TRAVEL KM", "DataColumn": None, "DataType": "flt", "Active": True},
            "SQL": {"DataField": "ItemQuantity", "DataType": "flt", "Active": True}}

        tblWorkOrderItems["Item Quantity Unit"] = {
            "Excel": {"DataField": "Unit", "Value": "km", "DataColumn": None, "DataType": "str", "Active": True,
                      "Key": {"Unit Type": {"Value": "Currency", "DataType": "int", "KeyType": "Reference"}}},
            "SQL": {"DataField": "ItemQuantityUnits", "Package": "ProgramBase", "FKTable": "Unit", "FKField": "id", "DataType": "int", "Active": True,
                       "Key": {"ItemQuantityUnits": {"DataField": "ItemQuantityUnits", "DataType": "int", "Package": "ProgramBase",
                                                     "FKTable": "Unit", "FKField": "NameText",
                                                     "Key": {"Unit Type": {"DataField": "UnitType", "DataType": "int", "Package": "ProgramBase",
                                                                           "FKTable": "UnitType", "FKField": "NameText", "KeyType": "Reference"}}}}}}

        tblWorkOrderItems["Item Rate"] = {
            "Excel": {"DataField": "TRAVEL KM RATE", "DataColumn": None, "DataType": "flt", "Active": True},
            "SQL": {"DataField": "ItemRate", "DataType": "flt", "Active": True}}

        tblWorkOrderItems["Item Rate Unit"] = {
            "Excel": {"DataField": "Unit", "Value": "$/km", "DataColumn": None, "DataType": "str", "Active": True,
                      "Key": {"Unit Type": {"Value": "Currency", "DataType": "int", "KeyType": "Reference"}}},
            "SQL": {"DataField": "ItemRateUnits", "Package": "ProgramBase", "FKTable": "Unit", "FKField": "id", "DataType": "int", "Active": True,
                       "Key": {"ItemRateUnits": {"DataField": "ItemRateUnits", "DataType": "int", "Package": "ProgramBase",
                                                 "FKTable": "Unit", "FKField": "NameText",
                                                 "Key": {"Unit Type": {"DataField": "UnitType", "DataType": "int", "Package": "ProgramBase",
                                                                       "FKTable": "UnitType", "FKField": "NameText", "KeyType": "Reference"}}}}}}

        tblWorkOrderItems["Item Amount"] = {
            "Excel": {"DataField": None, "DataColumn": None, "DataType": None, "Active": False},
            "SQL": {"DataField": "ItemAmount", "Value": "={ItemQuantity}*{ItemRate}", "DataType": "flt", "Active": True}}

        tblWorkOrderItems["Item Currency"] = {
            "Excel": {"DataField": "Currency", "DataColumn": None, "DataType": "str", "Active": True, "Value": "CAD",
                      "Key": {"Country": {"DataField": "COUNTRY", "DataColumn": None, "DataType": "str"}}},
            "SQL": {"DataField": "Currency", "Package": "ProjectList", "FKTable": "Currency", "FKField": "NameText", "DataType": "int", "Active": True,
                       "Key": {"Country": {"DataField": "Country", "DataType": "int",
                                           "Package": "ProgramBase", "FKTable": "Country", "FKField": "NameText"}}}}

        tblWorkOrderItems["Location Tax"] = {
            "Excel": {"DataField": "PROVINCIAL TAX", "DataColumn": None, "DataType": "flt", "Active": True,
                      "Key": {"Location": {"DataField": "PROVINCE", "DataType": "str"},
                              "Tax": {"DataField": "PROVINCIAL TAX", "DataType": "flt"},
                              "StartDate": {"DataField": "DATE", "DataType": "date", "KeyType": "Reference"}}},
            "SQL": {"DataField": "Tax", "Package": "ProjectList", "Value": "[{Location}: {Tax}]", "DataType": "list", "Active": True,
                       "Key": {"Location": {"DataField": "Country", "DataType": "int",
                                            "Package": "ProgramBase", "FKTable": "Province", "FKField": "NameText"},
                               "StartDate": {"DataField": "ItemDate", "DataType": "date", "KeyType": "Reference", "Format": "%B %d, %Y"}}}}

        tblWorkOrderItems["Federal Tax"] = {
            "Excel": {"DataField": "FEDERAL TAX", "DataColumn": None, "DataType": "flt", "Active": True,
                      "Key": {"Location": {"Value": "Canada", "DataType": "str"},
                              "Tax": {"DataField": "FEDERAL TAX", "DataType": "flt"},
                              "StartDate": {"DataField": "DATE", "DataType": "date", "KeyType": "Reference"}}},
            "SQL": {"DataField": "Tax", "Package": "ProjectList", "Value": "[{Location}: {Tax}]", "DataType": "list", "Active": True,
                       "Key": {"Location": {"DataField": "Country", "DataType": "int",
                                            "Package": "ProgramBase", "FKTable": "Country", "FKField": "NameText"},
                               "StartDate": {"DataField": "ItemDate", "DataType": "date", "KeyType": "Reference", "Format": "%B %d, %Y"}}}}

        tblWorkOrderItems["ItemStatus"] = {
            "Excel": {"DataField": "Status", "DataColumn": None, "DataType": "str", "Active": True, "Value": "Active"},
            "SQL": {"DataField": "ItemStatus", "Package": "ProjectList", "FKTable": "WorkOrderItemStatus", "FKField": "NameText", "DataType": "int", "Active": True,
                       "Key": {"ItemStatus": {"DataField": "ItemStatus", "DataType": "int",
                                               "Package": "ProjectList", "FKTable": "WorkOrderItemStatus", "FKField": "NameText"}}}}

        alternateentries = {}
        alternateentries["TravelKM"] = []
        alternateentries["TravelKM"].append({"DataField": "Item Description", "DataSource": "Excel", "ItemName": "Value", "ItemValue": "TRAVEL KM", "Active": True})
        alternateentries["TravelKM"].append({"DataField": "Item Quantity", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "TRAVEL KM", "Active": True})
        alternateentries["TravelKM"].append({"DataField": "Item Quantity Unit", "DataSource": "Excel", "ItemName": "Value", "ItemValue": "km", "Active": True})
        alternateentries["TravelKM"].append({"DataField": "Item Rate", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "TRAVEL KM RATE", "Active": True})
        alternateentries["TravelKM"].append({"DataField": "Item Rate Unit", "DataSource": "Excel", "ItemName": "Value", "ItemValue": "$/km", "Active": True})
        alternateentries["TravelKM"].append({"DataField": "Item Amount", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": None, "Active": False})
        alternateentries["TravelKM"].append({"DataField": "Item Amount", "DataSource": "SQL", "ItemName": "Value", "ItemValue": "={ItemQuantity}*{ItemRate}", "Active": True})

        alternateentries["TravelHR"] = []
        alternateentries["TravelHR"].append({"DataField": "Item Description", "DataSource": "Excel", "ItemName": "Value", "ItemValue": "TRAVEL HR", "Active": True})
        alternateentries["TravelHR"].append({"DataField": "Item Quantity", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "TRAVEL HR", "Active": True})
        alternateentries["TravelHR"].append({"DataField": "Item Quantity Unit", "DataSource": "Excel", "ItemName": "Value", "ItemValue": "hr", "Active": True})
        alternateentries["TravelHR"].append({"DataField": "Item Rate", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "TRAVEL HR RATE", "Active": True})
        alternateentries["TravelHR"].append({"DataField": "Item Rate Unit", "DataSource": "Excel", "ItemName": "Value", "ItemValue": "$/hr", "Active": True})
        alternateentries["TravelHR"].append({"DataField": "Item Amount", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": None, "Active": False})
        alternateentries["TravelHR"].append({"DataField": "Item Amount", "DataSource": "SQL", "ItemName": "Value", "ItemValue": "={ItemQuantity}*{ItemRate}", "Active": True})

        alternateentries["Technician"] = []
        alternateentries["Technician"].append({"DataField": "Item Description", "DataSource": "Excel", "ItemName": "Value", "ItemValue": "TECHNICIAN", "Active": True})
        alternateentries["Technician"].append({"DataField": "Item Quantity", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "TECHNICIAN QTY", "Active": True})
        alternateentries["Technician"].append({"DataField": "Item Quantity Unit", "DataSource": "Excel", "ItemName": "Value", "ItemValue": "hr", "Active": True})
        alternateentries["Technician"].append({"DataField": "Item Rate", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "TECHNICIAN RATE", "Active": True})
        alternateentries["Technician"].append({"DataField": "Item Rate Unit", "DataSource": "Excel", "ItemName": "Value", "ItemValue": "$/hr", "Active": True})
        alternateentries["Technician"].append({"DataField": "Item Amount", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": None, "Active": False})
        alternateentries["Technician"].append({"DataField": "Item Amount", "DataSource": "SQL", "ItemName": "Value", "ItemValue": "={ItemQuantity}*{ItemRate}", "Active": True})

        alternateentries["Engineer"] = []
        alternateentries["Engineer"].append({"DataField": "Item Description", "DataSource": "Excel", "ItemName": "Value", "ItemValue": "ENGINEER", "Active": True})
        alternateentries["Engineer"].append({"DataField": "Item Quantity", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "ENGINEER QTY", "Active": True})
        alternateentries["Engineer"].append({"DataField": "Item Quantity Unit", "DataSource": "Excel", "ItemName": "Value", "ItemValue": "hr", "Active": True})
        alternateentries["Engineer"].append({"DataField": "Item Rate", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "ENGINEER RATE", "Active": True})
        alternateentries["Engineer"].append({"DataField": "Item Rate Unit", "DataSource": "Excel", "ItemName": "Value", "ItemValue": "$/hr", "Active": True})
        alternateentries["Engineer"].append({"DataField": "Item Amount", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": None, "Active": False})
        alternateentries["Engineer"].append({"DataField": "Item Amount", "DataSource": "SQL", "ItemName": "Value", "ItemValue": "={ItemQuantity}*{ItemRate}", "Active": True})

        alternateentries["Repairs"] = []
        alternateentries["Repairs"].append({"DataField": "Item Description", "DataSource": "Excel", "ItemName": "Value", "ItemValue": "REPAIR PROCEDURE", "Active": True})
        alternateentries["Repairs"].append({"DataField": "Item Quantity", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": None, "Active": False})
        alternateentries["Repairs"].append({"DataField": "Item Quantity Unit", "DataSource": "Excel", "ItemName": "Value", "ItemValue": None, "Active": False})
        alternateentries["Repairs"].append({"DataField": "Item Rate", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": None, "Active": False})
        alternateentries["Repairs"].append({"DataField": "Item Rate Unit", "DataSource": "Excel", "ItemName": "Value", "ItemValue": None, "Active": False})
        alternateentries["Repairs"].append({"DataField": "Item Amount", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "REPAIR PROCEDURE2", "Active": True})
        alternateentries["Repairs"].append({"DataField": "Item Amount", "DataSource": "SQL", "ItemName": "DataField", "ItemValue": None, "Active": False})

        alternateentries["Inspection Certification"] = []
        alternateentries["Inspection Certification"].append({"DataField": "Item Description", "DataSource": "Excel", "ItemName": "Value", "ItemValue": "TRAVEL KM", "Active": True})
        alternateentries["Inspection Certification"].append({"DataField": "Item Quantity", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": None, "Active": False})
        alternateentries["Inspection Certification"].append({"DataField": "Item Quantity Unit", "DataSource": "Excel", "ItemName": "Value", "ItemValue": None, "Active": False})
        alternateentries["Inspection Certification"].append({"DataField": "Item Rate", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": None, "Active": False})
        alternateentries["Inspection Certification"].append({"DataField": "Item Rate Unit", "DataSource": "Excel", "ItemName": "Value", "ItemValue": None, "Active": False})
        alternateentries["Inspection Certification"].append({"DataField": "Item Amount", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "INSPECTION CERTIFICATION", "Active": True})
        alternateentries["Inspection Certification"].append({"DataField": "Item Amount", "DataSource": "SQL", "ItemName": "DataField", "ItemValue": None, "Active": False})

        alternateentries["Accommodation"] = []
        alternateentries["Accommodation"].append({"DataField": "Item Description", "DataSource": "Excel", "ItemName": "Value", "ItemValue": "ACCOMMODATIONS", "Active": True})
        alternateentries["Accommodation"].append({"DataField": "Item Quantity", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "ACCOMMODATIONS QTY", "Active": True})
        alternateentries["Accommodation"].append({"DataField": "Item Quantity Unit", "DataSource": "Excel", "ItemName": "Value", "ItemValue": "$", "Active": True})
        alternateentries["Accommodation"].append({"DataField": "Item Rate", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "ACCOMMODATIONS RATE", "Active": True})
        alternateentries["Accommodation"].append({"DataField": "Item Rate Unit", "DataSource": "Excel", "ItemName": "ItemValue", "ItemValue": "$/day", "Active": True})
        alternateentries["Accommodation"].append({"DataField": "Item Amount", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": None, "Active": False})
        alternateentries["Accommodation"].append({"DataField": "Item Amount", "DataSource": "SQL", "ItemName": "Value", "ItemValue": "={ItemQuantity}*{ItemRate}", "Active": True})

        alternateentries["Substance"] = []
        alternateentries["Substance"].append({"DataField": "Item Description", "DataSource": "Excel", "ItemName": "Value", "ItemValue": "SUBSISTENCE", "Active": True})
        alternateentries["Substance"].append({"DataField": "Item Quantity", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "SUBSISTENCE RATE", "Active": True})
        alternateentries["Substance"].append({"DataField": "Item Quantity Unit", "DataSource": "Excel", "ItemName": "Value", "ItemValue": "$/day", "Active": True})
        alternateentries["Substance"].append({"DataField": "Item Rate", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "SUBSISTENCE QTY", "Active": True})
        alternateentries["Substance"].append({"DataField": "Item Rate Unit", "DataSource": "Excel", "ItemName": "Value", "ItemValue": "day", "Active": True})
        alternateentries["Substance"].append({"DataField": "Item Amount", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": None, "Active": False})
        alternateentries["Substance"].append({"DataField": "Item Amount", "DataSource": "SQL", "ItemName": "Value", "ItemValue": "={ItemQuantity}*{ItemRate}", "Active": True})

        alternateentries["Item Charge"] = []
        alternateentries["Item Charge"].append({"DataField": "Item Description", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "OTHER ITEM", "Active": True})
        alternateentries["Item Charge"].append({"DataField": "Item Quantity", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": None, "Active": False})
        alternateentries["Item Charge"].append({"DataField": "Item Quantity Unit", "DataSource": "Excel", "ItemName": "Value", "ItemValue": None, "Active": False})
        alternateentries["Item Charge"].append({"DataField": "Item Rate", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": None, "Active": False})
        alternateentries["Item Charge"].append({"DataField": "Item Rate Unit", "DataSource": "Excel", "ItemName": "Value", "ItemValue": None, "Active": False})
        alternateentries["Item Charge"].append({"DataField": "Item Amount", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "OTHER ITEM VALUE", "Active": True})
        alternateentries["Item Charge"].append({"DataField": "Item Amount", "DataSource": "SQL", "ItemName": "Value", "ItemValue": None, "Active": False})

        alternateentries["Rate Item"] = []
        alternateentries["Rate Item"].append({"DataField": "Item Description", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "SCOPE", "Active": True})
        alternateentries["Rate Item"].append({"DataField": "Item Quantity", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": None, "Active": False})
        alternateentries["Rate Item"].append({"DataField": "Item Quantity Unit", "DataSource": "Excel", "ItemName": "Value", "ItemValue": None, "Active": False})
        alternateentries["Rate Item"].append({"DataField": "Item Rate", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": None, "Active": False})
        alternateentries["Rate Item"].append({"DataField": "Item Rate Unit", "DataSource": "Excel", "ItemName": "Value", "ItemValue": None, "Active": False})
        alternateentries["Rate Item"].append({"DataField": "Item Amount", "DataSource": "Excel", "ItemName": "DataField", "ItemValue": "RATE SHEET", "Active": True})
        alternateentries["Rate Item"].append({"DataField": "Item Amount", "DataSource": "SQL", "ItemName": "Value", "ItemValue": None, "Active": False})


        tblExcelBook["Work Order Items"] = {"Package": "ProjectList", "DataMap": tblWorkOrderItems, "AdditionalEntries": alternateentries,
                                      "UniqueFields": [["Work Order", "Item Description", "Item Quantity", "Item Rate"]]}

        tblInvoice = {}
        tblInvoice["INVOICE TITLE"] = {"Excel": {"DataType": "str", "Active": True, "DataColumn": "AN"},
                                       "SQL": {"Table": "tblProjectList", "Active": True}}
        tblInvoice["INVOICE NUMBER"] = {"Excel": {"DataField": "INVOICE NUMBER", "DataColumn": None, "DataType": "str", "Active": True}}
        tblInvoice["INVOICE DATE"] = {"Excel": {"DataField": "INVOICE DATE", "DataColumn": None, "DataType": "str", "Active": True}}
        tblInvoice["APPROVAL TYPE"] = {"Excel": {"DataField": "APPROVAL TYPE", "DataColumn": None, "DataType": "str", "Active": True}}
        tblInvoice["APPROVAL NUMBER"] = {"Excel": {"DataField": "APPROVAL NUMBER", "DataColumn": None, "DataType": "str", "Active": True}}
        tblInvoice["SUB TOTAL"] = {"Excel": {"DataField": "SUB TOTAL", "DataColumn": None, "DataType": "str", "Active": True}}
        tblInvoice["TAXES"] = {"Excel": {"DataField": "TAXES", "DataColumn": None, "DataType": "str", "Active": True}}
        tblInvoice["TERM"] = {"Excel": {"DataField": "TERM", "DataColumn": None, "DataType": "str", "Active": True}}
        tblInvoice["LAST REMINDER SENT"] = {"Excel": {"DataField": "LAST REMINDER SENT", "DataColumn": None, "DataType": "str", "Active": True}}
        tblInvoice["PAYMENT STATUS"] = {"Excel": {"DataField": "PAYMENT STATUS", "DataColumn": None, "DataType": "str", "Active": True}}
        tblInvoice["DATE PAID"] = {"Excel": {"DataField": "DATE PAID", "DataColumn": None, "DataType": "str", "Active": True}}
        tblExcelBook["Invoice"] = {"Package": "ProjectList", "DataMap": tblInvoice, "UniqueFields": [[]]}

        tlbSoldInvoices = {}
        tblExcelBook["SoldInvoices"] = {"Package": "ProjectList", "DataMap": tlbSoldInvoices, "UniqueFields": [[]]}

        tblRateSheet = {}
        tblRateSheet["PROJECT NUMBER"] = {"Excel": {"DataField": "PROJECT NUMBER", "DataColumn": None, "DataType": "str", "Active": True}}
        tblRateSheet["PROJECT TITLE"] = {"Excel": {"DataField": "PROJECT TITLE", "DataColumn": None, "DataType": "str", "Active": True}}
        tblRateSheet["STATUS"] = {"Excel": {"DataField": "STATUS", "DataColumn": None, "DataType": "str", "Active": True}}
        tblRateSheet["CONSIGNEE"] = {"Excel": {"DataField": "CONSIGNEE", "DataColumn": None, "DataType": "str", "Active": True}}
        tblRateSheet["OWNER"] = {"Excel": {"DataField": "OWNER", "DataColumn": None, "DataType": "str", "Active": True}}
        tblExcelBook["RateSheet"] = {"Package": "ProjectList", "DataMap": tblRateSheet, "UniqueFields": [[]]}
        return tblExcelBook