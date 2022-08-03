#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, csv, tempfile, datetime
from qgis.core import *
from PyQt5 import QtCore, QtGui
from processing.tools import *

from dialog_lumens_base import DialogLumensBase
from dialog_lumens_viewer import DialogLumensViewer

from menu_factory import MenuFactory

class DialogLumensAddDataProperties(QtGui.QDialog):
    """LUMENS dialog class for the "Add Data" data properties.
    
    Attributes:
        dataType (str): the type of the added data, can be either raster, vector, or csv files.
        dataFile (str): the file path of the added data.
        dataDescription (str): the description of the added data.
        dataPeriod (int): the period of the added data.
        dataTableCsv (str): the path to the table csv temporary file
        dataFieldAttribute (str): the selected attribute of the added shapefile data.
        dataDissolvedShapefile (str): the file path of the added shapefile data that has been dissolved.
    """
    
    def __init__(self, parent, dataType, dataFile):
        """Constructor method for initializing a LUMENS "Add Data" data properties dialog window instance.
        
        Args:
            parent: the dialog window's parent instance.
            dataType (str): the type of the added data.
            dataFile (str): the file path of the added data.
        """
        super(DialogLumensAddDataProperties, self).__init__(parent)
        self.parent = parent
        self.dialogTitle = MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_PROPERTIES)
        
        self.dataType = dataType
        self.dataFile = dataFile
        # Use file name without extension as data description
        self.dataDescription = os.path.splitext(os.path.basename(dataFile))[0]
        self.dataPeriod = 0
        self.dataTableCsv = None
        self.dataFieldAttribute = None
        self.dataDissolvedShapefile = None
        
        # The classification of the data to be added
        self.classifiedOptions = {
            1: MenuFactory.getLabel(MenuFactory.APP_PROP_FIRST_CLASS), #'Undisturbed forest', # Hutan primer
            2: MenuFactory.getLabel(MenuFactory.APP_PROP_SECOND_CLASS), #'Logged-over forest', # Hutan sekunder
            3: MenuFactory.getLabel(MenuFactory.APP_PROP_THIRD_CLASS), #'Monoculture tree-based plantation', # Tanaman pohon monokulture
            4: MenuFactory.getLabel(MenuFactory.APP_PROP_FOURTH_CLASS), #'Mixed tree-based plantation', # Tanaman pohon campuran
            5: MenuFactory.getLabel(MenuFactory.APP_PROP_FIFTH_CLASS), #'Agriculture/annual crop', # Tanaman pertanian semusim 
            6: MenuFactory.getLabel(MenuFactory.APP_PROP_SIXTH_CLASS), #'Shrub, grass, and cleared land', # Semak, rumput, dan lahan terbuka
            7: MenuFactory.getLabel(MenuFactory.APP_PROP_SEVENTH_CLASS), #'Settlement and built-up area', # Pemukiman
            8: MenuFactory.getLabel(MenuFactory.APP_PROP_EIGHTH_CLASS), #'Others',
        }
        self.isRasterFile = False
        self.isVectorFile = False
        self.isCsvFile = False
        
        if self.dataFile.lower().endswith(self.parent.main.appSettings['selectRasterfileExt']):
            self.isRasterFile = True
        elif self.dataFile.lower().endswith(self.parent.main.appSettings['selectShapefileExt']):
            self.isVectorFile = True
        elif self.dataFile.lower().endswith(self.parent.main.appSettings['selectCsvfileExt']):
            self.isCsvFile = True
        
        if self.parent.main.appSettings['debug']:
            print 'DEBUG: DialogLumensAddDataProperties init'
            self.logger = logging.getLogger(type(self).__name__)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            fh = logging.FileHandler(os.path.join(self.parent.main.appSettings['appDir'], 'logs', type(self).__name__ + '.log'))
            fh.setFormatter(formatter)
            self.logger.addHandler(ch)
            self.logger.addHandler(fh)
            self.logger.setLevel(logging.DEBUG)
        
        self.setupUi(self)
        
        # Raster data table is loaded only for 'Land use/cover' and 'Planning unit'
        if self.isRasterFile and self.dataType in (MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_LAND_USE_COVER), MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_PLANNING_UNIT)):
            self.loadRasterDataTable()
        elif self.isVectorFile:
            self.loadDataFieldAttributes()
            
        if self.parent.main.appSettings['dataMappingFile']:
            self.lineEditDataMapping.setText(self.parent.main.appSettings['dataMappingFile'])
            self.processDataMapping(self.parent.main.appSettings['dataMappingFile'])   
        
        self.buttonProcessDissolve.clicked.connect(self.handlerProcessDissolve)
        self.buttonProcessSave.clicked.connect(self.handlerProcessSave)
        self.buttonSelectDataMapping.clicked.connect(self.handlerSelectDataMapping)
    
    
    def setupUi(self, parent):
        """Method for building the dialog UI.
        
        Args:
            parent: the dialog's parent instance.
        """
        self.dialogLayout = QtGui.QVBoxLayout()
        
        addFileType = None
        
        if self.isRasterFile:
            addFileType = MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_RASTER)
        elif self.isVectorFile:
            addFileType = MenuFactory.getLabel(MenuFactory.APP_ADD_VECTOR_DATA)
        elif self.isCsvFile:
            addFileType = MenuFactory.getLabel(MenuFactory.APP_ADD_TABULAR_DATA)
        
        self.groupBoxDataProperties = QtGui.QGroupBox('{0}: {1}'.format(self.dataType, addFileType))
        self.layoutGroupBoxDataProperties = QtGui.QVBoxLayout()
        self.layoutGroupBoxDataProperties.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxDataProperties.setLayout(self.layoutGroupBoxDataProperties)
        self.layoutDataPropertiesInfo = QtGui.QVBoxLayout()
        self.layoutDataProperties = QtGui.QGridLayout()
        self.layoutGroupBoxDataProperties.addLayout(self.layoutDataPropertiesInfo)
        self.layoutGroupBoxDataProperties.addLayout(self.layoutDataProperties)
        
        self.labelDataPropertiesInfo = QtGui.QLabel()
        self.labelDataPropertiesInfo.setText('\n')
        self.layoutDataPropertiesInfo.addWidget(self.labelDataPropertiesInfo)
        
        rowCount = 0
        
        self.labelDataDescription = QtGui.QLabel()
        self.labelDataDescription.setText('&' + MenuFactory.getLabel(MenuFactory.APP_PROP_DESCRIPTION) + ':')
        self.lineEditDataDescription = QtGui.QLineEdit()
        self.lineEditDataDescription.setText(self.dataDescription)
        self.labelDataDescription.setBuddy(self.lineEditDataDescription)
        
        td = datetime.date.today()
        self.labelDataSpinBoxPeriod = QtGui.QLabel()
        self.labelDataSpinBoxPeriod.setText('&' + MenuFactory.getLabel(MenuFactory.APP_PROP_YEAR) + ':')
        self.spinBoxDataPeriod = QtGui.QSpinBox()
        self.spinBoxDataPeriod.setRange(1, 9999)
        # self.spinBoxDataPeriod.setValue(td.year)
        self.labelDataSpinBoxPeriod.setBuddy(self.spinBoxDataPeriod)
        
        if self.dataType == MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_LAND_USE_COVER):
            # Description + Period
            self.layoutDataProperties.addWidget(self.labelDataDescription, rowCount, 0)
            self.layoutDataProperties.addWidget(self.lineEditDataDescription, rowCount, 1)
            rowCount += 1
            self.layoutDataProperties.addWidget(self.labelDataSpinBoxPeriod, rowCount, 0)
            self.layoutDataProperties.addWidget(self.spinBoxDataPeriod, rowCount, 1)
        else:
            # Description only
            self.layoutDataProperties.addWidget(self.labelDataDescription, rowCount, 0)
            self.layoutDataProperties.addWidget(self.lineEditDataDescription, rowCount, 1)
        
        self.labeldataFieldAttribute = QtGui.QLabel()
        self.labeldataFieldAttribute.setText(MenuFactory.getLabel(MenuFactory.APP_PROP_FIELD_ATTRIBUTE) + ':')
        self.comboBoxDataFieldAttribute = QtGui.QComboBox()
        self.comboBoxDataFieldAttribute.setDisabled(True)
        
        if self.isVectorFile:
            # For vector data files
            rowCount += 1
            self.layoutDataProperties.addWidget(self.labeldataFieldAttribute, rowCount, 0)
            self.layoutDataProperties.addWidget(self.comboBoxDataFieldAttribute, rowCount, 1)
        
        self.dataTable = QtGui.QTableWidget()
        self.dataTable.setDisabled(True)
        self.dataTable.verticalHeader().setVisible(False)
        
        self.labelDataMapping = QtGui.QLabel()
        self.labelDataMapping.setText(MenuFactory.getLabel(MenuFactory.APP_PROP_CLASS_DEFINITION_FILE) + ':')
        self.lineEditDataMapping = QtGui.QLineEdit()
        self.lineEditDataMapping.setReadOnly(True)
        self.buttonSelectDataMapping = QtGui.QPushButton()
        self.buttonSelectDataMapping.setText('&' + MenuFactory.getLabel(MenuFactory.APP_BROWSE) + ':')
        self.buttonSelectDataMapping.setDisabled(True)
        
        rowCount += 1
        
        if self.dataType == MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_LAND_USE_COVER) or self.dataType == MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_PLANNING_UNIT):
            dataTableColumnSpan = 2
            if self.isVectorFile or self.isRasterFile:
                self.layoutDataProperties.addWidget(self.labelDataMapping, rowCount, 0)
                self.layoutDataProperties.addWidget(self.lineEditDataMapping, rowCount, 1)
                self.layoutDataProperties.addWidget(self.buttonSelectDataMapping, rowCount, 2)
                dataTableColumnSpan = 3
                rowCount += 1
            if self.isRasterFile:
                self.buttonSelectDataMapping.setEnabled(True)
            self.layoutDataProperties.addWidget(self.dataTable, rowCount, 0, 1, dataTableColumnSpan)
        
        ######################################################################
        
        self.layoutButtonProcess = QtGui.QHBoxLayout()
        self.buttonProcessDissolve = QtGui.QPushButton()
        self.buttonProcessDissolve.setText('&' + MenuFactory.getLabel(MenuFactory.APP_PROP_DISSOLVE))
        self.buttonProcessDissolve.setVisible(False)
        self.buttonProcessSave = QtGui.QPushButton()
        self.buttonProcessSave.setText('&' + MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_PROPERTIES_SAVE))
        self.layoutButtonProcess.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonProcess.addWidget(self.buttonProcessDissolve)
        self.layoutButtonProcess.addWidget(self.buttonProcessSave)
        
        if self.isVectorFile:
            self.buttonProcessDissolve.setVisible(True)
            self.buttonProcessSave.setDisabled(True)
        
        self.dialogLayout.addWidget(self.groupBoxDataProperties)
        self.dialogLayout.addLayout(self.layoutButtonProcess)
        
        self.setLayout(self.dialogLayout)
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(800, 600)
        self.resize(parent.sizeHint())
    
    
    def getDataDescription(self):
        """Getter method.
        """
        return self.dataDescription
    
    
    def getDataPeriod(self):
        """Getter method.
        """
        return self.dataPeriod
    
    
    def getDataTableCsv(self):
        """Getter method.
        """
        return self.dataTableCsv
    
    
    def getDataFieldAttribute(self):
        """Getter method.
        """
        return self.dataFieldAttribute
    
    
    def getDataDissolvedShapefile(self):
        """Getter method.
        """
        return self.dataDissolvedShapefile
    
    
    def loadRasterDataTable(self):
        """Method for loading the raster properties to the data table.
        
        The raster loading process calls the following algorithm:
        1. r:lumensdatapropertiesraster
        """
        algName = 'r:dbaddrasterprop'
        
        outputs = general.runalg(
            algName,
            self.dataFile,
            None,
        )
        
        outputsKey = 'data_table'
        
        if outputs and outputsKey in outputs and os.path.exists(outputs[outputsKey]):  
            with open(outputs[outputsKey], 'rb') as f:
                hasHeader = csv.Sniffer().has_header(f.read(1024))
                f.seek(0)
                reader = csv.reader(f)
                
                if hasHeader: # Set the column headers
                    headerRow = reader.next()
                    fields = [str(field) for field in headerRow]
                    
                    fields.append('Legend') # Additional columns ('Classified' only for Land Use/Cover types)
                    
                    if self.dataType == MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_LAND_USE_COVER):
                        fields.append('Classified')
                    
                    self.dataTable.setColumnCount(len(fields))
                    self.dataTable.setHorizontalHeaderLabels(fields)
                
                dataTable = []
                
                for row in reader:
                    dataRow = [QtGui.QTableWidgetItem(field) for field in row]
                    dataTable.append(dataRow)
                
                self.dataTable.setRowCount(len(dataTable))
                
                tableRow = 0
                columnLegend = 0
                columnClassified = 0
                
                for dataRow in dataTable:
                    tableColumn = 0
                    for fieldTableItem in dataRow:
                        fieldTableItem.setFlags(fieldTableItem.flags() & ~QtCore.Qt.ItemIsEnabled)
                        self.dataTable.setItem(tableRow, tableColumn, fieldTableItem)
                        self.dataTable.horizontalHeader().setResizeMode(tableColumn, QtGui.QHeaderView.ResizeToContents)
                        tableColumn += 1
                    
                    # Additional columns ('Classified' only for Land Use/Cover types)
                    fieldLegend = QtGui.QTableWidgetItem('Unidentified Landuse {0}'.format(tableRow + 1))
                    columnLegend = tableColumn
                    self.dataTable.setItem(tableRow, tableColumn, fieldLegend)
                    self.dataTable.horizontalHeader().setResizeMode(columnLegend, QtGui.QHeaderView.ResizeToContents)
                    
                    if self.dataType == MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_LAND_USE_COVER):
                        tableColumn += 1
                        columnClassified = tableColumn
                        comboBoxClassified = QtGui.QComboBox()
                        for key, val in self.classifiedOptions.iteritems():
                            comboBoxClassified.addItem(val, key)
                        self.dataTable.setCellWidget(tableRow, tableColumn, comboBoxClassified)
                        self.dataTable.horizontalHeader().setResizeMode(columnClassified, QtGui.QHeaderView.ResizeToContents)
                    
                    tableRow += 1
                
                self.dataTable.setEnabled(True)
    
    
    def loadDataFieldAttributes(self):
        """Method for loading the shapefile's attributes.
        """
        registry = QgsProviderRegistry.instance()
        provider = registry.provider('ogr', self.dataFile)
        
        if not provider.isValid():
            return
        
        attributes = []
        
        for field in provider.fields():
            attributes.append(field.name())
        
        self.comboBoxDataFieldAttribute.clear()
        self.comboBoxDataFieldAttribute.addItems(sorted(attributes))
        self.comboBoxDataFieldAttribute.setEnabled(True)
    
    
    #***********************************************************
    # Process dialog
    #***********************************************************
    def validDissolved(self):
        """Method for validating the form values before dissolving.
        """
        valid = False
        
        if self.dataType == MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_LAND_USE_COVER) and self.isVectorFile and self.dataDescription and self.dataPeriod and self.dataFieldAttribute:
            valid = True
        elif self.dataType == MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_PLANNING_UNIT) and self.isVectorFile and self.dataDescription and self.dataFieldAttribute:
            valid = True
        else:
            QtGui.QMessageBox.critical(self, MenuFactory.getLabel(MenuFactory.MSG_ERROR), MenuFactory.getDescription(MenuFactory.MSG_ERROR))
        
        return valid
    
    
    def validForm(self):
        """Method for validating the form values.
        """
        valid = False
        
        if self.dataType == MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_LAND_USE_COVER) and self.isRasterFile and self.dataDescription and self.dataPeriod and self.dataTableCsv:
            valid = True
        elif self.dataType == MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_LAND_USE_COVER) and self.isVectorFile and self.dataDescription and self.dataPeriod and self.dataFieldAttribute and self.dataTableCsv:
            valid = True
        elif self.dataType == MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_PLANNING_UNIT) and self.isRasterFile and self.dataDescription and self.dataTableCsv:
            valid = True
        elif self.dataType == MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_PLANNING_UNIT) and self.isVectorFile and self.dataDescription and self.dataFieldAttribute and self.dataTableCsv:
            valid = True
        elif self.dataType == MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_FACTOR) and self.isRasterFile and self.dataDescription:
            valid = True
        elif self.dataType == MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_TABLE) and self.isCsvFile and self.dataDescription:
            valid = True
        else:
            QtGui.QMessageBox.critical(self, MenuFactory.getLabel(MenuFactory.MSG_ERROR), MenuFactory.getDescription(MenuFactory.MSG_ERROR))
        
        return valid
    
    
    def setFormFields(self):
        """Set the required values from the form widgets.
        """
        self.dataDescription = unicode(self.lineEditDataDescription.text())
        self.dataPeriod = self.spinBoxDataPeriod.value()
        self.dataFieldAttribute = unicode(self.comboBoxDataFieldAttribute.currentText())
        self.dataTableCsv = DialogLumensBase.writeTableCsv(self.dataTable, True)
        
    
    def handlerProcessDissolve(self):
        """Slot method to pass the form values and execute the "Dissolve" R algorithm.
        
        The "Dissolve" process calls the following algorithm:
        1. r:lumensdissolve
        """
        self.setFormFields()
        
        if self.validDissolved():
            logging.getLogger(type(self).__name__).info('start: %s' % 'LUMENS Dissolve')
            self.buttonProcessDissolve.setDisabled(True)
                
            algName = 'r:dbdissolve'
            
            outputs = general.runalg(
                algName,
                self.dataFile,
                self.dataFieldAttribute,
                None,
            )
            
            # Display ROut file in debug mode
            if self.parent.main.appSettings['debug']:
                dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.parent.main.appSettings['ROutFile'])
                dialog.exec_()
            
            outputsKey = 'admin_output'
            
            if outputs and outputsKey in outputs and os.path.exists(outputs[outputsKey]):
                self.dataDissolvedShapefile = outputs[outputsKey]
                
                registry = QgsProviderRegistry.instance()
                provider = registry.provider('ogr', outputs[outputsKey])
                
                if not provider.isValid():
                    logging.getLogger(type(self).__name__).error('LUMENS Dissolve: invalid shapefile')
                    return
                
                attributes = []
                for field in provider.fields():
                    attributes.append(field.name())
                
                # Additional columns ('Legend', 'Classified' only for Land Use/Cover types)
                if self.dataType == MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_LAND_USE_COVER):
                    attributes.append('Legend')
                    attributes.append('Classified')
                
                features = provider.getFeatures()
                
                if features:
                    self.dataTable.setEnabled(True)
                    self.dataTable.setRowCount(provider.featureCount())
                    self.dataTable.setColumnCount(len(attributes))
                    self.dataTable.verticalHeader().setVisible(False)
                    self.dataTable.setHorizontalHeaderLabels(attributes)
                    
                    # Need a nicer way than manual looping
                    tableRow = 0
                    for feature in features:
                        tableColumn = 0
                        for attribute in attributes:
                            if attribute == 'Legend' or attribute == 'Classified': # Skip the additional column
                                continue
                            attributeValue = str(feature.attribute(attribute))
                            attributeValueTableItem = QtGui.QTableWidgetItem(attributeValue)
                            if tableColumn == 1 and self.dataType == MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_PLANNING_UNIT): # Editable second column for Vector Planning Units
                                pass
                            else:
                                attributeValueTableItem.setFlags(attributeValueTableItem.flags() & ~QtCore.Qt.ItemIsEnabled)
                            self.dataTable.setItem(tableRow, tableColumn, attributeValueTableItem)
                            self.dataTable.horizontalHeader().setResizeMode(tableColumn, QtGui.QHeaderView.ResizeToContents)
                            tableColumn += 1
                        
                        # Additional columns ('Legend', 'Classified' only for Land Use/Cover types)
                        if self.dataType == MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_LAND_USE_COVER):
                            fieldLegend = QtGui.QTableWidgetItem('Unidentified Landuse {0}'.format(tableRow + 1))
                            columnLegend = tableColumn
                            self.dataTable.setItem(tableRow, tableColumn, fieldLegend)
                            self.dataTable.horizontalHeader().setResizeMode(columnLegend, QtGui.QHeaderView.ResizeToContents)
                            
                            tableColumn += 1
                            columnClassified = tableColumn
                            comboBoxClassified = QtGui.QComboBox()
                            for key, val in self.classifiedOptions.iteritems():
                                comboBoxClassified.addItem(val, key)
                            self.dataTable.setCellWidget(tableRow, tableColumn, comboBoxClassified)
                            self.dataTable.horizontalHeader().setResizeMode(columnClassified, QtGui.QHeaderView.ResizeToContents)
                        
                        tableRow += 1
                    
                    self.dataTable.resizeColumnsToContents()
                    self.buttonProcessSave.setEnabled(True)
            
            self.buttonSelectDataMapping.setEnabled(True)
            self.buttonProcessDissolve.setEnabled(True)
            logging.getLogger(type(self).__name__).info('end: %s' % 'LUMENS Dissolve')
        
    
    def handlerProcessSave(self):
        """Slot method for saving the form values before closing the dialog.
        """
        self.setFormFields()
        
        if self.validForm():
            self.accept()
    
    
    def handlerSelectDataMapping(self):
        """Slot method for selecting a data mapping file in CSV format.
        """
        dataMappingFile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, MenuFactory.getLabel(MenuFactory.MGS_APP_SELECT_DATA_MAPPING_FILE), QtCore.QDir.homePath(), MenuFactory.getDescription(MenuFactory.MGS_APP_SELECT_DATA_MAPPING_FILE) + ' (*{0})'.format(self.parent.main.appSettings['selectCsvfileExt'])))
        
        if dataMappingFile:
            logging.getLogger(type(self).__name__).info('select data mapping file: %s', dataMappingFile)
            
            self.lineEditDataMapping.setText(dataMappingFile)
            
            self.processDataMapping(dataMappingFile)
            
            self.parent.main.appSettings['dataMappingFile'] = dataMappingFile
    
    
    def processDataMapping(self, dataMappingFile):
        """Method for processing the data mapping file and mapping the data
        in the data table.
        
        Args:
            dataMappingFile (str): the file path of a data mapping file.
        """
        dataMappingClassified = {}
        dataMappingLegend = {}
        dataMappingZone = {}
        
        with open(dataMappingFile, 'rb') as f:
            hasHeader = csv.Sniffer().has_header(f.read(1024))
            f.seek(0)
            reader = csv.reader(f)
            
            if hasHeader: # Skip the header
                next(reader)
            
            if self.dataType == MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_PLANNING_UNIT):
                for row in reader:
                    dataMappingZone[str(row[0]).lower()] = str(row[1])
                
                fieldColumn = zoneColumn = 0
                
                for headerColumn in range(self.dataTable.columnCount()):
                    headerItem = self.dataTable.horizontalHeaderItem(headerColumn)
                    headerText = headerItem.text()
                    if self.isVectorFile:
                        if headerText == unicode(self.comboBoxDataFieldAttribute.currentText()):
                            fieldColumn = headerColumn
                        else:
                            zoneColumn = headerColumn
                    if self.isRasterFile:
                        if headerText == 'ID':
                            fieldColumn = headerColumn
                        elif headerText == 'Legend':
                            zoneColumn = headerColumn
                            
                for tableRow in range(self.dataTable.rowCount()):
                    fieldItem = self.dataTable.item(tableRow, fieldColumn)
                    fieldItemText = fieldItem.text().lower()
                    
                    if fieldItemText in dataMappingZone:
                        legend = dataMappingZone[fieldItemText]
                        newFieldLegend = QtGui.QTableWidgetItem(legend)
                        self.dataTable.setItem(tableRow, zoneColumn, newFieldLegend)                  
            
            if self.dataType == MenuFactory.getLabel(MenuFactory.APP_ADD_DATA_LAND_USE_COVER):
                for row in reader:
                    dataMappingLegend[str(row[0]).lower()] = str(row[1])
                    dataMappingClassified[str(row[0]).lower()] = str(row[2]).lower()
                
                fieldColumn = classifiedColumn = legendColumn = 0
                
                for headerColumn in range(self.dataTable.columnCount()):
                    headerItem = self.dataTable.horizontalHeaderItem(headerColumn)
                    headerText = headerItem.text()
                    if self.isVectorFile:
                        if headerText == unicode(self.comboBoxDataFieldAttribute.currentText()):
                            fieldColumn = headerColumn
                        elif headerText == 'Classified':
                            classifiedColumn = headerColumn
                        elif headerText == 'Legend':
                            legendColumn = headerColumn
                    elif self.isRasterFile:
                        if headerText == 'ID':
                            fieldColumn = headerColumn
                        elif headerText == 'Classified':
                            classifiedColumn = headerColumn
                        elif headerText == 'Legend':
                            legendColumn = headerColumn
                    
                for tableRow in range(self.dataTable.rowCount()):
                    fieldItem = self.dataTable.item(tableRow, fieldColumn)
                    fieldItemText = fieldItem.text().lower()
                    classifiedWidget = self.dataTable.cellWidget(tableRow, classifiedColumn)
                    
                    if fieldItemText in dataMappingClassified:
                        legend = dataMappingLegend[fieldItemText]
                        newFieldLegend = QtGui.QTableWidgetItem(legend)
                        self.dataTable.setItem(tableRow, legendColumn, newFieldLegend)
                        
                        classification = dataMappingClassified[fieldItemText]
                        
                        # Perform case insensitive search of the ComboBox
                        classifiedOptionIndex = classifiedWidget.findText(classification, QtCore.Qt.MatchFixedString)
                        # Found a data mapping match!
                        if classifiedOptionIndex >= 0:
                            classifiedWidget.setCurrentIndex(classifiedOptionIndex)
    
    
    def accept(self):
        """Overload method that is called when the dialog is accepted.
        """
        QtGui.QDialog.accept(self)
    
    
    def reject(self):
        """Overload method that is called when the dialog is rejected (canceled).
        """
        QtGui.QDialog.reject(self)
