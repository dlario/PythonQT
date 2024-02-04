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

from sqlalchemy import JSON, Column, DateTime, Integer, String, Boolean

from PackageManager.Packages.ProgramBase.Database.dbBase import MainBase
import datetime


# region Lists
class TableSelectionType(MainBase):
    __tablename__ = 'lsttableselectiontype'
    id = Column(Integer, primary_key=True)
    Name_id = Column(Integer)
    NameText = Column(String(75), unique=True)


class DataType(MainBase):
    __tablename__ = 'lstdatatype'
    id = Column(Integer, primary_key=True)
    Name_id = Column(Integer)
    NameText = Column(String(75), unique=True)


class DataBaseType(MainBase):
    __tablename__ = 'lstdatabasetype'
    id = Column(Integer, primary_key=True)
    Name_id = Column(Integer)
    NameText = Column(String(75), unique=True)
    Syntax = Column(String(255))


class TableType(MainBase):
    __tablename__ = 'lsttabletype'
    id = Column(Integer, primary_key=True)
    Name_id = Column(Integer)
    NameText = Column(String(75), unique=True)


class DatabaseAction(MainBase):
    __tablename__ = 'lstdbaction'
    id = Column(Integer, primary_key=True)
    Name_id = Column(Integer)
    NameText = Column(String(75), unique=True)


class SessionBase(MainBase):
    __tablename__ = 'lstsessionbase'
    id = Column(Integer, primary_key=True)
    NameText = Column(String(75), unique=True)


class SessionNames(MainBase):
    __tablename__ = 'lstsession'
    id = Column(Integer, primary_key=True)
    Name_id = Column(Integer)
    NameText = Column(String(75), unique=True)


# endregion

# region Tables
class Reference(MainBase):
    __tablename__ = 'reference'
    id = Column(Integer, primary_key=True)
    Remote_id = Column(Integer)
    Word = Column(String(75))
    Grammar = Column(String(75))
    Definition = Column(String(255))
    Synonym = Column(String(255))
    Antonym = Column(String(255))
    AlsoKnownAs = Column(String(255))
    Misspelling = Column(String(255))
    PositiveTag = Column(String(255))
    NegativeTag = Column(String(255))

class DataCorrection(MainBase):
    __tablename__ = 'datacorrection'
    id = Column(Integer, primary_key=True)
    OriginalMasterTable_id = Column(Integer)
    OriginalRecord_id = Column(Integer)
    CorrectedMasterTable_id = Column(Integer)
    CorrectedRecord_id = Column(Integer)
    Date_Created = Column(DateTime, default=datetime.datetime.now())
    Date_Modified = Column(DateTime, default=datetime.datetime.now())
    Date_Accessed = Column(DateTime, default=datetime.datetime.now())


class SyncRules(MainBase):
    __tablename__ = 'syncrules'
    id = Column(Integer, primary_key=True)
    ptable_id = Column(Integer)
    pfield_id = Column(Integer)
    ctable_id = Column(Integer)
    cfield_id = Column(Integer)


class FieldKeyRegistry(MainBase):
    __tablename__ = 'fieldkeyregistry'
    id = Column(Integer, primary_key=True)
    table_id = Column(Integer)
    field_id = Column(Integer)
    client_id = Column(Integer)
    cfield_id = Column(Integer)


class ForeignKeyRegistry(MainBase):
    __tablename__ = 'foreignkeyregistry'
    id = Column(Integer, primary_key=True)
    ptable_id = Column(Integer)
    pfield_id = Column(Integer)
    ctable_id = Column(Integer)
    cfield_id = Column(Integer)


# region Base
class BaseInformation(MainBase):
    __tablename__ = 'baseinformation'
    id = Column(Integer, primary_key=True)
    Name = Column(String(255))
    AbstractView = Column(String(255))
    TableArgs = Column(String(255))
    MetaData = Column(String(255))


class BaseDefaultFields(MainBase):
    __tablename__ = 'basedefaultfields'
    id = Column(Integer, primary_key=True)
    Name = Column(String(255))
    DataType = Column(String(255))
    DataTypeValue = Column(String(255))


class SessionInformation(MainBase):
    __tablename__ = 'sessioninformation'
    id = Column(Integer, primary_key=True)
    SessionName = Column(String(255))
    DatabaseType = Column(Integer)
    Address = Column(String(255))
    Port = Column(Integer)
    Login = Column(String(255))
    Password = Column(String(255))
    Schema = Column(String(255))
    LBP = Column(Integer)


class SSHTunnelForwarder(MainBase):
    __tablename__ = 'sshtunnelforwarder'
    id = Column(Integer, primary_key=True)
    Address = Column(String(255))
    Port = Column(Integer)
    Login = Column(String(255))
    Password = Column(String(255))


class ExcelTable(MainBase):
    __tablename__ = 'exceltable'
    id = Column(Integer, primary_key=True)
    MasterTable_id = Column(Integer)
    NameText = Column(String(75), unique=True)
    WorkBook = Column(String(255))
    Sheet = Column(String(255))
    HeaderRow = Column(Integer)
    StartRow = Column(Integer)
    StartColumn = Column(Integer)


