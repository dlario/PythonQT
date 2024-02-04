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

import sys
#import pyodbc
import os
import sqlite3
import datetime
import collections
import json

from PySide6.QtGui import QStandardItem, QStandardItemModel

def loadDefaultValue(database, datatable, location, setting):

    SQLSelect = "SELECT key"
    SQLFrom = " FROM %s" % (datatable)
    SQLWhere = " WHERE location = %i AND title = \"%s\"" % (location, str(setting))

    strSQL = SQLSelect + SQLFrom + SQLWhere + ";"

    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(strSQL)
    SettingValue = None
    record = cursor.fetchone()
    if record is not None:
        if record[0] is not None:
            if record[0] == "text":
                pass
            else:
                SettingValue = str(record[0])

    cursor.close()
    conn.close()

    return SettingValue

def loadSettings(database, datatable, ID):
    data = {}
    data["TableName"] = datatable
    data["Setting_id"] = int(ID)

    SQLSelect = "SELECT {TableName}.ID," \
                "{TableName}.location," \
                "{TableName}.section," \
                "{TableName}.title," \
                "{TableName}.key," \
                "{TableName}.\"desc\"," \
                "tblDataTypes.dataType," \
                "tblOptionTypes.optionType," \
                "tblOptionTypes.\"default\"," \
                "tblOptionTypes.options," \
                "{TableName}.options AS linkedoptions".format(**data)
    SQLFrom = " FROM {TableName}" \
              " LEFT JOIN tblDataTypes ON ({TableName}.datatype = tblDataTypes.ID)" \
              " LEFT JOIN tblOptionTypes ON ({TableName}.optiontype = tblOptionTypes.ID)".format(**data)
    SQLWhere = " WHERE {TableName}.ID = {Setting_id}".format(**data)

    strSQL = SQLSelect + SQLFrom + SQLWhere # + ";"

    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(strSQL)
    row = cursor.fetchone()
    fieldDict = {item[0]: row[i] for i, item in enumerate(cursor.description)}

    return fieldDict

def dictSettings(ID=None,
                 location=None,
                 section=None,
                 title=None,
                 key=None,
                 desc=None,
                 dataType=None,
                 optionType=None,
                 default=None,
                 options=None):

    ItemNames = ['ID', 'location', 'section', 'title', 'key', 'desc', 'dataType', 'optionType', 'default', 'options']
    Items = [ID, location, section, title, key, desc, dataType, optionType, default, options]

    fieldDict = {item: Items[i] for i, item in enumerate(ItemNames)}
    return fieldDict

def saveSettings(Database = None, Datatable = None,
                 Location = None,
                 SettingDict = None,
                 Datatype = None,
                 OptionType = None):

    SQLUpdate ="UPDATE %s" % Datatable
    SQLWhere = " WHERE ID = %s" % SettingDict['ID']
    SQLSet = " SET location = \"%s\"," % SettingDict['location']
    SQLSet += " section = \"%s\"," % SettingDict['section']
    SQLSet += " title = \"%s\"," % SettingDict['title']
    SQLSet += " key = \"%s\"," % SettingDict['key']
    SQLSet += " \"desc\" = \"%s\"," % SettingDict['desc']
    SQLSet += " options = \"%s\"," % SettingDict['options']

    if Datatype == None: Datatype = 0
    if OptionType == None: OptionType = 0

    SQLSet += " datatype = %i," % int(Datatype)
    SQLSet += " optiontype = %i" % int(OptionType)

    strSQL = SQLUpdate + SQLSet + SQLWhere # + ";"
    #print(strSQL)

    conn = sqlite3.connect(Database)
    cursor = conn.cursor()
    cursor.execute(strSQL)
    conn.commit()
    cursor.close()
    conn.close()

def addSettings(Database = None, Datatable = None,
                 Location = None,
                 SettingDict = None,
                 Datatype = 0,
                 OptionType = 0):
    #Not sure if default above takes none values into account
    if Datatype == None: Datatype = 0
    if OptionType == None: OptionType = 0

    print(SettingDict)
    print(Datatable)
    #SQLInsert ="INSERT INTO %s(location, section, title, key, desc, options, type, OptionType)" % Datatable

    #SQLValues = " VALUES(%s, %s, %s, %s, %s, %s, %i, %i)" % (SettingDict['location'], SettingDict['section'],
    #                                                SettingDict['title'], SettingDict['key'], SettingDict['desc'],
    #                                                SettingDict['options'], int(Datatype), int(OptionType))
    #strSQL = SQLInsert + SQLValues

    #print(strSQL)

    conn = sqlite3.connect(Database)
    cursor = conn.cursor()
    data = {}
    data["TableName"] = Datatable
    #date["Setting_id"] = int(ID)

    cursor.execute('''INSERT INTO tblProgramSettings (location, section, title, key, desc, options, dataType) VALUES(:location, :section, :title, :key, :desc, :options, :dataType)''', SettingDict)
    newID = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()
    return newID

