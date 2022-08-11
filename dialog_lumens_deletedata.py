#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from qgis.core import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


from tools import general

from dialog_lumens_base import DialogLumensBase
from dialog_lumens_viewer import DialogLumensViewer

from menu_factory import MenuFactory

class DialogLumensDeleteData(QDialog): # DialogLumensBase
    """LUMENS "Delete Data" dialog class. 
    """
  
    def __init__(self, parent):
        super(DialogLumensDeleteData, self).__init__(parent)

        self.main = parent
        self.dialogTitle = MenuFactory.getLabel(MenuFactory.APP_PROJECT_DELETE_DATA)

        if self.main.appSettings['debug']:
            print ('DEBUG: DialogLumensDeleteData init')
            self.logger = logging.getLogger(type(self).__name__)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            fh = logging.FileHandler(os.path.join(self.main.appSettings['appDir'], 'logs', type(self).__name__ + '.log'))
            fh.setFormatter(formatter)
            self.logger.addHandler(ch)
            self.logger.addHandler(fh)
            self.logger.setLevel(logging.DEBUG)

        self.base = DialogLumensBase(parent)

        self.setupUi(self)

        self.loadDataFromLookupTable()

        self.buttonProcessDeleteData.clicked.connect(self.handlerProcessDelete)


    def setupUi(self, parent):
        """Method for building the dialog UI.
        
        Args:
            parent: the dialog's parent instance.
        """
        self.dialogLayout = QVBoxLayout()

        self.groupBoxDeleteData = QGroupBox(MenuFactory.getLabel(MenuFactory.APP_PROJECT_DELETE_DATA))
        self.layoutGroupBoxDeleteData = QVBoxLayout()
        self.layoutGroupBoxDeleteData.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.groupBoxDeleteData.setLayout(self.layoutGroupBoxDeleteData)
        self.layoutDeleteDataInfo = QVBoxLayout()
        self.layoutDeleteData = QVBoxLayout()
        self.layoutGroupBoxDeleteData.addLayout(self.layoutDeleteDataInfo)
        self.layoutGroupBoxDeleteData.addLayout(self.layoutDeleteData)

        self.labelDeleteDataInfo = QLabel()
        self.labelDeleteDataInfo.setText('\n')
        self.labelDeleteDataInfo.setWordWrap(True)
        self.layoutDeleteDataInfo.addWidget(self.labelDeleteDataInfo)

        self.dataTable = QTableWidget()
        self.dataTable.setDisabled(True)
        self.dataTable.verticalHeader().setVisible(False)
        self.layoutDeleteData.addWidget(self.dataTable)

        self.layoutButtonProcessDeleteData = QHBoxLayout()
        self.buttonProcessDeleteData = QPushButton()
        self.buttonProcessDeleteData.setText('&' + MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_PROSES))
        self.layoutButtonProcessDeleteData.setAlignment(Qt.AlignRight)
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

                data = QTableWidgetItem(value['RST_DATA'])
                data.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.dataTable.setItem(tableRow, 0, data)
                self.dataTable.horizontalHeader().setResizeMode(0, QHeaderView.ResizeToContents)

                description = QTableWidgetItem(value['RST_NAME'])
                description.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.dataTable.setItem(tableRow, 1, description)
                self.dataTable.horizontalHeader().setResizeMode(1, QHeaderView.ResizeToContents)

                # Additional checkbox column for marking the deleted data
                fieldDelete = QTableWidgetItem(MenuFactory.getLabel(MenuFactory.APP_DELETE_DATA_DELETE_ACTION))
                fieldDelete.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                fieldDelete.setCheckState(Qt.Unchecked)
                self.dataTable.setItem(tableRow, 2, fieldDelete)
                self.dataTable.horizontalHeader().setResizeMode(2, QHeaderView.ResizeToContents)

                tableRow += 1


        if(len(self.main.dataPlanningUnit)):
            dataPlanningUnit = self.main.dataPlanningUnit
            for value in dataPlanningUnit.values():
                self.dataTable.insertRow(tableRow)

                data = QTableWidgetItem(value['RST_DATA'])
                data.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.dataTable.setItem(tableRow, 0, data)
                self.dataTable.horizontalHeader().setResizeMode(0, QHeaderView.ResizeToContents)

                description = QTableWidgetItem(value['RST_NAME'])
                description.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.dataTable.setItem(tableRow, 1, description)
                self.dataTable.horizontalHeader().setResizeMode(1, QHeaderView.ResizeToContents)

                # Additional checkbox column for marking the deleted data
                fieldDelete = QTableWidgetItem(MenuFactory.getLabel(MenuFactory.APP_DELETE_DATA_DELETE_ACTION))
                fieldDelete.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                fieldDelete.setCheckState(Qt.Unchecked)
                self.dataTable.setItem(tableRow, 2, fieldDelete)
                self.dataTable.horizontalHeader().setResizeMode(2, QHeaderView.ResizeToContents)

                tableRow += 1

        if(len(self.main.dataFactor)):
            dataFactor = self.main.dataFactor
            for value in dataFactor.values():
                self.dataTable.insertRow(tableRow)

                data = QTableWidgetItem(value['RST_DATA'])
                data.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.dataTable.setItem(tableRow, 0, data)
                self.dataTable.horizontalHeader().setResizeMode(0, QHeaderView.ResizeToContents)

                description = QTableWidgetItem(value['RST_NAME'])
                description.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.dataTable.setItem(tableRow, 1, description)
                self.dataTable.horizontalHeader().setResizeMode(1, QHeaderView.ResizeToContents)

                # Additional checkbox column for marking the deleted data
                fieldDelete = QTableWidgetItem(MenuFactory.getLabel(MenuFactory.APP_DELETE_DATA_DELETE_ACTION))
                fieldDelete.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                fieldDelete.setCheckState(Qt.Unchecked)
                self.dataTable.setItem(tableRow, 2, fieldDelete)
                self.dataTable.horizontalHeader().setResizeMode(2, QHeaderView.ResizeToContents)

                tableRow += 1

        if(len(self.main.dataTable)):
            dataLookupTable = self.main.dataTable
            for value in dataLookupTable.values():
                self.dataTable.insertRow(tableRow)

                data = QTableWidgetItem(value['TBL_DATA'])
                data.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.dataTable.setItem(tableRow, 0, data)
                self.dataTable.horizontalHeader().setResizeMode(0, QHeaderView.ResizeToContents)

                description = QTableWidgetItem(value['TBL_NAME'])
                description.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.dataTable.setItem(tableRow, 1, description)
                self.dataTable.horizontalHeader().setResizeMode(1, QHeaderView.ResizeToContents)

                # Additional checkbox column for marking the deleted data
                fieldDelete = QTableWidgetItem(MenuFactory.getLabel(MenuFactory.APP_DELETE_DATA_DELETE_ACTION))
                fieldDelete.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                fieldDelete.setCheckState(Qt.Unchecked)
                self.dataTable.setItem(tableRow, 2, fieldDelete)
                self.dataTable.horizontalHeader().setResizeMode(2, QHeaderView.ResizeToContents)

                tableRow += 1

        self.dataTable.setEnabled(True)


    def handlerProcessDelete(self):
        """Slot method to handle delete data.
        
        Data are collected from temporary user folder, which are from all csv:
        csv_land_use_cover, csv_planning_unit, csv_factor_data, csv_lookup_table
        
        The "Delete Data" process calls the following algorithm:
        1. dbdelete
        """
        algName = 'r:db_delete'
        
        checkedDelete = []
        for i in range(self.dataTable.rowCount()):
            if self.dataTable.item(i, 2).checkState() == Qt.Checked:
                checkedDelete.append(self.dataTable.item(i, 0).text())

        if len(checkedDelete) > 0:
            activeProject = self.main.appSettings['DialogLumensOpenDatabase']['projectFile'].replace(os.path.sep, '/')

            checkedDelete.sort()
            checkedDeleteCsv = self.writeListCsv(checkedDelete, True)
            
            logging.getLogger(type(self).__name__).info('start: LUMENS Delete Data')

            self.main.setWindowState(Qt.WindowMinimized)

            print ('DEBUG')
            print (checkedDeleteCsv)

            outputs = general.run(
                algName, {
                    'proj.file': activeProject,
                    'csv_delete_data': checkedDeleteCsv,
                    'statusoutput': 'TEMPORARY_OUTPUT'
                }
            )

            # Display ROut file in debug mode
            if self.main.appSettings['debug']:
                dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                dialog.exec_()
                
            self.main.setWindowState(Qt.WindowActive)

            algSuccess = self.base.outputsMessageBox(algName, outputs, '', '')
            
            if algSuccess:
                self.main.loadAddedDataInfo()
                self.loadDataFromLookupTable()
                self.close()

            logging.getLogger(type(self).__name__).info('end: LUMENS Delete Data')
        else:
            QMessageBox.information(self.main, self.dialogTitle, MenuFactory.getLabel(MenuFactory.MSG_DB_CHOOSE_DATA_TO_BE_DELETED))
            return
