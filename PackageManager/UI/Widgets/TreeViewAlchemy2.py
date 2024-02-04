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
## August 8, 2019 - David James Lario - Created

#Python Imports
from copy import *
from io import *
import os
from pickle import dumps, load, loads
#PySide Imports
from PySide6.QtCore import QModelIndex, Qt, QMimeData, QAbstractItemModel
from PySide6.QtGui import QStandardItem, QStandardItemModel, QMouseEvent
from PySide6.QtWidgets import QTableView

#Core Imports

#Database Imports
from PackageManager.Core.Database import DatabaseTools

#Widgets

#Base Forms

#Import Tables
from PackageManager.Packages.ProgramBase.Database.dbMaster import *

from PackageManager.Packages.ProjectList.Database.dbFinance import *

#Default Settings
basepath = os.path.dirname(os.path.abspath(__file__))
settingDatabase = "DSSettings.db"
settingTable = "tblProgramSettings"
basepath = os.path.dirname(os.path.abspath(__file__))


def clonebranch(SSession, STree, SParent_id, DSession, DTree, DParent_id, DPG_id=1, DSG_id=1):
    def treeitemdata(SelectedTreeItem):

        newtreeitemdata = {}
        newtreeitemdata['id'] = SelectedTreeItem.id
        newtreeitemdata['TreePath'] = SelectedTreeItem.TreePath

        newtreeitemdata['PrimaryGroup_id'] = SelectedTreeItem.PrimaryGroup_id
        newtreeitemdata['Tree_id'] = SelectedTreeItem.Tree_id
        newtreeitemdata['ParentTree_id'] = SelectedTreeItem.ParentTree_id

        if SelectedTreeItem.TreePath is None:
            newtreeitemdata['TreePath'] = []
        else:
            newtreeitemdata['TreePath'] = DatabaseTools.strToMyList(SelectedTreeItem.TreePath)

        newtreeitemdata['ItemMaster_id'] = SelectedTreeItem.ItemMaster_id
        newtreeitemdata['ItemTable_id'] = SelectedTreeItem.ItemTable_id
        newtreeitemdata['ItemTableType_id'] = SelectedTreeItem.ItemTableType_id
        newtreeitemdata['Item_id'] = SelectedTreeItem.Item_id
        newtreeitemdata['DisplayName'] = SelectedTreeItem.DisplayName
        newtreeitemdata['ItemOrder'] = SelectedTreeItem.ItemOrder
        newtreeitemdata['FlattenedOrder'] = SelectedTreeItem.FlattenedOrder
        newtreeitemdata['ItemLevel'] = SelectedTreeItem.ItemLevel

        newtreeitemdata['ForeColor'] = SelectedTreeItem.ForeColor
        newtreeitemdata['Expanded'] = SelectedTreeItem.Expanded
        newtreeitemdata['Header'] = SelectedTreeItem.Header
        newtreeitemdata['ChartColor'] = SelectedTreeItem.ChartColor

        # newtreeitemdata['Tags'] = DatabaseTools.strToMyList(SelectedTreeItem.Tags)[-1]

        newtreeitemdata['Date_Created'] = SelectedTreeItem.Date_Created
        newtreeitemdata['Date_Modified'] = SelectedTreeItem.Date_Modified
        newtreeitemdata['Date_Accessed'] = SelectedTreeItem.Date_Accessed

        return newtreeitemdata

    def AddTreeRoot(SSession, STree, DSession, DTree, RootName, indexlist, newtreeitemdata=None, LinkedTable=None):

        itemcount = 0
        treeviewindex = 1
        for index in indexlist:
            treeviewindex = index

        currentdatetime = datetime.datetime.now()

        if newtreeitemdata is None:
            newtreeitemdata = {}
            newtreeitemdata['id'] = 0
            newtreeitemdata['TreePath'] = []
            newtreeitemdata['Tree_id'] = None
            newtreeitemdata['PrimaryGroup_id'] = 0
            newtreeitemdata['SourcePG'] = None
            newtreeitemdata['DestinationPG'] = None
            newtreeitemdata['SecondaryGroup_id'] = 0
            newtreeitemdata['SourceSG'] = None
            newtreeitemdata['DestinationSG'] = None
            newtreeitemdata['ParentTree_id'] = ("0")
            newtreeitemdata['ItemTable'] = None
            newtreeitemdata['ItemMaster_id'] = 0
            newtreeitemdata['ItemTableType_id'] = 0
            newtreeitemdata['ItemTable_id'] = 0
            newtreeitemdata['Item_id'] = 0
            newtreeitemdata['ItemName'] = ""
            newtreeitemdata['DisplayName'] = RootName
            newtreeitemdata['ItemOrder'] = 0
            newtreeitemdata['FlattenedOrder'] = 1
            newtreeitemdata['ItemLevel'] = 0
            newtreeitemdata['ForeColor'] = None
            newtreeitemdata['Expanded'] = 0
            newtreeitemdata['Header'] = None
            newtreeitemdata['Tags'] = []
            newtreeitemdata['Date_Created'] = str(currentdatetime)
            newtreeitemdata["id"] = None

        newtreeitemdata['Date_Modified'] = str(currentdatetime)
        newtreeitemdata['Date_Accessed'] = str(currentdatetime)

        # print("Adding Root", newtreeitemdata)
        treeItemDict = addTreeItem(SSession, STree, DSession, DTree, newtreeitemdata)
        # print("After", treeItemDict)
        # print("Root Tree_id ", treeItemDict["Tree_id"])
        return treeItemDict

    def addTreeItem(SSession, STree, DSession, DTree, treeItemDict):
        # Adds a tree item to the treemodel from the treeItemDict.
        # If the treeItem has a tree_id it will not create a database entry
        # Create the Tree
        # Add to Database

        # print("Teees", treeItemDict['Tree_id'], treeItemDict['ParentTree_id'])
        # Create the Linked Tree
        currentdatetime = datetime.datetime.now()
        if DTree is not None:
            DSession.begin(subtransactions=True)
            CreateUpdateAttribute = DTree(PrimaryGroup_id=int(treeItemDict["PrimaryGroup_id"]),
                                          SecondaryGroup_id=int(treeItemDict["SecondaryGroup_id"]),
                                          ReferenceTreeRecord=treeItemDict["id"],
                                          ParentTree_id=str(treeItemDict["ParentTree_id"]),
                                          TreePath=DatabaseTools.myListToStr(treeItemDict["TreePath"]),
                                          ItemMaster_id=int(treeItemDict["ItemMaster_id"]),
                                          ItemTable_id=int(treeItemDict["ItemTable_id"]),
                                          ItemTableType_id=int(treeItemDict["ItemTableType_id"]),
                                          Item_id=int(treeItemDict["Item_id"]),
                                          DisplayName=treeItemDict["DisplayName"],
                                          ItemOrder=int(treeItemDict["ItemOrder"]),
                                          FlattenedOrder=int(treeItemDict["FlattenedOrder"]),
                                          ItemLevel=int(treeItemDict["ItemLevel"]),
                                          ForeColor=treeItemDict["ForeColor"],
                                          Expanded=int(treeItemDict["Expanded"]),
                                          Tags=DatabaseTools.myListToStr(treeItemDict["Tags"]),
                                          Header=treeItemDict["Header"],
                                          Date_Created=str(currentdatetime),
                                          Date_Modified=str(currentdatetime),
                                          Date_Accessed=str(currentdatetime))
            DSession.add(CreateUpdateAttribute)
            DSession.commit()

            '''Update the Tree_id and ParentTree_id, TreePath needs to updated to the new format
            and Tags if required.'''

            DSession.begin()

            # For combined tables
            if treeItemDict["id"] != None:
                treeItemDict["Tree_id"] = "(%s-%s-%s-%s)" % (
                str(treeItemDict["PrimaryGroup_id"]), str(treeItemDict["SecondaryGroup_id"]),
                str(treeItemDict["ItemMaster_id"]), str(treeItemDict["id"]))
                CreateUpdateAttribute.Tree_id = treeItemDict["Tree_id"]
            else:
                treeItemDict["Tree_id"] = "(%s-%s-%s-%s)" % (
                str(treeItemDict["PrimaryGroup_id"]), str(treeItemDict["SecondaryGroup_id"]),
                str(treeItemDict["ItemMaster_id"]), str(CreateUpdateAttribute.id))
                CreateUpdateAttribute.Tree_id = treeItemDict["Tree_id"]
                treeItemDict["id"] = CreateUpdateAttribute.id

            treepath = treeItemDict["Tree_id"]

            treeItemDict["TreePath"].append(treepath)
            CreateUpdateAttribute.TreePath = DatabaseTools.myListToStr(treeItemDict["TreePath"])

            newtag = "(%s-%s)" % (treeItemDict["ItemTable_id"], treeItemDict["Item_id"])
            treeItemDict['Tags'].append(newtag)
            CreateUpdateAttribute.Tags = DatabaseTools.myListToStr(treeItemDict['Tags'])

            DSession.commit()

        return treeItemDict

    def tvtreebranch(SSession, STree, SParent_id, DSession, DTree, DParent_id, TagList, AdditionalInfo):
        # Load the table data that have parents that match the ParentID
        OriginalTreeParent = SSession.query(STree).filter_by(Tree_id=SParent_id).first()
        # Parent Tree Information
        DestinationTreeParent = DSession.query(DTree).filter_by(Tree_id=DParent_id).first()

        rowcount = 0
        treeviewindex = 1  # todo... or this

        records2 = SSession.query(STree).filter_by(ParentTree_id=str(SParent_id)).order_by("DisplayName").all()
        for row, record3 in enumerate(records2):
            rowcount += 1
            # Initialize the Data
            newtreeitemdata = treeitemdata(record3)
            # Adding the tree specific information
            # newtag = "(%s-%s)" % (str(DestinationRecord.ItemMaster_id), str(DestinationRecord.Item_id))
            treepath2 = DatabaseTools.strToMyList(DestinationTreeParent.TreePath)
            # treepath2.append(str(DestinationTreeParent.Tree_id))
            newtreeitemdata['PrimaryGroup_id'] = AdditionalInfo["PrimaryGroup_id"]
            newtreeitemdata['SecondaryGroup_id'] = AdditionalInfo["SecondaryGroup_id"]

            newtreeitemdata['TreePath'] = treepath2  # DatabaseTools.myListToStr(treepath2)
            newtreeitemdata['ItemLevel'] = len(treepath2) - 1
            newtreeitemdata['ItemOrder'] = rowcount
            newtreeitemdata['ParentTree_id'] = DestinationTreeParent.Tree_id
            newtreeitemdata['Tree_id'] = None
            newtreeitemdata['ItemTable'] = None
            newtreeitemdata['ItemName'] = None
            newtreeitemdata['id'] = None
            newtreeitemdata['PrimaryGroup_id'] = DestinationTreeParent.PrimaryGroup_id
            newtreeitemdata['Tags'] = TagList

            newtreeitemdata = addTreeItem(SSession, STree, DSession, DTree, newtreeitemdata)
            ParentID = newtreeitemdata['Tree_id']

            # Checking for presence of child items.
            record4 = SSession.query(STree).filter_by(ParentTree_id=str(record3.Tree_id)).first()
            if record4 is not None:
                tvtreebranch(SSession, STree, record3.Tree_id, DSession, DTree, ParentID, newtreeitemdata['Tags'],
                             AdditionalInfo)

    OriginalTreeParent = SSession.query(STree).filter_by(Tree_id=SParent_id).first()
    newtreeitemdata = treeitemdata(OriginalTreeParent)
    newtag = "(%s-%s)" % (str(OriginalTreeParent.ItemMaster_id), str(OriginalTreeParent.Item_id))

    DestinationTreeParent = DSession.query(DTree).filter_by(Tree_id=DParent_id).first()

    if DParent_id is None or DestinationTreeParent is None:
        newtreeitemdata['PrimaryGroup_id'] = DPG_id
        newtreeitemdata["SecondaryGroup_id"] = DSG_id
        newtreeitemdata['DestinationPG'] = DPG_id
        newtreeitemdata['DestinationSG'] = DSG_id

        newtreeitemdata['TreePath'] = []
        newtreeitemdata['ItemLevel'] = 0
        newtreeitemdata['Tree_id'] = None
        newtreeitemdata['ParentTree_id'] = "(0)"
        newtreeitemdata['Tags'] = []
        newtreeitemdata['ItemTable'] = 0
        newtreeitemdata['ItemName'] = ""
        newtreeitemdata = AddTreeRoot(SSession, STree, DSession, DTree, "Activity Tasks", [], newtreeitemdata, DTree)

    else:
        newtreeitemdata['PrimaryGroup_id'] = DPG_id
        newtreeitemdata["SecondaryGroup_id"] = DSG_id
        newtreeitemdata['TreePath'] = DatabaseTools.strToMyList(DestinationTreeParent.TreePath)
        newtreeitemdata['ItemLevel'] = DestinationTreeParent.ItemLevel + 1
        newtreeitemdata['Tree_id'] = None
        newtreeitemdata['ParentTree_id'] = DestinationTreeParent.Tree_id
        newtreeitemdata['Tags'].append(newtag)
        # newtreeitemdata = DModel.addTreeItem(DTree, newtreeitemdata)

    ParentID = newtreeitemdata['Tree_id']
    AdditionalInfo = {}
    AdditionalInfo["Tags"] = newtag
    AdditionalInfo["PrimaryGroup_id"] = DPG_id
    AdditionalInfo["SecondaryGroup_id"] = DSG_id

    tvtreebranch(SSession, STree, SParent_id, DSession, DTree, ParentID, newtreeitemdata['Tags'], AdditionalInfo)


