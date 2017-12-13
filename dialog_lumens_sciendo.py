#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, datetime, glob, tempfile, csv
from qgis.core import *
from processing.tools import *
from PyQt4 import QtCore, QtGui

from utils import QPlainTextEditLogger
from dialog_lumens_base import DialogLumensBase
from dialog_lumens_viewer import DialogLumensViewer
import resource


class DialogLumensSCIENDO(QtGui.QDialog, DialogLumensBase):
    """LUMENS "SCIENDO" module dialog class.
    """
    
    def loadTemplateFiles(self):
        """Method for loading the list of module template files inside the project folder.
        
        This method is also called to load the module template files in the main window dashboard tab.
        """
        templateFiles = [os.path.basename(name) for name in glob.glob(os.path.join(self.settingsPath, '*.ini')) if os.path.isfile(os.path.join(self.settingsPath, name))]
        
        if templateFiles:
            self.comboBoxLowEmissionDevelopmentAnalysisTemplate.clear()
            self.comboBoxLowEmissionDevelopmentAnalysisTemplate.addItems(sorted(templateFiles))
            self.comboBoxLowEmissionDevelopmentAnalysisTemplate.setEnabled(True)
            self.buttonLoadLowEmissionDevelopmentAnalysisTemplate.setEnabled(True)
            
            self.comboBoxCreateRasterCubeTemplate.clear()
            self.comboBoxCreateRasterCubeTemplate.addItems(sorted(templateFiles))
            self.comboBoxCreateRasterCubeTemplate.setEnabled(True)
            self.buttonLoadCreateRasterCubeTemplate.setEnabled(True)
            
            # MainWindow SCIENDO dashboard templates
            self.main.comboBoxLowEmissionDevelopmentAnalysisTemplate.clear()
            self.main.comboBoxLowEmissionDevelopmentAnalysisTemplate.addItems(sorted(templateFiles))
            self.main.comboBoxLowEmissionDevelopmentAnalysisTemplate.setEnabled(True)
            self.main.buttonProcessSCIENDOLowEmissionDevelopmentAnalysisTemplate.setEnabled(True)
            
            # self.main.comboBoxLandUseChangeModelingTemplate.clear()
            # self.main.comboBoxLandUseChangeModelingTemplate.addItems(sorted(templateFiles))
            # self.main.comboBoxLandUseChangeModelingTemplate.setEnabled(True)
            # self.main.buttonProcessSCIENDOLandUseChangeModelingTemplate.setEnabled(True)
        else:
            self.comboBoxLowEmissionDevelopmentAnalysisTemplate.setDisabled(True)
            self.buttonLoadLowEmissionDevelopmentAnalysisTemplate.setDisabled(True)
            
            self.comboBoxCreateRasterCubeTemplate.setDisabled(True)
            self.buttonLoadCreateRasterCubeTemplate.setDisabled(True)
            
            # MainWindow SCIENDO dashboard templates
            self.main.comboBoxLowEmissionDevelopmentAnalysisTemplate.setDisabled(True)
            self.main.buttonProcessSCIENDOLowEmissionDevelopmentAnalysisTemplate.setDisabled(True)
            
            # self.main.comboBoxLandUseChangeModelingTemplate.setDisabled(True)
            # self.main.buttonProcessSCIENDOLandUseChangeModelingTemplate.setDisabled(True)
    
    
    def loadTemplate(self, tabName, fileName, returnTemplateSettings=False):
        """Method for loading the values saved in the module template file to the form widgets.
        
        Args:
            tabName (str): the tab where the form widget values will be populated.
            templateFile (str): a file path to the template file that will be loaded.
            returnTemplateSettings (bool): if true return a dict of the settings in the template file.
        """
        templateFilePath = os.path.join(self.settingsPath, fileName)
        settings = QtCore.QSettings(templateFilePath, QtCore.QSettings.IniFormat)
        settings.setFallbacksEnabled(True) # only use ini files
        
        templateSettings = {}
        dialogsToLoad = None
        
        td = datetime.date.today()
        
        if tabName == 'Low Emission Development Analysis':
            dialogsToLoad = (
                'DialogLumensSCIENDOHistoricalBaselineProjection',
                'DialogLumensSCIENDOHistoricalBaselineAnnualProjection',
                'DialogLumensSCIENDODriversAnalysis',
                'DialogLumensSCIENDOBuildScenario',
            )
            
            # start tab
            settings.beginGroup(tabName)
            
            # 'Historical baseline projection' groupbox widgets
            # start dialog
            settings.beginGroup('DialogLumensSCIENDOHistoricalBaselineProjection')
            
            templateSettings['DialogLumensSCIENDOHistoricalBaselineProjection'] = {}
            templateSettings['DialogLumensSCIENDOHistoricalBaselineProjection']['QUESCDatabase'] = QUESCDatabase = settings.value('QUESCDatabase')
            templateSettings['DialogLumensSCIENDOHistoricalBaselineProjection']['iteration'] = iteration = settings.value('iteration')
            
            if not returnTemplateSettings:
                if QUESCDatabase:
                    indexQUESCDatabase = self.comboBoxHistoricalBaselineProjectionQUESCDatabase.findText(QUESCDatabase)
                    if indexQUESCDatabase != -1:
                        self.comboBoxHistoricalBaselineProjectionQUESCDatabase.setCurrentIndex(indexQUESCDatabase)
                        
                if iteration:
                    self.spinBoxHistoricalBaselineProjectionIteration.setValue(int(iteration))
                else:
                    self.spinBoxHistoricalBaselineProjectionIteration.setValue(5)
            
            settings.endGroup()
            # /dialog
            
            # 'Historical baseline annual projection' groupbox widgets
            # start dialog
            settings.beginGroup('DialogLumensSCIENDOHistoricalBaselineAnnualProjection')
            
            templateSettings['DialogLumensSCIENDOHistoricalBaselineAnnualProjection'] = {}
            templateSettings['DialogLumensSCIENDOHistoricalBaselineAnnualProjection']['iteration'] = iteration = settings.value('iteration')
            
            if not returnTemplateSettings:
                if iteration:
                    self.spinBoxHistoricalBaselineAnnualProjectionIteration.setValue(int(iteration))
                else:
                    self.spinBoxHistoricalBaselineAnnualProjectionIteration.setValue(5)
            
            settings.endGroup()
            # /dialog
            
            # 'Drivers analysis' groupbox widgets
            # start dialog
            settings.beginGroup('DialogLumensSCIENDODriversAnalysis')
            
            templateSettings['DialogLumensSCIENDODriversAnalysis'] = {}
            templateSettings['DialogLumensSCIENDODriversAnalysis']['landUseCoverChangeDrivers'] = landUseCoverChangeDrivers = settings.value('landUseCoverChangeDrivers')
            templateSettings['DialogLumensSCIENDODriversAnalysis']['landUseCoverChangeType'] = landUseCoverChangeType = settings.value('landUseCoverChangeType')
            
            if not returnTemplateSettings:
                if landUseCoverChangeDrivers and os.path.exists(landUseCoverChangeDrivers):
                    self.lineEditDriversAnalysisLandUseCoverChangeDrivers.setText(landUseCoverChangeDrivers)
                else:
                    self.lineEditDriversAnalysisLandUseCoverChangeDrivers.setText('')
                if landUseCoverChangeType:
                    self.lineEditDriversAnalysisLandUseCoverChangeType.setText(landUseCoverChangeType)
                else:
                    self.lineEditDriversAnalysisLandUseCoverChangeType.setText('Land use change')
            
            settings.endGroup()
            # /dialog
            
            # 'Build scenario' groupbox widgets
            # start dialog
            settings.beginGroup('DialogLumensSCIENDOBuildScenario')
            
            templateSettings['DialogLumensSCIENDOBuildScenario'] = {}
            templateSettings['DialogLumensSCIENDOBuildScenario']['historicalBaselineCar'] = historicalBaselineCar = settings.value('historicalBaselineCar')
            
            if not returnTemplateSettings:
                if historicalBaselineCar and os.path.exists(historicalBaselineCar):
                    self.lineEditBuildScenarioHistoricalBaselineCar.setText(historicalBaselineCar)
                else:
                    self.lineEditBuildScenarioHistoricalBaselineCar.setText('')
            
            if not returnTemplateSettings:
                self.currentLowEmissionDevelopmentAnalysisTemplate = templateFile
                self.loadedLowEmissionDevelopmentAnalysisTemplate.setText(templateFile)
                self.comboBoxLowEmissionDevelopmentAnalysisTemplate.setCurrentIndex(self.comboBoxLowEmissionDevelopmentAnalysisTemplate.findText(templateFile))
                self.buttonSaveLowEmissionDevelopmentAnalysisTemplate.setEnabled(True)
            
            settings.endGroup()
            # /dialog
            
            settings.endGroup()
            # /tab
        elif tabName == 'Land Use Change Modeling':
            dialogsToLoad = (
                'DialogLumensSCIENDOCalculateTransitionMatrix',
            )
            
            # start tab
            settings.beginGroup(tabName)
            
            # 'Land Use Change Modeling' tab widgets
            # start dialog
            settings.beginGroup('DialogLumensSCIENDOCalculateTransitionMatrix')
            
            templateSettings['DialogLumensSCIENDOCalculateTransitionMatrix'] = {}
            templateSettings['DialogLumensSCIENDOCalculateTransitionMatrix']['factorsDir'] = factorsDir = settings.value('factorsDir')
            templateSettings['DialogLumensSCIENDOCalculateTransitionMatrix']['landUseLookup'] = landUseLookup = settings.value('landUseLookup')
            templateSettings['DialogLumensSCIENDOCalculateTransitionMatrix']['baseYear'] = baseYear = settings.value('baseYear')
            templateSettings['DialogLumensSCIENDOCalculateTransitionMatrix']['location'] = location = settings.value('location')
            
            if not returnTemplateSettings:
                if factorsDir and os.path.isdir(factorsDir):
                    self.lineEditLandUseChangeModelingFactorsDir.setText(factorsDir)
                else:
                    self.lineEditLandUseChangeModelingFactorsDir.setText('')
                if landUseLookup and os.path.exists(landUseLookup):
                    self.lineEditLandUseChangeModelingLandUseLookup.setText(landUseLookup)
                else:
                    self.lineEditLandUseChangeModelingLandUseLookup.setText('')
                if baseYear:
                    self.spinBoxLandUseChangeModelingBaseYear.setValue(int(baseYear))
                else:
                    self.spinBoxLandUseChangeModelingBaseYear.setValue(td.year)
                if location:
                    self.lineEditLandUseChangeModelingLocation.setText(location)
                else:
                    self.lineEditLandUseChangeModelingLocation.setText('location')
                
                self.currentLandUseChangeModelingTemplate = templateFile
                self.loadedLandUseChangeModelingTemplate.setText(templateFile)
                self.comboBoxLandUseChangeModelingTemplate.setCurrentIndex(self.comboBoxLandUseChangeModelingTemplate.findText(templateFile))
                self.buttonSaveLandUseChangeModelingTemplate.setEnabled(True)
            
            settings.endGroup()
            # /dialog
            
            settings.endGroup()
            # /tab
        
        if returnTemplateSettings:
            return templateSettings
        else:
            # Log to history log
            logging.getLogger(self.historyLog).info('Loaded template: %s', templateFile)
    
    
    def checkForDuplicateTemplates(self, tabName, templateToSkip):
        """Method for checking whether the new template values to be saved already exists in a saved template file.
        
        Args:
            tabName (str): the tab to be checked.
            templateToSkip (str): the template file to skip (when saving an existing template file).
        """
        duplicateTemplate = None
        templateFiles = [os.path.basename(name) for name in glob.glob(os.path.join(self.settingsPath, '*.ini')) if os.path.isfile(os.path.join(self.settingsPath, name))]
        dialogsToLoad = None
        
        if tabName == 'Low Emission Development Analysis':
            dialogsToLoad = (
                'DialogLumensSCIENDOHistoricalBaselineProjection',
                'DialogLumensSCIENDOHistoricalBaselineAnnualProjection',
                'DialogLumensSCIENDODriversAnalysis',
                'DialogLumensSCIENDOBuildScenario',
            )
        elif tabName == 'Land Use Change Modeling':
            dialogsToLoad = (
                'DialogLumensSCIENDOCalculateTransitionMatrix',
            )
        
        for templateFile in templateFiles:
            if templateFile == templateToSkip:
                continue
            
            duplicateTemplate = templateFile
            templateSettings = self.loadTemplate(tabName, templateFile, True)
            
            print 'DEBUG'
            print templateFile, templateSettings
            
            # Loop thru all dialogs in a tab
            for dialog in dialogsToLoad:
                # Loop thru all settings in a dialog
                for key, val in self.main.appSettings[dialog].iteritems():
                    if templateSettings[dialog][key] != val:
                        # A setting doesn't match! This is not a matching template file, move along
                        duplicateTemplate = None
                    else:
                        print 'DEBUG equal settings'
                        print templateSettings[dialog][key], val
        
        # Found a duplicate template, offer to load it?
        if duplicateTemplate:
            reply = QtGui.QMessageBox.question(
                self,
                'Load Existing Template',
                'The template you are about to save matches an existing template.\nDo you want to load \'{0}\' instead?'.format(duplicateTemplate),
                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                QtGui.QMessageBox.No
            )
            
            if reply == QtGui.QMessageBox.Yes:
                if tabName == 'Low Emission Development Analysis':
                    self.handlerLoadLowEmissionDevelopmentAnalysisTemplate(duplicateTemplate)
                elif tabName == 'Land Use Change Modeling':
                    self.handlerLoadLandUseChangeModelingTemplate(duplicateTemplate)
                
                return True
        
        return False
    
    
    def saveTemplate(self, tabName, fileName):
        """Method for saving the form values based on the associated tab and dialog to a template file.
        
        Args:
            tabName (str): the tab with the form values to save.
            fileName (str): the target template file name to create.
        """
        self.setAppSettings()
        
        # Check if current form values duplicate an existing template
        if not self.checkForDuplicateTemplates(tabName, fileName):
            templateFilePath = os.path.join(self.main.appSettings['DialogLumensOpenDatabase']['projectFolder'], self.main.appSettings['folderSCIENDO'], fileName)
            settings = QtCore.QSettings(templateFilePath, QtCore.QSettings.IniFormat)
            settings.setFallbacksEnabled(True) # only use ini files
            
            dialogsToSave = None
            
            if tabName == 'Low Emission Development Analysis':
                dialogsToSave = (
                    'DialogLumensSCIENDOHistoricalBaselineProjection',
                    'DialogLumensSCIENDOHistoricalBaselineAnnualProjection',
                    'DialogLumensSCIENDODriversAnalysis',
                    'DialogLumensSCIENDOBuildScenario',
                )
            elif tabName == 'Land Use Change Modeling':
                dialogsToSave = (
                    'DialogLumensSCIENDOCalculateTransitionMatrix',
                )
            
            settings.beginGroup(tabName)
            for dialog in dialogsToSave:
                settings.beginGroup(dialog)
                for key, val in self.main.appSettings[dialog].iteritems():
                    settings.setValue(key, val)
                settings.endGroup()
            settings.endGroup()
            
            # Log to history log
            logging.getLogger(self.historyLog).info('Saved template: %s', fileName)
    
    
    def __init__(self, parent):
        super(DialogLumensSCIENDO, self).__init__(parent)
        
        self.main = parent
        self.dialogTitle = 'SCIENDO'
        self.checkBoxQUESCDatabaseCount = 0
        self.tableAddFactorRowCount = 0
        self.listOfQUESCDatabase = []
        self.settingsPath = os.path.join(self.main.appSettings['DialogLumensOpenDatabase']['projectFolder'], self.main.appSettings['folderSCIENDO'])
        self.currentLowEmissionDevelopmentAnalysisTemplate = None
        self.currentLandUseChangeModelingTemplate = None
        
        # Init logging
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        if self.main.appSettings['debug']:
            print 'DEBUG: DialogLumensSCIENDO init'
            self.logger = logging.getLogger(type(self).__name__)
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            fh = logging.FileHandler(os.path.join(self.main.appSettings['appDir'], 'logs', type(self).__name__ + '.log'))
            fh.setFormatter(formatter)
            self.logger.addHandler(ch)
            self.logger.addHandler(fh)
            self.logger.setLevel(logging.DEBUG)
        
        self.setupUi(self)
        
        # History log
        self.historyLog = '{0}{1}'.format('history', type(self).__name__)
        self.historyLogPath = os.path.join(self.settingsPath, self.historyLog + '.log')
        self.historyLogger = logging.getLogger(self.historyLog)
        fh = logging.FileHandler(self.historyLogPath)
        fh.setFormatter(formatter)
        self.log_box.setFormatter(formatter)
        self.historyLogger.addHandler(fh)
        self.historyLogger.addHandler(self.log_box)
        self.historyLogger.setLevel(logging.INFO)
        
        self.loadHistoryLog()
        
        self.loadTemplateFiles()
        
        self.tabWidget.currentChanged.connect(self.handlerTabWidgetChanged)
        
        # 'Low Emission Development Analysis' tab checkboxes
        self.checkBoxHistoricalBaselineProjection.toggled.connect(self.toggleHistoricalBaselineProjection)
        self.checkBoxHistoricalBaselineAnnualProjection.toggled.connect(self.toggleHistoricalBaselineAnnualProjection)
        self.checkBoxDriversAnalysis.toggled.connect(self.toggleDriversAnalysis)
        self.checkBoxBuildScenario.toggled.connect(self.toggleBuildScenario)
        
        # 'Low Emission Development Analysis' tab buttons
        self.buttonSelectDriversAnalysisLandUseCoverChangeDrivers.clicked.connect(self.handlerSelectDriversAnalysisLandUseCoverChangeDrivers)
        self.buttonSelectBuildScenarioHistoricalBaselineCar.clicked.connect(self.handlerSelectBuildScenarioHistoricalBaselineCar)
        self.buttonProcessLowEmissionDevelopmentAnalysis.clicked.connect(self.handlerProcessLowEmissionDevelopmentAnalysis)
        self.buttonHelpSCIENDOLowEmissionDevelopmentAnalysis.clicked.connect(lambda:self.handlerDialogHelp('SCIENDO'))
        self.buttonLoadLowEmissionDevelopmentAnalysisTemplate.clicked.connect(self.handlerLoadLowEmissionDevelopmentAnalysisTemplate)
        self.buttonSaveLowEmissionDevelopmentAnalysisTemplate.clicked.connect(self.handlerSaveLowEmissionDevelopmentAnalysisTemplate)
        self.buttonSaveAsLowEmissionDevelopmentAnalysisTemplate.clicked.connect(self.handlerSaveAsLowEmissionDevelopmentAnalysisTemplate)
        
        # 'Land Use Change Modeling' tab buttons
        self.buttonAddFactorRow.clicked.connect(self.handlerButtonAddFactorRow)
        self.buttonSelectLandUseChangeModelingFactorsDir.clicked.connect(self.handlerSelectLandUseChangeModelingFactorsDir)
        self.buttonSelectLandUseChangeModelingLandUseLookup.clicked.connect(self.handlerSelectLandUseChangeModelingLandUseLookup)
        self.buttonProcessCreateRasterCube.clicked.connect(self.handlerProcessLandUseChangeModeling)
        self.buttonHelpSCIENDOCreateRasterCube.clicked.connect(lambda:self.handlerDialogHelp('SCIENDO'))
        #self.buttonLoadLandUseChangeModelingTemplate.clicked.connect(self.handlerLoadLandUseChangeModelingTemplate)
        #self.buttonSaveLandUseChangeModelingTemplate.clicked.connect(self.handlerSaveLandUseChangeModelingTemplate)
        #self.buttonSaveAsLandUseChangeModelingTemplate.clicked.connect(self.handlerSaveAsLandUseChangeModelingTemplate)
    
    
    def setupUi(self, parent):
        """Method for building the dialog UI.
        
        Args:
            parent: the dialog's parent instance.
        """
        self.setStyleSheet('QDialog { background-color: rgb(225, 229, 237); } QMessageBox QLabel{ color: #fff; }')
        self.dialogLayout = QtGui.QVBoxLayout()

        self.groupBoxSCIENDODialog = QtGui.QGroupBox('Scenario simulation and development')
        self.layoutGroupBoxSCIENDODialog = QtGui.QVBoxLayout()
        self.layoutGroupBoxSCIENDODialog.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxSCIENDODialog.setLayout(self.layoutGroupBoxSCIENDODialog)
        self.labelSCIENDODialogInfo = QtGui.QLabel()
        self.labelSCIENDODialogInfo.setText('\n')
        self.labelSCIENDODialogInfo.setWordWrap(True)
        self.layoutGroupBoxSCIENDODialog.addWidget(self.labelSCIENDODialogInfo)

        self.tabWidget = QtGui.QTabWidget()
        tabWidgetStylesheet = """
        QTabWidget::pane {
            border: none;
            background-color: rgb(244, 248, 252);
        }
        QTabBar::tab {
            background-color: rgb(174, 176, 178);
            color: rgb(95, 98, 102);
            height: 35px; 
            width: 200px;  
            font-size: 13px;                 
        }
        QTabBar::tab:selected, QTabBar::tab:hover {
            background-color: rgb(244, 248, 252);
            color: rgb(56, 65, 73);
        }
        QTabBar::tab:selected{
            font: bold;
        }        
        """
        self.tabWidget.setStyleSheet(tabWidgetStylesheet)
        
        self.tabLowEmissionDevelopmentAnalysis = QtGui.QWidget()
        self.tabLandUseChangeModeling = QtGui.QWidget()
        self.tabLog = QtGui.QWidget()
        
        self.tabWidget.addTab(self.tabLowEmissionDevelopmentAnalysis, 'Historical baseline analysis')
        self.tabWidget.addTab(self.tabLandUseChangeModeling, 'Land use simulation')
        self.tabWidget.addTab(self.tabLog, 'Log')
        
        ###self.layoutTabLowEmissionDevelopmentAnalysis = QtGui.QVBoxLayout()
        self.layoutTabLowEmissionDevelopmentAnalysis = QtGui.QGridLayout()
        self.layoutTabLandUseChangeModeling = QtGui.QVBoxLayout()
        ##self.layoutTabLandUseChangeModeling = QtGui.QGridLayout()
        self.layoutTabLog = QtGui.QVBoxLayout()
        
        self.tabLowEmissionDevelopmentAnalysis.setLayout(self.layoutTabLowEmissionDevelopmentAnalysis)
        self.tabLandUseChangeModeling.setLayout(self.layoutTabLandUseChangeModeling)
        self.tabLog.setLayout(self.layoutTabLog)

        self.dialogLayout.addWidget(self.groupBoxSCIENDODialog)
        self.dialogLayout.addWidget(self.tabWidget)
        
        #***********************************************************
        # Setup 'Low Emission Development Analysis' tab
        #***********************************************************
        # 'Historical baseline projection' GroupBox
        self.groupBoxHistoricalBaselineProjection = QtGui.QGroupBox('Periodic projection parameter')
        self.layoutGroupBoxHistoricalBaselineProjection = QtGui.QHBoxLayout()
        self.groupBoxHistoricalBaselineProjection.setLayout(self.layoutGroupBoxHistoricalBaselineProjection)
        self.layoutOptionsHistoricalBaselineProjection = QtGui.QVBoxLayout()
        self.layoutOptionsHistoricalBaselineProjection.setContentsMargins(5, 0, 5, 0)
        self.contentOptionsHistoricalBaselineProjection = QtGui.QWidget()
        self.contentOptionsHistoricalBaselineProjection.setLayout(self.layoutOptionsHistoricalBaselineProjection)
        self.layoutOptionsHistoricalBaselineProjection.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.checkBoxHistoricalBaselineProjection = QtGui.QCheckBox()
        self.checkBoxHistoricalBaselineProjection.setChecked(False)
        self.contentOptionsHistoricalBaselineProjection.setDisabled(True)
        self.layoutGroupBoxHistoricalBaselineProjection.addWidget(self.checkBoxHistoricalBaselineProjection)
        self.layoutGroupBoxHistoricalBaselineProjection.addWidget(self.contentOptionsHistoricalBaselineProjection)
        self.layoutGroupBoxHistoricalBaselineProjection.insertStretch(2, 1)
        self.layoutGroupBoxHistoricalBaselineProjection.setAlignment(self.checkBoxHistoricalBaselineProjection, QtCore.Qt.AlignTop)
        self.layoutHistoricalBaselineProjectionInfo = QtGui.QVBoxLayout()
        self.layoutHistoricalBaselineProjection = QtGui.QGridLayout()
        self.layoutOptionsHistoricalBaselineProjection.addLayout(self.layoutHistoricalBaselineProjectionInfo)
        self.layoutOptionsHistoricalBaselineProjection.addLayout(self.layoutHistoricalBaselineProjection)
        
        self.labelHistoricalBaselineProjectionInfo = QtGui.QLabel()
        self.labelHistoricalBaselineProjectionInfo.setText('Conduct periodic projection\n')
        self.layoutHistoricalBaselineProjectionInfo.addWidget(self.labelHistoricalBaselineProjectionInfo)
        
        self.labelHistoricalBaselineProjectionQUESCDatabase = QtGui.QLabel()
        self.labelHistoricalBaselineProjectionQUESCDatabase.setText('QUES-C Database:')
        self.layoutHistoricalBaselineProjection.addWidget(self.labelHistoricalBaselineProjectionQUESCDatabase, 0, 0)
        
        self.comboBoxHistoricalBaselineProjectionQUESCDatabase = QtGui.QComboBox()
        self.comboBoxHistoricalBaselineProjectionQUESCDatabase.setDisabled(True)
        self.layoutHistoricalBaselineProjection.addWidget(self.comboBoxHistoricalBaselineProjectionQUESCDatabase, 0, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxHistoricalBaselineProjectionQUESCDatabase)
        
        self.labelHistoricalBaselineProjectionIteration = QtGui.QLabel()
        self.labelHistoricalBaselineProjectionIteration.setText('&Iteration:')
        self.layoutHistoricalBaselineProjection.addWidget(self.labelHistoricalBaselineProjectionIteration, 1, 0)
        
        self.spinBoxHistoricalBaselineProjectionIteration = QtGui.QSpinBox()
        self.spinBoxHistoricalBaselineProjectionIteration.setRange(1, 99)
        self.spinBoxHistoricalBaselineProjectionIteration.setValue(3)
        self.layoutHistoricalBaselineProjection.addWidget(self.spinBoxHistoricalBaselineProjectionIteration, 1, 1)
        self.labelHistoricalBaselineProjectionIteration.setBuddy(self.spinBoxHistoricalBaselineProjectionIteration) 
        
        # 'Historical baseline annual projection' GroupBox
        self.groupBoxHistoricalBaselineAnnualProjection = QtGui.QGroupBox('Annual projection parameter')
        self.layoutGroupBoxHistoricalBaselineAnnualProjection = QtGui.QHBoxLayout()
        self.groupBoxHistoricalBaselineAnnualProjection.setLayout(self.layoutGroupBoxHistoricalBaselineAnnualProjection)
        self.layoutOptionsHistoricalBaselineAnnualProjection = QtGui.QVBoxLayout()
        self.layoutOptionsHistoricalBaselineAnnualProjection.setContentsMargins(5, 0, 5, 0)
        self.contentOptionsHistoricalBaselineAnnualProjection = QtGui.QWidget()
        self.contentOptionsHistoricalBaselineAnnualProjection.setLayout(self.layoutOptionsHistoricalBaselineAnnualProjection)
        self.layoutOptionsHistoricalBaselineAnnualProjection.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.checkBoxHistoricalBaselineAnnualProjection = QtGui.QCheckBox()
        self.checkBoxHistoricalBaselineAnnualProjection.setChecked(False)
        self.contentOptionsHistoricalBaselineAnnualProjection.setDisabled(True)
        self.layoutGroupBoxHistoricalBaselineAnnualProjection.addWidget(self.checkBoxHistoricalBaselineAnnualProjection)
        self.layoutGroupBoxHistoricalBaselineAnnualProjection.addWidget(self.contentOptionsHistoricalBaselineAnnualProjection)
        self.layoutGroupBoxHistoricalBaselineAnnualProjection.insertStretch(2, 1)
        self.layoutGroupBoxHistoricalBaselineAnnualProjection.setAlignment(self.checkBoxHistoricalBaselineAnnualProjection, QtCore.Qt.AlignTop)
        self.layoutHistoricalBaselineAnnualProjectionInfo = QtGui.QVBoxLayout()
        self.layoutHistoricalBaselineAnnualProjection = QtGui.QGridLayout()
        self.layoutOptionsHistoricalBaselineAnnualProjection.addLayout(self.layoutHistoricalBaselineAnnualProjectionInfo)
        self.layoutOptionsHistoricalBaselineAnnualProjection.addLayout(self.layoutHistoricalBaselineAnnualProjection)
        
        self.labelHistoricalBaselineAnnualProjectionInfo = QtGui.QLabel()
        self.labelHistoricalBaselineAnnualProjectionInfo.setText('Conduct annual projection\n')
        self.layoutHistoricalBaselineAnnualProjectionInfo.addWidget(self.labelHistoricalBaselineAnnualProjectionInfo)
        
        self.labelHistoricalBaselineAnnualProjectionIteration = QtGui.QLabel()
        self.labelHistoricalBaselineAnnualProjectionIteration.setText('&Iteration:')
        self.layoutHistoricalBaselineAnnualProjection.addWidget(self.labelHistoricalBaselineAnnualProjectionIteration, 0, 0)
        
        self.spinBoxHistoricalBaselineAnnualProjectionIteration = QtGui.QSpinBox()
        self.spinBoxHistoricalBaselineAnnualProjectionIteration.setRange(1, 9999)
        self.spinBoxHistoricalBaselineAnnualProjectionIteration.setValue(5)
        self.layoutHistoricalBaselineAnnualProjection.addWidget(self.spinBoxHistoricalBaselineAnnualProjectionIteration, 0, 1)
        self.labelHistoricalBaselineAnnualProjectionIteration.setBuddy(self.spinBoxHistoricalBaselineAnnualProjectionIteration)
        
        self.populateQUESCDatabase()

        # 'Drivers analysis' GroupBox
        self.groupBoxDriversAnalysis = QtGui.QGroupBox('Drivers analysis parameter')
        self.layoutGroupBoxDriversAnalysis = QtGui.QHBoxLayout()
        self.groupBoxDriversAnalysis.setLayout(self.layoutGroupBoxDriversAnalysis)
        self.layoutOptionsDriversAnalysis = QtGui.QVBoxLayout()
        self.layoutOptionsDriversAnalysis.setContentsMargins(5, 0, 5, 0)
        self.contentOptionsDriversAnalysis = QtGui.QWidget()
        self.contentOptionsDriversAnalysis.setLayout(self.layoutOptionsDriversAnalysis)
        self.layoutOptionsDriversAnalysis.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.checkBoxDriversAnalysis = QtGui.QCheckBox()
        self.checkBoxDriversAnalysis.setChecked(False)
        self.contentOptionsDriversAnalysis.setDisabled(True)
        self.layoutGroupBoxDriversAnalysis.addWidget(self.checkBoxDriversAnalysis)
        self.layoutGroupBoxDriversAnalysis.addWidget(self.contentOptionsDriversAnalysis)
        self.layoutGroupBoxDriversAnalysis.setAlignment(self.checkBoxDriversAnalysis, QtCore.Qt.AlignTop)
        self.layoutDriversAnalysisInfo = QtGui.QVBoxLayout()
        self.layoutDriversAnalysis = QtGui.QGridLayout()
        self.layoutOptionsDriversAnalysis.addLayout(self.layoutDriversAnalysisInfo)
        self.layoutOptionsDriversAnalysis.addLayout(self.layoutDriversAnalysis)
        
        self.labelDriversAnalysisInfo = QtGui.QLabel()
        self.labelDriversAnalysisInfo.setText('Conduct drivers analysis\n')
        self.layoutDriversAnalysisInfo.addWidget(self.labelDriversAnalysisInfo)
        
        self.labelDriversAnalysisLandUseCoverChangeDrivers = QtGui.QLabel()
        self.labelDriversAnalysisLandUseCoverChangeDrivers.setText('Drivers of land use change:')
        self.layoutDriversAnalysis.addWidget(self.labelDriversAnalysisLandUseCoverChangeDrivers, 0, 0)
        
        self.lineEditDriversAnalysisLandUseCoverChangeDrivers = QtGui.QLineEdit()
        self.lineEditDriversAnalysisLandUseCoverChangeDrivers.setReadOnly(True)
        self.layoutDriversAnalysis.addWidget(self.lineEditDriversAnalysisLandUseCoverChangeDrivers, 0, 1)
        
        self.buttonSelectDriversAnalysisLandUseCoverChangeDrivers = QtGui.QPushButton()
        self.buttonSelectDriversAnalysisLandUseCoverChangeDrivers.setText('&Browse')
        self.layoutDriversAnalysis.addWidget(self.buttonSelectDriversAnalysisLandUseCoverChangeDrivers, 0, 2)
        
        self.labelDriversAnalysislandUseCoverChangeType = QtGui.QLabel()
        self.labelDriversAnalysislandUseCoverChangeType.setText('Land use trajectory:')
        self.layoutDriversAnalysis.addWidget(self.labelDriversAnalysislandUseCoverChangeType, 1, 0)
        
        self.lineEditDriversAnalysisLandUseCoverChangeType = QtGui.QLineEdit()
        self.lineEditDriversAnalysisLandUseCoverChangeType.setText('Provide trajectory name')
        self.layoutDriversAnalysis.addWidget(self.lineEditDriversAnalysisLandUseCoverChangeType, 1, 1)
        self.labelDriversAnalysislandUseCoverChangeType.setBuddy(self.lineEditDriversAnalysisLandUseCoverChangeType)
        
        # 'Build scenario' GroupBox
        self.groupBoxBuildScenario = QtGui.QGroupBox('Scenario builder')
        self.layoutGroupBoxBuildScenario = QtGui.QHBoxLayout()
        self.groupBoxBuildScenario.setLayout(self.layoutGroupBoxBuildScenario)
        self.layoutOptionsBuildScenario = QtGui.QVBoxLayout()
        self.layoutOptionsBuildScenario.setContentsMargins(5, 0, 5, 0)
        self.contentOptionsBuildScenario = QtGui.QWidget()
        self.contentOptionsBuildScenario.setLayout(self.layoutOptionsBuildScenario)
        self.layoutOptionsBuildScenario.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.checkBoxBuildScenario = QtGui.QCheckBox()
        self.checkBoxBuildScenario.setChecked(False)
        self.contentOptionsBuildScenario.setDisabled(True)
        self.layoutGroupBoxBuildScenario.addWidget(self.checkBoxBuildScenario)
        self.layoutGroupBoxBuildScenario.addWidget(self.contentOptionsBuildScenario)
        self.layoutGroupBoxBuildScenario.setAlignment(self.checkBoxBuildScenario, QtCore.Qt.AlignTop)
        self.layoutBuildScenarioInfo = QtGui.QVBoxLayout()
        self.layoutBuildScenario = QtGui.QGridLayout()
        self.layoutOptionsBuildScenario.addLayout(self.layoutBuildScenarioInfo)
        self.layoutOptionsBuildScenario.addLayout(self.layoutBuildScenario)
        
        self.labelBuildScenarioInfo = QtGui.QLabel()
        self.labelBuildScenarioInfo.setText('Build scenario\n')
        self.layoutBuildScenarioInfo.addWidget(self.labelBuildScenarioInfo)
        
        self.labelBuildScenarioHistoricalBaselineCar = QtGui.QLabel()
        self.labelBuildScenarioHistoricalBaselineCar.setText('Historical baseline data:')
        self.layoutBuildScenario.addWidget(self.labelBuildScenarioHistoricalBaselineCar, 0, 0)
        
        self.lineEditBuildScenarioHistoricalBaselineCar = QtGui.QLineEdit()
        self.lineEditBuildScenarioHistoricalBaselineCar.setReadOnly(True)
        self.layoutBuildScenario.addWidget(self.lineEditBuildScenarioHistoricalBaselineCar, 0, 1)
        
        self.buttonSelectBuildScenarioHistoricalBaselineCar = QtGui.QPushButton()
        self.buttonSelectBuildScenarioHistoricalBaselineCar.setText('&Browse')
        self.layoutBuildScenario.addWidget(self.buttonSelectBuildScenarioHistoricalBaselineCar, 0, 2)
        
        # Process tab button
        self.layoutButtonLowEmissionDevelopmentAnalysis = QtGui.QHBoxLayout()
        self.buttonProcessLowEmissionDevelopmentAnalysis = QtGui.QPushButton()
        self.buttonProcessLowEmissionDevelopmentAnalysis.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonProcessLowEmissionDevelopmentAnalysis.setText('&Process')
        icon = QtGui.QIcon(':/ui/icons/iconActionHelp.png')
        self.buttonHelpSCIENDOLowEmissionDevelopmentAnalysis = QtGui.QPushButton()
        self.buttonHelpSCIENDOLowEmissionDevelopmentAnalysis.setIcon(icon)
        self.layoutButtonLowEmissionDevelopmentAnalysis.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonLowEmissionDevelopmentAnalysis.addWidget(self.buttonProcessLowEmissionDevelopmentAnalysis)
        self.layoutButtonLowEmissionDevelopmentAnalysis.addWidget(self.buttonHelpSCIENDOLowEmissionDevelopmentAnalysis)
        
        # Template GroupBox
        self.groupBoxLowEmissionDevelopmentAnalysisTemplate = QtGui.QGroupBox('Cponfiguration')
        self.layoutGroupBoxLowEmissionDevelopmentAnalysisTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxLowEmissionDevelopmentAnalysisTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLowEmissionDevelopmentAnalysisTemplate.setLayout(self.layoutGroupBoxLowEmissionDevelopmentAnalysisTemplate)
        self.layoutLowEmissionDevelopmentAnalysisTemplateInfo = QtGui.QVBoxLayout()
        self.layoutLowEmissionDevelopmentAnalysisTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxLowEmissionDevelopmentAnalysisTemplate.addLayout(self.layoutLowEmissionDevelopmentAnalysisTemplateInfo)
        self.layoutGroupBoxLowEmissionDevelopmentAnalysisTemplate.addLayout(self.layoutLowEmissionDevelopmentAnalysisTemplate)
        
        self.labelLoadedLowEmissionDevelopmentAnalysisTemplate = QtGui.QLabel()
        self.labelLoadedLowEmissionDevelopmentAnalysisTemplate.setText('Loaded configuration:')
        self.layoutLowEmissionDevelopmentAnalysisTemplate.addWidget(self.labelLoadedLowEmissionDevelopmentAnalysisTemplate, 0, 0)
        
        self.loadedLowEmissionDevelopmentAnalysisTemplate = QtGui.QLabel()
        self.loadedLowEmissionDevelopmentAnalysisTemplate.setText('<None>')
        self.layoutLowEmissionDevelopmentAnalysisTemplate.addWidget(self.loadedLowEmissionDevelopmentAnalysisTemplate, 0, 1)
        
        self.labelLowEmissionDevelopmentAnalysisTemplate = QtGui.QLabel()
        self.labelLowEmissionDevelopmentAnalysisTemplate.setText('Name:')
        self.layoutLowEmissionDevelopmentAnalysisTemplate.addWidget(self.labelLowEmissionDevelopmentAnalysisTemplate, 1, 0)
        
        self.comboBoxLowEmissionDevelopmentAnalysisTemplate = QtGui.QComboBox()
        self.comboBoxLowEmissionDevelopmentAnalysisTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxLowEmissionDevelopmentAnalysisTemplate.setDisabled(True)
        self.comboBoxLowEmissionDevelopmentAnalysisTemplate.addItem('No configuration found')
        self.layoutLowEmissionDevelopmentAnalysisTemplate.addWidget(self.comboBoxLowEmissionDevelopmentAnalysisTemplate, 1, 1)
        
        self.layoutButtonLowEmissionDevelopmentAnalysisTemplate = QtGui.QHBoxLayout()
        self.layoutButtonLowEmissionDevelopmentAnalysisTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadLowEmissionDevelopmentAnalysisTemplate = QtGui.QPushButton()
        self.buttonLoadLowEmissionDevelopmentAnalysisTemplate.setDisabled(True)
        self.buttonLoadLowEmissionDevelopmentAnalysisTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadLowEmissionDevelopmentAnalysisTemplate.setText('Load')
        self.buttonSaveLowEmissionDevelopmentAnalysisTemplate = QtGui.QPushButton()
        self.buttonSaveLowEmissionDevelopmentAnalysisTemplate.setDisabled(True)
        self.buttonSaveLowEmissionDevelopmentAnalysisTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveLowEmissionDevelopmentAnalysisTemplate.setText('Save')
        self.buttonSaveAsLowEmissionDevelopmentAnalysisTemplate = QtGui.QPushButton()
        self.buttonSaveAsLowEmissionDevelopmentAnalysisTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsLowEmissionDevelopmentAnalysisTemplate.setText('Save As')
        self.layoutButtonLowEmissionDevelopmentAnalysisTemplate.addWidget(self.buttonLoadLowEmissionDevelopmentAnalysisTemplate)
        self.layoutButtonLowEmissionDevelopmentAnalysisTemplate.addWidget(self.buttonSaveLowEmissionDevelopmentAnalysisTemplate)
        self.layoutButtonLowEmissionDevelopmentAnalysisTemplate.addWidget(self.buttonSaveAsLowEmissionDevelopmentAnalysisTemplate)
        self.layoutGroupBoxLowEmissionDevelopmentAnalysisTemplate.addLayout(self.layoutButtonLowEmissionDevelopmentAnalysisTemplate)
        
        # Place the GroupBoxes
        self.layoutTabLowEmissionDevelopmentAnalysis.addWidget(self.groupBoxHistoricalBaselineProjection, 0, 0)
        self.layoutTabLowEmissionDevelopmentAnalysis.addWidget(self.groupBoxHistoricalBaselineAnnualProjection, 1, 0)
        self.layoutTabLowEmissionDevelopmentAnalysis.addWidget(self.groupBoxDriversAnalysis, 2, 0)
        self.layoutTabLowEmissionDevelopmentAnalysis.addWidget(self.groupBoxBuildScenario, 3, 0)
        self.layoutTabLowEmissionDevelopmentAnalysis.addLayout(self.layoutButtonLowEmissionDevelopmentAnalysis, 4, 0, 1, 2, QtCore.Qt.AlignRight)
        self.layoutTabLowEmissionDevelopmentAnalysis.addWidget(self.groupBoxLowEmissionDevelopmentAnalysisTemplate, 0, 1, 4, 1)
        self.layoutTabLowEmissionDevelopmentAnalysis.setColumnStretch(0, 3)
        self.layoutTabLowEmissionDevelopmentAnalysis.setColumnStretch(1, 1) # Smaller template column
        
        #***********************************************************
        # Setup 'Land Use Change Modeling' tab
        #***********************************************************
        self.tabWidgetLandUseChangeModeling = QtGui.QTabWidget()
        LandUseChangeModelingTabWidgetStylesheet = """
        QTabWidget QWidget {
            background-color: rgb(217, 229, 252);
            color: rgb(95, 98, 102);
        }
        QTabBar::tab {
            background-color: rgb(244, 248, 252);
            height: 35px;
            width: 240px;
        }
        QTabBar::tab:selected, QTabBar::tab:hover {
            background-color: rgb(217, 229, 252);
            font: bold;
        }
        """
        self.tabWidgetLandUseChangeModeling.setStyleSheet(LandUseChangeModelingTabWidgetStylesheet)
        
        self.tabCreateRasterCubeOfFactors = QtGui.QWidget()
        self.tabCalculateTransitionMatrix = QtGui.QWidget()
        # self.tabCalculateWeightOfEvidence = QtGui.QWidget()
        self.tabSimulateLandUseChangeModeling = QtGui.QWidget()
        
        self.tabWidgetLandUseChangeModeling.addTab(self.tabCreateRasterCubeOfFactors, 'Create Raster Cube Of Factors')
        self.tabWidgetLandUseChangeModeling.addTab(self.tabCalculateTransitionMatrix, 'Calculate Transition Matrix')
        # self.tabWidgetLandUseChangeModeling.addTab(self.tabCalculateWeightOfEvidence, 'Calculate Weight Of Evidence')
        self.tabWidgetLandUseChangeModeling.addTab(self.tabSimulateLandUseChangeModeling, 'Simulate LUC Modeling')
        
        self.layoutTabLandUseChangeModeling.addWidget(self.tabWidgetLandUseChangeModeling)
        
        self.layoutTabCreateRasterCubeOfFactors = QtGui.QGridLayout()
        self.layoutTabCalculateTransitionMatrix = QtGui.QGridLayout()
        # self.layoutTabCalculateWeightOfEvidence = QtGui.QGridLayout()
        self.layoutTabSimulateLandUseChangeModeling = QtGui.QGridLayout()
        
        self.tabCreateRasterCubeOfFactors.setLayout(self.layoutTabCreateRasterCubeOfFactors)
        self.tabCalculateTransitionMatrix.setLayout(self.layoutTabCalculateTransitionMatrix)
        # self.tabCalculateWeightOfEvidence.setLayout(self.layoutTabCalculateWeightOfEvidence)
        self.tabSimulateLandUseChangeModeling.setLayout(self.layoutTabSimulateLandUseChangeModeling)
        
        #***********************************************************
        # 'Create Raster Cube Of Factors' sub tab
        #***********************************************************
        # 'Raster Cube' GroupBox
        self.groupBoxCreateRasterCubeOfFactors = QtGui.QGroupBox('Add factors')
        self.layoutGroupBoxCreateRasterCubeOfFactors = QtGui.QVBoxLayout()
        self.layoutGroupBoxCreateRasterCubeOfFactors.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxCreateRasterCubeOfFactors.setLayout(self.layoutGroupBoxCreateRasterCubeOfFactors)
        self.layoutCreateRasterCubeOfFactorsInfo = QtGui.QVBoxLayout()
        self.layoutCreateRasterCubeOfFactors = QtGui.QVBoxLayout()
        self.layoutGroupBoxCreateRasterCubeOfFactors.addLayout(self.layoutCreateRasterCubeOfFactorsInfo)
        self.layoutGroupBoxCreateRasterCubeOfFactors.addLayout(self.layoutCreateRasterCubeOfFactors)
        
        self.labelCreateRasterCubeOfFactorsInfo = QtGui.QLabel()
        self.labelCreateRasterCubeOfFactorsInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutCreateRasterCubeOfFactorsInfo.addWidget(self.labelCreateRasterCubeOfFactorsInfo)
        
        self.layoutButtonCreateRasterCubeOfFactors = QtGui.QHBoxLayout()
        self.layoutButtonCreateRasterCubeOfFactors.setContentsMargins(0, 0, 0, 0)
        self.layoutButtonCreateRasterCubeOfFactors.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.buttonAddFactorRow = QtGui.QPushButton()
        self.buttonAddFactorRow.setText('Add Factor')
        self.buttonAddFactorRow.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.layoutButtonCreateRasterCubeOfFactors.addWidget(self.buttonAddFactorRow)
        
        self.layoutContentCreateRasterCubeOfFactors = QtGui.QVBoxLayout()
        self.layoutContentCreateRasterCubeOfFactors.setContentsMargins(2, 2, 2, 2)
        self.contentCreateRasterCubeOfFactors = QtGui.QWidget()
        self.contentCreateRasterCubeOfFactors.setLayout(self.layoutContentCreateRasterCubeOfFactors)
        self.scrollCreateRasterCubeOfFactors = QtGui.QScrollArea()
        self.scrollCreateRasterCubeOfFactors.setWidgetResizable(True)
        self.scrollCreateRasterCubeOfFactors.setWidget(self.contentCreateRasterCubeOfFactors)
        
        self.layoutTableAddFactor = QtGui.QVBoxLayout()
        self.layoutTableAddFactor.setAlignment(QtCore.Qt.AlignTop)
        self.layoutContentCreateRasterCubeOfFactors.addLayout(self.layoutTableAddFactor)
        
        self.layoutCreateRasterCubeOfFactors.addLayout(self.layoutButtonCreateRasterCubeOfFactors)
        self.layoutCreateRasterCubeOfFactors.addWidget(self.scrollCreateRasterCubeOfFactors)

        # Template GroupBox
        self.groupBoxCreateRasterCubeTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxCreateRasterCubeTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxCreateRasterCubeTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxCreateRasterCubeTemplate.setLayout(self.layoutGroupBoxCreateRasterCubeTemplate)
        self.layoutCreateRasterCubeTemplateInfo = QtGui.QVBoxLayout()
        self.layoutCreateRasterCubeTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxCreateRasterCubeTemplate.addLayout(self.layoutCreateRasterCubeTemplateInfo)
        self.layoutGroupBoxCreateRasterCubeTemplate.addLayout(self.layoutCreateRasterCubeTemplate)
        
        self.labelLoadedCreateRasterCubeTemplate = QtGui.QLabel()
        self.labelLoadedCreateRasterCubeTemplate.setText('Loaded template:')
        self.layoutCreateRasterCubeTemplate.addWidget(self.labelLoadedCreateRasterCubeTemplate, 0, 0)
        
        self.loadedCreateRasterCubeTemplate = QtGui.QLabel()
        self.loadedCreateRasterCubeTemplate.setText('<None>')
        self.layoutCreateRasterCubeTemplate.addWidget(self.loadedCreateRasterCubeTemplate, 0, 1)
        
        self.labelCreateRasterCubeTemplate = QtGui.QLabel()
        self.labelCreateRasterCubeTemplate.setText('Template name:')
        self.layoutCreateRasterCubeTemplate.addWidget(self.labelCreateRasterCubeTemplate, 1, 0)
        
        self.comboBoxCreateRasterCubeTemplate = QtGui.QComboBox()
        self.comboBoxCreateRasterCubeTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxCreateRasterCubeTemplate.setDisabled(True)
        self.comboBoxCreateRasterCubeTemplate.addItem('No template found')
        self.layoutCreateRasterCubeTemplate.addWidget(self.comboBoxCreateRasterCubeTemplate, 1, 1)
        
        self.layoutButtonCreateRasterCubeTemplate = QtGui.QHBoxLayout()
        self.layoutButtonCreateRasterCubeTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadCreateRasterCubeTemplate = QtGui.QPushButton()
        self.buttonLoadCreateRasterCubeTemplate.setDisabled(True)
        self.buttonLoadCreateRasterCubeTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadCreateRasterCubeTemplate.setText('Load')
        self.buttonSaveCreateRasterCubeTemplate = QtGui.QPushButton()
        self.buttonSaveCreateRasterCubeTemplate.setDisabled(True)
        self.buttonSaveCreateRasterCubeTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveCreateRasterCubeTemplate.setText('Save')
        self.buttonSaveAsCreateRasterCubeTemplate = QtGui.QPushButton()
        self.buttonSaveAsCreateRasterCubeTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsCreateRasterCubeTemplate.setText('Save As')
        self.layoutButtonCreateRasterCubeTemplate.addWidget(self.buttonLoadCreateRasterCubeTemplate)
        self.layoutButtonCreateRasterCubeTemplate.addWidget(self.buttonSaveCreateRasterCubeTemplate)
        self.layoutButtonCreateRasterCubeTemplate.addWidget(self.buttonSaveAsCreateRasterCubeTemplate)
        self.layoutGroupBoxCreateRasterCubeTemplate.addLayout(self.layoutButtonCreateRasterCubeTemplate)
        
        
        # don't forget to remove a few of unnecessary lines below
        
        # 'Functions' GroupBox
        self.groupBoxLandUseChangeModelingFunctions = QtGui.QGroupBox('Functions')
        self.layoutGroupBoxLandUseChangeModelingFunctions = QtGui.QVBoxLayout()
        self.layoutGroupBoxLandUseChangeModelingFunctions.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLandUseChangeModelingFunctions.setLayout(self.layoutGroupBoxLandUseChangeModelingFunctions)
        self.layoutLandUseChangeModelingFunctionsInfo = QtGui.QVBoxLayout()
        self.layoutLandUseChangeModelingFunctions = QtGui.QGridLayout()
        self.layoutGroupBoxLandUseChangeModelingFunctions.addLayout(self.layoutLandUseChangeModelingFunctionsInfo)
        self.layoutGroupBoxLandUseChangeModelingFunctions.addLayout(self.layoutLandUseChangeModelingFunctions)
        
        self.labelLandUseChangeModelingFunctionsInfo = QtGui.QLabel()
        self.labelLandUseChangeModelingFunctionsInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutLandUseChangeModelingFunctionsInfo.addWidget(self.labelLandUseChangeModelingFunctionsInfo)
        
        self.checkBoxCalculateTransitionMatrix = QtGui.QCheckBox('Calculate transition matrix')
        self.checkBoxCreateRasterCubeOfFactors = QtGui.QCheckBox('Create raster cube of factors')
        self.checkBoxCalculateWeightOfEvidence = QtGui.QCheckBox('Calculate weight of evidence')
        self.checkBoxSimulateLandUseChange = QtGui.QCheckBox('Simulate land use change')
        self.checkBoxSimulateWithScenario = QtGui.QCheckBox('Simulate with scenario')
        
        self.layoutLandUseChangeModelingFunctions.addWidget(self.checkBoxCalculateTransitionMatrix)
        self.layoutLandUseChangeModelingFunctions.addWidget(self.checkBoxCreateRasterCubeOfFactors)
        self.layoutLandUseChangeModelingFunctions.addWidget(self.checkBoxCalculateWeightOfEvidence)
        self.layoutLandUseChangeModelingFunctions.addWidget(self.checkBoxSimulateLandUseChange)
        self.layoutLandUseChangeModelingFunctions.addWidget(self.checkBoxSimulateWithScenario)
        
        
        # 'Parameters' GroupBox
        self.groupBoxLandUseChangeModelingParameters = QtGui.QGroupBox('Parameters')
        self.layoutGroupBoxLandUseChangeModelingParameters = QtGui.QVBoxLayout()
        self.layoutGroupBoxLandUseChangeModelingParameters.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLandUseChangeModelingParameters.setLayout(self.layoutGroupBoxLandUseChangeModelingParameters)
        self.layoutLandUseChangeModelingParametersInfo = QtGui.QVBoxLayout()
        self.layoutLandUseChangeModelingParameters = QtGui.QGridLayout()
        self.layoutGroupBoxLandUseChangeModelingParameters.addLayout(self.layoutLandUseChangeModelingParametersInfo)
        self.layoutGroupBoxLandUseChangeModelingParameters.addLayout(self.layoutLandUseChangeModelingParameters)
        
        self.labelLandUseChangeModelingParametersInfo = QtGui.QLabel()
        self.labelLandUseChangeModelingParametersInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutLandUseChangeModelingParametersInfo.addWidget(self.labelLandUseChangeModelingParametersInfo)
        
        self.labelLandUseChangeModelingFactorsDir = QtGui.QLabel()
        self.labelLandUseChangeModelingFactorsDir.setText('Factors directory:')
        self.layoutLandUseChangeModelingParameters.addWidget(self.labelLandUseChangeModelingFactorsDir, 0, 0)
        
        self.lineEditLandUseChangeModelingFactorsDir = QtGui.QLineEdit()
        self.lineEditLandUseChangeModelingFactorsDir.setReadOnly(True)
        self.layoutLandUseChangeModelingParameters.addWidget(self.lineEditLandUseChangeModelingFactorsDir, 0, 1)
        
        self.buttonSelectLandUseChangeModelingFactorsDir = QtGui.QPushButton()
        self.buttonSelectLandUseChangeModelingFactorsDir.setText('&Browse')
        self.layoutLandUseChangeModelingParameters.addWidget(self.buttonSelectLandUseChangeModelingFactorsDir, 0, 2)
        
        self.labelLandUseChangeModelingLandUseLookup = QtGui.QLabel()
        self.labelLandUseChangeModelingLandUseLookup.setText('Land use lookup table:')
        self.layoutLandUseChangeModelingParameters.addWidget(self.labelLandUseChangeModelingLandUseLookup, 1, 0)
        
        self.lineEditLandUseChangeModelingLandUseLookup = QtGui.QLineEdit()
        self.lineEditLandUseChangeModelingLandUseLookup.setReadOnly(True)
        self.layoutLandUseChangeModelingParameters.addWidget(self.lineEditLandUseChangeModelingLandUseLookup, 1, 1)
        
        self.buttonSelectLandUseChangeModelingLandUseLookup = QtGui.QPushButton()
        self.buttonSelectLandUseChangeModelingLandUseLookup.setText('&Browse')
        self.layoutLandUseChangeModelingParameters.addWidget(self.buttonSelectLandUseChangeModelingLandUseLookup, 1, 2)
        
        self.labelLandUseChangeModelingBaseYear = QtGui.QLabel()
        self.labelLandUseChangeModelingBaseYear.setText('Base &year:')
        self.layoutLandUseChangeModelingParameters.addWidget(self.labelLandUseChangeModelingBaseYear, 2, 0)
        
        self.spinBoxLandUseChangeModelingBaseYear = QtGui.QSpinBox()
        self.spinBoxLandUseChangeModelingBaseYear.setRange(1, 9999)
        td = datetime.date.today()
        self.spinBoxLandUseChangeModelingBaseYear.setValue(td.year)
        self.layoutLandUseChangeModelingParameters.addWidget(self.spinBoxLandUseChangeModelingBaseYear, 2, 1)
        self.labelLandUseChangeModelingBaseYear.setBuddy(self.spinBoxLandUseChangeModelingBaseYear)
        
        self.labelLandUseChangeModelingLocation = QtGui.QLabel()
        self.labelLandUseChangeModelingLocation.setText('Location:')
        self.layoutLandUseChangeModelingParameters.addWidget(self.labelLandUseChangeModelingLocation, 3, 0)
        
        self.lineEditLandUseChangeModelingLocation = QtGui.QLineEdit()
        self.lineEditLandUseChangeModelingLocation.setText('location')
        self.layoutLandUseChangeModelingParameters.addWidget(self.lineEditLandUseChangeModelingLocation, 3, 1)
        self.labelLandUseChangeModelingLocation.setBuddy(self.lineEditLandUseChangeModelingLocation)
        
         # end: dont forget to remove
        
        # Process tab button
        self.layoutButtonCreateRasterCube = QtGui.QHBoxLayout()
        self.buttonProcessCreateRasterCube = QtGui.QPushButton()
        self.buttonProcessCreateRasterCube.setText('&Process')
        self.buttonHelpSCIENDOCreateRasterCube = QtGui.QPushButton()
        self.buttonHelpSCIENDOCreateRasterCube.setIcon(icon)
        self.layoutButtonCreateRasterCube.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonCreateRasterCube.addWidget(self.buttonProcessCreateRasterCube)
        self.layoutButtonCreateRasterCube.addWidget(self.buttonHelpSCIENDOCreateRasterCube)

        # Place the GroupBoxes
        self.layoutTabCreateRasterCubeOfFactors.addWidget(self.groupBoxCreateRasterCubeOfFactors, 0, 0)
        self.layoutTabCreateRasterCubeOfFactors.addLayout(self.layoutButtonCreateRasterCube, 1, 0, 1, 2, QtCore.Qt.AlignRight)
        self.layoutTabCreateRasterCubeOfFactors.addWidget(self.groupBoxCreateRasterCubeTemplate, 0, 1, 1, 1)
        self.layoutTabCreateRasterCubeOfFactors.setColumnStretch(0, 3)
        self.layoutTabCreateRasterCubeOfFactors.setColumnStretch(1, 1) # Smaller template column
        
        #***********************************************************
        # Setup 'Calculate Transition Matrix' sub tab
        #***********************************************************
        # 'Setup initial and final map' GroupBox
        self.groupBoxSetupInitialAndFinalMap = QtGui.QGroupBox('Setup initial and final map')
        self.layoutSetupInitialAndFinalMap = QtGui.QVBoxLayout()
        self.layoutSetupInitialAndFinalMap.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxSetupInitialAndFinalMap.setLayout(self.layoutSetupInitialAndFinalMap)
        
        self.layoutSetupInitialAndFinalMapInfo = QtGui.QVBoxLayout()
        self.labelSetupInitialAndFinalMapInfo = QtGui.QLabel()
        self.labelSetupInitialAndFinalMapInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutSetupInitialAndFinalMapInfo.addWidget(self.labelSetupInitialAndFinalMapInfo)
        
        self.layoutTransitionMatrixPerRegions = QtGui.QGridLayout()
        self.layoutTransitionMatrixPerRegions.setContentsMargins(0, 0, 0, 0)

        self.labelTransitionMatrixInitialMap = QtGui.QLabel()
        self.labelTransitionMatrixInitialMap.setText('Earlier land use/cover:')
        self.layoutTransitionMatrixPerRegions.addWidget(self.labelTransitionMatrixInitialMap, 0, 0)
        
        self.comboBoxTransitionMatrixInitialMap = QtGui.QComboBox()
        self.comboBoxTransitionMatrixInitialMap.setDisabled(True)
        self.layoutTransitionMatrixPerRegions.addWidget(self.comboBoxTransitionMatrixInitialMap, 0, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataLandUseCover, self.comboBoxTransitionMatrixInitialMap)
        
        self.labelTransitionMatrixFinalMap = QtGui.QLabel()
        self.labelTransitionMatrixFinalMap.setText('Later land use/cover:')
        self.layoutTransitionMatrixPerRegions.addWidget(self.labelTransitionMatrixFinalMap, 1, 0)
        
        self.comboBoxTransitionMatrixFinalMap = QtGui.QComboBox()
        self.comboBoxTransitionMatrixFinalMap.setDisabled(True)
        self.layoutTransitionMatrixPerRegions.addWidget(self.comboBoxTransitionMatrixFinalMap, 1, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataLandUseCover, self.comboBoxTransitionMatrixFinalMap)
        
        self.labelTransitionMatrixRegions = QtGui.QLabel()
        self.labelTransitionMatrixRegions.setText('Planning unit:')
        self.layoutTransitionMatrixPerRegions.addWidget(self.labelTransitionMatrixRegions, 2, 0)
        
        self.comboBoxTransitionMatrixRegions = QtGui.QComboBox()
        self.comboBoxTransitionMatrixRegions.setDisabled(True)
        self.layoutTransitionMatrixPerRegions.addWidget(self.comboBoxTransitionMatrixRegions, 2, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataPlanningUnit, self.comboBoxTransitionMatrixRegions)           

        self.labelTransitionMatrixIteration = QtGui.QLabel()
        self.labelTransitionMatrixIteration.setText('Iteration:')
        self.layoutTransitionMatrixPerRegions.addWidget(self.labelTransitionMatrixIteration, 3, 0)
        
        self.spinBoxTransitionMatrixIteration = QtGui.QSpinBox()
        self.spinBoxTransitionMatrixIteration.setRange(1, 99)
        self.spinBoxTransitionMatrixIteration.setValue(5)
        self.layoutTransitionMatrixPerRegions.addWidget(self.spinBoxTransitionMatrixIteration, 3, 1)
        self.labelLandUseChangeModelingBaseYear.setBuddy(self.spinBoxTransitionMatrixIteration)
        
        self.layoutSetupInitialAndFinalMap.addLayout(self.layoutSetupInitialAndFinalMapInfo)
        self.layoutSetupInitialAndFinalMap.addLayout(self.layoutTransitionMatrixPerRegions)

        # Template GroupBox
        self.groupBoxTransitionMatrixTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxTransitionMatrixTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxTransitionMatrixTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxTransitionMatrixTemplate.setLayout(self.layoutGroupBoxTransitionMatrixTemplate)
        self.layoutTransitionMatrixTemplateInfo = QtGui.QVBoxLayout()
        self.layoutTransitionMatrixTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxTransitionMatrixTemplate.addLayout(self.layoutTransitionMatrixTemplateInfo)
        self.layoutGroupBoxTransitionMatrixTemplate.addLayout(self.layoutTransitionMatrixTemplate)
        
        self.labelLoadedTransitionMatrixTemplate = QtGui.QLabel()
        self.labelLoadedTransitionMatrixTemplate.setText('Loaded template:')
        self.layoutTransitionMatrixTemplate.addWidget(self.labelLoadedTransitionMatrixTemplate, 0, 0)
        
        self.loadedTransitionMatrixTemplate = QtGui.QLabel()
        self.loadedTransitionMatrixTemplate.setText('<None>')
        self.layoutTransitionMatrixTemplate.addWidget(self.loadedTransitionMatrixTemplate, 0, 1)
        
        self.labelTransitionMatrixTemplate = QtGui.QLabel()
        self.labelTransitionMatrixTemplate.setText('Template name:')
        self.layoutTransitionMatrixTemplate.addWidget(self.labelTransitionMatrixTemplate, 1, 0)
        
        self.comboBoxTransitionMatrixTemplate = QtGui.QComboBox()
        self.comboBoxTransitionMatrixTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxTransitionMatrixTemplate.setDisabled(True)
        self.comboBoxTransitionMatrixTemplate.addItem('No template found')
        self.layoutTransitionMatrixTemplate.addWidget(self.comboBoxTransitionMatrixTemplate, 1, 1)
        
        self.layoutButtonTransitionMatrixTemplate = QtGui.QHBoxLayout()
        self.layoutButtonTransitionMatrixTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadTransitionMatrixTemplate = QtGui.QPushButton()
        self.buttonLoadTransitionMatrixTemplate.setDisabled(True)
        self.buttonLoadTransitionMatrixTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadTransitionMatrixTemplate.setText('Load')
        self.buttonSaveTransitionMatrixTemplate = QtGui.QPushButton()
        self.buttonSaveTransitionMatrixTemplate.setDisabled(True)
        self.buttonSaveTransitionMatrixTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveTransitionMatrixTemplate.setText('Save')
        self.buttonSaveAsTransitionMatrixTemplate = QtGui.QPushButton()
        self.buttonSaveAsTransitionMatrixTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsTransitionMatrixTemplate.setText('Save As')
        self.layoutButtonTransitionMatrixTemplate.addWidget(self.buttonLoadTransitionMatrixTemplate)
        self.layoutButtonTransitionMatrixTemplate.addWidget(self.buttonSaveTransitionMatrixTemplate)
        self.layoutButtonTransitionMatrixTemplate.addWidget(self.buttonSaveAsTransitionMatrixTemplate)
        self.layoutGroupBoxTransitionMatrixTemplate.addLayout(self.layoutButtonTransitionMatrixTemplate)

        # Process tab button
        self.layoutButtonTransitionMatrix = QtGui.QHBoxLayout()
        self.buttonProcessTransitionMatrix = QtGui.QPushButton()
        self.buttonProcessTransitionMatrix.setText('&Process')
        self.buttonHelpSCIENDOTransitionMatrix = QtGui.QPushButton()
        self.buttonHelpSCIENDOTransitionMatrix.setIcon(icon)
        self.layoutButtonTransitionMatrix.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonTransitionMatrix.addWidget(self.buttonProcessTransitionMatrix)
        self.layoutButtonTransitionMatrix.addWidget(self.buttonHelpSCIENDOTransitionMatrix)
        
        # Place the GroupBoxes
        self.layoutTabCalculateTransitionMatrix.addWidget(self.groupBoxSetupInitialAndFinalMap, 0, 0)
        self.layoutTabCalculateTransitionMatrix.addLayout(self.layoutButtonTransitionMatrix, 1, 0, 1, 2, QtCore.Qt.AlignRight)
        self.layoutTabCalculateTransitionMatrix.addWidget(self.groupBoxTransitionMatrixTemplate, 0, 1, 1, 1)
        self.layoutTabCalculateTransitionMatrix.setColumnStretch(0, 3)
        self.layoutTabCalculateTransitionMatrix.setColumnStretch(1, 1) 
        
        #***********************************************************
        # Setup 'Simulate Land Use Change Modeling' sub tab
        #***********************************************************
        # 'Simulate Land Use Change Modeling' GroupBox
        self.groupBoxLandUseChangeSimulation = QtGui.QGroupBox('Transitions')
        self.layoutGroupBoxLandUseChangeSimulation = QtGui.QVBoxLayout()
        self.layoutGroupBoxLandUseChangeSimulation.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLandUseChangeSimulation.setLayout(self.layoutGroupBoxLandUseChangeSimulation)
        
        self.layouLandUseChangeSimulationInfo = QtGui.QVBoxLayout()
        self.labelLandUseChangeSimulationInfo = QtGui.QLabel()
        self.labelLandUseChangeSimulationInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layouLandUseChangeSimulationInfo.addWidget(self.labelLandUseChangeSimulationInfo)        
        
        self.tableListOfTransitions = QtGui.QTableWidget()
        self.tableListOfTransitions.setEnabled(True)
        self.tableListOfTransitions.setRowCount(25)
        self.tableListOfTransitions.setColumnCount(4)
        self.tableListOfTransitions.verticalHeader().setVisible(False)
        self.tableListOfTransitions.setHorizontalHeaderLabels(['From', 'To', 'Percent', 'Patch Size (Ha)'])
        
        #tableRow = 0
        #for 
        
        self.layoutGroupBoxLandUseChangeSimulation.addLayout(self.layouLandUseChangeSimulationInfo)
        self.layoutGroupBoxLandUseChangeSimulation.addWidget(self.tableListOfTransitions)
        
        # Template GroupBox
        self.groupBoxLandUseChangeSimulationTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxLandUseChangeSimulationTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxLandUseChangeSimulationTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLandUseChangeSimulationTemplate.setLayout(self.layoutGroupBoxLandUseChangeSimulationTemplate)
        self.layoutLandUseChangeSimulationTemplateInfo = QtGui.QVBoxLayout()
        self.layoutLandUseChangeSimulationTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxLandUseChangeSimulationTemplate.addLayout(self.layoutLandUseChangeSimulationTemplateInfo)
        self.layoutGroupBoxLandUseChangeSimulationTemplate.addLayout(self.layoutLandUseChangeSimulationTemplate)
        
        self.labelLoadedLandUseChangeSimulationTemplate = QtGui.QLabel()
        self.labelLoadedLandUseChangeSimulationTemplate.setText('Loaded template:')
        self.layoutLandUseChangeSimulationTemplate.addWidget(self.labelLoadedLandUseChangeSimulationTemplate, 0, 0)
        
        self.loadedLandUseChangeSimulationTemplate = QtGui.QLabel()
        self.loadedLandUseChangeSimulationTemplate.setText('<None>')
        self.layoutLandUseChangeSimulationTemplate.addWidget(self.loadedLandUseChangeSimulationTemplate, 0, 1)
        
        self.labelLandUseChangeSimulationTemplate = QtGui.QLabel()
        self.labelLandUseChangeSimulationTemplate.setText('Template name:')
        self.layoutLandUseChangeSimulationTemplate.addWidget(self.labelLandUseChangeSimulationTemplate, 1, 0)
        
        self.comboBoxLandUseChangeSimulationTemplate = QtGui.QComboBox()
        self.comboBoxLandUseChangeSimulationTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxLandUseChangeSimulationTemplate.setDisabled(True)
        self.comboBoxLandUseChangeSimulationTemplate.addItem('No template found')
        self.layoutLandUseChangeSimulationTemplate.addWidget(self.comboBoxLandUseChangeSimulationTemplate, 1, 1)
        
        self.layoutButtonLandUseChangeSimulationTemplate = QtGui.QHBoxLayout()
        self.layoutButtonLandUseChangeSimulationTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadLandUseChangeSimulationTemplate = QtGui.QPushButton()
        self.buttonLoadLandUseChangeSimulationTemplate.setDisabled(True)
        self.buttonLoadLandUseChangeSimulationTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadLandUseChangeSimulationTemplate.setText('Load')
        self.buttonSaveLandUseChangeSimulationTemplate = QtGui.QPushButton()
        self.buttonSaveLandUseChangeSimulationTemplate.setDisabled(True)
        self.buttonSaveLandUseChangeSimulationTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveLandUseChangeSimulationTemplate.setText('Save')
        self.buttonSaveAsLandUseChangeSimulationTemplate = QtGui.QPushButton()
        self.buttonSaveAsLandUseChangeSimulationTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsLandUseChangeSimulationTemplate.setText('Save As')
        self.layoutButtonLandUseChangeSimulationTemplate.addWidget(self.buttonLoadLandUseChangeSimulationTemplate)
        self.layoutButtonLandUseChangeSimulationTemplate.addWidget(self.buttonSaveLandUseChangeSimulationTemplate)
        self.layoutButtonLandUseChangeSimulationTemplate.addWidget(self.buttonSaveAsLandUseChangeSimulationTemplate)
        self.layoutGroupBoxLandUseChangeSimulationTemplate.addLayout(self.layoutButtonLandUseChangeSimulationTemplate)
        
        # Process tab button
        self.layoutButtonLandUseChangeSimulation = QtGui.QHBoxLayout()
        self.buttonProcessLandUseChangeSimulation = QtGui.QPushButton()
        self.buttonProcessLandUseChangeSimulation.setText('&Process')
        self.buttonHelpSCIENDOLandUseChangeSimulation = QtGui.QPushButton()
        self.buttonHelpSCIENDOLandUseChangeSimulation.setIcon(icon)
        self.layoutButtonLandUseChangeSimulation.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonLandUseChangeSimulation.addWidget(self.buttonProcessLandUseChangeSimulation)
        self.layoutButtonLandUseChangeSimulation.addWidget(self.buttonHelpSCIENDOLandUseChangeSimulation)        
        
        # Place the GroupBoxes
        self.layoutTabSimulateLandUseChangeModeling.addWidget(self.groupBoxLandUseChangeSimulation, 0, 0)
        self.layoutTabSimulateLandUseChangeModeling.addLayout(self.layoutButtonLandUseChangeSimulation, 1, 0, 1, 2, QtCore.Qt.AlignRight)
        self.layoutTabSimulateLandUseChangeModeling.addWidget(self.groupBoxLandUseChangeSimulationTemplate, 0, 1, 1, 1)
        self.layoutTabSimulateLandUseChangeModeling.setColumnStretch(0, 3)
        self.layoutTabSimulateLandUseChangeModeling.setColumnStretch(1, 1) 
        
        
        #***********************************************************
        # Setup 'Log' tab
        #***********************************************************
        # 'History Log' GroupBox
        self.groupBoxHistoryLog = QtGui.QGroupBox('{0} {1}'.format(self.dialogTitle, 'history log'))
        self.layoutGroupBoxHistoryLog = QtGui.QVBoxLayout()
        self.layoutGroupBoxHistoryLog.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxHistoryLog.setLayout(self.layoutGroupBoxHistoryLog)
        self.layoutHistoryLogInfo = QtGui.QVBoxLayout()
        self.layoutHistoryLog = QtGui.QVBoxLayout()
        self.layoutGroupBoxHistoryLog.addLayout(self.layoutHistoryLogInfo)
        self.layoutGroupBoxHistoryLog.addLayout(self.layoutHistoryLog)
        
        self.labelHistoryLogInfo = QtGui.QLabel()
        self.labelHistoryLogInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutHistoryLogInfo.addWidget(self.labelHistoryLogInfo)
        
        self.log_box = QPlainTextEditLogger(self)
        self.layoutHistoryLog.addWidget(self.log_box.widget)
        
        self.layoutTabLog.addWidget(self.groupBoxHistoryLog)
        
        
        self.setLayout(self.dialogLayout)
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(800, 640)
        self.resize(parent.sizeHint())
    
    
    def showEvent(self, event):
        """Overload method that is called when the dialog widget is shown.
        
        Args:
            event (QShowEvent): the show widget event.
        """
        super(DialogLumensSCIENDO, self).showEvent(event)
    
    
    def closeEvent(self, event):
        """Overload method that is called when the dialog widget is closed.
        
        Args:
            event (QCloseEvent): the close widget event.
        """
        super(DialogLumensSCIENDO, self).closeEvent(event)
    
    
    def loadHistoryLog(self):
        """Method for loading the module history log file.
        """
        if os.path.exists(self.historyLogPath):
            logText = open(self.historyLogPath).read()
            self.log_box.widget.setPlainText(logText)
    
    
    def handlerTabWidgetChanged(self, index):
        """Slot method for scrolling the log to the latest output.
        
        Args:
            index (int): the current tab index.
        """
        if self.tabWidget.widget(index) == self.tabLog:
            self.log_box.widget.verticalScrollBar().triggerAction(QtGui.QAbstractSlider.SliderToMaximum)


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


    def addFactorRow(self):
        """Method for adding a factor row to the input table
        """
        self.tableAddFactorRowCount = self.tableAddFactorRowCount + 1
        
        layoutFactorRow = QtGui.QHBoxLayout()
        
        buttonDeleteFactorRow = QtGui.QPushButton()
        icon = QtGui.QIcon(':/ui/icons/iconActionClear.png')
        buttonDeleteFactorRow.setIcon(icon)
        buttonDeleteFactorRow.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        buttonDeleteFactorRow.setObjectName('buttonDeleteFactorRow_{0}'.format(str(self.tableAddFactorRowCount)))
        layoutFactorRow.addWidget(buttonDeleteFactorRow)
        
        buttonDeleteFactorRow.clicked.connect(self.handlerDeleteFactorRow)
        
        comboBoxFactorData = QtGui.QComboBox()
        comboBoxFactorData.setDisabled(True)
        comboBoxFactorData.setObjectName('comboBoxFactorData_{0}'.format(str(self.tableAddFactorRowCount)))
        layoutFactorRow.addWidget(comboBoxFactorData)
        
        comboBoxFactorData.currentIndexChanged.connect(self.handlerChangeFactorData)

        lineEditFactorTitle = QtGui.QLineEdit()
        lineEditFactorTitle.setDisabled(True)
        lineEditFactorTitle.setObjectName('lineEditFactorTitle_{0}'.format(str(self.tableAddFactorRowCount)))
        layoutFactorRow.addWidget(lineEditFactorTitle)
        
        lineEditFactorPath = QtGui.QLineEdit()
        lineEditFactorPath.setVisible(False)
        lineEditFactorPath.setObjectName('lineEditFactorPath_{0}'.format(str(self.tableAddFactorRowCount)))
        layoutFactorRow.addWidget(lineEditFactorPath)
        
        self.layoutTableAddFactor.addLayout(layoutFactorRow)
        self.populateAddedDataComboBox(self.main.dataFactor, comboBoxFactorData)
        

    def populateQUESCDatabase(self):
        layoutCheckBoxQUESCDatabase = QtGui.QVBoxLayout()
        self.checkBoxQUESCDatabaseCount = 0
        if len(self.main.dataTable):
            dataTable = self.main.dataTable
            dataQUESCDatabase = []
            for value in dataTable.values():
                dataTableName = value[list(value)[0]]
                if 'out_hist_quesc_' in dataTableName:
                    dataQUESCDatabase.append(dataTableName)
            for name in dataQUESCDatabase:
                self.checkBoxQUESCDatabaseCount = self.checkBoxQUESCDatabaseCount + 1
                checkBoxHistoricalBaselineAnnualProjectionQUESCDatabase = QtGui.QCheckBox()
                checkBoxHistoricalBaselineAnnualProjectionQUESCDatabase.setObjectName('checkBoxHistoricalBaselineAnnualProjectionQUESCDatabase_{0}'.format(str(self.checkBoxQUESCDatabaseCount)))
                checkBoxHistoricalBaselineAnnualProjectionQUESCDatabase.setText(name)
                layoutCheckBoxQUESCDatabase.addWidget(checkBoxHistoricalBaselineAnnualProjectionQUESCDatabase)
                checkBoxHistoricalBaselineAnnualProjectionQUESCDatabase.toggled.connect(self.toggleHistoricalBaselineAnnualProjectionQUESCDatabase)
        else:
            labelQUESCDatabaseHistoricalBaselineAnnualProjection = QtGui.QLabel()
            labelQUESCDatabaseHistoricalBaselineAnnualProjection.setText('\nNo QUES-C Database found!\n')
            layoutCheckBoxQUESCDatabase.addWidget(labelQUESCDatabaseHistoricalBaselineAnnualProjection)
            
        self.layoutOptionsHistoricalBaselineAnnualProjection.addLayout(layoutCheckBoxQUESCDatabase)
                        
    
    #***********************************************************
    # 'Low Emission Development Analysis' tab QGroupBox toggle handlers
    #***********************************************************
    def toggleHistoricalBaselineProjection(self, checked):
        """Slot method for handling checkbox toggling.
        
        Args:
            checked (bool): the checkbox status.
        """
        if checked:
            self.contentOptionsHistoricalBaselineProjection.setEnabled(True)
        else:
            self.contentOptionsHistoricalBaselineProjection.setDisabled(True)
    
    
    def toggleHistoricalBaselineAnnualProjection(self, checked):
        """Slot method for handling checkbox toggling.
        
        Args:
            checked (bool): the checkbox status.
        """
        if checked:
            self.contentOptionsHistoricalBaselineAnnualProjection.setEnabled(True)
        else:
            self.contentOptionsHistoricalBaselineAnnualProjection.setDisabled(True)


    def toggleHistoricalBaselineAnnualProjectionQUESCDatabase(self, checked):
        """Slot method for handling checkbox toggling.
        
        Args:
            checked (bool): the checkbox status.
        """
        checkBoxSender = self.sender()
        objectName = checkBoxSender.objectName()
        checkBoxIndex = objectName.split('_')[1]
        
        checkBoxQUESCDatabase = self.contentOptionsHistoricalBaselineAnnualProjection.findChild(QtGui.QCheckBox, 'checkBoxHistoricalBaselineAnnualProjectionQUESCDatabase_' + checkBoxIndex)
        checkBoxName = checkBoxQUESCDatabase.text()
        
        if checked:
            self.listOfQUESCDatabase.append(checkBoxName)
        else:
            self.listOfQUESCDatabase.remove(checkBoxName)
    
    
    def toggleDriversAnalysis(self, checked):
        """Slot method for handling checkbox toggling.
        
        Args:
            checked (bool): the checkbox status.
        """
        if checked:
            self.contentOptionsDriversAnalysis.setEnabled(True)
        else:
            self.contentOptionsDriversAnalysis.setDisabled(True)
    
    
    def toggleBuildScenario(self, checked):
        """Slot method for handling checkbox toggling.
        
        Args:
            checked (bool): the checkbox status.
        """
        if checked:
            self.contentOptionsBuildScenario.setEnabled(True)
        else:
            self.contentOptionsBuildScenario.setDisabled(True)
    
    
    #***********************************************************
    # 'Low Emission Development Analysis' tab QPushButton handlers
    #***********************************************************
    def handlerLoadLowEmissionDevelopmentAnalysisTemplate(self, fileName=None):
        """Slot method for loading a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.comboBoxLowEmissionDevelopmentAnalysisTemplate.currentText()
        reply = None
        
        if fileName:
            templateFile = fileName
        else:
            reply = QtGui.QMessageBox.question(
                self,
                'Load Template',
                'Do you want to load \'{0}\'?'.format(templateFile),
                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                QtGui.QMessageBox.No
            )
            
        if reply == QtGui.QMessageBox.Yes or fileName:
            self.loadTemplate('Low Emission Development Analysis', templateFile)
    
    
    def handlerSaveLowEmissionDevelopmentAnalysisTemplate(self, fileName=None):
        """Slot method for saving a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.currentLowEmissionDevelopmentAnalysisTemplate
        
        if fileName:
            templateFile = fileName
        
        reply = QtGui.QMessageBox.question(
            self,
            'Save Template',
            'Do you want save \'{0}\'?\nThis action will overwrite the template file.'.format(templateFile),
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
            QtGui.QMessageBox.No
        )
            
        if reply == QtGui.QMessageBox.Yes:
            self.saveTemplate('Low Emission Development Analysis', templateFile)
            return True
        else:
            return False
    
    
    def handlerSaveAsLowEmissionDevelopmentAnalysisTemplate(self):
        """Slot method for saving a module template to a new file.
        """
        fileName, ok = QtGui.QInputDialog.getText(self, 'Save As', 'Enter a new template name:')
        fileSaved = False
        
        if ok:
            now = QtCore.QDateTime.currentDateTime().toString('yyyyMMdd-hhmmss')
            fileName = now + '__' + fileName + '.ini'
            
            if os.path.exists(os.path.join(self.settingsPath, fileName)):
                fileSaved = self.handlerSaveLowEmissionDevelopmentAnalysisTemplate(fileName)
            else:
                self.saveTemplate('Low Emission Development Analysis', fileName)
                fileSaved = True
            
            self.loadTemplateFiles()
            
            # Load the newly saved template file
            if fileSaved:
                self.handlerLoadLowEmissionDevelopmentAnalysisTemplate(fileName)
          
    
    def handlerSelectDriversAnalysisLandUseCoverChangeDrivers(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Use/Cover Change Drivers', QtCore.QDir.homePath(), 'Land Use/Cover Change Drivers (*{0})'.format(self.main.appSettings['selectTextfileExt'])))
        
        if file:
            self.lineEditDriversAnalysisLandUseCoverChangeDrivers.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectBuildScenarioHistoricalBaselineCar(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Historical Baseline Car', QtCore.QDir.homePath(), 'Historical Baseline Car (*{0})'.format(self.main.appSettings['selectCarfileExt'])))
        
        if file:
            self.lineEditBuildScenarioHistoricalBaselineCar.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    #***********************************************************
    # 'Land Use Change Modeling' tab QPushButton handlers
    #***********************************************************
    def handlerLoadLandUseChangeModelingTemplate(self, fileName=None):
        """Slot method for loading a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.comboBoxLandUseChangeModelingTemplate.currentText()
        reply = None
        
        if fileName:
            templateFile = fileName
        else:
            reply = QtGui.QMessageBox.question(
                self,
                'Load Template',
                'Do you want to load \'{0}\'?'.format(templateFile),
                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                QtGui.QMessageBox.No
            )
            
        if reply == QtGui.QMessageBox.Yes or fileName:
            self.loadTemplate('Land Use Change Modeling', templateFile)
    
    
    def handlerSaveLandUseChangeModelingTemplate(self, fileName=None):
        """Slot method for saving a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.currentLandUseChangeModelingTemplate
        
        if fileName:
            templateFile = fileName
        
        reply = QtGui.QMessageBox.question(
            self,
            'Save Template',
            'Do you want save \'{0}\'?\nThis action will overwrite the template file.'.format(templateFile),
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
            QtGui.QMessageBox.No
        )
            
        if reply == QtGui.QMessageBox.Yes:
            self.saveTemplate('Land Use Change Modeling', templateFile)
            return True
        else:
            return False
    
    
    def handlerSaveAsLandUseChangeModelingTemplate(self):
        """Slot method for saving a module template to a new file.
        """
        fileName, ok = QtGui.QInputDialog.getText(self, 'Save As', 'Enter a new template name:')
        fileSaved = False
        
        if ok:
            now = QtCore.QDateTime.currentDateTime().toString('yyyyMMdd-hhmmss')
            fileName = now + '__' + fileName + '.ini'
            
            if os.path.exists(os.path.join(self.settingsPath, fileName)):
                fileSaved = self.handlerSaveLandUseChangeModelingTemplate(fileName)
            else:
                self.saveTemplate('Land Use Change Modeling', fileName)
                fileSaved = True
            
            self.loadTemplateFiles()
            
            # Load the newly saved template file
            if fileSaved:
                self.handlerLoadLandUseChangeModelingTemplate(fileName)
    

    def handlerButtonAddFactorRow(self):
        """Slot method for adding a factor row
        """
        self.addFactorRow()
        
        
    def handlerChangeFactorData(self, currentIndex=None, rowNumber=None, RST_DATA=None):
        """Slot method for changing a planning unit data.
        
        Args:
            rowNumber (int): the planning unit table row.
            RST_DATA (str): the RST_DATA key of an added factor data.
        """
        tableRow = None
        
        if not rowNumber:
            buttonSender = self.sender()
            objectName = buttonSender.objectName()
            tableRow = objectName.split('_')[1]
        else:
            tableRow = str(rowNumber)
            
        comboBoxFactorData = self.contentCreateRasterCubeOfFactors.findChild(QtGui.QComboBox, 'comboBoxFactorData_' + tableRow)
        
        factorData = comboBoxFactorData.currentText()
        addedFactor = comboBoxFactorData.itemData(comboBoxFactorData.findText(factorData))
        
        lineEditFactorTitle = self.contentCreateRasterCubeOfFactors.findChild(QtGui.QLineEdit, 'lineEditFactorTitle_' + tableRow)
        lineEditFactorTitle.setText(addedFactor['RST_NAME'])        
        lineEditFactorPath = self.contentCreateRasterCubeOfFactors.findChild(QtGui.QLineEdit, 'lineEditFactorPath_' + tableRow)
        lineEditFactorPath.setText(addedFactor['RST_PATH'])
        
        
    def handlerDeleteFactorRow(self):
        """Slot method for deleting a factor row
        """
        buttonSender = self.sender()
        objectName = buttonSender.objectName()
        tableRow = objectName.split('_')[1]
        layoutRow = self.layoutTableAddFactor.itemAt(int(tableRow) - 1).layout()
        self.clearLayout(layoutRow)
        
        
    def handlerSelectLandUseChangeModelingFactorsDir(self):
        """Slot method for a directory select dialog.
        """
        dir = unicode(QtGui.QFileDialog.getExistingDirectory(self, 'Select Factors Directory'))
        
        if dir:
            self.lineEditLandUseChangeModelingFactorsDir.setText(dir)
            logging.getLogger(type(self).__name__).info('select directory: %s', dir)
    
    
    def handlerSelectLandUseChangeModelingLandUseLookup(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Use Lookup Table', QtCore.QDir.homePath(), 'Land Use Lookup Table (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditLandUseChangeModelingLandUseLookup.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    #***********************************************************
    # Process tabs
    #***********************************************************
    def setAppSettings(self):
        """Set the required values from the form widgets.
        """
        # 'Historical baseline projection' groupbox fields
        self.main.appSettings['DialogLumensSCIENDOHistoricalBaselineProjection']['QUESCDatabase'] \
            = unicode(self.comboBoxHistoricalBaselineProjectionQUESCDatabase.currentText())
        self.main.appSettings['DialogLumensSCIENDOHistoricalBaselineProjection']['iteration'] \
            = self.spinBoxHistoricalBaselineProjectionIteration.value()
        
        # 'Historical baseline annual projection' groupbox fields
        self.main.appSettings['DialogLumensSCIENDOHistoricalBaselineAnnualProjection']['iteration'] \
            = self.spinBoxHistoricalBaselineAnnualProjectionIteration.value()
        
        # 'Drivers analysis' groupbox fields
        self.main.appSettings['DialogLumensSCIENDODriversAnalysis']['landUseCoverChangeDrivers'] \
            = unicode(self.lineEditDriversAnalysisLandUseCoverChangeDrivers.text())
        self.main.appSettings['DialogLumensSCIENDODriversAnalysis']['landUseCoverChangeType'] \
            = unicode(self.lineEditDriversAnalysisLandUseCoverChangeType.text())
        
        # 'Build scenario' groupbox fields
        self.main.appSettings['DialogLumensSCIENDOBuildScenario']['historicalBaselineCar'] \
            = unicode(self.lineEditBuildScenarioHistoricalBaselineCar.text())
        
        # 'Land Use Change Modeling' tab fields
        self.main.appSettings['DialogLumensSCIENDOCalculateTransitionMatrix']['factorsDir'] \
            = self.main.appSettings['DialogLumensSCIENDOCreateRasterCube']['factorsDir'] \
            = self.main.appSettings['DialogLumensSCIENDOCalculateWeightofEvidence']['factorsDir'] \
            = self.main.appSettings['DialogLumensSCIENDOSimulateLandUseChange']['factorsDir'] \
            = self.main.appSettings['DialogLumensSCIENDOSimulateWithScenario']['factorsDir'] \
            = unicode(self.lineEditLandUseChangeModelingFactorsDir.text()).replace(os.path.sep, '/')
        self.main.appSettings['DialogLumensSCIENDOCalculateTransitionMatrix']['landUseLookup'] \
            = self.main.appSettings['DialogLumensSCIENDOCreateRasterCube']['landUseLookup'] \
            = self.main.appSettings['DialogLumensSCIENDOCalculateWeightofEvidence']['landUseLookup'] \
            = self.main.appSettings['DialogLumensSCIENDOSimulateLandUseChange']['landUseLookup'] \
            = self.main.appSettings['DialogLumensSCIENDOSimulateWithScenario']['landUseLookup'] \
            = unicode(self.lineEditLandUseChangeModelingLandUseLookup.text())
        self.main.appSettings['DialogLumensSCIENDOCalculateTransitionMatrix']['baseYear'] \
            = self.main.appSettings['DialogLumensSCIENDOCreateRasterCube']['baseYear'] \
            = self.main.appSettings['DialogLumensSCIENDOCalculateWeightofEvidence']['baseYear'] \
            = self.main.appSettings['DialogLumensSCIENDOSimulateLandUseChange']['baseYear'] \
            = self.main.appSettings['DialogLumensSCIENDOSimulateWithScenario']['baseYear'] \
            = self.spinBoxLandUseChangeModelingBaseYear.value()
        self.main.appSettings['DialogLumensSCIENDOCalculateTransitionMatrix']['location'] \
            = self.main.appSettings['DialogLumensSCIENDOCreateRasterCube']['location'] \
            = self.main.appSettings['DialogLumensSCIENDOCalculateWeightofEvidence']['location'] \
            = self.main.appSettings['DialogLumensSCIENDOSimulateLandUseChange']['location'] \
            = self.main.appSettings['DialogLumensSCIENDOSimulateWithScenario']['location'] \
            = unicode(self.lineEditLandUseChangeModelingLocation.text())
    
    
    def handlerProcessLowEmissionDevelopmentAnalysis(self):
        """Slot method to pass the form values and execute the "SCIENDO Low Emission Development Analysis" R algorithms.
        
        Depending on the checked groupbox, the "SCIENDO Low Emission Development Analysis" process calls the following algorithms:
        1. r:sciendoperiodprojection
        2. r:sciendoannualprojection
        3. modeler:drivers_analysis
        4. r:abacususingabsolutearea
        """
        self.setAppSettings()
        activeProject = self.main.appSettings['DialogLumensOpenDatabase']['projectFile'].replace(os.path.sep, '/')
        
        if self.checkBoxHistoricalBaselineProjection.isChecked():
            formName = 'DialogLumensSCIENDOHistoricalBaselineProjection'
            algName = 'r:sciendoperiodprojection'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                logging.getLogger(self.historyLog).info('alg start: %s' % formName)
                self.buttonProcessLowEmissionDevelopmentAnalysis.setDisabled(True)
                
                # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                self.main.setWindowState(QtCore.Qt.WindowMinimized)
                
                outputs = general.runalg(
                    algName,
                    activeProject,
                    self.main.appSettings[formName]['QUESCDatabase'],
                    self.main.appSettings[formName]['iteration'],
                    None,
                )
                
                # Display ROut file in debug mode
                if self.main.appSettings['debug']:
                    dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                    dialog.exec_()
                
                # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
                self.main.setWindowState(QtCore.Qt.WindowActive)
                
                algSuccess = self.outputsMessageBox(algName, outputs, '', '')
                
                if algSuccess:
                    self.main.loadAddedDataInfo()
                
                self.buttonProcessLowEmissionDevelopmentAnalysis.setEnabled(True)
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
                logging.getLogger(self.historyLog).info('alg end: %s' % formName)
        
        if self.checkBoxHistoricalBaselineAnnualProjection.isChecked():
            if len(self.listOfQUESCDatabase) > 1:
                formName = 'DialogLumensSCIENDOHistoricalBaselineAnnualProjection'
                algName = 'r:sciendoannualprojection'
                
                self.listOfQUESCDatabase.sort()
                QUESCDatabaseCsv = self.writeListCsv(self.listOfQUESCDatabase, True)
                
                if self.validForm(formName):
                    logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                    logging.getLogger(self.historyLog).info('alg start: %s' % formName)
                    self.buttonProcessLowEmissionDevelopmentAnalysis.setDisabled(True)
                    
                    # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                    self.main.setWindowState(QtCore.Qt.WindowMinimized)
                    
                    outputs = general.runalg(
                        algName,
                        activeProject,
                        QUESCDatabaseCsv,
                        self.main.appSettings[formName]['iteration'],
                        None,
                    )
                    
                    # Display ROut file in debug mode
                    if self.main.appSettings['debug']:
                        dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                        dialog.exec_()
                    
                    ##print outputs
                    
                    # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
                    self.main.setWindowState(QtCore.Qt.WindowActive)
                    
                    algSuccess = self.outputsMessageBox(algName, outputs, '', '')
                    
                    if algSuccess:
                        self.main.loadAddedDataInfo()
                    
                    self.buttonProcessLowEmissionDevelopmentAnalysis.setEnabled(True)
                    logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
                    logging.getLogger(self.historyLog).info('alg end: %s' % formName)
            else: 
                QtGui.QMessageBox.information(self, 'Historical Baseline Annual Projection', 'Choose at least two QUES-C database.')
                return 
        
        
        if self.checkBoxDriversAnalysis.isChecked():
            formName = 'DialogLumensSCIENDODriversAnalysis'
            algName = 'modeler:drivers_analysis'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                logging.getLogger(self.historyLog).info('alg start: %s' % formName)
                self.buttonProcessLowEmissionDevelopmentAnalysis.setDisabled(True)
                
                # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                self.main.setWindowState(QtCore.Qt.WindowMinimized)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['landUseCoverChangeDrivers'],
                    self.main.appSettings[formName]['landUseCoverChangeType'],
                )
                
                # Display ROut file in debug mode
                if self.main.appSettings['debug']:
                    dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                    dialog.exec_()
                
                ##print outputs
                
                # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
                self.main.setWindowState(QtCore.Qt.WindowActive)
                
                algSuccess = self.outputsMessageBox(algName, outputs, '', '')
                
                if algSuccess:
                    self.main.loadAddedDataInfo()                
                
                self.buttonProcessLowEmissionDevelopmentAnalysis.setEnabled(True)
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
                logging.getLogger(self.historyLog).info('alg end: %s' % formName)
        
        
        if self.checkBoxBuildScenario.isChecked():
            formName = 'DialogLumensSCIENDOBuildScenario'
            algName = 'r:abacususingabsolutearea'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                logging.getLogger(self.historyLog).info('alg start: %s' % formName)
                self.buttonProcessLowEmissionDevelopmentAnalysis.setDisabled(True)
                
                # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                self.main.setWindowState(QtCore.Qt.WindowMinimized)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['historicalBaselineCar'],
                )
                
                # Display ROut file in debug mode
                if self.main.appSettings['debug']:
                    dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                    dialog.exec_()
                
                ##print outputs
                
                # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
                self.main.setWindowState(QtCore.Qt.WindowActive)
                
                self.outputsMessageBox(algName, outputs, '', '')
                
                self.buttonProcessLowEmissionDevelopmentAnalysis.setEnabled(True)
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
                logging.getLogger(self.historyLog).info('alg end: %s' % formName)
    
    
    def handlerProcessLandUseChangeModeling(self):
        """Slot method to pass the form values and execute the "SCIENDO Land Use Change Modeling" R algorithms.
        
        Depending on the checked groupbox, the "SCIENDO Land Use Change Modeling" process calls the following algorithms:
        1. modeler:sciendo1_calculate_transition_matrix
        2. modeler:sciendo1_create_raster_cube
        3. modeler:sciendo3_calculate_weight_of_evidence
        4. modeler:sciendo4_simulate_land_use_change
        5. modeler:sciendo5_simulate_with_scenario
        """
        if self.checkBoxCalculateTransitionMatrix.isChecked():
            formName = 'DialogLumensSCIENDOCalculateTransitionMatrix'
            algName = 'modeler:sciendo1_calculate_transition_matrix'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                logging.getLogger(self.historyLog).info('alg start: %s' % formName)
                self.buttonProcessLandUseChangeModeling.setDisabled(True)
                
                # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                self.main.setWindowState(QtCore.Qt.WindowMinimized)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['factorsDir'],
                    self.main.appSettings[formName]['landUseLookup'],
                    self.main.appSettings[formName]['baseYear'],
                    self.main.appSettings[formName]['location'],
                )
                
                # Display ROut file in debug mode
                if self.main.appSettings['debug']:
                    dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                    dialog.exec_()
                
                ##print outputs
                
                # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
                self.main.setWindowState(QtCore.Qt.WindowActive)
                
                self.outputsMessageBox(algName, outputs, '', '')
                
                self.buttonProcessLandUseChangeModeling.setEnabled(True)
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
                logging.getLogger(self.historyLog).info('alg end: %s' % formName)
        
        if self.checkBoxCreateRasterCubeOfFactors.isChecked():
            formName = 'DialogLumensSCIENDOCreateRasterCube'
            algName = 'modeler:sciendo1_create_raster_cube'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                logging.getLogger(self.historyLog).info('alg start: %s' % formName)
                self.buttonProcessLandUseChangeModeling.setDisabled(True)
                
                # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                self.main.setWindowState(QtCore.Qt.WindowMinimized)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['factorsDir'],
                    self.main.appSettings[formName]['landUseLookup'],
                    self.main.appSettings[formName]['baseYear'],
                    self.main.appSettings[formName]['location'],
                )
                
                # Display ROut file in debug mode
                if self.main.appSettings['debug']:
                    dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                    dialog.exec_()
                
                ##print outputs
                
                # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
                self.main.setWindowState(QtCore.Qt.WindowActive)
                
                self.outputsMessageBox(algName, outputs, '', '')
                
                self.buttonProcessLandUseChangeModeling.setEnabled(True)
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
                logging.getLogger(self.historyLog).info('alg end: %s' % formName)
        
        if self.checkBoxCalculateWeightOfEvidence.isChecked():
            formName = 'DialogLumensSCIENDOCalculateWeightofEvidence'
            algName = 'modeler:sciendo3_calculate_weight_of_evidence'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                logging.getLogger(self.historyLog).info('alg start: %s' % formName)
                self.buttonProcessLandUseChangeModeling.setDisabled(True)
                
                # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                self.main.setWindowState(QtCore.Qt.WindowMinimized)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['factorsDir'],
                    self.main.appSettings[formName]['landUseLookup'],
                    self.main.appSettings[formName]['baseYear'],
                    self.main.appSettings[formName]['location'],
                )
                
                # Display ROut file in debug mode
                if self.main.appSettings['debug']:
                    dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                    dialog.exec_()
                
                ##print outputs
                
                # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
                self.main.setWindowState(QtCore.Qt.WindowActive)
                
                self.outputsMessageBox(algName, outputs, '', '')
                
                self.buttonProcessLandUseChangeModeling.setEnabled(True)
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
                logging.getLogger(self.historyLog).info('alg end: %s' % formName)
        
        if self.checkBoxSimulateLandUseChange.isChecked():
            formName = 'DialogLumensSCIENDOSimulateLandUseChange'
            algName = 'modeler:sciendo4_simulate_land_use_change'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                logging.getLogger(self.historyLog).info('alg start: %s' % formName)
                self.buttonProcessLandUseChangeModeling.setDisabled(True)
                
                # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                self.main.setWindowState(QtCore.Qt.WindowMinimized)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['factorsDir'],
                    self.main.appSettings[formName]['landUseLookup'],
                    self.main.appSettings[formName]['baseYear'],
                    self.main.appSettings[formName]['location'],
                )
                
                # Display ROut file in debug mode
                if self.main.appSettings['debug']:
                    dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                    dialog.exec_()
                
                ##print outputs
                
                # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
                self.main.setWindowState(QtCore.Qt.WindowActive)
                
                algSuccess = self.outputsMessageBox(algName, outputs, '', '')
                
                if algSuccess:
                    self.main.loadAddedDataInfo()                
                
                self.buttonProcessLandUseChangeModeling.setEnabled(True)
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
                logging.getLogger(self.historyLog).info('alg end: %s' % formName)
        
        if self.checkBoxSimulateWithScenario.isChecked():
            formName = 'DialogLumensSCIENDOSimulateWithScenario'
            algName = 'modeler:sciendo5_simulate_with_scenario'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                logging.getLogger(self.historyLog).info('alg start: %s' % formName)
                self.buttonProcessLandUseChangeModeling.setDisabled(True)
                
                # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                self.main.setWindowState(QtCore.Qt.WindowMinimized)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['factorsDir'],
                    self.main.appSettings[formName]['landUseLookup'],
                    self.main.appSettings[formName]['baseYear'],
                    self.main.appSettings[formName]['location'],
                )
                
                # Display ROut file in debug mode
                if self.main.appSettings['debug']:
                    dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                    dialog.exec_()
                
                ##print outputs
                
                # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
                self.main.setWindowState(QtCore.Qt.WindowActive)
                
                algSuccess = self.outputsMessageBox(algName, outputs, '', '')
                
                if algSuccess:
                    self.main.loadAddedDataInfo()                
                
                self.buttonProcessLandUseChangeModeling.setEnabled(True)
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
                logging.getLogger(self.historyLog).info('alg end: %s' % formName)
    
