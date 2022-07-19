#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, glob, tempfile, csv
from qgis.core import *
# from processing.tools import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from utils import QPlainTextEditLogger
from dialog_lumens_base import DialogLumensBase
from dialog_lumens_pur_referenceclasses import DialogLumensPURReferenceClasses
from dialog_lumens_viewer import DialogLumensViewer
import resource

from menu_factory import MenuFactory

class DialogLumensPUR(QDialog): # DialogLumensBase
    """LUMENS "PUR" module dialog class.
    """
    
    def loadTemplateFiles(self):
        """Method for loading the list of module template files inside the project folder.
        
        This method is also called to load the module template files in the main window dashboard tab.
        """
        templateFiles = [os.path.basename(name) for name in glob.glob(os.path.join(self.settingsPath, '*.ini')) if os.path.isfile(os.path.join(self.settingsPath, name))]
        
        if templateFiles:
            self.comboBoxPURTemplate.clear()
            self.comboBoxPURTemplate.addItems(sorted(templateFiles))
            self.comboBoxPURTemplate.setEnabled(True)
            self.buttonLoadPURTemplate.setEnabled(True)
            
            # MainWindow PUR dashboard templates
            self.main.comboBoxPURTemplate.clear()
            self.main.comboBoxPURTemplate.addItems(sorted(templateFiles))
            self.main.comboBoxPURTemplate.setEnabled(True)
            self.main.buttonProcessPURTemplate.setEnabled(True)
        else:
            self.comboBoxPURTemplate.setDisabled(True)
            self.buttonLoadPURTemplate.setDisabled(True)
            
            # MainWindow PUR dashboard templates
            self.main.comboBoxPURTemplate.setDisabled(True)
            self.main.buttonProcessPURTemplate.setDisabled(True)
    
    
    def loadTemplate(self, tabName, templateFile, returnTemplateSettings=False):
        """Method for loading the values saved in the module template file to the form widgets.
        
        Args:
            tabName (str): the tab where the form widget values will be populated.
            templateFile (str): a file path to the template file that will be loaded.
            returnTemplateSettings (bool): if true return a dict of the settings in the template file.
        """
        templateFilePath = os.path.join(self.settingsPath, templateFile)
        settings = QtCore.QSettings(templateFilePath, QtCore.QSettings.IniFormat)
        settings.setFallbacksEnabled(True) # only use ini files
        
        templateSettings = {}
        dialogsToLoad = None
        
        if tabName == 'Setup':
            dialogsToLoad = (
                'DialogLumensPUR',
            )
            
            # start tab
            settings.beginGroup(tabName)
            
            # 'Setup' tab widgets
            # start dialog
            settings.beginGroup('DialogLumensPUR')
            
            templateSettings['DialogLumensPUR'] = {}
            templateSettings['DialogLumensPUR']['referenceData'] = referenceData = settings.value('referenceData')
            templateSettings['DialogLumensPUR']['referenceClasses'] = referenceClasses = settings.value('referenceClasses')
            templateSettings['DialogLumensPUR']['referenceMapping'] = referenceMapping = settings.value('referenceMapping')
            templateSettings['DialogLumensPUR']['planningUnits'] = planningUnits = settings.value('planningUnits')
            
            if not returnTemplateSettings:
                if referenceData:
                    indexReferenceData = self.comboBoxReferenceData.findText(referenceData)
                    if indexReferenceData != -1:
                        self.comboBoxReferenceData.setCurrentIndex(referenceData)
                if referenceClasses:
                    self.updateReferenceClasses(referenceClasses)
                if referenceMapping:
                    self.updateReferenceMapping(referenceMapping)
                if planningUnits:
                    self.updatePlanningUnits(planningUnits)
                    
                self.currentPURTemplate = templateFile
                self.loadedPURTemplate.setText(templateFile)
                self.comboBoxPURTemplate.setCurrentIndex(self.comboBoxPURTemplate.findText(templateFile))
                self.buttonSavePURTemplate.setEnabled(True)
                
                # Log to history log
                logging.getLogger(self.historyLog).info('Loaded configuration: %s', templateFile)
            
            settings.endGroup()
            # /dialog
            
            settings.endGroup()
            # /tab
            
        if returnTemplateSettings:
            return templateSettings
        
        """
        print 'DEBUG'
        settings.beginGroup(tabName)
        for dialog in dialogsToLoad:
            settings.beginGroup(dialog)
            for key in self.main.appSettings[dialog].keys():
                print key, settings.value(key)
            settings.endGroup()
        settings.endGroup()
        """
    
    
    def checkForDuplicateTemplates(self, tabName, templateToSkip):
        """Method for checking whether the new template values to be saved already exists in a saved template file.
        
        Args:
            tabName (str): the tab to be checked.
            templateToSkip (str): the template file to skip (when saving an existing template file).
        """
        duplicateTemplate = None
        templateFiles = [os.path.basename(name) for name in glob.glob(os.path.join(self.settingsPath, '*.ini')) if os.path.isfile(os.path.join(self.settingsPath, name))]
        dialogsToLoad = None
        
        if tabName == 'Setup':
            dialogsToLoad = (
                'DialogLumensPUR',
            )
        
        for templateFile in templateFiles:
            if templateFile == templateToSkip:
                continue
            
            duplicateTemplate = templateFile
            templateSettings = self.loadTemplate(tabName, templateFile, True)
            
            print('DEBUG')
            print(templateFile, templateSettings)
            
            # Loop thru all dialogs in a tab
            for dialog in dialogsToLoad:
                # Loop thru all settings in a dialog
                for key, val in self.main.appSettings[dialog].iteritems():
                    if templateSettings[dialog][key] != val:
                        # A setting doesn't match! This is not a matching template file, move along
                        duplicateTemplate = None
                    else:
                        print('DEBUG equal settings')
                        print(templateSettings[dialog][key], val)
        
        # Found a duplicate template, offer to load it?
        if duplicateTemplate:
            reply = QtGui.QMessageBox.question(
                self,
                MenuFactory.getLabel(MenuFactory.CONF_LOAD_EXISTING_CONFIGURATION),
                MenuFactory.getDescription(MenuFactory.CONF_LOAD_EXISTING_CONFIGURATION) + ' \'{0}\'?'.format(duplicateTemplate),
                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                QtGui.QMessageBox.No
            )
            
            if reply == QtGui.QMessageBox.Yes:
                self.handlerLoadPURTemplate(duplicateTemplate)
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
            templateFilePath = os.path.join(self.main.appSettings['DialogLumensOpenDatabase']['projectFolder'], self.main.appSettings['folderPUR'], fileName)
            settings = QtCore.QSettings(templateFilePath, QtCore.QSettings.IniFormat)
            settings.setFallbacksEnabled(True) # only use ini files
            
            dialogsToSave = None
            
            if tabName == 'Setup':
                dialogsToSave = (
                    'DialogLumensPUR',
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
        super(DialogLumensPUR, self).__init__(parent)
        
        self.main = parent
        self.dialogTitle = 'PUR'
        self.settingsPath = os.path.join(self.main.appSettings['DialogLumensOpenDatabase']['projectFolder'], self.main.appSettings['folderPUR'])
        self.currentPURTemplate = None
        
        # default Reference Classes
        self.referenceClasses = {
            1: MenuFactory.getLabel(MenuFactory.PURBUILD_CONSERVATION),
            2: MenuFactory.getLabel(MenuFactory.PURBUILD_PRODUCTION),
            3: MenuFactory.getLabel(MenuFactory.PURBUILD_OTHER),
        }
        self.tableReferenceMappingData = {}
        self.tablePlanningUnitRowCount = 0
        self.tablePlanningUnitData = []
        
        # Init logging
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Module debug log to stdout and file
        if self.main.appSettings['debug']:
            print('DEBUG: DialogLumensPUR init')
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
        # self.historyLog = '{0}{1}'.format('history', type(self).__name__)
        # self.historyLogPath = os.path.join(self.settingsPath, self.historyLog + '.log')
        # self.historyLogger = logging.getLogger(self.historyLog)
        # fh = logging.FileHandler(self.historyLogPath)
        # fh.setFormatter(formatter)
        # self.log_box.setFormatter(formatter)
        # self.historyLogger.addHandler(fh)
        # self.historyLogger.addHandler(self.log_box)
        # self.historyLogger.setLevel(logging.INFO)
        
        # self.loadHistoryLog()
        
        # self.loadTemplateFiles()
        
        self.tabWidget.currentChanged.connect(self.handlerTabWidgetChanged)
        self.buttonProcessSetup.clicked.connect(self.handlerProcessSetup)
        self.buttonHelp.clicked.connect(lambda:self.handlerDialogHelp('PUR'))
        self.buttonLoadPURTemplate.clicked.connect(self.handlerLoadPURTemplate)
        self.buttonSavePURTemplate.clicked.connect(self.handlerSavePURTemplate)
        self.buttonSaveAsPURTemplate.clicked.connect(self.handlerSaveAsPURTemplate)
        # 'Setup reference' buttons
        self.buttonEditReferenceClasses.clicked.connect(self.handlerEditReferenceClasses)
        self.buttonLoadLookupTableReferenceData.clicked.connect(self.handlerLoadLookupTableReference)
        # 'Setup planning unit' buttons
        self.buttonAddPlanningUnitRow.clicked.connect(self.handlerButtonAddPlanningUnitRow)
        self.buttonClearAllPlanningUnits.clicked.connect(self.handlerButtonClearAllPlanningUnits)
        # 'Reconcile' tab button
        self.buttonProcessReconcile.clicked.connect(self.handlerProcessReconcile)
    
    
    def setupUi(self, parent):
        """Method for building the dialog UI.
        
        Args:
            parent: the dialog's parent instance.
        """
        self.setStyleSheet('QDialog { background-color: rgb(225, 229, 237); }')
        self.dialogLayout = QVBoxLayout()

        self.groupBoxPURDialog = QGroupBox(MenuFactory.getDescription(MenuFactory.PUR_TITLE))
        self.layoutGroupBoxPURDialog = QVBoxLayout()
        self.layoutGroupBoxPURDialog.setAlignment(Qt.AlignTop)
        self.groupBoxPURDialog.setLayout(self.layoutGroupBoxPURDialog)
        self.labelPURDialogInfo = QLabel()
        self.labelPURDialogInfo.setText('\n ')
        self.labelPURDialogInfo.setWordWrap(True)
        self.layoutGroupBoxPURDialog.addWidget(self.labelPURDialogInfo)

        self.tabWidget = QTabWidget()
        tabWidgetStylesheet = """
        QTabWidget::pane {
            border: none;
            background-color: rgb(244, 248, 252);
        }
        QTabBar::tab {
            background-color: rgb(174, 176, 178);
            color: rgb(95, 98, 102);
            height: 35px; 
            width: 100px;  
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
        
        self.tabSetup = QWidget()
        self.tabReconcile = QWidget()
        self.tabLog = QWidget()
        
        self.tabWidget.addTab(self.tabSetup, MenuFactory.getLabel(MenuFactory.PURBUILD_BUILD))
        self.tabWidget.addTab(self.tabReconcile, MenuFactory.getLabel(MenuFactory.PURRECONCILE_RECONCILE))
        self.tabWidget.addTab(self.tabLog, MenuFactory.getLabel(MenuFactory.PURLOG_LOG))
        
        ##self.layoutTabSetup = QtGui.QVBoxLayout()
        self.layoutTabSetup = QGridLayout()
        self.layoutTabReconcile = QVBoxLayout()
        self.layoutTabLog = QVBoxLayout()

        self.dialogLayout.addWidget(self.groupBoxPURDialog)
        self.dialogLayout.addWidget(self.tabWidget)
        #self.setStyleSheet('QWidget { background-color: #ccc; }')
        ##self.dialogLayout.setContentsMargins(10, 10, 10, 10)
        
        #***********************************************************
        # Setup 'Create reference data' tab
        #***********************************************************
        
        # 'Setup reference' GroupBox
        self.groupBoxSetupReference = QGroupBox(MenuFactory.getLabel(MenuFactory.PURBUILD_SETUP_REFERENCE))
        self.layoutGroupBoxSetupReference = QVBoxLayout()
        self.layoutGroupBoxSetupReference.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.groupBoxSetupReference.setLayout(self.layoutGroupBoxSetupReference)
        self.layoutSetupReferenceInfo = QVBoxLayout()
        self.layoutSetupReferenceOptions = QGridLayout()
        self.layoutGroupBoxSetupReference.addLayout(self.layoutSetupReferenceInfo)
        self.layoutGroupBoxSetupReference.addLayout(self.layoutSetupReferenceOptions)
        
        self.labelSetupReferenceInfo = QLabel()
        self.labelSetupReferenceInfo.setText('\n')
        self.labelSetupReferenceInfo.setWordWrap(True)
        self.layoutSetupReferenceInfo.addWidget(self.labelSetupReferenceInfo)
        
        self.labelShapefile = QLabel()
        self.labelShapefile.setText(MenuFactory.getLabel(MenuFactory.PURBUILD_REFERENCE_DATA) + ':')
        self.layoutSetupReferenceOptions.addWidget(self.labelShapefile, 0, 0)
        self.comboBoxReferenceData = QComboBox()
        self.comboBoxReferenceData.setDisabled(True)
        self.layoutSetupReferenceOptions.addWidget(self.comboBoxReferenceData, 0, 1)
        DialogLumensBase.handlerPopulateNameFromLookupData(parent, self.main.dataPlanningUnit, self.comboBoxReferenceData)
        self.buttonLoadLookupTableReferenceData = QPushButton()
        self.buttonLoadLookupTableReferenceData.setText(MenuFactory.getLabel(MenuFactory.PURBUILD_LOAD_TABLE))
        self.layoutSetupReferenceOptions.addWidget(self.buttonLoadLookupTableReferenceData, 0, 2)
        self.labelReferenceClasses = QLabel()
        self.labelReferenceClasses.setText(MenuFactory.getLabel(MenuFactory.PURBUILD_REFERENCE_CLASS) + ':')
        self.layoutSetupReferenceOptions.addWidget(self.labelReferenceClasses, 1, 0)
        self.buttonEditReferenceClasses = QPushButton()
        self.buttonEditReferenceClasses.setText(MenuFactory.getLabel(MenuFactory.PURBUILD_EDIT_CLASS))
        self.buttonEditReferenceClasses.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.layoutSetupReferenceOptions.addWidget(self.buttonEditReferenceClasses, 1, 1)
        
        #######################################################################
        # 'Attribute reference mapping' GroupBox
        self.groupBoxReferenceMapping = QGroupBox(MenuFactory.getLabel(MenuFactory.PURBUILD_ATTRIBUTE_REFERENCE_MAPPING))
        self.layoutGroupBoxReferenceMapping = QVBoxLayout()
        self.layoutGroupBoxReferenceMapping.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.groupBoxReferenceMapping.setLayout(self.layoutGroupBoxReferenceMapping)
        
        self.layoutReferenceMappingInfo = QVBoxLayout()
        self.labelReferenceMappingInfo = QLabel()
        self.labelReferenceMappingInfo.setText('\n')
        self.labelReferenceMappingInfo.setWordWrap(True)
        self.layoutReferenceMappingInfo.addWidget(self.labelReferenceMappingInfo)
        
        self.tableReferenceMapping = QTableWidget()
        self.tableReferenceMapping.setRowCount(1)
        self.tableReferenceMapping.setColumnCount(2)
        self.tableReferenceMapping.setSelectionMode(QAbstractItemView.NoSelection)
        self.tableReferenceMapping.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableReferenceMapping.verticalHeader().setVisible(False)
        self.tableReferenceMapping.setHorizontalHeaderLabels([MenuFactory.getLabel(MenuFactory.PURBUILD_ATTRIBUTE_VALUE), MenuFactory.getLabel(MenuFactory.PURBUILD_REFERENCE_CLASS)])
        # self.tableReferenceMapping.horizontalHeader().setResizeMode(0, QHeaderView.ResizeToContents)
        
        attribute = QTableWidgetItem('ATTRIBUTE_VALUE')
        comboBoxReferenceClasses = QComboBox()
        
        for key, val in iter(self.referenceClasses.items()):
            comboBoxReferenceClasses.addItem(val, key)
        
        self.tableReferenceMapping.setItem(0, 0, attribute)
        self.tableReferenceMapping.setCellWidget(0, 1, comboBoxReferenceClasses)
        
        self.layoutGroupBoxReferenceMapping.addLayout(self.layoutReferenceMappingInfo)
        self.layoutGroupBoxReferenceMapping.addWidget(self.tableReferenceMapping)
        
        #######################################################################
        
        # 'Setup planning unit' GroupBox
        self.groupBoxSetupPlanningUnit = QGroupBox(MenuFactory.getLabel(MenuFactory.PURBUILD_SETUP_PLANNING_UNIT))
        self.layoutGroupBoxSetupPlanningUnit = QVBoxLayout()
        self.layoutGroupBoxSetupPlanningUnit.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.groupBoxSetupPlanningUnit.setLayout(self.layoutGroupBoxSetupPlanningUnit)
        
        self.layoutSetupPlanningUnitInfo = QVBoxLayout()
        self.labelSetupPlanningUnitInfo = QLabel()
        self.labelSetupPlanningUnitInfo.setText('\n')
        self.labelSetupPlanningUnitInfo.setWordWrap(True)
        self.layoutSetupPlanningUnitInfo.addWidget(self.labelSetupPlanningUnitInfo)
        
        self.layoutButtonSetupPlanningUnit = QHBoxLayout()
        self.layoutButtonSetupPlanningUnit.setContentsMargins(0, 0, 0, 0)
        self.layoutButtonSetupPlanningUnit.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.buttonAddPlanningUnitRow = QPushButton()
        self.buttonAddPlanningUnitRow.setText(MenuFactory.getLabel(MenuFactory.PURBUILD_ADD_PLANNING_UNIT))
        self.buttonAddPlanningUnitRow.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.layoutButtonSetupPlanningUnit.addWidget(self.buttonAddPlanningUnitRow)
        self.buttonClearAllPlanningUnits = QPushButton()
        self.buttonClearAllPlanningUnits.setText(MenuFactory.getLabel(MenuFactory.PURBUILD_CLEAR_PLANNING_UNIT))
        self.buttonClearAllPlanningUnits.setVisible(False) # BUG, hide it
        self.buttonClearAllPlanningUnits.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.layoutButtonSetupPlanningUnit.addWidget(self.buttonClearAllPlanningUnits)
        
        self.layoutContentGroupBoxSetupPlanningUnit = QVBoxLayout()
        self.layoutContentGroupBoxSetupPlanningUnit.setContentsMargins(5, 5, 5, 5)
        self.contentGroupBoxSetupPlanningUnit = QWidget()
        self.contentGroupBoxSetupPlanningUnit.setLayout(self.layoutContentGroupBoxSetupPlanningUnit)
        self.scrollSetupPlanningUnit = QScrollArea()
        ##self.scrollSetupPlanningUnit.setStyleSheet('QScrollArea > QWidget > QWidget { background: white; }')
        self.scrollSetupPlanningUnit.setWidgetResizable(True)
        self.scrollSetupPlanningUnit.setWidget(self.contentGroupBoxSetupPlanningUnit)
        
        self.layoutGroupBoxSetupPlanningUnit.addLayout(self.layoutSetupPlanningUnitInfo)
        self.layoutGroupBoxSetupPlanningUnit.addLayout(self.layoutButtonSetupPlanningUnit)
        self.layoutGroupBoxSetupPlanningUnit.addWidget(self.scrollSetupPlanningUnit)
        
        self.layoutTablePlanningUnit = QVBoxLayout()
        self.layoutTablePlanningUnit.setAlignment(Qt.AlignTop)
        self.layoutContentGroupBoxSetupPlanningUnit.addLayout(self.layoutTablePlanningUnit)
        
        # Create 3 default planning units
        ##self.addPlanningUnitRow()
        ##self.addPlanningUnitRow()
        ##self.addPlanningUnitRow()
        
        # Process tab button
        self.layoutButtonSetup = QHBoxLayout()
        self.buttonProcessSetup = QPushButton()
        self.buttonProcessSetup.setText('&' + MenuFactory.getLabel(MenuFactory.PURBUILD_BUILD))
        icon = QIcon(':/ui/icons/iconActionHelp.png')
        self.buttonHelp = QPushButton()
        self.buttonHelp.setIcon(icon)
        self.layoutButtonSetup.setAlignment(Qt.AlignRight)
        self.layoutButtonSetup.addWidget(self.buttonProcessSetup)
        self.layoutButtonSetup.addWidget(self.buttonHelp)
        
        # Template GroupBox
        self.groupBoxPURTemplate = QGroupBox(MenuFactory.getLabel(MenuFactory.CONF_TITLE))
        self.layoutGroupBoxPURTemplate = QVBoxLayout()
        self.layoutGroupBoxPURTemplate.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.groupBoxPURTemplate.setLayout(self.layoutGroupBoxPURTemplate)
        self.layoutPURTemplateInfo = QVBoxLayout()
        self.layoutPURTemplate = QGridLayout()
        self.layoutGroupBoxPURTemplate.addLayout(self.layoutPURTemplateInfo)
        self.layoutGroupBoxPURTemplate.addLayout(self.layoutPURTemplate)
        
        self.labelLoadedPURTemplate = QLabel()
        self.labelLoadedPURTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_LOADED_CONFIGURATION) + ':')
        self.layoutPURTemplate.addWidget(self.labelLoadedPURTemplate, 0, 0)
        
        self.loadedPURTemplate = QLabel()
        self.loadedPURTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NONE))
        self.layoutPURTemplate.addWidget(self.loadedPURTemplate, 0, 1)
        
        self.labelPURTemplate = QLabel()
        self.labelPURTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NAME) + ':')
        self.layoutPURTemplate.addWidget(self.labelPURTemplate, 1, 0)
        
        self.comboBoxPURTemplate = QComboBox()
        self.comboBoxPURTemplate.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.comboBoxPURTemplate.setDisabled(True)
        self.comboBoxPURTemplate.addItem(MenuFactory.getLabel(MenuFactory.CONF_NO_FOUND))
        self.layoutPURTemplate.addWidget(self.comboBoxPURTemplate, 1, 1)
        
        self.layoutButtonPURTemplate = QHBoxLayout()
        self.layoutButtonPURTemplate.setAlignment(Qt.AlignRight|Qt.AlignTop)
        self.buttonLoadPURTemplate = QPushButton()
        self.buttonLoadPURTemplate.setDisabled(True)
        self.buttonLoadPURTemplate.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.buttonLoadPURTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_LOAD))
        self.buttonSavePURTemplate = QPushButton()
        self.buttonSavePURTemplate.setDisabled(True)
        self.buttonSavePURTemplate.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.buttonSavePURTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_SAVE))
        self.buttonSaveAsPURTemplate = QPushButton()
        self.buttonSaveAsPURTemplate.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.buttonSaveAsPURTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_SAVE_AS))
        self.layoutButtonPURTemplate.addWidget(self.buttonLoadPURTemplate)
        self.layoutButtonPURTemplate.addWidget(self.buttonSavePURTemplate)
        self.layoutButtonPURTemplate.addWidget(self.buttonSaveAsPURTemplate)
        self.layoutGroupBoxPURTemplate.addLayout(self.layoutButtonPURTemplate)
        
        # Place the GroupBoxes
        self.layoutTabSetup.addWidget(self.groupBoxSetupReference, 0, 0)
        self.layoutTabSetup.addWidget(self.groupBoxReferenceMapping, 1, 0)
        self.layoutTabSetup.addWidget(self.groupBoxSetupPlanningUnit, 2, 0)
        self.layoutTabSetup.addLayout(self.layoutButtonSetup, 3, 0, 1, 2, Qt.AlignRight)
        self.layoutTabSetup.addWidget(self.groupBoxPURTemplate, 0, 1, 3, 1)
        self.layoutTabSetup.setColumnStretch(0, 3)
        self.layoutTabSetup.setColumnStretch(1, 1) # Smaller template column

        self.tabSetup.setLayout(self.layoutTabSetup)
        
        #***********************************************************
        # Setup 'Reconcile' tab
        #***********************************************************
        self.groupBoxReconcile = QGroupBox(MenuFactory.getLabel(MenuFactory.PURRECONCILE_UNRESOLVED_CASES))
        self.layoutGroupBoxReconcile = QVBoxLayout()
        self.layoutGroupBoxReconcile.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.groupBoxReconcile.setLayout(self.layoutGroupBoxReconcile)
        
        self.labelReconcileInfo = QLabel()
        self.labelReconcileInfo.setText('\n')
        self.labelReconcileInfo.setWordWrap(True)
        self.layoutGroupBoxReconcile.addWidget(self.labelReconcileInfo)
        
        self.reconcileTable = QTableWidget()
        self.reconcileTable.setDisabled(True)
        self.reconcileTable.verticalHeader().setVisible(False)
        self.layoutGroupBoxReconcile.addWidget(self.reconcileTable)
        
        self.layoutButtonReconcile = QHBoxLayout()
        self.buttonProcessReconcile = QPushButton()
        self.buttonProcessReconcile.setText('&' + MenuFactory.getLabel(MenuFactory.PURRECONCILE_RECONCILE))
        self.buttonProcessReconcile.setDisabled(True)
        self.layoutButtonReconcile.setAlignment(Qt.AlignRight)
        self.layoutButtonReconcile.addWidget(self.buttonProcessReconcile)
        
        self.layoutTabReconcile.addWidget(self.groupBoxReconcile)
        self.layoutTabReconcile.addLayout(self.layoutButtonReconcile)
        
        self.tabReconcile.setLayout(self.layoutTabReconcile)
        
        #***********************************************************
        # Setup 'Log' tab
        #***********************************************************
        self.tabLog.setLayout(self.layoutTabLog)
        
        # 'History Log' GroupBox
        self.groupBoxHistoryLog = QGroupBox('{0} {1}'.format(self.dialogTitle, 'history log'))
        self.layoutGroupBoxHistoryLog = QVBoxLayout()
        self.layoutGroupBoxHistoryLog.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.groupBoxHistoryLog.setLayout(self.layoutGroupBoxHistoryLog)
        self.layoutHistoryLogInfo = QVBoxLayout()
        self.layoutHistoryLog = QVBoxLayout()
        self.layoutGroupBoxHistoryLog.addLayout(self.layoutHistoryLogInfo)
        self.layoutGroupBoxHistoryLog.addLayout(self.layoutHistoryLog)
        
        self.labelHistoryLogInfo = QLabel()
        self.labelHistoryLogInfo.setText('\n')
        self.layoutHistoryLogInfo.addWidget(self.labelHistoryLogInfo)
        
        self.log_box = QPlainTextEditLogger(self)
        self.layoutHistoryLog.addWidget(self.log_box.widget)
        
        self.layoutTabLog.addWidget(self.groupBoxHistoryLog)
        
        
        self.setLayout(self.dialogLayout)
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(840, 500)
        self.resize(parent.sizeHint())
    
    
    def loadHistoryLog(self):
        """Method for loading the module history log file.
        """
        if os.path.exists(self.historyLogPath):
            logText = open(self.historyLogPath).read()
            self.log_box.widget.setPlainText(logText)
    
    
    def showEvent(self, event):
        """Overload method that is called when the dialog widget is shown.
        
        Args:
            event (QShowEvent): the show widget event.
        """
        super(DialogLumensPUR, self).showEvent(event)
    
    
    def closeEvent(self, event):
        """Overload method that is called when the dialog widget is closed.
        
        Args:
            event (QCloseEvent): the close widget event.
        """
        super(DialogLumensPUR, self).closeEvent(event)
    
    
    def addPlanningUnitRow(self, planningUnitData=None, referenceClassID=None, planningUnitType=None):
        """Method for adding a planning unit table row.
        
        Args:
            planningUnitData (str): the RST_DATA key of an added planning unit data.
            referenceClassID (int): the reference class id associated with the planning unit.
            planningUnitType (str): the type of the planning unit.
        """
        self.tablePlanningUnitRowCount = self.tablePlanningUnitRowCount + 1
        
        layoutRow = QHBoxLayout()
        
        buttonDeletePlanningUnitData = QPushButton()
        icon = QIcon(':/ui/icons/iconActionClear.png')
        buttonDeletePlanningUnitData.setIcon(icon)
        buttonDeletePlanningUnitData.setObjectName('buttonDeletePlanningUnitData_{0}'.format(str(self.tablePlanningUnitRowCount)))
        layoutRow.addWidget(buttonDeletePlanningUnitData)
        
        buttonDeletePlanningUnitData.clicked.connect(self.handlerDeletePlanningUnitData)
        
        comboBoxPlanningUnitData = QComboBox()
        comboBoxPlanningUnitData.setDisabled(True)
        comboBoxPlanningUnitData.setObjectName('comboBoxPlanningUnitData_{0}'.format(str(self.tablePlanningUnitRowCount)))
        layoutRow.addWidget(comboBoxPlanningUnitData)
        
        comboBoxPlanningUnitData.currentIndexChanged.connect(self.handlerChangePlanningUnitData)
        
        lineEditPlanningUnitTitle = QLineEdit()
        lineEditPlanningUnitTitle.setDisabled(True)
        lineEditPlanningUnitTitle.setObjectName('lineEditPlanningUnitTitle_{0}'.format(str(self.tablePlanningUnitRowCount)))
        layoutRow.addWidget(lineEditPlanningUnitTitle)
        
        comboBoxReferenceClasses = QComboBox()
        for key, val in self.referenceClasses.iteritems():
            comboBoxReferenceClasses.addItem(val, key)
        comboBoxReferenceClasses.setObjectName('comboBoxReferenceClasses_{0}'.format(str(self.tablePlanningUnitRowCount)))
        layoutRow.addWidget(comboBoxReferenceClasses)
        
        comboBoxPlanningUnitType = QComboBox()
        comboBoxPlanningUnitType.addItems([MenuFactory.getLabel(MenuFactory.PUBBUILD_RECONCILIATION), MenuFactory.getLabel(MenuFactory.PUBBUILD_ADDITIONAL)])
        comboBoxPlanningUnitType.setObjectName('comboBoxPlanningUnitType_{0}'.format(str(self.tablePlanningUnitRowCount)))
        layoutRow.addWidget(comboBoxPlanningUnitType)
        
        self.layoutTablePlanningUnit.addLayout(layoutRow)
        
        self.populateAddedDataComboBox(self.main.dataPlanningUnit, comboBoxPlanningUnitData)
        
        if planningUnitData:
            self.handlerChangePlanningUnitData(rowNumber=self.tablePlanningUnitRowCount, RST_DATA=planningUnitData)
            
        if referenceClassID:
            comboBoxReferenceClasses.setCurrentIndex(comboBoxReferenceClasses.findData(referenceClassID))
        
        if planningUnitType != None:
            if planningUnitType == 0:
                comboBoxPlanningUnitType.setCurrentIndex(comboBoxPlanningUnitType.findText(MenuFactory.getLabel(MenuFactory.PUBBUILD_RECONCILIATION)))
            elif planningUnitType == 1:
                comboBoxPlanningUnitType.setCurrentIndex(comboBoxPlanningUnitType.findText(MenuFactory.getLabel(MenuFactory.PUBBUILD_ADDITIONAL)))
    
    
    def clearPlanningUnitRows(self):
        """Method for clearing all planning unit rows.
        """
        for planningUnitButton in self.contentGroupBoxSetupPlanningUnit.findChildren(QPushButton):
            if 'buttonDeletePlanningUnitData' in planningUnitButton.objectName():
                planningUnitButton.click()
    
    
    def clearLayout(self, layout):
        """Method for removing a layout and all its child widgets.
        
        Args:
            layout (QLayout): the layout to be removed.
        """
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)

            if isinstance(item, QWidgetItem):
                item.widget().deleteLater() # use this to properly delete the widget
            elif isinstance(item, QtGui.QSpacerItem):
                pass
            else:
                self.clearLayout(item.layout())
            
            layout.removeItem(item)
    
    
    def updateReferenceClasses(self, newReferenceClasses):
        """Method for loading the reference classes comboboxes with the new values.
        
        Args:
            newReferenceClasses (dict): the new reference classes.
        """
        self.referenceClasses = newReferenceClasses
        
        # Update reference classes in 'Setup reference data' groupbox
        for comboBoxReferenceClasses in self.tableReferenceMapping.findChildren(QComboBox):
            comboBoxReferenceClasses.clear()
            for key, val in self.referenceClasses.iteritems():
                comboBoxReferenceClasses.addItem(val, key)
                
        # Update reference classes in 'Setup planning unit' groupbox
        for comboBoxReferenceClasses in self.contentGroupBoxSetupPlanningUnit.findChildren(QComboBox):
            if 'comboBoxReferenceClasses' in comboBoxReferenceClasses.objectName():
                comboBoxReferenceClasses.clear()
                for key, val in self.referenceClasses.iteritems():
                    comboBoxReferenceClasses.addItem(val, key)
    
    
    def updateReferenceMapping(self, referenceMapping):
        """Method for loading the mapping in the reference mapping table.
        
        Args:
            referenceMapping (dict): a map between the attributes and the reference classes.
        """
        for tableRow in range(0, self.tableReferenceMapping.rowCount()):
            attributeValue = self.tableReferenceMapping.item(tableRow, 0).text()
            comboBoxReferenceClasses = self.tableReferenceMapping.cellWidget(tableRow, 1)
            referenceClassID = referenceMapping[attributeValue]
            comboBoxReferenceClasses.setCurrentIndex(comboBoxReferenceClasses.findData(referenceClassID))
    
    
    def updatePlanningUnits(self, planningUnits):
        """Method for loading the planning units to the planning unit table.
        
        Args:
            planningUnits (list of dict): a dict list of planning units.
        """
        self.clearPlanningUnitRows()
        
        for planningUnit in planningUnits:
            self.addPlanningUnitRow(planningUnit['planningUnitData'], planningUnit['referenceClassID'], planningUnit['planningUnitType'])
        
    
    @staticmethod
    def writeTableCsv(tableWidget, forwardDirSeparator=False):
        """Method for writing the table data to a temp csv file.
        
        Args:
            forwardDirSeparator (bool): return the temp csv file path with forward slash dir separator.
        """
        dataTable = []
        
        headerRow = []
        
        # Write table header too
        for headerColumn in range(tableWidget.columnCount()):
            headerItem = tableWidget.horizontalHeaderItem(headerColumn)
            headerRow.append(headerItem.text())
        
        dataTable.append(headerRow)
        
        # Loop rows
        for tableRow in range(tableWidget.rowCount()):
            dataRow = []
            
            # Loop row columns
            for tableColumn in range(tableWidget.columnCount()):
                item = tableWidget.item(tableRow, tableColumn)
                widget = tableWidget.cellWidget(tableRow, tableColumn)
                
                # Check if cell is a combobox widget
                if widget and isinstance(widget, QComboBox):
                    dataRow.append(widget.currentText())
                else:
                    itemText = item.text()
                    
                    if itemText:
                        dataRow.append(itemText)
                    else:
                        return '' # Cell is empty!
                
            dataTable.append(dataRow)
        
        if dataTable:
            handle, tableCsvFilePath = tempfile.mkstemp(suffix='.csv')
        
            with os.fdopen(handle, 'w') as f:
                writer = csv.writer(f)
                for dataRow in dataTable:
                    writer.writerow(dataRow)
            
            if forwardDirSeparator:
                return tableCsvFilePath.replace(os.path.sep, '/')
            
            return tableCsvFilePath
        
        # Table unused, or something wrong with the table
        return ''
    
    
    #***********************************************************
    # 'Setup' tab QPushButton handlers
    #***********************************************************
    def handlerTabWidgetChanged(self, index):
        """Slot method for scrolling the log to the latest output.
        
        Args:
            index (int): the current tab index.
        """
        if self.tabWidget.widget(index) == self.tabLog:
            self.log_box.widget.verticalScrollBar().triggerAction(QAbstractSlider.SliderToMaximum)
    
    
    def handlerLoadPURTemplate(self, fileName=None):
        """Slot method for loading a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.comboBoxPURTemplate.currentText()
        reply = None
        
        if fileName:
            templateFile = fileName
        else:
            reply = QMessageBox.question(
                self,
                MenuFactory.getLabel(MenuFactory.CONF_LOAD_TEMPLATE),
                MenuFactory.getDescription(MenuFactory.CONF_LOAD_TEMPLATE) + ' \'{0}\'?'.format(templateFile),
                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                QtGui.QMessageBox.No
            )
            
        if reply == QMessageBox.Yes or fileName:
            self.loadTemplate('Setup', templateFile)
    
    
    def handlerSavePURTemplate(self, fileName=None):
        """Slot method for saving a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.currentPURTemplate
        
        if fileName:
            templateFile = fileName
        
        reply = QMessageBox.question(
            self,
            MenuFactory.getLabel(MenuFactory.CONF_SAVE_TEMPLATE),
            MenuFactory.getDescription(MenuFactory.CONF_SAVE_TEMPLATE), # 'Do you want save \'{0}\'?\nThis action will overwrite the template file.'.format(templateFile),
            QMessageBox.Yes|QMessageBox.No,
            QMessageBox.No
        )
            
        if reply == QMessageBox.Yes:
            self.saveTemplate('Setup', templateFile)
            return True
        else:
            return False
    
    
    def handlerSaveAsPURTemplate(self):
        """Slot method for saving a module template to a new file.
        """
        fileName, ok = QInputDialog.getText(self, MenuFactory.getLabel(MenuFactory.CONF_SAVE_AS_TEMPATE), MenuFactory.getDescription(MenuFactory.CONF_SAVE_AS_TEMPATE) + ':')
        fileSaved = False
        
        if ok:
            now = QDateTime.currentDateTime().toString('yyyyMMdd-hhmmss')
            fileName = now + '__' + fileName + '.ini'
            
            if os.path.exists(os.path.join(self.settingsPath, fileName)):
                fileSaved = self.handlerSavePURTemplate(fileName)
            else:
                self.saveTemplate('Setup', fileName)
                fileSaved = True
            
            self.loadTemplateFiles()
            
            # Load the newly saved template file
            if fileSaved:
                self.handlerLoadPURTemplate(fileName)
    
    
    def handlerButtonAddPlanningUnitRow(self):
        """Slot method for adding a planning unit to the planning unit table.
        """
        self.addPlanningUnitRow()
    
    
    def handlerButtonClearAllPlanningUnits(self):
        """Slot method for clearing all planning units in the planning unit table.
        """
        self.clearPlanningUnitRows()
    
    
    def handlerChangePlanningUnitData(self, currentIndex=None, rowNumber=None, RST_DATA=None):
        """Slot method for changing a planning unit data.
        
        Args:
            rowNumber (int): the planning unit table row.
            RST_DATA (str): the RST_DATA key of an added planning unit data.
        """
        planningUnitData = None
        tableRow = None
        
        if not rowNumber:
            buttonSender = self.sender()
            objectName = buttonSender.objectName()
            tableRow = objectName.split('_')[1]
        else:
            tableRow = str(rowNumber)
        
        comboBoxPlanningUnitData = self.contentGroupBoxSetupPlanningUnit.findChild(QtGui.QComboBox, 'comboBoxPlanningUnitData_' + tableRow)
        
        if RST_DATA:
            planningUnitData = RST_DATA
            comboBoxPlanningUnitData.setCurrentIndex(comboBoxPlanningUnitData.findText(planningUnitData))
        else:
            planningUnitData = comboBoxPlanningUnitData.currentText()
        
        addedPlanningUnit = comboBoxPlanningUnitData.itemData(comboBoxPlanningUnitData.findText(planningUnitData))
        
        lineEditPlanningUnitTitle = self.contentGroupBoxSetupPlanningUnit.findChild(QLineEdit, 'lineEditPlanningUnitTitle_' + tableRow)
        lineEditPlanningUnitTitle.setText(addedPlanningUnit['RST_NAME'])
    
    
    def handlerDeletePlanningUnitData(self):
        """Slot method for deleting a planning unit from the planning unit table.
        """
        buttonSender = self.sender()
        objectName = buttonSender.objectName()
        tableRow = objectName.split('_')[1]
        layoutRow = self.layoutTablePlanningUnit.itemAt(int(tableRow) - 1).layout()
        self.clearLayout(layoutRow)
    
    
    def handlerLoadLookupTableReference(self):
        """Slot method for calling spesific planning unit lookup table and
           populating the reference mapping table from the selected reference data.
        """      
        activeProject = self.main.appSettings['DialogLumensOpenDatabase']['projectFile'].replace(os.path.sep, '/')
        selectedReferenceData = self.comboBoxReferenceData.currentText()
        customTable = 0
        attributeValues = []
        
        outputs = general.runalg(
            'r:toolsgetlut',
            activeProject,
            customTable,
            selectedReferenceData,
            None,
        )        
        
        outputKey = 'main_data'
        if outputs and outputKey in outputs:
            if os.path.exists(outputs[outputKey]):
                with open(outputs[outputKey], 'rb') as f:
                    reader = csv.reader(f)
                    next(reader)
                    for attributeValue in reader:
                        attributeValues.append(attributeValue[0])
                    
                    # Clear the table first
                    self.tableReferenceMapping.setRowCount(0)
                    self.tableReferenceMapping.setRowCount(len(attributeValues))
                    
                    row = 0
                    for attributeValue in sorted(attributeValues):
                        comboboxReferenceClasses = QtGui.QComboBox()
                        for key, val in self.referenceClasses.iteritems():
                            comboboxReferenceClasses.addItem(val, key)
                        
                        self.tableReferenceMapping.setItem(row, 0, QtGui.QTableWidgetItem(attributeValue))
                        self.tableReferenceMapping.setCellWidget(row, 1, comboboxReferenceClasses)
                        row = row + 1
        
    
    def handlerEditReferenceClasses(self):
        """Slot method for showing the PUR reference class editing dialog.
        """
        dialog = DialogLumensPURReferenceClasses(self)
        
        if dialog.exec_() == QDialog.Accepted:
            self.updateReferenceClasses(dialog.getReferenceClasses())
    
    
    def reconcileUnresolvedCases(self):
        """Method for dealing with unresolved cases found after PUR setup algorithm.
        
        Loads the unresolved cases CSV output from PUR setup algorithm to the
        table in the reconcile tab where the user can select an action to resolve
        the case.
        
        Args:
            outputs (dict): the output dict of the executed algorithm.
        """
        outputs = self.outputsPURSetup
        unresolvedCases = False
        unresolvedCasesKey = 'database_unresolved_out'
        attributeKey = 'data_attribute'
        
        print('DEBUG')
        print(outputs)
        
        if outputs and (unresolvedCasesKey in outputs) and (attributeKey in outputs):
            if os.path.exists(outputs[unresolvedCasesKey]):
                with open(outputs[unresolvedCasesKey], 'rb') as f:
                    hasHeader = csv.Sniffer().has_header(f.read(1024))
                    f.seek(0)
                    reader = csv.reader(f)
                    if hasHeader: # Skip the header
                        next(reader)
                    for row in reader: # Just read the first row
                        # Look for "There are no unresolved area in this analysis session"
                        statusMessage = str(row[0])
                        if 'no unresolved' not in statusMessage:
                            unresolvedCases = True
                        break
                
                if unresolvedCases:
                    # Confirm if user wants to process unresolved cases
                    # reply = QtGui.QMessageBox.question(
                    #     self,
                    #     'Reconcile Unresolved Cases',
                    #     'Found unresolved cases.\nDo you want to manually reconcile them?',
                    #     QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                    #     QtGui.QMessageBox.No
                    # )
                    # 
                    # if reply == QtGui.QMessageBox.Yes:
                    attributes = []
                    
                    # Options for reconcile action
                    with open(outputs[attributeKey], 'rb') as f:
                        hasHeader = csv.Sniffer().has_header(f.read(1024))
                        f.seek(0)
                        reader = csv.reader(f)
                        if hasHeader: # Skip the header
                            next(reader)
                        for row in reader:
                            attribute = str(row[1])
                            # Don't add "unresolved_caseN"
                            if 'unresolved_' not in attribute:
                                attributes.append(attribute)
                    
                    sortedAttributes = sorted(attributes)
                    
                    # Populate the reconcile table
                    with open(outputs[unresolvedCasesKey], 'rb') as f:
                        hasHeader = csv.Sniffer().has_header(f.read(1024))
                        f.seek(0)
                        reader = csv.reader(f)
                        
                        if hasHeader: # Set the column headers
                            headerRow = reader.next()
                            fields = [str(field) for field in headerRow]
                            
                            fields.append('Reconcile Action')
                            
                            self.reconcileTable.setColumnCount(len(fields))
                            self.reconcileTable.setHorizontalHeaderLabels(fields)
                        
                        dataTable = []
                        
                        for row in reader:
                            dataRow = [QtGui.QTableWidgetItem(field) for field in row]
                            dataTable.append(dataRow)
                        
                        self.reconcileTable.setRowCount(len(dataTable))
                        
                        tableRow = 0
                        
                        for dataRow in dataTable:
                            tableColumn = 0
                            
                            for fieldTableItem in dataRow:
                                fieldTableItem.setFlags(fieldTableItem.flags() & ~QtCore.Qt.ItemIsEnabled)
                                self.reconcileTable.setItem(tableRow, tableColumn, fieldTableItem)
                                self.reconcileTable.horizontalHeader().setResizeMode(tableColumn, QtGui.QHeaderView.ResizeToContents)
                                tableColumn += 1
                            
                            comboBoxAction = QtGui.QComboBox()
                            comboBoxAction.addItems(sortedAttributes)
                            
                            self.reconcileTable.setCellWidget(tableRow, tableColumn, comboBoxAction)
                            self.reconcileTable.horizontalHeader().setResizeMode(tableColumn, QtGui.QHeaderView.ResizeToContents)
                            
                            tableRow += 1
                        
                        self.reconcileTable.setEnabled(True)
                        self.buttonProcessReconcile.setEnabled(True)
                        
                        # Switch to reconcile tab
                        self.tabWidget.setCurrentWidget(self.tabReconcile)
        else:
            logging.getLogger(type(self).__name__).error('Reconcile PUR error')
            logging.getLogger(self.historyLog).info('Reconcile PUR error')
    
    
    #***********************************************************
    # Process tabs
    #***********************************************************
    def setAppSettings(self):
        """Set the required values from the form widgets.
        """
        # 'Setup reference' GroupBox values
        self.main.appSettings[type(self).__name__]['referenceData'] = self.comboBoxReferenceData.currentText() # unicode
        self.main.appSettings[type(self).__name__]['referenceClasses'] = self.referenceClasses
        
        self.tableReferenceMappingData = {}
        for tableRow in range(0, self.tableReferenceMapping.rowCount()):
            attributeValue = self.tableReferenceMapping.item(tableRow, 0).text()
            comboBoxReferenceClasses = self.tableReferenceMapping.cellWidget(tableRow, 1)
            referenceClassID = comboBoxReferenceClasses.itemData(comboBoxReferenceClasses.currentIndex())
            self.tableReferenceMappingData[attributeValue] = referenceClassID
        
        self.main.appSettings[type(self).__name__]['referenceMapping'] = self.tableReferenceMappingData
        
        # 'Setup planning unit' GroupBox values
        self.tablePlanningUnitData = []
        for tableRow in range(1, self.tablePlanningUnitRowCount + 1):
            comboBoxPlanningUnitData = self.findChild(QtGui.QComboBox, 'comboBoxPlanningUnitData_' + str(tableRow))
            
            if not comboBoxPlanningUnitData: # Row has been deleted
                print('DEBUG: skipping a deleted row.')
                continue
            
            lineEditPlanningUnitTitle = self.findChild(QLineEdit, 'lineEditPlanningUnitTitle_' + str(tableRow))
            comboBoxReferenceClasses = self.findChild(QComboBox, 'comboBoxReferenceClasses_' + str(tableRow))
            comboBoxPlanningUnitType = self.findChild(QComboBox, 'comboBoxPlanningUnitType_' + str(tableRow))
            
            planningUnitData = str(comboBoxPlanningUnitData.currentText())
            planningUnitTitle = str(lineEditPlanningUnitTitle.text())
            referenceClassID = comboBoxReferenceClasses.itemData(comboBoxReferenceClasses.currentIndex())
            planningUnitType = str(comboBoxPlanningUnitType.currentText())
            
            if planningUnitData and planningUnitTitle and referenceClassID and planningUnitType:
                if planningUnitType == MenuFactory.getLabel(MenuFactory.PUBBUILD_RECONCILIATION):
                    planningUnitType = 0
                else:
                    planningUnitType = 1
                
                tableRowData = {
                    'planningUnitData': planningUnitData,
                    'planningUnitTitle': planningUnitTitle,
                    'referenceClassID': referenceClassID,
                    'planningUnitType': planningUnitType,
                }
                
                self.tablePlanningUnitData.append(tableRowData)
            else:
                print('DEBUG: ERROR incomplete planning unit details.')
        
        self.main.appSettings[type(self).__name__]['planningUnits'] = self.tablePlanningUnitData
        
        print('DEBUG: appSettings["DialogLumensPUR"]')
        print(self.main.appSettings[type(self).__name__])
    
    
    def handlerProcessSetup(self):
        """Slot method to pass the form values and execute the "PUR" R algorithms.
        
        The "PUR" process calls the following algorithms:
        1. r:pursetup
        """
        self.setAppSettings()
        
        if self.validForm():
            logging.getLogger(type(self).__name__).info('Processing PUR start: %s' % self.dialogTitle)
            logging.getLogger(self.historyLog).info('Processing PUR start: %s' % self.dialogTitle)
            self.buttonProcessSetup.setDisabled(True)
            
            algName = 'r:pursetup'
            
            # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
            self.main.setWindowState(Qt.WindowMinimized)
            
            # Pass referenceClasses, referenceMapping, planningUnits as temp csv files
            activeProject = self.main.appSettings['DialogLumensOpenDatabase']['projectFile'].replace(os.path.sep, '/')
            referenceClasses = self.main.appSettings[type(self).__name__]['referenceClasses']
            referenceMapping = self.main.appSettings[type(self).__name__]['referenceMapping']
            planningUnits = self.main.appSettings[type(self).__name__]['planningUnits']
            
            handleReferenceClasses, csvReferenceClasses = tempfile.mkstemp(suffix='.csv')
            handleReferenceMapping, csvReferenceMapping = tempfile.mkstemp(suffix='.csv')
            handlePlanningUnits, csvPlanningUnits = tempfile.mkstemp(suffix='.csv')
            
            with os.fdopen(handleReferenceClasses, 'w') as f:
                writer = csv.writer(f)
                writer.writerows(referenceClasses.items())
            
            with os.fdopen(handleReferenceMapping, 'w') as f:
                writer = csv.writer(f)
                writer.writerows(referenceMapping.items())
            
            with os.fdopen(handlePlanningUnits, 'w') as f:
                writer = csv.DictWriter(f, planningUnits[0].keys())
                writer.writerows(planningUnits)
            
            self.outputsPURSetup = general.runalg(
                algName,
                activeProject,
                self.main.appSettings[type(self).__name__]['referenceData'],
                csvReferenceClasses.replace(os.path.sep, '/'),
                csvReferenceMapping.replace(os.path.sep, '/'),
                csvPlanningUnits.replace(os.path.sep, '/'),
                None,
                None,
                None,
                None,
                None,
                None,
            )
            
            # Display ROut file in debug mode
            if self.main.appSettings['debug']:
                dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                dialog.exec_()
            
            # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
            self.main.setWindowState(Qt.WindowActive)
            
            algSuccess = self.outputsMessageBox(algName, self.outputsPURSetup, MenuFactory.getLabel(MenuFactory.MSG_PUR_SETUP_RUN_SUCCESS), 'Something happened.')

            if algSuccess:
                self.main.addLayer(self.outputsPURSetup['PUR_rec1_shp'])
                # self.main.addLayer(self.outputsPURSetup['PUR_dbfinal'])
                self.main.loadAddedDataInfo()
            
            self.buttonProcessSetup.setEnabled(True)
            logging.getLogger(type(self).__name__).info('Processing PUR end: %s' % self.dialogTitle)
            logging.getLogger(self.historyLog).info('Processing PUR end: %s' % self.dialogTitle)
            
            # Check for and offer to reconcile unresolved cases
            self.reconcileUnresolvedCases()
    
    
    def handlerProcessReconcile(self):
        """Slot method to handle reconciling unresolved cases in the reconcile tab.
        
        The Reconcile process calls the following algorithms:
        1. r:purreconciliation
        """
        algName = 'r:purreconciliation'
        
        outputs = self.outputsPURSetup
        reconKey = 'PUR_rec1_shp'
        
        if outputs and (reconKey in outputs):
            logging.getLogger(type(self).__name__).info('Reconcile PUR start')
            logging.getLogger(self.historyLog).info('Reconcile PUR start')
            self.buttonProcessReconcile.setDisabled(True)
            
            activeProject = self.main.appSettings['DialogLumensOpenDatabase']['projectFile'].replace(os.path.sep, '/')
            reconcileTableCsv = DialogLumensPUR.writeTableCsv(self.reconcileTable, True)
            
            # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
            # self.main.setWindowState(QtCore.Qt.WindowMinimized)
            
            print('DEBUG')
            print(reconcileTableCsv)
            print(outputs[reconKey])
            
            outputsReconcile = general.runalg(
                algName,
                activeProject,
                outputs[reconKey].replace(os.path.sep, '/'),
                reconcileTableCsv.replace(os.path.sep, '/'),
                None,
            )
            
            # Display ROut file in debug mode
            if self.main.appSettings['debug']:
                dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                dialog.exec_()
            
            # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
            # self.main.setWindowState(QtCore.Qt.WindowActive)
            
            algSuccess = self.outputsMessageBox(algName, outputsReconcile, MenuFactory.getLabel(MenuFactory.MSG_PUR_RECONCILE_RUN_SUCCESS), 'Something happened.')

            if algSuccess:
                self.main.loadAddedDataInfo()

            self.buttonProcessReconcile.setEnabled(True)
            logging.getLogger(type(self).__name__).info('Reconcile PUR end')
            logging.getLogger(self.historyLog).info('Reconcile PUR end')
        else:
            logging.getLogger(type(self).__name__).error('Reconcile PUR error')
            logging.getLogger(self.historyLog).info('Reconcile PUR error')
