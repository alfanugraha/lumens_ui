#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, csv, tempfile, datetime
from qgis.core import *
from PyQt4 import QtCore, QtGui
from processing.tools import *

from dialog_lumens_base import DialogLumensBase


class DialogTableEditor(QtGui.QDialog, DialogLumensBase):
    """LUMENS dialog class for edit table viewer.
    """
    
    def __init__(self, parent):
        super(DialogTableEditor, self).__init__(parent)
        
        self.main = parent
        self.dialogTitle = 'LUMENS Table Viewer'
        
        if self.main.appSettings['debug']:
            print 'DEBUG: DialogTableEditor init'
            self.logger = logging.getLogger(type(self).__name__)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            fh = logging.FileHandler(os.path.join(self.main.appSettings['appDir'], 'logs', type(self).__name__ + '.log'))
            fh.setFormatter(formatter)
            self.logger.addHandler(ch)
            self.logger.addHandler(fh)
            self.logger.setLevel(logging.DEBUG)
        
        self.setupUi(self)
        
        self.buttonProcessTableEditor.clicked.connect(self.handlerProcessTableEditor)
        
    
    def setupUi(self, parent):
        """Method for building the dialog UI.
        
        Args:
            parent: the dialog's parent instance.
        """
        self.dialogLayout = QtGui.QVBoxLayout()

        self.groupBoxTableEditor = QtGui.QGroupBox('Table Editor')
        self.layoutGroupBoxTableEditor = QtGui.QVBoxLayout()
        self.layoutGroupBoxTableEditor.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxTableEditor.setLayout(self.layoutGroupBoxTableEditor)
        self.layoutTableEditorInfo = QtGui.QVBoxLayout()
        self.layoutTableEditor = QtGui.QVBoxLayout()
        self.layoutGroupBoxTableEditor.addLayout(self.layoutTableEditorInfo)
        self.layoutGroupBoxTableEditor.addLayout(self.layoutTableEditor)

        self.labelTableEditorInfo = QtGui.QLabel()
        self.labelTableEditorInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.labelTableEditorInfo.setWordWrap(True)
        self.layoutTableEditorInfo.addWidget(self.labelTableEditorInfo)

        self.labelLookupTable = QtGui.QLabel()
        self.labelLookupTable.setText('Lookup Table:')
        self.layoutTableEditor.addWidget(self.labelLookupTable)
        self.comboBoxDataTable = QtGui.QComboBox()
        self.comboBoxDataTable.setDisabled(True)
        self.layoutTableEditor.addWidget(self.comboBoxDataTable)
        self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxDataTable)
        self.buttonLoadLookupTable = QtGui.QPushButton()
        self.buttonLoadLookupTable.setText('Load Table')
        self.layoutTableEditor.addWidget(self.buttonLoadLookupTable)
        
        self.dataLookupTable = QtGui.QTableWidget()
        self.dataLookupTable.setDisabled(True)
        self.dataLookupTable.verticalHeader().setVisible(False)
        self.layoutTableEditor.addWidget(self.dataLookupTable)

        self.layoutButtonProcessTableEditor = QtGui.QHBoxLayout()
        self.buttonProcessTableEditor = QtGui.QPushButton()
        self.buttonProcessTableEditor.setText('&Process')
        self.layoutButtonProcessTableEditor.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonProcessTableEditor.addWidget(self.buttonProcessTableEditor)

        self.dialogLayout.addWidget(self.groupBoxTableEditor)
        self.dialogLayout.addLayout(self.layoutButtonProcessTableEditor)

        self.setLayout(self.dialogLayout)
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(640, 480)
        self.resize(parent.sizeHint())
    
    
    def loadDataFromLookupTable(self):
        """Load all data in one big table viewer.
        """
        self.dataLookupTable.setRowCount(0)
        self.dataLookupTable.setColumnCount(0)
        
        fields = ['Data', 'Description', 'Action']
        self.checkBoxDeleteDataCount = 0
        self.dataLookupTable.setColumnCount(len(fields))
        self.dataLookupTable.setHorizontalHeaderLabels(fields)

        tableRow = 0

        if(len(self.main.dataTable)):
            dataLookupTable = self.main.dataTable
            for value in dataLookupTable.values():
                self.dataLookupTable.insertRow(tableRow)

                data = QtGui.QTableWidgetItem(value['TBL_DATA'])
                data.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.dataLookupTable.setItem(tableRow, 0, data)
                self.dataLookupTable.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)

                description = QtGui.QTableWidgetItem(value['TBL_NAME'])
                description.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.dataLookupTable.setItem(tableRow, 1, description)
                self.dataLookupTable.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.ResizeToContents)

                # Additional checkbox column for marking the deleted data
                fieldDelete = QtGui.QTableWidgetItem('Delete')
                fieldDelete.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                fieldDelete.setCheckState(QtCore.Qt.Unchecked)
                self.dataLookupTable.setItem(tableRow, 2, fieldDelete)
                self.dataLookupTable.horizontalHeader().setResizeMode(2, QtGui.QHeaderView.ResizeToContents)

                tableRow += 1

        self.dataLookupTable.setEnabled(True)
        
    
    def handlerProcessTableEditor(self):
        """Slot method for process table viewer.
        """
        algName = 'r:toolstableeditor'
    
    
