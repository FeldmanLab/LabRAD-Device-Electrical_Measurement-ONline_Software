import sys
import twisted
from PyQt5 import QtCore, QtGui, QtTest, uic
from twisted.internet.defer import inlineCallbacks, Deferred
import numpy as np
import pyqtgraph as pg
#import exceptions
import time
import threading
import copy

from DEMONSFormat import *

path = os.path.dirname(os.path.realpath(__file__))
Ui_CustomOutputSetting, QtBaseClass = uic.loadUiType(os.path.join(path , "CustomOutputInstrumentSetting.ui"))

class CustomOutputSetting(QtGui.QMainWindow, Ui_CustomOutputSetting):
    complete = QtCore.pyqtSignal()

    def __init__(self, reactor, parent = None):
        super(CustomOutputSetting, self).__init__(parent)
        from labrad.units import V, mV, us, ns, GHz, MHz, Hz, K, deg, s,A 

        self.reactor = reactor
        self.setupUi(self)
        
        self.Servers = {}
        self.Devices = {}

        self.parent = parent

        self.DeviceList = {}



        self.units = {
            'Hz': Hz,
            'V': V,
            'mV': mV,
            'us': us,
            'ns': ns,
            'GHz': GHz,
            'MHz': MHz,
            's': s,
            'A': A
            
        }

        self.InstrumentDict = {
            'Name': 'Default',
            'InstrumentType': 'COut',
            'DefString': None,
            'CustomFn': ReadCustomInstrumentSetting,
            'ControlOutput': None,
            'Minimum': None,
            'Maximum': None
        }
        self.lineEdit = {
            'Name': self.lineEdit_Name,
            'DefString': self.lineEdit_Defstring,
            'Minimum': self.lineEdit_Min,
            'Maximum': self.lineEdit_Max,
        }
        ##Input 
        self.DetermineEnableConditions()

        self.lineEdit_Name.editingFinished.connect(lambda: UpdateLineEdit_String(self.InstrumentDict,'Name',self.lineEdit))
        self.lineEdit_Defstring.editingFinished.connect(lambda: UpdateLineEdit_String(self.InstrumentDict,'DefString',self.lineEdit))
        
        self.lineEdit_Min.editingFinished.connect(lambda: UpdateLineEdit_Bound(self.InstrumentDict,'Minimum',self.lineEdit))
        self.lineEdit_Max.editingFinished.connect(lambda: UpdateLineEdit_Bound(self.InstrumentDict,'Maximum',self.lineEdit))

        self.pushButton_Done.clicked.connect(lambda: self.done())
        self.pushButton_Cancel.clicked.connect(lambda: self.closeWindow())


    def Refreshinterface(self):
        self.DetermineEnableConditions()
        RefreshButtonStatus(self.ButtonsCondition)
        for key, dlist in self.DeviceList.items():
            RefreshIndicator(dlist['ServerIndicator'],dlist['ServerObject'])
            RefreshIndicator(dlist['DeviceIndicator'],dlist['DeviceObject'])

    def DetermineEnableConditions(self):
        self.ButtonsCondition = {
        }

    def done(self):
        self.complete.emit()
        self.close()

    def closeWindow(self):
        self.close()

    def initialize(self,input_dictionary):
        self.lineEdit_Name.setText(input_dictionary['Name'])
        self.lineEdit_Defstring.setText(input_dictionary['DefString'])

    def clearInfo(self):
        self.InstrumentDict = {
            'Name': 'Default',
            'InstrumentType': 'COut',
            'DefString': None,
            'CustomFn': ReadCustomOutputSetting,
        }

        self.lineEdit_Name.setText('')
        self.lineEdit_Defstring.setText('')

    def moveDefault(self):
        self.move(400,100)

def ReadCustomOutputSetting(instrumentDict,variable_list,value_list):
    custom_variable = instrumentDict['DefString']
    operator_list = ['^','*','/','+','-','(',')','ARCTAN']
    unit_list = ['mV','uV','nV','pV','mA','uA','nA','pA']
    return loopCustom(variable_list,operator_list,unit_list, value_list,custom_variable)


def WriteCustomOutputInstrumentSetting(instrumentDict,variable_list,value_list):
    custom_variable = instrumentDict['DefString']
    operator_list = ['^','*','/','+','-','(',')','ARCTAN']
    unit_list = ['mV','uV','nV','pV','mA','uA','nA','pA']
    return loopCustom(variable_list,operator_list,unit_list, value_list,custom_variable)