def clonefullbranch(treeviewdict, bases, sessions, SSession, STree, SParent_id, SPrimaryKey, SSecondaryKey, DSession,
                    DTree, DParent_id, DPrimaryKey, DSecondaryKey):
    RecordCount = 0

    def treeitemdata(SelectedTreeItem):

        newtreeitemdata = {}
        newtreeitemdata['id'] = SelectedTreeItem.id
        newtreeitemdata['TreePath'] = SelectedTreeItem.TreePath

        newtreeitemdata['PrimaryGroup_id'] = SelectedTreeItem.PrimaryGroup_id
        newtreeitemdata['Tree_id'] = SelectedTreeItem.Tree_id
        newtreeitemdata['ParentTree_id'] = SelectedTreeItem.ParentTree_id

        if SelectedTreeItem.TreePath is None:
            newtreeitemdata['TreePath'] = []
        else:
            newtreeitemdata['TreePath'] = DatabaseTools.strToMyList(SelectedTreeItem.TreePath)

        newtreeitemdata['ItemMaster_id'] = SelectedTreeItem.ItemMaster_id
        newtreeitemdata['ItemTable_id'] = SelectedTreeItem.ItemTable_id
        newtreeitemdata['ItemTableType_id'] = SelectedTreeItem.ItemTableType_id
        newtreeitemdata['Item_id'] = SelectedTreeItem.Item_id
        newtreeitemdata['DisplayName'] = SelectedTreeItem.DisplayName
        newtreeitemdata['ItemOrder'] = SelectedTreeItem.ItemOrder
        newtreeitemdata['FlattenedOrder'] = SelectedTreeItem.FlattenedOrder
        newtreeitemdata['ItemLevel'] = SelectedTreeItem.ItemLevel

        newtreeitemdata['ForeColor'] = SelectedTreeItem.ForeColor
        newtreeitemdata['Expanded'] = SelectedTreeItem.Expanded
        newtreeitemdata['Header'] = SelectedTreeItem.Header
        newtreeitemdata['ChartColor'] = SelectedTreeItem.ChartColor

        # newtreeitemdata['Tags'] = DatabaseTools.strToMyList(SelectedTreeItem.Tags)[-1]

        newtreeitemdata['Date_Created'] = SelectedTreeItem.Date_Created
        newtreeitemdata['Date_Modified'] = SelectedTreeItem.Date_Modified
        newtreeitemdata['Date_Accessed'] = SelectedTreeItem.Date_Accessed

        return newtreeitemdata

    def AddTreeRoot(SSession, STree, DSession, DTree, RootName, indexlist, newtreeitemdata=None, LinkedTable=None):

        itemcount = 0
        treeviewindex = 1
        for index in indexlist:
            treeviewindex = index

        currentdatetime = datetime.datetime.now()

        if newtreeitemdata is None:
            newtreeitemdata = {}
            newtreeitemdata['id'] = 0
            newtreeitemdata['TreePath'] = []
            newtreeitemdata['Tree_id'] = None
            newtreeitemdata['PrimaryGroup_id'] = 0
            newtreeitemdata['SourcePG'] = None
            newtreeitemdata['DestinationPG'] = None
            newtreeitemdata['SecondaryGroup_id'] = 0
            newtreeitemdata['SourceSG'] = None
            newtreeitemdata['DestinationSG'] = None
            newtreeitemdata['ParentTree_id'] = ("0")
            newtreeitemdata['ItemTable'] = None
            newtreeitemdata['ItemMaster_id'] = 0
            newtreeitemdata['ItemTableType_id'] = 0
            newtreeitemdata['ItemTable_id'] = 0
            newtreeitemdata['Item_id'] = 0
            newtreeitemdata['ItemName'] = ""
            newtreeitemdata['DisplayName'] = RootName
            newtreeitemdata['ItemOrder'] = 0
            newtreeitemdata['FlattenedOrder'] = 1
            newtreeitemdata['ItemLevel'] = 0
            newtreeitemdata['ForeColor'] = None
            newtreeitemdata['Expanded'] = 0
            newtreeitemdata['Header'] = None
            newtreeitemdata['Tags'] = []
            newtreeitemdata['Date_Created'] = str(currentdatetime)
            newtreeitemdata["id"] = None

        newtreeitemdata['Date_Modified'] = str(currentdatetime)
        newtreeitemdata['Date_Accessed'] = str(currentdatetime)

        # print("Adding Root", newtreeitemdata)
        treeItemDict = addTreeItem(SSession, STree, DSession, DTree, newtreeitemdata)
        # print("After", treeItemDict)
        # print("Root Tree_id ", treeItemDict["Tree_id"])
        return treeItemDict

    def addTreeItem(SSession, STree, DSession, DTree, treeItemDict):
        # Adds a tree item to the treemodel from the treeItemDict.
        # If the treeItem has a tree_id it will not create a database entry
        # Create the Tree
        # Add to Database

        # print("Teees", treeItemDict['Tree_id'], treeItemDict['ParentTree_id'])
        # Create the Linked Tree
        currentdatetime = datetime.datetime.now()
        if DTree is not None:
            DSession.begin(subtransactions=True)
            CreateUpdateAttribute = DTree(PrimaryGroup_id=int(treeItemDict["PrimaryGroup_id"]),
                                          SecondaryGroup_id=int(treeItemDict["SecondaryGroup_id"]),
                                          ReferenceTreeRecord=treeItemDict["id"],
                                          ParentTree_id=str(treeItemDict["ParentTree_id"]),
                                          TreePath=DatabaseTools.myListToStr(treeItemDict["TreePath"]),
                                          ItemMaster_id=int(treeItemDict["ItemMaster_id"]),
                                          ItemTable_id=int(treeItemDict["ItemTable_id"]),
                                          ItemTableType_id=int(treeItemDict["ItemTableType_id"]),
                                          Item_id=int(treeItemDict["Item_id"]),
                                          DisplayName=treeItemDict["DisplayName"],
                                          ItemOrder=int(treeItemDict["ItemOrder"]),
                                          FlattenedOrder=int(treeItemDict["FlattenedOrder"]),
                                          ItemLevel=int(treeItemDict["ItemLevel"]),
                                          ForeColor=treeItemDict["ForeColor"],
                                          Expanded=int(treeItemDict["Expanded"]),
                                          Tags=DatabaseTools.myListToStr(treeItemDict["Tags"]),
                                          Header=treeItemDict["Header"],
                                          Date_Created=str(currentdatetime),
                                          Date_Modified=str(currentdatetime),
                                          Date_Accessed=str(currentdatetime))
            DSession.add(CreateUpdateAttribute)
            DSession.commit()

            '''Update the Tree_id and ParentTree_id, TreePath needs to updated to the new format
            and Tags if required.'''

            DSession.begin()

            # For combined tables
            if treeItemDict["id"] != None:
                treeItemDict["Tree_id"] = "(%s-%s-%s-%s)" % (
                    str(treeItemDict["PrimaryGroup_id"]), str(treeItemDict["SecondaryGroup_id"]),
                    str(treeItemDict["ItemTable_id"]), str(treeItemDict["id"]))
                CreateUpdateAttribute.Tree_id = treeItemDict["Tree_id"]
            else:
                treeItemDict["Tree_id"] = "(%s-%s-%s-%s)" % (
                    str(treeItemDict["PrimaryGroup_id"]), str(treeItemDict["SecondaryGroup_id"]),
                    str(treeItemDict["ItemTable_id"]), str(CreateUpdateAttribute.id))
                CreateUpdateAttribute.Tree_id = treeItemDict["Tree_id"]
                treeItemDict["id"] = CreateUpdateAttribute.id

            treepath = treeItemDict["Tree_id"]

            treeItemDict["TreePath"].append(treepath)
            CreateUpdateAttribute.TreePath = DatabaseTools.myListToStr(treeItemDict["TreePath"])

            newtag = "(%s-%s)" % (treeItemDict["ItemTable_id"], treeItemDict["Item_id"])
            treeItemDict['Tags'].append(newtag)
            CreateUpdateAttribute.Tags = DatabaseTools.myListToStr(treeItemDict['Tags'])

            DSession.commit()

        return treeItemDict

    def tvtreebranch(SSession, STree, SParent_id, DSession, DTree, DParent_id, TagList, AdditionalInfo):
        # Load the table data that have parents that match the ParentID
        OriginalTreeParent = SSession.query(STree).filter_by(PrimaryGroup_id=SPrimaryKey,
                                                             SecondaryGroup_id=SSecondaryKey,
                                                             Tree_id=SParent_id).first()
        # Parent Tree Information
        DestinationTreeParent = DSession.query(DTree).filter_by(PrimaryGroup_id=DPrimaryKey,
                                                                SecondaryGroup_id=DSecondaryKey,
                                                                Tree_id=DParent_id).first()

        rowcount = 0
        treeviewindex = 1  # todo... or this

        records2 = SSession.query(STree).filter_by(PrimaryGroup_id=SPrimaryKey, SecondaryGroup_id=SSecondaryKey,
                                                   ParentTree_id=str(SParent_id)).order_by("DisplayName").all()
        for row, record3 in enumerate(records2):
            rowcount += 1
            # Initialize the Data
            newtreeitemdata = treeitemdata(record3)
            # Adding the tree specific information
            # newtag = "(%s-%s)" % (str(DestinationRecord.ItemMaster_id), str(DestinationRecord.Item_id))
            treepath2 = DatabaseTools.strToMyList(DestinationTreeParent.TreePath)
            # treepath2.append(str(DestinationTreeParent.Tree_id))
            newtreeitemdata['PrimaryGroup_id'] = AdditionalInfo["PrimaryGroup_id"]
            newtreeitemdata['SecondaryGroup_id'] = AdditionalInfo["SecondaryGroup_id"]

            newtreeitemdata['TreePath'] = treepath2  # DatabaseTools.myListToStr(treepath2)
            newtreeitemdata['ItemLevel'] = len(treepath2) - 1
            newtreeitemdata['ItemOrder'] = rowcount
            newtreeitemdata['ParentTree_id'] = DestinationTreeParent.Tree_id
            newtreeitemdata['Tree_id'] = None
            newtreeitemdata['ItemTable'] = None
            newtreeitemdata['ItemName'] = None
            newtreeitemdata['id'] = None
            newtreeitemdata['PrimaryGroup_id'] = DestinationTreeParent.PrimaryGroup_id
            newtreeitemdata['Tags'] = TagList

            newtreeitemdata = addTreeItem(SSession, STree, DSession, DTree, newtreeitemdata)
            ParentID = newtreeitemdata['Tree_id']

            # Checking for presence of child items.

            record4 = SSession.query(STree).filter_by(PrimaryGroup_id=SPrimaryKey, SecondaryGroup_id=SSecondaryKey,
                                                      ParentTree_id=str(record3.Tree_id)).first()
            if record4 is not None:
                tvtreebranch(SSession, STree, record3.Tree_id, DSession, DTree, ParentID, newtreeitemdata['Tags'],
                             AdditionalInfo)

    def tvtreelinkedbranch(treeviewdict, bases, sessions, SSession, STree, SParent_id, SPrimaryKey, SSecondaryKey,
                           DSession, DTree, DParent_id, DPrimaryKey, DSecondaryKey, TreePath, TagList, ItemLevel):

        OriginalTreeParent = SSession.query(STree).filter_by(PrimaryGroup_id=SPrimaryKey,
                                                             SecondaryGroup_id=SSecondaryKey,
                                                             Tree_id=SParent_id).first()
        # Parent Tree Information
        DestinationTreeParent = DSession.query(DTree).filter_by(PrimaryGroup_id=DPrimaryKey,
                                                                SecondaryGroup_id=int(DSecondaryKey),
                                                                Tree_id=DParent_id).first()

        if SParent_id:
            parentstuff = SParent_id[1:-1]
            parentstufflist = parentstuff.split("-")  # last item, remove brackets split by the -

            records = SSession.query(STree).filter_by(PrimaryGroup_id=SPrimaryKey) \
                .filter_by(SecondaryGroup_id=SSecondaryKey) \
                .filter_by(ParentTree_id=SParent_id) \
                .order_by(STree.ItemOrder).order_by(STree.DisplayName).all()

            # TotalRecords =
            RecordCount = 0
            rowcount = 0
            treeviewindex = 1  # todo... or this

            for row, record1 in enumerate(records):
                # print("record1", record1.Tree_id, record1.DisplayName)
                # Each the primary group will determine which branch items to follow.
                # The new tree will only have the primary group of the generated
                # print("Primary Group:", PrimaryGroup_id, record1.DisplayName)
                RecordCount += 1
                # Initialize the Data
                a = record1.DisplayName

                item_id = record1.id  # Item_id

                newtreeitemdata = treeItemFromdb(SSession, STree, item_id, treeviewdict["MasterTable_id"])

                treepath2 = TreePath.copy()

                # sourceid = "(%s-%s-%s)" % (SourcePG, SourceTable_id, itemlistdata["id"])
                # destinationid = "(%s-%s-%s)" % (DestinationPG, SourceTable_id, itemlistdata["id"])

                newtreeitemdata['TreePath'] = treepath2  # DatabaseTools.myListToStr(treepath2)
                newtreeitemdata['ItemLevel'] = ItemLevel + 1
                newtreeitemdata['ItemOrder'] = RecordCount
                newtreeitemdata['ItemTable_id'] = record1.ItemTable_id
                newtreeitemdata['ParentTree_id'] = DParent_id
                newtreeitemdata['id'] = record1.id
                # newtreeitemdata['SourcePG'] = SourcePG

                newtreeitemdata['DestinationPG'] = DPrimaryKey
                newtreeitemdata['DestinationSG'] = DSecondaryKey
                newtreeitemdata['PrimaryGroup_id'] = DPrimaryKey
                newtreeitemdata["SecondaryGroup_id"] = DSecondaryKey

                newtreeitemdata['MasterTable_id'] = treeviewdict["MasterTable_id"]

                taglist1 = TagList.copy()
                newtreeitemdata['Tags'] = taglist1

                newtreeitemdata1a = addTreeItem(SSession, STree, DSession, DTree, newtreeitemdata)
                destinationparent_id2 = newtreeitemdata1a["Tree_id"]

                fulltagname = taglist1[-1][1:-1]
                lasttag = taglist1[-1][1:-1].split("-")  # last item, remove brackets split by the -
                table_id = int(lasttag[0])

                secondarylist = [190, 19, 680, 672, 145, 611, 644, 571]  # Secondary Tables
                if table_id in secondarylist:  # Tree View Secondary
                    newtreeitemdata["LinkedTree_id"] = fulltagname
                else:
                    newtreeitemdata["LinkedTree_id"] = None

                if newtreeitemdata["LinkedTree_id"]:
                    branchmaster_id = newtreeitemdata["LinkedTree_id"]
                    branchitems = branchmaster_id.split("-")

                    linkedTable_id = int(branchitems[0])
                    linkedRecord_id = int(branchitems[1])

                    mastertablequery = treeviewdict["MasterSession"].query(treeviewdict["MasterTable"]).filter_by(
                        id=linkedTable_id).first()
                    SessionName = treeviewdict["MasterSession"].query(SessionNames).filter_by(
                        id=mastertablequery.Session).first()
                    BaseName = treeviewdict["MasterSession"].query(SessionBase).filter_by(
                        id=mastertablequery.Base).first()
                    LinkedSourceReference = DatabaseTools.get_class_by_tablename(bases[BaseName.NameText],
                                                                                 mastertablequery.TableName)

                    secondaryrecord = sessions[SessionName.NameText].query(LinkedSourceReference).filter_by(
                        id=linkedRecord_id).first()

                    primaryrecord = sessions[SessionName.NameText].query(treeviewdict["PrimaryGroup"]).filter_by(
                        id=secondaryrecord.PrimaryGroup_id).first()

                    mastertablequery2 = treeviewdict["MasterSession"].query(treeviewdict["MasterTable"]).filter_by(
                        id=primaryrecord.MasterTable_id).first()
                    SessionName2 = treeviewdict["MasterSession"].query(SessionNames).filter_by(
                        id=mastertablequery2.Session).first()
                    BaseName2 = treeviewdict["MasterSession"].query(SessionBase).filter_by(
                        id=mastertablequery2.Base).first()
                    LinkedSourceTable = DatabaseTools.get_class_by_tablename(bases[BaseName2.NameText],
                                                                             mastertablequery2.TableName)

                    record2 = sessions[SessionName2.NameText].query(LinkedSourceTable).filter_by(
                        PrimaryGroup_id=secondaryrecord.PrimaryGroup_id) \
                        .filter_by(SecondaryGroup_id=secondaryrecord.SecondaryGroup_id) \
                        .filter_by(ParentTree_id="(0)") \
                        .order_by(STree.ItemOrder).order_by(STree.DisplayName).first()

                    SourceTable_id2 = linkedTable_id
                    SourceSession2 = sessions[SessionName.NameText]
                    SourceTree2 = LinkedSourceTable

                    treeviewdict["TreeItems"] = LinkedSourceTable
                    treeviewdict["Session"] = sessions[SessionName.NameText]

                    if record2.Tree_id is not None:
                        RecordCount += 1
                        # Initialize the Data

                        newtreeitemdata2 = treeItemFromdb(treeviewdict["Session"], SourceTree2, record2.id,
                                                          treeviewdict["MasterTable_id"])

                        treepath3 = treepath2.copy()
                        newtreeitemdata2['LinkedTree'] = record2.id
                        newtreeitemdata2['TreePath'] = treepath3  # DatabaseTools.myListToStr(treepath2)
                        newtreeitemdata2['ItemLevel'] = ItemLevel
                        newtreeitemdata2['ItemOrder'] = RecordCount
                        newtreeitemdata2['ItemTable_id'] = record2.ItemTable_id
                        newtreeitemdata2['ParentTree_id'] = newtreeitemdata['Tree_id']
                        newtreeitemdata2['id'] = record2.id
                        taglist2 = taglist1.copy()
                        newtreeitemdata2['Tags'] = taglist2

                        records5 = SourceSession2.query(SourceTree2).filter_by(
                            ParentTree_id=str(record2.Tree_id)).order_by(SourceTree2.DisplayName).all()
                        if records5 is not None:
                            tvtreelinkedbranch(treeviewdict, bases, sessions, SSession, STree, record2.Tree_id,
                                               secondaryrecord.PrimaryGroup_id, secondaryrecord.SecondaryGroup_id,
                                               DSession, DTree, destinationparent_id2, DPrimaryKey, DSecondaryKey,
                                               treepath3, taglist1, ItemLevel)
                            # createtvtreebranch(treeviewdict2, newtreeitemdata2["TreePath"], taglist1, itemlistdata2, record2.Tree_id, destinationparent_id2, ItemLevel)
                            # treeviewdict, treepath, taglist, itemlistdata, sourceparentid, destinationparent_id, ItemLevel):

                            # print("level created")
                else:
                    records3 = SSession.query(STree).filter_by(
                        ParentTree_id=str(record1.Tree_id)).order_by(STree.DisplayName).all()
                    if records3:
                        tvtreelinkedbranch(treeviewdict, bases, sessions, SSession, STree, record1.Tree_id, SPrimaryKey,
                                           SSecondaryKey, DSession, DTree, destinationparent_id2, DPrimaryKey,
                                           DSecondaryKey, treepath2, taglist1, ItemLevel)
                        # createtvtreebranch(treeviewdict, newtreeitemdata["TreePath"], taglist1, sourceitemlistdata, record1.Tree_id, destinationparent_id2, ItemLevel + 1)

    OriginalTreeParent = SSession.query(STree).filter_by(PrimaryGroup_id=SPrimaryKey, SecondaryGroup_id=SSecondaryKey,
                                                         Tree_id=SParent_id).first()
    newtreeitemdata = treeitemdata(OriginalTreeParent)
    newtag = "(%s-%s)" % (str(OriginalTreeParent.ItemTable_id), str(OriginalTreeParent.Item_id))
    TagList = []
    TagList.append(newtag)

    DestinationTreeParent = DSession.query(DTree).filter_by(PrimaryGroup_id=DPrimaryKey,
                                                            SecondaryGroup_id=DSecondaryKey, Tree_id=DParent_id).first()
    ItemLevel = 0
    RecordCount = 0

    if DParent_id is None or DestinationTreeParent is None:
        newtreeitemdata['PrimaryGroup_id'] = DPrimaryKey
        newtreeitemdata["SecondaryGroup_id"] = DSecondaryKey
        newtreeitemdata['DestinationPG'] = DPrimaryKey
        newtreeitemdata['DestinationSG'] = DSecondaryKey

        newtreeitemdata['TreePath'] = []
        newtreeitemdata['ItemLevel'] = 0
        newtreeitemdata['Tree_id'] = None
        newtreeitemdata['ParentTree_id'] = "(0)"
        newtreeitemdata['Tags'] = []
        newtreeitemdata['ItemTable'] = 0
        newtreeitemdata['ItemName'] = ""
        newtreeitemdata = AddTreeRoot(SSession, STree, DSession, DTree, "Activity Tasks", [], newtreeitemdata, DTree)

    else:
        newtreeitemdata['PrimaryGroup_id'] = DPrimaryKey
        newtreeitemdata["SecondaryGroup_id"] = DSecondaryKey
        newtreeitemdata['TreePath'] = DatabaseTools.strToMyList(DestinationTreeParent.TreePath)
        newtreeitemdata['ItemLevel'] = DestinationTreeParent.ItemLevel + 1
        newtreeitemdata['Tree_id'] = None
        newtreeitemdata['ParentTree_id'] = DestinationTreeParent.Tree_id
        newtreeitemdata['Tags'].append(newtag)
        # newtreeitemdata = DModel.addTreeItem(DTree, newtreeitemdata)

    tvtreelinkedbranch(treeviewdict, bases, sessions, SSession, STree, SParent_id, SPrimaryKey, SSecondaryKey, DSession,
                       DTree, newtreeitemdata['Tree_id'], DPrimaryKey, DSecondaryKey, [], TagList, ItemLevel)


# tvtreebranch(SSession, STree, SParent_id, DSession, DTree, ParentID, newtreeitemdata['Tags'], AdditionalInfo)


def createbranch(treedict):
    # The id column entry can be single entry or a list of entries.  This is typeically for the parent list
    # if priminary group id is not it should load them all

    SourceTable_id = treedict["MasterTable_id"]
    MasterSession = treedict["MasterSession"]
    SourceSession = treedict["Session"]
    SourceTree = treedict["TreeItems"]

    if type(id) is not list:
        baseidlist = []
        baseidlist.append(id)
    else:
        baseidlist = id

    for itemlistdata in linkeditemlist:

        modelrootitem = SourceSession.query(SourceTree).filter_by(id=itemlistdata["id"]).first()

        mastertablequery = MasterSession.query(treedict["MasterTable"]).filter_by(id=modelrootitem.ItemTable_id).first()
        SessionName = MasterSession.query(SessionNames).filter_by(id=mastertablequery.Session).first()
        BaseName = MasterSession.query(SessionBase).filter_by(id=mastertablequery.Base).first()

        newtreeitemdata = treeItemFromdb(SourceSession, SourceTree, itemlistdata["id"], SourceTable_id)
        sourceid = "(%s-%s-%s-%s)" % (
        newtreeitemdata['SourcePG'], newtreeitemdata['SourceSG'], SourceTable_id, itemlistdata["id"])

        sourceparent_id = "(0)"
        destinationparent_id = "(0)"
        treepath = []
        # newtreeitemdata['ItemTable_id'] = modelrootitem.ItemMaster_id
        newtreeitemdata['ItemLevel'] = 0
        newtreeitemdata['Tags'] = []
        newtreeitemdata['ParentTree_id'] = "(0)"
        newtreeitemdata['MasterTable_id'] = SourceTable_id
        # newtreeitemdata['SourcePG'] = itemlistdata["PrimaryGroup_id"]
        # newtreeitemdata['PrimaryGroup_id'] = itemlistdata["PrimaryGroup_id"]

        if itemlistdata['DestinationPG'] is None:
            newtreeitemdata['DestinationPG'] = newtreeitemdata['SourcePG']
        else:
            newtreeitemdata['DestinationPG'] = itemlistdata['DestinationPG']

        if itemlistdata['DestinationSG'] is None:
            newtreeitemdata['DestinationSG'] = newtreeitemdata['SourceSG']
        else:
            newtreeitemdata['DestinationSG'] = itemlistdata['DestinationSG']

        destinationid = "(%s-%s-%s-%s)" % (
        newtreeitemdata['DestinationPG'], newtreeitemdata['DestinationSG'], SourceTable_id, itemlistdata["id"])

        originaltree_id = newtreeitemdata["Tree_id"]
        newtreeitemdata2 = AddTreeRoot("Ginger", [], newtreeitemdata=newtreeitemdata,
                                       LinkedTable=treedict["GeneratedTree"])
        # newtreeitemdata["Tree_id"] = id

        linkeditemlist = []
        createtvtreebranch(treedict, treepath, newtreeitemdata2['Tags'], itemlistdata, sourceparent_id,
                           destinationparent_id, modelrootitem.ItemMaster_id, newtreeitemdata['ItemLevel'])


