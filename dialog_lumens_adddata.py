#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, datetime
from qgis.core import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from tools import general

from dialog_lumens_base import DialogLumensBase
from dialog_lumens_viewer import DialogLumensViewer
from dialog_lumens_adddata_properties import DialogLumensAddDataProperties

from menu_factory import MenuFactory

class DialogLumensAddData(QDialog): 
    """LUMENS "Add Data" dialog class.
    """
    
    def __init__(self, parent):
        super(DialogLumensAddData, self).__init__(parent)
        
        self.main = parent
        self.dialogTitle = MenuFactory.getLabel(MenuFactory.APP_PROJ_ADD_DATA)
        self.tableAddDataRowCount = 0
        self.tableAddData = []
        
        if self.main.appSettings['debug']:
            print ('DEBUG: DialogLumensAddData init')
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
        
        self.buttonAddDataRow.clicked.connect(self.handlerButtonAddDataRow)
        self.buttonProcessAddData.clicked.connect(self.handlerProcessAddData)
    
    
    def setupUi(self, parent):
        """Method for building the dialog UI.
        
        Args:
            parent: the dialog's parent instance.
        """
        #self.setStyleSheet('background-color: rgb(173, 185, 202);')
        self.dialogLayout = QVBoxLayout()
        
        self.groupBoxAddData = QGroupBox(MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_DEFINE_PROPERTIES))
        self.layoutGroupBoxAddData = QVBoxLayout()
        self.layoutGroupBoxAddData.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.groupBoxAddData.setLayout(self.layoutGroupBoxAddData)
        self.layoutAddDataInfo = QVBoxLayout()
        self.layoutAddData = QVBoxLayout()
        self.layoutGroupBoxAddData.addLayout(self.layoutAddDataInfo)
        self.layoutGroupBoxAddData.addLayout(self.layoutAddData)
        
        self.labelAddDataInfo = QLabel()
        self.labelAddDataInfo.setText('\n')
        self.labelAddDataInfo.setWordWrap(True)
        self.layoutAddDataInfo.addWidget(self.labelAddDataInfo)
        
        self.layoutButtonAddData = QHBoxLayout()
        self.layoutButtonAddData.setContentsMargins(0, 0, 0, 0)
        self.layoutButtonAddData.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.buttonAddDataRow = QPushButton()
        self.buttonAddDataRow.setText(MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_ADD_ITEM))
        self.buttonAddDataRow.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.layoutButtonAddData.addWidget(self.buttonAddDataRow)
        
        self.layoutContentAddData = QVBoxLayout()
        self.layoutContentAddData.setContentsMargins(5, 5, 5, 5)
        self.contentAddData = QWidget()
        self.contentAddData.setLayout(self.layoutContentAddData)
        self.scrollAddData = QScrollArea()
        self.scrollAddData.setWidgetResizable(True);
        self.scrollAddData.setWidget(self.contentAddData)
        self.layoutTableAddData = QVBoxLayout()
        self.layoutTableAddData.setAlignment(Qt.AlignTop)
        self.layoutContentAddData.addLayout(self.layoutTableAddData)
        
        self.layoutAddData.addLayout(self.layoutButtonAddData)
        self.layoutAddData.addWidget(self.scrollAddData)
        
        self.layoutButtonProcessAddData = QHBoxLayout()
        self.buttonProcessAddData = QPushButton()
        self.buttonProcessAddData.setText('&' + MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_PROSES))
        self.layoutButtonProcessAddData.setAlignment(Qt.AlignRight)
        self.layoutButtonProcessAddData.addWidget(self.buttonProcessAddData)
        
        self.dialogLayout.addWidget(self.groupBoxAddData)
        self.dialogLayout.addLayout(self.layoutButtonProcessAddData)
        
        self.setLayout(self.dialogLayout)
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(640, 480)
        self.resize(parent.sizeHint())
    
    
    def showEvent(self, event):
        """Overload method that is called when the dialog widget is shown.
        
        Args:
            event (QShowEvent): the show widget event.
        """
        super(DialogLumensAddData, self).showEvent(event)
    
    
    def closeEvent(self, event):
        """Overload method that is called when the dialog widget is closed.
        
        Args:
            event (QCloseEvent): the close widget event.
        """
        super(DialogLumensAddData, self).closeEvent(event)
    
    
    def clearLayout(self, layout):
        """Method for removing a layout and all its child widgets.
        
        Args:
            layout (QLayout): the layout to be removed.
        """
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)

            if isinstance(item, QWidgetItem):
                item.widget().deleteLater() # use this to properly delete the widget
            elif isinstance(item, QSpacerItem):
                pass
            else:
                self.clearLayout(item.layout())

            layout.removeItem(item)


    def clearAllLayout(self):
        """Method for removing all layouts and its child widgets.
        """
        numberOfDataRow = self.tableAddDataRowCount
        for i in range(numberOfDataRow):
            layout = self.layoutTableAddData.itemAt(int(i)).layout()

            for j in reversed(range(layout.count())):
                item = layout.itemAt(j)

                if isinstance(item, QWidgetItem):
                    item.widget().deleteLater()  # use this to properly delete the widget
                elif isinstance(item, QSpacerItem):
                    pass
                else:
                    self.clearLayout(item.layout())

                layout.removeItem(item)


    def addDataRow(self):
        """Method for adding a data row to the input table.
        """
        self.tableAddDataRowCount = self.tableAddDataRowCount + 1
        
        layoutDataRow = QHBoxLayout()
        
        buttonDeleteDataRow = QPushButton()
        icon = QIcon(':/ui/icons/iconActionClear.png')
        buttonDeleteDataRow.setIcon(icon)
        buttonDeleteDataRow.setObjectName('buttonDeleteDataRow_{0}'.format(str(self.tableAddDataRowCount)))
        layoutDataRow.addWidget(buttonDeleteDataRow)
        
        comboBoxDataType = QComboBox()
        comboBoxDataType.addItems([MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_LAND_USE_COVER), MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_PLANNING_UNIT), MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_FACTOR), MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_TABLE)])
        comboBoxDataType.setObjectName('comboBoxDataType_{0}'.format(str(self.tableAddDataRowCount)))
        layoutDataRow.addWidget(comboBoxDataType)
        
        lineEditDataFile = QLineEdit()
        lineEditDataFile.setReadOnly(True)
        lineEditDataFile.setObjectName('lineEditDataFile_{0}'.format(str(self.tableAddDataRowCount)))
        layoutDataRow.addWidget(lineEditDataFile)
        
        buttonSelectDataFile = QPushButton()
        buttonSelectDataFile.setText(MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_SELECT_FILE))
        buttonSelectDataFile.setObjectName('buttonSelectDataFile_{0}'.format(str(self.tableAddDataRowCount)))
        layoutDataRow.addWidget(buttonSelectDataFile)

        buttonDataProperties = QPushButton()
        buttonDataProperties.setDisabled(True)
        buttonDataProperties.setText(MenuFactory.getLabel(MenuFactory.APP_PROPERTIES))
        buttonDataProperties.setObjectName('buttonDataProperties_{0}'.format(str(self.tableAddDataRowCount)))
        layoutDataRow.addWidget(buttonDataProperties)
        
        # Hidden fields set from the data properties dialog
        lineEditDataDescription = QLineEdit()
        lineEditDataDescription.setObjectName('lineEditDataDescription_{0}'.format(str(self.tableAddDataRowCount)))
        lineEditDataDescription.setVisible(False)
        layoutDataRow.addWidget(lineEditDataDescription)
        
        spinBoxDataPeriod = QSpinBox()
        spinBoxDataPeriod.setRange(1, 9999)
        spinBoxDataPeriod.setObjectName('spinBoxDataPeriod_{0}'.format(str(self.tableAddDataRowCount)))
        spinBoxDataPeriod.setVisible(False)
        layoutDataRow.addWidget(spinBoxDataPeriod)
        
        lineEditDataFieldAttribute = QLineEdit()
        lineEditDataFieldAttribute.setObjectName('lineEditDataFieldAttribute_{0}'.format(str(self.tableAddDataRowCount)))
        lineEditDataFieldAttribute.setVisible(False)
        layoutDataRow.addWidget(lineEditDataFieldAttribute)
        
        lineEditDataDissolvedShapefile = QLineEdit()
        lineEditDataDissolvedShapefile.setObjectName('lineEditDataDissolvedShapefile_{0}'.format(str(self.tableAddDataRowCount)))
        lineEditDataDissolvedShapefile.setVisible(False)
        layoutDataRow.addWidget(lineEditDataDissolvedShapefile)
        
        lineEditDataTableCsv = QLineEdit()
        lineEditDataTableCsv.setObjectName('lineEditDataTableCsv_{0}'.format(str(self.tableAddDataRowCount)))
        lineEditDataTableCsv.setVisible(False)
        layoutDataRow.addWidget(lineEditDataTableCsv)
        
        self.layoutTableAddData.addLayout(layoutDataRow)
        
        buttonSelectDataFile.clicked.connect(self.handlerSelectDataFile)
        buttonDataProperties.clicked.connect(self.handlerDataProperties)
        buttonDeleteDataRow.clicked.connect(self.handlerDeleteDataRow)
    
    
    #***********************************************************
    # 'Add Data' QPushButton handlers
    #***********************************************************
    def handlerButtonAddDataRow(self):
        """Slot method for adding a data row.
        """
        self.addDataRow()
    
    
    def handlerSelectDataFile(self):
        """Slot method for a file select dialog to select a spatial file.
        """
        buttonSender = self.sender()
        objectName = buttonSender.objectName()
        tableRow = objectName.split('_')[1]
        
        comboBoxDataType = self.contentAddData.findChild(QComboBox, 'comboBoxDataType_' + tableRow)
        dataType = unicode(comboBoxDataType.currentText())
        
        # Land use/cover and planning unit data types can be raster or vector
        # Factor data types can be raster only
        # Table data types can be csv only
        fileFilter = '*{0} *{1}'.format(self.main.appSettings['selectRasterfileExt'], self.main.appSettings['selectShapefileExt'])
        
        if dataType == MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_FACTOR):
            fileFilter = '*{0}'.format(self.main.appSettings['selectRasterfileExt'])
        elif dataType == MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_TABLE):
            fileFilter = '*{0}'.format(self.main.appSettings['selectCsvfileExt'])
        
        file = unicode(QFileDialog.getOpenFileName(
            self, MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_SELECT_FILE), QDir.homePath(), MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_SELECT_FILE) + ' ({0})'.format(fileFilter)))
        
        if file:
            # comboBoxDataType.setDisabled(True)
            lineEditDataFile = self.contentAddData.findChild(QLineEdit, 'lineEditDataFile_' + tableRow)
            lineEditDataFile.setText(file)
            buttonSelectDataFile = self.contentAddData.findChild(QPushButton, 'buttonSelectDataFile_' + tableRow)
            buttonSelectDataFile.setDisabled(True)
            buttonDataProperties = self.contentAddData.findChild(QPushButton, 'buttonDataProperties_' + tableRow)
            buttonDataProperties.setEnabled(True)
    
    
    def handlerDataProperties(self):
        """Slot method for setting the data's properties.
        
        Opens a DialogLumensAddDataProperties dialog instance.
        """
        buttonSender = self.sender()
        objectName = buttonSender.objectName()
        tableRow = objectName.split('_')[1]
        
        comboBoxDataType = self.contentAddData.findChild(QComboBox, 'comboBoxDataType_' + tableRow)
        dataType = unicode(comboBoxDataType.currentText())
        lineEditDataFile = self.contentAddData.findChild(QLineEdit, 'lineEditDataFile_' + tableRow)
        dataFile = unicode(lineEditDataFile.text())
        
        dialog = DialogLumensAddDataProperties(self, dataType, dataFile)
        if dialog.exec_():
            buttonDataProperties = self.contentAddData.findChild(QPushButton, 'buttonDataProperties_' + tableRow)
            # Set the hidden fields
            lineEditDataDescription = self.contentAddData.findChild(QLineEdit, 'lineEditDataDescription_' + tableRow)
            lineEditDataDescription.setText(dialog.getDataDescription())
            spinBoxDataPeriod = self.contentAddData.findChild(QSpinBox, 'spinBoxDataPeriod_' + tableRow)
            spinBoxDataPeriod.setValue(dialog.getDataPeriod())
            lineEditDataFieldAttribute = self.contentAddData.findChild(QLineEdit, 'lineEditDataFieldAttribute_' + tableRow)
            lineEditDataFieldAttribute.setText(dialog.getDataFieldAttribute())
            lineEditDataDissolvedShapefile = self.contentAddData.findChild(QLineEdit, 'lineEditDataDissolvedShapefile_' + tableRow)
            lineEditDataDissolvedShapefile.setText(dialog.getDataDissolvedShapefile())
            lineEditDataTableCsv = self.contentAddData.findChild(QLineEdit, 'lineEditDataTableCsv_' + tableRow)
            lineEditDataTableCsv.setText(dialog.getDataTableCsv())
    
    
    def handlerDeleteDataRow(self):
        """Slot method for deleting a data row.
        """
        buttonSender = self.sender()
        objectName = buttonSender.objectName()
        tableRow = objectName.split('_')[1]
        layoutRow = self.layoutTableAddData.itemAt(int(tableRow) - 1).layout()
        self.clearLayout(layoutRow)
    
    
    #***********************************************************
    # Process dialog
    #***********************************************************
    def setAppSettings(self):
        """Set the required values from the form widgets.
        """
        self.tableAddData = []
        
        for tableRow in range(1, self.tableAddDataRowCount + 1):
            lineEditDataFile = self.findChild(QLineEdit, 'lineEditDataFile_' + str(tableRow))
            
            if not lineEditDataFile: # Row has been deleted
                print ('DEBUG: skipping a deleted row.')
                continue
            
            comboBoxDataType = self.findChild(QComboBox, 'comboBoxDataType_' + str(tableRow))
            lineEditDataDescription = self.findChild(QLineEdit, 'lineEditDataDescription_' + str(tableRow))
            spinBoxDataPeriod = self.findChild(QSpinBox, 'spinBoxDataPeriod_' + str(tableRow))
            lineEditDataFieldAttribute = self.findChild(QLineEdit, 'lineEditDataFieldAttribute_' + str(tableRow))
            lineEditDataDissolvedShapefile = self.findChild(QLineEdit, 'lineEditDataDissolvedShapefile_' + str(tableRow))
            lineEditDataTableCsv = self.findChild(QLineEdit, 'lineEditDataTableCsv_' + str(tableRow))
            
            dataFile = unicode(lineEditDataFile.text())
            dataType = unicode(comboBoxDataType.currentText())
            dataDescription = unicode(lineEditDataDescription.text())
            dataPeriod = spinBoxDataPeriod.value()
            dataFieldAttribute = unicode(lineEditDataFieldAttribute.text())
            dataDissolvedShapefile = unicode(lineEditDataDissolvedShapefile.text())
            dataTableCsv = unicode(lineEditDataTableCsv.text())
            
            if dataType == MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_LAND_USE_COVER):
                dataType = 0
            elif dataType == MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_PLANNING_UNIT):
                dataType = 1
            elif dataType == MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_FACTOR):
                dataType = 2
            elif dataType == MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_TABLE):
                dataType = 3
            
            tableRowData = {
                'dataFile': dataFile,
                'dataType': dataType,
                'dataPeriod': dataPeriod,
                'dataDescription': dataDescription,
                'dataFieldAttribute': dataFieldAttribute,
                'dataDissolvedShapefile': dataDissolvedShapefile,
                'dataTableCsv': dataTableCsv,
            }
            
            self.tableAddData.append(tableRowData)
    
    
    def validForm(self):
        """Method for validating the form values.
        """
        valid = False
        
        # Data type ids
        landUseCover = 0
        planningUnit = 1
        factor = 2
        table = 3
        
        for tableRowData in self.tableAddData:
            isRasterFile = False
            isVectorFile = False
            isCsvFile = False
            
            dataFile = tableRowData['dataFile']
            dataType = tableRowData['dataType']
            dataPeriod = tableRowData['dataPeriod']
            dataDescription = tableRowData['dataDescription']
            dataFieldAttribute = tableRowData['dataFieldAttribute']
            dataDissolvedShapefile = tableRowData['dataDissolvedShapefile']
            dataTableCsv = tableRowData['dataTableCsv']
            
            if dataFile.lower().endswith(self.main.appSettings['selectRasterfileExt']):
                isRasterFile = True
            elif dataFile.lower().endswith(self.main.appSettings['selectShapefileExt']):
                isVectorFile = True
            elif dataFile.lower().endswith(self.main.appSettings['selectCsvfileExt']):
                isCsvFile = True
            
            if dataType == landUseCover and isRasterFile and dataDescription and dataPeriod and dataTableCsv:
                valid = True
            elif dataType == landUseCover and isVectorFile and dataDescription and dataPeriod and dataFieldAttribute and dataDissolvedShapefile and dataTableCsv:
                valid = True
            elif dataType == planningUnit and isRasterFile and dataDescription and dataTableCsv:
                valid = True
            elif dataType == planningUnit and isVectorFile and dataDescription and dataFieldAttribute and dataDissolvedShapefile and dataTableCsv:
                valid = True
            elif dataType == factor and isRasterFile and dataDescription:
                valid = True
            elif dataType == table and isCsvFile and dataDescription:
                valid = True
            else:
                QMessageBox.critical(self.main, MenuFactory.getLabel(MenuFactory.MSG_ERROR), MenuFactory.getDescription(MenuFactory.MSG_ERROR))
        
        return valid
    
    
    def handlerProcessAddData(self):
        """Slot method to pass the form values and execute the "Add Data" R algorithms.
        
        Depending on the type of the added data file (vector or raster) the appropriate
        R algorithm is called.
        
        The "Add Data" process calls the following algorithms:
        1. r:dbaddraster
        2. r:dbaddvector
        3. r:dbaddlut
        """
        self.setAppSettings()
        
        if self.validForm():
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            self.buttonProcessAddData.setDisabled(True)
            
            algName = None
            outputs = None
            activeProject = self.main.appSettings['DialogLumensOpenDatabase']['projectFile'].replace(os.path.sep, '/')
            
            # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
            # self.main.setWindowState(Qt.WindowMinimized)
            
            for tableRowData in self.tableAddData:
                # The algName to be used depends on the type of the dataFile (vector or raster)
                
                print ('DEBUG')
                print (tableRowData)
                
                if tableRowData['dataFile'].lower().endswith(self.main.appSettings['selectRasterfileExt']):
                    algName = 'r:db_add_raster'
                    
                    outputs = general.run(
                        algName, {
                            'proj.file': activeProject,
                            'type': tableRowData['dataType'],
                            'data': tableRowData['dataFile'].replace(os.path.sep, '/'),
                            'period': tableRowData['dataPeriod'],
                            'description': tableRowData['dataDescription'],
                            'attribute_table': tableRowData['dataTableCsv'],
                            'statusoutput': 'TEMPORARY_OUTPUT'
                        }    
                    )
                elif tableRowData['dataFile'].lower().endswith(self.main.appSettings['selectShapefileExt']):
                    algName = 'r:db_add_vector'
                    
                    outputs = general.run(
                        algName, {
                            'proj.file': activeProject,
                            'type': tableRowData['dataType'],
                            'data': tableRowData['dataDissolvedShapefile'].replace(os.path.sep, '/'),
                            'attribute_field_id': tableRowData['dataFieldAttribute'],
                            'period': tableRowData['dataPeriod'],
                            'description': tableRowData['dataDescription'],
                            'attribute_table': tableRowData['dataTableCsv'],
                            'statusoutput': 'TEMPORARY_OUTPUT'
                        }
                    )
                elif tableRowData['dataFile'].lower().endswith(self.main.appSettings['selectCsvfileExt']):
                    algName = 'r:db_add_lut'
                    
                    tableRowDataFile = tableRowData['dataFile'].replace(os.path.sep, '/')
                    if 'habitat' in tableRowData['dataDescription']:
                        self.main.appSettings['defaultHabitatLookupTable'] = tableRowDataFile
                        print (self.main.appSettings['defaultHabitatLookupTable'])
                    
                    outputs = general.run(
                        algName, {
                            'proj.file': activeProject,
                            'description': tableRowData['dataDescription'],
                            'attribute_table': tableRowDataFile,
                            'statusoutput': 'TEMPORARY_OUTPUT'
                        }     
                    )
                
                # Display ROut file in debug mode
                if self.main.appSettings['debug']:
                    dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                    dialog.exec_()
            
            # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
            # self.main.setWindowState(Qt.WindowActive)
            
            algSuccess = self.outputsMessageBox(algName, outputs, 'Data successfully added to LUMENS database!', 'Failed to add data to LUMENS database.')
            
            self.buttonProcessAddData.setEnabled(True)
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            
            if algSuccess:
                # Reload added data info
                self.main.loadAddedDataInfo()
                self.clearAllLayout()
                self.close()