def loadDataTypes(database, datatable):
    SQLSelect = "SELECT id, dataType"
    SQLFrom = " FROM %s" % (datatable)
    SQLOrder = " ORDER BY dataType"

    strSQL = SQLSelect + SQLFrom + SQLOrder # + ";"

    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(strSQL)

    OptionTypes = []

    for row in cursor.fetchall():
        t = [row[0], row[1]]
        #t =  row[1]
        OptionTypes.append(t)

    cursor.close()
    conn.close()

    return OptionTypes

def loadOptionsTypes(database, datatable):
    SQLSelect = "SELECT ID, optionType, options"
    SQLFrom = " FROM %s" % (datatable)
    SQLOrder = " ORDER BY optionType, options"

    strSQL = SQLSelect + SQLFrom + SQLOrder # + ";"

    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(strSQL)

    OptionTypes = []

    for row in cursor.fetchall():
        t = [row[0], row[1], row[2]]
        #print(t)
        OptionTypes.append(t)

    cursor.close()
    conn.close()

    return OptionTypes

def loadOptions(database, datatable, optiontype):
    SQLSelect = "SELECT ID, optionType, options"
    SQLFrom = " FROM %s" % (datatable)
    SQLWhere = " WHERE ID = %i " % (optiontype)

    strSQL = SQLSelect + SQLFrom + SQLWhere + ";"

    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(strSQL)

    OptionTypes = []

    for row in cursor.fetchall():
        t = [row.ID, row.optionType, row.options]
        OptionTypes.append(t)

    cursor.close()
    conn.close()
    #print(OptionTypes)

    return OptionTypes

def createJson(location):
        conn = sqlite3.connect(datatable)
        cursor = conn.cursor()

        cursor.execute('''
                    SELECT ID, type, title, description, section, key, type
                    FROM tblSettings
                    WHERE location = ?
                    ORDER BY section, title
                    '''), (location)

        rows = cursor.fetchall()

        # Convert query to row arrays

        rowarray_list = []
        for row in rows:
            t = (row.type, row.title, row.description, row.section,
                 row.key)
            rowarray_list.append(t)

        j = json.dumps(rowarray_list)
        rowarrays_file = 'settings.js'
        f = open(rowarrays_file,'w')

        # Convert query to objects of key-value pairs

        objects_list = []
        for row in rows:
            d = collections.OrderedDict()
            d['ID'] = row.ID
            d['type'] = row.type
            d['title'] = row.title
            d['desc'] = row.description
            d['section'] = row.section
            d['key'] = row.key
            objects_list.append(d)

        j = json.dumps(objects_list)
        objects_file = 'settings.js'
        self.JsonSetting = open(objects_file,'w')

        conn.close()

def saveDefaultValue(datatable = None, settingID = None, setting = None, decription = None):
        SQLUpdate ="UPDATE %s" % datatable
        SQLWhere = " WHERE ID = " + str(settingID)

        if type(setting) == str:
            SQLSet = " SET %s = \"%s\"" % str(setting)
        if type(setting) == int:
            SQLSet = "SET key = %s" % setting
        strSQL = SQLUpdate + SQLSet + SQLWhere + ";"
        #print(strSQL)
        try:
            conn = sqlite3.connect(datatable)
            cursor = conn.cursor()
            cursor.execute(strSQL)
            conn.commit()

        except:
            print("Update Error")
            print(strSQL)

def SettingTable(datatable):
        conn = sqlite3.connect(datatablen)
        cursor = conn.cursor()

        newTable = QStandardItemModel()

        strSQL = "SELECT * FROM tblProgramSettings ORDER BY section, title"

        cursor.execute(strSQL)

        recordrow = 0
        for record in cursor.fetchall(): # cursors are iterable
            newTable.setItem(recordrow, 0, QStandardItem(str(record[0])))
            newTable.setItem(recordrow, 1, QStandardItem(str(record[1])))
            newTable.setItem(recordrow, 2, QStandardItem(str(record[2])))
            newTable.setItem(recordrow, 3, QStandardItem(str(record[3])))
            newTable.setItem(recordrow, 4, QStandardItem(str(record[4])))
            recordrow += 1

        fieldColumn = 0
        for headerName in cursor.description:
            newTable.setHeaderData(fieldColumn, Qt.Horizontal, headerName[0], role=Qt.DisplayRole)
            fieldColumn += 1

        cursor.close()
        conn.close()

        return newTable