def createtvtreebranch(treedict, treepath, taglist, itemlistdata, sourceparentid, destinationparentid, master_id,
                       ItemLevel):
    SourceTree = treedict["TreeItems"]
    records2 = treedict["Session"].query(SourceTree).filter_by(PrimaryGroup_id=itemlistdata['SourcePG']) \
        .filter_by(SecondaryGroup_id=itemlistdata['SourceSG']) \
        .filter_by(ParentTree_id=sourceparentid) \
        .order_by(SourceTree.ItemOrder).order_by(SourceTree.DisplayName).all()
    rowcount = 0
    treeviewindex = 1  # todo... or this
    for row, record2 in enumerate(records2):
        # Each the primary group will determine which branch items to follow.
        # The new tree will only have the primary group of the generated
        # print("Primary Group:", PrimaryGroup_id, record2.DisplayName)
        RecordCount += 1
        # Initialize the Data
        pg = itemlistdata['SourcePG']
        sg = itemlistdata['SourceSG']
        item_id = record2.id  # Item_id

        newtreeitemdata = treeItemFromdb(treedict["Session"], SourceTree, item_id, treedict["MasterTable_id"])

        treepath2 = treepath.copy()

        # sourceid = "(%s-%s-%s)" % (SourcePG, SourceTable_id, itemlistdata["id"])
        # destinationid = "(%s-%s-%s)" % (DestinationPG, SourceTable_id, itemlistdata["id"])

        newtreeitemdata['TreePath'] = treepath2  # DatabaseTools.myListToStr(treepath2)
        newtreeitemdata['ItemLevel'] = ItemLevel + 1
        newtreeitemdata['ItemOrder'] = RecordCount
        newtreeitemdata['ItemTable_id'] = record2.ItemTable_id
        newtreeitemdata['ParentTree_id'] = destinationparentid
        newtreeitemdata['id'] = record2.id
        # newtreeitemdata['SourcePG'] = SourcePG

        if itemlistdata['DestinationPG'] is None:
            newtreeitemdata['DestinationPG'] = newtreeitemdata['SourcePG']
        else:
            newtreeitemdata['DestinationPG'] = itemlistdata['DestinationPG']

        if itemlistdata['DestinationSG'] is None:
            newtreeitemdata['DestinationSG'] = newtreeitemdata['SourceSG']
        else:
            newtreeitemdata['DestinationSG'] = itemlistdata['DestinationSG']

        newtreeitemdata['MasterTable_id'] = treedict["MasterTable_id"]

        destinationid = "(%s-%s-%s-%s)" % (DestinationPG, DestinationSG, treedict["MasterTable_id"], itemlistdata["id"])

        taglist2 = taglist.copy()
        newtreeitemdata['Tags'] = taglist2

        newtreeitemdata2 = addTreeItem(treedict["GeneratedTree"], newtreeitemdata)

        linkeditemlist = []
        for branchmaster_id in linkeditemlist:
            # if the mastertable and item_id match parent table then add this to the tree.
            # 3mastertablequery2 = treedict["MasterTable"].filter_by(id=branchmaster_id).first()
            # TableClass2 = DatabaseTools.get_class_by_tablename(bases[mastertablequery2.Session], mastertablequery2.ReferenceTable)

            records4 = treedict["Session"].query(SourceTree).filter_by(ItemMaster_id=record2.ItemMaster_id) \
                .filter_by(Item_id=record2.Item_id) \
                .filter_by(PrimaryGroup_id=newtreeitemdata['SourcePG']) \
                .order_by(SourceTree.DisplayName).all()

            for record4 in records4:
                if record4.Tree_id is not None:
                    RecordCount += 1
                    # Initialize the Data
                    item_id3 = record4.id  # Item_id

                    newtreeitemdata3 = treeItemFromdb(treedict["Session"], SourceTree, item_id3,
                                                      treedict["MasterTable_id"])
                    PrimaryGroup_id3 = newtreeitemdata['SourcePG']  # record4.PrimaryGroup_id
                    # print(branchmaster_id, item_id3, newtreeitemdata2)
                    treepath3 = treepath2.copy()
                    # treepath2.append(newtreeitemdata['Tree_id'])
                    newtreeitemdata3['TreePath'] = treepath3  # DatabaseTools.myListToStr(treepath2)
                    newtreeitemdata3['ItemLevel'] = ItemLevel + 2
                    newtreeitemdata3['ItemOrder'] = RecordCount
                    newtreeitemdata3['PrimaryGroup_id'] = newtreeitemdata['SourcePG']  # ParentPG

                    newtreeitemdata3['ParentTree_id'] = newtreeitemdata['Tree_id']
                    newtreeitemdata3['id'] = record4.id

                    taglist3 = taglist2.copy()

                    newtag = "(%s-%s)" % (newtreeitemdata["ItemTable_id"], newtreeitemdata["Item_id"])
                    if newtag not in taglist3: taglist3.append(newtag)

                    newtreeitemdata3['Tags'] = taglist3

                    # Checking for presence of child items.
                    # mastertablequery3 = treedict["MasterTable"].filter_by(id=branchmaster_id).first()
                    # TableClass3 = DatabaseTools.get_class_by_tablename(bases[mastertablequery3.ReferenceTableSession], mastertablequery3.ReferenceTable)
                    records5 = treedict["Session"].query(SourceTree).filter_by(
                        ParentTree_id=str(record4.Tree_id)).order_by(SourceTree.DisplayName).all()
                    if records5 is not None:
                        PrimaryGroup_idb = newtreeitemdata['SourcePG']

                        createtvtreebranch(newtreeitemdata3["TreePath"], taglist3, itemlistdata, record4.Tree_id,
                                           destinationid, branchmaster_id, ItemLevel + 2)
                        # treepath, taglist, itemlistdata, sourceparentid, destinationparentid, master_id, ItemLevel):

        records3 = treedict["Session"].query(SourceTree).filter_by(ParentTree_id=str(record2.Tree_id)).order_by(
            SourceTree.DisplayName).all()

        # records3 = sessions[mastertablequery.ReferenceTableSession].query(TableClass) \
        # .filter_by(ParentTree_id=str(record2.Tree_id)).order_by(mastertablequery.RefTableDisplayNameColumn).all()
        if records3 is not None:
            # if record2.LinkChildren == 1:
            PrimaryGroup_ida = newtreeitemdata['SourcePG']

            createtvtreebranch(newtreeitemdata["TreePath"], taglist2, itemlistdata, record2.Tree_id,
                               newtreeitemdata2["Tree_id"], master_id, ItemLevel + 1)


def defaultTreeItem():
    newtreeitemdata = {}
    newtreeitemdata['TreePath'] = []
    newtreeitemdata['PrimaryGroup_id'] = 0
    newtreeitemdata['SourcePG'] = 1
    newtreeitemdata['DestinationPG'] = 1
    newtreeitemdata['SourceSG'] = 1
    newtreeitemdata['DestinationSG'] = 1
    newtreeitemdata['SecondaryGroup_id'] = 1
    newtreeitemdata['Tree_id'] = None
    newtreeitemdata['ParentTree_id'] = "0"  # Follows the top item
    newtreeitemdata['ItemTable'] = None
    newtreeitemdata['ItemTable_id'] = 0
    newtreeitemdata['ItemMaster_id'] = 0
    newtreeitemdata['ItemTable'] = None
    newtreeitemdata['ItemTableType_id'] = 0
    newtreeitemdata['Item_id'] = 0
    newtreeitemdata['ItemName'] = None
    newtreeitemdata['DisplayName'] = None
    newtreeitemdata['ItemOrder'] = 0
    newtreeitemdata['FlattenedOrder'] = 0
    newtreeitemdata['ItemLevel'] = 0
    newtreeitemdata['ForeColor'] = None
    newtreeitemdata['Expanded'] = 0
    newtreeitemdata['Header'] = None
    newtreeitemdata['Tags'] = []
    newtreeitemdata['Date_Created'] = None
    newtreeitemdata['Date_Modified'] = None
    newtreeitemdata['Date_Accessed'] = None

    # newtreeitemdata = currentTreeItem(ID=Tree_id)

    # treepath = []
    # treepath.append(Tree_id)
    # newtreeitemdata['TreePath'] = str(DatabaseTools.myListToStr(treepath))
    itemlevel = 0
    # newtreeitemdata['ItemLevel'] = len(treepath) - 1

    return newtreeitemdata


def treeItemFromdb(SourceSession, SourceTree, id, SourceTable_id, tree_id=None):
    # todo the id and tree_id arre not the same
    # Creates a tree item from the data
    # Can be a list table or tree table
    # TreeClass - Where the tree data is coming from

    newtreeitemdata = defaultTreeItem()
    # print(treedict["ItemMasterTable"])

    if tree_id is None:
        SelectedTreeItem = SourceSession.query(SourceTree).filter_by(id=id).first()
        newtreeitemdata['id'] = id
    else:
        SelectedTreeItem = SourceSession.query(SourceTree).filter_by(tree_id=tree_id).first()
        newtreeitemdata['id'] = SelectedTreeItem.id

    if SelectedTreeItem is not None:

        newtreeitemdata['ItemName'] = SelectedTreeItem.DisplayName

        # newtreeitemdata['ItemName'] = SelectedTreeItem.NameText

        # if mastertablequery.TableType_id == 11: #Tree Item
        '''if SelectedTreeItem.TreePath is not None:
            newtreeitemdata['TreePath'] = str(SelectedTreeItem.Tree_id) #DatabaseTools.strToMyList(SelectedTreeItem.TreePath)
        else:
            newtreeitemdata['TreePath'] = str(SelectedTreeItem.Tree_id)'''

        newtreeitemdata['PrimaryGroup_id'] = SelectedTreeItem.PrimaryGroup_id
        newtreeitemdata['SecondaryGroup_id'] = SelectedTreeItem.SecondaryGroup_id

        newtreeitemdata['SourcePG'] = SelectedTreeItem.PrimaryGroup_id
        newtreeitemdata['SourceSG'] = SelectedTreeItem.SecondaryGroup_id
        # newtreeitemdata['DestinationPG'] = SelectedTreeItem.DestinationPG
        # newtreeitemdata['SecondaryGroup_id'] = SelectedTreeItem.SecondaryGroup_id
        newtreeitemdata['Tree_id'] = str(SelectedTreeItem.Tree_id)
        newtreeitemdata['ParentTree_id'] = str(SelectedTreeItem.ParentTree_id)
        newtreeitemdata['ItemMaster_id'] = SelectedTreeItem.ItemMaster_id
        newtreeitemdata['ItemTable'] = None

        try:
            newtreeitemdata['ItemTableType_id'] = SelectedTreeItem.ItemTableType_id
        except:
            newtreeitemdata['ItemTableType_id'] = None

        newtreeitemdata['ItemTable_id'] = SelectedTreeItem.ItemTable_id
        newtreeitemdata['Item_id'] = SelectedTreeItem.Item_id
        newtreeitemdata['DisplayName'] = SelectedTreeItem.DisplayName
        try:
            newtreeitemdata['ItemOrder'] = SelectedTreeItem.ItemOrder
        except:
            pass
        # newtreeitemdata['FlattenedOrder'] = SelectedTreeItem.FlattenedOrder
        try:
            newtreeitemdata['ItemLevel'] = SelectedTreeItem.ItemLevel
        except:
            pass

        try:
            newtreeitemdata['ForeColor'] = SelectedTreeItem.ForeColor
        except:
            pass
        # newtreeitemdata['Expanded'] = SelectedTreeItem.Expanded
        try:
            newtreeitemdata['Header'] = SelectedTreeItem.Header
        except:
            pass

        newtag = "(%s-%s)" % (SelectedTreeItem.ItemMaster_id, SelectedTreeItem.Item_id)
        newtreeitemdata['Tags'] = [newtag]

        newtreeitemdata['Date_Created'] = None
        newtreeitemdata['Date_Modified'] = None
        newtreeitemdata['Date_Accessed'] = None
    return newtreeitemdata


def AddTreeRoot(RootName, indexlist, newtreeitemdata=None, LinkedTable=None):
    itemcount = 0
    treeviewindex = 1
    for index in indexlist:
        treeviewindex = index

    currentdatetime = datetime.datetime.now()

    if newtreeitemdata is None:
        newtreeitemdata = {}
        newtreeitemdata['id'] = 0
        newtreeitemdata['TreePath'] = []
        newtreeitemdata['Tree_id'] = None
        newtreeitemdata['PrimaryGroup_id'] = 0
        newtreeitemdata['SourcePG'] = None
        newtreeitemdata['DestinationPG'] = None
        newtreeitemdata['SecondaryGroup_id'] = 0
        newtreeitemdata['SourceSG'] = None
        newtreeitemdata['DestinationSG'] = None
        newtreeitemdata['ParentTree_id'] = ("0")
        newtreeitemdata['ItemTable'] = None
        newtreeitemdata['ItemMaster_id'] = 0
        newtreeitemdata['ItemTableType_id'] = 0
        newtreeitemdata['ItemTable_id'] = 0
        newtreeitemdata['Item_id'] = 0
        newtreeitemdata['ItemName'] = ""
        newtreeitemdata['DisplayName'] = RootName
        newtreeitemdata['ItemOrder'] = 0
        newtreeitemdata['FlattenedOrder'] = 1
        newtreeitemdata['ItemLevel'] = 0
        newtreeitemdata['ForeColor'] = None
        newtreeitemdata['Expanded'] = 0
        newtreeitemdata['Header'] = None
        newtreeitemdata['Tags'] = []
        newtreeitemdata['Date_Created'] = str(currentdatetime)
        newtreeitemdata["id"] = None

    newtreeitemdata['Date_Modified'] = str(currentdatetime)
    newtreeitemdata['Date_Accessed'] = str(currentdatetime)

    # print("Adding Root", newtreeitemdata)
    treeItemDict = addTreeItem(LinkedTable, newtreeitemdata)
    # print("After", treeItemDict)
    # print("Root Tree_id ", treeItemDict["Tree_id"])
    return treeItemDict


def addTreeItem(tableclass, treeItemDict):
    # Adds a tree item to the treemodel from the treeItemDict.
    # If the treeItem has a tree_id it will not create a database entry
    # Create the Tree
    # Add to Database

    # print("Teees", treeItemDict['Tree_id'], treeItemDict['ParentTree_id'])
    # Create the Linked Tree
    currentdatetime = datetime.datetime.now()
    if tableclass is not None:
        treedict["GeneratedSession"].begin(subtransactions=True)
        CreateUpdateAttribute = tableclass(PrimaryGroup_id=int(treeItemDict["PrimaryGroup_id"]),
                                           SecondaryGroup_id=int(treeItemDict["SecondaryGroup_id"]),
                                           ReferenceTreeRecord=treeItemDict["id"],
                                           ParentTree_id=str(treeItemDict["ParentTree_id"]),
                                           TreePath=DatabaseTools.myListToStr(treeItemDict["TreePath"]),
                                           ItemMaster_id=int(treeItemDict["ItemMaster_id"]),
                                           ItemTable_id=int(treeItemDict["ItemTable_id"]),
                                           ItemTableType_id=int(treeItemDict["ItemTableType_id"]),
                                           Item_id=int(treeItemDict["Item_id"]),
                                           DisplayName=treeItemDict["DisplayName"],
                                           ItemOrder=int(treeItemDict["ItemOrder"]),
                                           FlattenedOrder=int(treeItemDict["FlattenedOrder"]),
                                           ItemLevel=int(treeItemDict["ItemLevel"]),
                                           ForeColor=treeItemDict["ForeColor"],
                                           Expanded=int(treeItemDict["Expanded"]),
                                           Tags=DatabaseTools.myListToStr(treeItemDict["Tags"]),
                                           Header=treeItemDict["Header"],
                                           Date_Created=str(currentdatetime),
                                           Date_Modified=str(currentdatetime),
                                           Date_Accessed=str(currentdatetime))
        treedict["GeneratedSession"].add(CreateUpdateAttribute)
        treedict["GeneratedSession"].commit()

        '''Update the Tree_id and ParentTree_id, TreePath needs to updated to the new format
        and Tags if required.'''

        treedict["GeneratedSession"].begin()

        # For combined tables
        if treeItemDict["id"] != None:
            treeItemDict["Tree_id"] = "(%s-%s-%s-%s)" % (
            str(treeItemDict["DestinationPG"]), str(treeItemDict["DestinationSG"]), str(treeItemDict["MasterTable_id"]),
            str(treeItemDict["id"]))
            CreateUpdateAttribute.Tree_id = treeItemDict["Tree_id"]
        else:
            treeItemDict["Tree_id"] = "(%s-%s-%s-%s)" % (
            str(treeItemDict["DestinationPG"]), str(treeItemDict["DestinationSG"]), str(treeItemDict["MasterTable_id"]),
            str(CreateUpdateAttribute.id))
            CreateUpdateAttribute.Tree_id = treeItemDict["Tree_id"]
            treeItemDict["id"] = CreateUpdateAttribute.id

        treepath = treeItemDict["Tree_id"]

        treeItemDict["TreePath"].append(treepath)
        CreateUpdateAttribute.TreePath = DatabaseTools.myListToStr(treeItemDict["TreePath"])

        newtag = "(%s-%s)" % (treeItemDict["ItemTable_id"], treeItemDict["Item_id"])
        treeItemDict['Tags'].append(newtag)
        CreateUpdateAttribute.Tags = DatabaseTools.myListToStr(treeItemDict['Tags'])

        treedict["GeneratedSession"].commit()

    else:  # Recreate Original Tree
        if treeItemDict["ItemTable_id"] is None: treeItemDict["ItemTable_id"] = 0

        treeItemDict["TreePath"].append(treeItemDict["Tree_id"])

        newtag = "(%s-%s)" % (treeItemDict["ItemMaster_id"], treeItemDict["Item_id"])
        treeItemDict['Tags'].append(newtag)

        return treeItemDict


class PyMimeData(QMimeData):
    """ The PyMimeData wraps a Python instance as MIME data.
    """
    # The MIME type for instances.
    MIME_TYPE = "application/x-ets-qt4-instance"

    def __init__(self, data=None):
        """ Initialise the instance.
        """
        QMimeData.__init__(self)

        # Keep a local reference to be returned if possible.
        self._local_instance = data

        if data is not None:
            # We may not be able to pickle the data.
            try:
                pdata = dumps(data)
            except:
                return

                # This format (as opposed to using a single sequence) allows the
                # type to be extracted without unpickling the data itself.
        self.setData(self.MIME_TYPE, dumps(data.__class__) + pdata)

    @classmethod
    def coerce(cls, md):
        """ Coerce a QMimeData instance to a PyMimeData instance if
        possible.
        """
        # See if the data is already of the right type.  If it is then we know
        # we are in the same process.
        if isinstance(md, cls):
            return md

        # See if the data type is supported.
        if not md.hasFormat(cls.MIME_TYPE):
            return None

        nmd = cls()
        nmd.setData(cls.MIME_TYPE, md.data())

        return nmd

    def instance(self):
        """ Return the instance.
        """
        if self._local_instance is not None:
            return self._local_instance

        io = StringIO(str(self.data(self.MIME_TYPE)))

        try:
            # Skip the type.
            load(io)
            # Recreate the instance.
            return load(io)
        except:
            pass

        return None

    def instanceType(self):
        """ Return the type of the instance.
        """
        if self._local_instance is not None:
            return self._local_instance.__class__

        try:
            return loads(str(self.data(self.MIME_TYPE)))
        except:
            pass

        return None


class treeItem_class(object):
    '''
    A Specialized SubClass of the TreeItemBaseClass
    '''

    def __init__(self, treeDict):

        # self.treeDict = treeDict
        # the first should replace everything else in the future.
        # treemodel.currentTreeItem(self, ID=None) would load the dictionary
        self.Record_id = int(treeDict['id'])
        self.Tree_id = str(treeDict['Tree_id'])
        self.TreePath = treeDict['TreePath']

        try:
            self.PrimaryGroup_id = int(treeDict['PrimaryGroup_id'])
            self.SecondaryGroup_id = int(treeDict['SecondaryGroup_id'])
        except:
            pass

        self.ParentTree_id = str(treeDict['ParentTree_id'])
        # self.ItemMaster = treeDict['ItemMasterTable']
        try:
            self.ItemMaster = treeDict['ItemMaster_id']
        except:
            pass
        self.ItemTable = treeDict['ItemTable']
        if treeDict['ItemTable_id'] is not None: self.ItemTable_id = int(treeDict['ItemTable_id'])
        self.Item = treeDict['Item_id']
        self.ItemName = treeDict['ItemName']

        self.Display = []

        if treeDict['DisplayName'] != None:
            DisplayValue = treeDict['DisplayName']
        else:
            DisplayValue = ""

        if self.ItemName != None:
            if str(self.ItemName) != DisplayValue:
                DisplayValue += str(self.ItemName)
        else:
            if str(treeDict['DisplayName']) != DisplayValue:
                DisplayValue += str(treeDict['DisplayName'])

        self.Display.append(DisplayValue)
        self.Order = treeDict['ItemOrder']
        self.FlattenedOrder = treeDict['FlattenedOrder']
        self.Level = treeDict['ItemLevel']
        self.ForeColor = treeDict['ForeColor']
        self.Expanded = treeDict['Expanded']
        self.Header = treeDict['Header']


