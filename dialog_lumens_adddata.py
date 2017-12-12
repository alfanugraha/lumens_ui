#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, datetime
from qgis.core import *
from PyQt4 import QtCore, QtGui
from processing.tools import *

from dialog_lumens_base import DialogLumensBase
from dialog_lumens_viewer import DialogLumensViewer
from dialog_lumens_adddata_properties import DialogLumensAddDataProperties


class DialogLumensAddData(QtGui.QDialog, DialogLumensBase):
    """LUMENS "Add Data" dialog class.
    """
    
    def __init__(self, parent):
        super(DialogLumensAddData, self).__init__(parent)
        
        self.main = parent
        self.dialogTitle = 'Add data'
        self.tableAddDataRowCount = 0
        self.tableAddData = []
        
        if self.main.appSettings['debug']:
            print 'DEBUG: DialogLumensAddData init'
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
        
        self.buttonAddDataRow.clicked.connect(self.handlerButtonAddDataRow)
        self.buttonProcessAddData.clicked.connect(self.handlerProcessAddData)
    
    
    def setupUi(self, parent):
        """Method for building the dialog UI.
        
        Args:
            parent: the dialog's parent instance.
        """
        #self.setStyleSheet('background-color: rgb(173, 185, 202);')
        self.dialogLayout = QtGui.QVBoxLayout()
        
        self.groupBoxAddData = QtGui.QGroupBox('Define properties')
        self.layoutGroupBoxAddData = QtGui.QVBoxLayout()
        self.layoutGroupBoxAddData.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxAddData.setLayout(self.layoutGroupBoxAddData)
        self.layoutAddDataInfo = QtGui.QVBoxLayout()
        self.layoutAddData = QtGui.QVBoxLayout()
        self.layoutGroupBoxAddData.addLayout(self.layoutAddDataInfo)
        self.layoutGroupBoxAddData.addLayout(self.layoutAddData)
        
        self.labelAddDataInfo = QtGui.QLabel()
        self.labelAddDataInfo.setText('\n')
        self.labelAddDataInfo.setWordWrap(True)
        self.layoutAddDataInfo.addWidget(self.labelAddDataInfo)
        
        self.layoutButtonAddData = QtGui.QHBoxLayout()
        self.layoutButtonAddData.setContentsMargins(0, 0, 0, 0)
        self.layoutButtonAddData.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.buttonAddDataRow = QtGui.QPushButton()
        self.buttonAddDataRow.setText('Add item')
        self.buttonAddDataRow.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.layoutButtonAddData.addWidget(self.buttonAddDataRow)
        
        self.layoutContentAddData = QtGui.QVBoxLayout()
        self.layoutContentAddData.setContentsMargins(5, 5, 5, 5)
        self.contentAddData = QtGui.QWidget()
        self.contentAddData.setLayout(self.layoutContentAddData)
        self.scrollAddData = QtGui.QScrollArea()
        self.scrollAddData.setWidgetResizable(True);
        self.scrollAddData.setWidget(self.contentAddData)
        self.layoutTableAddData = QtGui.QVBoxLayout()
        self.layoutTableAddData.setAlignment(QtCore.Qt.AlignTop)
        self.layoutContentAddData.addLayout(self.layoutTableAddData)
        
        self.layoutAddData.addLayout(self.layoutButtonAddData)
        self.layoutAddData.addWidget(self.scrollAddData)
        
        self.layoutButtonProcessAddData = QtGui.QHBoxLayout()
        self.buttonProcessAddData = QtGui.QPushButton()
        self.buttonProcessAddData.setText('&Process')
        self.layoutButtonProcessAddData.setAlignment(QtCore.Qt.AlignRight)
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

            if isinstance(item, QtGui.QWidgetItem):
                item.widget().deleteLater() # use this to properly delete the widget
            elif isinstance(item, QtGui.QSpacerItem):
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

                if isinstance(item, QtGui.QWidgetItem):
                    item.widget().deleteLater()  # use this to properly delete the widget
                elif isinstance(item, QtGui.QSpacerItem):
                    pass
                else:
                    self.clearLayout(item.layout())

                layout.removeItem(item)


    def addDataRow(self):
        """Method for adding a data row to the input table.
        """
        self.tableAddDataRowCount = self.tableAddDataRowCount + 1
        
        layoutDataRow = QtGui.QHBoxLayout()
        
        buttonDeleteDataRow = QtGui.QPushButton()
        icon = QtGui.QIcon(':/ui/icons/iconActionClear.png')
        buttonDeleteDataRow.setIcon(icon)
        buttonDeleteDataRow.setObjectName('buttonDeleteDataRow_{0}'.format(str(self.tableAddDataRowCount)))
        layoutDataRow.addWidget(buttonDeleteDataRow)
        
        comboBoxDataType = QtGui.QComboBox()
        comboBoxDataType.addItems(['Land use/cover', 'Planning unit', 'Factor', 'Table'])
        comboBoxDataType.setObjectName('comboBoxDataType_{0}'.format(str(self.tableAddDataRowCount)))
        layoutDataRow.addWidget(comboBoxDataType)
        
        lineEditDataFile = QtGui.QLineEdit()
        lineEditDataFile.setReadOnly(True)
        lineEditDataFile.setObjectName('lineEditDataFile_{0}'.format(str(self.tableAddDataRowCount)))
        layoutDataRow.addWidget(lineEditDataFile)
        
        buttonSelectDataFile = QtGui.QPushButton()
        buttonSelectDataFile.setText('Select file')
        buttonSelectDataFile.setObjectName('buttonSelectDataFile_{0}'.format(str(self.tableAddDataRowCount)))
        layoutDataRow.addWidget(buttonSelectDataFile)

        buttonDataProperties = QtGui.QPushButton()
        buttonDataProperties.setDisabled(True)
        buttonDataProperties.setText('Properties')
        buttonDataProperties.setObjectName('buttonDataProperties_{0}'.format(str(self.tableAddDataRowCount)))
        layoutDataRow.addWidget(buttonDataProperties)
        
        # Hidden fields set from the data properties dialog
        lineEditDataDescription = QtGui.QLineEdit()
        lineEditDataDescription.setObjectName('lineEditDataDescription_{0}'.format(str(self.tableAddDataRowCount)))
        lineEditDataDescription.setVisible(False)
        layoutDataRow.addWidget(lineEditDataDescription)
        
        spinBoxDataPeriod = QtGui.QSpinBox()
        spinBoxDataPeriod.setRange(1, 9999)
        spinBoxDataPeriod.setObjectName('spinBoxDataPeriod_{0}'.format(str(self.tableAddDataRowCount)))
        spinBoxDataPeriod.setVisible(False)
        layoutDataRow.addWidget(spinBoxDataPeriod)
        
        lineEditDataFieldAttribute = QtGui.QLineEdit()
        lineEditDataFieldAttribute.setObjectName('lineEditDataFieldAttribute_{0}'.format(str(self.tableAddDataRowCount)))
        lineEditDataFieldAttribute.setVisible(False)
        layoutDataRow.addWidget(lineEditDataFieldAttribute)
        
        lineEditDataDissolvedShapefile = QtGui.QLineEdit()
        lineEditDataDissolvedShapefile.setObjectName('lineEditDataDissolvedShapefile_{0}'.format(str(self.tableAddDataRowCount)))
        lineEditDataDissolvedShapefile.setVisible(False)
        layoutDataRow.addWidget(lineEditDataDissolvedShapefile)
        
        lineEditDataTableCsv = QtGui.QLineEdit()
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
        
        comboBoxDataType = self.contentAddData.findChild(QtGui.QComboBox, 'comboBoxDataType_' + tableRow)
        dataType = unicode(comboBoxDataType.currentText())
        
        # Land use/cover and planning unit data types can be raster or vector
        # Factor data types can be raster only
        # Table data types can be csv only
        fileFilter = '*{0} *{1}'.format(self.main.appSettings['selectRasterfileExt'], self.main.appSettings['selectShapefileExt'])
        
        if dataType == 'Factor':
            fileFilter = '*{0}'.format(self.main.appSettings['selectRasterfileExt'])
        elif dataType == 'Table':
            fileFilter = '*{0}'.format(self.main.appSettings['selectCsvfileExt'])
        
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select File', QtCore.QDir.homePath(), 'File ({0})'.format(fileFilter)))
        
        if file:
            # comboBoxDataType.setDisabled(True)
            lineEditDataFile = self.contentAddData.findChild(QtGui.QLineEdit, 'lineEditDataFile_' + tableRow)
            lineEditDataFile.setText(file)
            buttonSelectDataFile = self.contentAddData.findChild(QtGui.QPushButton, 'buttonSelectDataFile_' + tableRow)
            buttonSelectDataFile.setDisabled(True)
            buttonDataProperties = self.contentAddData.findChild(QtGui.QPushButton, 'buttonDataProperties_' + tableRow)
            buttonDataProperties.setEnabled(True)
    
    
    def handlerDataProperties(self):
        """Slot method for setting the data's properties.
        
        Opens a DialogLumensAddDataProperties dialog instance.
        """
        buttonSender = self.sender()
        objectName = buttonSender.objectName()
        tableRow = objectName.split('_')[1]
        
        comboBoxDataType = self.contentAddData.findChild(QtGui.QComboBox, 'comboBoxDataType_' + tableRow)
        dataType = unicode(comboBoxDataType.currentText())
        lineEditDataFile = self.contentAddData.findChild(QtGui.QLineEdit, 'lineEditDataFile_' + tableRow)
        dataFile = unicode(lineEditDataFile.text())
        
        dialog = DialogLumensAddDataProperties(self, dataType, dataFile)
        if dialog.exec_():
            buttonDataProperties = self.contentAddData.findChild(QtGui.QPushButton, 'buttonDataProperties_' + tableRow)
            # Set the hidden fields
            lineEditDataDescription = self.contentAddData.findChild(QtGui.QLineEdit, 'lineEditDataDescription_' + tableRow)
            lineEditDataDescription.setText(dialog.getDataDescription())
            spinBoxDataPeriod = self.contentAddData.findChild(QtGui.QSpinBox, 'spinBoxDataPeriod_' + tableRow)
            spinBoxDataPeriod.setValue(dialog.getDataPeriod())
            lineEditDataFieldAttribute = self.contentAddData.findChild(QtGui.QLineEdit, 'lineEditDataFieldAttribute_' + tableRow)
            lineEditDataFieldAttribute.setText(dialog.getDataFieldAttribute())
            lineEditDataDissolvedShapefile = self.contentAddData.findChild(QtGui.QLineEdit, 'lineEditDataDissolvedShapefile_' + tableRow)
            lineEditDataDissolvedShapefile.setText(dialog.getDataDissolvedShapefile())
            lineEditDataTableCsv = self.contentAddData.findChild(QtGui.QLineEdit, 'lineEditDataTableCsv_' + tableRow)
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
            lineEditDataFile = self.findChild(QtGui.QLineEdit, 'lineEditDataFile_' + str(tableRow))
            
            if not lineEditDataFile: # Row has been deleted
                print 'DEBUG: skipping a deleted row.'
                continue
            
            comboBoxDataType = self.findChild(QtGui.QComboBox, 'comboBoxDataType_' + str(tableRow))
            lineEditDataDescription = self.findChild(QtGui.QLineEdit, 'lineEditDataDescription_' + str(tableRow))
            spinBoxDataPeriod = self.findChild(QtGui.QSpinBox, 'spinBoxDataPeriod_' + str(tableRow))
            lineEditDataFieldAttribute = self.findChild(QtGui.QLineEdit, 'lineEditDataFieldAttribute_' + str(tableRow))
            lineEditDataDissolvedShapefile = self.findChild(QtGui.QLineEdit, 'lineEditDataDissolvedShapefile_' + str(tableRow))
            lineEditDataTableCsv = self.findChild(QtGui.QLineEdit, 'lineEditDataTableCsv_' + str(tableRow))
            
            dataFile = unicode(lineEditDataFile.text())
            dataType = unicode(comboBoxDataType.currentText())
            dataDescription = unicode(lineEditDataDescription.text())
            dataPeriod = spinBoxDataPeriod.value()
            dataFieldAttribute = unicode(lineEditDataFieldAttribute.text())
            dataDissolvedShapefile = unicode(lineEditDataDissolvedShapefile.text())
            dataTableCsv = unicode(lineEditDataTableCsv.text())
            
            if dataType == 'Land use/cover':
                dataType = 0
            elif dataType == 'Planning unit':
                dataType = 1
            elif dataType == 'Factor':
                dataType = 2
            elif dataType == 'Table':
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
                QtGui.QMessageBox.critical(self, 'Error', 'Missing some input. Please complete the fields.')
        
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
            # self.main.setWindowState(QtCore.Qt.WindowMinimized)
            
            for tableRowData in self.tableAddData:
                # The algName to be used depends on the type of the dataFile (vector or raster)
                
                print 'DEBUG'
                print tableRowData
                
                if tableRowData['dataFile'].lower().endswith(self.main.appSettings['selectRasterfileExt']):
                    algName = 'r:dbaddraster'
                    
                    outputs = general.runalg(
                        algName,
                        activeProject,
                        tableRowData['dataType'],
                        tableRowData['dataFile'].replace(os.path.sep, '/'),
                        tableRowData['dataPeriod'],
                        tableRowData['dataDescription'],
                        tableRowData['dataTableCsv'],
                        None,
                    )
                elif tableRowData['dataFile'].lower().endswith(self.main.appSettings['selectShapefileExt']):
                    algName = 'r:dbaddvector'
                    
                    outputs = general.runalg(
                        algName,
                        activeProject,
                        tableRowData['dataType'],
                        tableRowData['dataDissolvedShapefile'].replace(os.path.sep, '/'),
                        tableRowData['dataFieldAttribute'],
                        tableRowData['dataPeriod'],
                        tableRowData['dataDescription'],
                        tableRowData['dataTableCsv'],
                        None,
                    )
                elif tableRowData['dataFile'].lower().endswith(self.main.appSettings['selectCsvfileExt']):
                    algName = 'r:dbaddlut'
                    
                    tableRowDataFile = tableRowData['dataFile'].replace(os.path.sep, '/')
                    if 'habitat' in tableRowData['dataDescription']:
                        self.main.appSettings['defaultHabitatLookupTable'] = tableRowDataFile
                        print self.main.appSettings['defaultHabitatLookupTable']
                    
                    outputs = general.runalg(
                        algName,
                        activeProject,
                        tableRowData['dataDescription'],
                        tableRowDataFile,
                        None,
                    )
                
                # Display ROut file in debug mode
                if self.main.appSettings['debug']:
                    dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                    dialog.exec_()
            
            # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
            # self.main.setWindowState(QtCore.Qt.WindowActive)
            
            algSuccess = self.outputsMessageBox(algName, outputs, 'Data successfully added to LUMENS database!', 'Failed to add data to LUMENS database.')
            
            self.buttonProcessAddData.setEnabled(True)
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            
            if algSuccess:
                # Reload added data info
                self.main.loadAddedDataInfo()
                self.clearAllLayout()
                self.close()
