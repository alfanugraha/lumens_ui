#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, datetime, glob
from qgis.core import *
from processing.tools import *
from PyQt4 import QtCore, QtGui

from utils import QPlainTextEditLogger
from dialog_lumens_base import DialogLumensBase
from dialog_lumens_viewer import DialogLumensViewer
import resource

from menu_factory import MenuFactory

class DialogLumensTAOpportunityCost(QtGui.QDialog, DialogLumensBase):
    """LUMENS "TA Opportunity Cost" module dialog class.
    """
    
    def loadTemplateFiles(self):
        """Method for loading the list of module template files inside the project folder.
        
        This method is also called to load the module template files in the main window dashboard tab.
        """
        templateFiles = [os.path.basename(name) for name in glob.glob(os.path.join(self.settingsPath, '*.ini')) if os.path.isfile(os.path.join(self.settingsPath, name))]
        
        if templateFiles:
            self.comboBoxAbacusOpportunityCostTemplate.clear()
            self.comboBoxAbacusOpportunityCostTemplate.addItems(sorted(templateFiles))
            self.comboBoxAbacusOpportunityCostTemplate.setEnabled(True)
            self.buttonLoadAbacusOpportunityCostTemplate.setEnabled(True)
            
            self.comboBoxOpportunityCostCurveTemplate.clear()
            self.comboBoxOpportunityCostCurveTemplate.addItems(sorted(templateFiles))
            self.comboBoxOpportunityCostCurveTemplate.setEnabled(True)
            self.buttonLoadOpportunityCostCurveTemplate.setEnabled(True)
            
            self.comboBoxOpportunityCostMapTemplate.clear()
            self.comboBoxOpportunityCostMapTemplate.addItems(sorted(templateFiles))
            self.comboBoxOpportunityCostMapTemplate.setEnabled(True)
            self.buttonLoadOpportunityCostMapTemplate.setEnabled(True)
            
            # MainWindow TA Opportunity Cost dashboard templates
            self.main.comboBoxAbacusOpportunityCostTemplate.clear()
            self.main.comboBoxAbacusOpportunityCostTemplate.addItems(sorted(templateFiles))
            self.main.comboBoxAbacusOpportunityCostTemplate.setEnabled(True)
            
            self.main.comboBoxOpportunityCostCurveTemplate.clear()
            self.main.comboBoxOpportunityCostCurveTemplate.addItems(sorted(templateFiles))
            self.main.comboBoxOpportunityCostCurveTemplate.setEnabled(True)
            
            self.main.comboBoxOpportunityCostMapTemplate.clear()
            self.main.comboBoxOpportunityCostMapTemplate.addItems(sorted(templateFiles))
            self.main.comboBoxOpportunityCostMapTemplate.setEnabled(True)
            
            self.main.buttonProcessTAOpportunityCostTemplate.setEnabled(True)
        else:
            self.comboBoxAbacusOpportunityCostTemplate.setDisabled(True)
            self.buttonLoadAbacusOpportunityCostTemplate.setDisabled(True)
            
            self.comboBoxOpportunityCostCurveTemplate.setDisabled(True)
            self.buttonLoadOpportunityCostCurveTemplate.setDisabled(True)
            
            self.comboBoxOpportunityCostMapTemplate.setDisabled(True)
            self.buttonLoadOpportunityCostMapTemplate.setDisabled(True)
            
            # MainWindow TA Opportunity Cost dashboard templates
            self.main.comboBoxAbacusOpportunityCostTemplate.setDisabled(True)
            
            self.main.comboBoxOpportunityCostCurveTemplate.setDisabled(True)
            
            self.main.comboBoxOpportunityCostMapTemplate.setDisabled(True)
            
            self.main.buttonProcessTAOpportunityCostTemplate.setDisabled(True)
        
    
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
        
        td = datetime.date.today()
        
        if tabName == MenuFactory.getLabel(MenuFactory.TAOPCOST_ABACUS_OPPORTUNITY_COST):
            dialogsToLoad = (
                'DialogLumensTAAbacusOpportunityCostCurve',
            )
            
            # start tab
            settings.beginGroup(tabName)
            
            # 'Abacus opportunity cost' groupbox widgets
            # start dialog
            settings.beginGroup('DialogLumensTAAbacusOpportunityCostCurve')
            
            templateSettings['DialogLumensTAAbacusOpportunityCostCurve'] = {}
            templateSettings['DialogLumensTAAbacusOpportunityCostCurve']['projectFile'] = projectFile = settings.value('projectFile')
            
            if not returnTemplateSettings:
                if projectFile and os.path.isdir(projectFile):
                    self.lineEditAOCProjectFile.setText(projectFile)
                else:
                    self.lineEditAOCProjectFile.setText('')
                
                self.currentAbacusOpportunityCostTemplate = templateFile
                self.loadedAbacusOpportunityCostTemplate.setText(templateFile)
                self.comboBoxAbacusOpportunityCostTemplate.setCurrentIndex(self.comboBoxAbacusOpportunityCostTemplate.findText(templateFile))
                self.buttonSaveAbacusOpportunityCostTemplate.setEnabled(True)
            
            settings.endGroup()
            # /dialog
            
            settings.endGroup()
            # /tab
        elif tabName == MenuFactory.getLabel(MenuFactory.TAOPCOST_OPPORTUNITY_COST_CURVE):
            dialogsToLoad = (
                'DialogLumensTAOpportunityCostCurve',
            )
            
            # start tab
            settings.beginGroup(tabName)
            
            # 'Opportunity Cost Curve' tab widgets
            # start dialog
            settings.beginGroup('DialogLumensTAOpportunityCostCurve')
            
            templateSettings['DialogLumensTAOpportunityCostCurve'] = {}
            templateSettings['DialogLumensTAOpportunityCostCurve']['csvNPVTable'] = csvNPVTable = settings.value('csvNPVTable')
            templateSettings['DialogLumensTAOpportunityCostCurve']['costThreshold'] = costThreshold = settings.value('costThreshold')
            templateSettings['DialogLumensTAOpportunityCostCurve']['outputOpportunityCostDatabase'] = outputOpportunityCostDatabase = settings.value('outputOpportunityCostDatabase')
            templateSettings['DialogLumensTAOpportunityCostCurve']['outputOpportunityCostReport'] = outputOpportunityCostReport = settings.value('outputOpportunityCostReport')
            
            if not returnTemplateSettings:
                if csvNPVTable and os.path.exists(csvNPVTable):
                    self.lineEditOCCCsvNPVTable.setText(csvNPVTable)
                else:
                    self.lineEditOCCCsvNPVTable.setText('')
                if costThreshold:
                    self.spinBoxOCCCostThreshold.setValue(int(costThreshold))
                else:
                    self.spinBoxOCCCostThreshold.setValue(5)
                if outputOpportunityCostDatabase:
                    self.lineEditOCCOutputOpportunityCostDatabase.setText(outputOpportunityCostDatabase)
                else:
                    self.lineEditOCCOutputOpportunityCostDatabase.setText('')
                if outputOpportunityCostReport:
                    self.lineEditOCCOutputOpportunityCostReport.setText(outputOpportunityCostReport)
                else:
                    self.lineEditOCCOutputOpportunityCostReport.setText('')
                
                self.currentOpportunityCostCurveTemplate = templateFile
                self.loadedOpportunityCostCurveTemplate.setText(templateFile)
                self.comboBoxOpportunityCostCurveTemplate.setCurrentIndex(self.comboBoxOpportunityCostCurveTemplate.findText(templateFile))
                self.buttonSaveOpportunityCostCurveTemplate.setEnabled(True)
            
            settings.endGroup()
            # /dialog
            
            settings.endGroup()
            # /tab
        elif tabName == MenuFactory.getLabel(MenuFactory.TAOPCOST_OPPORTUNITY_COST_MAP):
            dialogsToLoad = (
                'DialogLumensTAOpportunityCostMap',
            )
            
            # start tab
            settings.beginGroup(tabName)
            
            # 'Opportunity Cost Map' tab widgets
            # start dialog
            settings.beginGroup('DialogLumensTAOpportunityCostMap')
            
            templateSettings['DialogLumensTAOpportunityCostMap'] = {}
            templateSettings['DialogLumensTAOpportunityCostMap']['csvProfitability'] = csvProfitability = settings.value('csvProfitability')
            
            if not returnTemplateSettings:
                if csvProfitability and os.path.exists(csvProfitability):
                    self.lineEditOCMCsvProfitability.setText(csvProfitability)
                else:
                    self.lineEditOCMCsvProfitability.setText('')
                
                self.currentOpportunityCostMapTemplate = templateFile
                self.loadedOpportunityCostMapTemplate.setText(templateFile)
                self.comboBoxOpportunityCostMapTemplate.setCurrentIndex(self.comboBoxOpportunityCostMapTemplate.findText(templateFile))
                self.buttonSaveOpportunityCostMapTemplate.setEnabled(True)
            
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
        
        if tabName == MenuFactory.getLabel(MenuFactory.TAOPCOST_ABACUS_OPPORTUNITY_COST):
            dialogsToLoad = (
                'DialogLumensTAAbacusOpportunityCostCurve',
            )
        elif tabName == MenuFactory.getLabel(MenuFactory.TAOPCOST_OPPORTUNITY_COST_CURVE):
            dialogsToLoad = (
                'DialogLumensTAOpportunityCostCurve',
            )
        elif tabName == MenuFactory.getLabel(MenuFactory.TAOPCOST_OPPORTUNITY_COST_MAP):
            dialogsToLoad = (
                'DialogLumensTAOpportunityCostMap',
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
                MenuFactory.getLabel(MenuFactory.CONF_LOAD_EXISTING_CONFIGURATION),
                MenuFactory.getDescription(MenuFactory.CONF_LOAD_EXISTING_CONFIGURATION) + ' \'{0}\'?'.format(duplicateTemplate),
                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                QtGui.QMessageBox.No
            )
            
            if reply == QtGui.QMessageBox.Yes:
                if tabName == MenuFactory.getLabel(MenuFactory.TAOPCOST_ABACUS_OPPORTUNITY_COST):
                    self.handlerLoadAbacusOpportunityCostTemplate(duplicateTemplate)
                elif tabName == MenuFactory.getLabel(MenuFactory.TAOPCOST_OPPORTUNITY_COST_CURVE):
                    self.handlerLoadOpportunityCostCurveTemplate(duplicateTemplate)
                elif tabName == MenuFactory.getLabel(MenuFactory.TAOPCOST_OPPORTUNITY_COST_MAP):
                    self.handlerLoadOpportunityCostMapTemplate(duplicateTemplate)
                    
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
            templateFilePath = os.path.join(self.main.appSettings['DialogLumensOpenDatabase']['projectFolder'], self.main.appSettings['folderTA'], fileName)
            settings = QtCore.QSettings(templateFilePath, QtCore.QSettings.IniFormat)
            settings.setFallbacksEnabled(True) # only use ini files
            
            dialogsToSave = None
            
            if tabName == MenuFactory.getLabel(MenuFactory.TAOPCOST_ABACUS_OPPORTUNITY_COST):
                dialogsToSave = (
                    'DialogLumensTAAbacusOpportunityCostCurve',
                )
            elif tabName == MenuFactory.getLabel(MenuFactory.TAOPCOST_OPPORTUNITY_COST_CURVE):
                dialogsToSave = (
                    'DialogLumensTAOpportunityCostCurve',
                )
            elif tabName == MenuFactory.getLabel(MenuFactory.TAOPCOST_OPPORTUNITY_COST_MAP):
                dialogsToSave = (
                    'DialogLumensTAOpportunityCostMap',
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
        super(DialogLumensTAOpportunityCost, self).__init__(parent)
        
        self.main = parent
        self.dialogTitle = 'LUMENS ' + MenuFactory.getDescription(MenuFactory.TA_TITLE) + ' [' + MenuFactory.getLabel(MenuFactory.TAOPCOST_TITLE) + ']'
        self.settingsPath = os.path.join(self.main.appSettings['DialogLumensOpenDatabase']['projectFolder'], self.main.appSettings['folderTA'])
        self.currentAbacusOpportunityCostTemplate = None
        self.currentOpportunityCostCurveTemplate = None
        self.currentOpportunityCostMapTemplate = None
        
        # Init logging
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        if self.main.appSettings['debug']:
            print 'DEBUG: DialogLumensTAOpportunityCost init'
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
        
        # 'Abacus Opportunity Cost' tab buttons
        self.buttonSelectAOCProjectFile.clicked.connect(self.handlerSelectAOCProjectFile)
        self.buttonProcessAbacusOpportunityCost.clicked.connect(self.handlerProcessAbacusOpportunityCost)
        self.buttonHelpTAAbacusOpportunityCost.clicked.connect(lambda:self.handlerDialogHelp('TA'))
        self.buttonLoadAbacusOpportunityCostTemplate.clicked.connect(self.handlerLoadAbacusOpportunityCostTemplate)
        self.buttonSaveAbacusOpportunityCostTemplate.clicked.connect(self.handlerSaveAbacusOpportunityCostTemplate)
        self.buttonSaveAsAbacusOpportunityCostTemplate.clicked.connect(self.handlerSaveAsAbacusOpportunityCostTemplate)
        
        # 'Opportunity Cost Curve' tab buttons
        self.buttonSelectOCCCsvNPVTable.clicked.connect(self.handlerSelectOCCCsvNPVTable)
        self.buttonSelectOCCOutputOpportunityCostDatabase.clicked.connect(self.handlerSelectOCCOutputOpportunityCostDatabase)
        self.buttonSelectOCCOutputOpportunityCostReport.clicked.connect(self.handlerSelectOCCOutputOpportunityCostReport)
        self.buttonProcessOpportunityCostCurve.clicked.connect(self.handlerProcessOpportunityCostCurve)
        self.buttonHelpTAOpportunityCostCurve.clicked.connect(lambda:self.handlerDialogHelp('TA'))
        self.buttonLoadOpportunityCostCurveTemplate.clicked.connect(self.handlerLoadOpportunityCostCurveTemplate)
        self.buttonSaveOpportunityCostCurveTemplate.clicked.connect(self.handlerSaveOpportunityCostCurveTemplate)
        self.buttonSaveAsOpportunityCostCurveTemplate.clicked.connect(self.handlerSaveAsOpportunityCostCurveTemplate)
        
        # 'Opportunity Cost Map' tab buttons
        self.buttonSelectOCMCsvProfitability.clicked.connect(self.handlerSelectOCMCsvProfitability)
        self.buttonProcessOpportunityCostMap.clicked.connect(self.handlerProcessOpportunityCostMap)
        self.buttonHelpTAOpportunityCostMap.clicked.connect(lambda:self.handlerDialogHelp('TA'))
        self.buttonLoadOpportunityCostMapTemplate.clicked.connect(self.handlerLoadOpportunityCostMapTemplate)
        self.buttonSaveOpportunityCostMapTemplate.clicked.connect(self.handlerSaveOpportunityCostMapTemplate)
        self.buttonSaveAsOpportunityCostMapTemplate.clicked.connect(self.handlerSaveAsOpportunityCostMapTemplate)
        
    
    def setupUi(self, parent):
        """Method for building the dialog UI.
        
        Args:
            parent: the dialog's parent instance.
        """
        self.setStyleSheet('QDialog { background-color: rgb(225, 229, 237); }')
        self.dialogLayout = QtGui.QVBoxLayout()

        self.groupBoxTADialog = QtGui.QGroupBox(MenuFactory.getDescription(MenuFactory.TA_TITLE))
        self.layoutGroupBoxTADialog = QtGui.QVBoxLayout()
        self.layoutGroupBoxTADialog.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxTADialog.setLayout(self.layoutGroupBoxTADialog)
        self.labelTADialogInfo = QtGui.QLabel()
        self.labelTADialogInfo.setText(MenuFactory.getDescription(MenuFactory.TAOPCOST_TITLE))
        self.layoutGroupBoxTADialog.addWidget(self.labelTADialogInfo)

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
            width: 190px;      
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
        
        self.tabAbacusOpportunityCost = QtGui.QWidget()
        self.tabOpportunityCostCurve = QtGui.QWidget()
        self.tabOpportunityCostMap = QtGui.QWidget()
        self.tabLog = QtGui.QWidget()
        
        self.tabWidget.addTab(self.tabAbacusOpportunityCost, MenuFactory.getLabel(MenuFactory.TAOPCOST_ABACUS_OPPORTUNITY_COST))
        self.tabWidget.addTab(self.tabOpportunityCostCurve, MenuFactory.getLabel(MenuFactory.TAOPCOST_OPPORTUNITY_COST_CURVE))
        self.tabWidget.addTab(self.tabOpportunityCostMap, MenuFactory.getLabel(MenuFactory.TAOPCOST_OPPORTUNITY_COST_MAP))
        self.tabWidget.addTab(self.tabLog, MenuFactory.getLabel(MenuFactory.TA_LOG))
        
        ##self.layoutTabAbacusOpportunityCost = QtGui.QVBoxLayout()
        self.layoutTabAbacusOpportunityCost = QtGui.QGridLayout()
        ##self.layoutTabOpportunityCostCurve = QtGui.QVBoxLayout()
        self.layoutTabOpportunityCostCurve = QtGui.QGridLayout()
        ##self.layoutTabOpportunityCostMap = QtGui.QVBoxLayout()
        self.layoutTabOpportunityCostMap = QtGui.QGridLayout()
        self.layoutTabLog = QtGui.QVBoxLayout()
        
        self.tabAbacusOpportunityCost.setLayout(self.layoutTabAbacusOpportunityCost)
        self.tabOpportunityCostCurve.setLayout(self.layoutTabOpportunityCostCurve)
        self.tabOpportunityCostMap.setLayout(self.layoutTabOpportunityCostMap)
        self.tabLog.setLayout(self.layoutTabLog)

        self.dialogLayout.addWidget(self.groupBoxTADialog)
        self.dialogLayout.addWidget(self.tabWidget)
        
        #***********************************************************
        # Setup 'Abacus opportunity cost' tab
        #***********************************************************
        # 'Other' GroupBox
        self.groupBoxOther = QtGui.QGroupBox(MenuFactory.getLabel(MenuFactory.TAOPCOST_OTHER))
        self.layoutGroupBoxOther = QtGui.QVBoxLayout()
        self.layoutGroupBoxOther.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxOther.setLayout(self.layoutGroupBoxOther)
        self.layoutOtherInfo = QtGui.QVBoxLayout()
        self.layoutOther = QtGui.QGridLayout()
        self.layoutGroupBoxOther.addLayout(self.layoutOtherInfo)
        self.layoutGroupBoxOther.addLayout(self.layoutOther)
        
        self.labelOtherInfo = QtGui.QLabel()
        self.labelOtherInfo.setText(MenuFactory.getDescription(MenuFactory.TAOPCOST_OTHER))
        self.layoutOtherInfo.addWidget(self.labelOtherInfo)
        
        self.labelAOCProjectFile = QtGui.QLabel(parent)
        self.labelAOCProjectFile.setText(MenuFactory.getLabel(MenuFactory.TAOPCOST_ABACUS_PROJECT_FILE) + ':')
        self.layoutOther.addWidget(self.labelAOCProjectFile, 0, 0)
        
        self.lineEditAOCProjectFile = QtGui.QLineEdit(parent)
        self.lineEditAOCProjectFile.setReadOnly(True)
        self.layoutOther.addWidget(self.lineEditAOCProjectFile, 0, 1)
        
        self.buttonSelectAOCProjectFile = QtGui.QPushButton(parent)
        self.buttonSelectAOCProjectFile.setText('&' + MenuFactory.getLabel(MenuFactory.TAOPCOST_ABACUS_BROWSE))
        self.layoutOther.addWidget(self.buttonSelectAOCProjectFile, 0, 2)
        
        # Process tab button
        self.layoutButtonAbacusOpportunityCost = QtGui.QHBoxLayout()
        self.buttonProcessAbacusOpportunityCost = QtGui.QPushButton()
        self.buttonProcessAbacusOpportunityCost.setText('&' + MenuFactory.getLabel(MenuFactory.TAOPCOST_ABACUS_PROCESS))
        icon = QtGui.QIcon(':/ui/icons/iconActionHelp.png')
        self.buttonHelpTAAbacusOpportunityCost = QtGui.QPushButton()
        self.buttonHelpTAAbacusOpportunityCost.setIcon(icon)
        self.layoutButtonAbacusOpportunityCost.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonAbacusOpportunityCost.addWidget(self.buttonProcessAbacusOpportunityCost)
        self.layoutButtonAbacusOpportunityCost.addWidget(self.buttonHelpTAAbacusOpportunityCost)
        
        # Template GroupBox
        self.groupBoxAbacusOpportunityCostTemplate = QtGui.QGroupBox(MenuFactory.getLabel(MenuFactory.CONF_TEMPLATE))
        self.layoutGroupBoxAbacusOpportunityCostTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxAbacusOpportunityCostTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxAbacusOpportunityCostTemplate.setLayout(self.layoutGroupBoxAbacusOpportunityCostTemplate)
        self.layoutAbacusOpportunityCostTemplateInfo = QtGui.QVBoxLayout()
        self.layoutAbacusOpportunityCostTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxAbacusOpportunityCostTemplate.addLayout(self.layoutAbacusOpportunityCostTemplateInfo)
        self.layoutGroupBoxAbacusOpportunityCostTemplate.addLayout(self.layoutAbacusOpportunityCostTemplate)
        
        self.labelLoadedAbacusOpportunityCostTemplate = QtGui.QLabel()
        self.labelLoadedAbacusOpportunityCostTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_LOADED_TEMPLATE) + ':')
        self.layoutAbacusOpportunityCostTemplate.addWidget(self.labelLoadedAbacusOpportunityCostTemplate, 0, 0)
        
        self.loadedAbacusOpportunityCostTemplate = QtGui.QLabel()
        self.loadedAbacusOpportunityCostTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NONE))
        self.layoutAbacusOpportunityCostTemplate.addWidget(self.loadedAbacusOpportunityCostTemplate, 0, 1)
        
        self.labelAbacusOpportunityCostTemplate = QtGui.QLabel()
        self.labelAbacusOpportunityCostTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_TEMPLATE_NAME) + ':')
        self.layoutAbacusOpportunityCostTemplate.addWidget(self.labelAbacusOpportunityCostTemplate, 1, 0)
        
        self.comboBoxAbacusOpportunityCostTemplate = QtGui.QComboBox()
        self.comboBoxAbacusOpportunityCostTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxAbacusOpportunityCostTemplate.setDisabled(True)
        self.comboBoxAbacusOpportunityCostTemplate.addItem(MenuFactory.getLabel(MenuFactory.CONF_NO_TEMPLATE_FOUND))
        self.layoutAbacusOpportunityCostTemplate.addWidget(self.comboBoxAbacusOpportunityCostTemplate, 1, 1)
        
        self.layoutButtonAbacusOpportunityCostTemplate = QtGui.QHBoxLayout()
        self.layoutButtonAbacusOpportunityCostTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadAbacusOpportunityCostTemplate = QtGui.QPushButton()
        self.buttonLoadAbacusOpportunityCostTemplate.setDisabled(True)
        self.buttonLoadAbacusOpportunityCostTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadAbacusOpportunityCostTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_LOAD))
        self.buttonSaveAbacusOpportunityCostTemplate = QtGui.QPushButton()
        self.buttonSaveAbacusOpportunityCostTemplate.setDisabled(True)
        self.buttonSaveAbacusOpportunityCostTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAbacusOpportunityCostTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_SAVE))
        self.buttonSaveAsAbacusOpportunityCostTemplate = QtGui.QPushButton()
        self.buttonSaveAsAbacusOpportunityCostTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsAbacusOpportunityCostTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_SAVE_AS))
        self.layoutButtonAbacusOpportunityCostTemplate.addWidget(self.buttonLoadAbacusOpportunityCostTemplate)
        self.layoutButtonAbacusOpportunityCostTemplate.addWidget(self.buttonSaveAbacusOpportunityCostTemplate)
        self.layoutButtonAbacusOpportunityCostTemplate.addWidget(self.buttonSaveAsAbacusOpportunityCostTemplate)
        self.layoutGroupBoxAbacusOpportunityCostTemplate.addLayout(self.layoutButtonAbacusOpportunityCostTemplate)
        
        # Place the GroupBoxes
        self.layoutTabAbacusOpportunityCost.addWidget(self.groupBoxOther, 0, 0)
        self.layoutTabAbacusOpportunityCost.addLayout(self.layoutButtonAbacusOpportunityCost, 1, 0, 1, 2, QtCore.Qt.AlignRight)
        self.layoutTabAbacusOpportunityCost.addWidget(self.groupBoxAbacusOpportunityCostTemplate, 0, 1, 1, 1)
        self.layoutTabAbacusOpportunityCost.setColumnStretch(0, 3)
        self.layoutTabAbacusOpportunityCost.setColumnStretch(1, 1) # Smaller template column
        
        
        #***********************************************************
        # Setup 'Opportunity cost curve' tab
        #***********************************************************
        # 'Parameters' GroupBox
        self.groupBoxOCCParameters = QtGui.QGroupBox(MenuFactory.getLabel(MenuFactory.TAOPCOST_PARAMETERIZATION))
        self.layoutGroupBoxOCCParameters = QtGui.QVBoxLayout()
        self.layoutGroupBoxOCCParameters.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxOCCParameters.setLayout(self.layoutGroupBoxOCCParameters)
        self.layoutOCCParametersInfo = QtGui.QVBoxLayout()
        self.layoutOCCParameters = QtGui.QGridLayout()
        self.layoutGroupBoxOCCParameters.addLayout(self.layoutOCCParametersInfo)
        self.layoutGroupBoxOCCParameters.addLayout(self.layoutOCCParameters)
        
        self.labelOCCParametersInfo = QtGui.QLabel()
        self.labelOCCParametersInfo.setText(MenuFactory.getDescription(MenuFactory.TAOPCOST_PARAMETERIZATION))
        self.layoutOCCParametersInfo.addWidget(self.labelOCCParametersInfo)
        
        self.labelOCCCsvNPVTable = QtGui.QLabel(parent)
        self.labelOCCCsvNPVTable.setText(MenuFactory.getLabel(MenuFactory.TAOPCOST_PROFITABILITY_LOOKUP_TABLE) + ':')
        self.layoutOCCParameters.addWidget(self.labelOCCCsvNPVTable, 0, 0)
        
        self.lineEditOCCCsvNPVTable = QtGui.QLineEdit(parent)
        self.lineEditOCCCsvNPVTable.setReadOnly(True)
        self.layoutOCCParameters.addWidget(self.lineEditOCCCsvNPVTable, 0, 1)
        
        self.buttonSelectOCCCsvNPVTable = QtGui.QPushButton()
        self.buttonSelectOCCCsvNPVTable.setText(MenuFactory.getLabel(MenuFactory.TA_BROWSE))
        self.layoutOCCParameters.addWidget(self.buttonSelectOCCCsvNPVTable, 0, 2)
        
        self.labelOCCCostThreshold = QtGui.QLabel()
        self.labelOCCCostThreshold.setText(MenuFactory.getLabel(MenuFactory.TAOPCOST_COST_THRESHOLD) + ':')
        self.layoutOCCParameters.addWidget(self.labelOCCCostThreshold, 1, 0)
        
        self.spinBoxOCCCostThreshold = QtGui.QSpinBox()
        self.spinBoxOCCCostThreshold.setValue(5)
        self.layoutOCCParameters.addWidget(self.spinBoxOCCCostThreshold, 1, 1)
        self.labelOCCCostThreshold.setBuddy(self.spinBoxOCCCostThreshold)
        
        self.labelOCCOutputOpportunityCostDatabase = QtGui.QLabel()
        self.labelOCCOutputOpportunityCostDatabase.setText(MenuFactory.getLabel(MenuFactory.TAOPCOST_OPCOST_DATABASE) + ':')
        self.layoutOCCParameters.addWidget(self.labelOCCOutputOpportunityCostDatabase, 2, 0)
        
        self.lineEditOCCOutputOpportunityCostDatabase = QtGui.QLineEdit()
        self.lineEditOCCOutputOpportunityCostDatabase.setReadOnly(True)
        self.layoutOCCParameters.addWidget(self.lineEditOCCOutputOpportunityCostDatabase, 2, 1)
        
        self.buttonSelectOCCOutputOpportunityCostDatabase = QtGui.QPushButton(parent)
        self.buttonSelectOCCOutputOpportunityCostDatabase.setText(MenuFactory.getLabel(MenuFactory.TA_BROWSE))
        self.layoutOCCParameters.addWidget(self.buttonSelectOCCOutputOpportunityCostDatabase, 2, 2)
        
        self.labelOCCOutputOpportunityCostReport = QtGui.QLabel()
        self.labelOCCOutputOpportunityCostReport.setText(MenuFactory.getLabel(MenuFactory.TAOPCOST_OPCOST_REPORT) + ':')
        self.layoutOCCParameters.addWidget(self.labelOCCOutputOpportunityCostReport, 3, 0)
        
        self.lineEditOCCOutputOpportunityCostReport = QtGui.QLineEdit()
        self.lineEditOCCOutputOpportunityCostReport.setReadOnly(True)
        self.layoutOCCParameters.addWidget(self.lineEditOCCOutputOpportunityCostReport, 3, 1)
        
        self.buttonSelectOCCOutputOpportunityCostReport = QtGui.QPushButton(parent)
        self.buttonSelectOCCOutputOpportunityCostReport.setText(MenuFactory.getLabel(MenuFactory.TA_BROWSE))
        self.layoutOCCParameters.addWidget(self.buttonSelectOCCOutputOpportunityCostReport, 3, 2)
        
        # Process tab button
        self.layoutButtonOpportunityCostCurve = QtGui.QHBoxLayout()
        self.buttonProcessOpportunityCostCurve = QtGui.QPushButton()
        self.buttonProcessOpportunityCostCurve.setText(MenuFactory.getLabel(MenuFactory.TA_PROCESS))
        self.buttonHelpTAOpportunityCostCurve = QtGui.QPushButton()
        self.buttonHelpTAOpportunityCostCurve.setIcon(icon)
        self.layoutButtonOpportunityCostCurve.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonOpportunityCostCurve.addWidget(self.buttonProcessOpportunityCostCurve)
        self.layoutButtonOpportunityCostCurve.addWidget(self.buttonHelpTAOpportunityCostCurve)
        
        # Template GroupBox
        self.groupBoxOpportunityCostCurveTemplate = QtGui.QGroupBox(MenuFactory.getLabel(MenuFactory.CONF_TEMPLATE))
        self.layoutGroupBoxOpportunityCostCurveTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxOpportunityCostCurveTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxOpportunityCostCurveTemplate.setLayout(self.layoutGroupBoxOpportunityCostCurveTemplate)
        self.layoutOpportunityCostCurveTemplateInfo = QtGui.QVBoxLayout()
        self.layoutOpportunityCostCurveTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxOpportunityCostCurveTemplate.addLayout(self.layoutOpportunityCostCurveTemplateInfo)
        self.layoutGroupBoxOpportunityCostCurveTemplate.addLayout(self.layoutOpportunityCostCurveTemplate)
        
        self.labelLoadedOpportunityCostCurveTemplate = QtGui.QLabel()
        self.labelLoadedOpportunityCostCurveTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_LOADED_TEMPLATE) + ':')
        self.layoutOpportunityCostCurveTemplate.addWidget(self.labelLoadedOpportunityCostCurveTemplate, 0, 0)
        
        self.loadedOpportunityCostCurveTemplate = QtGui.QLabel()
        self.loadedOpportunityCostCurveTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NONE))
        self.layoutOpportunityCostCurveTemplate.addWidget(self.loadedOpportunityCostCurveTemplate, 0, 1)
        
        self.labelOpportunityCostCurveTemplate = QtGui.QLabel()
        self.labelOpportunityCostCurveTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_TEMPLATE_NAME) + ':')
        self.layoutOpportunityCostCurveTemplate.addWidget(self.labelOpportunityCostCurveTemplate, 1, 0)
        
        self.comboBoxOpportunityCostCurveTemplate = QtGui.QComboBox()
        self.comboBoxOpportunityCostCurveTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxOpportunityCostCurveTemplate.setDisabled(True)
        self.comboBoxOpportunityCostCurveTemplate.addItem(MenuFactory.getLabel(MenuFactory.CONF_NO_TEMPLATE_FOUND))
        self.layoutOpportunityCostCurveTemplate.addWidget(self.comboBoxOpportunityCostCurveTemplate, 1, 1)
        
        self.layoutButtonOpportunityCostCurveTemplate = QtGui.QHBoxLayout()
        self.layoutButtonOpportunityCostCurveTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadOpportunityCostCurveTemplate = QtGui.QPushButton()
        self.buttonLoadOpportunityCostCurveTemplate.setDisabled(True)
        self.buttonLoadOpportunityCostCurveTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadOpportunityCostCurveTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_LOAD))
        self.buttonSaveOpportunityCostCurveTemplate = QtGui.QPushButton()
        self.buttonSaveOpportunityCostCurveTemplate.setDisabled(True)
        self.buttonSaveOpportunityCostCurveTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveOpportunityCostCurveTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_SAVE))
        self.buttonSaveAsOpportunityCostCurveTemplate = QtGui.QPushButton()
        self.buttonSaveAsOpportunityCostCurveTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsOpportunityCostCurveTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_SAVE_AS))
        self.layoutButtonOpportunityCostCurveTemplate.addWidget(self.buttonLoadOpportunityCostCurveTemplate)
        self.layoutButtonOpportunityCostCurveTemplate.addWidget(self.buttonSaveOpportunityCostCurveTemplate)
        self.layoutButtonOpportunityCostCurveTemplate.addWidget(self.buttonSaveAsOpportunityCostCurveTemplate)
        self.layoutGroupBoxOpportunityCostCurveTemplate.addLayout(self.layoutButtonOpportunityCostCurveTemplate)
        
        # Place the GroupBoxes
        self.layoutTabOpportunityCostCurve.addWidget(self.groupBoxOCCParameters, 0, 0)
        self.layoutTabOpportunityCostCurve.addLayout(self.layoutButtonOpportunityCostCurve, 1, 0, 1, 2, QtCore.Qt.AlignRight)
        self.layoutTabOpportunityCostCurve.addWidget(self.groupBoxOpportunityCostCurveTemplate, 0, 1, 1, 1)
        self.layoutTabOpportunityCostCurve.setColumnStretch(0, 3)
        self.layoutTabOpportunityCostCurve.setColumnStretch(1, 1) # Smaller template column
        
        ##self.layoutTabOpportunityCostCurve.insertStretch(2, 1)
        
        ##self.layoutTabOpportunityCostCurve.setStretchFactor(self.groupBoxOCCParameters, 4)
        
        
        #***********************************************************
        # Setup 'Opportunity cost map' tab
        #***********************************************************
        # 'Parameters' GroupBox
        self.groupBoxOCMParameters = QtGui.QGroupBox(MenuFactory.getLabel(MenuFactory.TAOPCOST_PARAMETERIZATION))
        self.layoutGroupBoxOCMParameters = QtGui.QVBoxLayout()
        self.layoutGroupBoxOCMParameters.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxOCMParameters.setLayout(self.layoutGroupBoxOCMParameters)
        self.layoutOCMParametersInfo = QtGui.QVBoxLayout()
        self.layoutOCMParameters = QtGui.QGridLayout()
        self.layoutGroupBoxOCMParameters.addLayout(self.layoutOCMParametersInfo)
        self.layoutGroupBoxOCMParameters.addLayout(self.layoutOCMParameters)
        
        self.labelOCMParametersInfo = QtGui.QLabel()
        self.labelOCMParametersInfo.setText(MenuFactory.getDescription(MenuFactory.TAOPCOST_PARAMETERIZATION))
        self.layoutOCMParametersInfo.addWidget(self.labelOCMParametersInfo)
        
        self.labelOCMCsvProfitability = QtGui.QLabel(parent)
        self.labelOCMCsvProfitability.setText(MenuFactory.getLabel(MenuFactory.TAOPCOST_PROFITABILITY_LOOKUP_TABLE) + ':')
        self.layoutOCMParameters.addWidget(self.labelOCMCsvProfitability, 0, 0)
        
        self.lineEditOCMCsvProfitability = QtGui.QLineEdit(parent)
        self.lineEditOCMCsvProfitability.setReadOnly(True)
        self.layoutOCMParameters.addWidget(self.lineEditOCMCsvProfitability, 0, 1)
        
        self.buttonSelectOCMCsvProfitability = QtGui.QPushButton()
        self.buttonSelectOCMCsvProfitability.setText(MenuFactory.getLabel(MenuFactory.TA_BROWSE))
        self.layoutOCMParameters.addWidget(self.buttonSelectOCMCsvProfitability, 0, 2)
        
        # Process tab button
        self.layoutButtonOpportunityCostMap = QtGui.QHBoxLayout()
        self.buttonProcessOpportunityCostMap = QtGui.QPushButton()
        self.buttonProcessOpportunityCostMap.setText(MenuFactory.getLabel(MenuFactory.TA_PROCESS))
        self.buttonHelpTAOpportunityCostMap = QtGui.QPushButton()
        self.buttonHelpTAOpportunityCostMap.setIcon(icon)
        self.layoutButtonOpportunityCostMap.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonOpportunityCostMap.addWidget(self.buttonProcessOpportunityCostMap)
        self.layoutButtonOpportunityCostMap.addWidget(self.buttonHelpTAOpportunityCostMap)
        
        # Template GroupBox
        self.groupBoxOpportunityCostMapTemplate = QtGui.QGroupBox(MenuFactory.getLabel(MenuFactory.CONF_TEMPLATE))
        self.layoutGroupBoxOpportunityCostMapTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxOpportunityCostMapTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxOpportunityCostMapTemplate.setLayout(self.layoutGroupBoxOpportunityCostMapTemplate)
        self.layoutOpportunityCostMapTemplateInfo = QtGui.QVBoxLayout()
        self.layoutOpportunityCostMapTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxOpportunityCostMapTemplate.addLayout(self.layoutOpportunityCostMapTemplateInfo)
        self.layoutGroupBoxOpportunityCostMapTemplate.addLayout(self.layoutOpportunityCostMapTemplate)
        
        self.labelLoadedOpportunityCostMapTemplate = QtGui.QLabel()
        self.labelLoadedOpportunityCostMapTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_LOADED_TEMPLATE) + ':')
        self.layoutOpportunityCostMapTemplate.addWidget(self.labelLoadedOpportunityCostMapTemplate, 0, 0)
        
        self.loadedOpportunityCostMapTemplate = QtGui.QLabel()
        self.loadedOpportunityCostMapTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NONE))
        self.layoutOpportunityCostMapTemplate.addWidget(self.loadedOpportunityCostMapTemplate, 0, 1)
        
        self.labelOpportunityCostMapTemplate = QtGui.QLabel()
        self.labelOpportunityCostMapTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_TEMPLATE_NAME) + ':')
        self.layoutOpportunityCostMapTemplate.addWidget(self.labelOpportunityCostMapTemplate, 1, 0)
        
        self.comboBoxOpportunityCostMapTemplate = QtGui.QComboBox()
        self.comboBoxOpportunityCostMapTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxOpportunityCostMapTemplate.setDisabled(True)
        self.comboBoxOpportunityCostMapTemplate.addItem(MenuFactory.getLabel(MenuFactory.CONF_NO_TEMPLATE_FOUND))
        self.layoutOpportunityCostMapTemplate.addWidget(self.comboBoxOpportunityCostMapTemplate, 1, 1)
        
        self.layoutButtonOpportunityCostMapTemplate = QtGui.QHBoxLayout()
        self.layoutButtonOpportunityCostMapTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadOpportunityCostMapTemplate = QtGui.QPushButton()
        self.buttonLoadOpportunityCostMapTemplate.setDisabled(True)
        self.buttonLoadOpportunityCostMapTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadOpportunityCostMapTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_LOAD))
        self.buttonSaveOpportunityCostMapTemplate = QtGui.QPushButton()
        self.buttonSaveOpportunityCostMapTemplate.setDisabled(True)
        self.buttonSaveOpportunityCostMapTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveOpportunityCostMapTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_SAVE))
        self.buttonSaveAsOpportunityCostMapTemplate = QtGui.QPushButton()
        self.buttonSaveAsOpportunityCostMapTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsOpportunityCostMapTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_SAVE_AS))
        self.layoutButtonOpportunityCostMapTemplate.addWidget(self.buttonLoadOpportunityCostMapTemplate)
        self.layoutButtonOpportunityCostMapTemplate.addWidget(self.buttonSaveOpportunityCostMapTemplate)
        self.layoutButtonOpportunityCostMapTemplate.addWidget(self.buttonSaveAsOpportunityCostMapTemplate)
        self.layoutGroupBoxOpportunityCostMapTemplate.addLayout(self.layoutButtonOpportunityCostMapTemplate)
        
        # Place the GroupBoxes
        self.layoutTabOpportunityCostMap.addWidget(self.groupBoxOCMParameters, 0, 0)
        self.layoutTabOpportunityCostMap.addLayout(self.layoutButtonOpportunityCostMap, 1, 0, 1, 2, QtCore.Qt.AlignRight)
        self.layoutTabOpportunityCostMap.addWidget(self.groupBoxOpportunityCostMapTemplate, 0, 1, 1, 1)
        self.layoutTabOpportunityCostMap.setColumnStretch(0, 3)
        self.layoutTabOpportunityCostMap.setColumnStretch(1, 1) # Smaller template column
        
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
        self.labelHistoryLogInfo.setText(MenuFactory.getLabel(MenuFactory.TA_HISTORY_LOG))
        self.layoutHistoryLogInfo.addWidget(self.labelHistoryLogInfo)
        
        self.log_box = QPlainTextEditLogger(self)
        self.layoutHistoryLog.addWidget(self.log_box.widget)
        
        self.layoutTabLog.addWidget(self.groupBoxHistoryLog)
        
        
        self.setLayout(self.dialogLayout)
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(700, 480)
        self.resize(parent.sizeHint())
    
    
    def showEvent(self, event):
        """Overload method that is called when the dialog widget is shown.
        
        Args:
            event (QShowEvent): the show widget event.
        """
        super(DialogLumensTAOpportunityCost, self).showEvent(event)
    
    
    def closeEvent(self, event):
        """Overload method that is called when the dialog widget is closed.
        
        Args:
            event (QCloseEvent): the close widget event.
        """
        super(DialogLumensTAOpportunityCost, self).closeEvent(event)
    
    
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
    
    
    #***********************************************************
    # 'Abacus Opportunity Cost' tab QPushButton handlers
    #***********************************************************
    def handlerLoadAbacusOpportunityCostTemplate(self, fileName=None):
        """Slot method for loading a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.comboBoxAbacusOpportunityCostTemplate.currentText()
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
            self.loadTemplate(MenuFactory.getLabel(MenuFactory.TAOPCOST_ABACUS_OPPORTUNITY_COST), templateFile)
    
    
    def handlerSaveAbacusOpportunityCostTemplate(self, fileName=None):
        """Slot method for saving a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.currentAbacusOpportunityCostTemplate
        
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
            self.saveTemplate(MenuFactory.getLabel(MenuFactory.TAOPCOST_ABACUS_OPPORTUNITY_COST), templateFile)
            return True
        else:
            return False
    
    
    def handlerSaveAsAbacusOpportunityCostTemplate(self):
        """Slot method for saving a module template to a new file.
        """
        fileName, ok = QtGui.QInputDialog.getText(self, MenuFactory.getLabel(MenuFactory.CONF_SAVE_AS), MenuFactory.getDescription(MenuFactory.CONF_SAVE_AS) + ':')
        fileSaved = False
        
        if ok:
            now = QtCore.QDateTime.currentDateTime().toString('yyyyMMdd-hhmmss')
            fileName = now + '__' + fileName + '.ini'
            
            if os.path.exists(os.path.join(self.settingsPath, fileName)):
                fileSaved = self.handlerSaveAbacusOpportunityCostTemplate(fileName)
            else:
                self.saveTemplate(MenuFactory.getLabel(MenuFactory.TAOPCOST_ABACUS_OPPORTUNITY_COST), fileName)
                fileSaved = True
            
            self.loadTemplateFiles()
            
            # Load the newly saved template file
            if fileSaved:
                self.handlerLoadAbacusOpportunityCostTemplate(fileName)
    
    
    def handlerSelectAOCProjectFile(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Project File', QtCore.QDir.homePath(), 'Project File (*{0})'.format(self.main.appSettings['selectCarfileExt'])))
        
        if file:
            self.lineEditAOCProjectFile.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    #***********************************************************
    # 'Opportunity Cost Curve' tab QPushButton handlers
    #***********************************************************
    def handlerLoadOpportunityCostCurveTemplate(self, fileName=None):
        """Slot method for loading a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.comboBoxOpportunityCostCurveTemplate.currentText()
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
            self.loadTemplate(MenuFactory.getLabel(MenuFactory.TAOPCOST_OPPORTUNITY_COST_CURVE), templateFile)
    
    
    def handlerSaveOpportunityCostCurveTemplate(self, fileName=None):
        """Slot method for saving a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.currentOpportunityCostCurveTemplate
        
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
            self.saveTemplate(MenuFactory.getLabel(MenuFactory.TAOPCOST_OPPORTUNITY_COST_CURVE), templateFile)
            return True
        else:
            return False
    
    
    def handlerSaveAsOpportunityCostCurveTemplate(self):
        """Slot method for saving a module template to a new file.
        """
        fileName, ok = QtGui.QInputDialog.getText(self, MenuFactory.getLabel(MenuFactory.CONF_SAVE_AS), MenuFactory.getDescription(MenuFactory.CONF_SAVE_AS) + ':')
        fileSaved = False
        
        if ok:
            now = QtCore.QDateTime.currentDateTime().toString('yyyyMMdd-hhmmss')
            fileName = now + '__' + fileName + '.ini'
            
            if os.path.exists(os.path.join(self.settingsPath, fileName)):
                fileSaved = self.handlerSaveOpportunityCostCurveTemplate(fileName)
            else:
                self.saveTemplate(MenuFactory.getLabel(MenuFactory.TAOPCOST_OPPORTUNITY_COST_CURVE), fileName)
                fileSaved = True
            
            self.loadTemplateFiles()
            
            # Load the newly saved template file
            if fileSaved:
                self.handlerLoadOpportunityCostCurveTemplate(fileName)
    
    
    def handlerSelectOCCCsvNPVTable(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, MenuFactory.getLabel(MenuFactory.MSG_TA_SELECT_NPV_TABLE), QtCore.QDir.homePath(), MenuFactory.getDescription(MenuFactory.MSG_TA_SELECT_NPV_TABLE) + ' (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditOCCCsvNPVTable.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectOCCOutputOpportunityCostDatabase(self):
        """Slot method for a file select dialog.
        """
        outputfile = unicode(QtGui.QFileDialog.getSaveFileName(
            self, MenuFactory.getLabel(MenuFactory.MSG_TA_SELECT_OPCOST_DB), QtCore.QDir.homePath(), MenuFactory.getDescription(MenuFactory.MSG_TA_SELECT_OPCOST_DB) + ' (*{0})'.format(self.main.appSettings['selectDatabasefileExt'])))
        
        if outputfile:
            self.lineEditOCCOutputOpportunityCostDatabase.setText(outputfile)
            logging.getLogger(type(self).__name__).info('select output file: %s', outputfile)
    
    
    def handlerSelectOCCOutputOpportunityCostReport(self):
        """Slot method for a file select dialog.
        """
        outputfile = unicode(QtGui.QFileDialog.getSaveFileName(
            self, MenuFactory.getLabel(MenuFactory.MSG_TA_SELECT_OPCOST_REPORT), QtCore.QDir.homePath(), MenuFactory.getDescription(MenuFactory.MSG_TA_SELECT_OPCOST_REPORT) + ' (*{0})'.format(self.main.appSettings['selectHTMLfileExt'])))
        
        if outputfile:
            self.lineEditOCCOutputOpportunityCostReport.setText(outputfile)
            logging.getLogger(type(self).__name__).info('select output file: %s', outputfile)
    
    
    #***********************************************************
    # 'Opportunity Cost Map' tab QPushButton handlers
    #***********************************************************
    def handlerLoadOpportunityCostMapTemplate(self, fileName=None):
        """Slot method for loading a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.comboBoxOpportunityCostMapTemplate.currentText()
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
            self.loadTemplate(MenuFactory.getLabel(MenuFactory.TAOPCOST_OPPORTUNITY_COST_MAP), templateFile)
    
    
    def handlerSaveOpportunityCostMapTemplate(self, fileName=None):
        """Slot method for saving a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.currentOpportunityCostMapTemplate
        
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
            self.saveTemplate(MenuFactory.getLabel(MenuFactory.TAOPCOST_OPPORTUNITY_COST_MAP), templateFile)
            return True
        else:
            return False
    
    
    def handlerSaveAsOpportunityCostMapTemplate(self):
        """Slot method for saving a module template to a new file.
        """
        fileName, ok = QtGui.QInputDialog.getText(self, MenuFactory.getLabel(MenuFactory.CONF_SAVE_AS), MenuFactory.getDescription(MenuFactory.CONF_SAVE_AS) + ':')
        fileSaved = False
        
        if ok:
            now = QtCore.QDateTime.currentDateTime().toString('yyyyMMdd-hhmmss')
            fileName = now + '__' + fileName + '.ini'
            
            if os.path.exists(os.path.join(self.settingsPath, fileName)):
                fileSaved = self.handlerSaveOpportunityCostMapTemplate(fileName)
            else:
                self.saveTemplate(MenuFactory.getLabel(MenuFactory.TAOPCOST_OPPORTUNITY_COST_MAP), fileName)
                fileSaved = True
            
            self.loadTemplateFiles()
            
            # Load the newly saved template file
            if fileSaved:
                self.handlerLoadOpportunityCostMapTemplate(fileName)
    
    
    def handlerSelectOCMCsvProfitability(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, MenuFactory.getLabel(MenuFactory.MSG_TA_SELECT_PROFIT_TABLE), QtCore.QDir.homePath(), MenuFactory.getDescription(MenuFactory.MSG_TA_SELECT_PROFIT_TABLE) + ' (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditOCMCsvProfitability.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    #***********************************************************
    # Process tabs
    #***********************************************************
    def setAppSettings(self):
        """Set the required values from the form widgets.
        """
        # 'Abacus Opportunity Cost' tab fields
        self.main.appSettings['DialogLumensTAAbacusOpportunityCostCurve']['projectFile'] = unicode(self.lineEditAOCProjectFile.text())
        
        # 'Opportunity Cost Curve' tab fields
        self.main.appSettings['DialogLumensTAOpportunityCostCurve']['csvNPVTable'] = unicode(self.lineEditOCCCsvNPVTable.text())
        self.main.appSettings['DialogLumensTAOpportunityCostCurve']['costThreshold'] = self.spinBoxOCCCostThreshold.value()
        
        outputOpportunityCostDatabase = unicode(self.lineEditOCCOutputOpportunityCostDatabase.text())
        outputOpportunityCostReport = unicode(self.lineEditOCCOutputOpportunityCostReport.text())
        
        if not outputOpportunityCostDatabase:
            self.main.appSettings['DialogLumensTAOpportunityCostCurve']['outputOpportunityCostDatabase'] = '__UNSET__'
        
        if not outputOpportunityCostReport:
            self.main.appSettings['DialogLumensTAOpportunityCostCurve']['outputOpportunityCostReport'] = '__UNSET__'
        
        # 'Opportunity Cost Map' tab fields
        self.main.appSettings['DialogLumensTAOpportunityCostMap']['csvProfitability'] = unicode(self.lineEditOCMCsvProfitability.text())
    
    
    def handlerProcessAbacusOpportunityCost(self):
        """Slot method to pass the form values and execute the "TA Abacus Opportunity Cost" R algorithm.
        
        The "TA Abacus Opportunity Cost" process calls the following algorithm:
        1. modeler:abacus_opportunity_cost
        """
        self.setAppSettings()
        
        formName = 'DialogLumensTAAbacusOpportunityCostCurve'
        algName = 'modeler:abacus_opportunity_cost'
        
        if self.validForm(formName):
            logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
            logging.getLogger(self.historyLog).info('alg start: %s' % formName)
            self.buttonProcessAbacusOpportunityCost.setDisabled(True)
            
            # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
            self.main.setWindowState(QtCore.Qt.WindowMinimized)
            
            outputs = general.runalg(
                algName,
                self.main.appSettings[formName]['projectFile'],
            )
            
            # Display ROut file in debug mode
            if self.main.appSettings['debug']:
                dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                dialog.exec_()
            
            ##print outputs
            
            # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
            self.main.setWindowState(QtCore.Qt.WindowActive)
            
            self.outputsMessageBox(algName, outputs, '', '')
            
            self.buttonProcessAbacusOpportunityCost.setEnabled(True)
            logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
            logging.getLogger(self.historyLog).info('alg end: %s' % formName)
    
    
    def handlerProcessOpportunityCostCurve(self):
        """Slot method to pass the form values and execute the "TA Opportunity Cost Curve" R algorithm.
        
        The "TA Opportunity Cost Curve" process calls the following algorithm:
        1. modeler:opportunity_cost
        """
        self.setAppSettings()
        
        formName = 'DialogLumensTAOpportunityCostCurve'
        algName = 'modeler:opportunity_cost'
        
        if self.validForm(formName):
            logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
            logging.getLogger(self.historyLog).info('alg start: %s' % formName)
            self.buttonProcessOpportunityCostCurve.setDisabled(True)
            
            outputOpportunityCostDatabase = self.main.appSettings[formName]['outputOpportunityCostDatabase']
            outputOpportunityCostReport = self.main.appSettings[formName]['outputOpportunityCostReport']
            
            if outputOpportunityCostDatabase == '__UNSET__':
                outputOpportunityCostDatabase = None
            
            if outputOpportunityCostReport == '__UNSET__':
                outputOpportunityCostReport = None
            
            # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
            self.main.setWindowState(QtCore.Qt.WindowMinimized)
            
            outputs = general.runalg(
                algName,
                self.main.appSettings[formName]['csvNPVTable'],
                self.main.appSettings[formName]['costThreshold'],
                outputOpportunityCostDatabase,
                outputOpportunityCostReport,
            )
            
            # Display ROut file in debug mode
            if self.main.appSettings['debug']:
                dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                dialog.exec_()
            
            ##print outputs
            
            # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
            self.main.setWindowState(QtCore.Qt.WindowActive)
            
            self.outputsMessageBox(algName, outputs, '', '')
            
            self.buttonProcessOpportunityCostCurve.setEnabled(True)
            logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
            logging.getLogger(self.historyLog).info('alg end: %s' % formName)
    
    
    def handlerProcessOpportunityCostMap(self):
        """Slot method to pass the form values and execute the "TA Opportunity Cost Map" R algorithm.
        
        The "TA Opportunity Cost Map" process calls the following algorithm:
        1. modeler:opcost_map
        """
        self.setAppSettings()
        
        formName = 'DialogLumensTAOpportunityCostMap'
        algName = 'modeler:opcost_map'
        
        if self.validForm(formName):
            logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
            logging.getLogger(self.historyLog).info('alg start: %s' % formName)
            self.buttonProcessOpportunityCostMap.setDisabled(True)
            
            # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
            self.main.setWindowState(QtCore.Qt.WindowMinimized)
            
            outputs = general.runalg(
                algName,
                self.main.appSettings[formName]['csvProfitability'],
            )
            
            # Display ROut file in debug mode
            if self.main.appSettings['debug']:
                dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                dialog.exec_()
            
            ##print outputs
            
            # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
            self.main.setWindowState(QtCore.Qt.WindowActive)
            
            self.outputsMessageBox(algName, outputs, '', '')
            
            self.buttonProcessOpportunityCostMap.setEnabled(True)
            logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
            logging.getLogger(self.historyLog).info('alg end: %s' % formName)
    
