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

import os

#PySide Imports
from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (QMdiSubWindow)

#Other Programs

#Scripts

#Database

#Import Tables

#Addon Programs
#from yahoo_finance_data.yahoo_finance_historical_data_extract import YFHistDataExtr

import numpy as np

#12Data
from twelvedata import TDClient
from polygon import StocksClient

#from sklearn import preprocessing
#from sklearn.ensemble import RandomForestClassifier
#from sklearn import neighbors
#from sklearn.ensemble import AdaBoostClassifier
#from sklearn.ensemble import GradientBoostingClassifier
#from sklearn.svm import SVC
#import operator

#from sklearn import *
#from dateutil import parser
#from backtest import Strategy, Portfolio

#use('PySide6Agg')
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure

from qtalchemy import QueryTableModel

#Default Settings
basepath = os.path.dirname(os.path.abspath(__file__))
settingDatabase = "DSSettings.db"
settingTable = "tblProgramSettings"
from PackageManager.Packages.StockTrader.Resources import ICON_DIR

from PackageManager.Packages.StockTrader.Database.dbStockTrader import *
from PackageManager.Packages.ProjectList.Database.dbFinance import Currency

class StockTrader(QMdiSubWindow):
    def __init__(self, main, parent):
        super(StockTrader, self).__init__()

        self.PackageName = "StockTrader"
        self.setWindowTitle("StockMarket")
        self.setWindowIcon(QIcon(ICON_DIR + 'ProgramLogo.png'))

        self.ReferenceNumber_id = None
        self.main = main

        loader = QUiLoader()
        uiFile = os.path.join(basepath, 'frmStockMarket.ui')
        self.ui = loader.load(uiFile, self)

        self.TDKey = "0e36f5016f8d42f6b611f608e5b43ab4"
        self.PolyKey = "Xvj7uRpPnV2pwB3AS0LcQMcW56ZaCaTo"

        self.initDatabase()
        self.loadData()
        self.initCommands()

    def initDatabase(self):
        # Loading The Database
        pass
        self.sqlRegister = self.main.instance.sqlRegister
        # This is just an example of how to register a database
        base = "MainBase"
        name = "self.session"
        dbtype = "mysql+pymysql"
        login = ""
        password = ""
        location = "127.0.0.1"
        port = "3306"
        schema = "PackageManager"
        key = None,
        sshTunnel = None

        connectiondict = {}
        connectiondict["Location1"] = {"Base": "MainBase", "Session": "Location1", "DatabaseType": "mysql+pymysql",
                                       "Login": "", "Password": "", "Address": "127.0.0.1",
                                       "Port": "3306", "Schema": "PackageManager", "Key": None, "SSHTunnel": None,
                                       "SyncType": "ASAP"}

        self.sqlRegister.registarInstance(connectiondict["Location1"])

        self.sqlRegister.sqlDict["Location1"].createSession(base, dbtype, login, password, location, port,
                                                                   schema, key, sshTunnel)
        # This is the table coordinator
        self.sqlRegister.masterSession = self.sqlRegister.sqlDict["Location1"].session
        self.sqlRegister.masterBase = self.sqlRegister.sqlDict["Location1"].base
        self.session = self.sqlRegister.sqlDict["Location1"].session
        self.base = self.sqlRegister.sqlDict["Location1"].base

        self.sqlRegister.masterTable = "MasterTable"
        self.sqlRegister.masterFieldList = "MasterFieldList"

    def initCommands(self):
        self.ui.cmbNewPortfolio.clicked.connect(self.on_cmbNewPortfolio_clicked)
        self.ui.cmdBuyOrder.clicked.connect(self.on_cmdBuyOrder_clicked)
        self.ui.cmdBuy.clicked.connect(self.on_cmdBuy_clicked)
        self.ui.cmdSell.clicked.connect(self.on_cmdSell_clicked)
        #self.ui.cmdSell.textChanged.connect(self.on_cmdSell_editTextChanged)
        self.ui.cmbCreateAccount.clicked.connect(self.on_cmbCreateAccount_clicked)

    def testYahooFinance(self):
        import yfinance as yf
        ticker = yf.Ticker('GOOGL').info
        market_price = ticker['regularMarketPrice']
        previous_close_price = ticker['regularMarketPreviousClose']
        print('Ticker: GOOGL')
        print('Market Price:', market_price)
        print('Previous Close Price:', previous_close_price)

    def testtwelvedata(self):
        client = TDClient(apikey=self.TDKey)
        ts = client.time_series(
            symbol="MSFT",
            outputsize=75,
            interval="1day",
        )

        # 1. Returns OHLCV chart
        ts.as_pyplot_figure()

        # 2. Returns OHLCV + BBANDS(close, 20, 2, SMA) + %B(close, 20, 2 SMA) + STOCH(14, 3, 3, SMA, SMA)
        ts.with_bbands().with_percent_b().with_stoch(slow_k_period=3).as_pyplot_figure()

    def testpolygonio(self):
        ticker = "AAPL"
        timout = 15
        max_connections = 100
        client = StocksClient(self.PolyKey, connect_timeout=timout, max_connections=max_connections)
        # List Aggregates (Bars)

        # Get Last Trade
        trade = client.get_last_trade(ticker)
        print(trade)


        client.close()

    def loadData(self):
        self.refreshAccountTable()
        self.loadMarket()
        self.loadCompany()
        self.loadCurrency()
        self.loadPortfolio()

        #Set Default Values
        for row in range(self.ui.cmbCurrency.model().rowCount()):
            DefaultValue = "CAD"
            if self.ui.cmbCurrency.model().index(row, 1).data() == DefaultValue:
                self.ui.cmbCurrency.setCurrentIndex(row)
                break

    def loadMarket(self):
        # Add Stockdata
        qrymarket = self.session.query(Market.id, Market.NameText.label("Market")).order_by(Market.NameText)
        self.ui.cmbMarket.setModel(QueryTableModel(qrymarket))
        #self.ui.cmbMarket.model().reset_content_from_self.session()
        self.ui.cmbMarket.setModelColumn(1)

    def loadCompany(self):
        qrycompany = self.session.query(TradingCompany.id, TradingCompany.NameText.label("Program Name"), TradingCompany.Ticker).order_by(
            TradingCompany.NameText)
        self.ui.mplfigs.setModel(QueryTableModel(qrycompany))
        #self.ui.mplfigs.model().reset_content_from_self.session()
        self.ui.mplfigs.hideColumn(0)

        self.ui.cmbStockCompany.setModel(QueryTableModel(qrycompany))
        #self.ui.cmbStockCompany.model().reset_content_from_self.session()
        self.ui.cmbStockCompany.setModelColumn(1)

    def loadCurrency(self):
        qrycurrency = self.session.query(Currency.id, Currency.NameText.label("Currency")).order_by(Currency.NameText)
        self.ui.cmbCurrency.setModel(QueryTableModel(qrycurrency))
        #self.ui.cmbCurrency.model().reset_content_from_self.session()
        self.ui.cmbCurrency.setModelColumn(1)

    def loadPortfolio(self):
        qryportfolio = self.session.query(PortfolioList.id, PortfolioList.Title.label("Program Name"),
                                     Market.NameText.label("Market")) \
            .join(Market, PortfolioList.Market_id == Market.id).order_by(PortfolioList.Title)
        self.ui.tblPorfolio.setModel(QueryTableModel(qryportfolio))
        #self.ui.tblPorfolio.model().reset_content_from_self.session()
        self.ui.tblPorfolio.hideColumn(0)

    @Slot()
    def on_cmdAddCompany_clicked(self):

        data = {}
        data["Market"] = 1
        data["Company"] = self.ui.txtCompanyName.text()
        data["Ticker"] = self.ui.txtTickerName.text()

        self.session.begin()
        newcompany = TradingCompany(Market_id=data["Market"],
                             NameText=data["Company"],
                             Ticker=data["Ticker"])
        self.session.add(newcompany)
        self.session.commit()

        self.loadTables()

    def refreshAccountTable(self):
        qryaccount = self.session.query(StockAccount.id, StockAccount.NameText.label("Account Name"),
                                     StockAccount.Cash.label("Cash"), StockAccount.Currency, StockAccount.Date_Created,
                                        StockAccount.Comments).order_by(StockAccount.NameText)
        self.ui.tblAccounts.setModel(QueryTableModel(qryaccount))
        #self.ui.tblAccounts.model().reset_content_from_list.session()
        self.ui.tblAccounts.hideColumn(0)

    @Slot()
    def on_cmbCreateAccount_clicked(self):
        self.session.begin_nested()
        newaccount = StockAccount(NameText=self.ui.txtAccount.text(),
                                  Cash=self.ui.spnStartingCash.value(),
                                  Currency=self.ui.cmbCurrency.model().index(self.ui.cmbCurrency.currentIndex(), 0).data(),
                                  Comments=self.ui.txtAccountComments.text())
        self.session.add(newaccount)
        self.session.commit()
        self.refreshAccountTable()


    @Slot()
    def on_cmbNewPortfolio_clicked(self):
        self.session.begin()

        newportfolio = PortfolioList(
            Market_id=self.ui.cmbMarket.model().index(self.ui.cmbMarket.currentIndex(), 0, None).data(),
            Title=self.ui.txtPortfolio.text())
        self.session.add(newportfolio)
        self.session.commit()

        qryportfolio = self.session.query(PortfolioList.id, PortfolioList.Title.label("Program Name"),
                                     Market.NameText.label("Market")) \
            .join(Market, PortfolioList.Market_id == Market.id).order_by(PortfolioList.Title)
        self.ui.tblPorfolio.setModel(QueryTableModel(qryportfolio))
        self.ui.tblPorfolio.model().reset_content_from_self.session()
        self.ui.tblPorfolio.hideColumn(0)

    @Slot()
    def on_cmdBuyOrder_clicked(self):
        print("Buy-Sell Order!!")

        self.session.begin()
        newcompany = TradingCompany(NameText=data["Company"],
                             Ticker=data["Ticker"])
        self.session.add(newcompany)
        self.session.commit()

    @Slot()
    def on_cmdBuy_clicked(self):
        print("Buy Now!!")

        if self.ui.boolbuyupperdir.text() == "^":
            buyupperdir = 1
        else:
            buyupperdir = -1

        if self.ui.boolbuylowerdir.text() == "^":
            buylowerdir = 1
        else:
            buylowerdir = -1

        if self.ui.boolselldirupper.text() == "^":
            selldirupper = 1
        else:
            selldirupper = -1

        if self.ui.boolselldirlower.text() == "^":
            selldirlower = 1
        else:
            selldirlower = -1

        self.session.begin()

        stockrecord = StockPortfolio(
            Portfolio_id=self.ui.tblPorfolio.model().index(self.ui.tblPorfolio.currentIndex(), 0, None).data(),
            Company_id=self.ui.cmbStockCompany.model().index(self.ui.cmbStockCompany.currentIndex(), 0,
                                                             None).data(),
            BuyUpper=self.ui.spnbuyupper.currentText(),
            BuyUpperDirection=buyupperdir,
            BuyLower=self.ui.spnbuylower.currentText(),
            BuyLowerDirection=buylowerdir,
            SellUpper=self.ui.spnsellupper.currentText(),
            SellUpperDirection=selldirupper,
            SellLower=self.ui.spnselllower.currentText(),
            SellLowerDirection=selldirlower,
            Quantity=self.ui.spnBuyOrder.currentText())
        self.session.add(stockrecord)
        self.session.commit()

    @Slot()
    def on_cmdSell_clicked(self):
        print("Sell Now!!")

        self.session.begin()
        newcompany = TradingCompany(NameText=data["Company"],
                             Ticker=data["Ticker"])
        self.session.add(newcompany)
        self.session.commit()

    @Slot()
    def on_cmdSell_editTextChanged(self, textvalue):
        print(textvalue)


    def mplfigs_cell_clicked(self, index):

        self.ticker = self.mplfigs.model().index(index.row(), 2, None).data()

        print(self.ticker)
        self.rmmpl()
        self.uploadStockData()

        # self.addmpl(self.fig_dict[text])
        self.plotStock()

    def addmpl(self, fig):
        self.canvas = FigureCanvas(fig)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()
        self.toolbar = NavigationToolbar(self.canvas,
                                         self.mplwindow, coordinates=True)
        self.mplvl.addWidget(self.toolbar)

    # This is the alternate toolbar placement. Susbstitute the three lines above
    # for these lines to see the different look.
    #        self.toolbar = NavigationToolbar(self.canvas,
    #                self, coordinates=True)
    #        self.addToolBar(self.toolbar)

    def rmmpl(self):
        self.ui.mplvl.removeWidget(self.canvas)
        self.canvas.close()
        self.ui.mplvl.removeWidget(self.toolbar)
        self.toolbar.close()

    def moving_average(self, x, n, type='simple'):
        """
        compute an n period moving average.

        type is 'simple' | 'exponential'

        """
        x = np.asarray(x)
        if type == 'simple':
            weights = np.ones(n)
        else:
            weights = np.exp(np.linspace(-1., 0., n))

        weights /= weights.sum()

        a = np.convolve(x, weights, mode='full')[:len(x)]
        a[:n] = a[n]
        return a

    def relative_strength(self, prices, n=14):
        """
        compute the n period relative strength indicator
        http://stockcharts.com/school/doku.php?id=chart_school:glossary_r#relativestrengthindex
        http://www.investopedia.com/terms/r/rsi.asp
        """

        deltas = np.diff(prices)
        seed = deltas[:n + 1]
        up = seed[seed >= 0].sum() / n
        down = -seed[seed < 0].sum() / n
        rs = up / down
        rsi = np.zeros_like(prices)
        rsi[:n] = 100. - 100. / (1. + rs)

        for i in range(n, len(prices)):
            delta = deltas[i - 1]  # cause the diff is 1 shorter

            if delta > 0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta

            up = (up * (n - 1) + upval) / n
            down = (down * (n - 1) + downval) / n

            rs = up / down
            rsi[i] = 100. - 100. / (1. + rs)

        return rsi

    def moving_average_convergence(self, x, nslow=26, nfast=12):
        """
        compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
        return value is emaslow, emafast, macd which are len(x) arrays
        """
        emaslow = self.moving_average(x, nslow, type='exponential')
        emafast = self.moving_average(x, nfast, type='exponential')
        return emaslow, emafast, emafast - emaslow

    def plotStock(self):
        plt.rc('axes', grid=True)
        plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)

        textsize = 9
        left, width = 0.1, 0.8
        rect1 = [left, 0.7, width, 0.2]
        rect2 = [left, 0.3, width, 0.4]
        rect3 = [left, 0.1, width, 0.2]

        # fig = plt.figure(facecolor='white')
        fig = Figure()
        axescolor = '#f6f6f6'  # the axes background color

        ax1 = fig.add_axes(rect1, axisbg=axescolor)  # left, bottom, width, height
        ax2 = fig.add_axes(rect2, axisbg=axescolor, sharex=ax1)
        ax2t = ax2.twinx()
        ax3 = fig.add_axes(rect3, axisbg=axescolor, sharex=ax1)

        # plot the relative strength indicator
        prices = self.r.adj_close
        rsi = self.relative_strength(prices)
        fillcolor = 'darkgoldenrod'

        ax1.plot(self.r.date, rsi, color=fillcolor)
        ax1.axhline(70, color=fillcolor)
        ax1.axhline(30, color=fillcolor)
        ax1.fill_between(self.r.date, rsi, 70, where=(rsi >= 70), facecolor=fillcolor, edgecolor=fillcolor)
        ax1.fill_between(self.r.date, rsi, 30, where=(rsi <= 30), facecolor=fillcolor, edgecolor=fillcolor)
        ax1.text(0.6, 0.9, '>70 = overbought', va='top', transform=ax1.transAxes, fontsize=textsize)
        ax1.text(0.6, 0.1, '<30 = oversold', transform=ax1.transAxes, fontsize=textsize)
        ax1.set_ylim(0, 100)
        ax1.set_yticks([30, 70])
        ax1.text(0.025, 0.95, 'RSI (14)', va='top', transform=ax1.transAxes, fontsize=textsize)
        ax1.set_title('%s daily' % self.ticker)

        # plot the price and volume data
        dx = self.r.adj_close - self.r.close
        low = self.r.low + dx
        high = self.r.high + dx

        deltas = np.zeros_like(prices)
        deltas[1:] = np.diff(prices)
        up = deltas > 0
        ax2.vlines(self.r.date[up], low[up], high[up], color='black', label='_nolegend_')
        ax2.vlines(self.r.date[~up], low[~up], high[~up], color='black', label='_nolegend_')
        ma20 = self.moving_average(prices, 20, type='simple')
        ma200 = self.moving_average(prices, 200, type='simple')

        linema20, = ax2.plot(self.r.date, ma20, color='blue', lw=2, label='MA (20)')
        linema200, = ax2.plot(self.r.date, ma200, color='red', lw=2, label='MA (200)')

        last = self.r[-1]
        s = '%s O:%1.2f H:%1.2f L:%1.2f C:%1.2f, V:%1.1fM Chg:%+1.2f' % (
            self.today.strftime('%d-%b-%Y'),
            last.open, last.high,
            last.low, last.close,
            last.volume * 1e-6,
            last.close - last.open)
        t4 = ax2.text(0.3, 0.9, s, transform=ax2.transAxes, fontsize=textsize)

        props = font_manager.FontProperties(size=10)
        leg = ax2.legend(loc='center left', shadow=True, fancybox=True, prop=props)
        leg.get_frame().set_alpha(0.5)

        volume = (self.r.close * self.r.volume) / 1e6  # dollar volume in millions
        vmax = volume.max()
        poly = ax2t.fill_between(self.r.date, volume, 0, label='Volume', facecolor=fillcolor, edgecolor=fillcolor)
        ax2t.set_ylim(0, 5 * vmax)
        ax2t.set_yticks([])

        # compute the MACD indicator
        fillcolor = 'darkslategrey'
        nslow = 26
        nfast = 12
        nema = 9
        emaslow, emafast, macd = self.moving_average_convergence(prices, nslow=nslow, nfast=nfast)
        ema9 = self.moving_average(macd, nema, type='exponential')
        ax3.plot(self.r.date, macd, color='black', lw=2)
        ax3.plot(self.r.date, ema9, color='blue', lw=1)
        ax3.fill_between(self.r.date, macd - ema9, 0, alpha=0.5, facecolor=fillcolor, edgecolor=fillcolor)

        ax3.text(0.025, 0.95, 'MACD (%d, %d, %d)' % (nfast, nslow, nema), va='top',
                 transform=ax3.transAxes, fontsize=textsize)

        # ax3.set_yticks([])
        # turn off upper axis tick labels, rotate the lower ones, etc
        for ax in ax1, ax2, ax2t, ax3:
            if ax != ax3:
                for label in ax.get_xticklabels():
                    label.set_visible(False)
            else:
                for label in ax.get_xticklabels():
                    label.set_rotation(30)
                    label.set_horizontalalignment('right')

            ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')

        class MyLocator(mticker.MaxNLocator):
            def __init__(self, *args, **kwargs):
                mticker.MaxNLocator.__init__(self, *args, **kwargs)

            def __call__(self, *args, **kwargs):
                return mticker.MaxNLocator.__call__(self, *args, **kwargs)

        # at most 5 ticks, pruning the upper and lower so they don't overlap
        # with other ticks
        # ax2.yaxis.set_major_locator(mticker.MaxNLocator(5, prune='both'))
        # ax3.yaxis.set_major_locator(mticker.MaxNLocator(5, prune='both'))

        ax2.yaxis.set_major_locator(MyLocator(5, prune='both'))
        ax3.yaxis.set_major_locator(MyLocator(5, prune='both'))

        self.addmpl(fig)
        # plt.show()