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

from PackageManager.Core.Database import DatabaseTools


def loadformdata(Base, formname, itemdata = {}):
    #Should replace this with query FormData
    #FormDataTables = FormDataTableInfo(Base, session, form_id)

    if formname == "Person":
        itemdata["Form_id"] = 1
        itemdata["FormName"] = "Person"
        itemdata["MainTableClass"] = Person
        itemdata["AttributeTableClass"] = PersonAttribute
        itemdata["AttributeTableName"] = "personattribute"
        itemdata["AttributeTable_id"] = None
        itemdata["CollectionAttributeTableName"] = "attPerson"
        itemdata["CollectionAttributeTable_id"] = -1

    return itemdata

class frmBase(object):
    pass

class frmAttributeBase(object):
    def loadcollectionmodel(self, index, MultipleRecordID = 0):
        data = {}
        data["row"] = index.row()
        data["id"] = self.dialog.tblAttributeCollectionTable.model().index(data["row"], 0).data()
        data["Name"] = self.dialog.tblAttributeCollectionTable.model().index(data["row"], 1).data()
        data["Table"] = self.dialog.tblAttributeCollectionTable.model().index(data["row"], 2).data()
        data["Table_id"] = self.dialog.tblAttributeCollectionTable.model().index(data["row"], 3).data()
        print("Data:", data)

        if self.dialog.txtItemID.text() != "": self.widgetData["Parent_id"] = int(self.dialog.txtItemID.text())
        #self.widgetData["Collection"] = collection # Person
        self.widgetData["Group_id"] = int(self.dialog.cmbAttributeGroup.model().index(self.dialog.cmbAttributeGroup.currentIndex(), 0, None).data())
        if self.widgetData["Group_id"] is None: self.widgetData["Group"] = None
        self.widgetData["AttributeCollectionTable_id"] = self.dialog.tblAttributeCollectionTable.model().index(index.row(), 0).data()
        self.widgetData["AttributeTable_id"] = self.dialog.tblAttributeCollectionTable.model().index(
            index.row(), 3).data()
        #if data["Table_id"] is not None: self.widgetData["AttributeTable_id"] = int(data["Table_id"])
        self.widgetData["AttributeTableName"] = data["Table"]
        self.widgetData["AttributeTable"] = data["Table"]

        connt = engines["Phoebe"].connect()
        # print("Widget Category", widgetData["AttributeCollectionTable_id"])
        if self.widgetData["AttributeCollectionTable_id"] is not None:
            print("Loading Attributes", self.widgetData)
            self.CollectionModel, self.widgetData, rowcount = DatabaseTools.loadAttributeModel(connt, session, MainBase, self.widgetData, MultipleRecordID)
            self.CollectionTemplate, rowcount2 = DatabaseTools.itemAttributes2(connt, MainBase, self.widgetData)

            self.dialog.tblAttributesItems.setModel(self.CollectionModel)
            self.dialog.cmbAttributeItemField.setModel(self.CollectionTemplate)
            self.dialog.cmbAttributeItemField.setModelColumn(self.widgetData["FieldName"])
            self.loadTableCombo(connt, self.widgetData, self.dialog.tblAttributesItems, rowcount)

            # Set some columns to be hidden
            setwidth = 0

            self.dialog.tblAttributesItems.setColumnWidth(self.widgetData["Item_id"], setwidth)
            self.dialog.tblAttributesItems.setColumnWidth(self.widgetData["PosAttributeTable_id"],setwidth)
            self.dialog.tblAttributesItems.setColumnWidth(self.widgetData["AttributeTableType_id"],setwidth)
            self.dialog.tblAttributesItems.setColumnWidth(self.widgetData["AttributeTableType"],setwidth)
            self.dialog.tblAttributesItems.setColumnWidth(self.widgetData["List_id"],setwidth)
            self.dialog.tblAttributesItems.setColumnWidth(self.widgetData["List"],setwidth)
            self.dialog.tblAttributesItems.setColumnWidth(self.widgetData["DataType_id"],setwidth)
            self.dialog.tblAttributesItems.setColumnWidth(self.widgetData["DataType"],setwidth)

        connt.close()

    def loadmultiplecollectionmodel(self):

        data = {}
        data["row"] = self.dialog.tblAttributeCollectionTable.selectionModel().currentIndex().row()
        data["id"] = self.dialog.tblAttributeCollectionTable.model().index(data["row"], 0).data()
        data["Name"] = self.dialog.tblAttributeCollectionTable.model().index(data["row"], 1).data()
        data["Table"] = self.dialog.tblAttributeCollectionTable.model().index(data["row"], 2).data()

        if self.dialog.txtItemID.text() != "": self.widgetData["Parent_id"] = int(self.dialog.txtItemID.text())
        #self.widgetData["Collection"] = collection # Person
        self.widgetData["Group_id"] = int(self.dialog.cmbAttributeGroup.model().index(self.dialog.cmbAttributeGroup.currentIndex(), 0, None).data())

        if self.widgetData["Group_id"] is None: self.widgetData["Group"] = None
        self.widgetData["AttributeCollectionTable_id"] = self.dialog.tblAttributeCollectionTable.model().index(self.dialog.tblAttributeCollectionTable.currentIndex().row(), 0).data()

        if data["id"]is not None: self.widgetData["AttributeTable_id"] = int(data["id"])
        self.widgetData["AttributeTable"] = data["Table"]

    def loadwidgetmapmodel(self, index, multipleitemid=0):
        Collection_id = self.dialog.tblAttributeCollectionTable.model().index(self.dialog.tblAttributeCollectionTable.currentIndex().row(), 0).data()
        print(" Collection ID: ", Collection_id)

        Group_id = self.dialog.cmbAttributeGroup.model().index(self.dialog.cmbAttributeGroup.currentIndex(), 0, None).data()
        print(" Group ID: ", Group_id)

        AttributeCollectionTable_id = self.dialog.tblAttributeCollectionTable.model().index(self.dialog.tblAttributeCollectionTable.currentIndex().row(), 0).data()
        print(" AttributeCollectionTable ID: ", AttributeCollectionTable_id)

        AttributeTable_id = self.dialog.tblAttributeCollectionTable.model().index(self.dialog.tblAttributeCollectionTable.currentIndex().row(), 3).data()
        #AttributeTable_id = self.dialog.tblAttributesItems.model().index(self.dialog.tblAttributesItems.currentIndex().row(), self.widgetData["PosAttributeTable_id"]).data()
        print(" Attribute Table ID: ", AttributeTable_id)

        Item_id = self.dialog.tblAttributesItems.model().index(self.dialog.tblAttributesItems.currentIndex().row(), self.widgetData["PosAttributeTable_id"]).data()
        print(" Item ID: ", Item_id)

        print(" Reference Table: ", self.dialog.tblAttributesItems.model().index(self.dialog.tblAttributesItems.currentIndex().row(), self.widgetData["ReferenceTable"]).data())

        List_id = self.dialog.tblAttributesItems.model().index(self.dialog.tblAttributesItems.currentIndex().row(), self.widgetData["List"]).data()
        if List_id == None: List_id = 0
        print(" List ID: ", List_id)

        print(" List: ", self.dialog.tblAttributesItems.model().index(self.dialog.tblAttributesItems.currentIndex().row(), self.widgetData["List_id"]).data())
        print(" Field Name: ", self.dialog.tblAttributesItems.model().index(self.dialog.tblAttributesItems.currentIndex().row(), self.widgetData["FieldName"]).data())

        databaseIndex = self.dialog.tblAttributesItems.model().index(self.dialog.tblAttributesItems.currentIndex().row(), self.widgetData["Value"])

        if isinstance(self.dialog.tblAttributesItems.indexWidget(databaseIndex), QComboBox):
            indexvalue = self.dialog.tblAttributesItems.indexWidget(databaseIndex).model().index(self.dialog.tblAttributesItems.indexWidget(databaseIndex).currentIndex(), 0).data()
            indexvalue2 = self.dialog.tblAttributesItems.indexWidget(databaseIndex).model().index(self.dialog.tblAttributesItems.indexWidget(databaseIndex).currentIndex(), 1).data()

            print(" Field Value: ", indexvalue, indexvalue2)
        else:
            #Text Value
            print(" Field Value: ", databaseIndex.data())


        formatobjectrecords = session.query(FormObjectMapping).all()
            #.filter_by(Form_id=1). \
            #                          filter_by(Collection_id=int(Collection_id)). \
            #                          filter_by(Group_id=int(Group_id)). \
            #                          filter_by(AttributeCollectionTable_id=int(AttributeCollectionTable_id)). \
            #                          filter_by(AttributeTable_id=AttributeTable_id). \
            #                          filter_by(AttributeItem_id=Item_id).all()

        GeneratedTableModel = QStandardItemModel(0, 5)

        if formatobjectrecords is not None:
            rowcount = 0
            for record in formatobjectrecords:
                fieldDict = DatabaseTools.row2dict(record)
                print("Control Data", fieldDict)
                if fieldDict is not None:
                    GeneratedTableModel.setItem(rowcount, 0, QStandardItem("%i" % int(fieldDict["id"])))
                    GeneratedTableModel.setItem(rowcount, 1, QStandardItem(fieldDict["NameText"]))
                    GeneratedTableModel.setItem(rowcount, 2, QStandardItem(fieldDict["ControlName"]))
                    GeneratedTableModel.setItem(rowcount, 3, QStandardItem(fieldDict["AttributeTableFilter"]))
                    GeneratedTableModel.setItem(rowcount, 4, QStandardItem(fieldDict["AttributeTableFilterValue"]))
                    GeneratedTableModel.setItem(rowcount, 5, QStandardItem(fieldDict["TreePath"]))
                    rowcount += 1
            self.widgetData["Row Count"] = rowcount

        GeneratedTableModel.setHeaderData(0, Qt.Horizontal, '#', role=Qt.DisplayRole)
        GeneratedTableModel.setHeaderData(1, Qt.Horizontal, 'FieldName', role=Qt.DisplayRole)
        GeneratedTableModel.setHeaderData(2, Qt.Horizontal, 'Widget Name', role=Qt.DisplayRole)
        GeneratedTableModel.setHeaderData(5, Qt.Horizontal, 'Tree Path', role=Qt.DisplayRole)
        self.dialog.tblWidgetMap.setModel(GeneratedTableModel)

        self.dialog.tblWidgetMap.setColumnWidth(0, 20)
        self.dialog.tblWidgetMap.setColumnWidth(1, 150)
        self.dialog.tblWidgetMap.setColumnWidth(2, 150)


    # @pyqtSlot(int)
    def on_cmbAttributeField_currentIndexChanged(self, index):
        listDataModel2 = QStandardItemModel(0, 0)
        self.dialog.cmbAttributeItemValue.setModel(listDataModel2)
        self.dialog.cmbAttributeItemValue.setModelColumn(1)

        AttributeIndex = self.dialog.cmbAttributeItemField.currentIndex()
        referenceList = self.dialog.cmbAttributeItemField.model().index(AttributeIndex, self.widgetData["List"]).data()
        referenceListid = self.dialog.cmbAttributeItemField.model().index(AttributeIndex, self.widgetData["List_id"]).data()
        attributelistValue = self.dialog.cmbAttributeItemField.model().index(AttributeIndex, self.widgetData["Value"]).data()
        if attributelistValue == "-" or attributelistValue == None: attributelistValue = 0

        if referenceList is not None and referenceList[:3] == "lst":
            tableName = DatabaseTools.get_class_by_tablename(MainBase, referenceList.lower())
            tableData = session.query(tableName).order_by(tableName.NameText)
            listDataModel2 = QStandardItemModel(0, 0)
            cmbboxindex = None
            for row2, record in enumerate(tableData):
                listDataModel2.setItem(row2, 0, QStandardItem("%i" % record.id))
                listDataModel2.setItem(row2, 1, QStandardItem(record.NameText))
                if record.Name_id is not None and record.Name_id != "":
                    referenceid = QStandardItem("%i" % record.Name_id)
                    listDataModel2.setItem(row2, 2, referenceid)
                if record.id == int(attributelistValue):
                    cmbboxindex = row2

            if cmbboxindex is not None: self.dialog.cmbAttributeItemField.setCurrentIndex(cmbboxindex)
        elif referenceList is not None:

            if referenceList == "Reference":
                tableName = DatabaseTools.get_class_by_tablename(MainBase, referenceList.lower())
                tableData = session.query(tableName).order_by(tableName.Word)

            else:
                referenceList2 = "btb" + referenceList[3:]
                tableName = DatabaseTools.get_class_by_tablename(MainBase, referenceList2)
                tableData = session.query(tableName).order_by(tableName.Title)

            listDataModel2 = QStandardItemModel(0, 0)
            cmbboxindex = None
            if tableData is not None:
                for row2, record in enumerate(tableData):
                    listDataModel2.setItem(row2, 0, QStandardItem("%i" % record.id))
                    if referenceList == "Reference":
                        listDataModel2.setItem(row2, 1, QStandardItem(record.Word))
                    else:
                        if record.Title is not None:
                            RecordTitle = str(record.Title)
                            listDataModel2.setItem(row2, 0, QStandardItem("%i" % record.id))
                            listDataModel2.setItem(row2, 1, QStandardItem(RecordTitle))

                    if record.id == int(attributelistValue):
                        # print("Record Found", record.id, record.Name)
                        cmbboxindex = row2

        self.dialog.cmbAttributeItemValue.setModel(listDataModel2)
        self.dialog.cmbAttributeItemValue.setModelColumn(1)

    def on_tabletextbox_ValueChanged(self, datadict):
        # print("on_tblAddress_txtValueChanged", datadict['row'])

        tableDict = self.loadTableDict(self.dialog.tblAttributesItems.model(), datadict['row'])
        tableDict["MultipleItem_id"] = self.dialog.spnMultipleRecord.value()
        # tableDict["Value"], =  self.dialog.tblAttributesItems.model().index(datadict['row'], self.widgetData["Value"]).data()
        databaseIndex = self.dialog.tblAttributesItems.model().index(datadict['row'], self.widgetData["Value"])
        # print(self.dialog.tblAttributesItems.indexWidget(databaseIndex).text())
        tableDict["Value"] = self.dialog.tblAttributesItems.indexWidget(databaseIndex).text()

        newitemid = self.saveAttributeTableData(self.widgetData["AttributeTableClass"], tableDict)

        if newitemid is not None:
            self.dialog.tblAttributesItems.model().setItem(datadict['row'], self.widgetData["Item_id"], QStandardItem("%i" % newitemid))

    # @pyqtSlot(dict)
    def on_tablecmbbox_ValueChanged(self, datadict):
        # print("on_tblAttributesItems_ValueChanged", datadict['row'])

        tableDict = self.loadTableDict(self.dialog.tblAttributesItems.model(), datadict['row'])
        # tableDict["List_id"] = datadict['index']
        tableDict["MultipleItem_id"] = self.dialog.spnMultipleRecord.value()
        # print("Index", datadict['index'], tableDict)
        databaseIndex = self.dialog.tblAttributesItems.model().index(datadict['row'], self.widgetData["Value"])

        indexvalue = self.dialog.tblAttributesItems.indexWidget(databaseIndex).model().index(datadict['index'], 0).data()

        tableDict["Value"] = indexvalue

        newitemid = self.saveAttributeTableData(self.widgetData["AttributeTableClass"], tableDict)

        if newitemid is not None:
            self.dialog.tblAttributesItems.model().setItem(datadict['row'], self.widgetData["Item_id"], QStandardItem("%i" % newitemid))

    def loadTableDict(self, tablemodel, row):

        tableDict = {}
        tableDict["Item_id"] = tablemodel.index(row, self.widgetData["Item_id"]).data()
        tableDict["AttributeTable_id"] = self.dialog.tblAttributeCollectionTable.model().index(self.dialog.tblAttributeCollectionTable.currentIndex().row(), 3).data()
        tableDict["AttributeTable"] = self.widgetData["AttributeTable"]
        tableDict["AttributeTableType_id"] = tablemodel.index(row, self.widgetData["AttributeTableType_id"]).data()
        tableDict["AttributeTableType"] = tablemodel.index(row, self.widgetData["AttributeTableType"]).data()
        tableDict["ReferenceTable"] = tablemodel.index(row, self.widgetData["ReferenceTable"]).data()
        tableDict["TreePath"] = tablemodel.index(row, self.widgetData["PTreePath"]).data()
        tableDict["List"] = tablemodel.index(row, self.widgetData["List"]).data()
        tableDict["List_id"] = tablemodel.index(row, self.widgetData["List_id"]).data()

        tableDict["FieldName"] = tablemodel.index(row, self.widgetData["FieldName"]).data()

        tableDict["DataType_id"] = tablemodel.index(row, self.widgetData["DataType_id"]).data()
        tableDict["DataType"] = tablemodel.index(row, self.widgetData["DataType"]).data()

        return tableDict

    def loadTableCombo(self, conn, widgetData, tblTable, rowcount):
        # Going to have to put this back in the main code till i figure out how to hook the on change
        # This little ditty is used to load data into a column of a table.
        # cursor = conn.cursor()
        if tblTable is not None:
            listDataModel2 = None
            for row in range(rowcount):
                #referenceList = tblTable.model().index(row, widgetData["List"]).data()
                #referencetable = tblTable.model().index(row, widgetData["ReferenceTable"]).data()
                #print("This is it", referenceList, referencetable)
                attributelistValue = tblTable.model().index(row, widgetData["Value"]).data()

                referencetable = tblTable.model().index(row, widgetData["ReferenceTable"]).data()
                #referencetable = tblTable.model().index(row, widgetData["List"]).data()

                #if referencetable is not None:
                referencetable = tblTable.model().index(row, widgetData["List"]).data()

                if attributelistValue == "-" or attributelistValue is None: attributelistValue = 0

                # print("Loading Combobox", referencetable, attributelistValue)
                # Since we are going through the rows might as well add the parent id to the mix
                if referencetable is not None and referencetable[:3] == "lst" and attributelistValue is not None:
                    tableName = DatabaseTools.get_class_by_tablename(Base, referencetable.lower())
                    # print("ReferenceList", referenceList)
                    tableData = session.query(tableName).order_by(tableName.NameText)
                    listDataModel2 = QStandardItemModel(0, 0)
                    cmbboxindex = None
                    for row2, record in enumerate(tableData):
                        listDataModel2.setItem(row2, 0, QStandardItem("%i" % record.id))
                        listDataModel2.setItem(row2, 1, QStandardItem(record.NameText))
                        # print(record.Name)
                        if record.Name_id is not None and record.Name_id != "":
                            referenceid = QStandardItem("%i" % record.Name_id)
                            listDataModel2.setItem(row2, widgetData["List"], referenceid)
                        # Add Value from wherever
                            # print(widgetData["List_id"], record.id,record.NameText, referenceid )

                        if record.id == int(attributelistValue):
                            # print("Record Found", record.id, record.Name)
                            cmbboxindex = row2

                    # widgetData["Value"] = 7
                    tblTable.openPersistentEditor(listDataModel2.index(row, widgetData["Value"]))

                    c = lario.customTable.TableComboModel(None, dataModel=listDataModel2, row=row, column=widgetData["Value"])
                    # print("Combobox Inserted",row, widgetData["Value"])
                    i = tblTable.model().index(row, widgetData["Value"])
                    tblTable.setIndexWidget(i, c)
                    if cmbboxindex is not None: tblTable.indexWidget(i).setCurrentIndex(cmbboxindex)

                    c.currentIndexChanged2[dict].connect(self.on_tablecmbbox_ValueChanged)
                # This is the reference of a attribute table
                elif referencetable is not None and referencetable != "None":
                    tableData = None
                    if referencetable == "Reference":
                        tableName = DatabaseTools.get_class_by_tablename(Base, referencetable.lower())
                        tableData = session.query(tableName).order_by(tableName.Word)

                    else:
                        referencetable2 = "btb" + referencetable[3:]
                        tableName = DatabaseTools.get_class_by_tablename(Base, referencetable2)
                        if tableName is not None:
                            tableData = session.query(tableName).order_by(tableName.Title)

                    listDataModel2 = QStandardItemModel(0, 0)
                    cmbboxindex = None
                    if tableData is not None:
                        for row2, record in enumerate(tableData):
                            listDataModel2.setItem(row2, 0, lario.TreeView.QStandardItem("%i" % record.id))
                            if referencetable == "Reference":
                                listDataModel2.setItem(row2, 1, lario.TreeView.QStandardItem(record.Word))
                            else:
                                if record.Title is not None:
                                    RecordTitle = str(record.Title)
                                    listDataModel2.setItem(row2, 1, lario.TreeView.QStandardItem(RecordTitle))

                                    # if record.Name_id is not None and record.Name_id != "":
                                    #    referenceid = lario.TreeView.QStandardItem("%i" % record.Name_id)
                                    #    listDataModel2.setItem(row2, 3, referenceid)

                            if record.id == int(attributelistValue):
                                # print("Record Found", record.id, record.Name)
                                cmbboxindex = row2
                    tblTable.openPersistentEditor(listDataModel2.index(row, widgetData["Value"]))

                    c = lario.customTable.TableComboModel(None, dataModel=listDataModel2, row=row, column=widgetData["Value"])
                    # print("Combobox Inserted",row, widgetData["Value"])
                    i = tblTable.model().index(row, widgetData["Value"])
                    tblTable.setIndexWidget(i, c)
                    if cmbboxindex is not None: tblTable.indexWidget(i).setCurrentIndex(cmbboxindex)

                    c.currentIndexChanged2[dict].connect(self.on_tablecmbbox_ValueChanged)
                else:
                    # print("Setting Text Value", attributelistValue)
                    c = lario.customTable.TableLineEditModel(None, row=row, column=widgetData["Value"])
                    i = tblTable.model().index(row, widgetData["Value"])
                    tblTable.setIndexWidget(i, c)

                    databaseIndex = tblTable.model().index(row, self.widgetData["Value"])

                    if attributelistValue is not None and tblTable.indexWidget(databaseIndex) is not None:
                        tblTable.indexWidget(databaseIndex).setText(str(attributelistValue))
                    c.textChanged2[dict].connect(self.on_tabletextbox_ValueChanged)

        return listDataModel2


    def saveAttributeTableData(self, tableClass, tableDict, widgetData=None):
        #This function is similar to controltodatabase in DatabaseTools.
        #TODO: We should try to update saveAttributeTableData to reference the DatabaseTools.controltodatabase

        if widgetData is None: widgetData = self.widgetData

        if widgetData["Parent_id"] != -1:
            currentdatetime = datetime.datetime.now()
            # print("saving", tableDict)
            session.begin()
            # print("AttributeTableTypeID", tableDict["AttributeTableType_id"])
            CreateUpdateAttribute = session.query(tableClass).filter(tableClass.id==tableDict["Item_id"]).first()
            print("Saving", tableDict["TreePath"])
            if CreateUpdateAttribute is None:
                CreateUpdateAttribute = tableClass(Parent_id=widgetData["Parent_id"],
                        MultipleItem_id=tableDict["MultipleItem_id"],
                        Collection_id=widgetData["Collection_id"],
                        Group_id=widgetData["Group_id"],
                        AttributeCollectionTable_id=widgetData["AttributeCollectionTable_id"],
                        ReferenceTable=tableDict["ReferenceTable"],
                        AttributeTable_id=tableDict["AttributeTable_id"],
                        AttributeTable=tableDict["AttributeTable"],
                        AttributeTableType_id=tableDict["AttributeTableType_id"],
                        AttributeTableType=tableDict["AttributeTableType"],
                        TreePath=tableDict["TreePath"],
                        List_id=tableDict["List_id"],
                        List=tableDict["List"],
                        FieldName=tableDict["FieldName"],
                        AttributeValueDataType_id=tableDict["DataType_id"],
                        AttributeValueDataType=tableDict["DataType"],
                        AttributeValue=tableDict["Value"],
                        AttributeOrder=0,

                        Date_Created=currentdatetime,
                        Date_Modified=currentdatetime,
                        Date_Accessed=currentdatetime)
                session.add(CreateUpdateAttribute)
            else:
                # print("Updating")
                CreateUpdateAttribute.FieldName = tableDict["FieldName"]
                CreateUpdateAttribute.AttributeValue = tableDict["Value"],
                CreateUpdateAttribute.AttributeOrder = 0
                 # Will Make this generic when we make generic attribute case
            session.commit()
            return CreateUpdateAttribute.id
        else:
            print("Record Needs to be Selected")

    def saveWidgetMapping(self, tabledict, controlname):
        pass #This is now taken care with widgetmap

    def GetWidget(self, Form, WidgetName):
        returnwidget = None
        returntype = None
        for widget in Form.children():
            if widget.objectName() == WidgetName:
                returnwidget = widget

                if isinstance(widget, QLineEdit):
                    returntype = "QLineEdit"
                if isinstance(widget, QComboBox):
                    returntype = "QCombobox"
                break

        return returnwidget, returntype

    def updatecontrolfromattribute(self, layout, Form_id):
        # A single attribute value is to update possibly multiple widgets

        attributetable = session.query(self.widgetData["AttributeTableClass"]).filter_by(Parent_id = self.widgetData["Parent_id"])
        treepath = 0

        #Checking to see how many widgets are attached to this
        for attributerecords in attributetable:
            print(1, attributerecords.FieldName, attributerecords.AttributeValue)
            NewValue = attributerecords.AttributeValue
            formatobjectrecords = session.query(FormObjectMapping).filter_by(Form_id = Form_id). \
                                                  filter_by(Collection_id = int(attributerecords.Collection_id)). \
                                                  filter_by(Group_id = int(attributerecords.Group_id)). \
                                                  filter_by(AttributeCollectionTable_id = int(attributerecords.AttributeCollectionTable_id)). \
                                                  filter_by(TreePath = int(treepath))

            for record in formatobjectrecords:
                widget, widgettype = self.GetWidget(layout, record.ControlName)
                print(2, record.ControlName, attributerecords.FieldName, attributerecords.AttributeValue)
                if isinstance(widget, QLineEdit):
                    widget.text(NewValue)

                if widgettype == "QCombobox":
                    for row in range(widget.model().rowCount(None)):
                        if int(widget.model().index(row, 0, None).data()) == int(NewValue):
                            widget.setCurrentIndex(row)
                            break