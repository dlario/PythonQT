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

from sqlalchemy import Column, DateTime, Integer, VARCHAR, DECIMAL, String, Boolean, ForeignKey, Float, \
    JSON

from PackageManager.Packages.ProgramBase.Database.dbBase import MainBase
import datetime

class UnitType(MainBase):
    __tablename__ = 'lstunittype'
    id = Column(Integer, primary_key=True)
    Name_id = Column(Integer)
    NameText = Column(String(75), unique=True)


class Unit(MainBase):
    __tablename__ = 'lstunit'
    id = Column(Integer, primary_key=True)
    UnitType = Column(Integer)
    Name_id = Column(Integer)
    NameText = Column(String(75), unique=True)