class treeCategory_class(object):
    '''
    A Specialized SubClass of the TreeItemBaseClass
    '''

    def __init__(self, Tree_id=None, Category=None, Header=None, Display=None):
        self.Tree_id = Tree_id
        self.Category = Category
        self.Header = Header
        self.Display = Display


class sqlStandardItemModel(QStandardItemModel):
    def __init__(self, Parent=None, session=None, tableclass=None, **kwargs):
        super(sqlStandardItemModel, self).__init__(**kwargs)

        self.session = session
        self.TreeGeneratedClass = tableclass
        self.fieldNames = []
        self.fieldNameCount = None
        self.fieldDict = None

        # self.setupModelData()

    def setupModelData2(self):

        records = self.session.query(self.TreeGeneratedClass)
        recordrow = 0
        self.fieldDict = records.keys()

        for record in records:  # cursors are iterable
            for key, value in self.fieldDict:
                self.setItem(recordrow, key, QStandardItem(str(value)))
            recordrow += 1

    def setupModelData(self):

        records = self.session.query(self.TreeGeneratedClass)
        recordrow = 0

        for record in records:  # cursors are iterable]
            self.fieldDict = DatabaseTools.row2dict(record)
            for key, value in enumerate(self.fieldDict):
                if value == "Display":
                    Display = []
                    Display.append(str(record[6]))
                    self.setItem(recordrow, key, QStandardItem(Display[0]))
                else:
                    self.setItem(recordrow, key, QStandardItem(str(value)))
            recordrow += 1

    def data(self, index, role):
        if not index.isValid():
            return
        elif role != Qt.DisplayRole:
            return
        return self.setItem[index.row()][index.column()]

    def headerCount(self):
        return self.fieldNameCount

    def headerData(self, column=0, orientation=Qt.Horizontal, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if len(self.fieldNames) != 0:
                data = self.fieldNames[column]
            else:
                data = "-"
        else:
            data = QAbstractTableModel.headerData(self, column, orientation, role)
        return data

    def CloneBranch(self, ParentID, ParentLevel, CloneID):
        pass


class TreeItem(object):
    '''
    a python object used to return row/column data, and keep note of
    it's parents and/or children
    '''

    def __init__(self, TreeClassItem, Header, parentItem):
        self.TreeClassItem = TreeClassItem
        self.parentItem = parentItem
        self.Header = Header  # This is the display in tree value
        self.Display = []  # These are the additional column items
        self.childItems = []
        self._colors = None
        self.ColumnsViewed = 1
        self.settingDatabase = "DSSettings.db"
        self.settingTable = "tblProgramSettings"

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        # This will have to be updated with the length of the display list
        return self.ColumnsViewed

    def data(self, column):

        '''FileLocation = ProgramSettings.loadDefaultValue(self.settingDatabase, self.settingTable, 1, "Icon Location")
        Filelocation = FileLocation + "Excel.bmp"
        iconQPixmap = QPixmap(FileLocation)'''

        # This Allows a sub class to be put in that can store additional information
        if self.TreeClassItem == None:
            try:
                if column == 0:
                    return self.Header
                if column == 1:
                    return ""

                    return self.Display[column]
            except:
                pass
        else:
            try:
                return self.TreeClassItem.Display[column]
            except:
                pass
        return

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            row = index.row()
            column = index.column()
            ch = (value)

            self.__colors[row][column] = ch
            self.dataChanged.emit(index, index)
            return True

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0


class streeModel(QAbstractItemModel):
    def __init__(self, session, treeviewdict, inParent=None, header="", groupid=0, **kwargs):
        super(streeModel, self).__init__(inParent, **kwargs)

        # self.treeviewdict = {}
        # self.treeviewdict["MasterTreeTable"]: Top Level Tree Grouping (ie on Projects)
        # self.treeviewdict["TreeGroup"]: Second Level Tree Grouping
        # self.treeviewdict["ItemMasterTable"]: Mastertable used in all databases
        # self.treeviewdict["ItemTable"] = Same as Master Table?!?
        # self.treeviewdict["ItemTableType"] = Used for Grouping Items
        # self.treeviewdict["TreeItems"]:The Actual Itemts Use
        # self.treeviewdict["GeneratedTree"]:Used for linking items (Branch Duplication Sycronization)

        '''TreeItems.id
            TreeItems.PrimaryGroup_id
            TreeItems.Tree_id
            TreeItems.ParentTree_id
            TreeItems.ItemTableType_id
            TreeItems.ItemTable_id
            TreeItems.Item_id'''

        self.Display = []
        self.rootItem = TreeItem(None, "ALL", None)
        self.parents = {0: self.rootItem}
        self.session = session

        self.treeviewdict = treeviewdict
        self.PrimaryGroup_id = groupid
        self.fieldNames = []
        self.fieldNameCount = None
        self.fieldDict = None
        # self.Headers =  ("Category", "Item", "Description")
        self.Headers = []
        self.Headers.append(header)

        self.RecordCount = 0

    def defaultTreeItem(self):
        newtreeitemdata = {}
        newtreeitemdata['TreePath'] = []

        newtreeitemdata['PrimaryGroup_id'] = 0
        newtreeitemdata['Tree_id'] = None
        newtreeitemdata['ParentTree_id'] = "0"  # Follows the top item
        newtreeitemdata['ItemTableType_id'] = 0
        newtreeitemdata['ItemName'] = None
        newtreeitemdata['ItemTable'] = None
        newtreeitemdata['ItemTable_id'] = 0
        newtreeitemdata['Item_id'] = 0
        newtreeitemdata['DisplayName'] = None
        newtreeitemdata['ItemOrder'] = 0
        newtreeitemdata['FlattenedOrder'] = 0
        newtreeitemdata['ItemLevel'] = 0
        newtreeitemdata['ForeColor'] = None
        newtreeitemdata['Expanded'] = 0
        newtreeitemdata['Header'] = None
        newtreeitemdata['Tags'] = []
        newtreeitemdata['Date_Created'] = None
        newtreeitemdata['Date_Modified'] = None
        newtreeitemdata['Date_Accessed'] = None

        # newtreeitemdata = self.currentTreeItem(ID=Tree_id)

        # treepath = []
        # treepath.append(Tree_id)
        # newtreeitemdata['TreePath'] = str(DatabaseTools.myListToStr(treepath))
        itemlevel = 0
        # newtreeitemdata['ItemLevel'] = len(treepath) - 1

        return newtreeitemdata

    def currentTreeItem(self, ID=None):

        TreeItems = self.treeviewdict["TreeItems"]
        ItemMasterTable = self.treeviewdict["ItemMasterTable"]
        ItemTable = self.treeviewdict["ItemTable"]

        SelectedTreeItem = self.session.query(TreeItems.id, TreeItems.Tree_id, TreeItems.TreePath,
                                              TreeItems.ParentTree_id) \
            .filter(TreeItems.id == ID).first()

        # newtreeitemdata = dict(SelectedTreeItem)  This way should of worked.

        newtreeitemdata = self.defaultTreeItem()
        if SelectedTreeItem.TreePath is not None:
            newtreeitemdata['TreePath'] = DatabaseTools.strToMyList(SelectedTreeItem.TreePath)
        else:
            newtreeitemdata['TreePath'] = []

        newtreeitemdata['PrimaryGroup_id'] = SelectedTreeItem.PrimaryGroup_id
        newtreeitemdata['Tree_id'] = SelectedTreeItem.Tree_id
        newtreeitemdata['ParentTree_id'] = SelectedTreeItem.ParentTree_id

        newtreeitemdata['ItemTableType_id'] = SelectedTreeItem.ItemTableType_id
        newtreeitemdata['ItemName'] = None
        newtreeitemdata['ItemTable'] = None
        newtreeitemdata['ItemTable_id'] = SelectedTreeItem.ItemTable_id
        newtreeitemdata['Item_id'] = SelectedTreeItem.Item_id
        newtreeitemdata['ItemOrder'] = SelectedTreeItem.ItemOrder
        # newtreeitemdata['FlattenedOrder'] = SelectedTreeItem.FlattenedOrder
        newtreeitemdata['ItemLevel'] = SelectedTreeItem.ItemLevel
        newtreeitemdata['ForeColor'] = SelectedTreeItem.ForeColor
        # newtreeitemdata['Expanded'] = SelectedTreeItem.Expanded
        newtreeitemdata['Header'] = SelectedTreeItem.Header

        if SelectedTreeItem.Tags is not None:
            newtreeitemdata['Tags'] = DatabaseTools.strToMyList(SelectedTreeItem.Tags)
        else:
            newtreeitemdata['Tags'] = []

        newtreeitemdata['Date_Created'] = None
        newtreeitemdata['Date_Modified'] = None
        newtreeitemdata['Date_Accessed'] = None

        return newtreeitemdata

    def AddTreeRoot(self, RootName, indexlist, PrimaryGroup_id, newtreeitemdata=None):

        itemcount = 0
        treeviewindex = 1
        for index in indexlist:
            treeviewindex = index

        currentdatetime = datetime.datetime.now()

        if newtreeitemdata is None:
            newtreeitemdata = {}
            newtreeitemdata['TreePath'] = []
            newtreeitemdata['Tree_id'] = None
            newtreeitemdata['PrimaryGroup_id'] = PrimaryGroup_id
            newtreeitemdata['ParentTree_id'] = "0"
            newtreeitemdata['ItemMaster'] = None
            newtreeitemdata['ItemMasterTable'] = 0
            newtreeitemdata['ItemMaster_id'] = 1
            newtreeitemdata['ItemName'] = ""
            newtreeitemdata['ItemTable'] = None
            newtreeitemdata['ItemTable_id'] = 0
            newtreeitemdata['ItemTableType_id'] = 0
            newtreeitemdata['Item_id'] = 0
            newtreeitemdata['DisplayName'] = RootName
            newtreeitemdata['ItemOrder'] = 0
            newtreeitemdata['FlattenedOrder'] = 1
            newtreeitemdata['ItemLevel'] = 0
            newtreeitemdata['ForeColor'] = None
            newtreeitemdata['Expanded'] = 0
            newtreeitemdata['Header'] = None
            newtreeitemdata['Tags'] = []
            newtreeitemdata['Date_Created'] = str(currentdatetime)

        newtreeitemdata['Date_Modified'] = str(currentdatetime)
        newtreeitemdata['Date_Accessed'] = str(currentdatetime)

        ActivityTypeParentID = self.addTreeItem(self.treeviewdict["TreeItems"], newtreeitemdata)
        return ActivityTypeParentID

    def addTreeItem(self, tableclass, treeItemDict):
        currentdatetime = datetime.datetime.now()

        # print("AttributeTableTypeID", tableDict["AttributeTableType_id"])
        # CreateUpdateAttribute = self.session.query(self.TreeItems).filter(self.TreeItems.id==tableDict["Item_id"]).first()
        CreateUpdateAttribute = None
        # print("Adding Tree Items", treeItemDict)
        if CreateUpdateAttribute is None:
            self.session.begin(subtransactions=True)
            CreateUpdateAttribute = tableclass(PrimaryGroup_id=int(treeItemDict["PrimaryGroup_id"]),
                                               ParentTree_id=int(treeItemDict["ParentTree_id"]),
                                               TreePath=DatabaseTools.myListToStr(treeItemDict["TreePath"]),
                                               ItemMaster_id=int(treeItemDict["ItemMaster_id"]),
                                               ItemTableType_id=int(treeItemDict["ItemTableType_id"]),
                                               ItemTable_id=int(treeItemDict["ItemTable_id"]),
                                               Item_id=int(treeItemDict["Item_id"]),
                                               DisplayName=treeItemDict["DisplayName"],
                                               ItemOrder=int(treeItemDict["ItemOrder"]),
                                               FlattenedOrder=int(treeItemDict["FlattenedOrder"]),
                                               ItemLevel=int(treeItemDict["ItemLevel"]),
                                               ForeColor=treeItemDict["ForeColor"],
                                               Expanded=int(treeItemDict["Expanded"]),
                                               Tags=DatabaseTools.myListToStr(treeItemDict["Tags"]),
                                               Header=treeItemDict["Header"],
                                               Date_Created=str(currentdatetime),
                                               Date_Modified=str(currentdatetime),
                                               Date_Accessed=str(currentdatetime))
            self.session.add(CreateUpdateAttribute)
            self.session.commit()
        else:
            # print("Updating")
            CreateUpdateAttribute.FieldName = treeItemDict["FieldName"]
            CreateUpdateAttribute.AttributeValue = treeItemDict["Value"],
            CreateUpdateAttribute.AttributeOrder = 0
            # Will Make this generic when we make generic attribute case

        self.session.begin()
        if treeItemDict["Tree_id"] is not None:
            CreateUpdateAttribute.Tree_id = treeItemDict["Tree_id"]
        else:
            treeItemDict["Tree_id"] = CreateUpdateAttribute.id
            CreateUpdateAttribute.Tree_id = CreateUpdateAttribute.id

        treeItemDict["TreePath"].append(treeItemDict["Tree_id"])
        CreateUpdateAttribute.TreePath = DatabaseTools.myListToStr(treeItemDict["TreePath"])

        CreateUpdateAttribute.Tags = DatabaseTools.myListToStr(treeItemDict["Tags"])

        self.session.commit()
        # print(treeItemDict)
        TIC = treeItem_class(treeItemDict)
        # print("level", treeItemDict['ItemLevel'])

        if treeItemDict['ItemLevel'] == 0:
            # Root Level Entries
            newparent = TreeItem(TIC, treeItemDict['Header'], self.rootItem)
            self.rootItem.appendChild(newparent)
            # Create the Dictonary Linking Values
            self.parents[CreateUpdateAttribute.Tree_id] = newparent
        else:
            # print("parent", treeItemDict['ParentTree_id'])
            # print(self.parents)
            parentItem = self.parents[int(treeItemDict['ParentTree_id'])]
            newItem = TreeItem(TIC, treeItemDict['Header'], parentItem)

            parentItem.appendChild(newItem)
            self.parents[CreateUpdateAttribute.Tree_id] = newItem
            # self.insertRow(0, currentSelectedIndex)
        return CreateUpdateAttribute.Tree_id

    def root(self):
        return self.parents[0].internalPointer()

    def insertRow(self, row, parent):
        return self.insertRows(row, 1, parent)

    def insertRows(self, row, count, parent):
        self.beginInsertRows(parent, row, (row + (count - 1)))
        self.endInsertRows()
        return True

    def removeRow(self, row, parentIndex):
        return self.removeRows(row, 1, parentIndex)

    def removeRows(self, row, count, parentIndex):
        self.beginRemoveRows(parentIndex, row, row)
        node = self.nodeFromIndex(parentIndex)
        node.removeChild(row)
        self.endRemoveRows()
        return True

    def setupModelData(self, Tree_id, Group_id=None):

        newtreeitemdata = self.currentTreeItem(ID=Tree_id)

        self.session.begin()
        treerecords = self.session.query(self.treeviewdict["GeneratedTree"])
        if treerecords is not None:
            treerecords.delete(synchronize_session=False)
        self.session.commit()

        treepath = []
        treepath.append(Tree_id)
        newtreeitemdata['TreePath'] = treepath  # str(DatabaseTools.myListToStr(treepath))
        itemlevel = 0
        newtreeitemdata['ItemLevel'] = len(treepath) - 1
        # print(newtreeitemdata)
        DynamicParentID = self.addTreeItem(self.treeviewdict["GeneratedTree"], newtreeitemdata)
        ParentID = newtreeitemdata['Tree_id']

        self.tvtreebranch(treepath, Group_id, ParentID)

    def setupModelData2(self, Tree_id, Group_id=None):

        newtreeitemdata = self.currentTreeItem(ID=Tree_id)

        if self.treeviewdict["GeneratedTree"] != self.treeviewdict["TreeItems"]:
            self.session.begin()
            treerecords = self.session.query(self.treeviewdict["GeneratedTree"])
            if treerecords is not None:
                treerecords.delete(synchronize_session=False)
            self.session.commit()

        treepath = []
        treepath.append(Tree_id)
        newtreeitemdata['TreePath'] = treepath  # str(DatabaseTools.myListToStr(treepath))
        itemlevel = 0
        newtreeitemdata['ItemLevel'] = len(treepath) - 1
        DynamicParentID = self.addTreeItem(self.treeviewdict["GeneratedTree"], newtreeitemdata)
        ParentID = newtreeitemdata['Tree_id']

        self.tvtreebranch(treepath, Group_id, ParentID)

    def tvtreebranch(self, treepath, Group_id, ParentID):

        # Load the table data that have parents that match the ParentID
        records2 = self.session.query(self.treeviewdict["TreeItems"]).filter_by(PrimaryGroup_id=int(Group_id)) \
            .filter_by(ParentTree_id=int(ParentID)). \
            order_by("DisplayName").all()

        rowcount = 0
        treeviewindex = 1  # todo... or this

        for row, record2 in enumerate(records2):
            self.RecordCount += 1
            # Initialize the Data

            newtreeitemdata = self.currentTreeItem(ID=record2.Tree_id)

            treepath2 = treepath.copy()
            treepath2.append(str(newtreeitemdata['Tree_id']))
            newtreeitemdata['TreePath'] = treepath2  # DatabaseTools.myListToStr(treepath2)
            newtreeitemdata['ItemLevel'] = len(treepath2) - 1
            newtreeitemdata['ItemOrder'] = self.RecordCount
            # y = newtreeitemdata['Tree_id']
            # z = newtreeitemdata['ParentTree_id']
            # print(y, z)

            DynamicParentID = self.addTreeItem(self.treeviewdict["GeneratedTree"], newtreeitemdata)

            # Checking for presence of child items.
            records3 = self.session.query(self.treeviewdict["TreeItems"]).filter_by(PrimaryGroup_id=int(Group_id)) \
                .filter_by(ParentTree_id=int(newtreeitemdata['Tree_id'])).all()
            if records3 is not None:
                self.tvtreebranch(treepath2, Group_id, newtreeitemdata['Tree_id'])

    def mimeTypes(self):
        types = QListWidget
        types.append('application/x-ets-qt4-instance')
        return types

    def mimeData(self, index):
        node = self.nodeFromIndex(index[0])
        mimeData = PyMimeData(node)
        return mimeData

    def dropMimeData(self, mimedata, action, row, column, parentIndex):
        if action == Qt.IgnoreAction:
            return True

        dragNode = mimedata.instance()
        parentNode = self.nodeFromIndex(parentIndex)

        # make an copy of the node being moved
        newNode = deepcopy(dragNode)
        newNode.setParent(parentNode)
        self.insertRow(len(parentNode) - 1, parentIndex)
        # self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),parentIndex, parentIndex)
        return True

    def columnCount(self, parent=None):
        if parent and parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return len(self.Headers)

    def recordCount(self):
        return self.RecordCount

    def data(self, index, role):
        if not index.isValid():
            return

        item = index.internalPointer()
        if role == Qt.DisplayRole:
            try:
                return item.data(index.column())
            except:
                pass

        if role == Qt.UserRole:
            if item:
                return item.Header
        return

    def returnHeaderData(self):
        SQLQuery = 'select * from %s' % (self.datatable)

    def headerData(self, column, orientation, role):
        if (orientation == Qt.Horizontal and
                role == Qt.DisplayRole):
            try:
                return self.Headers[column]
            except IndexError:
                pass

        return

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        if not childItem:
            return QModelIndex()

        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent=QModelIndex()):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            p_Item = self.rootItem
        else:
            p_Item = parent.internalPointer()
        return p_Item.childCount()

    def treeTableModel(self, SWhere=None, Orientation="Vertical"):
        modelData = QAbstractItemModel

        records = self.session.query(self.TreeGeneratedClass)
        recordrow = 0
        self.fieldDict = records.keys()

        if Orientation == "Vertical":
            recordrow = 0
            for record in records:  # cursors are iterable
                for key in self.fieldDict:
                    modelData.setItem(recordrow, key, QStandardItem(str(record[key])))
                recordrow += 1

            # Header Data
            modelData.sort(3, Qt.AscendingOrder)

            fieldColumn = 0
            for key, value in self.fieldDict:
                # print(headerName[0])
                modelData.setHeaderData(key, Qt.Horizontal, value, role=Qt.DisplayRole)
                fieldColumn += 1
        else:
            recordcolumn = 0
            for record in records:  # cursors are iterable
                for key, value in self.fieldDict:
                    modelData.setItem(key, recordcolumn, QStandardItem(str(record[key])))
                recordcolumn += 1
        return modelData

    def searchModel(self, treepath):
        '''
        get the modelIndex for a given appointment
        '''

        def searchNode(node):
            '''
            a function called recursively, looking at all nodes beneath node
            '''
            for child in node.childItems:
                if treepath == child.TreeClassItem.TreePath:
                    index = self.createIndex(child.row(), 0, child)
                    return index

                if child.childCount() > 0:
                    result = searchNode(child)
                    if result:
                        return result

        retarg = searchNode(self.parents[0])
        return retarg

    def find_Tree_Branch(self, cname):
        app = None
        for category in self.categories:
            if category.cname == cname:
                app = category
                break
        if app != None:
            index = self.searchModel(app)
            return (True, index)
        return (False, None)

    def paintEvent(self, event):
        painter = QPainter(
            self.viewport())  # See: http://stackoverflow.com/questions/12226930/overriding-qpaintevents-in-pyqt
        painter.drawEllipse(self.center, 10, 10)
        QTableWidget.paintEvent(self, event)

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        index = self.indexAt(event.pos())
        sellst = self.selectedList()
        if index.isValid():
            target_node = index.internalPointer().node
            dragged_nodes, drag_type, qdrag = self.drag
            # I don't think we need qdrag for anything, but it can't hurt.
            if target_node.drop_on_ok(drag_type, dragged_nodes):
                self.selectNodes(sellst, but_not=dragged_nodes)
                target_node.drop_on(drag_type, dragged_nodes)
                event.acceptProposedAction()
                self.mt_update()
                self.drag = None
                return
        event.ignore()
        self.mt_update()
        self.drag = None

    def mouseMoveEvent(self, event):
        if self.drag is not None:
            pass  # QTreeView.mouseMoveEvent(self, event)
            return
        if ((event.globalPos() - self.mouse_press_qpoint).manhattanLength()
                < QApplication.startDragDistance()):
            return
        #
        # starting a drag
        # [logic bug, after bruce change 070507: should not do this
        #  if we already started dragging out a selection. How can we tell?
        #  Only by whether the initial press had eventInRect, I think
        #  (not yet recorded), or at least, the initial move (#e could record here).]
        #
        index = self.indexAt(event.pos())

        sellst = self.selectedList()  # bruce 070507 move earlier

        DEBUG2 = True

        if index.isValid():
            thisnode = index.internalPointer().node

            # bruce 070507 bring in some code from modelTreeGui.py
            alreadySelected = (thisnode in sellst)

            item = index.internalPointer()
            rect = self.visualRect(index)
            if DEBUG2:
                print("visualRect coords", rect.left(), rect.right(), rect.top(), rect.bottom())
            # qfm = QFontMetrics(QLineEdit(self).font())
            # rect.setWidth(qfm.width(item.node.NameText) + _ICONSIZE[0] + 4)
            if DEBUG2:
                print("visualRect coords, modified:", rect.left(), rect.right(), rect.top(), rect.bottom())
                # looks like icon and text, a bit taller than text (guesses)
            eventInRect = rect.contains(event.pos())
            if DEBUG2:
                print("valid index: eventInRect = %r, item = %r, index = %r, alreadySelected = %r" % \
                      (eventInRect, item, index, alreadySelected))  #######
        else:
            thisnode = item = None
            alreadySelected = eventInRect = False

        if not eventInRect:
            # nothing to drag, but [bruce 070507] let super handle it (for dragging over nodes to select)
            self.drag_is_not_DND = True  ### not yet used
            # QTreeView.mouseMoveEvent(self, event)
            return

        if thisnode in sellst:
            # if dragging something selected, drag along all other selected ones
            dragged_nodes = sellst
        else:
            # if dragging something unselected, ignore any selected ones
            dragged_nodes = [thisnode]
        qdrag = QDrag(self)
        drag_type = 'move'  # how do I decide between 'move' and 'copy'?
        self.drag = (dragged_nodes, drag_type, qdrag)
        mimedata = QMimeData()
        mimedata.setText("need a string here for a valid mimetype")
        qdrag.setMimeData(mimedata)
        display_prefs = {}
        pixmap = dragged_nodes[0].node_icon(display_prefs)
        qdrag.setPixmap(pixmap)
        qdrag.setHotSpot(QPoint(-8, 8))
        qdrag.start()

    def mousePressEvent(self, event):
        self.drag_is_not_DND = False  # don't know yet
        qp = event.globalPos()  # clone the point to keep it constant
        self.mouse_press_qpoint = QPoint(qp.x(), qp.y())
        self.mouse_press_event = QMouseEvent(event.type(),
                                             QPoint(event.x(), event.y()),
                                             event.button(), event.buttons(),
                                             event.modifiers())

    def mouseReleaseEvent(self, event):
        self.drag_is_not_DND = False
        if self.drag is None:
            pass
            # QTreeView.mousePressEvent(self, self.mouse_press_event)
        self.drag = None
        # QTreeView.mouseReleaseEvent(self, event)

    def contextMenuEvent(self, event):
        # menu = QMenu(self)
        pos = event.pos()
        index = self.indexAt(pos)
        if index.isValid():
            item = self.indexAt(pos).internalPointer()
            node = self.item_to_node_dict[item]
            nodeset = [node]  # ? ? ? ?
            optflag = False  # ? ? ? ?
            cmenu_spec = self.treemodel.make_cmenuspec_for_set(nodeset, optflag)
            for x in cmenu_spec:
                if x is not None:
                    str, thunk = x[:2]
                    # act = QAction(str, self)
                    # act.setEnabled("disabled" not in x[2:])
                    # self.connect(act, SIGNAL("triggered()"), thunk)
                    # menu.addAction(act)
                    pass
                else:
                    pass
                    # menu.addSeparator()
                    # menu.exec_(event.globalPos())

    def flags(self, index):
        # Qt.ItemIsEnabled|Qt.ItemIsEditable|Qt.ItemIsSelectable
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable


