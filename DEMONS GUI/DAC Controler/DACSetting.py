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
Ui_DACSetting, QtBaseClass = uic.loadUiType(os.path.join(path , "DACSettingWindow.ui"))

class DACSetting(QtGui.QMainWindow, Ui_DACSetting):
    complete = QtCore.pyqtSignal()

    def __init__(self, reactor, parent = None):
        super(DACSetting, self).__init__(parent)
        from labrad.units import V, mV, us, ns, GHz, MHz, Hz, K, deg, s

        self.reactor = reactor
        self.parent = parent

        self.setupUi(self)

        self.Servers = None
        self.Devices = None

        self.lineEdit = {
            'DAC0Min': self.lineEdit_DAC0Min,
            'DAC0Max': self.lineEdit_DAC0Max,

            'DAC1Min': self.lineEdit_DAC1Min,
            'DAC1Max': self.lineEdit_DAC1Max,

        }

        self.targetnumber = {
            'DAC0Min': -10.0,
            'DAC0Max': 10.0,

            'DAC1Min': -10.0,
            'DAC1Max': 10.0,
        }

        #self.parameters()
        ##Input 
        #self.DetermineEnableConditions()

        

        self.lineEdit_DAC0Min.editingFinished.connect(lambda: UpdateLineEdit_Bound(self.targetnumber,'DAC0Min',self.lineEdit))
        self.lineEdit_DAC0Max.editingFinished.connect(lambda: UpdateLineEdit_Bound(self.targetnumber,'DAC0Max',self.lineEdit))
        self.lineEdit_DAC1Min.editingFinished.connect(lambda: UpdateLineEdit_Bound(self.targetnumber,'DAC1Min',self.lineEdit))
        self.lineEdit_DAC1Max.editingFinished.connect(lambda: UpdateLineEdit_Bound(self.targetnumber,'DAC1Max',self.lineEdit))


        self.pushButton_Done.clicked.connect(lambda: self.done())
        self.pushButton_Cancel.clicked.connect(lambda: self.closeWindow())


    def done(self):
        self.complete.emit()
        print('New DAC Bounds: '+str(self.targetnumber))
        self.close()

    def closeWindow(self):
        self.close()

    def initialize(self,input_dict):
        for key in input_dict:
            self.lineEdit[key].setText(str(input_dict[key]))
            self.targetnumber[key] = input_dict[key]

        # self.lineEdit_Name.setText(input_dictionary['Name'])
        # self.comboBox_Measurement.setCurrentText(input_dictionary['Measurement'])
        # if input_dictionary['Measurement'] == 'Input':
        #     self.comboBox_ADCInput.setCurrentText(input_dictionary['ADC Input'])
        # elif input_dictionary['Measurement'] == 'Output':
        #     self.comboBox_DACOutput.setCurrentText(input_dictionary['DAC Output'])
        # self.comboBox_DACADC_SelectDevice.setCurrentText(input_dictionary['Device'])

    def moveDefault(self):
        self.move(400,100)
