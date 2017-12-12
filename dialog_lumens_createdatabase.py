#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, tempfile, csv
from qgis.core import *
from PyQt4 import QtCore, QtGui
from processing.tools import *

from dialog_lumens_base import DialogLumensBase
from dialog_lumens_viewer import DialogLumensViewer


class DialogLumensCreateDatabase(QtGui.QDialog, DialogLumensBase):
    """LUMENS "Create Database" dialog class.
    """
    
    def __init__(self, parent):
        super(DialogLumensCreateDatabase, self).__init__(parent)
        
        self.main = parent
        self.dialogTitle = 'Create'
        
        self.main.appSettings['DialogLumensCreateDatabase']['outputFolder'] = os.path.join(self.main.appSettings['appDir'], 'output')
        self.dissolvedShapefile = None # For holding the temporary dissolved shapefile path
        
        if self.main.appSettings['debug']:
            print 'DEBUG: DialogLumensCreateDatabase init'
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
        
        self.buttonSelectOutputFolder.clicked.connect(self.handlerSelectOutputFolder)
        self.buttonSelectShapefile.clicked.connect(self.handlerSelectShapefile)
        self.buttonProcessDissolve.clicked.connect(self.handlerProcessDissolve)
        self.buttonProcessCreateDatabase.clicked.connect(self.handlerProcessCreateDatabase)
        self.buttonCreateHelp.clicked.connect(lambda:self.handlerDialogHelp('Create'))
    
    
    def setupUi(self, parent):
        """Method for building the dialog UI.
        
        Args:
            parent: the dialog's parent instance.
        """
        self.dialogLayout = QtGui.QVBoxLayout()
        
        #######################################################################
        # 'Database details' GroupBox
        self.groupBoxDatabaseDetails = QtGui.QGroupBox('Project details')
        self.layoutGroupBoxDatabaseDetails = QtGui.QVBoxLayout()
        self.layoutGroupBoxDatabaseDetails.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxDatabaseDetails.setLayout(self.layoutGroupBoxDatabaseDetails)
        self.layoutDatabaseDetailsInfo = QtGui.QVBoxLayout()
        self.layoutDatabaseDetails = QtGui.QGridLayout()
        self.layoutGroupBoxDatabaseDetails.addLayout(self.layoutDatabaseDetailsInfo)
        self.layoutGroupBoxDatabaseDetails.addLayout(self.layoutDatabaseDetails)
        
        self.labelDatabaseDetailsInfo = QtGui.QLabel()
        self.labelDatabaseDetailsInfo.setText('\n')
        self.labelDatabaseDetailsInfo.setWordWrap(True)
        self.layoutDatabaseDetailsInfo.addWidget(self.labelDatabaseDetailsInfo)
        
        self.labelProjectName = QtGui.QLabel()
        self.labelProjectName.setText('Project &name:')
        self.layoutDatabaseDetails.addWidget(self.labelProjectName, 0, 0)
        
        self.lineEditProjectName = QtGui.QLineEdit()
        self.lineEditProjectName.setText('project_name')
        self.layoutDatabaseDetails.addWidget(self.lineEditProjectName, 0, 1)
        
        self.labelProjectName.setBuddy(self.lineEditProjectName)
        
        self.labelOutputFolder = QtGui.QLabel()
        self.labelOutputFolder.setText('Output folder:')
        self.layoutDatabaseDetails.addWidget(self.labelOutputFolder, 1, 0)
        
        self.lineEditOutputFolder = QtGui.QLineEdit()
        self.lineEditOutputFolder.setReadOnly(True)
        self.lineEditOutputFolder.setText(self.main.appSettings['DialogLumensCreateDatabase']['outputFolder'])
        self.layoutDatabaseDetails.addWidget(self.lineEditOutputFolder, 1, 1)
        
        self.buttonSelectOutputFolder = QtGui.QPushButton()
        self.buttonSelectOutputFolder.setText('&Browse')
        self.layoutDatabaseDetails.addWidget(self.buttonSelectOutputFolder, 1, 2)
        
        self.labelShapefile = QtGui.QLabel()
        self.labelShapefile.setText('Project boundary:')
        self.layoutDatabaseDetails.addWidget(self.labelShapefile, 2, 0)
        
        self.lineEditShapefile = QtGui.QLineEdit()
        self.lineEditShapefile.setReadOnly(True)
        self.layoutDatabaseDetails.addWidget(self.lineEditShapefile, 2, 1)
        
        self.buttonSelectShapefile = QtGui.QPushButton()
        self.buttonSelectShapefile.setText('&Browse')
        self.layoutDatabaseDetails.addWidget(self.buttonSelectShapefile, 2, 2)
        
        self.labelShapefileAttr = QtGui.QLabel()
        self.labelShapefileAttr.setText('Boundary &attribute:')
        self.layoutDatabaseDetails.addWidget(self.labelShapefileAttr, 3, 0)
        
        self.comboBoxShapefileAttr = QtGui.QComboBox()
        self.comboBoxShapefileAttr.setDisabled(True)
        self.layoutDatabaseDetails.addWidget(self.comboBoxShapefileAttr, 3, 1)
        
        self.labelShapefileAttr.setBuddy(self.comboBoxShapefileAttr)
        
        self.labelProjectDescription = QtGui.QLabel()
        self.labelProjectDescription.setText('&Description:')
        self.layoutDatabaseDetails.addWidget(self.labelProjectDescription, 4, 0)
        
        self.lineEditProjectDescription = QtGui.QLineEdit()
        self.lineEditProjectDescription.setText('description')
        self.layoutDatabaseDetails.addWidget(self.lineEditProjectDescription, 4, 1)
        
        self.labelProjectDescription.setBuddy(self.lineEditProjectDescription)
        
        self.labelProjectLocation = QtGui.QLabel()
        self.labelProjectLocation.setText('&Location:')
        self.layoutDatabaseDetails.addWidget(self.labelProjectLocation, 5, 0)
        
        self.lineEditProjectLocation = QtGui.QLineEdit()
        self.lineEditProjectLocation.setText('location')
        self.layoutDatabaseDetails.addWidget(self.lineEditProjectLocation, 5, 1)
        
        self.labelProjectLocation.setBuddy(self.lineEditProjectLocation)
        
        self.labelProjectProvince = QtGui.QLabel()
        self.labelProjectProvince.setText('&Province:')
        self.layoutDatabaseDetails.addWidget(self.labelProjectProvince, 6, 0)
        
        self.lineEditProjectProvince = QtGui.QLineEdit()
        self.lineEditProjectProvince.setText('province')
        self.layoutDatabaseDetails.addWidget(self.lineEditProjectProvince, 6, 1)
        
        self.labelProjectProvince.setBuddy(self.lineEditProjectProvince)
        
        self.labelProjectCountry = QtGui.QLabel()
        self.labelProjectCountry.setText('&Country:')
        self.layoutDatabaseDetails.addWidget(self.labelProjectCountry, 7, 0)
        
        self.lineEditProjectCountry = QtGui.QLineEdit()
        self.lineEditProjectCountry.setText('country')
        self.layoutDatabaseDetails.addWidget(self.lineEditProjectCountry, 7, 1)
        
        self.labelProjectCountry.setBuddy(self.lineEditProjectCountry)
        
        self.labelProjectSpatialRes = QtGui.QLabel()
        self.labelProjectSpatialRes.setText('Spatial &resolution:')
        self.layoutDatabaseDetails.addWidget(self.labelProjectSpatialRes, 8, 0)
        
        self.spinBoxProjectSpatialRes = QtGui.QSpinBox()
        self.spinBoxProjectSpatialRes.setRange(1, 9999)
        self.spinBoxProjectSpatialRes.setValue(100)
        self.layoutDatabaseDetails.addWidget(self.spinBoxProjectSpatialRes, 8, 1)
        
        self.labelProjectSpatialRes.setBuddy(self.spinBoxProjectSpatialRes)
        
        #######################################################################
        # 'Dissolved' GroupBox
        self.groupBoxDissolved = QtGui.QGroupBox('Dissolved')
        self.layoutGroupBoxDissolved = QtGui.QVBoxLayout()
        self.layoutGroupBoxDissolved.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxDissolved.setLayout(self.layoutGroupBoxDissolved)
        
        self.layoutDissolvedInfo = QtGui.QVBoxLayout()
        self.labelDissolvedInfo = QtGui.QLabel()
        self.labelDissolvedInfo.setText('\n')
        self.labelDissolvedInfo.setWordWrap(True)
        self.layoutDissolvedInfo.addWidget(self.labelDissolvedInfo)
        
        self.tableDissolved = QtGui.QTableWidget()
        self.tableDissolved.setDisabled(True)
        self.tableDissolved.verticalHeader().setVisible(False)
        
        self.layoutGroupBoxDissolved.addLayout(self.layoutDissolvedInfo)
        self.layoutGroupBoxDissolved.addWidget(self.tableDissolved)
        
        #######################################################################
        # Dialog buttons
        self.layoutButtonProcess = QtGui.QHBoxLayout()
        self.buttonProcessDissolve = QtGui.QPushButton()
        self.buttonProcessDissolve.setText('&Dissolve')
        self.buttonProcessCreateDatabase = QtGui.QPushButton()
        self.buttonProcessCreateDatabase.setDisabled(True)
        self.buttonProcessCreateDatabase.setText('&Create')
        icon = QtGui.QIcon(':/ui/icons/iconActionHelp.png')
        self.buttonCreateHelp = QtGui.QPushButton()
        self.buttonCreateHelp.setIcon(icon)
        self.layoutButtonProcess.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonProcess.addWidget(self.buttonProcessDissolve)
        self.layoutButtonProcess.addWidget(self.buttonProcessCreateDatabase)
        self.layoutButtonProcess.addWidget(self.buttonCreateHelp)
        
        self.dialogLayout.addWidget(self.groupBoxDatabaseDetails)
        self.dialogLayout.addWidget(self.groupBoxDissolved)
        self.dialogLayout.addLayout(self.layoutButtonProcess)
        
        self.setLayout(self.dialogLayout)
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(640, 480)
        self.resize(parent.sizeHint())
    
    
    def showEvent(self, event):
        """Overload method that is called when the dialog widget is shown.
        
        Args:
            event (QShowEvent): the show widget event.
        """
        super(DialogLumensCreateDatabase, self).showEvent(event)
        self.loadSelectedVectorLayer()
    
    
    def closeEvent(self, event):
        """Overload method that is called when the dialog widget is closed.
        
        Args:
            event (QCloseEvent): the close widget event.
        """
        super(DialogLumensCreateDatabase, self).closeEvent(event)
    
    
    def loadSelectedVectorLayer(self):
        """Load the attributes of the selected layer in the layer list into the shapefile attribute combobox.
        """
        selectedIndexes = self.main.layerListView.selectedIndexes()
        
        if not selectedIndexes:
            return
        
        layerItemIndex = selectedIndexes[0]
        layerItem = self.main.layerListModel.itemFromIndex(layerItemIndex)
        layerItemData = layerItem.data()
        
        if layerItemData['layerType'] == 'vector':
            provider = self.main.qgsLayerList[layerItemData['layer']].dataProvider()
            
            if not provider.isValid():
                logging.getLogger(type(self).__name__).error('invalid shapefile')
                return
            
            attributes = []
            for field in provider.fields():
                attributes.append(field.name())
            
            self.lineEditShapefile.setText(layerItemData['layerFile'])
            
            self.comboBoxShapefileAttr.clear()
            self.comboBoxShapefileAttr.addItems(sorted(attributes))
            self.comboBoxShapefileAttr.setEnabled(True)
    
    
    #***********************************************************
    # 'Create Database' QPushButton handlers
    #***********************************************************
    def handlerSelectOutputFolder(self):
        """Slot method for a folder select dialog to select a folder as output dir.
        """
        outputFolder = unicode(QtGui.QFileDialog.getExistingDirectory(self, 'Select Output Folder'))
        
        if outputFolder:
            self.lineEditOutputFolder.setText(outputFolder)
            
            logging.getLogger(type(self).__name__).info('select output folder: %s', outputFolder)
    
    
    def handlerSelectShapefile(self):
        """Slot method for a file select dialog to select a .shp file and load the attributes in the shapefile attribute combobox.
        """
        shapefile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Shapefile', QtCore.QDir.homePath(), 'Shapefile (*{0})'.format(self.main.appSettings['selectShapefileExt'])))
        
        if shapefile:
            self.lineEditShapefile.setText(shapefile)
            
            registry = QgsProviderRegistry.instance()
            provider = registry.provider('ogr', shapefile)
            
            if not provider.isValid():
                logging.getLogger(type(self).__name__).error('select shapefile: invalid shapefile')
                return
            
            attributes = []
            for field in provider.fields():
                attributes.append(field.name())
            
            self.comboBoxShapefileAttr.clear()
            self.comboBoxShapefileAttr.addItems(sorted(attributes))
            self.comboBoxShapefileAttr.setEnabled(True)
            
            # If dissolve has been run but the shapefile is change, disable the create database button
            if self.dissolvedShapefile:
                self.buttonProcessCreateDatabase.setDisabled(True)
            
            logging.getLogger(type(self).__name__).info('select shapefile: %s', shapefile)
    
    
    #***********************************************************
    # Process dialog
    #***********************************************************
    def setAppSettings(self):
        """Set the required values from the form widgets.
        """
        self.main.appSettings[type(self).__name__]['projectName'] = unicode(self.lineEditProjectName.text())
        # BUG in R script execution? outputFolder path separator must be forward slash
        self.main.appSettings[type(self).__name__]['outputFolder'] = unicode(self.lineEditOutputFolder.text()).replace(os.path.sep, '/')
        self.main.appSettings[type(self).__name__]['shapefile'] = unicode(self.lineEditShapefile.text())
        
        # After dissolving, use dissolved shapefile instead
        if self.dissolvedShapefile:
            self.main.appSettings[type(self).__name__]['dissolvedShapefile'] = self.dissolvedShapefile
        else:
            self.main.appSettings[type(self).__name__]['dissolvedShapefile'] = 'UNSET'
        
        self.main.appSettings[type(self).__name__]['shapefileAttr'] = unicode(self.comboBoxShapefileAttr.currentText())
        self.main.appSettings[type(self).__name__]['projectDescription'] = unicode(self.lineEditProjectDescription.text())
        self.main.appSettings[type(self).__name__]['projectLocation'] = unicode(self.lineEditProjectLocation.text())
        self.main.appSettings[type(self).__name__]['projectProvince'] = unicode(self.lineEditProjectProvince.text())
        self.main.appSettings[type(self).__name__]['projectCountry'] = unicode(self.lineEditProjectCountry.text())
        self.main.appSettings[type(self).__name__]['projectSpatialRes'] = self.spinBoxProjectSpatialRes.value()
    
    
    def getDissolvedTableCsv(self, forwardDirSeparator=False):
        """Method for writing the dissolved table to a temp csv file. Inspired from DialogLumensViewer.
        
        Args:
            forwardDirSeparator (bool): return the temp csv file path with forward slash dir separator.
        """
        rowCount = self.tableDissolved.rowCount()
        columnCount = self.tableDissolved.columnCount()
        
        # Check table first
        if not rowCount:
            QtGui.QMessageBox.critical(self, 'Error', 'Invalid dissolved table!')
            return False
        
        # Now write the table csv
        handle, csvFilePath = tempfile.mkstemp(suffix='.csv')
        
        with os.fdopen(handle, 'w') as f:
            writer = csv.writer(f)
            
            headerItems = []
            
            # Loop columns and write table header
            for tableColumn in range(columnCount):    
                headerItem = self.tableDissolved.horizontalHeaderItem(tableColumn)
                headerItems.append(headerItem.text())
            
            writer.writerow(headerItems)
            
            # Loop rows and write table body
            for tableRow in range(rowCount):
                dataRow = []
                
                # Loop row columns
                for tableColumn in range(columnCount):
                    item = self.tableDissolved.item(tableRow, tableColumn)
                    dataRow.append(item.text())
                
                writer.writerow(dataRow)
        
        if forwardDirSeparator:
            return csvFilePath.replace(os.path.sep, '/')
        
        return csvFilePath
    
    
    def handlerProcessDissolve(self):
        """Slot method to pass the form values and execute the "Dissolve" R algorithm.
        
        The "Dissolve" process calls the following algorithm:
        1. r:lumensdissolve
        """
        self.setAppSettings()
        
        if self.validForm():
            logging.getLogger(type(self).__name__).info('start: %s' % 'LUMENS Dissolve')
            
            self.buttonProcessDissolve.setDisabled(True)
            
            algName = 'r:dbdissolve'
            
            # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
            # self.main.setWindowState(QtCore.Qt.WindowMinimized)
            
            outputs = general.runalg(
                algName,
                self.main.appSettings[type(self).__name__]['shapefile'],
                self.main.appSettings[type(self).__name__]['shapefileAttr'],
                None,
            )
            
            # Display ROut file in debug mode
            if self.main.appSettings['debug']:
                dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                dialog.exec_()
            
            if outputs and os.path.exists(outputs['admin_output']):
                self.dissolvedShapefile = outputs['admin_output'] # To be processed in setAppSettings()
                
                registry = QgsProviderRegistry.instance()
                provider = registry.provider('ogr', outputs['admin_output'])
                
                if not provider.isValid():
                    logging.getLogger(type(self).__name__).error('LUMENS Dissolve: invalid shapefile')
                    return
                
                attributes = []
                for field in provider.fields():
                    attributes.append(field.name())
                
                features = provider.getFeatures()
                
                if features:
                    self.tableDissolved.setEnabled(True)
                    self.tableDissolved.setRowCount(provider.featureCount())
                    self.tableDissolved.setColumnCount(len(attributes))
                    self.tableDissolved.verticalHeader().setVisible(False)
                    self.tableDissolved.setHorizontalHeaderLabels(attributes)
                    
                    # Need a nicer way than manual looping
                    tableRow = 0
                    for feature in features:
                        tableColumn = 0
                        for attribute in attributes:
                            attributeValue = str(feature.attribute(attribute))
                            attributeValueTableItem = QtGui.QTableWidgetItem(attributeValue)
                            self.tableDissolved.setItem(tableRow, tableColumn, attributeValueTableItem)
                            self.tableDissolved.horizontalHeader().setResizeMode(tableColumn, QtGui.QHeaderView.ResizeToContents)
                            tableColumn += 1
                        tableRow += 1
                    
                    self.buttonProcessCreateDatabase.setEnabled(True)
            
            # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
            # self.main.setWindowState(QtCore.Qt.WindowActive)
            
            self.buttonProcessDissolve.setEnabled(True)
            logging.getLogger(type(self).__name__).info('end: %s' % 'LUMENS Dissolve')
    
    
    def handlerProcessCreateDatabase(self):
        """Slot method to pass the form values and execute the "Create Database" R algorithms.
        
        Upon successful completion of the algorithms the new project database will be opened
        and the dialog will close. The "Create Database" process calls the following algorithm:
        1. modeler:lumens_create_database
        """
        self.setAppSettings()
        
        dissolvedTableCsv = self.getDissolvedTableCsv(True)
        
        if self.validForm() and dissolvedTableCsv:
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            
            self.buttonProcessCreateDatabase.setDisabled(True)
            
            algName = 'r:dbcreate'
            
            # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
            # self.main.setWindowState(QtCore.Qt.WindowMinimized)
            
            outputs = general.runalg(
                algName,
                self.main.appSettings[type(self).__name__]['projectName'],
                self.main.appSettings[type(self).__name__]['outputFolder'],
                self.main.appSettings[type(self).__name__]['projectDescription'],
                self.main.appSettings[type(self).__name__]['projectLocation'],
                self.main.appSettings[type(self).__name__]['projectProvince'],
                self.main.appSettings[type(self).__name__]['projectCountry'],
                self.main.appSettings[type(self).__name__]['dissolvedShapefile'],
                self.main.appSettings[type(self).__name__]['shapefileAttr'],
                self.main.appSettings[type(self).__name__]['projectSpatialRes'],
                dissolvedTableCsv,
                None,
            )
            
            # Display ROut file in debug mode
            if self.main.appSettings['debug']:
                dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                dialog.exec_()
            
            # Construct the project .lpj filepath
            lumensDatabase = os.path.join(
                self.main.appSettings[type(self).__name__]['outputFolder'],
                self.main.appSettings[type(self).__name__]['projectName'],
                "{0}{1}".format(self.main.appSettings[type(self).__name__]['projectName'], self.main.appSettings['selectProjectfileExt'])
            )
            
            # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
            # self.main.setWindowState(QtCore.Qt.WindowActive)
            
            algSuccess = self.outputsMessageBox(algName, outputs, 'LUMENS database successfully created!\nClick OK to open the database.', 'Failed to create the LUMENS database.')
            
            self.buttonProcessCreateDatabase.setEnabled(True)
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)

            lumensHTMLReport = os.path.join(
                self.main.appSettings[type(self).__name__]['outputFolder'],
                self.main.appSettings[type(self).__name__]['projectName'],
                "DATA",
                "{0}{1}".format(self.main.appSettings[type(self).__name__]['projectName'], self.main.appSettings['selectHTMLfileExt'])              
            ).replace(os.path.sep, '/')
            
            # If LUMENS database file exists, open it and close this dialog
            if algSuccess and os.path.exists(lumensDatabase):
                self.main.lumensOpenDatabase(lumensDatabase)
                self.close()
                
                if os.path.exists(lumensHTMLReport):
                    dialog = DialogLumensViewer(self, 'LUMENS Create Database Report', 'html', lumensHTMLReport)
                    dialog.exec_()
            else:
                logging.getLogger(type(self).__name__).error('modeler:lumens_create_database failed...')
            
            
