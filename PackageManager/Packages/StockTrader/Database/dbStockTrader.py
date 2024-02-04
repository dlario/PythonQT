## Copyright 2023 David Lario
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

from sqlalchemy import Column, TIMESTAMP, Integer, String, DateTime, Boolean, Numeric

from PackageManager.Packages.ProgramBase.Database.dbBase import MainBase
import datetime

class StockAccount(MainBase):
    __tablename__ = 'stockaccount'
    id = Column(Integer, primary_key=True)
    Name_id = Column(Integer)
    NameText = Column(String(75), unique=True)
    Cash = Column(Numeric(10,2))
    Currency = Column(Integer)
    Comments = Column(String(255))
    Date_Created = Column(DateTime, default=datetime.datetime.now())
    Date_Modified = Column(DateTime, default=datetime.datetime.now())
    Date_Accessed = Column(DateTime, default=datetime.datetime.now())

class AccountHistory(MainBase):
    __tablename__ = 'accounthistory'
    id = Column(Integer, primary_key=True)
    TransactionDate = Column(TIMESTAMP)
    Stock_ID = Column(Integer)
    TransactionType = Column(Integer)
    Quantity = Column(Integer)
    Price = Column(Numeric(10,2))
    Currency = Column(Integer)
    Account_id = Column(Integer)


class PortfolioList(MainBase):
    __tablename__ = 'lstportfolio'
    id = Column(Integer, primary_key=True)
    Market_id = Column(Integer)
    Title = Column(String(255))


class StockPortfolio(MainBase):
    __tablename__ = 'stockportfolio'
    id = Column(Integer, primary_key=True)
    Portfolio_id = Column(Integer)
    Company_id = Column(Integer)
    BuyUpper = Column(Integer)
    BuyUpperDirection = Column(Boolean)
    BuyLower = Column(Integer)
    BuyLowerDirection = Column(Boolean)
    SellUpper = Column(Integer)
    SellUpperDirection = Column(Boolean)
    SellLower = Column(Integer)
    SellLowerDirection = Column(Boolean)
    Quantity = Column(Integer)
    BuyDateTime = Column(TIMESTAMP)
    SellDateTime = Column(TIMESTAMP)
    BuyLevel = Column(Integer)
    SellLevel = Column(Integer)


class Market(MainBase):
    __tablename__ = 'lstmarket'
    id = Column(Integer, primary_key=True)
    NameText = Column(String(50))


class TradingCompany(MainBase):
    __tablename__ = 'lsttradingcompany'
    id = Column(Integer, primary_key=True)
    Market_id = Column(Integer)
    NameText = Column(String(255))
    Ticker = Column(String(10))