class linkedtreemodel(QAbstractItemModel):
    def __init__(self, masterdata, treeviewdict, inParent=None, header="", SourcePG=0, DestinationPG=None,
                 linkeditemlist=None, **kwargs):
        super(linkedtreemodel, self).__init__(inParent, **kwargs)

        '''TreeItems.id
            TreeItems.PrimaryGroup_id
            TreeItems.SecondaryGroup_id
            TreeItems.Tree_id
            TreeItems.ParentTree_id
            TreeItems.ItemTable_id
            TreeItems.Item_id
            TreeItems.DisplayName
            TreeItems.ItemOrder
            TreeItems.FlattenedOrder
            TreeItems.ItemLevel
            TreeItems.ForeColor
            TreeItems.Expanded
            TreeItems.Header
            TreeItems.Tags'''

        self.Display = []
        self.rootItem = TreeItem(None, "ALL", None)
        self.parents = {"0": self.rootItem}

        self.MasterData = masterdata
        #self.bases = masterdata.basedict
        #self.sessions = masterdata.sessiondict
        self.treeviewdict = treeviewdict
        self.SourcePG = SourcePG
        self.DestinationSG = 0
        self.DestinationPG = DestinationPG
        self.DestinationSG = 0
        self.DestinationG = None
        self.fieldNames = []
        self.fieldNameCount = None
        self.fieldDict = None
        # self.Headers =  ("Category", "Item", "Description")
        self.Headers = []
        self.Headers.append(header)

        self.RecordCount = 0

    def clearGenerated(self):
        if treeviewdict["GeneratedTree"] is not None:
            self.treeviewdict["GeneratedSession"].begin()
            treerecords = self.treeviewdict["GeneratedSession"].query(treeviewdict["GeneratedTree"])
            if treerecords is not None:
                treerecords.delete(synchronize_session=False)
            self.treeviewdict["GeneratedSession"].commit()

    def defaultTreeItem(self):
        newtreeitemdata = {}
        newtreeitemdata['TreePath'] = []
        newtreeitemdata['PrimaryGroup_id'] = 0
        newtreeitemdata['SourcePG'] = 1
        newtreeitemdata['DestinationPG'] = 1
        newtreeitemdata['SourceSG'] = 1
        newtreeitemdata['DestinationSG'] = 1
        newtreeitemdata['SecondaryGroup_id'] = 1
        newtreeitemdata['Tree_id'] = None
        newtreeitemdata['LinkedTree_id'] = None
        newtreeitemdata['ParentTree_id'] = "0"  # Follows the top item
        newtreeitemdata['ItemTable'] = None
        newtreeitemdata['ItemTable_id'] = 0
        newtreeitemdata['ItemMaster_id'] = 0
        newtreeitemdata['ItemTable'] = None
        newtreeitemdata['ItemTableType_id'] = 0
        newtreeitemdata['Item_id'] = 0
        newtreeitemdata['ItemName'] = None
        newtreeitemdata['DisplayName'] = None
        newtreeitemdata['ItemOrder'] = 0
        newtreeitemdata['FlattenedOrder'] = 0
        newtreeitemdata['ItemLevel'] = 0
        newtreeitemdata['ForeColor'] = None
        newtreeitemdata['Expanded'] = 0
        newtreeitemdata['Header'] = None
        newtreeitemdata['Tags'] = []
        newtreeitemdata['Date_Created'] = None
        newtreeitemdata['Date_Modified'] = None
        newtreeitemdata['Date_Accessed'] = None

        # newtreeitemdata = self.currentTreeItem(ID=Tree_id)

        # treepath = []
        # treepath.append(Tree_id)
        # newtreeitemdata['TreePath'] = str(DatabaseTools.myListToStr(treepath))
        itemlevel = 0
        # newtreeitemdata['ItemLevel'] = len(treepath) - 1

        return newtreeitemdata

    def treeItemFromdb(self, SourceSession, SourceTree, id, SourceTable_id, tree_id=None, ItemColumnName="Tree_id"):
        # todo the id and tree_id are not the same
        # Creates a tree item from the data
        # Can be a list table or tree table
        # TreeClass - Where the tree data is coming from

        newtreeitemdata = self.defaultTreeItem()
        # print(self.treeviewdict["ItemMasterTable"])

        if tree_id is None:
            SelectedTreeItem = SourceSession.query(SourceTree).filter_by(id=id).first()
            newtreeitemdata['id'] = id
        else:
            ItemColumn = getattr(SourceTree, ItemColumnName)
            SelectedTreeItem = SourceSession.query(SourceTree).filter_by(ItemColumn=tree_id).first()
            newtreeitemdata['id'] = SelectedTreeItem.id

        if SelectedTreeItem is not None:

            newtreeitemdata['ItemName'] = SelectedTreeItem.DisplayName

            # newtreeitemdata['ItemName'] = SelectedTreeItem.NameText

            # if mastertablequery.TableType_id == 11: #Tree Item
            '''if SelectedTreeItem.TreePath is not None:
                newtreeitemdata['TreePath'] = str(SelectedTreeItem.Tree_id) #DatabaseTools.strToMyList(SelectedTreeItem.TreePath)
            else:
                newtreeitemdata['TreePath'] = str(SelectedTreeItem.Tree_id)'''

            newtreeitemdata['PrimaryGroup_id'] = SelectedTreeItem.PrimaryGroup_id
            newtreeitemdata['SecondaryGroup_id'] = SelectedTreeItem.SecondaryGroup_id

            newtreeitemdata['SourcePG'] = SelectedTreeItem.PrimaryGroup_id
            newtreeitemdata['SourceSG'] = SelectedTreeItem.SecondaryGroup_id
            # newtreeitemdata['DestinationPG'] = SelectedTreeItem.DestinationPG
            # newtreeitemdata['SecondaryGroup_id'] = SelectedTreeItem.SecondaryGroup_id
            newtreeitemdata['Tree_id'] = str(SelectedTreeItem.Tree_id)
            newtreeitemdata['LinkedTree_id'] = SelectedTreeItem.LinkedTree_id
            newtreeitemdata['ParentTree_id'] = str(SelectedTreeItem.ParentTree_id)
            newtreeitemdata['ItemMaster_id'] = SelectedTreeItem.ItemMaster_id
            newtreeitemdata['ItemTable'] = None

            try:
                newtreeitemdata['ItemTableType_id'] = SelectedTreeItem.ItemTableType_id
            except:
                newtreeitemdata['ItemTableType_id'] = None

            newtreeitemdata['ItemTable_id'] = SelectedTreeItem.ItemTable_id
            newtreeitemdata['Item_id'] = SelectedTreeItem.Item_id
            newtreeitemdata['DisplayName'] = SelectedTreeItem.DisplayName
            try:
                newtreeitemdata['ItemOrder'] = SelectedTreeItem.ItemOrder
            except:
                pass
            # newtreeitemdata['FlattenedOrder'] = SelectedTreeItem.FlattenedOrder
            try:
                newtreeitemdata['ItemLevel'] = SelectedTreeItem.ItemLevel
            except:
                pass

            try:
                newtreeitemdata['ForeColor'] = SelectedTreeItem.ForeColor
            except:
                pass
            # newtreeitemdata['Expanded'] = SelectedTreeItem.Expanded
            try:
                newtreeitemdata['Header'] = SelectedTreeItem.Header
            except:
                pass

            newtag = "(%s-%s)" % (SelectedTreeItem.ItemMaster_id, SelectedTreeItem.Item_id)
            newtreeitemdata['Tags'] = [newtag]

            newtreeitemdata['Date_Created'] = None
            newtreeitemdata['Date_Modified'] = None
            newtreeitemdata['Date_Accessed'] = None
        return newtreeitemdata

    def AddTreeRoot(self, RootName, indexlist, newtreeitemdata=None, LinkedTable=None):

        itemcount = 0
        treeviewindex = 1
        for index in indexlist:
            treeviewindex = index

        currentdatetime = datetime.datetime.now()

        if newtreeitemdata is None:
            newtreeitemdata = {}
            newtreeitemdata['id'] = 0
            newtreeitemdata['TreePath'] = []
            newtreeitemdata['Tree_id'] = None
            newtreeitemdata['PrimaryGroup_id'] = 0
            newtreeitemdata['SourcePG'] = None
            newtreeitemdata['DestinationPG'] = None
            newtreeitemdata['SecondaryGroup_id'] = 0
            newtreeitemdata['SourceSG'] = None
            newtreeitemdata['DestinationSG'] = None
            newtreeitemdata['ParentTree_id'] = ("0")
            newtreeitemdata['ItemTable'] = None
            newtreeitemdata['ItemMaster_id'] = 0
            newtreeitemdata['ItemTableType_id'] = 0
            newtreeitemdata['ItemTable_id'] = 0
            newtreeitemdata['Item_id'] = 0
            newtreeitemdata['ItemName'] = ""
            newtreeitemdata['DisplayName'] = RootName
            newtreeitemdata['ItemOrder'] = 0
            newtreeitemdata['FlattenedOrder'] = 1
            newtreeitemdata['ItemLevel'] = 0
            newtreeitemdata['ForeColor'] = None
            newtreeitemdata['Expanded'] = 0
            newtreeitemdata['Header'] = None
            newtreeitemdata['Tags'] = []
            newtreeitemdata['Date_Created'] = str(currentdatetime)
            newtreeitemdata["id"] = None

        newtreeitemdata['Date_Modified'] = str(currentdatetime)
        newtreeitemdata['Date_Accessed'] = str(currentdatetime)

        # print("Adding Root", newtreeitemdata)
        treeItemDict = self.addTreeItem(LinkedTable, newtreeitemdata)
        # print("After", treeItemDict)
        # print("Root Tree_id ", treeItemDict["Tree_id"])
        return treeItemDict

    def addTreeItem(self, tableclass, treeItemDict):
        # Adds a tree item to the treemodel from the treeItemDict.
        # If the treeItem has a tree_id it will not create a database entry
        # Create the Tree
        # Add to Database

        # print("Teees", treeItemDict['Tree_id'], treeItemDict['ParentTree_id'])
        # Create the Linked Tree
        currentdatetime = datetime.datetime.now()
        if tableclass is not None:
            self.treeviewdict["GeneratedSession"].begin(subtransactions=True)
            CreateUpdateAttribute = tableclass(PrimaryGroup_id=int(treeItemDict["PrimaryGroup_id"]),
                                               SecondaryGroup_id=int(treeItemDict["SecondaryGroup_id"]),
                                               ReferenceTreeRecord=treeItemDict["id"],
                                               ParentTree_id=str(treeItemDict["ParentTree_id"]),
                                               TreePath=DatabaseTools.myListToStr(treeItemDict["TreePath"]),
                                               ItemMaster_id=int(treeItemDict["ItemMaster_id"]),
                                               ItemTable_id=int(treeItemDict["ItemTable_id"]),
                                               ItemTableType_id=int(treeItemDict["ItemTableType_id"]),
                                               Item_id=int(treeItemDict["Item_id"]),
                                               DisplayName=treeItemDict["DisplayName"],
                                               ItemOrder=int(treeItemDict["ItemOrder"]),
                                               FlattenedOrder=int(treeItemDict["FlattenedOrder"]),
                                               ItemLevel=int(treeItemDict["ItemLevel"]),
                                               ForeColor=treeItemDict["ForeColor"],
                                               Expanded=int(treeItemDict["Expanded"]),
                                               Tags=DatabaseTools.myListToStr(treeItemDict["Tags"]),
                                               Header=treeItemDict["Header"],
                                               Date_Created=str(currentdatetime),
                                               Date_Modified=str(currentdatetime),
                                               Date_Accessed=str(currentdatetime))
            self.treeviewdict["GeneratedSession"].add(CreateUpdateAttribute)
            self.treeviewdict["GeneratedSession"].commit()

            '''Update the Tree_id and ParentTree_id, TreePath needs to updated to the new format
            and Tags if required.'''

            self.treeviewdict["GeneratedSession"].begin()

            # For combined tables
            if treeItemDict["id"] != None:
                treeItemDict["Tree_id"] = "(%s-%s-%s-%s)" % (
                str(treeItemDict["DestinationPG"]), str(treeItemDict["DestinationSG"]),
                str(treeItemDict["MasterTable_id"]), str(treeItemDict["id"]))
                CreateUpdateAttribute.Tree_id = treeItemDict["Tree_id"]
            else:
                treeItemDict["Tree_id"] = "(%s-%s-%s-%s)" % (
                str(treeItemDict["DestinationPG"]), str(treeItemDict["DestinationSG"]),
                str(treeItemDict["MasterTable_id"]), str(CreateUpdateAttribute.id))
                CreateUpdateAttribute.Tree_id = treeItemDict["Tree_id"]
                treeItemDict["id"] = CreateUpdateAttribute.id

            treepath = treeItemDict["Tree_id"]

            treeItemDict["TreePath"].append(treepath)
            CreateUpdateAttribute.TreePath = DatabaseTools.myListToStr(treeItemDict["TreePath"])

            newtag = "(%s-%s)" % (treeItemDict["ItemTable_id"], treeItemDict["Item_id"])
            treeItemDict['Tags'].append(newtag)
            CreateUpdateAttribute.Tags = DatabaseTools.myListToStr(treeItemDict['Tags'])

            self.treeviewdict["GeneratedSession"].commit()

            # print(treeItemDict)
            TIC = treeItem_class(treeItemDict)
            # print("level", treeItemDict['ItemLevel'], treeItemDict['Tree_id'], treeItemDict['ParentTree_id'])

            if treeItemDict['ItemLevel'] == 0:
                # Root Level Entries

                newparent = TreeItem(TIC, treeItemDict['Header'], self.rootItem)
                self.rootItem.appendChild(newparent)
                # Create the Dictonary Linking Values
                self.parents[str(CreateUpdateAttribute.Tree_id)] = newparent
            else:
                try:
                    parentItem = self.parents[str(treeItemDict['ParentTree_id'])]
                    newItem = TreeItem(TIC, treeItemDict['Header'], parentItem)
                    parentItem.appendChild(newItem)
                    self.parents[str(CreateUpdateAttribute.Tree_id)] = newItem
                except:
                    print("Cant Find Parent", str(treeItemDict['ParentTree_id']))
            return treeItemDict
        else:  # Recreate Original Tree
            if treeItemDict["ItemTable_id"] is None: treeItemDict["ItemTable_id"] = 0

            treeItemDict["TreePath"].append(treeItemDict["Tree_id"])

            newtag = "(%s-%s)" % (treeItemDict["ItemMaster_id"], treeItemDict["Item_id"])

            treeItemDict['Tags'].append(newtag)
            # treeItemDict["DisplayName"]="3432"
            TIC = treeItem_class(treeItemDict)
            if treeItemDict['ItemLevel'] == 0:
                # Root Level Entries
                newparent = TreeItem(TIC, treeItemDict['Header'], self.rootItem)
                self.rootItem.appendChild(newparent)
                # Create the Dictonary Linking Values
                self.parents[str(treeItemDict["Tree_id"])] = newparent
            else:
                parentItem = self.parents[str(treeItemDict['ParentTree_id'])]
                newItem = TreeItem(TIC, treeItemDict['Header'], parentItem)
                # self.rootItem.appendChild(newItem)
                parentItem.appendChild(newItem)
                self.parents[str(treeItemDict["Tree_id"])] = newItem

            return treeItemDict

    def setupModelData(self, SourceSession, SourceTree, IndexList=None, Parent_id="(0)",
                       ParentColumnName="ParentTree_id", ItemColumnName="Tree_id"):

        if type(id) is not list:
            baseidlist = []
            baseidlist.append(id)
        else:
            baseidlist = id

        for baseitem_id in IndexList:
            # Changed ItemID to rootid
            newtreeitemdata = self.treeItemFromdb(SourceSession, SourceTree, int(baseitem_id["root_id"]),
                                                  self.treeviewdict["MasterTable"])

            newtreeitemdata['ItemLevel'] = 0
            newtreeitemdata['TreePath'] = []
            newtreeitemdata["ParentTree_id"] = ""

            newtreeitemdata2 = self.AddTreeRoot("Ginger", [], newtreeitemdata=newtreeitemdata, LinkedTable=None)

            mastertablequery = self.sessions["PackageManager"].query(self.treeviewdict["MasterTable"]).filter_by(
                id=self.treeviewdict["MasterTable_id"]).first()
            self.readtvtreebranch(newtreeitemdata2["TreePath"], newtreeitemdata2["Tags"], newtreeitemdata2["Tree_id"],
                                  0, newtreeitemdata2["id"], ParentColumnName, ItemColumnName)

    def readtvtreebranch(self, treepath, taglist, Parent_id, ItemLevel, Tree_id=None, ParentColumnName="ParentTree_id",
                         ItemColumnName="Tree_id"):
        # parentid = Parent_id.split("-")
        # Load the table data that have parents that match the ParentID
        # May need to filter by primary and secondary ID

        # This allows for us to use other columns as parent child relationships
        ParentColumn = getattr(self.treeviewdict["TreeItems"], ParentColumnName)
        ItemColumn = getattr(self.treeviewdict["TreeItems"], ItemColumnName)

        records2 = self.treeviewdict["Session"].query(self.treeviewdict["TreeItems"]).filter(
            ParentColumn == str(Parent_id)).order_by("ItemOrder").all()

        '''if Tree_id is None:
            records2 = self.treeviewdict["Session"].query(self.treeviewdict["TreeItems"]).filter(ParentColumn==str(Parent_id)).\
                order_by("ItemOrder").all()
        else:
            records2 = self.treeviewdict["Session"].query(self.treeviewdict["TreeItems"]).filter_by(id=int(Tree_id)).\
                order_by("ItemOrder").all()'''

        rowcount = 0
        treeviewindex = 1  # todo... or this
        for row, record2 in enumerate(records2):
            if record2 is not None:
                self.RecordCount += 1
                # Initialize the Data

                newtreeitemdata = self.treeItemFromdb(self.treeviewdict["Session"], self.treeviewdict["TreeItems"],
                                                      record2.id, self.treeviewdict["MasterTable_id"], None, "Tree_id")

                newtreeitemdata['TreePath'] = treepath.copy()
                newtreeitemdata['ItemLevel'] = ItemLevel + 1
                newtreeitemdata['ItemOrder'] = self.RecordCount
                newtreeitemdata['ParentTree_id'] = Parent_id
                newtreeitemdata['id'] = record2.id

                newtreeitemdata2 = self.addTreeItem(None, newtreeitemdata)

                # print(Parent_id, newtreeitemdata['Tree_id'])
                # Checking for presence of child items.
                records3 = self.treeviewdict["Session"].query(self.treeviewdict["TreeItems"]).filter(
                    ParentColumn == str(newtreeitemdata['Tree_id'])).first()

                if records3 is not None and newtreeitemdata2['Tree_id'] != Parent_id:
                    self.readtvtreebranch(newtreeitemdata2['TreePath'], newtreeitemdata2['Tags'],
                                          newtreeitemdata2['Tree_id'], newtreeitemdata['ItemLevel'], None,
                                          ParentColumnName, ItemColumnName)

    def createLinkedTree(self, linkeditemlist, treeviewdict2=None):
        # The id column entry can be single entry or a list of entries.  This is typeically for the parent list
        # if priminary group id is not it should load them all
        if treeviewdict2 is None: treeviewdict2 = self.treeviewdict

        SourceTable_id = treeviewdict2["MasterTable_id"]
        MasterSession = treeviewdict2["MasterSession"]
        SourceSession = treeviewdict2["Session"]
        SourceTree = treeviewdict2["TreeItems"]

        if type(id) is not list:
            baseidlist = []
            baseidlist.append(id)
        else:
            baseidlist = id

        for itemlistdata in linkeditemlist:

            modelrootitem = SourceSession.query(SourceTree).filter_by(id=itemlistdata["root_id"]).first()

            mastertablequery = MasterSession.query(treeviewdict2["MasterTable"]).filter_by(
                id=modelrootitem.ItemTable_id).first()
            SessionName = MasterSession.query(SessionNames).filter_by(id=mastertablequery.Session).first()
            BaseName = MasterSession.query(SessionBase).filter_by(id=mastertablequery.Base).first()

            newtreeitemdata = self.treeItemFromdb(SourceSession, SourceTree, itemlistdata["root_id"], SourceTable_id)
            sourceid = "(%s-%s-%s-%s)" % (
            newtreeitemdata['SourcePG'], newtreeitemdata['SourceSG'], SourceTable_id, itemlistdata["root_id"])

            sourceparent_id = "(0)"
            destinationparent_id = "(0)"
            treepath = []
            # newtreeitemdata['ItemTable_id'] = modelrootitem.ItemMaster_id
            newtreeitemdata['ItemLevel'] = 0
            newtreeitemdata['Tags'] = []
            newtreeitemdata['ParentTree_id'] = "(0)"
            newtreeitemdata['MasterTable_id'] = SourceTable_id
            # newtreeitemdata['SourcePG'] = itemlistdata["PrimaryGroup_id"]
            # newtreeitemdata['PrimaryGroup_id'] = itemlistdata["PrimaryGroup_id"]

            if itemlistdata['DestinationPG'] is None:
                newtreeitemdata['DestinationPG'] = newtreeitemdata['SourcePG']
                itemlistdata['DestinationPG'] = newtreeitemdata['SourcePG']
            else:
                newtreeitemdata['DestinationPG'] = itemlistdata['DestinationPG']

            if itemlistdata['DestinationSG'] is None:
                newtreeitemdata['DestinationSG'] = newtreeitemdata['SourceSG']
            else:
                newtreeitemdata['DestinationSG'] = itemlistdata['DestinationSG']
                itemlistdata['DestinationSG'] = itemlistdata['DestinationSG']

            destinationid = "(%s-%s-%s-%s)" % (
            newtreeitemdata['DestinationPG'], newtreeitemdata['DestinationSG'], SourceTable_id, itemlistdata["root_id"])

            originaltree_id = newtreeitemdata["Tree_id"]
            newtreeitemdata2 = self.AddTreeRoot("Ginger", [], newtreeitemdata=newtreeitemdata,
                                                LinkedTable=treeviewdict2["GeneratedTree"])
            # newtreeitemdata["Tree_id"] = id

            linkeditemlist = []
            # newtreeitemdata2['Tags']
            self.createtvtreebranch(treeviewdict2, treepath, [], itemlistdata, sourceparent_id, destinationparent_id,
                                    newtreeitemdata['ItemLevel'])

    def createtvtreebranch(self, treeviewdict, treepath, taglist, itemlistdata, sourceparentid, destinationparent_id,
                           ItemLevel):
        SourceTree = treeviewdict["TreeItems"]
        sourceitemlistdata = itemlistdata
        # print(sourceparentid)

        if sourceparentid:
            parentstuff = sourceparentid[1:-1]
            parentstufflist = parentstuff.split("-")  # last item, remove brackets split by the -

            # print(sourceparentid, parentstufflist)
            if sourceparentid == "(0)":
                records1 = treeviewdict["Session"].query(SourceTree).filter_by(PrimaryGroup_id=itemlistdata['SourcePG']) \
                    .filter_by(SecondaryGroup_id=itemlistdata['SourceSG']) \
                    .filter_by(ParentTree_id=sourceparentid) \
                    .order_by(SourceTree.ItemOrder).order_by(SourceTree.DisplayName).all()
            else:
                records1 = treeviewdict["Session"].query(SourceTree).filter_by(PrimaryGroup_id=parentstufflist[0]) \
                    .filter_by(SecondaryGroup_id=parentstufflist[1]) \
                    .filter_by(ParentTree_id=sourceparentid) \
                    .order_by(SourceTree.ItemOrder).order_by(SourceTree.DisplayName).all()
            rowcount = 0
            treeviewindex = 1  # todo... or this
            for row, record1 in enumerate(records1):
                # print("record1", record1.Tree_id, record1.DisplayName)
                # Each the primary group will determine which branch items to follow.
                # The new tree will only have the primary group of the generated
                # print("Primary Group:", PrimaryGroup_id, record1.DisplayName)
                self.RecordCount += 1
                # Initialize the Data
                pg = itemlistdata['SourcePG']
                sg = itemlistdata['SourceSG']
                item_id = record1.id  # Item_id

                newtreeitemdata = self.treeItemFromdb(treeviewdict["Session"], SourceTree, item_id,
                                                      treeviewdict["MasterTable_id"])

                treepath2 = treepath.copy()

                # sourceid = "(%s-%s-%s)" % (self.SourcePG, SourceTable_id, itemlistdata["id"])
                # destinationid = "(%s-%s-%s)" % (self.DestinationPG, SourceTable_id, itemlistdata["id"])

                newtreeitemdata['TreePath'] = treepath2  # DatabaseTools.myListToStr(treepath2)
                newtreeitemdata['ItemLevel'] = ItemLevel + 1
                newtreeitemdata['ItemOrder'] = self.RecordCount
                newtreeitemdata['ItemTable_id'] = record1.ItemTable_id
                newtreeitemdata['ItemMaster_id'] = treeviewdict["MasterTable_id"]
                newtreeitemdata['ParentTree_id'] = destinationparent_id
                newtreeitemdata['id'] = record1.id
                # newtreeitemdata['SourcePG'] = self.SourcePG

                if itemlistdata['DestinationPG'] is None:
                    newtreeitemdata['DestinationPG'] = newtreeitemdata['SourcePG']
                else:
                    newtreeitemdata['DestinationPG'] = itemlistdata['DestinationPG']

                if itemlistdata['DestinationSG'] is None:
                    newtreeitemdata['DestinationSG'] = newtreeitemdata['SourceSG']
                else:
                    newtreeitemdata['DestinationSG'] = itemlistdata['DestinationSG']

                DPG = newtreeitemdata['DestinationPG']
                DSG = newtreeitemdata['DestinationSG']

                newtreeitemdata['MasterTable_id'] = treeviewdict["MasterTable_id"]

                # destinationid = "(%s-%s-%s-%s)" % (newtreeitemdata['DestinationPG'], newtreeitemdata['DestinationSG'], treeviewdict["MasterTable_id"], itemlistdata["root_id"])
                taglist1 = taglist.copy()
                newtreeitemdata['Tags'] = taglist1

                newtreeitemdata1a = self.addTreeItem(treeviewdict["GeneratedTree"], newtreeitemdata)
                destinationparent_id2 = newtreeitemdata1a["Tree_id"]

                fulltagname = taglist1[-1][1:-1]
                lasttag = taglist1[-1][1:-1].split("-")  # last item, remove brackets split by the -
                table_id = int(lasttag[0])

                secondarylist = [190, 19, 680, 672, 145, 611, 644, 571]  # Secondary Tables
                if table_id in secondarylist:  # Tree View Secondary
                    newtreeitemdata["LinkedTree_id"] = fulltagname
                else:
                    newtreeitemdata["LinkedTree_id"] = None

                if newtreeitemdata["LinkedTree_id"]:
                    branchmaster_id = newtreeitemdata["LinkedTree_id"]
                    branchitems = branchmaster_id.split("-")

                    linkedTable_id = int(branchitems[0])
                    linkedRecord_id = int(branchitems[1])

                    mastertablequery = treeviewdict["MasterSession"].query(treeviewdict["MasterTable"]).filter_by(
                        id=linkedTable_id).first()
                    SessionName = treeviewdict["MasterSession"].query(SessionNames).filter_by(
                        id=mastertablequery.Session).first()
                    BaseName = treeviewdict["MasterSession"].query(SessionBase).filter_by(
                        id=mastertablequery.Base).first()
                    LinkedSourceReference = DatabaseTools.get_class_by_tablename(self.bases[BaseName.NameText],
                                                                                 mastertablequery.TableName)

                    secondaryrecord = self.sessions[SessionName.NameText].query(LinkedSourceReference).filter_by(
                        id=linkedRecord_id).first()

                    primaryrecord = self.sessions[SessionName.NameText].query(treeviewdict["PrimaryGroup"]).filter_by(
                        id=secondaryrecord.PrimaryGroup_id).first()

                    mastertablequery = treeviewdict["MasterSession"].query(treeviewdict["MasterTable"]).filter_by(
                        id=primaryrecord.MasterTable_id).first()
                    if mastertablequery:
                        SessionName = treeviewdict["MasterSession"].query(SessionNames).filter_by(
                            id=mastertablequery.Session).first()
                        BaseName = treeviewdict["MasterSession"].query(SessionBase).filter_by(
                            id=mastertablequery.Base).first()
                        LinkedSourceTable = DatabaseTools.get_class_by_tablename(self.bases[BaseName.NameText],
                                                                                 mastertablequery.TableName)

                        record2 = self.sessions[SessionName.NameText].query(LinkedSourceTable).filter_by(
                            PrimaryGroup_id=secondaryrecord.PrimaryGroup_id) \
                            .filter_by(SecondaryGroup_id=secondaryrecord.SecondaryGroup_id) \
                            .filter_by(ParentTree_id="(0)") \
                            .order_by(SourceTree.ItemOrder).order_by(SourceTree.DisplayName).first()

                        itemlistdata2 = itemlistdata
                        itemlistdata2['SourcePG'] = secondaryrecord.PrimaryGroup_id
                        itemlistdata2['SourceSG'] = secondaryrecord.SecondaryGroup_id

                        SourceTable_id2 = linkedTable_id
                        SourceSession2 = self.sessions[SessionName.NameText]
                        SourceTree2 = LinkedSourceTable
                        treeviewdict2 = treeviewdict

                        treeviewdict2["TreeItems"] = LinkedSourceTable
                        treeviewdict2["Session"] = self.sessions[SessionName.NameText]

                        if record2.Tree_id is not None:
                            self.RecordCount += 1
                            # Initialize the Data

                            newtreeitemdata2 = self.treeItemFromdb(treeviewdict2["Session"], SourceTree2, record2.id,
                                                                   treeviewdict2["MasterTable_id"])

                            treepath3 = treepath2.copy()

                            newtreeitemdata2['TreePath'] = treepath3  # DatabaseTools.myListToStr(treepath2)
                            newtreeitemdata2['ItemLevel'] = ItemLevel
                            newtreeitemdata2['ItemOrder'] = self.RecordCount
                            newtreeitemdata2['ItemTable_id'] = record2.ItemTable_id
                            newtreeitemdata2['ParentTree_id'] = newtreeitemdata['Tree_id']
                            newtreeitemdata2['id'] = record2.id
                            taglist2 = taglist1.copy()
                            newtreeitemdata2['Tags'] = taglist2

                            records5 = SourceSession2.query(SourceTree2).filter_by(
                                ParentTree_id=str(record2.Tree_id)).order_by(SourceTree2.DisplayName).all()
                            if records5 is not None:
                                self.createtvtreebranch(treeviewdict2, newtreeitemdata2["TreePath"], taglist1,
                                                        itemlistdata2, record2.Tree_id, destinationparent_id2,
                                                        ItemLevel)
                                # print("level created")
                        else:
                            print("fail")
                else:
                    records3 = treeviewdict["Session"].query(SourceTree).filter_by(
                        ParentTree_id=str(record1.Tree_id)).order_by(SourceTree.DisplayName).all()
                    if records3 is not None:
                        for check in records3:
                            pass
                            # print(check.DisplayName)
                        self.createtvtreebranch(treeviewdict, newtreeitemdata["TreePath"], taglist1, sourceitemlistdata,
                                                record1.Tree_id, destinationparent_id2, ItemLevel + 1)

    def root(self):
        return self.parents[str(0)].internalPointer()

    def insertRow(self, row, parent):
        return self.insertRows(row, 1, parent)

    def insertRows(self, row, count, parent):
        self.beginInsertRows(parent, row, (row + (count - 1)))
        self.endInsertRows()
        return True

    def removeRow(self, row, parentIndex):
        return self.removeRows(row, 1, parentIndex)

    def removeRows(self, row, count, parentIndex):
        self.beginRemoveRows(parentIndex, row, row)
        node = self.nodeFromIndex(parentIndex)
        node.removeChild(row)
        self.endRemoveRows()
        return True

    def mimeTypes(self):
        types = QListWidget
        types.append('application/x-ets-qt4-instance')
        return types

    def mimeData(self, index):
        node = self.nodeFromIndex(index[0])
        mimeData = PyMimeData(node)
        return mimeData

    def dropMimeData(self, mimedata, action, row, column, parentIndex):
        if action == Qt.IgnoreAction:
            return True

        dragNode = mimedata.instance()
        parentNode = self.nodeFromIndex(parentIndex)

        # make an copy of the node being moved
        newNode = deepcopy(dragNode)
        newNode.setParent(parentNode)
        self.insertRow(len(parentNode) - 1, parentIndex)
        # self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),parentIndex, parentIndex)
        return True

    def columnCount(self, parent=None):
        if parent and parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return len(self.Headers)

    def recordCount(self):
        return self.RecordCount

    def data(self, index, role):
        if not index.isValid():
            return

        item = index.internalPointer()
        if role == Qt.DisplayRole:
            try:
                return item.data(index.column())
            except:
                pass

        if role == Qt.UserRole:
            if item:
                return item.Header
        return

    def returnHeaderData(self):
        SQLQuery = 'select * from %s' % (self.datatable)

    def headerData(self, column, orientation, role):
        if (orientation == Qt.Horizontal and
                role == Qt.DisplayRole):
            try:
                return self.Headers[column]
            except IndexError:
                pass

        return

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        if not childItem:
            return QModelIndex()

        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent=QModelIndex()):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            p_Item = self.rootItem
        else:
            p_Item = parent.internalPointer()
        return p_Item.childCount()

    def treeTableModel(self, SWhere=None, Orientation="Vertical"):
        modelData = QAbstractItemModel

        records = self.session.query(self.TreeGeneratedClass)
        recordrow = 0
        self.fieldDict = records.keys()

        if Orientation == "Vertical":
            recordrow = 0
            for record in records:  # cursors are iterable
                for key in self.fieldDict:
                    modelData.setItem(recordrow, key, QStandardItem(str(record[key])))
                recordrow += 1

            # Header Data
            modelData.sort(3, Qt.AscendingOrder)

            fieldColumn = 0
            for key, value in self.fieldDict:
                # print(headerName[0])
                modelData.setHeaderData(key, Qt.Horizontal, value, role=Qt.DisplayRole)
                fieldColumn += 1
        else:
            recordcolumn = 0
            for record in records:  # cursors are iterable
                for key, value in self.fieldDict:
                    modelData.setItem(key, recordcolumn, QStandardItem(str(record[key])))
                recordcolumn += 1
        return modelData

    def searchModel(self, treepath):
        '''
        get the modelIndex for a given appointment
        '''

        def searchNode(node):
            '''
            a function called recursively, looking at all nodes beneath node
            '''
            for child in node.childItems:
                if treepath == child.TreeClassItem.TreePath:
                    index = self.createIndex(child.row(), 0, child)
                    return index

                if child.childCount() > 0:
                    result = searchNode(child)
                    if result:
                        return result

        retarg = searchNode(self.parents[0])
        return retarg

    def find_Tree_Branch(self, cname):
        app = None
        for category in self.categories:
            if category.cname == cname:
                app = category
                break
        if app != None:
            index = self.searchModel(app)
            return (True, index)
        return (False, None)

    def paintEvent(self, event):
        painter = QPainter(
            self.viewport())  # See: http://stackoverflow.com/questions/12226930/overriding-qpaintevents-in-pyqt
        painter.drawEllipse(self.center, 10, 10)
        QTableWidget.paintEvent(self, event)

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        index = self.indexAt(event.pos())
        sellst = self.selectedList()
        if index.isValid():
            target_node = index.internalPointer().node
            dragged_nodes, drag_type, qdrag = self.drag
            # I don't think we need qdrag for anything, but it can't hurt.
            if target_node.drop_on_ok(drag_type, dragged_nodes):
                self.selectNodes(sellst, but_not=dragged_nodes)
                target_node.drop_on(drag_type, dragged_nodes)
                event.acceptProposedAction()
                self.mt_update()
                self.drag = None
                return
        event.ignore()
        self.mt_update()
        self.drag = None

    def mouseMoveEvent(self, event):
        if self.drag is not None:
            pass  # QTreeView.mouseMoveEvent(self, event)
            return
        if ((event.globalPos() - self.mouse_press_qpoint).manhattanLength()
                < QApplication.startDragDistance()):
            return
        #
        # starting a drag
        # [logic bug, after bruce change 070507: should not do this
        #  if we already started dragging out a selection. How can we tell?
        #  Only by whether the initial press had eventInRect, I think
        #  (not yet recorded), or at least, the initial move (#e could record here).]
        #
        index = self.indexAt(event.pos())

        sellst = self.selectedList()  # bruce 070507 move earlier

        DEBUG2 = True

        if index.isValid():
            thisnode = index.internalPointer().node

            # bruce 070507 bring in some code from modelTreeGui.py
            alreadySelected = (thisnode in sellst)

            item = index.internalPointer()
            rect = self.visualRect(index)
            if DEBUG2:
                print("visualRect coords", rect.left(), rect.right(), rect.top(), rect.bottom())
            # qfm = QFontMetrics(QLineEdit(self).font())
            # rect.setWidth(qfm.width(item.node.NameText) + _ICONSIZE[0] + 4)
            if DEBUG2:
                print("visualRect coords, modified:", rect.left(), rect.right(), rect.top(), rect.bottom())
                # looks like icon and text, a bit taller than text (guesses)
            eventInRect = rect.contains(event.pos())
            if DEBUG2:
                print("valid index: eventInRect = %r, item = %r, index = %r, alreadySelected = %r" % \
                      (eventInRect, item, index, alreadySelected))  #######
        else:
            thisnode = item = None
            alreadySelected = eventInRect = False

        if not eventInRect:
            # nothing to drag, but [bruce 070507] let super handle it (for dragging over nodes to select)
            self.drag_is_not_DND = True  ### not yet used
            # QTreeView.mouseMoveEvent(self, event)
            return

        if thisnode in sellst:
            # if dragging something selected, drag along all other selected ones
            dragged_nodes = sellst
        else:
            # if dragging something unselected, ignore any selected ones
            dragged_nodes = [thisnode]
        qdrag = QDrag(self)
        drag_type = 'move'  # how do I decide between 'move' and 'copy'?
        self.drag = (dragged_nodes, drag_type, qdrag)
        mimedata = QMimeData()
        mimedata.setText("need a string here for a valid mimetype")
        qdrag.setMimeData(mimedata)
        display_prefs = {}
        pixmap = dragged_nodes[0].node_icon(display_prefs)
        qdrag.setPixmap(pixmap)
        qdrag.setHotSpot(QPoint(-8, 8))
        qdrag.start()

    def mousePressEvent(self, event):
        self.drag_is_not_DND = False  # don't know yet
        qp = event.globalPos()  # clone the point to keep it constant
        self.mouse_press_qpoint = QPoint(qp.x(), qp.y())
        self.mouse_press_event = QMouseEvent(event.type(),
                                             QPoint(event.x(), event.y()),
                                             event.button(), event.buttons(),
                                             event.modifiers())

    def mouseReleaseEvent(self, event):
        self.drag_is_not_DND = False
        if self.drag is None:
            pass
            # QTreeView.mousePressEvent(self, self.mouse_press_event)
        self.drag = None
        # QTreeView.mouseReleaseEvent(self, event)

    def contextMenuEvent(self, event):
        # menu = QMenu(self)
        pos = event.pos()
        index = self.indexAt(pos)
        if index.isValid():
            item = self.indexAt(pos).internalPointer()
            node = self.item_to_node_dict[item]
            nodeset = [node]  # ? ? ? ?
            optflag = False  # ? ? ? ?
            cmenu_spec = self.treemodel.make_cmenuspec_for_set(nodeset, optflag)
            for x in cmenu_spec:
                if x is not None:
                    str, thunk = x[:2]
                    # act = QAction(str, self)
                    # act.setEnabled("disabled" not in x[2:])
                    # self.connect(act, SIGNAL("triggered()"), thunk)
                    # menu.addAction(act)
                    pass
                else:
                    pass
                    # menu.addSeparator()
                    # menu.exec_(event.globalPos())

    def flags(self, index):
        # Qt.ItemIsEnabled|Qt.ItemIsEditable|Qt.ItemIsSelectable
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable


