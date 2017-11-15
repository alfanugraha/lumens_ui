#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from qgis.core import *
from PyQt4 import QtCore, QtGui
from processing.tools import *

from dialog_lumens_base import DialogLumensBase
from dialog_lumens_viewer import DialogLumensViewer


class DialogLumensDeleteData(QtGui.QDialog, DialogLumensBase):
    """LUMENS "Delete Data" dialog class. 
    """
  
    def __init__(self, parent):
        super(DialogLumensDeleteData, self).__init__(parent)

        self.main = parent
        self.dialogTitle = 'LUMENS Delete Data'

        if self.main.appSettings['debug']:
            print 'DEBUG: DialogLumensDeleteData init'
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

        self.loadDataFromLookupTable()

        self.buttonProcessDeleteData.clicked.connect(self.handlerProcessDelete)


    def setupUi(self, parent):
        """Method for building the dialog UI.
        
        Args:
            parent: the dialog's parent instance.
        """
        self.dialogLayout = QtGui.QVBoxLayout()

        self.groupBoxDeleteData = QtGui.QGroupBox('Delete Data')
        self.layoutGroupBoxDeleteData = QtGui.QVBoxLayout()
        self.layoutGroupBoxDeleteData.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxDeleteData.setLayout(self.layoutGroupBoxDeleteData)
        self.layoutDeleteDataInfo = QtGui.QVBoxLayout()
        self.layoutDeleteData = QtGui.QVBoxLayout()
        self.layoutGroupBoxDeleteData.addLayout(self.layoutDeleteDataInfo)
        self.layoutGroupBoxDeleteData.addLayout(self.layoutDeleteData)

        self.labelDeleteDataInfo = QtGui.QLabel()
        self.labelDeleteDataInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutDeleteDataInfo.addWidget(self.labelDeleteDataInfo)

        self.dataTable = QtGui.QTableWidget()
        self.dataTable.setDisabled(True)
        self.dataTable.verticalHeader().setVisible(False)
        self.layoutDeleteData.addWidget(self.dataTable)

        self.layoutButtonProcessDeleteData = QtGui.QHBoxLayout()
        self.buttonProcessDeleteData = QtGui.QPushButton()
        self.buttonProcessDeleteData.setText('&Process')
        self.layoutButtonProcessDeleteData.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonProcessDeleteData.addWidget(self.buttonProcessDeleteData)

        self.dialogLayout.addWidget(self.groupBoxDeleteData)
        self.dialogLayout.addLayout(self.layoutButtonProcessDeleteData)

        self.setLayout(self.dialogLayout)
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(640, 480)
        self.resize(parent.sizeHint())


    def loadDataFromLookupTable(self):
        """Load all data in one big table viewer.
        """
        self.dataTable.setRowCount(0)
        self.dataTable.setColumnCount(0)
        
        fields = ['Data', 'Description', 'Action']
        self.checkBoxDeleteDataCount = 0
        self.dataTable.setColumnCount(len(fields))
        self.dataTable.setHorizontalHeaderLabels(fields)

        tableRow = 0

        if(len(self.main.dataLandUseCover)):
            dataLandUseCover = self.main.dataLandUseCover
            for value in dataLandUseCover.values():
                self.dataTable.insertRow(tableRow)

                data = QtGui.QTableWidgetItem(value['RST_DATA'])
                data.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.dataTable.setItem(tableRow, 0, data)
                self.dataTable.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)

                description = QtGui.QTableWidgetItem(value['RST_NAME'])
                description.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.dataTable.setItem(tableRow, 1, description)
                self.dataTable.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.ResizeToContents)

                # Additional checkbox column for marking the deleted data
                fieldDelete = QtGui.QTableWidgetItem('Delete')
                fieldDelete.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                fieldDelete.setCheckState(QtCore.Qt.Unchecked)
                self.dataTable.setItem(tableRow, 2, fieldDelete)
                self.dataTable.horizontalHeader().setResizeMode(2, QtGui.QHeaderView.ResizeToContents)

                tableRow += 1


        if(len(self.main.dataPlanningUnit)):
            dataPlanningUnit = self.main.dataPlanningUnit
            for value in dataPlanningUnit.values():
                self.dataTable.insertRow(tableRow)

                data = QtGui.QTableWidgetItem(value['RST_DATA'])
                data.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.dataTable.setItem(tableRow, 0, data)
                self.dataTable.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)

                description = QtGui.QTableWidgetItem(value['RST_NAME'])
                description.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.dataTable.setItem(tableRow, 1, description)
                self.dataTable.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.ResizeToContents)

                # Additional checkbox column for marking the deleted data
                fieldDelete = QtGui.QTableWidgetItem('Delete')
                fieldDelete.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                fieldDelete.setCheckState(QtCore.Qt.Unchecked)
                self.dataTable.setItem(tableRow, 2, fieldDelete)
                self.dataTable.horizontalHeader().setResizeMode(2, QtGui.QHeaderView.ResizeToContents)

                tableRow += 1

        if(len(self.main.dataFactor)):
            dataFactor = self.main.dataFactor
            for value in dataFactor.values():
                self.dataTable.insertRow(tableRow)

                data = QtGui.QTableWidgetItem(value['RST_DATA'])
                data.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.dataTable.setItem(tableRow, 0, data)
                self.dataTable.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)

                description = QtGui.QTableWidgetItem(value['RST_NAME'])
                description.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.dataTable.setItem(tableRow, 1, description)
                self.dataTable.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.ResizeToContents)

                # Additional checkbox column for marking the deleted data
                fieldDelete = QtGui.QTableWidgetItem('Delete')
                fieldDelete.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                fieldDelete.setCheckState(QtCore.Qt.Unchecked)
                self.dataTable.setItem(tableRow, 2, fieldDelete)
                self.dataTable.horizontalHeader().setResizeMode(2, QtGui.QHeaderView.ResizeToContents)

                tableRow += 1

        if(len(self.main.dataTable)):
            dataLookupTable = self.main.dataTable
            for value in dataLookupTable.values():
                self.dataTable.insertRow(tableRow)

                data = QtGui.QTableWidgetItem(value['TBL_DATA'])
                data.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.dataTable.setItem(tableRow, 0, data)
                self.dataTable.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)

                description = QtGui.QTableWidgetItem(value['TBL_NAME'])
                description.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.dataTable.setItem(tableRow, 1, description)
                self.dataTable.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.ResizeToContents)

                # Additional checkbox column for marking the deleted data
                fieldDelete = QtGui.QTableWidgetItem('Delete')
                fieldDelete.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                fieldDelete.setCheckState(QtCore.Qt.Unchecked)
                self.dataTable.setItem(tableRow, 2, fieldDelete)
                self.dataTable.horizontalHeader().setResizeMode(2, QtGui.QHeaderView.ResizeToContents)

                tableRow += 1

        self.dataTable.setEnabled(True)


    def handlerProcessDelete(self):
        """Slot method to handle delete data.
        
        Data are collected from temporary user folder, which are from all csv:
        csv_land_use_cover, csv_planning_unit, csv_factor_data, csv_lookup_table
        
        The "Delete Data" process calls the following algorithm:
        1. dbdelete
        """
        algName = 'r:dbdelete'
        
        checkedDelete = []
        for i in range(self.dataTable.rowCount()):
            if self.dataTable.item(i, 2).checkState() == QtCore.Qt.Checked:
                checkedDelete.append(self.dataTable.item(i, 0).text())

        if len(checkedDelete) > 0:
            activeProject = self.main.appSettings['DialogLumensOpenDatabase']['projectFile'].replace(os.path.sep, '/')

            checkedDelete.sort()
            checkedDeleteCsv = self.writeListCsv(checkedDelete, True)
            
            logging.getLogger(type(self).__name__).info('start: LUMENS Delete Data')

            self.main.setWindowState(QtCore.Qt.WindowMinimized)

            print 'DEBUG'
            print checkedDeleteCsv

            outputs = general.runalg(
                algName,
                activeProject,
                checkedDeleteCsv,
                None
            )

            # Display ROut file in debug mode
            if self.main.appSettings['debug']:
                dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                dialog.exec_()
                
            self.main.setWindowState(QtCore.Qt.WindowActive)

            algSuccess = self.outputsMessageBox(algName, outputs, '', '')
            
            if algSuccess:
                self.main.loadAddedDataInfo()
                self.loadDataFromLookupTable()
                self.close()

            logging.getLogger(type(self).__name__).info('end: LUMENS Delete Data')
        else:
            QtGui.QMessageBox.information(self, self.dialogTitle, 'Choose data to be deleted.')
            return
