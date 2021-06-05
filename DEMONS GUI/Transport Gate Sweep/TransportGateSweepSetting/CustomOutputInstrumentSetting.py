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
        self.Buslist = []


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
            'DefInvString': None,
            'WriteFn': WriteCustomOutputSetting,
        	'CustomRead': ReadCustomOutputSetting,
            'ControlOutput': None,
            'Minimum': None,
            'Maximum': None
        }
        self.lineEdit = {
            'Name': self.lineEdit_Name,
            'DefString': self.lineEdit_Defstring,
            'DefInvString': self.lineEdit_DefInvstring,
            'Minimum': self.lineEdit_Min,
            'Maximum': self.lineEdit_Max,
        }
        ##Input 
        self.DetermineEnableConditions()

        self.lineEdit_Name.editingFinished.connect(lambda: UpdateLineEdit_String(self.InstrumentDict,'Name',self.lineEdit))
        self.lineEdit_Defstring.editingFinished.connect(lambda: UpdateLineEdit_String(self.InstrumentDict,'DefString',self.lineEdit))
        
        self.lineEdit_DefInvstring.editingFinished.connect(lambda: UpdateLineEdit_String(self.InstrumentDict,'DefInvString',self.lineEdit))

        self.lineEdit_Min.editingFinished.connect(lambda: UpdateLineEdit_Bound(self.InstrumentDict,'Minimum',self.lineEdit))
        self.lineEdit_Max.editingFinished.connect(lambda: UpdateLineEdit_Bound(self.InstrumentDict,'Maximum',self.lineEdit))

        self.pushButton_Done.clicked.connect(lambda: self.done())
        self.pushButton_Cancel.clicked.connect(lambda: self.closeWindow())

        self.comboBox_Output.currentIndexChanged.connect(lambda: SetComboBox_Parameter(self.InstrumentDict, 'ControlOutput',self.comboBox_Output.currentText()))

    def Refreshinterface(self):
        self.DetermineEnableConditions()
        RefreshButtonStatus(self.ButtonsCondition)
        for key, dlist in self.DeviceList.items():
            RefreshIndicator(dlist['ServerIndicator'],dlist['ServerObject'])
            RefreshIndicator(dlist['DeviceIndicator'],dlist['DeviceObject'])
        ReconstructComboBox(self.comboBox_Output,self.Buslist)

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
        self.lineEdit_DefInvstring.setText(input_dictionary['DefInvString'])
        ReconstructComboBox(self.comboBox_Output,self.Buslist)
        self.comboBox_Output.setCurrentText(input_dictionary['ControlOutput'])
        self.lineEdit_Min.setText(input_dictionary['Minimum'])
        self.lineEdit_Max.setText(input_dictionary['Maximum'])
    def clearInfo(self):
        self.InstrumentDict = {
            'Name': 'Default',
            'InstrumentType': 'COut',
            'DefString': None,
            'DefInvString': None,
            'CustomRead': ReadCustomOutputSetting,
            'WriteFn': WriteCustomOutputSetting,
            'ControlOutput': None,
            'Minimum': None,
            'Maximum': None

        }

        self.lineEdit_Name.setText('')
        self.lineEdit_Defstring.setText('')
        self.lineEdit_DefInvstring.setText('')
        self.lineEdit_Max.setText('')
        self.lineEdit_Min.setText('')

        ReconstructComboBox(self.comboBox_Output,self.Buslist)

    def moveDefault(self):
        self.move(400,100)

def ReadCustomOutputSetting(instrumentDict,variable_list,value_list):
    custom_variable = instrumentDict['DefString']
    operator_list = ['^','*','/','+','-','(',')','ARCTAN']
    unit_list = ['mV','uV','nV','pV','mA','uA','nA','pA']
    return loopCustom(variable_list,operator_list,unit_list, value_list,custom_variable)

@inlineCallbacks
def WriteCustomOutputSetting(instrumentDict,value,instrumentBus,queryfunction,variables):
    custom_variable = instrumentDict['DefInvString']
    operator_list = ['^','*','/','+','-','(',')','ARCTAN']
    unit_list = ['mV','uV','nV','pV','mA','uA','nA','pA']

    # could adjust this to some simpler query that only pings the output variables
    indep_vals, dep_vals, custom_vals = yield queryfunction()
    values = list(indep_vals + dep_vals + custom_vals)
    cvar_location = variables.index(instrumentDict['Name'])
    values[cvar_location] = value
    
    g = loopCustom(variables,operator_list,unit_list, [values],custom_variable)
    desired_instr = instrumentDict['ControlOutput']
    yield instrumentBus[desired_instr]['WriteFn'](instrumentBus[desired_instr],g[0])
    returnValue(1)