class treeModel(QAbstractItemModel):
    # Dexton Mohn Say Hi!!!!! October 13, 2019
    def __init__(self, basedict, sessiondict, treeviewdict, inParent=None, header="", PrimaryGroup_id=1, **kwargs):
        super(treeModel, self).__init__(inParent, **kwargs)

        # treeviewdict["MasterTable"] = MasterTable
        # treeviewdict["DescriptorTable"] = TaskDescriptorTable
        # treeviewdict["ItemTable"] = TaskItemTable
        # treeviewdict["Session"] = sessions["TaskManager"]
        # treeviewdict["SessionName"] = "TaskManager"
        # treeviewdict["TreeItems"] = TaskTree
        # treeviewdict["Header"] = "Tree Header"
        # treeviewdict["GeneratedTree"] = GeneratedTaskTree
        # treeviewdict["ComponentTable"] = TaskComponents
        # treeviewdict["MasterTreeTable"] = MasterTaskTreeTable
        # treeviewdict["TreeGroup"] = TaskTreeGroup
        # treeviewdict["MasterTable_id"] = 360
        # treeviewdict["MasterTableSession"] = sessions["PackageManager"]

        '''TreeItems.id
            TreeItems.PrimaryGroup_id
            TreeItems.Tree_id
            TreeItems.ParentTree_id
            TreeItems.ItemMaster_id
            TreeItems.ItemTableType_id
            TreeItems.ItemTable_id
            TreeItems.Item_id
            TreeItems.DisplayName
            TreeItems.ItemOrder
            TreeItems.FlattenedOrder
            TreeItems.ItemLevel
            TreeItems.ForeColor
            TreeItems.Expanded
            TreeItems.Header
            TreeItems.Tags'''

        self.Display = []
        self.rootItem = TreeItem(None, "ALL", None)
        self.parents = {0: self.rootItem}

        self.bases = basedict
        self.sessions = sessiondict

        self.treeviewdict = treeviewdict
        self.PrimaryGroup_id = PrimaryGroup_id
        self.SourceSession = treeviewdict["Session"]
        self.SourceTree = treeviewdict["TreeItems"]
        self.PrimaryGroup_id = 0
        self.fieldNames = []
        self.fieldNameCount = None
        self.fieldDict = None
        # self.Headers =  ("Category", "Item", "Description")
        self.Headers = []
        self.Headers.append(header)

        self.RecordCount = 0

    def defaultTreeItem(self):
        newtreeitemdata = {}
        newtreeitemdata['TreePath'] = []

        newtreeitemdata['PrimaryGroup_id'] = 0
        newtreeitemdata['Tree_id'] = None
        newtreeitemdata['ParentTree_id'] = "0"  # Follows the top item
        newtreeitemdata['ItemMaster'] = None
        newtreeitemdata['ItemMasterTable'] = None
        newtreeitemdata['ItemMasterTableType'] = 0
        newtreeitemdata['ItemMaster_id'] = 0
        newtreeitemdata['ItemTableType_id'] = 0
        newtreeitemdata['ItemName'] = None
        newtreeitemdata['ItemTable'] = None
        newtreeitemdata['ItemTable_id'] = 0
        newtreeitemdata['Item_id'] = 0
        newtreeitemdata['DisplayName'] = None
        newtreeitemdata['ItemOrder'] = 0
        newtreeitemdata['FlattenedOrder'] = 0
        newtreeitemdata['ItemLevel'] = 0
        newtreeitemdata['ForeColor'] = None
        newtreeitemdata['Expanded'] = 0
        newtreeitemdata['Header'] = None
        newtreeitemdata['Tags'] = []
        newtreeitemdata['Date_Created'] = None
        newtreeitemdata['Date_Modified'] = None
        newtreeitemdata['Date_Accessed'] = None

        # newtreeitemdata = self.currentTreeItem(ID=Tree_id)

        # treepath = []
        # treepath.append(Tree_id)
        # newtreeitemdata['TreePath'] = str(DatabaseTools.myListToStr(treepath))
        itemlevel = 0
        # newtreeitemdata['ItemLevel'] = len(treepath) - 1

        return newtreeitemdata

    def treeItemFromdb(self, tree_id, PrimaryGroup_id=None, location=0):
        # todo the id and tree_id arre not the same
        # Creates a tree item from the data
        # Can be a list table or tree table
        # TreeClass - Where the tree data is coming from
        if location == 0:
            treetable = self.treeviewdict["TreeItems"]
        else:
            treetable = self.treeviewdict["GeneratedTree"]

        if PrimaryGroup_id == None:
            PrimaryGroup_id = self.PrimaryGroup_id

        newtreeitemdata = self.defaultTreeItem()
        # print(self.treeviewdict["ItemMasterTable"])

        SelectedTreeItem = self.SourceSession.query(treetable).filter_by(Tree_id=tree_id).filter_by(
            PrimaryGroup_id=self.PrimaryGroup_id).first()
        newtreeitemdata['id'] = SelectedTreeItem.id

        if SelectedTreeItem is not None:

            newtreeitemdata['ItemName'] = SelectedTreeItem.DisplayName

            newtreeitemdata['PrimaryGroup_id'] = PrimaryGroup_id
            # newtreeitemdata['SecondaryGrouop_id'] = SelectedTreeItem.SecondaryGroup_id
            newtreeitemdata['Tree_id'] = str(SelectedTreeItem.Tree_id)
            newtreeitemdata['ParentTree_id'] = str(SelectedTreeItem.ParentTree_id)
            newtreeitemdata['ItemMaster_id'] = SelectedTreeItem.ItemMaster_id
            newtreeitemdata['ItemTable'] = None

            try:
                newtreeitemdata['ItemTableType_id'] = SelectedTreeItem.ItemTableType_id
            except:
                newtreeitemdata['ItemTableType_id'] = None

            newtreeitemdata['ItemTable_id'] = SelectedTreeItem.ItemTable_id
            newtreeitemdata['Item_id'] = SelectedTreeItem.Item_id
            newtreeitemdata['DisplayName'] = SelectedTreeItem.DisplayName
            try:
                newtreeitemdata['ItemOrder'] = SelectedTreeItem.ItemOrder
            except:
                pass
            # newtreeitemdata['FlattenedOrder'] = SelectedTreeItem.FlattenedOrder
            try:
                newtreeitemdata['ItemLevel'] = SelectedTreeItem.ItemLevel
            except:
                pass

            try:
                newtreeitemdata['ForeColor'] = SelectedTreeItem.ForeColor
            except:
                pass
            # newtreeitemdata['Expanded'] = SelectedTreeItem.Expanded
            try:
                newtreeitemdata['Header'] = SelectedTreeItem.Header
            except:
                pass

            newtag = "(%s-%s)" % (SelectedTreeItem.ItemMaster_id, SelectedTreeItem.Item_id)
            newtreeitemdata['Tags'] = [newtag]

            newtreeitemdata['Date_Created'] = None
            newtreeitemdata['Date_Modified'] = None
            newtreeitemdata['Date_Accessed'] = None
        return newtreeitemdata

    def AddTreeRoot(self, RootName, indexlist, PrimaryGroup_id, newtreeitemdata=None):

        itemcount = 0
        treeviewindex = 1
        for index in indexlist:
            treeviewindex = index

        currentdatetime = datetime.datetime.now()

        if newtreeitemdata is None:
            newtreeitemdata = {}

            newtreeitemdata['TreePath'] = []
            newtreeitemdata['Tree_id'] = None
            newtreeitemdata['PrimaryGroup_id'] = 0
            newtreeitemdata['PrimaryGroup_id'] = PrimaryGroup_id
            newtreeitemdata['ParentTree_id'] = "0"
            newtreeitemdata['ItemMaster'] = None
            newtreeitemdata['ItemMasterTable'] = 0
            newtreeitemdata['ItemMaster_id'] = 1
            newtreeitemdata['ItemName'] = ""
            newtreeitemdata['ItemTable'] = None
            newtreeitemdata['ItemTable_id'] = 0
            newtreeitemdata['ItemTableType_id'] = 0
            newtreeitemdata['Item_id'] = 0
            newtreeitemdata['DisplayName'] = RootName
            newtreeitemdata['ItemOrder'] = 0
            newtreeitemdata['FlattenedOrder'] = 1
            newtreeitemdata['ItemLevel'] = 0
            newtreeitemdata['ForeColor'] = None
            newtreeitemdata['Expanded'] = 0
            newtreeitemdata['Header'] = None
            newtreeitemdata['Tags'] = []
            newtreeitemdata['Date_Created'] = str(currentdatetime)

        newtreeitemdata['Date_Modified'] = str(currentdatetime)
        newtreeitemdata['Date_Accessed'] = str(currentdatetime)

        ActivityTypeParentID = self.addTreeItem(newtreeitemdata)
        return ActivityTypeParentID

    def addTreeItem(self, treeItemDict):

        treeItemDict["TreePath"].append(treeItemDict["Tree_id"])

        newtag = "(%s-%s)" % (treeItemDict["ItemMaster_id"], treeItemDict["Item_id"])
        treeItemDict['Tags'].append(newtag)

        TIC = treeItem_class(treeItemDict)
        if treeItemDict['ItemLevel'] == 0:
            # Root Level Entries
            newparent = TreeItem(TIC, treeItemDict['Header'], self.rootItem)
            self.rootItem.appendChild(newparent)
            # Create the Dictonary Linking Values
            self.parents[str(treeItemDict["Tree_id"])] = newparent
        else:
            parentItem = self.parents[str(treeItemDict['ParentTree_id'])]
            newItem = TreeItem(TIC, treeItemDict['Header'], parentItem)

            parentItem.appendChild(newItem)
            self.parents[str(treeItemDict["Tree_id"])] = newItem

        return treeItemDict

    def root(self):
        return self.parents[0].internalPointer()

    def insertRow(self, row, parent):
        return self.insertRows(row, 1, parent)

    def insertRows(self, row, count, parent):
        self.beginInsertRows(parent, row, (row + (count - 1)))
        self.endInsertRows()
        return True

    def removeRow(self, row, parentIndex):
        return self.removeRows(row, 1, parentIndex)

    def removeRows(self, row, count, parentIndex):
        self.beginRemoveRows(parentIndex, row, row)
        node = self.nodeFromIndex(parentIndex)
        node.removeChild(row)
        self.endRemoveRows()
        return True

    def clearTree(self, Tree_id):
        self.session.begin()
        treerecords = self.session.query(self.treeviewdict["TreeItems"])
        if treerecords is not None:
            treerecords.delete(synchronize_session=False)
        self.session.commit()

    def loadOriginalData(self, Tree_id):

        newtreeitemdata = self.treeItemFromdb(Tree_id)

        treepath = []
        treepath.append(Tree_id)
        newtreeitemdata['TreePath'] = treepath  # str(DatabaseTools.myListToStr(treepath))
        itemlevel = 0
        newtreeitemdata['ItemLevel'] = len(treepath) - 1
        DynamicParentID = self.addTreeItem(newtreeitemdata)
        ParentID = newtreeitemdata['Tree_id']

        self.tvtreebranch(treepath, ParentID)

    def loadGeneratedData(self, Tree_id):

        newtreeitemdata = self.treeItemFromdb(Tree_id)

        treepath = []
        treepath.append(Tree_id)
        newtreeitemdata['TreePath'] = treepath  # str(DatabaseTools.myListToStr(treepath))
        itemlevel = 0
        newtreeitemdata['ItemLevel'] = len(treepath) - 1
        DynamicParentID = self.addTreeItem(newtreeitemdata)
        ParentID = newtreeitemdata['Tree_id']

        self.tvtreebranch(treepath, ParentID)

    def setupModelData(self, Tree_id):

        newtreeitemdata = self.treeItemFromdb(Tree_id)

        treepath = []
        treepath.append(Tree_id)
        newtreeitemdata['TreePath'] = treepath  # str(DatabaseTools.myListToStr(treepath))
        itemlevel = 0
        newtreeitemdata['ItemLevel'] = len(treepath) - 1
        DynamicParentID = self.addTreeItem(newtreeitemdata)
        ParentID = newtreeitemdata['Tree_id']

        self.tvtreebranch(treepath, ParentID)

    def setupModelData2(self, Tree_id, Group_id=None):

        newtreeitemdata = self.currentTreeItem(ID=Tree_id)

        if self.treeviewdict["GeneratedTree"] != self.treeviewdict["TreeItems"]:
            self.session.begin()
            treerecords = self.session.query(self.treeviewdict["GeneratedTree"])
            if treerecords is not None:
                treerecords.delete(synchronize_session=False)
            self.session.commit()

        treepath = []
        treepath.append(Tree_id)
        newtreeitemdata['TreePath'] = treepath  # str(DatabaseTools.myListToStr(treepath))
        itemlevel = 0
        newtreeitemdata['ItemLevel'] = len(treepath) - 1
        DynamicParentID = self.addTreeItem(self.treeviewdict["GeneratedTree"], newtreeitemdata)
        ParentID = newtreeitemdata['Tree_id']

        self.tvtreebranch(treepath, Group_id, ParentID)

    def tvtreebranch(self, treepath, ParentID):

        # Load the table data that have parents that match the ParentID
        records2 = self.SourceSession.query(self.treeviewdict["TreeItems"]).filter_by(
            PrimaryGroup_id=int(self.PrimaryGroup_id)).filter_by(ParentTree_id=str(ParentID)). \
            order_by("DisplayName").all()

        rowcount = 0
        treeviewindex = 1  # todo... or this

        for row, record2 in enumerate(records2):
            self.RecordCount += 1
            # Initialize the Data

            newtreeitemdata = self.treeItemFromdb(record2.Tree_id)

            treepath2 = treepath.copy()
            treepath2.append(str(newtreeitemdata['Tree_id']))
            newtreeitemdata['TreePath'] = treepath2  # DatabaseTools.myListToStr(treepath2)
            newtreeitemdata['ItemLevel'] = len(treepath2) - 1
            newtreeitemdata['ItemOrder'] = self.RecordCount
            # y = newtreeitemdata['Tree_id']
            # z = newtreeitemdata['ParentTree_id']
            # print(y, z)

            DynamicParentID = self.addTreeItem(newtreeitemdata)

            # Checking for presence of child items.
            records3 = self.SourceSession.query(self.treeviewdict["TreeItems"]).filter_by(
                PrimaryGroup_id=int(self.PrimaryGroup_id)) \
                .filter_by(ParentTree_id=newtreeitemdata['Tree_id']).all()
            if records3 is not None:
                self.tvtreebranch(treepath2, newtreeitemdata['Tree_id'])

    def mimeTypes(self):
        types = QListWidget
        types.append('application/x-ets-qt4-instance')
        return types

    def mimeData(self, index):
        node = self.nodeFromIndex(index[0])
        mimeData = PyMimeData(node)
        return mimeData

    def dropMimeData(self, mimedata, action, row, column, parentIndex):
        if action == Qt.IgnoreAction:
            return True

        dragNode = mimedata.instance()
        parentNode = self.nodeFromIndex(parentIndex)

        # make an copy of the node being moved
        newNode = deepcopy(dragNode)
        newNode.setParent(parentNode)
        self.insertRow(len(parentNode) - 1, parentIndex)
        # self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),parentIndex, parentIndex)
        return True

    def columnCount(self, parent=None):
        if parent and parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return len(self.Headers)

    def recordCount(self):
        return self.RecordCount

    def data(self, index, role):
        if not index.isValid():
            return

        item = index.internalPointer()
        if role == Qt.DisplayRole:
            try:
                return item.data(index.column())
            except:
                pass

        if role == Qt.UserRole:
            if item:
                return item.Header
        return

    def returnHeaderData(self):
        SQLQuery = 'select * from %s' % (self.datatable)

    def headerData(self, column, orientation, role):
        if (orientation == Qt.Horizontal and
                role == Qt.DisplayRole):
            try:
                return self.Headers[column]
            except IndexError:
                pass

        return

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        if not childItem:
            return QModelIndex()

        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent=QModelIndex()):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            p_Item = self.rootItem
        else:
            p_Item = parent.internalPointer()
        return p_Item.childCount()

    def treeTableModel(self, SWhere=None, Orientation="Vertical"):
        modelData = QAbstractItemModel

        records = self.session.query(self.TreeGeneratedClass)
        recordrow = 0
        self.fieldDict = records.keys()

        if Orientation == "Vertical":
            recordrow = 0
            for record in records:  # cursors are iterable
                for key in self.fieldDict:
                    modelData.setItem(recordrow, key, QStandardItem(str(record[key])))
                recordrow += 1

            # Header Data
            modelData.sort(3, Qt.AscendingOrder)

            fieldColumn = 0
            for key, value in self.fieldDict:
                # print(headerName[0])
                modelData.setHeaderData(key, Qt.Horizontal, value, role=Qt.DisplayRole)
                fieldColumn += 1
        else:
            recordcolumn = 0
            for record in records:  # cursors are iterable
                for key, value in self.fieldDict:
                    modelData.setItem(key, recordcolumn, QStandardItem(str(record[key])))
                recordcolumn += 1
        return modelData

    def searchModel(self, treepath):
        '''
        get the modelIndex for a given appointment
        '''

        def searchNode(node):
            '''
            a function called recursively, looking at all nodes beneath node
            '''
            for child in node.childItems:
                if treepath == child.TreeClassItem.TreePath:
                    index = self.createIndex(child.row(), 0, child)
                    return index

                if child.childCount() > 0:
                    result = searchNode(child)
                    if result:
                        return result

        retarg = searchNode(self.parents[0])
        return retarg

    def find_Tree_Branch(self, cname):
        app = None
        for category in self.categories:
            if category.cname == cname:
                app = category
                break
        if app != None:
            index = self.searchModel(app)
            return (True, index)
        return (False, None)

    def paintEvent(self, event):
        painter = QPainter(
            self.viewport())  # See: http://stackoverflow.com/questions/12226930/overriding-qpaintevents-in-pyqt
        painter.drawEllipse(self.center, 10, 10)
        QTableWidget.paintEvent(self, event)

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        index = self.indexAt(event.pos())
        sellst = self.selectedList()
        if index.isValid():
            target_node = index.internalPointer().node
            dragged_nodes, drag_type, qdrag = self.drag
            # I don't think we need qdrag for anything, but it can't hurt.
            if target_node.drop_on_ok(drag_type, dragged_nodes):
                self.selectNodes(sellst, but_not=dragged_nodes)
                target_node.drop_on(drag_type, dragged_nodes)
                event.acceptProposedAction()
                self.mt_update()
                self.drag = None
                return
        event.ignore()
        self.mt_update()
        self.drag = None

    def mouseMoveEvent(self, event):
        if self.drag is not None:
            pass  # QTreeView.mouseMoveEvent(self, event)
            return
        if ((event.globalPos() - self.mouse_press_qpoint).manhattanLength()
                < QApplication.startDragDistance()):
            return
        #
        # starting a drag
        # [logic bug, after bruce change 070507: should not do this
        #  if we already started dragging out a selection. How can we tell?
        #  Only by whether the initial press had eventInRect, I think
        #  (not yet recorded), or at least, the initial move (#e could record here).]
        #
        index = self.indexAt(event.pos())

        sellst = self.selectedList()  # bruce 070507 move earlier

        DEBUG2 = True

        if index.isValid():
            thisnode = index.internalPointer().node

            # bruce 070507 bring in some code from modelTreeGui.py
            alreadySelected = (thisnode in sellst)

            item = index.internalPointer()
            rect = self.visualRect(index)
            if DEBUG2:
                print("visualRect coords", rect.left(), rect.right(), rect.top(), rect.bottom())
            # qfm = QFontMetrics(QLineEdit(self).font())
            # rect.setWidth(qfm.width(item.node.NameText) + _ICONSIZE[0] + 4)
            if DEBUG2:
                print("visualRect coords, modified:", rect.left(), rect.right(), rect.top(), rect.bottom())
                # looks like icon and text, a bit taller than text (guesses)
            eventInRect = rect.contains(event.pos())
            if DEBUG2:
                print("valid index: eventInRect = %r, item = %r, index = %r, alreadySelected = %r" % \
                      (eventInRect, item, index, alreadySelected))  #######
        else:
            thisnode = item = None
            alreadySelected = eventInRect = False

        if not eventInRect:
            # nothing to drag, but [bruce 070507] let super handle it (for dragging over nodes to select)
            self.drag_is_not_DND = True  ### not yet used
            # QTreeView.mouseMoveEvent(self, event)
            return

        if thisnode in sellst:
            # if dragging something selected, drag along all other selected ones
            dragged_nodes = sellst
        else:
            # if dragging something unselected, ignore any selected ones
            dragged_nodes = [thisnode]
        qdrag = QDrag(self)
        drag_type = 'move'  # how do I decide between 'move' and 'copy'?
        self.drag = (dragged_nodes, drag_type, qdrag)
        mimedata = QMimeData()
        mimedata.setText("need a string here for a valid mimetype")
        qdrag.setMimeData(mimedata)
        display_prefs = {}
        pixmap = dragged_nodes[0].node_icon(display_prefs)
        qdrag.setPixmap(pixmap)
        qdrag.setHotSpot(QPoint(-8, 8))
        qdrag.start()

    def mousePressEvent(self, event):
        self.drag_is_not_DND = False  # don't know yet
        qp = event.globalPos()  # clone the point to keep it constant
        self.mouse_press_qpoint = QPoint(qp.x(), qp.y())
        self.mouse_press_event = QMouseEvent(event.type(),
                                             QPoint(event.x(), event.y()),
                                             event.button(), event.buttons(),
                                             event.modifiers())

    def mouseReleaseEvent(self, event):
        self.drag_is_not_DND = False
        if self.drag is None:
            pass
            # QTreeView.mousePressEvent(self, self.mouse_press_event)
        self.drag = None
        # QTreeView.mouseReleaseEvent(self, event)

    def contextMenuEvent(self, event):
        # menu = QMenu(self)
        pos = event.pos()
        index = self.indexAt(pos)
        if index.isValid():
            item = self.indexAt(pos).internalPointer()
            node = self.item_to_node_dict[item]
            nodeset = [node]  # ? ? ? ?
            optflag = False  # ? ? ? ?
            cmenu_spec = self.treemodel.make_cmenuspec_for_set(nodeset, optflag)
            for x in cmenu_spec:
                if x is not None:
                    str, thunk = x[:2]
                    # act = QAction(str, self)
                    # act.setEnabled("disabled" not in x[2:])
                    # self.connect(act, SIGNAL("triggered()"), thunk)
                    # menu.addAction(act)
                    pass
                else:
                    pass
                    # menu.addSeparator()
                    # menu.exec_(event.globalPos())

    def flags(self, index):
        # Qt.ItemIsEnabled|Qt.ItemIsEditable|Qt.ItemIsSelectable
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable


