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

from sqlalchemy.orm import relationship, backref
from sqlalchemy import Table, Column, DateTime, Integer, DECIMAL, String, Text, Date, Boolean, Numeric, MetaData, ForeignKey, \
    create_engine

from PackageManager.Packages.ProgramBase.Database.dbBase import MainBase
import datetime

# region AddOn
class AddonPrograms(MainBase):
    __tablename__ = 'addonprograms'
    id = Column(Integer, primary_key=True)
    ProgramName = Column(String(255))


class AddonProgramsClasses(MainBase):
    __tablename__ = 'addonprogramsclasses'
    id = Column(Integer, primary_key=True)
    Program_id = Column(Integer)
    ProgramName = Column(String(255))


class AddonProgramsClassesUsed(MainBase):
    __tablename__ = 'addonprogramsclassesused'
    id = Column(Integer, primary_key=True)
    Program_id = Column(Integer)
    ProgramName = Column(String(255))
# endregion

# region RecordGroup
class RecordGroup(MainBase):
    __tablename__ = 'recordgroup'
    id = Column(Integer, primary_key=True)
    Title = Column(String(255))
    FormID = Column(Integer)
    Abbreviation = Column(String(10))
    SessionID = Column(Integer)
    TableID = Column(Integer)
    IDWidgetName = Column(String(255))
    IDWidgetType = Column(Integer)
    NewItemWidgetName = Column(String(255))
    NewItemWidgetType = Column(Integer)
    CreateDictFunction = Column(String(255))
    

class RecordGroupParents(MainBase):
    __tablename__ = 'recordgroupparent'
    id = Column(Integer, primary_key=True)
    RecordGroupID = Column(Integer)
    ParentGroupID = Column(Integer)
    ParentFieldID = Column(Integer)
    ChildFieldID = Column(Integer)
    TableID = Column(Integer)

# endregion

# region Forms
class FormInformation(MainBase):
    __tablename__ = 'forminformation'
    id = Column(Integer, primary_key=True)
    FileName = Column(String(255))
    FilePath = Column(String(255))

class FormWidgets(MainBase):
    __tablename__ = 'formwidgets'
    id = Column(Integer, primary_key=True)
    Form = Column(Integer)
    WidgetType = Column(Integer)
    WidgetName = Column(String(255))
    TabOrder = Column(Integer)

# endregion

# region Widgets
class WidgetType(MainBase):
    __tablename__ = 'lstwidgettype'
    id = Column(Integer, primary_key=True)
    NameText = Column(String(50))


class WidgetData(MainBase):
    __tablename__ = 'widgetdata'
    id = Column(Integer, primary_key=True)
    Title = Column(String(50))
    Abbreviation = Column(String(10))
    SetFunctionName = Column(String(50))
    DefaultValue = Column(String(10))
    DataType = Column(Integer)


class WidgetDataHandling(MainBase):
    __tablename__ = 'widgetdatahandling'
    id = Column(Integer, primary_key=True)
    WidgetID = Column(Integer)
    Direction = Column(Integer)
    DataType = Column(Integer)
    DataTypeFormat = Column(Integer)
    Command = Column(String(50))
    Description = Column(String(255))
    Preferred = Column(Integer)
# endregion

# region Form Items
class FormItemData(MainBase):
    __tablename__ = 'formitemdata'
    id = Column(Integer, primary_key=True)
    RecordGroupID = Column(Integer)
    WidgetType = Column(Integer)
    ItemName = Column(String(50))
    DefaultValue = Column(String(50))
    WidgetName = Column(String(50))
    SetValue = Column(Integer)
    GetValue = Column(Integer)
    GetString = Column(String(255))
    UpdateValue = Column(Integer)
    QueryRecord = Column(String(255))
    ClearWidget = Column(String(255))
    FilterCheckBox = Column(String(50))
    Description = Column(String(255))
    DatabaseField = Column(Integer)
    ViewOrder = Column(Integer)
    Label = Column(String(50))
    ReferenceSession = Column(Integer)
    ReferenceTable = Column(Integer)
    ReferenceField = Column(Integer)
    JoinVariable = Column(String(50))
    LockedStatus = Column(Integer)

