#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, csv, tempfile, datetime
from qgis.core import *
from PyQt4 import QtCore, QtGui
from processing.tools import *

from dialog_lumens_base import DialogLumensBase

from menu_factory import MenuFactory

class DialogTableEditor(QtGui.QDialog, DialogLumensBase):
    """LUMENS dialog class for edit table viewer.
    """
    
    def __init__(self, parent):
        super(DialogTableEditor, self).__init__(parent)
        
        self.main = parent
        self.dialogTitle = MenuFactory.getLabel(MenuFactory.APP_TABLE_EDITOR)
        
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
        
        self.buttonLoadLookupTable.clicked.connect(self.handlerLoadLookupTable)
        self.buttonProcessTableEditor.clicked.connect(self.handlerSaveTableEditor)
        
    
    def setupUi(self, parent):
        """Method for building the dialog UI.
        
        Args:
            parent: the dialog's parent instance.
        """
        self.dialogLayout = QtGui.QVBoxLayout()

        self.groupBoxTableEditor = QtGui.QGroupBox(MenuFactory.getLabel(MenuFactory.APP_TABLE_EDITOR))
        self.layoutGroupBoxTableEditor = QtGui.QVBoxLayout()
        # self.layoutGroupBoxTableEditor.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxTableEditor.setLayout(self.layoutGroupBoxTableEditor)
        self.layoutTableEditorInfo = QtGui.QVBoxLayout()
        self.layoutTableEditor = QtGui.QGridLayout()
        self.layoutGroupBoxTableEditor.addLayout(self.layoutTableEditorInfo)
        self.layoutGroupBoxTableEditor.addLayout(self.layoutTableEditor)

        self.labelTableEditorInfo = QtGui.QLabel()
        self.labelTableEditorInfo.setText('\n')
        self.labelTableEditorInfo.setWordWrap(True)
        self.layoutTableEditorInfo.addWidget(self.labelTableEditorInfo)

        self.labelLookupTable = QtGui.QLabel()
        self.labelLookupTable.setText(MenuFactory.getLabel(MenuFactory.APP_TABLE_EDITOR_LOOKUP_TABLE) + ':')
        self.layoutTableEditor.addWidget(self.labelLookupTable, 0, 0)
        self.comboBoxDataTable = QtGui.QComboBox()
        self.comboBoxDataTable.setDisabled(True)
        self.layoutTableEditor.addWidget(self.comboBoxDataTable, 0, 1)
        self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxDataTable)
        self.buttonLoadLookupTable = QtGui.QPushButton()
        self.buttonLoadLookupTable.setText(MenuFactory.getLabel(MenuFactory.APP_TABLE_EDITOR_LOAD))
        self.layoutTableEditor.addWidget(self.buttonLoadLookupTable, 0, 2)
        
        self.dataLookupTable = QtGui.QTableWidget()
        self.dataLookupTable.setDisabled(True)
        self.dataLookupTable.verticalHeader().setVisible(False)
        self.layoutTableEditor.addWidget(self.dataLookupTable, 1, 0, 1, 3)

        self.layoutButtonProcessTableEditor = QtGui.QHBoxLayout()
        self.buttonProcessTableEditor = QtGui.QPushButton()
        self.buttonProcessTableEditor.setText(MenuFactory.getLabel(MenuFactory.APP_TABLE_EDITOR_SAVE))
        self.layoutButtonProcessTableEditor.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonProcessTableEditor.addWidget(self.buttonProcessTableEditor)

        self.dialogLayout.addWidget(self.groupBoxTableEditor)
        self.dialogLayout.addLayout(self.layoutButtonProcessTableEditor)

        self.setLayout(self.dialogLayout)
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(640, 480)
        self.resize(parent.sizeHint())
    
    
    def handlerLoadLookupTable(self):
        """Load all data in one big table viewer.
        """
        activeProject = self.main.appSettings['DialogLumensOpenDatabase']['projectFile'].replace(os.path.sep, '/')
        selectedLookupTable = self.comboBoxDataTable.currentText()
        customTable = 1
        
        outputs = general.runalg(
            'r:toolsgetlut',
            activeProject,
            customTable,
            selectedLookupTable,
            None,
        )        
        
        outputKey = 'main_data'
        if outputs and outputKey in outputs:
            if os.path.exists(outputs[outputKey]):
                with open(outputs[outputKey], 'rb') as f:
                    reader = csv.reader(f)
                    columns = next(reader)
                    
                    self.dataLookupTable.setColumnCount(len(columns))
                    self.dataLookupTable.setHorizontalHeaderLabels(columns)
                    
                    lookupTable = []

                    for row in reader:
                        dataRow = [QtGui.QTableWidgetItem(field) for field in row]
                        lookupTable.append(dataRow)
                        
                    self.dataLookupTable.setRowCount(len(lookupTable))

                    tableRow = 0
                    for dataRow in lookupTable:
                        tableColumn = 0
                        for fieldTableItem in dataRow:
                            # fieldTableItem.setFlags(fieldTableItem.flags() & ~QtCore.Qt.ItemIsEnabled)
                            self.dataLookupTable.setItem(tableRow, tableColumn, fieldTableItem)
                            self.dataLookupTable.horizontalHeader().setResizeMode(tableColumn, QtGui.QHeaderView.ResizeToContents)
                            tableColumn += 1
                            
                        tableRow += 1

                    self.dataLookupTable.setEnabled(True)
        
    
    def handlerSaveTableEditor(self):
        """Slot method for process table viewer.
        """
        algName = 'r:dbaddlut'
        activeProject = self.main.appSettings['DialogLumensOpenDatabase']['projectFile'].replace(os.path.sep, '/')
        tableDescription = self.comboBoxDataTable.currentText() + '_new'
        csvLookupTable = DialogLumensBase.writeTableCsv(self.dataLookupTable, True)
        
        outputs = general.runalg(
            algName,
            activeProject,
            tableDescription,
            csvLookupTable,
            None,
        )
        
        algSuccess = self.outputsMessageBox(algName, outputs, MenuFactory.getLabel(MenuFactory.MSG_DB_SUCCESS_ADDED), MenuFactory.getLabel(MenuFactory.MSG_DB_FAILED_ADDED))
        
        if algSuccess:
            self.main.loadAddedDataInfo()
            self.dataLookupTable.setRowCount(0)
            self.dataLookupTable.setColumnCount(0)
            self.close()
    
    