class MasterTable(MainBase):
    __tablename__ = 'mastertable'
    id = Column(Integer, primary_key=True)
    TableType_id = Column(Integer)  # , ForeignKey('lstdatatype.id'))
    Name_id = Column(Integer)  # , ForeignKey('reference.id'))
    NameText = Column(String(75), unique=True)
    Name = Column(String(255))  # relationship('Reference')
    Package = Column(String(75))
    File = Column(String(75))
    DataSourceFormat = Column(String(75))
    ClassName = Column(String(75))
    TableName = Column(String(75))
    DisplayColumn = Column(String(75))
    DisplayQuery = Column(String(255))
    DataQuery = Column(String(255))
    Description = Column(String(255))
    PrimaryKey = Column(String(25))
    Tags = Column(String(500))
    Active = Column(Boolean, unique=False, default=True)
    Date_Modified = Column(DateTime, default=datetime.datetime.now())
    Date_Accessed = Column(DateTime, default=datetime.datetime.now())


class FieldTable(MainBase):
    __tablename__ = 'fieldtable'
    id = Column(Integer, primary_key=True)
    Table_id = Column(Integer)
    Name_id = Column(Integer)
    NameText = Column(String(75))
    DataType_id = Column(Integer)
    DataType_Value = Column(String(255))
    PrimaryKey = Column(Integer)
    NotNull = Column(Integer)
    Unique = Column(Integer)
    Binary = Column(Integer)
    ZeroFill = Column(Integer)
    GeneratedColumn = Column(Integer)
    DefaultExpression = Column(String(255))
    Description = Column(String(255))
    ForeignKey = Column(String(255))
    Tags = Column(String(500))
    Active = Column(Boolean, unique=False, default=True)
    Date_Modified = Column(DateTime, default=datetime.datetime.now())
    Date_Accessed = Column(DateTime, default=datetime.datetime.now())

class DataMap(MainBase):
    __tablename__ = 'datamap'
    id = Column(Integer, primary_key=True)
    Parent_id = Column(Integer)
    Name = Column(String(255))
    DataField = Column(String(255))
    DataColumn = Column(Integer)
    DataType = Column(Integer)
    FKSheet = Column(String(255))
    FKTable = Column(String(255))
    FKField = Column(String(255))
    Active = Column(Boolean, unique=False, default=True)

class SyncOrder(MainBase):
    __tablename__ = 'syncorder'
    id = Column(Integer, primary_key=True)
    source_id = Column(Integer)
    destination_id = Column(Integer)
    table_id = Column(Integer)
    order = Column(Integer)


class SyncLog(MainBase):
    __tablename__ = 'synclog'
    id = Column(Integer, primary_key=True)
    sourceTable = Column(Integer)
    destinationTable = Column(Integer)
    SyncTableRowStart = Column(Integer)
    SyncTableRowEnd = Column(Integer)
    SyncDate = Column(DateTime, default=datetime.datetime.now())


class DataSyncRecords(MainBase):
    __tablename__ = 'datasyncrecords'
    id = Column(Integer, primary_key=True)
    DataSync_id = Column(Integer)
    OriginalValue = Column(String(255))
    NewValue = Column(String(255))
    Status = Column(Integer)
    Date_Created = Column(DateTime, default=datetime.datetime.now())
    Date_Modified = Column(DateTime, default=datetime.datetime.now())
    Date_Accessed = Column(DateTime, default=datetime.datetime.now())


class SyncJournal(MainBase):
    __tablename__ = 'syncjournal'
    id = Column(Integer, primary_key=True)
    action = Column(Integer)
    source = Column(String(50))
    recordJson = Column(JSON)
    syncStatus = Column(JSON)
    tagJSON = Column(JSON)
    Date_Created = Column(DateTime, default=datetime.datetime.now())


class DataSyncStatements(MainBase):
    __tablename__ = 'datasyncstatements'
    id = Column(Integer, primary_key=True)
    Source_id = Column(Integer)
    DataSync_id = Column(Integer)
    Table_id = Column(Integer)
    ItemList = Column(String(255))
    ValueList = Column(String(255))
    QueryString = Column(String(255))
    SyncTags = Column(String(255))
    JTags = Column(JSON)
    Date_Created = Column(DateTime, default=datetime.datetime.now())


class BulkUpdate(MainBase):
    __tablename__ = 'bulkupdate'
    id = Column(Integer, primary_key=True)
    Table_id = Column(Integer)
    Description = Column(String(255))


class BulkUpdateAffectedTable(MainBase):
    __tablename__ = 'bulkupdateaffectedtable'
    id = Column(Integer, primary_key=True)
    DST = Column(Integer)
    Table_id = Column(Integer)
    ColumnName = Column(String(255))


class DynamicRecordUpdate(MainBase):
    __tablename__ = 'dynamicrecordupdate'
    id = Column(Integer, primary_key=True)
    Table_id = Column(Integer)
    Column_id = Column(Integer)
    OldRecord_id = Column(Integer)
    OldTag_id = Column(Integer)
    NewRecord_id = Column(Integer)
    NewTag_id = Column(Integer)