class FormItemTreeViewData(MainBase):
    __tablename__ = 'formitemtvdata'
    id = Column(Integer, primary_key=True)
    FormItemData_id = Column(Integer)

# endregion

# region Form Functions
class FormFunctionTemplate(MainBase):
    __tablename__ = 'formfunctiontemplate'
    id = Column(Integer, primary_key=True)
    FunctionName = Column(String(50))
    Description = Column(String(255))
    FunctionPath = Column(String(255))
    Filename = Column(String(255))
    SubFunction = Column(Integer)
    DefaultOrder = Column(Integer)
    DefaultUse = Column(Integer)

class FormFunction(MainBase):
    __tablename__ = 'formfunction'
    id = Column(Integer, primary_key=True)
    RecordGroupID = Column(Integer)
    FormFunctionTemplateID = Column(Integer)


class VariableList(MainBase):
    __tablename__ = 'lstvariablelist'
    id = Column(Integer, primary_key=True)
    ItemName = Column(String(50))


class FunctionList(MainBase):
    __tablename__ = 'lstfunctionlist'
    id = Column(Integer, primary_key=True)
    ItemName = Column(String(50))


# endregion

# region FormDesign

class FormDesignTree(MainBase):
    __tablename__ = 'formdesigntree'
    id = Column(Integer, primary_key=True)
    PrimaryGroup_id = Column(Integer)  # , ForeignKey('treegroup.id'))
    SecondaryGroup_id = Column(Integer)  # , ForeignKey('treegroup.id'))
    ReferenceTreeRecord = Column(Integer)
    Tree_id = Column(String(50))
    LinkedTree_id = Column(String(50))
    ParentTree_id = Column(String(50))  # , ForeignKey('Equipmenttree.id'))
    TreePath = Column(String(255))
    ItemMaster_id = Column(Integer)
    ItemTable_id = Column(Integer)  # , ForeignKey('lstitemtable.id'))
    ItemTableType_id = Column(Integer)
    Item_id = Column(Integer)
    DisplayName = Column(String(255))
    ItemOrder = Column(Integer)
    FlattenedOrder = Column(Integer)
    ItemLevel = Column(Integer)
    ForeColor = Column(String(75))
    Expanded = Column(Integer)
    Header = Column(String(75))
    ChartColor = Column(String(75))
    Tags = Column(String(255))
    Date_Created = Column(DateTime, default=datetime.datetime.now())
    Date_Modified = Column(DateTime, default=datetime.datetime.now())
    Date_Accessed = Column(DateTime, default=datetime.datetime.now())


class FormDesignGeneratedTree(MainBase):
    __tablename__ = 'generatedformdesigntree'
    id = Column(Integer, primary_key=True)
    PrimaryGroup_id = Column(Integer)  # , ForeignKey('treegroup.id'))
    SecondaryGroup_id = Column(Integer)  # , ForeignKey('treegroup.id'))
    ReferenceTreeRecord = Column(Integer)
    Tree_id = Column(String(255))
    ParentTree_id = Column(String(255))  # , ForeignKey('Equipmenttree.id'))
    TreePath = Column(String(255))
    ItemMaster_id = Column(Integer)
    ItemTable_id = Column(Integer)  # , ForeignKey('lstitemtable.id'))
    ItemTableType_id = Column(Integer)
    Item_id = Column(Integer)
    DisplayName = Column(String(255))
    ItemOrder = Column(Integer)
    FlattenedOrder = Column(Integer)
    ItemLevel = Column(Integer)
    ForeColor = Column(String(75))
    Expanded = Column(Integer)
    Header = Column(String(75))
    ChartColor = Column(String(75))
    Tags = Column(String(255))
    Date_Created = Column(DateTime, default=datetime.datetime.now())
    Date_Modified = Column(DateTime, default=datetime.datetime.now())
    Date_Accessed = Column(DateTime, default=datetime.datetime.now())