class treeCategoryModel(QAbstractItemModel):
    def __init__(self, fileLocation=None, headers=("Item", "Value", "Description"),
                 DisplayItems=['title', 'key', 'desc'], sqlStr=None, inParent=None):
        super(treeCategoryModel, self).__init__(inParent)

        self.fileLocation = fileLocation

        self.categories = []
        self.rootItem = TreeItem(None, "ALL", None)
        self.parents = {0: self.rootItem}
        self.strSQL = sqlStr
        self.Headers = headers
        self.fieldNameCount = None
        self.fieldNames = None
        self.fieldDict = None
        self.DisplayItems = DisplayItems
        self.ColumnsViewed = len(self.DisplayItems)
        self.categorylist = []

    def setFileLocation(self, FileLocation):
        self.fileLocation = FileLocation

    def listCategories(self):
        return self.categorylist

    def columnCount(self, parent=None):
        if parent and parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return len(self.Headers)

    def data(self, index, role):

        if not index.isValid():
            return

        item = index.internalPointer()
        if role == Qt.DisplayRole:
            return item.data(index.column())
        if role == Qt.UserRole:
            if item:
                return item.Header
        else:
            pass
        return

    def headerData(self, column, orientation, role):
        if (orientation == Qt.Horizontal and
                role == Qt.DisplayRole):
            try:
                return self.Headers[column]
            except IndexError:
                pass

        return

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        if not childItem:
            return QModelIndex()

        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent=QModelIndex()):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            p_Item = self.rootItem
        else:
            p_Item = parent.internalPointer()
        return p_Item.childCount()

    def treeTableModel(self):

        modelData = QAbstractItemModel()
        conn = self.session.connection()
        cursor = conn.cursor()
        cursor.execute(self.strSQL)
        self.fieldNameCount

        recordrow = 0
        for record in cursor.fetchall():  # cursors are iterable
            for column in range(self.fieldNameCount):
                modelData.setItem(recordrow, column, QStandardItem(str(record[column])))
                recordrow += 1

        # Header Data
        modelData.sort(3, Qt.AscendingOrder)

        fieldColumn = 0
        for headerName in cursor.description:
            # print(headerName[0])
            modelData.setHeaderData(fieldColumn, Qt.Horizontal, headerName[0], role=Qt.DisplayRole)
            fieldColumn += 1

        cursor.close()
        conn.close()

        return modelData

    def setupModelData(self):
        # 0- TreeID
        # 1 - Category
        # 2 - Data in list format set by ColumnCount

        conn = self.session.connection()
        cursor = conn.cursor()
        cursor.execute(self.strSQL)
        self.fieldNameCount = len(cursor.description)
        self.fieldNames = [i[0] for i in cursor.description]
        self.fieldDict = {item[0]: i for i, item in enumerate(cursor.description)}

        for treeRecords in cursor.fetchall():
            # Tree_id, Category, Display
            Display = []

            for item in self.DisplayItems:
                Display.append(treeRecords[self.fieldDict[item]])

            TIC = treeCategory_class(Tree_id=treeRecords[self.fieldDict['id']],
                                     Category=treeRecords[self.fieldDict['section']],
                                     Display=Display)
            CatExist = False
            for category in self.categories:
                if category.Category == treeRecords[self.fieldDict['section']]:
                    CatExist = True
                    break

            if not CatExist:
                # Root Level Entries
                self.categorylist.append(treeRecords[self.fieldDict['section']])
                self.categories.append(TIC)
                newparent = TreeItem(None, treeRecords[self.fieldDict['section']], self.rootItem)
                newparent.ColumnsViewed = self.ColumnsViewed
                self.rootItem.appendChild(newparent)
                self.parents[treeRecords[self.fieldDict['section']]] = newparent
            try:
                parentItem = self.parents[treeRecords[self.fieldDict['section']]]
                # print(Display)
                newItem = TreeItem(TIC, Display, parentItem)
                newItem.ColumnsViewed = self.ColumnsViewed
                # Need to figure how Header is involved
                TIC.Header = treeRecords[self.fieldDict['title']]
                parentItem.appendChild(newItem)
            except:
                pass

    def searchModel(self, person):
        '''
        get the modelIndex for a given appointment
        '''

        def searchNode(node):
            '''
            a function called recursively, looking at all nodes beneath node
            '''
            for child in node.childItems:
                if person == child.ItemName:
                    index = self.createIndex(child.row(), 0, child)
                    return index

                if child.childCount() > 0:
                    result = searchNode(child)
                    if result:
                        return result

        retarg = searchNode(self.parents[0])
        print(retarg)
        return retarg

    def find_GivenName(self, cname):
        app = None
        for category in self.categories:
            if category.Category == cname:
                app = category
                break
        if app != None:
            index = self.searchModel(app)
            return (True, index)
        return (False, None)


