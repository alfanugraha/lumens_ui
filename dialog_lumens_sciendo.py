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

from menu_factory import MenuFactory

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
        
        if tabName == MenuFactory.getLabel(MenuFactory.SCIENDO_LED):
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
        elif tabName == MenuFactory.getLabel(MenuFactory.SCIENDO_LUCM):
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
        
        if tabName == MenuFactory.getLabel(MenuFactory.SCIENDO_LED):
            dialogsToLoad = (
                'DialogLumensSCIENDOHistoricalBaselineProjection',
                'DialogLumensSCIENDOHistoricalBaselineAnnualProjection',
                'DialogLumensSCIENDODriversAnalysis',
                'DialogLumensSCIENDOBuildScenario',
            )
        elif tabName == MenuFactory.getLabel(MenuFactory.SCIENDO_LUCM):
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
                MenuFactory.getLabel(MenuFactory.CONF_LOAD_TEMPLATE),
                MenuFactory.getDescription(MenuFactory.CONF_LOAD_TEMPLATE) + ' \'{0}\'?'.format(templateFile),
                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                QtGui.QMessageBox.No
            )
            
            if reply == QtGui.QMessageBox.Yes:
                if tabName == MenuFactory.getLabel(MenuFactory.SCIENDO_LED):
                    self.handlerLoadLowEmissionDevelopmentAnalysisTemplate(duplicateTemplate)
                elif tabName == MenuFactory.getLabel(MenuFactory.SCIENDO_LUCM):
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
            
            if tabName == MenuFactory.getLabel(MenuFactory.SCIENDO_LED):
                dialogsToSave = (
                    'DialogLumensSCIENDOHistoricalBaselineProjection',
                    'DialogLumensSCIENDOHistoricalBaselineAnnualProjection',
                    'DialogLumensSCIENDODriversAnalysis',
                    'DialogLumensSCIENDOBuildScenario',
                )
            elif tabName == MenuFactory.getLabel(MenuFactory.SCIENDO_LUCM):
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
        # self.simulationIndex = []
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
        
        # 'Calculate transistion matrix' tab buttons
        self.buttonProcessTransitionMatrix.clicked.connect(self.handlerProcessTransitionMatrix)
        
        # 'Create factor raster cube' tab buttons
        self.buttonSelectCreateRasterCubeOfFactorsDirectory.clicked.connect(self.handlerSelectLandUseChangeModelingFactorsDir)
        self.buttonProcessCreateRasterCube.clicked.connect(self.handlerProcessCreateRasterCube)
        # self.buttonAddFactorRow.clicked.connect(self.handlerButtonAddFactorRow)
        # self.buttonHelpSCIENDOCreateRasterCube.clicked.connect(lambda:self.handlerDialogHelp('SCIENDO'))
        # self.buttonSelectLandUseChangeModelingLandUseLookup.clicked.connect(self.handlerSelectLandUseChangeModelingLandUseLookup)
        # self.buttonProcessCreateRasterCube.clicked.connect(self.handlerProcessLandUseChangeModeling)
        #self.buttonLoadLandUseChangeModelingTemplate.clicked.connect(self.handlerLoadLandUseChangeModelingTemplate)
        #self.buttonSaveLandUseChangeModelingTemplate.clicked.connect(self.handlerSaveLandUseChangeModelingTemplate)
        #self.buttonSaveAsLandUseChangeModelingTemplate.clicked.connect(self.handlerSaveAsLandUseChangeModelingTemplate)
    
        # 'Calculate weight of evidence' tab buttons
        self.buttonProcessCalculateWeightOfEvidence.clicked.connect(self.handlerProcessCalculateWeightOfEvidence)
        
        # 'Simulate land use' tab buttons
        self.buttonProcessLandUseChangeSimulation.clicked.connect(self.handlerProcessSimulateLandUse)
        
    
    def setupUi(self, parent):
        """Method for building the dialog UI.
        
        Args:
            parent: the dialog's parent instance.
        """
        self.setStyleSheet('QDialog { background-color: rgb(225, 229, 237); } QMessageBox QLabel{ color: #fff; }')
        self.dialogLayout = QtGui.QVBoxLayout()

        self.groupBoxSCIENDODialog = QtGui.QGroupBox(MenuFactory.getDescription(MenuFactory.SCIENDO_TITLE))
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
        
        self.tabWidget.addTab(self.tabLowEmissionDevelopmentAnalysis, MenuFactory.getLabel(MenuFactory.SCIENDO_HISTORICAL_BASELINE_ANALYSIS))
        self.tabWidget.addTab(self.tabLandUseChangeModeling, MenuFactory.getLabel(MenuFactory.SCIENDO_LAND_USE_SIMULATION))
        self.tabWidget.addTab(self.tabLog, MenuFactory.getLabel(MenuFactory.SCIENDO_LOG))
        
        # self.layoutTabLowEmissionDevelopmentAnalysis = QtGui.QVBoxLayout()
        self.layoutTabLowEmissionDevelopmentAnalysis = QtGui.QGridLayout()
        self.layoutTabLandUseChangeModeling = QtGui.QVBoxLayout()
        # self.layoutTabLandUseChangeModeling = QtGui.QGridLayout()
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
        self.groupBoxHistoricalBaselineProjection = QtGui.QGroupBox(MenuFactory.getLabel(MenuFactory.SCIENDO_PERIODIC_PROJECTION_PARAMETER))
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
        self.labelHistoricalBaselineProjectionInfo.setText(MenuFactory.getLabel(MenuFactory.SCIENDO_CONDUCT_PERIODIC_PROJECTION))
        self.layoutHistoricalBaselineProjectionInfo.addWidget(self.labelHistoricalBaselineProjectionInfo)
        
        self.labelHistoricalBaselineProjectionQUESCDatabase = QtGui.QLabel()
        self.labelHistoricalBaselineProjectionQUESCDatabase.setText(MenuFactory.getLabel(MenuFactory.SCIENDO_QUESC_DATABASE) + ':')
        self.layoutHistoricalBaselineProjection.addWidget(self.labelHistoricalBaselineProjectionQUESCDatabase, 0, 0)
        
        self.comboBoxHistoricalBaselineProjectionQUESCDatabase = QtGui.QComboBox()
        self.comboBoxHistoricalBaselineProjectionQUESCDatabase.setDisabled(True)
        self.layoutHistoricalBaselineProjection.addWidget(self.comboBoxHistoricalBaselineProjectionQUESCDatabase, 0, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxHistoricalBaselineProjectionQUESCDatabase)
        
        self.labelHistoricalBaselineProjectionIteration = QtGui.QLabel()
        self.labelHistoricalBaselineProjectionIteration.setText(MenuFactory.getLabel(MenuFactory.SCIENDO_ITERATION) + ':')
        self.layoutHistoricalBaselineProjection.addWidget(self.labelHistoricalBaselineProjectionIteration, 1, 0)
        
        self.spinBoxHistoricalBaselineProjectionIteration = QtGui.QSpinBox()
        self.spinBoxHistoricalBaselineProjectionIteration.setRange(1, 99)
        self.spinBoxHistoricalBaselineProjectionIteration.setValue(3)
        self.layoutHistoricalBaselineProjection.addWidget(self.spinBoxHistoricalBaselineProjectionIteration, 1, 1)
        self.labelHistoricalBaselineProjectionIteration.setBuddy(self.spinBoxHistoricalBaselineProjectionIteration) 
        
        # 'Historical baseline annual projection' GroupBox
        self.groupBoxHistoricalBaselineAnnualProjection = QtGui.QGroupBox(MenuFactory.getLabel(MenuFactory.SCIENDO_ANNUAL_PROJECTION_PARAMETER))
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
        self.labelHistoricalBaselineAnnualProjectionInfo.setText(MenuFactory.getLabel(MenuFactory.SCIENDO_CONDUCT_ANNUAL_PROJECTION))
        self.layoutHistoricalBaselineAnnualProjectionInfo.addWidget(self.labelHistoricalBaselineAnnualProjectionInfo)
        
        self.labelHistoricalBaselineAnnualProjectionIteration = QtGui.QLabel()
        self.labelHistoricalBaselineAnnualProjectionIteration.setText(MenuFactory.getLabel(MenuFactory.SCIENDO_ITERATION))
        self.layoutHistoricalBaselineAnnualProjection.addWidget(self.labelHistoricalBaselineAnnualProjectionIteration, 0, 0)
        
        self.spinBoxHistoricalBaselineAnnualProjectionIteration = QtGui.QSpinBox()
        self.spinBoxHistoricalBaselineAnnualProjectionIteration.setRange(1, 9999)
        self.spinBoxHistoricalBaselineAnnualProjectionIteration.setValue(5)
        self.layoutHistoricalBaselineAnnualProjection.addWidget(self.spinBoxHistoricalBaselineAnnualProjectionIteration, 0, 1)
        self.labelHistoricalBaselineAnnualProjectionIteration.setBuddy(self.spinBoxHistoricalBaselineAnnualProjectionIteration)
        
        self.populateQUESCDatabase()

        # 'Drivers analysis' GroupBox
        self.groupBoxDriversAnalysis = QtGui.QGroupBox(MenuFactory.getLabel(MenuFactory.SCIENDO_DRIVERS_ANALYSIS_PARAMETER))
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
        self.labelDriversAnalysisInfo.setText(MenuFactory.getLabel(MenuFactory.SCIENDO_DRIVERS_ANALYSIS_PARAMETER))
        self.layoutDriversAnalysisInfo.addWidget(self.labelDriversAnalysisInfo)
        
        self.labelDriversAnalysisLandUseCoverChangeDrivers = QtGui.QLabel()
        self.labelDriversAnalysisLandUseCoverChangeDrivers.setText(MenuFactory.getLabel(MenuFactory.SCIENDO_DRIVERS_OF_LAND_USE_CHANGE) + ':')
        self.layoutDriversAnalysis.addWidget(self.labelDriversAnalysisLandUseCoverChangeDrivers, 0, 0)
        
        self.lineEditDriversAnalysisLandUseCoverChangeDrivers = QtGui.QLineEdit()
        self.lineEditDriversAnalysisLandUseCoverChangeDrivers.setReadOnly(True)
        self.layoutDriversAnalysis.addWidget(self.lineEditDriversAnalysisLandUseCoverChangeDrivers, 0, 1)
        
        self.buttonSelectDriversAnalysisLandUseCoverChangeDrivers = QtGui.QPushButton()
        self.buttonSelectDriversAnalysisLandUseCoverChangeDrivers.setText(MenuFactory.getLabel(MenuFactory.SCIENDO_BROWSE))
        self.layoutDriversAnalysis.addWidget(self.buttonSelectDriversAnalysisLandUseCoverChangeDrivers, 0, 2)
        
        self.labelDriversAnalysislandUseCoverChangeType = QtGui.QLabel()
        self.labelDriversAnalysislandUseCoverChangeType.setText(MenuFactory.getLabel(MenuFactory.SCIENDO_LAND_USE_TRAJECTORY) + ':')
        self.layoutDriversAnalysis.addWidget(self.labelDriversAnalysislandUseCoverChangeType, 1, 0)
        
        self.lineEditDriversAnalysisLandUseCoverChangeType = QtGui.QLineEdit()
        self.lineEditDriversAnalysisLandUseCoverChangeType.setText(MenuFactory.getLabel(MenuFactory.SCIENDO_PROVIDE_TRAJECTORY_NAME))
        self.layoutDriversAnalysis.addWidget(self.lineEditDriversAnalysisLandUseCoverChangeType, 1, 1)
        self.labelDriversAnalysislandUseCoverChangeType.setBuddy(self.lineEditDriversAnalysisLandUseCoverChangeType)
        
        # 'Build scenario' GroupBox
        self.groupBoxBuildScenario = QtGui.QGroupBox(MenuFactory.getLabel(MenuFactory.SCIENDO_SCENARIO_BUILDER))
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
        self.labelBuildScenarioInfo.setText(MenuFactory.getLabel(MenuFactory.SCIENDO_BUILD_SCENARIO))
        self.layoutBuildScenarioInfo.addWidget(self.labelBuildScenarioInfo)
        
        self.labelBuildScenarioHistoricalBaselineCar = QtGui.QLabel()
        self.labelBuildScenarioHistoricalBaselineCar.setText(MenuFactory.getLabel(MenuFactory.SCIENDO_HISTORICAL_BASELINE_DATA) + ':')
        self.layoutBuildScenario.addWidget(self.labelBuildScenarioHistoricalBaselineCar, 0, 0)
        
        self.lineEditBuildScenarioHistoricalBaselineCar = QtGui.QLineEdit()
        self.lineEditBuildScenarioHistoricalBaselineCar.setReadOnly(True)
        self.layoutBuildScenario.addWidget(self.lineEditBuildScenarioHistoricalBaselineCar, 0, 1)
        
        self.buttonSelectBuildScenarioHistoricalBaselineCar = QtGui.QPushButton()
        self.buttonSelectBuildScenarioHistoricalBaselineCar.setText(MenuFactory.getLabel(MenuFactory.SCIENDO_BROWSE))
        self.layoutBuildScenario.addWidget(self.buttonSelectBuildScenarioHistoricalBaselineCar, 0, 2)
        
        # Process tab button
        self.layoutButtonLowEmissionDevelopmentAnalysis = QtGui.QHBoxLayout()
        self.buttonProcessLowEmissionDevelopmentAnalysis = QtGui.QPushButton()
        self.buttonProcessLowEmissionDevelopmentAnalysis.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonProcessLowEmissionDevelopmentAnalysis.setText(MenuFactory.getLabel(MenuFactory.SCIENDO_PROCESS))
        icon = QtGui.QIcon(':/ui/icons/iconActionHelp.png')
        self.buttonHelpSCIENDOLowEmissionDevelopmentAnalysis = QtGui.QPushButton()
        self.buttonHelpSCIENDOLowEmissionDevelopmentAnalysis.setIcon(icon)
        self.layoutButtonLowEmissionDevelopmentAnalysis.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonLowEmissionDevelopmentAnalysis.addWidget(self.buttonProcessLowEmissionDevelopmentAnalysis)
        self.layoutButtonLowEmissionDevelopmentAnalysis.addWidget(self.buttonHelpSCIENDOLowEmissionDevelopmentAnalysis)
        
        # Template GroupBox
        self.groupBoxLowEmissionDevelopmentAnalysisTemplate = QtGui.QGroupBox(MenuFactory.getLabel(MenuFactory.CONF_TITLE))
        self.layoutGroupBoxLowEmissionDevelopmentAnalysisTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxLowEmissionDevelopmentAnalysisTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLowEmissionDevelopmentAnalysisTemplate.setLayout(self.layoutGroupBoxLowEmissionDevelopmentAnalysisTemplate)
        self.layoutLowEmissionDevelopmentAnalysisTemplateInfo = QtGui.QVBoxLayout()
        self.layoutLowEmissionDevelopmentAnalysisTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxLowEmissionDevelopmentAnalysisTemplate.addLayout(self.layoutLowEmissionDevelopmentAnalysisTemplateInfo)
        self.layoutGroupBoxLowEmissionDevelopmentAnalysisTemplate.addLayout(self.layoutLowEmissionDevelopmentAnalysisTemplate)
        
        self.labelLoadedLowEmissionDevelopmentAnalysisTemplate = QtGui.QLabel()
        self.labelLoadedLowEmissionDevelopmentAnalysisTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_LOADED_CONFIGURATION) + ':')
        self.layoutLowEmissionDevelopmentAnalysisTemplate.addWidget(self.labelLoadedLowEmissionDevelopmentAnalysisTemplate, 0, 0)
        
        self.loadedLowEmissionDevelopmentAnalysisTemplate = QtGui.QLabel()
        self.loadedLowEmissionDevelopmentAnalysisTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NONE))
        self.layoutLowEmissionDevelopmentAnalysisTemplate.addWidget(self.loadedLowEmissionDevelopmentAnalysisTemplate, 0, 1)
        
        self.labelLowEmissionDevelopmentAnalysisTemplate = QtGui.QLabel()
        self.labelLowEmissionDevelopmentAnalysisTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NAME) + ':')
        self.layoutLowEmissionDevelopmentAnalysisTemplate.addWidget(self.labelLowEmissionDevelopmentAnalysisTemplate, 1, 0)
        
        self.comboBoxLowEmissionDevelopmentAnalysisTemplate = QtGui.QComboBox()
        self.comboBoxLowEmissionDevelopmentAnalysisTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxLowEmissionDevelopmentAnalysisTemplate.setDisabled(True)
        self.comboBoxLowEmissionDevelopmentAnalysisTemplate.addItem(MenuFactory.getLabel(MenuFactory.CONF_NO_FOUND))
        self.layoutLowEmissionDevelopmentAnalysisTemplate.addWidget(self.comboBoxLowEmissionDevelopmentAnalysisTemplate, 1, 1)
        
        self.layoutButtonLowEmissionDevelopmentAnalysisTemplate = QtGui.QHBoxLayout()
        self.layoutButtonLowEmissionDevelopmentAnalysisTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadLowEmissionDevelopmentAnalysisTemplate = QtGui.QPushButton()
        self.buttonLoadLowEmissionDevelopmentAnalysisTemplate.setDisabled(True)
        self.buttonLoadLowEmissionDevelopmentAnalysisTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadLowEmissionDevelopmentAnalysisTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NO_FOUND))
        self.buttonSaveLowEmissionDevelopmentAnalysisTemplate = QtGui.QPushButton()
        self.buttonSaveLowEmissionDevelopmentAnalysisTemplate.setDisabled(True)
        self.buttonSaveLowEmissionDevelopmentAnalysisTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveLowEmissionDevelopmentAnalysisTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_SAVE))
        self.buttonSaveAsLowEmissionDevelopmentAnalysisTemplate = QtGui.QPushButton()
        self.buttonSaveAsLowEmissionDevelopmentAnalysisTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsLowEmissionDevelopmentAnalysisTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_SAVE_AS))
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
        QTabWidget::tab-bar{
            alignment: right;
        }
        QTabWidget QWidget {
            background-color: rgb(249, 237, 243);
            color: rgb(95, 98, 102);
        }
        QTabBar::tab {
            background-color: rgb(244, 248, 252);
            height: 35px;
            width: 210px;
        }
        QTabBar::tab:selected, QTabBar::tab:hover {
            background-color: rgb(249, 237, 243);
            font: bold;
        }
        """
        self.tabWidgetLandUseChangeModeling.setStyleSheet(LandUseChangeModelingTabWidgetStylesheet)
        
        self.tabCalculateTransitionMatrix = QtGui.QWidget()
        self.tabCreateRasterCubeOfFactors = QtGui.QWidget()
        self.tabCalculateWeightOfEvidence = QtGui.QWidget()
        self.tabSimulateLandUseChangeModeling = QtGui.QWidget()
        
        self.tabWidgetLandUseChangeModeling.addTab(self.tabCalculateTransitionMatrix, MenuFactory.getLabel(MenuFactory.SCIENDO_CALCULATE_TRANSITION_MATRIX))
        self.tabWidgetLandUseChangeModeling.addTab(self.tabCreateRasterCubeOfFactors, MenuFactory.getLabel(MenuFactory.SCIENDO_CREATE_FACTOR_RASTER_CUBE))
        self.tabWidgetLandUseChangeModeling.addTab(self.tabCalculateWeightOfEvidence, MenuFactory.getLabel(MenuFactory.SCIENDO_CALCULATE_WEIGHT_OF_EVIDENCE))
        self.tabWidgetLandUseChangeModeling.addTab(self.tabSimulateLandUseChangeModeling, MenuFactory.getLabel(MenuFactory.SCIENDO_SIMULATE_LAND_USE))
        
        self.layoutTabLandUseChangeModeling.addWidget(self.tabWidgetLandUseChangeModeling)
        
        self.layoutTabCalculateTransitionMatrix = QtGui.QGridLayout()
        self.layoutTabCreateRasterCubeOfFactors = QtGui.QGridLayout()
        self.layoutTabCalculateWeightOfEvidence = QtGui.QGridLayout()
        self.layoutTabSimulateLandUseChangeModeling = QtGui.QGridLayout()
        
        self.tabCalculateTransitionMatrix.setLayout(self.layoutTabCalculateTransitionMatrix)
        self.tabCreateRasterCubeOfFactors.setLayout(self.layoutTabCreateRasterCubeOfFactors)
        self.tabCalculateWeightOfEvidence.setLayout(self.layoutTabCalculateWeightOfEvidence)
        self.tabSimulateLandUseChangeModeling.setLayout(self.layoutTabSimulateLandUseChangeModeling)


        #***********************************************************
        # Setup 'Calculate Transition Matrix' sub tab
        #***********************************************************
        # 'Setup initial and final map' GroupBox
        self.groupBoxSetupInitialAndFinalMap = QtGui.QGroupBox(MenuFactory.getLabel(MenuFactory.SCIENDO_SETUP_INITIAL_AND_FINAL_MAP))
        self.layoutSetupInitialAndFinalMap = QtGui.QVBoxLayout()
        self.layoutSetupInitialAndFinalMap.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxSetupInitialAndFinalMap.setLayout(self.layoutSetupInitialAndFinalMap)
        
        self.layoutSetupInitialAndFinalMapInfo = QtGui.QVBoxLayout()
        self.labelSetupInitialAndFinalMapInfo = QtGui.QLabel()
        self.labelSetupInitialAndFinalMapInfo.setText('\n')
        self.layoutSetupInitialAndFinalMapInfo.addWidget(self.labelSetupInitialAndFinalMapInfo)
                 
        self.layoutTransitionMatrixPerRegions = QtGui.QGridLayout()
        self.layoutTransitionMatrixPerRegions.setContentsMargins(0, 0, 0, 0)
        
        self.labelTransitionMatrixInitialMap = QtGui.QLabel()
        self.labelTransitionMatrixInitialMap.setText(MenuFactory.getLabel(MenuFactory.SCIENDO_EARLIER_LAND_USE_COVER) + ':')
        self.layoutTransitionMatrixPerRegions.addWidget(self.labelTransitionMatrixInitialMap, 0, 0)
        
        self.comboBoxTransitionMatrixInitialMap = QtGui.QComboBox()
        self.comboBoxTransitionMatrixInitialMap.setDisabled(True)
        self.layoutTransitionMatrixPerRegions.addWidget(self.comboBoxTransitionMatrixInitialMap, 0, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataLandUseCover, self.comboBoxTransitionMatrixInitialMap)        

        self.labelTransitionMatrixFinalMap = QtGui.QLabel()
        self.labelTransitionMatrixFinalMap.setText(MenuFactory.getLabel(MenuFactory.SCIENDO_LATER_LAND_USE_COVER) + ':')
        self.layoutTransitionMatrixPerRegions.addWidget(self.labelTransitionMatrixFinalMap, 1, 0)
        
        self.comboBoxTransitionMatrixFinalMap = QtGui.QComboBox()
        self.comboBoxTransitionMatrixFinalMap.setDisabled(True)
        self.layoutTransitionMatrixPerRegions.addWidget(self.comboBoxTransitionMatrixFinalMap, 1, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataLandUseCover, self.comboBoxTransitionMatrixFinalMap)
        
        self.labelTransitionMatrixRegions = QtGui.QLabel()
        self.labelTransitionMatrixRegions.setText(MenuFactory.getLabel(MenuFactory.SCIENDO_PLANNING_UNIT) + ':')
        self.layoutTransitionMatrixPerRegions.addWidget(self.labelTransitionMatrixRegions, 2, 0)
        
        self.comboBoxTransitionMatrixRegions = QtGui.QComboBox()
        self.comboBoxTransitionMatrixRegions.setDisabled(True)
        self.layoutTransitionMatrixPerRegions.addWidget(self.comboBoxTransitionMatrixRegions, 2, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataPlanningUnit, self.comboBoxTransitionMatrixRegions) 

        self.layoutSetupInitialAndFinalMap.addLayout(self.layoutSetupInitialAndFinalMapInfo)
        self.layoutSetupInitialAndFinalMap.addLayout(self.layoutTransitionMatrixPerRegions)

        # Template GroupBox
        self.groupBoxTransitionMatrixTemplate = QtGui.QGroupBox(MenuFactory.getLabel(MenuFactory.CONF_TITLE))
        self.layoutGroupBoxTransitionMatrixTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxTransitionMatrixTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxTransitionMatrixTemplate.setLayout(self.layoutGroupBoxTransitionMatrixTemplate)
        self.layoutTransitionMatrixTemplateInfo = QtGui.QVBoxLayout()
        self.layoutTransitionMatrixTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxTransitionMatrixTemplate.addLayout(self.layoutTransitionMatrixTemplateInfo)
        self.layoutGroupBoxTransitionMatrixTemplate.addLayout(self.layoutTransitionMatrixTemplate)
        
        self.labelLoadedTransitionMatrixTemplate = QtGui.QLabel()
        self.labelLoadedTransitionMatrixTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_LOADED_CONFIGURATION) + ':')
        self.layoutTransitionMatrixTemplate.addWidget(self.labelLoadedTransitionMatrixTemplate, 0, 0)
        
        self.loadedTransitionMatrixTemplate = QtGui.QLabel()
        self.loadedTransitionMatrixTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NONE))
        self.layoutTransitionMatrixTemplate.addWidget(self.loadedTransitionMatrixTemplate, 0, 1)
        
        self.labelTransitionMatrixTemplate = QtGui.QLabel()
        self.labelTransitionMatrixTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NAME) + ':')
        self.layoutTransitionMatrixTemplate.addWidget(self.labelTransitionMatrixTemplate, 1, 0)
        
        self.comboBoxTransitionMatrixTemplate = QtGui.QComboBox()
        self.comboBoxTransitionMatrixTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxTransitionMatrixTemplate.setDisabled(True)
        self.comboBoxTransitionMatrixTemplate.addItem(MenuFactory.getLabel(MenuFactory.CONF_NO_FOUND))
        self.layoutTransitionMatrixTemplate.addWidget(self.comboBoxTransitionMatrixTemplate, 1, 1)
        
        self.layoutButtonTransitionMatrixTemplate = QtGui.QHBoxLayout()
        self.layoutButtonTransitionMatrixTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadTransitionMatrixTemplate = QtGui.QPushButton()
        self.buttonLoadTransitionMatrixTemplate.setDisabled(True)
        self.buttonLoadTransitionMatrixTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadTransitionMatrixTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NO_FOUND))
        self.buttonSaveTransitionMatrixTemplate = QtGui.QPushButton()
        self.buttonSaveTransitionMatrixTemplate.setDisabled(True)
        self.buttonSaveTransitionMatrixTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveTransitionMatrixTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_SAVE))
        self.buttonSaveAsTransitionMatrixTemplate = QtGui.QPushButton()
        self.buttonSaveAsTransitionMatrixTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsTransitionMatrixTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_SAVE_AS))
        self.layoutButtonTransitionMatrixTemplate.addWidget(self.buttonLoadTransitionMatrixTemplate)
        self.layoutButtonTransitionMatrixTemplate.addWidget(self.buttonSaveTransitionMatrixTemplate)
        self.layoutButtonTransitionMatrixTemplate.addWidget(self.buttonSaveAsTransitionMatrixTemplate)
        self.layoutGroupBoxTransitionMatrixTemplate.addLayout(self.layoutButtonTransitionMatrixTemplate)

        # Process tab button
        self.layoutButtonTransitionMatrix = QtGui.QHBoxLayout()
        self.buttonProcessTransitionMatrix = QtGui.QPushButton()
        self.buttonProcessTransitionMatrix.setText(MenuFactory.getLabel(MenuFactory.SCIENDO_PROCESS))
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
        # 'Create Raster Cube Of Factors' sub tab
        #***********************************************************
        # 'Raster Cube' GroupBox
        self.groupBoxCreateRasterCubeOfFactors = QtGui.QGroupBox(MenuFactory.getLabel(MenuFactory.SCIENDO_LIST_FACTORS))
        self.layoutGroupBoxCreateRasterCubeOfFactors = QtGui.QVBoxLayout()
        self.layoutGroupBoxCreateRasterCubeOfFactors.setAlignment(QtCore.Qt.AlignTop)
        self.groupBoxCreateRasterCubeOfFactors.setLayout(self.layoutGroupBoxCreateRasterCubeOfFactors)
        
        self.layoutCreateRasterCubeOfFactorsInfo = QtGui.QVBoxLayout()
        self.labelCreateRasterCubeOfFactorsInfo = QtGui.QLabel()
        self.labelCreateRasterCubeOfFactorsInfo.setText('\n')
        self.labelCreateRasterCubeOfFactorsInfo.setWordWrap(True)
        self.layoutCreateRasterCubeOfFactorsInfo.addWidget(self.labelCreateRasterCubeOfFactorsInfo)
        
        self.layoutCreateRasterCubeOfFactorsParameters = QtGui.QGridLayout()
        self.layoutCreateRasterCubeOfFactorsParameters.setContentsMargins(0, 0, 0, 0)
        
        self.labelCreateRasterCubeOfFactorsIndex = QtGui.QLabel()
        self.labelCreateRasterCubeOfFactorsIndex.setText(MenuFactory.getLabel(MenuFactory.SCIENDO_SIMULATION_DIRECTORY_INDEX) + ':')
        self.layoutCreateRasterCubeOfFactorsParameters.addWidget(self.labelCreateRasterCubeOfFactorsIndex, 0, 0)
        
        self.comboBoxCreateRasterCubeOfFactorsIndex = QtGui.QComboBox()
        self.comboBoxCreateRasterCubeOfFactorsIndex.setDisabled(True)
        self.layoutCreateRasterCubeOfFactorsParameters.addWidget(self.comboBoxCreateRasterCubeOfFactorsIndex, 0, 1)
        
        self.loadAddedSimulationIndex(self.comboBoxCreateRasterCubeOfFactorsIndex)
        
        self.labelCreateRasterCubeOfFactorsDirectory = QtGui.QLabel()
        self.labelCreateRasterCubeOfFactorsDirectory.setText(MenuFactory.getLabel(MenuFactory.SCIENDO_FACTOR_DIRECTORY) + ':')
        self.layoutCreateRasterCubeOfFactorsParameters.addWidget(self.labelCreateRasterCubeOfFactorsDirectory, 1, 0)
        
        self.lineEditCreateRasterCubeOfFactorsDirectory = QtGui.QLineEdit()
        self.lineEditCreateRasterCubeOfFactorsDirectory.setReadOnly(True)
        self.layoutCreateRasterCubeOfFactorsParameters.addWidget(self.lineEditCreateRasterCubeOfFactorsDirectory, 1, 1)
        
        self.buttonSelectCreateRasterCubeOfFactorsDirectory = QtGui.QPushButton()
        self.buttonSelectCreateRasterCubeOfFactorsDirectory.setText(MenuFactory.getLabel(MenuFactory.SCIENDO_BROWSE))
        self.layoutCreateRasterCubeOfFactorsParameters.addWidget(self.buttonSelectCreateRasterCubeOfFactorsDirectory, 1, 2)
        
        # self.layoutButtonCreateRasterCubeOfFactors = QtGui.QHBoxLayout()
        # self.layoutButtonCreateRasterCubeOfFactors.setContentsMargins(0, 0, 0, 0)
        # self.layoutButtonCreateRasterCubeOfFactors.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        # self.buttonAddFactorRow = QtGui.QPushButton()
        # self.buttonAddFactorRow.setText('Add Factor')
        # self.buttonAddFactorRow.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        # self.layoutButtonCreateRasterCubeOfFactors.addWidget(self.buttonAddFactorRow)
        # 
        # self.layoutContentCreateRasterCubeOfFactors = QtGui.QVBoxLayout()
        # self.layoutContentCreateRasterCubeOfFactors.setContentsMargins(2, 2, 2, 2)
        # self.contentCreateRasterCubeOfFactors = QtGui.QWidget()
        # self.contentCreateRasterCubeOfFactors.setLayout(self.layoutContentCreateRasterCubeOfFactors)
        # self.scrollCreateRasterCubeOfFactors = QtGui.QScrollArea()
        # self.scrollCreateRasterCubeOfFactors.setWidgetResizable(True)
        # self.scrollCreateRasterCubeOfFactors.setWidget(self.contentCreateRasterCubeOfFactors)
        # 
        # self.layoutTableAddFactor = QtGui.QVBoxLayout()
        # self.layoutTableAddFactor.setAlignment(QtCore.Qt.AlignTop)
        # self.layoutContentCreateRasterCubeOfFactors.addLayout(self.layoutTableAddFactor)
        
        self.layoutGroupBoxCreateRasterCubeOfFactors.addLayout(self.layoutCreateRasterCubeOfFactorsInfo)
        self.layoutGroupBoxCreateRasterCubeOfFactors.addLayout(self.layoutCreateRasterCubeOfFactorsParameters)

        # Template GroupBox
        self.groupBoxCreateRasterCubeTemplate = QtGui.QGroupBox(MenuFactory.getLabel(MenuFactory.CONF_TITLE))
        self.layoutGroupBoxCreateRasterCubeTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxCreateRasterCubeTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxCreateRasterCubeTemplate.setLayout(self.layoutGroupBoxCreateRasterCubeTemplate)
        self.layoutCreateRasterCubeTemplateInfo = QtGui.QVBoxLayout()
        self.layoutCreateRasterCubeTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxCreateRasterCubeTemplate.addLayout(self.layoutCreateRasterCubeTemplateInfo)
        self.layoutGroupBoxCreateRasterCubeTemplate.addLayout(self.layoutCreateRasterCubeTemplate)
        
        self.labelLoadedCreateRasterCubeTemplate = QtGui.QLabel()
        self.labelLoadedCreateRasterCubeTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_LOADED_CONFIGURATION) + ':')
        self.layoutCreateRasterCubeTemplate.addWidget(self.labelLoadedCreateRasterCubeTemplate, 0, 0)
        
        self.loadedCreateRasterCubeTemplate = QtGui.QLabel()
        self.loadedCreateRasterCubeTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NONE))
        self.layoutCreateRasterCubeTemplate.addWidget(self.loadedCreateRasterCubeTemplate, 0, 1)
        
        self.labelCreateRasterCubeTemplate = QtGui.QLabel()
        self.labelCreateRasterCubeTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NAME) + ':')
        self.layoutCreateRasterCubeTemplate.addWidget(self.labelCreateRasterCubeTemplate, 1, 0)
        
        self.comboBoxCreateRasterCubeTemplate = QtGui.QComboBox()
        self.comboBoxCreateRasterCubeTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxCreateRasterCubeTemplate.setDisabled(True)
        self.comboBoxCreateRasterCubeTemplate.addItem(MenuFactory.getLabel(MenuFactory.CONF_NO_FOUND))
        self.layoutCreateRasterCubeTemplate.addWidget(self.comboBoxCreateRasterCubeTemplate, 1, 1)
        
        self.layoutButtonCreateRasterCubeTemplate = QtGui.QHBoxLayout()
        self.layoutButtonCreateRasterCubeTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadCreateRasterCubeTemplate = QtGui.QPushButton()
        self.buttonLoadCreateRasterCubeTemplate.setDisabled(True)
        self.buttonLoadCreateRasterCubeTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadCreateRasterCubeTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NO_FOUND))
        self.buttonSaveCreateRasterCubeTemplate = QtGui.QPushButton()
        self.buttonSaveCreateRasterCubeTemplate.setDisabled(True)
        self.buttonSaveCreateRasterCubeTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveCreateRasterCubeTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_SAVE))
        self.buttonSaveAsCreateRasterCubeTemplate = QtGui.QPushButton()
        self.buttonSaveAsCreateRasterCubeTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsCreateRasterCubeTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_SAVE_AS))
        self.layoutButtonCreateRasterCubeTemplate.addWidget(self.buttonLoadCreateRasterCubeTemplate)
        self.layoutButtonCreateRasterCubeTemplate.addWidget(self.buttonSaveCreateRasterCubeTemplate)
        self.layoutButtonCreateRasterCubeTemplate.addWidget(self.buttonSaveAsCreateRasterCubeTemplate)
        self.layoutGroupBoxCreateRasterCubeTemplate.addLayout(self.layoutButtonCreateRasterCubeTemplate)
        
        # Process tab button
        self.layoutButtonCreateRasterCube = QtGui.QHBoxLayout()
        self.buttonProcessCreateRasterCube = QtGui.QPushButton()
        self.buttonProcessCreateRasterCube.setText(MenuFactory.getLabel(MenuFactory.SCIENDO_PROCESS))
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
        self.layoutTabCreateRasterCubeOfFactors.setColumnStretch(1, 1) 


        #***********************************************************
        # 'Calculate Weight of Evidence' sub tab
        #***********************************************************
        # 'WoE' GroupBox
        self.groupBoxCalculateWeightOfEvidence = QtGui.QGroupBox(MenuFactory.getLabel(MenuFactory.SCIENDO_PARAMETERIZATION))
        self.layoutGroupBoxCalculateWeightOfEvidence = QtGui.QVBoxLayout()
        self.layoutGroupBoxCalculateWeightOfEvidence.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxCalculateWeightOfEvidence.setLayout(self.layoutGroupBoxCalculateWeightOfEvidence)
        
        self.layoutCalculateWeightOfEvidenceInfo = QtGui.QVBoxLayout()
        self.labelCalculateWeightOfEvidenceInfo = QtGui.QLabel()
        self.labelCalculateWeightOfEvidenceInfo.setText('\n')
        self.labelCalculateWeightOfEvidenceInfo.setWordWrap(True)
        self.layoutCalculateWeightOfEvidenceInfo.addWidget(self.labelCalculateWeightOfEvidenceInfo)
        
        self.layoutCalculateWeightOfEvidenceParameters = QtGui.QGridLayout()
        self.layoutCalculateWeightOfEvidenceParameters.setContentsMargins(0, 0, 0, 0)
        
        self.labelCalculateWeightOfEvidenceIndex = QtGui.QLabel()
        self.labelCalculateWeightOfEvidenceIndex.setText(MenuFactory.getLabel(MenuFactory.SCIENDO_SIMULATION_DIRECTORY_INDEX) + ':')
        self.layoutCalculateWeightOfEvidenceParameters.addWidget(self.labelCalculateWeightOfEvidenceIndex, 0, 0)
        
        self.comboBoxCalculateWeightOfEvidenceIndex = QtGui.QComboBox()
        self.comboBoxCalculateWeightOfEvidenceIndex.setDisabled(True)
        self.layoutCalculateWeightOfEvidenceParameters.addWidget(self.comboBoxCalculateWeightOfEvidenceIndex, 0, 1)
        
        self.loadAddedSimulationIndex(self.comboBoxCalculateWeightOfEvidenceIndex)
        
        self.labelCalculateWeightOfEvidenceTable = QtGui.QLabel()
        self.labelCalculateWeightOfEvidenceTable.setText(MenuFactory.getLabel(MenuFactory.SCIENDO_LAND_COVER_LOOKUP_TABLE) + ':')
        self.layoutCalculateWeightOfEvidenceParameters.addWidget(self.labelCalculateWeightOfEvidenceTable, 1, 0)
        
        self.comboBoxCalculateWeightOfEvidenceTable = QtGui.QComboBox()
        self.comboBoxCalculateWeightOfEvidenceTable.setDisabled(True)
        self.layoutCalculateWeightOfEvidenceParameters.addWidget(self.comboBoxCalculateWeightOfEvidenceTable, 1, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxCalculateWeightOfEvidenceTable)      
        
        self.layoutGroupBoxCalculateWeightOfEvidence.addLayout(self.layoutCalculateWeightOfEvidenceInfo)
        self.layoutGroupBoxCalculateWeightOfEvidence.addLayout(self.layoutCalculateWeightOfEvidenceParameters)        

        # Template GroupBox
        self.groupBoxCalculateWeightOfEvidenceTemplate = QtGui.QGroupBox(MenuFactory.getLabel(MenuFactory.CONF_TITLE))
        self.layoutGroupBoxCalculateWeightOfEvidenceTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxCalculateWeightOfEvidenceTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxCalculateWeightOfEvidenceTemplate.setLayout(self.layoutGroupBoxCalculateWeightOfEvidenceTemplate)
        self.layoutCalculateWeightOfEvidenceTemplateInfo = QtGui.QVBoxLayout()
        self.layoutCalculateWeightOfEvidenceTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxCalculateWeightOfEvidenceTemplate.addLayout(self.layoutCalculateWeightOfEvidenceTemplateInfo)
        self.layoutGroupBoxCalculateWeightOfEvidenceTemplate.addLayout(self.layoutCalculateWeightOfEvidenceTemplate)
        
        self.labelLoadedCalculateWeightOfEvidenceTemplate = QtGui.QLabel()
        self.labelLoadedCalculateWeightOfEvidenceTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_LOADED_CONFIGURATION) + ':')
        self.layoutCalculateWeightOfEvidenceTemplate.addWidget(self.labelLoadedCalculateWeightOfEvidenceTemplate, 0, 0)
        
        self.loadedCalculateWeightOfEvidenceTemplate = QtGui.QLabel()
        self.loadedCalculateWeightOfEvidenceTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NONE))
        self.layoutCalculateWeightOfEvidenceTemplate.addWidget(self.loadedCalculateWeightOfEvidenceTemplate, 0, 1)
        
        self.labeCalculateWeightOfEvidenceTemplate = QtGui.QLabel()
        self.labeCalculateWeightOfEvidenceTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NAME) + ':')
        self.layoutCalculateWeightOfEvidenceTemplate.addWidget(self.labeCalculateWeightOfEvidenceTemplate, 1, 0)
        
        self.comboBoxCalculateWeightOfEvidenceTemplate = QtGui.QComboBox()
        self.comboBoxCalculateWeightOfEvidenceTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxCalculateWeightOfEvidenceTemplate.setDisabled(True)
        self.comboBoxCalculateWeightOfEvidenceTemplate.addItem(MenuFactory.getLabel(MenuFactory.CONF_NO_FOUND))
        self.layoutCalculateWeightOfEvidenceTemplate.addWidget(self.comboBoxCalculateWeightOfEvidenceTemplate, 1, 1)
        
        self.layoutButtonCalculateWeightOfEvidenceTemplate = QtGui.QHBoxLayout()
        self.layoutButtonCalculateWeightOfEvidenceTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadCalculateWeightOfEvidenceTemplate = QtGui.QPushButton()
        self.buttonLoadCalculateWeightOfEvidenceTemplate.setDisabled(True)
        self.buttonLoadCalculateWeightOfEvidenceTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadCalculateWeightOfEvidenceTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NO_FOUND))
        self.buttonSaveCalculateWeightOfEvidenceTemplate = QtGui.QPushButton()
        self.buttonSaveCalculateWeightOfEvidenceTemplate.setDisabled(True)
        self.buttonSaveCalculateWeightOfEvidenceTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveCalculateWeightOfEvidenceTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_SAVE))
        self.buttonSaveAsCalculateWeightOfEvidenceTemplate = QtGui.QPushButton()
        self.buttonSaveAsCalculateWeightOfEvidenceTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsCalculateWeightOfEvidenceTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_SAVE_AS))
        self.layoutButtonCalculateWeightOfEvidenceTemplate.addWidget(self.buttonLoadCalculateWeightOfEvidenceTemplate)
        self.layoutButtonCalculateWeightOfEvidenceTemplate.addWidget(self.buttonSaveCalculateWeightOfEvidenceTemplate)
        self.layoutButtonCalculateWeightOfEvidenceTemplate.addWidget(self.buttonSaveAsCalculateWeightOfEvidenceTemplate)
        self.layoutGroupBoxCalculateWeightOfEvidenceTemplate.addLayout(self.layoutButtonCalculateWeightOfEvidenceTemplate)
        
        # Process tab button
        self.layoutButtonCalculateWeightOfEvidence = QtGui.QHBoxLayout()
        self.buttonProcessCalculateWeightOfEvidence = QtGui.QPushButton()
        self.buttonProcessCalculateWeightOfEvidence.setText(MenuFactory.getLabel(MenuFactory.SCIENDO_PROCESS))
        self.buttonHelpSCIENDOWeightOfEvidence = QtGui.QPushButton()
        self.buttonHelpSCIENDOWeightOfEvidence.setIcon(icon)
        self.layoutButtonCalculateWeightOfEvidence.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonCalculateWeightOfEvidence.addWidget(self.buttonProcessCalculateWeightOfEvidence)
        self.layoutButtonCalculateWeightOfEvidence.addWidget(self.buttonHelpSCIENDOWeightOfEvidence)
        
        # Place the GroupBoxes
        self.layoutTabCalculateWeightOfEvidence.addWidget(self.groupBoxCalculateWeightOfEvidence, 0, 0)
        self.layoutTabCalculateWeightOfEvidence.addLayout(self.layoutButtonCalculateWeightOfEvidence, 1, 0, 1, 2, QtCore.Qt.AlignRight)
        self.layoutTabCalculateWeightOfEvidence.addWidget(self.groupBoxCalculateWeightOfEvidenceTemplate, 0, 1, 1, 1)
        self.layoutTabCalculateWeightOfEvidence.setColumnStretch(0, 3)
        self.layoutTabCalculateWeightOfEvidence.setColumnStretch(1, 1) 
        
        
        #***********************************************************
        # Setup 'Simulate Land Use Change Modeling' sub tab
        #***********************************************************
        # 'Simulate Land Use Change Modeling' GroupBox
        self.groupBoxLandUseChangeSimulation = QtGui.QGroupBox(MenuFactory.getLabel(MenuFactory.SCIENDO_PARAMETERIZATION))
        self.layoutGroupBoxLandUseChangeSimulation = QtGui.QVBoxLayout()
        self.layoutGroupBoxLandUseChangeSimulation.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLandUseChangeSimulation.setLayout(self.layoutGroupBoxLandUseChangeSimulation)
        
        self.layoutLandUseChangeSimulationInfo = QtGui.QVBoxLayout()
        self.labelLandUseChangeSimulationInfo = QtGui.QLabel()
        self.labelLandUseChangeSimulationInfo.setText('\n')
        self.labelLandUseChangeSimulationInfo.setWordWrap(True)
        self.layoutLandUseChangeSimulationInfo.addWidget(self.labelLandUseChangeSimulationInfo)        
        
        self.layoutLandUseChangeSimulationParameters = QtGui.QGridLayout()
        self.layoutLandUseChangeSimulationParameters.setContentsMargins(0, 0, 0, 0)
        
        self.labelLandUseChangeSimulationIndex = QtGui.QLabel()
        self.labelLandUseChangeSimulationIndex.setText(MenuFactory.getLabel(MenuFactory.SCIENDO_SIMULATION_DIRECTORY_INDEX) + ':')
        self.layoutLandUseChangeSimulationParameters.addWidget(self.labelLandUseChangeSimulationIndex, 0, 0)
        
        self.comboBoxLandUseChangeSimulationIndex = QtGui.QComboBox()
        self.comboBoxLandUseChangeSimulationIndex.setDisabled(True)
        self.layoutLandUseChangeSimulationParameters.addWidget(self.comboBoxLandUseChangeSimulationIndex, 0, 1)
        
        self.loadAddedSimulationIndex(self.comboBoxLandUseChangeSimulationIndex)      
        
        self.labelLandUseChangeSimulationIteration = QtGui.QLabel()
        self.labelLandUseChangeSimulationIteration.setText(MenuFactory.getLabel(MenuFactory.SCIENDO_ITERATION) + ':')
        self.layoutLandUseChangeSimulationParameters.addWidget(self.labelLandUseChangeSimulationIteration, 1, 0)
        
        self.spinBoxLandUseChangeSimulationIteration = QtGui.QSpinBox()
        self.spinBoxLandUseChangeSimulationIteration.setRange(1, 99)
        self.spinBoxLandUseChangeSimulationIteration.setValue(5)
        self.layoutLandUseChangeSimulationParameters.addWidget(self.spinBoxLandUseChangeSimulationIteration, 1, 1)
        
        # self.tableListOfTransitions = QtGui.QTableWidget()
        # self.tableListOfTransitions.setEnabled(True)
        # self.tableListOfTransitions.setRowCount(25)
        # self.tableListOfTransitions.setColumnCount(4)
        # self.tableListOfTransitions.verticalHeader().setVisible(False)
        # self.tableListOfTransitions.setHorizontalHeaderLabels(['From', 'To', 'Percent', 'Patch Size (Ha)'])
        
        self.layoutGroupBoxLandUseChangeSimulation.addLayout(self.layoutLandUseChangeSimulationInfo)
        self.layoutGroupBoxLandUseChangeSimulation.addLayout(self.layoutLandUseChangeSimulationParameters)
        
        # Template GroupBox
        self.groupBoxLandUseChangeSimulationTemplate = QtGui.QGroupBox(MenuFactory.getLabel(MenuFactory.CONF_TITLE))
        self.layoutGroupBoxLandUseChangeSimulationTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxLandUseChangeSimulationTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLandUseChangeSimulationTemplate.setLayout(self.layoutGroupBoxLandUseChangeSimulationTemplate)
        self.layoutLandUseChangeSimulationTemplateInfo = QtGui.QVBoxLayout()
        self.layoutLandUseChangeSimulationTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxLandUseChangeSimulationTemplate.addLayout(self.layoutLandUseChangeSimulationTemplateInfo)
        self.layoutGroupBoxLandUseChangeSimulationTemplate.addLayout(self.layoutLandUseChangeSimulationTemplate)
        
        self.labelLoadedLandUseChangeSimulationTemplate = QtGui.QLabel()
        self.labelLoadedLandUseChangeSimulationTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_LOADED_CONFIGURATION) + ':')
        self.layoutLandUseChangeSimulationTemplate.addWidget(self.labelLoadedLandUseChangeSimulationTemplate, 0, 0)
        
        self.loadedLandUseChangeSimulationTemplate = QtGui.QLabel()
        self.loadedLandUseChangeSimulationTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NONE))
        self.layoutLandUseChangeSimulationTemplate.addWidget(self.loadedLandUseChangeSimulationTemplate, 0, 1)
        
        self.labelLandUseChangeSimulationTemplate = QtGui.QLabel()
        self.labelLandUseChangeSimulationTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NAME) + ':')
        self.layoutLandUseChangeSimulationTemplate.addWidget(self.labelLandUseChangeSimulationTemplate, 1, 0)
        
        self.comboBoxLandUseChangeSimulationTemplate = QtGui.QComboBox()
        self.comboBoxLandUseChangeSimulationTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxLandUseChangeSimulationTemplate.setDisabled(True)
        self.comboBoxLandUseChangeSimulationTemplate.addItem(MenuFactory.getLabel(MenuFactory.CONF_NO_FOUND))
        self.layoutLandUseChangeSimulationTemplate.addWidget(self.comboBoxLandUseChangeSimulationTemplate, 1, 1)
        
        self.layoutButtonLandUseChangeSimulationTemplate = QtGui.QHBoxLayout()
        self.layoutButtonLandUseChangeSimulationTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadLandUseChangeSimulationTemplate = QtGui.QPushButton()
        self.buttonLoadLandUseChangeSimulationTemplate.setDisabled(True)
        self.buttonLoadLandUseChangeSimulationTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadLandUseChangeSimulationTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NO_FOUND))
        self.buttonSaveLandUseChangeSimulationTemplate = QtGui.QPushButton()
        self.buttonSaveLandUseChangeSimulationTemplate.setDisabled(True)
        self.buttonSaveLandUseChangeSimulationTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveLandUseChangeSimulationTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_SAVE))
        self.buttonSaveAsLandUseChangeSimulationTemplate = QtGui.QPushButton()
        self.buttonSaveAsLandUseChangeSimulationTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsLandUseChangeSimulationTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_SAVE_AS))
        self.layoutButtonLandUseChangeSimulationTemplate.addWidget(self.buttonLoadLandUseChangeSimulationTemplate)
        self.layoutButtonLandUseChangeSimulationTemplate.addWidget(self.buttonSaveLandUseChangeSimulationTemplate)
        self.layoutButtonLandUseChangeSimulationTemplate.addWidget(self.buttonSaveAsLandUseChangeSimulationTemplate)
        self.layoutGroupBoxLandUseChangeSimulationTemplate.addLayout(self.layoutButtonLandUseChangeSimulationTemplate)
        
        # Process tab button
        self.layoutButtonLandUseChangeSimulation = QtGui.QHBoxLayout()
        self.buttonProcessLandUseChangeSimulation = QtGui.QPushButton()
        self.buttonProcessLandUseChangeSimulation.setText(MenuFactory.getLabel(MenuFactory.SCIENDO_PROCESS))
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
        self.labelHistoryLogInfo.setText('\n')
        self.layoutHistoryLogInfo.addWidget(self.labelHistoryLogInfo)
        
        self.log_box = QPlainTextEditLogger(self)
        self.layoutHistoryLog.addWidget(self.log_box.widget)
        
        self.layoutTabLog.addWidget(self.groupBoxHistoryLog)
        
        
        self.setLayout(self.dialogLayout)
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(900, 640)
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
            labelQUESCDatabaseHistoricalBaselineAnnualProjection.setText(MenuFactory.getLabel(MenuFactory.MSG_SCIENDO_NO_QUESC_DB))
            layoutCheckBoxQUESCDatabase.addWidget(labelQUESCDatabaseHistoricalBaselineAnnualProjection)
            
        self.layoutOptionsHistoricalBaselineAnnualProjection.addLayout(layoutCheckBoxQUESCDatabase)


    def loadAddedSimulationIndex(self, comboBox):
        """Method for loading the list of added data.
    
        Looks in the Project SCIENDO dir of the currently open project.
        """
        csvSimulationIndex = os.path.join(self.main.appSettings['DialogLumensOpenDatabase']['projectFolder'], self.main.appSettings['folderSCIENDO'], 'list_of_idx_lusim.csv')
        
        if os.path.exists(csvSimulationIndex):
            with open(csvSimulationIndex, 'rb') as f:
                reader = csv.reader(f)
                next(reader)
                
                comboBox.clear()
                for row in reader:
                    comboBox.addItem(row[0])
                
                comboBox.setEnabled(True)
                    
    
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
                MenuFactory.getLabel(MenuFactory.CONF_LOAD_TEMPLATE),
                MenuFactory.getDescription(MenuFactory.CONF_LOAD_TEMPLATE) + ' \'{0}\'?'.format(templateFile),
                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                QtGui.QMessageBox.No
            )
            
        if reply == QtGui.QMessageBox.Yes or fileName:
            self.loadTemplate(MenuFactory.getLabel(MenuFactory.SCIENDO_LED), templateFile)
    
    
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
            MenuFactory.getLabel(MenuFactory.CONF_SAVE_TEMPLATE),
            MenuFactory.getDescription(MenuFactory.CONF_SAVE_TEMPLATE),
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
            QtGui.QMessageBox.No
        )
            
        if reply == QtGui.QMessageBox.Yes:
            self.saveTemplate(MenuFactory.getLabel(MenuFactory.SCIENDO_LED), templateFile)
            return True
        else:
            return False
    
    
    def handlerSaveAsLowEmissionDevelopmentAnalysisTemplate(self):
        """Slot method for saving a module template to a new file.
        """
        fileName, ok = QtGui.QInputDialog.getText(self, MenuFactory.getLabel(MenuFactory.CONF_SAVE_AS), MenuFactory.getDescription(MenuFactory.CONF_SAVE_AS) + ';')
        fileSaved = False
        
        if ok:
            now = QtCore.QDateTime.currentDateTime().toString('yyyyMMdd-hhmmss')
            fileName = now + '__' + fileName + '.ini'
            
            if os.path.exists(os.path.join(self.settingsPath, fileName)):
                fileSaved = self.handlerSaveLowEmissionDevelopmentAnalysisTemplate(fileName)
            else:
                self.saveTemplate(MenuFactory.getLabel(MenuFactory.SCIENDO_LED), fileName)
                fileSaved = True
            
            self.loadTemplateFiles()
            
            # Load the newly saved template file
            if fileSaved:
                self.handlerLoadLowEmissionDevelopmentAnalysisTemplate(fileName)
          
    
    def handlerSelectDriversAnalysisLandUseCoverChangeDrivers(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, MenuFactory.getLabel(MenuFactory.MSG_SCIENDO_SELECT_LAND_USE_DRIVERS), QtCore.QDir.homePath(), MenuFactory.getDescription(MenuFactory.MSG_SCIENDO_SELECT_LAND_USE_DRIVERS) + ' (*{0})'.format(self.main.appSettings['selectTextfileExt'])))
        
        if file:
            self.lineEditDriversAnalysisLandUseCoverChangeDrivers.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectBuildScenarioHistoricalBaselineCar(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, MenuFactory.getLabel(MenuFactory.MSG_SCIENDO_SELECT_HISTORICAL_BASELINE_CAR), QtCore.QDir.homePath(), MenuFactory.getLabel(MenuFactory.MSG_SCIENDO_SELECT_HISTORICAL_BASELINE_CAR) + ' (*{0})'.format(self.main.appSettings['selectCarfileExt'])))
        
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
                MenuFactory.getLabel(MenuFactory.CONF_LOAD_TEMPLATE),
                MenuFactory.getDescription(MenuFactory.CONF_LOAD_TEMPLATE) + ' \'{0}\'?'.format(templateFile),
                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                QtGui.QMessageBox.No
            )
            
        if reply == QtGui.QMessageBox.Yes or fileName:
            self.loadTemplate(MenuFactory.getLabel(MenuFactory.SCIENDO_LUCM), templateFile)
    
    
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
            MenuFactory.getLabel(MenuFactory.CONF_SAVE_TEMPLATE),
            MenuFactory.getDescription(MenuFactory.CONF_SAVE_TEMPLATE),
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
            QtGui.QMessageBox.No
        )
            
        if reply == QtGui.QMessageBox.Yes:
            self.saveTemplate(MenuFactory.getLabel(MenuFactory.SCIENDO_LUCM), templateFile)
            return True
        else:
            return False
    
    
    def handlerSaveAsLandUseChangeModelingTemplate(self):
        """Slot method for saving a module template to a new file.
        """
        fileName, ok = QtGui.QInputDialog.getText(self, MenuFactory.getLabel(MenuFactory.CONF_SAVE_AS), MenuFactory.getDescription(MenuFactory.CONF_SAVE_AS) + ';')
        fileSaved = False
        
        if ok:
            now = QtCore.QDateTime.currentDateTime().toString('yyyyMMdd-hhmmss')
            fileName = now + '__' + fileName + '.ini'
            
            if os.path.exists(os.path.join(self.settingsPath, fileName)):
                fileSaved = self.handlerSaveLandUseChangeModelingTemplate(fileName)
            else:
                self.saveTemplate(MenuFactory.getLabel(MenuFactory.SCIENDO_LUCM), fileName)
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
        dir = unicode(QtGui.QFileDialog.getExistingDirectory(self, MenuFactory.getLabel(MenuFactory.MSG_SCIENDO_SELECT_FACTORS_DIR)))
        
        if dir:
            self.lineEditCreateRasterCubeOfFactorsDirectory.setText(dir)
            logging.getLogger(type(self).__name__).info('select directory: %s', dir)
    
    
    def handlerSelectLandUseChangeModelingLandUseLookup(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, MenuFactory.getLabel(MenuFactory.MSG_SCIENDO_SELECT_LAND_USE_LOOKUP_TABLE), QtCore.QDir.homePath(), MenuFactory.getDescription(MenuFactory.MSG_SCIENDO_SELECT_LAND_USE_LOOKUP_TABLE) + ' (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
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
        
        # 'Calculate transition matrix' groupbox fields
        self.main.appSettings['DialogLumensSCIENDOCalculateTransitionMatrix']['landUse1'] \
            = unicode(self.comboBoxTransitionMatrixInitialMap.currentText())
        self.main.appSettings['DialogLumensSCIENDOCalculateTransitionMatrix']['landUse2'] \
            = unicode(self.comboBoxTransitionMatrixFinalMap.currentText())
        self.main.appSettings['DialogLumensSCIENDOCalculateTransitionMatrix']['planningUnit'] \
            = unicode(self.comboBoxTransitionMatrixRegions.currentText())
        
        # 'Create factor raster cube' groupbox fields
        self.main.appSettings['DialogLumensSCIENDOCreateRasterCube']['simulationIndex'] \
            = unicode(self.comboBoxCreateRasterCubeOfFactorsIndex.currentText())
        self.main.appSettings['DialogLumensSCIENDOCreateRasterCube']['factorsDir'] \
            = unicode(self.lineEditCreateRasterCubeOfFactorsDirectory.text()).replace(os.path.sep, '/')
        
        # 'Create factor raster cube' groupbox fields
        self.main.appSettings['DialogLumensSCIENDOCalculateWeightofEvidence']['simulationIndex'] \
            = unicode(self.comboBoxCalculateWeightOfEvidenceIndex.currentText())
        self.main.appSettings['DialogLumensSCIENDOCalculateWeightofEvidence']['landUseLookup'] \
            = unicode(self.comboBoxCalculateWeightOfEvidenceTable.currentText())
        
        # 'Simulate land use' tab fields
        self.main.appSettings['DialogLumensSCIENDOSimulateLandUseChange']['simulationIndex'] \
            = unicode(self.comboBoxLandUseChangeSimulationIndex.currentText())
        self.main.appSettings['DialogLumensSCIENDOSimulateLandUseChange']['iteration'] \
            = self.spinBoxLandUseChangeSimulationIteration.value()        
    
    
    def handlerProcessLowEmissionDevelopmentAnalysis(self):
        """Slot method to pass the form values and execute the "SCIENDO Low Emission Development Analysis" R algorithms.
        
        Depending on the checked groupbox, the "SCIENDO Low Emission Development Analysis" process calls the following algorithms:
        1. r:sciendoperiodprojection
        2. r:sciendoannualprojection
        3. r:sciendodriversanalysis
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
                QtGui.QMessageBox.information(self, MenuFactory.getLabel(MenuFactory.SCIENDO_HISTORICAL_BASELINE_ANNUAL_PROJECTION), MenuFactory.getLabel(MenuFactory.MSG_SCIENDO_CHOOSE_QUESC_DB))
                return 
        
        
        if self.checkBoxDriversAnalysis.isChecked():
            formName = 'DialogLumensSCIENDODriversAnalysis'
            algName = 'r:sciendodriversanalysis'
            
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
            algName = 'r:sciendobuildscenario'
            
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
    

    def handlerProcessTransitionMatrix(self):
        """Slot method to pass the form values and execute the "SCIENDO Land Use Simulation" R algorithms.
        
        "Calculate Transition Matrix" process calls the following algorithms:
        1. r:sciendo_lusim_calculate_transition
        """
        self.setAppSettings()
        
        algName = 'r:sciendolusimcalculatetransition'
        formName = 'DialogLumensSCIENDOCalculateTransitionMatrix'
        activeProject = self.main.appSettings['DialogLumensOpenDatabase']['projectFile'].replace(os.path.sep, '/')
        
        if self.validForm(formName):
            logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
            logging.getLogger(self.historyLog).info('alg start: %s' % formName)
            self.buttonProcessTransitionMatrix.setDisabled(True)
            
            # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
            self.main.setWindowState(QtCore.Qt.WindowMinimized)
            
            outputs = general.runalg(
                algName,
                activeProject,
                self.main.appSettings[formName]['landUse1'],
                self.main.appSettings[formName]['landUse2'],
                self.main.appSettings[formName]['planningUnit'],
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
                self.loadAddedSimulationIndex(self.comboBoxCreateRasterCubeOfFactorsIndex)
                self.loadAddedSimulationIndex(self.comboBoxCalculateWeightOfEvidenceIndex)
                self.loadAddedSimulationIndex(self.comboBoxLandUseChangeSimulationIndex)
            
            self.buttonProcessTransitionMatrix.setEnabled(True)
            logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
            logging.getLogger(self.historyLog).info('alg end: %s' % formName)
            
    
    def handlerProcessCreateRasterCube(self):
        """Slot method to pass the form values and execute the "SCIENDO Land Use Simulation" R algorithms.
        
        "Create Factor Raster Cube" process calls the following algorithms:
        1. r:sciendo_lusim_raster_cube
        """
        self.setAppSettings()
        
        algName = 'r:sciendolusimrastercube'
        formName = 'DialogLumensSCIENDOCreateRasterCube'
        activeProject = self.main.appSettings['DialogLumensOpenDatabase']['projectFile'].replace(os.path.sep, '/')
        
        if self.validForm(formName):
            logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
            logging.getLogger(self.historyLog).info('alg start: %s' % formName)
            self.buttonProcessCreateRasterCube.setDisabled(True)
            
            # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
            self.main.setWindowState(QtCore.Qt.WindowMinimized)
            
            outputs = general.runalg(
                algName,
                activeProject,
                self.main.appSettings[formName]['simulationIndex'],
                self.main.appSettings[formName]['factorsDir'],
                None,
            )
            
            # Display ROut file in debug mode
            if self.main.appSettings['debug']:
                dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                dialog.exec_()
            
            ##print outputs
            
            # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
            self.main.setWindowState(QtCore.Qt.WindowActive)
            
            self.outputsMessageBox(algName, outputs, '', '')
            
            self.buttonProcessCreateRasterCube.setEnabled(True)
            logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
            logging.getLogger(self.historyLog).info('alg end: %s' % formName)        


    def handlerProcessCalculateWeightOfEvidence(self):
        """Slot method to pass the form values and execute the "SCIENDO Land Use Simulation" R algorithms.
        
        "Calculate Weight Of Evidence" process calls the following algorithms:
        1. r:sciendo_lusim_woe
        """
        self.setAppSettings()
        
        algName = 'r:sciendolusimwoe'
        formName = 'DialogLumensSCIENDOCalculateWeightofEvidence'
        activeProject = self.main.appSettings['DialogLumensOpenDatabase']['projectFile'].replace(os.path.sep, '/')
        
        if self.validForm(formName):
            logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
            logging.getLogger(self.historyLog).info('alg start: %s' % formName)
            self.buttonProcessCalculateWeightOfEvidence.setDisabled(True)
            
            # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
            self.main.setWindowState(QtCore.Qt.WindowMinimized)
            
            outputs = general.runalg(
                algName,
                activeProject,
                self.main.appSettings[formName]['simulationIndex'],
                self.main.appSettings[formName]['landUseLookup'],
                None,
            )
            
            # Display ROut file in debug mode
            if self.main.appSettings['debug']:
                dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                dialog.exec_()
            
            ##print outputs
            
            # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
            self.main.setWindowState(QtCore.Qt.WindowActive)
            
            self.outputsMessageBox(algName, outputs, '', '')
            
            self.buttonProcessCalculateWeightOfEvidence.setEnabled(True)
            logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
            logging.getLogger(self.historyLog).info('alg end: %s' % formName) 


    def handlerProcessSimulateLandUse(self):
        """Slot method to pass the form values and execute the "SCIENDO Land Use Simulation" R algorithms.
        
        "Calculate Weight Of Evidence" process calls the following algorithms:
        1. r:sciendo_lusim_simulate
        """
        self.setAppSettings()
        
        algName = 'r:sciendolusimsimulate'
        formName = 'DialogLumensSCIENDOSimulateLandUseChange'
        activeProject = self.main.appSettings['DialogLumensOpenDatabase']['projectFile'].replace(os.path.sep, '/')
        
        if self.validForm(formName):
            logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
            logging.getLogger(self.historyLog).info('alg start: %s' % formName)
            self.buttonProcessLandUseChangeSimulation.setDisabled(True)
            
            # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
            self.main.setWindowState(QtCore.Qt.WindowMinimized)
            
            outputs = general.runalg(
                algName,
                activeProject,
                self.main.appSettings[formName]['simulationIndex'],
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
            
            self.outputsMessageBox(algName, outputs, '', '')
            
            self.buttonProcessLandUseChangeSimulation.setEnabled(True)
            logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
            logging.getLogger(self.historyLog).info('alg end: %s' % formName) 
            
    