class FormDesignComponents(MainBase):
    __tablename__ = 'formdesigncomponents'
    id = Column(Integer, primary_key=True)
    PrimaryGroup_id = Column(Integer)  # , ForeignKey('treegroup.id'))
    SecondaryGroup_id = Column(Integer)  # , ForeignKey('treegroup.id'))
    ReferenceTreeRecord = Column(Integer)
    Tree_id = Column(String(50))
    LinkedTree_id = Column(String(50))
    ParentTree_id = Column(String(50))  # , ForeignKey('Equipmenttree.id'))
    TreePath = Column(String(255))
    ItemMaster_id = Column(Integer)
    ItemTable_id = Column(Integer)  # , ForeignKey('lstitemtable.id'))
    ItemTableType_id = Column(Integer)
    Item_id = Column(Integer)
    DisplayName = Column(String(255))
    ItemOrder = Column(Integer)
    FlattenedOrder = Column(Integer)
    ItemLevel = Column(Integer)
    ForeColor = Column(String(75))
    Expanded = Column(Integer)
    Header = Column(String(75))
    ChartColor = Column(String(75))
    Tags = Column(String(255))
    Date_Created = Column(DateTime, default=datetime.datetime.now())
    Date_Modified = Column(DateTime, default=datetime.datetime.now())
    Date_Accessed = Column(DateTime, default=datetime.datetime.now())


class FormDesignBranchBuilder(MainBase):
    __tablename__ = 'formdesignbranchbuilder'
    id = Column(Integer, primary_key=True)
    PrimaryGroupTable_id = Column(Integer)  # Pointer
    PrimaryGroup_id = Column(Integer)  # Pointer
    PrimaryGroupTable_id = Column(Integer)  # Pointer
    SecondaryGroup_id = Column(Integer)  # Record Number
    SourceTable_id = Column(Integer)  #
    DestinationTable_id = Column(Integer)  #
    Description = Column(String(255))
    Tags = Column(String(255))

class FormDesignPrimaryGroup(MainBase):
    __tablename__ = 'formdesignprimarygroup'
    id = Column(Integer, primary_key=True)
    MasterTable_id = Column(Integer)
    Name_id = Column(Integer)  # , ForeignKey(Reference.id))
    NameText = Column(String(75))
    #Name = Column(String(75))
    Tags = Column(String(255))


class FormDesignSecondaryGroup(MainBase):
    __tablename__ = 'formdesignsecondarygroup'
    id = Column(Integer, primary_key=True)
    PrimaryGroup_id = Column(Integer)
    SecondaryGroup_id = Column(Integer)
    Name_id = Column(Integer)  # , ForeignKey(Reference.id))
    NameText = Column(String(75))
    #Name = Column(String(75))
    Tags = Column(String(255))


class FormDesignDescriptorTable(MainBase):
    __tablename__ = 'formdesigndescriptortable'
    id = Column(Integer, primary_key=True)
    MTTT_id = Column(Integer)
    Name_id = Column(Integer) #, ForeignKey(Reference.id))
    #Name = relationship('Reference')
    NameText = Column(String(75))
    MasterTable_id = Column(Integer)
    DisplayQuery = Column(String(255))


class FormDesignItemTable(MainBase):
    __tablename__ = 'formdesignitemtable'
    id = Column(Integer, primary_key=True)
    MTTT_id = Column(Integer)
    Name_id = Column(Integer) #, ForeignKey(Reference.id))
    #Name = relationship('Reference')
    NameText = Column(String(75))
    MasterTable_id = Column(Integer)
    DisplayQuery = Column(String(255))

class FormDesignTreeSetting(MainBase):
    __tablename__ = 'formdesigntreesetting'
    id = Column(Integer, primary_key=True)
    NameText = Column(String(75))
#