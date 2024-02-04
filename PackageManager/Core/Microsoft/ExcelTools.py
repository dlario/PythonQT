import xlwings as xw
import pandas as pd
import numpy as np
import os
import sys

class xlbook(object):
    def __init__(self, parent, path=None):
        self.parent = parent
        self.app = xw.App(visible=False)
        self.wb = self.app.books.add()
        self.ws = self.wb.sheets.active
        self.wb.activate()
        self.wb.save()
        self.wb.close()
        self.app.quit()
        self.app.kill()

    def loadDatamap(self):
        self.app = xw.App(visible=False)
        self.wb = self.app.books.open(self.parent.datamap)
        self.ws = self.wb.sheets.active
        self.wb.activate()

    def addRow(self, row):
        self.ws.range('A1').value = row
