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

from sqlalchemy import Table, Column,DateTime, Integer, String, Text, Date, Boolean, Numeric, MetaData, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship, Session, scoped_session, backref
from sqlalchemy.ext.declarative import declarative_base, declared_attr
import datetime
from qtalchemy import *

class Timestamp(object):
    Date_Created = Column(DateTime, default=datetime.datetime.now())
    Date_Modified = Column(DateTime, default=datetime.datetime.now())
    Date_Accessed = Column(DateTime, default=datetime.datetime.now())

class Base(object):
    mysql_engine='InnoDB',
    #id = Column(Integer, primary_key=True)

metadata = MetaData()
Base = declarative_base(metadata=metadata,cls=ModelObject)