class customStyledTable(QTableView):
    def __init__(self, parent=None):
        QTableView.__init__(self, parent)

    def paintEvent(self, event):
        super(customStyledTable, self).paintEvent(event)

        # set the pen
        pen = QPen(Qt.white, 4)

        # Create the painter
        painter = QPainter(self.viewport())

        # Shortcuts to vertical and horizontal headers
        vh = self.verticalHeader()
        hh = self.horizontalHeader()

        # Get the first and last rows that are visible in the view and if the
        # last visiable row returns -1 set it to the row count
        firstVisualRow = max([vh.visualIndexAt(0), 0])
        lastVisualRow = vh.visualIndexAt(vh.viewport().height())
        if lastVisualRow == -1:
            lastVisualRow = self.model().rowCount(self.rootIndex()) - 1

        # Get the first and last columns that are visible in the view and if
        # if the last visible column is -1 set it to the column count.
        firstVisualColumn = max([hh.visualIndexAt(0), 0])
        lastVisualColumn = hh.visualIndexAt(hh.viewport().width())
        if lastVisualColumn == -1:
            lastVisualColumn = hh.count() - 1

        # Iterate through each row and column drawing only the
        # bottom and left side lines for each cell. Skipping rows and columns
        # that are hidden
        for vrow in range(firstVisualRow, lastVisualRow + 1, 2):
            row = vh.logicalIndex(vrow)
            FirstRow = (vrow == 0)
            if vh.isSectionHidden(row):
                continue
            # Get top left Y coordinate and row height
            rowY = self.rowViewportPosition(row)
            rowh = self.rowHeight(row)
            for vcol in range(firstVisualColumn, lastVisualColumn + 1):
                col = hh.logicalIndex(vcol)
                FirstColumn = (vcol == 0)
                if hh.isSectionHidden(col):
                    continue
                # Get top left X coordinate and column width
                colX = self.columnViewportPosition(col)
                colw = self.columnWidth(col)

                # Get the model index
                index = self.model().createIndex(row, col)

                # Specify top, bottom, left and right of the cell
                top = rowY
                bottom = rowY
                left = colX
                right = colX + colw

                # Save the painter and set the pen
                painter.save()
                painter.setPen(pen)

                # Draw Horizontal Lines
                painter.drawLine(left, bottom, right, bottom)

                # Restore painter
                painter.restore()


def cloneBranch2(self, conn, cursor, SQLBranchParent, DestinationTable, GroupID, ParentID, optionalLevels):
    # This is used to put the entire contents of a branch into another branch.  It can be the same table or another table.
    # print(treeItemDict)

    SQLSelect = "SELECT tblEquipmentList.TreeID, " \
                "tblEquipmentList.ParentTreeID, " \
                "tblEquipmentList.Level, " \
                "tblEquipmentList.Order, " \
                "tblEquipmentList.Display, " \
                "tblEquipmentList.Icon, " \
                "tblEquipmentList.ForeColor, " \
                "tblEquipmentList.Tags, " \
                "tblEquipmentList.Expanded, " \
                "tblEquipmentList.Highlighted, " \
                "Null as LinkedData, Null as AdditionalItems, Null as ListNumber"
    SQLFrom = " FROM tblEquipmentList"
    SQLOrder = " ORDER BY tblEquipmentList.Level, tblEquipmentList.Order;"

    SQLWhere = BSWhere(Field, Value, Scope, DataType)

    cursor.execute('''INSERT INTO TreeItems(Tree_id, PrimaryGroup_id, ParentTree_id,
                    ItemMaster_id, ItemTableType_id, ItemTable_id, Item_id, DisplayName, ItemOrder, FlattenedOrder, ItemLevel,
                    ForeColor, expanded, Header)
              VALUES(:Tree_id, :PrimaryGroup_id, :ParentTree_id,
                    :ItemMaster_id, :ItemTableType_id :ItemTable_id, :Item_id, :DisplayName, :ItemOrder, :FlattenedOrder, :ItemLevel,
                    :ForeColor, :expanded, :Header)''', treeItemDict)
    newID = cursor.lastrowid

    cursor.execute("UPDATE TreeItems SET Tree_id = {id} WHERE id = {id}". \
                   format(id=newID))

    cursor.close()