#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from qgis.core import *
from PyQt4 import QtCore, QtGui
from processing.tools import *
from dialog_lumens_viewer import DialogLumensViewer


class DialogLumensImportDatabase(QtGui.QDialog):
    """LUMENS "Import Database" dialog class.
    """
    
    def __init__(self, parent):
        super(DialogLumensImportDatabase, self).__init__(parent)
        
        self.main = parent
        self.dialogTitle = 'LUMENS Import Database'
        
        if self.main.appSettings['debug']:
            print 'DEBUG: DialogLumensImportDatabase init'
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
        
        self.buttonSelectWorkingDir.clicked.connect(self.handlerSelectWorkingDir)
        self.buttonSelectLumensDatabase.clicked.connect(self.handlerSelectLumensDatabase)
        self.buttonProcessImportDatabase.clicked.connect(self.handlerProcessImportDatabase)
    
    
    def setupUi(self, parent):
        """Method for building the dialog UI.
        
        Args:
            parent: the dialog's parent instance.
        """
        self.dialogLayout = QtGui.QVBoxLayout()
        
        self.groupBoxDatabaseDetails = QtGui.QGroupBox('Database details')
        self.layoutGroupBoxDatabaseDetails = QtGui.QVBoxLayout()
        self.layoutGroupBoxDatabaseDetails.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxDatabaseDetails.setLayout(self.layoutGroupBoxDatabaseDetails)
        self.layoutDatabaseDetailsInfo = QtGui.QVBoxLayout()
        self.layoutDatabaseDetails = QtGui.QGridLayout()
        self.layoutGroupBoxDatabaseDetails.addLayout(self.layoutDatabaseDetailsInfo)
        self.layoutGroupBoxDatabaseDetails.addLayout(self.layoutDatabaseDetails)
        
        self.labelDatabaseDetailsInfo = QtGui.QLabel()
        self.labelDatabaseDetailsInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutDatabaseDetailsInfo.addWidget(self.labelDatabaseDetailsInfo)
        
        self.labelWorkingDir = QtGui.QLabel()
        self.labelWorkingDir.setText('Working directory:')
        self.layoutDatabaseDetails.addWidget(self.labelWorkingDir, 0, 0)
        
        self.lineEditWorkingDir = QtGui.QLineEdit()
        self.lineEditWorkingDir.setReadOnly(True)
        self.layoutDatabaseDetails.addWidget(self.lineEditWorkingDir, 0, 1)
        
        self.buttonSelectWorkingDir = QtGui.QPushButton()
        self.buttonSelectWorkingDir.setText('&Browse')
        self.layoutDatabaseDetails.addWidget(self.buttonSelectWorkingDir, 0, 2)
        
        self.labelLumensDatabase = QtGui.QLabel()
        self.labelLumensDatabase.setText('LUMENS database:')
        self.layoutDatabaseDetails.addWidget(self.labelLumensDatabase, 1, 0)
        
        self.lineEditLumensDatabase = QtGui.QLineEdit()
        self.lineEditLumensDatabase.setReadOnly(True)
        self.layoutDatabaseDetails.addWidget(self.lineEditLumensDatabase, 1, 1)
        
        self.buttonSelectLumensDatabase = QtGui.QPushButton()
        self.buttonSelectLumensDatabase.setText('&Browse')
        self.layoutDatabaseDetails.addWidget(self.buttonSelectLumensDatabase, 1, 2)
        
        self.layoutButtonImportDatabase = QtGui.QHBoxLayout()
        self.buttonProcessImportDatabase = QtGui.QPushButton()
        self.buttonProcessImportDatabase.setText('&Process')
        self.layoutButtonImportDatabase.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonImportDatabase.addWidget(self.buttonProcessImportDatabase)
        
        self.dialogLayout.addWidget(self.groupBoxDatabaseDetails)
        self.dialogLayout.addLayout(self.layoutButtonImportDatabase)
        
        self.setLayout(self.dialogLayout)
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(400, 200)
        self.resize(parent.sizeHint())
    
    
    #***********************************************************
    # 'Import Database' QPushButton handlers
    #***********************************************************
    def handlerSelectWorkingDir(self):
        """Slot method for a folder select dialog to select a folder as working dir.
        """
        workingDir = unicode(QtGui.QFileDialog.getExistingDirectory(self, 'Select Working Directory'))
        
        if workingDir:
            self.lineEditWorkingDir.setText(workingDir)
            
            logging.getLogger(type(self).__name__).info('select working directory: %s', workingDir)
    
    
    def handlerSelectLumensDatabase(self):
        """Slot method for a file select dialog to select a LUMENS .lpj project database file.
        """
        projectFile = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select LUMENS Database', QtCore.QDir.homePath(), 'LUMENS Database (*{0})'.format(self.main.appSettings['selectProjectfileExt'])))
        
        if projectFile:
            self.lineEditLumensDatabase.setText(projectFile)
            
            logging.getLogger(type(self).__name__).info('select LUMENS database: %s', projectFile)
    
    
    #***********************************************************
    # Process dialog
    #***********************************************************
    def setAppSettings(self):
        """Set the required values from the form widgets.
        """
        # BUG in R script execution? workingDir path separator must be forward slash
        self.main.appSettings[type(self).__name__]['workingDir'] = unicode(self.lineEditWorkingDir.text()).replace(os.path.sep, '/')
        self.main.appSettings[type(self).__name__]['projectFile'] = unicode(self.lineEditLumensDatabase.text())
    
    
    def validForm(self):
        """Method for validating the form values.
        """
        logging.getLogger(type(self).__name__).info('form validate: %s', type(self).__name__)
        logging.getLogger(type(self).__name__).info('form values: %s', self.main.appSettings[type(self).__name__])
        
        valid = True
        
        for key, val in self.main.appSettings[type(self).__name__].iteritems():
            if val == 0: # for values set specific to 0
                continue
            elif not val:
                valid = False
        
        if not valid:
            QtGui.QMessageBox.critical(self, 'Error', 'Missing some input. Please complete the fields.')
        
        return valid
    
    
    def outputsMessageBox(self, algName, outputs, successMessage, errorMessage):
        """Display a messagebox based on the processing result.
        
        Args:
            algName (str): the name of the executed algorithm.
            outputs (dict): the output of the executed algorithm.
            successMessage (str): the success message to be display in a message box.
            errorMessage (str): the error message to be display in a message box.
        """
        if outputs and outputs['statuscode'] == '1':
            QtGui.QMessageBox.information(self, 'Success', successMessage)
            return True
        else:
            statusMessage = '"{0}" failed with status message:'.format(algName)
            
            if outputs and outputs['statusmessage']:
                statusMessage = '{0} {1}'.format(statusMessage, outputs['statusmessage'])
            
            logging.getLogger(type(self).__name__).error(statusMessage)
            QtGui.QMessageBox.critical(self, 'Error', errorMessage)
            return False
    
    
    def handlerProcessImportDatabase(self):
        """Slot method to pass the form values and execute the "Import Database" R algorithm.
        
        Upon successful completion of the algorithms the imported project database will be opened
        and the dialog will close. The "Import Database" process calls the following algorithms:
        1. modeler:lumens_import_database
        """
        self.setAppSettings()
        
        if self.validForm():
            logging.getLogger(type(self).__name__).info('start: %s' % self.dialogTitle)
            self.buttonProcessImportDatabase.setDisabled(True)
            
            algName = 'modeler:lumens_import_database'
            
            # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
            self.main.setWindowState(QtCore.Qt.WindowMinimized)
            
            outputs = general.runalg(
                algName,
                self.main.appSettings[type(self).__name__]['workingDir'],
                self.main.appSettings[type(self).__name__]['projectFile'],
            )
            
            # Display ROut file in debug mode
            if self.main.appSettings['debug']:
                dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                dialog.exec_()
            
            # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
            self.main.setWindowState(QtCore.Qt.WindowActive)
            
            algSuccess = self.outputsMessageBox(algName, outputs, '', '')
            
            self.buttonProcessImportDatabase.setEnabled(True)
            logging.getLogger(type(self).__name__).info('end: %s' % self.dialogTitle)
            
            projectName = os.path.basename(os.path.splitext(self.main.appSettings[type(self).__name__]['projectFile'])[0])
            
            lumensDatabase = os.path.join(
                self.main.appSettings[type(self).__name__]['workingDir'],
                projectName,
                os.path.basename(self.main.appSettings[type(self).__name__]['projectFile'])
            )
            
            # if LUMENS database file exists, open it and close dialog
            if os.path.exists(lumensDatabase):
                self.main.lumensOpenDatabase(lumensDatabase)
                self.close()
            else:
                logging.getLogger(type(self).__name__).error('modeler:lumens_import_database failed...')
            