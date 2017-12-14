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


class DialogLumensTA(QtGui.QDialog, DialogLumensBase):
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
        
        if tabName == 'Abacus Opportunity Cost':
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
        elif tabName == 'Opportunity Cost Curve':
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
        elif tabName == 'Opportunity Cost Map':
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
        
        if tabName == 'Abacus Opportunity Cost':
            dialogsToLoad = (
                'DialogLumensTAAbacusOpportunityCostCurve',
            )
        elif tabName == 'Opportunity Cost Curve':
            dialogsToLoad = (
                'DialogLumensTAOpportunityCostCurve',
            )
        elif tabName == 'Opportunity Cost Map':
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
                'Load Existing Template',
                'The template you are about to save matches an existing template.\nDo you want to load \'{0}\' instead?'.format(duplicateTemplate),
                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                QtGui.QMessageBox.No
            )
            
            if reply == QtGui.QMessageBox.Yes:
                if tabName == 'Abacus Opportunity Cost':
                    self.handlerLoadAbacusOpportunityCostTemplate(duplicateTemplate)
                elif tabName == 'Opportunity Cost Curve':
                    self.handlerLoadOpportunityCostCurveTemplate(duplicateTemplate)
                elif tabName == 'Opportunity Cost Map':
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
            
            if tabName == 'Abacus Opportunity Cost':
                dialogsToSave = (
                    'DialogLumensTAAbacusOpportunityCostCurve',
                )
            elif tabName == 'Opportunity Cost Curve':
                dialogsToSave = (
                    'DialogLumensTAOpportunityCostCurve',
                )
            elif tabName == 'Opportunity Cost Map':
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
        super(DialogLumensTA, self).__init__(parent)
        
        self.main = parent
        self.dialogTitle = 'Trade-Off Analysis'
        self.settingsPath = os.path.join(self.main.appSettings['DialogLumensOpenDatabase']['projectFolder'], self.main.appSettings['folderTA'])
        self.currentAbacusOpportunityCostTemplate = None
        self.currentOpportunityCostCurveTemplate = None
        self.currentOpportunityCostMapTemplate = None
        
        # Init logging
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        if self.main.appSettings['debug']:
            print 'DEBUG: DialogLumensTA init'
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

        self.groupBoxTADialog = QtGui.QGroupBox('Trade-Off Analysis')
        self.layoutGroupBoxTADialog = QtGui.QVBoxLayout()
        self.layoutGroupBoxTADialog.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxTADialog.setLayout(self.layoutGroupBoxTADialog)
        self.labelTADialogInfo = QtGui.QLabel()
        self.labelTADialogInfo.setText('\n')
        self.labelTADialogInfo.setWordWrap(True)
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
        
        self.tabOpportunityCost = QtGui.QWidget()
        self.tabRegionalEconomy = QtGui.QWidget()
        self.tabLog = QtGui.QWidget()
        
        self.tabWidget.addTab(self.tabOpportunityCost, 'Opportunity Cost')
        self.tabWidget.addTab(self.tabRegionalEconomy, 'Regional Economy')
        self.tabWidget.addTab(self.tabLog, 'Log')
        
        self.layoutTabOpportunityCost = QtGui.QVBoxLayout()
        self.layoutTabRegionalEconomy = QtGui.QVBoxLayout()
        self.layoutTabLog = QtGui.QVBoxLayout()
        
        self.tabOpportunityCost.setLayout(self.layoutTabOpportunityCost)
        self.tabRegionalEconomy.setLayout(self.layoutTabRegionalEconomy)
        self.tabLog.setLayout(self.layoutTabLog)

        self.dialogLayout.addWidget(self.groupBoxTADialog)
        self.dialogLayout.addWidget(self.tabWidget)
        
        
        #***********************************************************
        # Setup 'Opportunity Cost' tab
        #***********************************************************
        self.tabWidgetOpportunityCost = QtGui.QTabWidget()
        OpportunityCostTabWidgetStylesheet = """
        QTabWidget QWidget {
            background-color: rgb(217, 229, 252);
            color: rgb(95, 98, 102);
        }
        QTabBar::tab {
            background-color: rgb(244, 248, 252);
            height: 35px;
            width: 200px;
        }
        QTabBar::tab:selected, QTabBar::tab:hover {
            background-color: rgb(217, 229, 252);
            font: bold;
        }
        """
        self.tabWidgetOpportunityCost.setStyleSheet(OpportunityCostTabWidgetStylesheet)
        
        self.tabAbacusOpportunityCost = QtGui.QWidget()
        self.tabOpportunityCostCurve = QtGui.QWidget()
        self.tabOpportunityCostMap = QtGui.QWidget()
        
        self.tabWidgetOpportunityCost.addTab(self.tabAbacusOpportunityCost, 'Abacus Opportunity Cost')
        self.tabWidgetOpportunityCost.addTab(self.tabOpportunityCostCurve, 'Opportunity Cost Curve')
        self.tabWidgetOpportunityCost.addTab(self.tabOpportunityCostMap, 'Opportunity Cost Map')
        
        self.layoutTabOpportunityCost.addWidget(self.tabWidgetOpportunityCost)
        
        self.layoutTabAbacusOpportunityCost = QtGui.QGridLayout()
        self.layoutTabOpportunityCostCurve = QtGui.QGridLayout()
        self.layoutTabOpportunityCostMap = QtGui.QGridLayout()
        
        self.tabAbacusOpportunityCost.setLayout(self.layoutTabAbacusOpportunityCost)
        self.tabOpportunityCostCurve.setLayout(self.layoutTabOpportunityCostCurve)
        self.tabOpportunityCostMap.setLayout(self.layoutTabOpportunityCostMap)
        
        #***********************************************************
        # Setup 'Abacus opportunity cost' tab
        #***********************************************************
        # 'Other' GroupBox
        self.groupBoxOther = QtGui.QGroupBox('Other')
        self.layoutGroupBoxOther = QtGui.QVBoxLayout()
        self.layoutGroupBoxOther.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxOther.setLayout(self.layoutGroupBoxOther)
        self.layoutOtherInfo = QtGui.QVBoxLayout()
        self.layoutOther = QtGui.QGridLayout()
        self.layoutGroupBoxOther.addLayout(self.layoutOtherInfo)
        self.layoutGroupBoxOther.addLayout(self.layoutOther)
        
        self.labelOtherInfo = QtGui.QLabel()
        self.labelOtherInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutOtherInfo.addWidget(self.labelOtherInfo)
        
        self.labelAOCProjectFile = QtGui.QLabel(parent)
        self.labelAOCProjectFile.setText('Abacus project file:')
        self.layoutOther.addWidget(self.labelAOCProjectFile, 0, 0)
        
        self.lineEditAOCProjectFile = QtGui.QLineEdit(parent)
        self.lineEditAOCProjectFile.setReadOnly(True)
        self.layoutOther.addWidget(self.lineEditAOCProjectFile, 0, 1)
        
        self.buttonSelectAOCProjectFile = QtGui.QPushButton(parent)
        self.buttonSelectAOCProjectFile.setText('&Browse')
        self.layoutOther.addWidget(self.buttonSelectAOCProjectFile, 0, 2)
        
        # Process tab button
        self.layoutButtonAbacusOpportunityCost = QtGui.QHBoxLayout()
        self.buttonProcessAbacusOpportunityCost = QtGui.QPushButton()
        self.buttonProcessAbacusOpportunityCost.setText('&Process')
        icon = QtGui.QIcon(':/ui/icons/iconActionHelp.png')
        self.buttonHelpTAAbacusOpportunityCost = QtGui.QPushButton()
        self.buttonHelpTAAbacusOpportunityCost.setIcon(icon)
        self.layoutButtonAbacusOpportunityCost.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonAbacusOpportunityCost.addWidget(self.buttonProcessAbacusOpportunityCost)
        self.layoutButtonAbacusOpportunityCost.addWidget(self.buttonHelpTAAbacusOpportunityCost)
        
        # Template GroupBox
        self.groupBoxAbacusOpportunityCostTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxAbacusOpportunityCostTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxAbacusOpportunityCostTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxAbacusOpportunityCostTemplate.setLayout(self.layoutGroupBoxAbacusOpportunityCostTemplate)
        self.layoutAbacusOpportunityCostTemplateInfo = QtGui.QVBoxLayout()
        self.layoutAbacusOpportunityCostTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxAbacusOpportunityCostTemplate.addLayout(self.layoutAbacusOpportunityCostTemplateInfo)
        self.layoutGroupBoxAbacusOpportunityCostTemplate.addLayout(self.layoutAbacusOpportunityCostTemplate)
        
        self.labelLoadedAbacusOpportunityCostTemplate = QtGui.QLabel()
        self.labelLoadedAbacusOpportunityCostTemplate.setText('Loaded template:')
        self.layoutAbacusOpportunityCostTemplate.addWidget(self.labelLoadedAbacusOpportunityCostTemplate, 0, 0)
        
        self.loadedAbacusOpportunityCostTemplate = QtGui.QLabel()
        self.loadedAbacusOpportunityCostTemplate.setText('<None>')
        self.layoutAbacusOpportunityCostTemplate.addWidget(self.loadedAbacusOpportunityCostTemplate, 0, 1)
        
        self.labelAbacusOpportunityCostTemplate = QtGui.QLabel()
        self.labelAbacusOpportunityCostTemplate.setText('Template name:')
        self.layoutAbacusOpportunityCostTemplate.addWidget(self.labelAbacusOpportunityCostTemplate, 1, 0)
        
        self.comboBoxAbacusOpportunityCostTemplate = QtGui.QComboBox()
        self.comboBoxAbacusOpportunityCostTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxAbacusOpportunityCostTemplate.setDisabled(True)
        self.comboBoxAbacusOpportunityCostTemplate.addItem('No template found')
        self.layoutAbacusOpportunityCostTemplate.addWidget(self.comboBoxAbacusOpportunityCostTemplate, 1, 1)
        
        self.layoutButtonAbacusOpportunityCostTemplate = QtGui.QHBoxLayout()
        self.layoutButtonAbacusOpportunityCostTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadAbacusOpportunityCostTemplate = QtGui.QPushButton()
        self.buttonLoadAbacusOpportunityCostTemplate.setDisabled(True)
        self.buttonLoadAbacusOpportunityCostTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadAbacusOpportunityCostTemplate.setText('Load')
        self.buttonSaveAbacusOpportunityCostTemplate = QtGui.QPushButton()
        self.buttonSaveAbacusOpportunityCostTemplate.setDisabled(True)
        self.buttonSaveAbacusOpportunityCostTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAbacusOpportunityCostTemplate.setText('Save')
        self.buttonSaveAsAbacusOpportunityCostTemplate = QtGui.QPushButton()
        self.buttonSaveAsAbacusOpportunityCostTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsAbacusOpportunityCostTemplate.setText('Save As')
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
        # Setup 'Opportunity cost curve' sub tab
        #***********************************************************
        # 'Parameters' GroupBox
        self.groupBoxOCCParameters = QtGui.QGroupBox('Parameters')
        self.layoutGroupBoxOCCParameters = QtGui.QVBoxLayout()
        self.layoutGroupBoxOCCParameters.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxOCCParameters.setLayout(self.layoutGroupBoxOCCParameters)
        self.layoutOCCParametersInfo = QtGui.QVBoxLayout()
        self.layoutOCCParameters = QtGui.QGridLayout()
        self.layoutGroupBoxOCCParameters.addLayout(self.layoutOCCParametersInfo)
        self.layoutGroupBoxOCCParameters.addLayout(self.layoutOCCParameters)
        
        self.labelOCCParametersInfo = QtGui.QLabel()
        self.labelOCCParametersInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutOCCParametersInfo.addWidget(self.labelOCCParametersInfo)
        
        self.labelOCCCsvNPVTable = QtGui.QLabel(parent)
        self.labelOCCCsvNPVTable.setText('Net Present Value (NPV) table:')
        self.layoutOCCParameters.addWidget(self.labelOCCCsvNPVTable, 0, 0)
        
        self.lineEditOCCCsvNPVTable = QtGui.QLineEdit(parent)
        self.lineEditOCCCsvNPVTable.setReadOnly(True)
        self.layoutOCCParameters.addWidget(self.lineEditOCCCsvNPVTable, 0, 1)
        
        self.buttonSelectOCCCsvNPVTable = QtGui.QPushButton()
        self.buttonSelectOCCCsvNPVTable.setText('&Browse')
        self.layoutOCCParameters.addWidget(self.buttonSelectOCCCsvNPVTable, 0, 2)
        
        self.labelOCCCostThreshold = QtGui.QLabel()
        self.labelOCCCostThreshold.setText('Cost &Threshold:')
        self.layoutOCCParameters.addWidget(self.labelOCCCostThreshold, 1, 0)
        
        self.spinBoxOCCCostThreshold = QtGui.QSpinBox()
        self.spinBoxOCCCostThreshold.setValue(5)
        self.layoutOCCParameters.addWidget(self.spinBoxOCCCostThreshold, 1, 1)
        self.labelOCCCostThreshold.setBuddy(self.spinBoxOCCCostThreshold)
        
        self.labelOCCOutputOpportunityCostDatabase = QtGui.QLabel()
        self.labelOCCOutputOpportunityCostDatabase.setText('[Output] Opportunity cost database:')
        self.layoutOCCParameters.addWidget(self.labelOCCOutputOpportunityCostDatabase, 2, 0)
        
        self.lineEditOCCOutputOpportunityCostDatabase = QtGui.QLineEdit()
        self.lineEditOCCOutputOpportunityCostDatabase.setReadOnly(True)
        self.layoutOCCParameters.addWidget(self.lineEditOCCOutputOpportunityCostDatabase, 2, 1)
        
        self.buttonSelectOCCOutputOpportunityCostDatabase = QtGui.QPushButton(parent)
        self.buttonSelectOCCOutputOpportunityCostDatabase.setText('&Browse')
        self.layoutOCCParameters.addWidget(self.buttonSelectOCCOutputOpportunityCostDatabase, 2, 2)
        
        self.labelOCCOutputOpportunityCostReport = QtGui.QLabel()
        self.labelOCCOutputOpportunityCostReport.setText('[Output] Opportunity cost report:')
        self.layoutOCCParameters.addWidget(self.labelOCCOutputOpportunityCostReport, 3, 0)
        
        self.lineEditOCCOutputOpportunityCostReport = QtGui.QLineEdit()
        self.lineEditOCCOutputOpportunityCostReport.setReadOnly(True)
        self.layoutOCCParameters.addWidget(self.lineEditOCCOutputOpportunityCostReport, 3, 1)
        
        self.buttonSelectOCCOutputOpportunityCostReport = QtGui.QPushButton(parent)
        self.buttonSelectOCCOutputOpportunityCostReport.setText('&Browse')
        self.layoutOCCParameters.addWidget(self.buttonSelectOCCOutputOpportunityCostReport, 3, 2)
        
        # Process tab button
        self.layoutButtonOpportunityCostCurve = QtGui.QHBoxLayout()
        self.buttonProcessOpportunityCostCurve = QtGui.QPushButton()
        self.buttonProcessOpportunityCostCurve.setText('&Process')
        self.buttonHelpTAOpportunityCostCurve = QtGui.QPushButton()
        self.buttonHelpTAOpportunityCostCurve.setIcon(icon)
        self.layoutButtonOpportunityCostCurve.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonOpportunityCostCurve.addWidget(self.buttonProcessOpportunityCostCurve)
        self.layoutButtonOpportunityCostCurve.addWidget(self.buttonHelpTAOpportunityCostCurve)
        
        # Template GroupBox
        self.groupBoxOpportunityCostCurveTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxOpportunityCostCurveTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxOpportunityCostCurveTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxOpportunityCostCurveTemplate.setLayout(self.layoutGroupBoxOpportunityCostCurveTemplate)
        self.layoutOpportunityCostCurveTemplateInfo = QtGui.QVBoxLayout()
        self.layoutOpportunityCostCurveTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxOpportunityCostCurveTemplate.addLayout(self.layoutOpportunityCostCurveTemplateInfo)
        self.layoutGroupBoxOpportunityCostCurveTemplate.addLayout(self.layoutOpportunityCostCurveTemplate)
        
        self.labelLoadedOpportunityCostCurveTemplate = QtGui.QLabel()
        self.labelLoadedOpportunityCostCurveTemplate.setText('Loaded template:')
        self.layoutOpportunityCostCurveTemplate.addWidget(self.labelLoadedOpportunityCostCurveTemplate, 0, 0)
        
        self.loadedOpportunityCostCurveTemplate = QtGui.QLabel()
        self.loadedOpportunityCostCurveTemplate.setText('<None>')
        self.layoutOpportunityCostCurveTemplate.addWidget(self.loadedOpportunityCostCurveTemplate, 0, 1)
        
        self.labelOpportunityCostCurveTemplate = QtGui.QLabel()
        self.labelOpportunityCostCurveTemplate.setText('Template name:')
        self.layoutOpportunityCostCurveTemplate.addWidget(self.labelOpportunityCostCurveTemplate, 1, 0)
        
        self.comboBoxOpportunityCostCurveTemplate = QtGui.QComboBox()
        self.comboBoxOpportunityCostCurveTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxOpportunityCostCurveTemplate.setDisabled(True)
        self.comboBoxOpportunityCostCurveTemplate.addItem('No template found')
        self.layoutOpportunityCostCurveTemplate.addWidget(self.comboBoxOpportunityCostCurveTemplate, 1, 1)
        
        self.layoutButtonOpportunityCostCurveTemplate = QtGui.QHBoxLayout()
        self.layoutButtonOpportunityCostCurveTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadOpportunityCostCurveTemplate = QtGui.QPushButton()
        self.buttonLoadOpportunityCostCurveTemplate.setDisabled(True)
        self.buttonLoadOpportunityCostCurveTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadOpportunityCostCurveTemplate.setText('Load')
        self.buttonSaveOpportunityCostCurveTemplate = QtGui.QPushButton()
        self.buttonSaveOpportunityCostCurveTemplate.setDisabled(True)
        self.buttonSaveOpportunityCostCurveTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveOpportunityCostCurveTemplate.setText('Save')
        self.buttonSaveAsOpportunityCostCurveTemplate = QtGui.QPushButton()
        self.buttonSaveAsOpportunityCostCurveTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsOpportunityCostCurveTemplate.setText('Save As')
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
        # Setup 'Opportunity cost map' sub tab
        #***********************************************************
        # 'Parameters' GroupBox
        self.groupBoxOCMParameters = QtGui.QGroupBox('Parameters')
        self.layoutGroupBoxOCMParameters = QtGui.QVBoxLayout()
        self.layoutGroupBoxOCMParameters.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxOCMParameters.setLayout(self.layoutGroupBoxOCMParameters)
        self.layoutOCMParametersInfo = QtGui.QVBoxLayout()
        self.layoutOCMParameters = QtGui.QGridLayout()
        self.layoutGroupBoxOCMParameters.addLayout(self.layoutOCMParametersInfo)
        self.layoutGroupBoxOCMParameters.addLayout(self.layoutOCMParameters)
        
        self.labelOCMParametersInfo = QtGui.QLabel()
        self.labelOCMParametersInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutOCMParametersInfo.addWidget(self.labelOCMParametersInfo)
        
        self.labelOCMCsvProfitability = QtGui.QLabel(parent)
        self.labelOCMCsvProfitability.setText('Profitability lookup table:')
        self.layoutOCMParameters.addWidget(self.labelOCMCsvProfitability, 0, 0)
        
        self.lineEditOCMCsvProfitability = QtGui.QLineEdit(parent)
        self.lineEditOCMCsvProfitability.setReadOnly(True)
        self.layoutOCMParameters.addWidget(self.lineEditOCMCsvProfitability, 0, 1)
        
        self.buttonSelectOCMCsvProfitability = QtGui.QPushButton()
        self.buttonSelectOCMCsvProfitability.setText('&Browse')
        self.layoutOCMParameters.addWidget(self.buttonSelectOCMCsvProfitability, 0, 2)
        
        # Process tab button
        self.layoutButtonOpportunityCostMap = QtGui.QHBoxLayout()
        self.buttonProcessOpportunityCostMap = QtGui.QPushButton()
        self.buttonProcessOpportunityCostMap.setText('&Process')
        self.buttonHelpTAOpportunityCostMap = QtGui.QPushButton()
        self.buttonHelpTAOpportunityCostMap.setIcon(icon)
        self.layoutButtonOpportunityCostMap.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonOpportunityCostMap.addWidget(self.buttonProcessOpportunityCostMap)
        self.layoutButtonOpportunityCostMap.addWidget(self.buttonHelpTAOpportunityCostMap)
        
        # Template GroupBox
        self.groupBoxOpportunityCostMapTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxOpportunityCostMapTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxOpportunityCostMapTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxOpportunityCostMapTemplate.setLayout(self.layoutGroupBoxOpportunityCostMapTemplate)
        self.layoutOpportunityCostMapTemplateInfo = QtGui.QVBoxLayout()
        self.layoutOpportunityCostMapTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxOpportunityCostMapTemplate.addLayout(self.layoutOpportunityCostMapTemplateInfo)
        self.layoutGroupBoxOpportunityCostMapTemplate.addLayout(self.layoutOpportunityCostMapTemplate)
        
        self.labelLoadedOpportunityCostMapTemplate = QtGui.QLabel()
        self.labelLoadedOpportunityCostMapTemplate.setText('Loaded template:')
        self.layoutOpportunityCostMapTemplate.addWidget(self.labelLoadedOpportunityCostMapTemplate, 0, 0)
        
        self.loadedOpportunityCostMapTemplate = QtGui.QLabel()
        self.loadedOpportunityCostMapTemplate.setText('<None>')
        self.layoutOpportunityCostMapTemplate.addWidget(self.loadedOpportunityCostMapTemplate, 0, 1)
        
        self.labelOpportunityCostMapTemplate = QtGui.QLabel()
        self.labelOpportunityCostMapTemplate.setText('Template name:')
        self.layoutOpportunityCostMapTemplate.addWidget(self.labelOpportunityCostMapTemplate, 1, 0)
        
        self.comboBoxOpportunityCostMapTemplate = QtGui.QComboBox()
        self.comboBoxOpportunityCostMapTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxOpportunityCostMapTemplate.setDisabled(True)
        self.comboBoxOpportunityCostMapTemplate.addItem('No template found')
        self.layoutOpportunityCostMapTemplate.addWidget(self.comboBoxOpportunityCostMapTemplate, 1, 1)
        
        self.layoutButtonOpportunityCostMapTemplate = QtGui.QHBoxLayout()
        self.layoutButtonOpportunityCostMapTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadOpportunityCostMapTemplate = QtGui.QPushButton()
        self.buttonLoadOpportunityCostMapTemplate.setDisabled(True)
        self.buttonLoadOpportunityCostMapTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadOpportunityCostMapTemplate.setText('Load')
        self.buttonSaveOpportunityCostMapTemplate = QtGui.QPushButton()
        self.buttonSaveOpportunityCostMapTemplate.setDisabled(True)
        self.buttonSaveOpportunityCostMapTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveOpportunityCostMapTemplate.setText('Save')
        self.buttonSaveAsOpportunityCostMapTemplate = QtGui.QPushButton()
        self.buttonSaveAsOpportunityCostMapTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsOpportunityCostMapTemplate.setText('Save As')
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
        # Setup 'Regional Economy' tab
        #***********************************************************
        self.tabWidgetRegionalEconomy = QtGui.QTabWidget()
        RegionalEconomyTabWidgetStylesheet = """
        QTabWidget QWidget {
            background-color: rgb(217, 229, 252);
            color: rgb(95, 98, 102);
        }
        QTabBar::tab {
            background-color: rgb(244, 248, 252);
            height: 35px;
            width: 200px;
        }
        QTabBar::tab:selected, QTabBar::tab:hover {
            background-color: rgb(217, 229, 252);
            font: bold;
        }
        """
        self.tabWidgetRegionalEconomy.setStyleSheet(RegionalEconomyTabWidgetStylesheet)

        self.tabInitRegionalEconomyParameterTable = QtGui.QWidget()
        self.tabInputOutputTable = QtGui.QWidget()
        self.tabDescriptiveAnalysis = QtGui.QWidget()
        self.tabRegionalEconomicScenarioImpact = QtGui.QWidget()
        self.tabLandRequirementAnalysis = QtGui.QWidget()
        self.tabLandUseChangeImpact = QtGui.QWidget()
        
        self.tabWidgetRegionalEconomy.addTab(self.tabInitRegionalEconomyParameterTable, 'Initialize')
        # self.tabWidgetRegionalEconomy.addTab(self.tabInputOutputTable, 'Input-Output Table')
        self.tabWidgetRegionalEconomy.addTab(self.tabDescriptiveAnalysis, 'Descriptive Analysis of Regional Economy')
        self.tabWidgetRegionalEconomy.addTab(self.tabRegionalEconomicScenarioImpact, 'Regional Economic Scenario Impact')
        self.tabWidgetRegionalEconomy.addTab(self.tabLandRequirementAnalysis, 'Land Requirement Analysis')
        self.tabWidgetRegionalEconomy.addTab(self.tabLandUseChangeImpact, 'Land Use Change Impact')
        
        self.layoutTabRegionalEconomy.addWidget(self.tabWidgetRegionalEconomy)
      
        self.layoutTabInitRegionalEconomyParameterTable = QtGui.QGridLayout()
        self.layoutTabInputOutputTable = QtGui.QGridLayout()
        self.layoutTabDescriptiveAnalysis = QtGui.QGridLayout()
        self.layoutTabRegionalEconomicScenarioImpact = QtGui.QGridLayout()
        self.layoutTabLandRequirementAnalysis = QtGui.QGridLayout()
        self.layoutTabLandUseChangeImpact = QtGui.QGridLayout()
      
        self.tabInitRegionalEconomyParameterTable.setLayout(self.layoutTabInitRegionalEconomyParameterTable)
        self.tabInputOutputTable.setLayout(self.layoutTabInputOutputTable)
        self.tabDescriptiveAnalysis.setLayout(self.layoutTabDescriptiveAnalysis)
        self.tabRegionalEconomicScenarioImpact.setLayout(self.layoutTabRegionalEconomicScenarioImpact)
        self.tabLandRequirementAnalysis.setLayout(self.layoutTabLandRequirementAnalysis)
        self.tabLandUseChangeImpact.setLayout(self.layoutTabLandUseChangeImpact)
        
        #***********************************************************
        # Setup 'Initialize' tab
        #***********************************************************
        self.groupBoxInitialInput = QtGui.QGroupBox('Initial input')
        self.layoutGroupBoxInitialInput = QtGui.QVBoxLayout()
        self.layoutGroupBoxInitialInput.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxInitialInput.setLayout(self.layoutGroupBoxInitialInput)
        
        self.layoutInitialInputInfo = QtGui.QGridLayout()
        self.layoutInitialInput = QtGui.QGridLayout()
        self.layoutGroupBoxInitialInput.addLayout(self.layoutInitialInputInfo)
        self.layoutGroupBoxInitialInput.addLayout(self.layoutInitialInput)
        
        self.labelInitialInputInfo = QtGui.QLabel()
        self.labelInitialInputInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutInitialInputInfo.addWidget(self.labelInitialInputInfo)
        
        self.labelInitialInputAreaName = QtGui.QLabel()
        self.labelInitialInputAreaName.setText('Area name:')
        self.layoutInitialInput.addWidget(self.labelInitialInputAreaName, 0, 0)
        
        self.lineEditInitialInputAreaName = QtGui.QLineEdit()
        self.lineEditInitialInputAreaName.setText('area')
        self.layoutInitialInput.addWidget(self.lineEditInitialInputAreaName, 0, 1)
        self.labelInitialInputAreaName.setBuddy(self.lineEditInitialInputAreaName)

        self.labelInitialInputPeriod = QtGui.QLabel()
        self.labelInitialInputPeriod.setText('&Period:')
        self.layoutInitialInput.addWidget(self.labelInitialInputPeriod, 1, 0)
        
        self.spinBoxInitialInputPeriod = QtGui.QSpinBox()
        self.spinBoxInitialInputPeriod.setRange(1, 9999)
        td = datetime.date.today()
        self.spinBoxInitialInputPeriod.setValue(td.year)
        self.layoutInitialInput.addWidget(self.spinBoxInitialInputPeriod, 1, 1)
        self.labelInitialInputPeriod.setBuddy(self.spinBoxInitialInputPeriod)
        
        self.labelInitialInputNumberOfSector = QtGui.QLabel()
        self.labelInitialInputNumberOfSector.setText('Number of sector:')
        self.layoutInitialInput.addWidget(self.labelInitialInputNumberOfSector, 2, 0)
        
        self.spinBoxInitialInputNumberOfSector = QtGui.QSpinBox()
        self.spinBoxInitialInputNumberOfSector.setRange(1, 99)
        self.spinBoxInitialInputNumberOfSector.setValue(10)
        self.layoutInitialInput.addWidget(self.spinBoxInitialInputNumberOfSector, 2, 1)
        self.labelInitialInputNumberOfSector.setBuddy(self.spinBoxInitialInputNumberOfSector)
        
        self.labelInitialInputFinancialUnit = QtGui.QLabel()
        self.labelInitialInputFinancialUnit.setText('Financial &unit:')
        self.layoutInitialInput.addWidget(self.labelInitialInputFinancialUnit, 3, 0)
        
        self.lineEditInitialInputFinancialUnit = QtGui.QLineEdit()
        self.lineEditInitialInputFinancialUnit.setText('Million Rupiah')
        self.layoutInitialInput.addWidget(self.lineEditInitialInputFinancialUnit, 3, 1)
        self.labelInitialInputFinancialUnit.setBuddy(self.lineEditInitialInputFinancialUnit)
        
        # Next tab button
        self.layoutButtonInitialize = QtGui.QHBoxLayout()
        self.buttonNextInitialize = QtGui.QPushButton()
        self.buttonNextInitialize.setText('&Next')
        self.layoutButtonInitialize.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonInitialize.addWidget(self.buttonNextInitialize)

        # Template GroupBox
        self.groupBoxInitializeTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxInitializeTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxInitializeTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxInitializeTemplate.setLayout(self.layoutGroupBoxInitializeTemplate)
        self.layoutInitializeTemplateInfo = QtGui.QVBoxLayout()
        self.layoutInitializeTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxInitializeTemplate.addLayout(self.layoutInitializeTemplateInfo)
        self.layoutGroupBoxInitializeTemplate.addLayout(self.layoutInitializeTemplate)
        
        self.labelLoadedInitializeTemplate = QtGui.QLabel()
        self.labelLoadedInitializeTemplate.setText('Loaded template:')
        self.layoutInitializeTemplate.addWidget(self.labelLoadedInitializeTemplate, 0, 0)
        
        self.loadedInitializeTemplate = QtGui.QLabel()
        self.loadedInitializeTemplate.setText('<None>')
        self.layoutInitializeTemplate.addWidget(self.loadedInitializeTemplate, 0, 1)
        
        self.labelInitializeTemplate = QtGui.QLabel()
        self.labelInitializeTemplate.setText('Template name:')
        self.layoutInitializeTemplate.addWidget(self.labelInitializeTemplate, 1, 0)
        
        self.comboBoxInitializeTemplate = QtGui.QComboBox()
        self.comboBoxInitializeTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxInitializeTemplate.setDisabled(True)
        self.comboBoxInitializeTemplate.addItem('No template found')
        self.layoutInitializeTemplate.addWidget(self.comboBoxInitializeTemplate, 1, 1)
        
        self.layoutButtonInitializeTemplate = QtGui.QHBoxLayout()
        self.layoutButtonInitializeTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadInitializeTemplate = QtGui.QPushButton()
        self.buttonLoadInitializeTemplate.setDisabled(True)
        self.buttonLoadInitializeTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadInitializeTemplate.setText('Load')
        self.buttonSaveInitializeTemplate = QtGui.QPushButton()
        self.buttonSaveInitializeTemplate.setDisabled(True)
        self.buttonSaveInitializeTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveInitializeTemplate.setText('Save')
        self.buttonSaveAsInitializeTemplate = QtGui.QPushButton()
        self.buttonSaveAsInitializeTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsInitializeTemplate.setText('Save As')
        self.layoutButtonInitializeTemplate.addWidget(self.buttonLoadInitializeTemplate)
        self.layoutButtonInitializeTemplate.addWidget(self.buttonSaveInitializeTemplate)
        self.layoutButtonInitializeTemplate.addWidget(self.buttonSaveAsInitializeTemplate)
        self.layoutGroupBoxInitializeTemplate.addLayout(self.layoutButtonInitializeTemplate)
        
        # Place the GroupBoxes
        self.layoutTabInitRegionalEconomyParameterTable.addWidget(self.groupBoxInitialInput, 0, 0)
        self.layoutTabInitRegionalEconomyParameterTable.addLayout(self.layoutButtonInitialize, 1, 0, 1, 2, QtCore.Qt.AlignRight)
        self.layoutTabInitRegionalEconomyParameterTable.addWidget(self.groupBoxInitializeTemplate, 0, 1, 1, 1)
        self.layoutTabInitRegionalEconomyParameterTable.setColumnStretch(0, 3)
        self.layoutTabInitRegionalEconomyParameterTable.setColumnStretch(1, 1)
        
        #***********************************************************
        # Setup 'Input-Output Table' tab
        #***********************************************************
        # 'Intermediate consumption matrix' GroupBox
        self.groupBoxIntermediateConsumptionMatrix = QtGui.QGroupBox('Intermediate consumption matrix')
        self.layoutGroupBoxIntermediateConsumptionMatrix = QtGui.QVBoxLayout()
        self.layoutGroupBoxIntermediateConsumptionMatrix.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxIntermediateConsumptionMatrix.setLayout(self.layoutGroupBoxIntermediateConsumptionMatrix)
        
        self.layoutIntermediateConsumptionMatrixInfo = QtGui.QVBoxLayout()
        self.labelIntermediateConsumptionMatrix = QtGui.QLabel()
        self.labelIntermediateConsumptionMatrix.setText('Lorem ipsum dolor sit amet...')
        self.layoutIntermediateConsumptionMatrixInfo.addWidget(self.labelIntermediateConsumptionMatrix)
        
        self.tableIntermediateConsumptionMatrix = QtGui.QTableWidget()
        self.tableIntermediateConsumptionMatrix.setDisabled(True)
        self.tableIntermediateConsumptionMatrix.verticalHeader().setVisible(False)
        
        self.layoutGroupBoxIntermediateConsumptionMatrix.addLayout(self.layoutIntermediateConsumptionMatrixInfo)
        self.layoutGroupBoxIntermediateConsumptionMatrix.addWidget(self.tableIntermediateConsumptionMatrix)

        # 'Final consumption matrix' GroupBox
        self.groupBoxFinalConsumptionMatrix = QtGui.QGroupBox('Final consumption matrix')
        self.layoutGroupBoxFinalConsumptionMatrix = QtGui.QGridLayout()
        self.layoutGroupBoxFinalConsumptionMatrix.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxFinalConsumptionMatrix.setLayout(self.layoutGroupBoxFinalConsumptionMatrix)
        
        self.layoutFinalConsumptionMatrixInfo = QtGui.QVBoxLayout()
        self.labelFinalConsumptionMatrix = QtGui.QLabel()
        self.labelFinalConsumptionMatrix.setText('Lorem ipsum dolor sit amet...')
        self.layoutFinalConsumptionMatrixInfo.addWidget(self.labelFinalConsumptionMatrix)
        
        self.tableFinalConsumptionMatrix = QtGui.QTableWidget()
        self.tableFinalConsumptionMatrix.setDisabled(True)
        self.tableFinalConsumptionMatrix.verticalHeader().setVisible(False)
        
        self.layoutButtonFinalConsumptionMatrix = QtGui.QVBoxLayout()
        icon = QtGui.QIcon(':/ui/icons/iconActionAdd.png')
        self.buttonAddFinalConsumptionMatrix = QtGui.QPushButton()
        self.buttonAddFinalConsumptionMatrix.setIcon(icon)
        self.buttonAddFinalConsumptionMatrix.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        icon = QtGui.QIcon(':/ui/icons/iconActionDelete.png')
        self.buttonRemoveFinalConsumptionMatrix = QtGui.QPushButton()
        self.buttonRemoveFinalConsumptionMatrix.setIcon(icon)
        self.buttonAddFinalConsumptionMatrix.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.layoutButtonFinalConsumptionMatrix.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.layoutButtonFinalConsumptionMatrix.addWidget(self.buttonAddFinalConsumptionMatrix)
        self.layoutButtonFinalConsumptionMatrix.addWidget(self.buttonRemoveFinalConsumptionMatrix)
        
        self.layoutGroupBoxFinalConsumptionMatrix.addLayout(self.layoutFinalConsumptionMatrixInfo, 0, 0, 1, 2, QtCore.Qt.AlignLeft)
        self.layoutGroupBoxFinalConsumptionMatrix.addWidget(self.tableFinalConsumptionMatrix, 1, 0)
        self.layoutGroupBoxFinalConsumptionMatrix.addLayout(self.layoutButtonFinalConsumptionMatrix, 1, 1, 2, 1, QtCore.Qt.AlignTop)

        # 'Added value matrix' GroupBox
        self.groupBoxAddedValueMatrix = QtGui.QGroupBox('Added value matrix')
        self.layoutGroupBoxAddedValueMatrix = QtGui.QVBoxLayout()
        self.layoutGroupBoxAddedValueMatrix.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxAddedValueMatrix.setLayout(self.layoutGroupBoxAddedValueMatrix)
        
        self.layoutAddedValueMatrixInfo = QtGui.QVBoxLayout()
        self.labelAddedValueMatrix = QtGui.QLabel()
        self.labelAddedValueMatrix.setText('Lorem ipsum dolor sit amet...')
        self.layoutAddedValueMatrixInfo.addWidget(self.labelAddedValueMatrix)
        
        self.tableAddedValueMatrix = QtGui.QTableWidget()
        self.tableAddedValueMatrix.setDisabled(True)
        self.tableAddedValueMatrix.verticalHeader().setVisible(False)

        self.layoutButtonAddedValueMatrix = QtGui.QHBoxLayout()
        icon = QtGui.QIcon(':/ui/icons/iconActionAdd.png')
        self.buttonAddAddedValueMatrix = QtGui.QPushButton()
        self.buttonAddAddedValueMatrix.setIcon(icon)
        self.buttonAddAddedValueMatrix.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        icon = QtGui.QIcon(':/ui/icons/iconActionDelete.png')
        self.buttonRemoveAddedValueMatrix = QtGui.QPushButton()
        self.buttonRemoveAddedValueMatrix.setIcon(icon)
        self.buttonRemoveAddedValueMatrix.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.layoutButtonAddedValueMatrix.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.layoutButtonAddedValueMatrix.addWidget(self.buttonAddAddedValueMatrix)
        self.layoutButtonAddedValueMatrix.addWidget(self.buttonRemoveAddedValueMatrix)
        
        self.layoutGroupBoxAddedValueMatrix.addLayout(self.layoutAddedValueMatrixInfo)
        self.layoutGroupBoxAddedValueMatrix.addWidget(self.tableAddedValueMatrix)
        self.layoutGroupBoxAddedValueMatrix.addLayout(self.layoutButtonAddedValueMatrix)

        # 'Labour matrix' GroupBox
        self.groupBoxLabourMatrix = QtGui.QGroupBox('Labour matrix')
        self.layoutGroupBoxLabourMatrix = QtGui.QVBoxLayout()
        self.layoutGroupBoxLabourMatrix.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLabourMatrix.setLayout(self.layoutGroupBoxLabourMatrix)
        
        self.layoutLabourMatrixInfo = QtGui.QVBoxLayout()
        self.labelLabourMatrix = QtGui.QLabel()
        self.labelLabourMatrix.setText('Lorem ipsum dolor sit amet...')
        self.layoutLabourMatrixInfo.addWidget(self.labelLabourMatrix)
        
        self.tableLabourMatrix = QtGui.QTableWidget()
        self.tableLabourMatrix.setDisabled(True)
        self.tableLabourMatrix.verticalHeader().setVisible(False)
        
        self.layoutGroupBoxLabourMatrix.addLayout(self.layoutLabourMatrixInfo)
        self.layoutGroupBoxLabourMatrix.addWidget(self.tableLabourMatrix)
        
        # Next tab button
        self.layoutButtonInputOutputTable = QtGui.QHBoxLayout()
        self.buttonNextInputOutputTable = QtGui.QPushButton()
        self.buttonNextInputOutputTable.setText('&Next')
        self.layoutButtonInputOutputTable.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonInputOutputTable.addWidget(self.buttonNextInputOutputTable)
        
        # Place the GroupBoxes
        self.layoutTabInputOutputTable.addWidget(self.groupBoxIntermediateConsumptionMatrix, 0, 0)
        self.layoutTabInputOutputTable.addWidget(self.groupBoxFinalConsumptionMatrix, 0, 1)
        self.layoutTabInputOutputTable.addWidget(self.groupBoxAddedValueMatrix, 1, 0)
        self.layoutTabInputOutputTable.addWidget(self.groupBoxLabourMatrix, 1, 1)
        self.layoutTabInputOutputTable.addLayout(self.layoutButtonInputOutputTable, 2, 0, 1, 2, QtCore.Qt.AlignRight)
        self.layoutTabInputOutputTable.setColumnStretch(0, 3)
        self.layoutTabInputOutputTable.setColumnStretch(1, 1)
        self.layoutTabInputOutputTable.setRowStretch(0, 3)
        self.layoutTabInputOutputTable.setRowStretch(1, 2)
        
        #***********************************************************
        # Setup 'Descriptive Analysis of Regional Economy' tab
        #***********************************************************
        # Use QScrollArea
        ##self.layoutContentDescriptiveAnalysis = QtGui.QVBoxLayout()
        self.layoutContentDescriptiveAnalysis = QtGui.QGridLayout()
        self.contentDescriptiveAnalysis = QtGui.QWidget()
        self.contentDescriptiveAnalysis.setLayout(self.layoutContentDescriptiveAnalysis)
        self.scrollDescriptiveAnalysis = QtGui.QScrollArea()
        self.scrollDescriptiveAnalysis.setWidgetResizable(True);
        self.scrollDescriptiveAnalysis.setWidget(self.contentDescriptiveAnalysis)
        self.layoutTabDescriptiveAnalysis.addWidget(self.scrollDescriptiveAnalysis)
        
        # 'Single period' GroupBox
        self.groupBoxSinglePeriod = QtGui.QGroupBox('Single period')
        self.layoutGroupBoxSinglePeriod = QtGui.QVBoxLayout()
        self.layoutGroupBoxSinglePeriod.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxSinglePeriod.setLayout(self.layoutGroupBoxSinglePeriod)
        self.layoutSinglePeriodInfo = QtGui.QVBoxLayout()
        self.layoutSinglePeriod = QtGui.QGridLayout()
        self.layoutGroupBoxSinglePeriod.addLayout(self.layoutSinglePeriodInfo)
        self.layoutGroupBoxSinglePeriod.addLayout(self.layoutSinglePeriod)
        
        self.labelSinglePeriodInfo = QtGui.QLabel()
        self.labelSinglePeriodInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutSinglePeriodInfo.addWidget(self.labelSinglePeriodInfo)
        
        self.labelSinglePeriod = QtGui.QLabel()
        self.labelSinglePeriod.setText('&Period T1:')
        self.layoutSinglePeriod.addWidget(self.labelSinglePeriod, 0, 0)
        
        self.spinBoxSinglePeriod = QtGui.QSpinBox()
        self.spinBoxSinglePeriod.setRange(1, 9999)
        td = datetime.date.today()
        self.spinBoxSinglePeriod.setValue(td.year)
        self.layoutSinglePeriod.addWidget(self.spinBoxSinglePeriod, 0, 1)
        self.labelSinglePeriod.setBuddy(self.spinBoxSinglePeriod)
        
        self.labelSingleIntermediateConsumptionMatrix = QtGui.QLabel()
        self.labelSingleIntermediateConsumptionMatrix.setText('Intermediate consumption matrix:')
        self.layoutSinglePeriod.addWidget(self.labelSingleIntermediateConsumptionMatrix, 1, 0)
        
        self.lineEditSingleIntermediateConsumptionMatrix = QtGui.QLineEdit()
        self.lineEditSingleIntermediateConsumptionMatrix.setReadOnly(True)
        self.layoutSinglePeriod.addWidget(self.lineEditSingleIntermediateConsumptionMatrix, 1, 1)
        
        self.buttonSelectSingleIntermediateConsumptionMatrix = QtGui.QPushButton()
        self.buttonSelectSingleIntermediateConsumptionMatrix.setText('&Browse')
        self.layoutSinglePeriod.addWidget(self.buttonSelectSingleIntermediateConsumptionMatrix, 1, 2)
        
        self.labelSingleValueAddedMatrix = QtGui.QLabel()
        self.labelSingleValueAddedMatrix.setText('Value added matrix:')
        self.layoutSinglePeriod.addWidget(self.labelSingleValueAddedMatrix, 2, 0)
        
        self.lineEditSingleValueAddedMatrix = QtGui.QLineEdit()
        self.lineEditSingleValueAddedMatrix.setReadOnly(True)
        self.layoutSinglePeriod.addWidget(self.lineEditSingleValueAddedMatrix, 2, 1)
        
        self.buttonSelectSingleValueAddedMatrix = QtGui.QPushButton()
        self.buttonSelectSingleValueAddedMatrix.setText('&Browse')
        self.layoutSinglePeriod.addWidget(self.buttonSelectSingleValueAddedMatrix, 2, 2)
        
        self.labelSingleFinalConsumptionMatrix = QtGui.QLabel()
        self.labelSingleFinalConsumptionMatrix.setText('Final consumption matrix:')
        self.layoutSinglePeriod.addWidget(self.labelSingleFinalConsumptionMatrix, 3, 0)
        
        self.lineEditSingleFinalConsumptionMatrix = QtGui.QLineEdit()
        self.lineEditSingleFinalConsumptionMatrix.setReadOnly(True)
        self.layoutSinglePeriod.addWidget(self.lineEditSingleFinalConsumptionMatrix, 3, 1)
        
        self.buttonSelectSingleFinalConsumptionMatrix = QtGui.QPushButton()
        self.buttonSelectSingleFinalConsumptionMatrix.setText('&Browse')
        self.layoutSinglePeriod.addWidget(self.buttonSelectSingleFinalConsumptionMatrix, 3, 2)
        
        self.labelSingleLabourRequirement = QtGui.QLabel()
        self.labelSingleLabourRequirement.setText('Labour requirement:')
        self.layoutSinglePeriod.addWidget(self.labelSingleLabourRequirement, 4, 0)
        
        self.lineEditSingleLabourRequirement = QtGui.QLineEdit()
        self.lineEditSingleLabourRequirement.setReadOnly(True)
        self.layoutSinglePeriod.addWidget(self.lineEditSingleLabourRequirement, 4, 1)
        
        self.buttonSelectSingleLabourRequirement = QtGui.QPushButton()
        self.buttonSelectSingleLabourRequirement.setText('&Browse')
        self.layoutSinglePeriod.addWidget(self.buttonSelectSingleLabourRequirement, 4, 2)
        
        # 'Multiple period' GroupBox
        self.groupBoxMultiplePeriod = QtGui.QGroupBox('Multiple period')
        self.layoutGroupBoxMultiplePeriod = QtGui.QHBoxLayout()
        self.groupBoxMultiplePeriod.setLayout(self.layoutGroupBoxMultiplePeriod)
        self.layoutOptionsMultiplePeriod = QtGui.QVBoxLayout()
        self.layoutOptionsMultiplePeriod.setContentsMargins(5, 0, 5, 0)
        self.contentOptionsMultiplePeriod = QtGui.QWidget()
        self.contentOptionsMultiplePeriod.setLayout(self.layoutOptionsMultiplePeriod)
        self.layoutOptionsMultiplePeriod.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.checkBoxMultiplePeriod = QtGui.QCheckBox()
        self.checkBoxMultiplePeriod.setChecked(False)
        self.contentOptionsMultiplePeriod.setDisabled(True)
        self.layoutGroupBoxMultiplePeriod.addWidget(self.checkBoxMultiplePeriod)
        self.layoutGroupBoxMultiplePeriod.addWidget(self.contentOptionsMultiplePeriod)
        #self.layoutGroupBoxMultiplePeriod.insertStretch(2, 1)
        self.layoutGroupBoxMultiplePeriod.setAlignment(self.checkBoxMultiplePeriod, QtCore.Qt.AlignTop)
        self.layoutMultiplePeriodInfo = QtGui.QVBoxLayout()
        self.layoutMultiplePeriod = QtGui.QGridLayout()
        self.layoutOptionsMultiplePeriod.addLayout(self.layoutMultiplePeriodInfo)
        self.layoutOptionsMultiplePeriod.addLayout(self.layoutMultiplePeriod)
        
        self.labelMultiplePeriodInfo = QtGui.QLabel()
        self.labelMultiplePeriodInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutMultiplePeriodInfo.addWidget(self.labelMultiplePeriodInfo)
        
        self.labelMultiplePeriod = QtGui.QLabel()
        self.labelMultiplePeriod.setText('&Period T2:')
        self.layoutMultiplePeriod.addWidget(self.labelMultiplePeriod, 0, 0)
        
        self.spinBoxMultiplePeriod = QtGui.QSpinBox()
        self.spinBoxMultiplePeriod.setRange(1, 9999)
        self.spinBoxMultiplePeriod.setValue(td.year)
        self.layoutMultiplePeriod.addWidget(self.spinBoxMultiplePeriod, 0, 1)
        self.labelMultiplePeriod.setBuddy(self.spinBoxMultiplePeriod)
        
        self.labelMultipleIntermediateConsumptionMatrix = QtGui.QLabel()
        self.labelMultipleIntermediateConsumptionMatrix.setText('Intermediate consumption matrix:')
        self.layoutMultiplePeriod.addWidget(self.labelMultipleIntermediateConsumptionMatrix, 1, 0)
        
        self.lineEditMultipleIntermediateConsumptionMatrix = QtGui.QLineEdit()
        self.lineEditMultipleIntermediateConsumptionMatrix.setReadOnly(True)
        self.layoutMultiplePeriod.addWidget(self.lineEditMultipleIntermediateConsumptionMatrix, 1, 1)
        
        self.buttonSelectMultipleIntermediateConsumptionMatrix = QtGui.QPushButton()
        self.buttonSelectMultipleIntermediateConsumptionMatrix.setText('&Browse')
        self.layoutMultiplePeriod.addWidget(self.buttonSelectMultipleIntermediateConsumptionMatrix, 1, 2)
        
        self.labelMultipleValueAddedMatrix = QtGui.QLabel()
        self.labelMultipleValueAddedMatrix.setText('Value added matrix:')
        self.layoutMultiplePeriod.addWidget(self.labelMultipleValueAddedMatrix, 2, 0)
        
        self.lineEditMultipleValueAddedMatrix = QtGui.QLineEdit()
        self.lineEditMultipleValueAddedMatrix.setReadOnly(True)
        self.layoutMultiplePeriod.addWidget(self.lineEditMultipleValueAddedMatrix, 2, 1)
        
        self.buttonSelectMultipleValueAddedMatrix = QtGui.QPushButton()
        self.buttonSelectMultipleValueAddedMatrix.setText('&Browse')
        self.layoutMultiplePeriod.addWidget(self.buttonSelectMultipleValueAddedMatrix, 2, 2)
        
        self.labelMultipleFinalConsumptionMatrix = QtGui.QLabel()
        self.labelMultipleFinalConsumptionMatrix.setText('Final consumption matrix:')
        self.layoutMultiplePeriod.addWidget(self.labelMultipleFinalConsumptionMatrix, 3, 0)
        
        self.lineEditMultipleFinalConsumptionMatrix = QtGui.QLineEdit()
        self.lineEditMultipleFinalConsumptionMatrix.setReadOnly(True)
        self.layoutMultiplePeriod.addWidget(self.lineEditMultipleFinalConsumptionMatrix, 3, 1)
        
        self.buttonSelectMultipleFinalConsumptionMatrix = QtGui.QPushButton()
        self.buttonSelectMultipleFinalConsumptionMatrix.setText('&Browse')
        self.layoutMultiplePeriod.addWidget(self.buttonSelectMultipleFinalConsumptionMatrix, 3, 2)
        
        self.labelMultipleLabourRequirement = QtGui.QLabel()
        self.labelMultipleLabourRequirement.setText('Labour requirement:')
        self.layoutMultiplePeriod.addWidget(self.labelMultipleLabourRequirement, 4, 0)
        
        self.lineEditMultipleLabourRequirement = QtGui.QLineEdit()
        self.lineEditMultipleLabourRequirement.setReadOnly(True)
        self.layoutMultiplePeriod.addWidget(self.lineEditMultipleLabourRequirement, 4, 1)
        
        self.buttonSelectMultipleLabourRequirement = QtGui.QPushButton()
        self.buttonSelectMultipleLabourRequirement.setText('&Browse')
        self.layoutMultiplePeriod.addWidget(self.buttonSelectMultipleLabourRequirement, 4, 2)
        
        # 'Other' GroupBox
        self.groupBoxOther = QtGui.QGroupBox('Other parameters')
        self.layoutGroupBoxOther = QtGui.QVBoxLayout()
        self.layoutGroupBoxOther.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxOther.setLayout(self.layoutGroupBoxOther)
        self.layoutOtherInfo = QtGui.QVBoxLayout()
        self.layoutOther = QtGui.QGridLayout()
        self.layoutGroupBoxOther.addLayout(self.layoutOtherInfo)
        self.layoutGroupBoxOther.addLayout(self.layoutOther)
        
        self.labelOtherInfo = QtGui.QLabel()
        self.labelOtherInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutOtherInfo.addWidget(self.labelOtherInfo)
        
        self.labelOtherValueAddedComponent = QtGui.QLabel()
        self.labelOtherValueAddedComponent.setText('Value added component:')
        self.layoutOther.addWidget(self.labelOtherValueAddedComponent, 0, 0)
        
        self.lineEditOtherValueAddedComponent = QtGui.QLineEdit()
        self.lineEditOtherValueAddedComponent.setReadOnly(True)
        self.layoutOther.addWidget(self.lineEditOtherValueAddedComponent, 0, 1)
        
        self.buttonSelectOtherValueAddedComponent = QtGui.QPushButton()
        self.buttonSelectOtherValueAddedComponent.setText('&Browse')
        self.layoutOther.addWidget(self.buttonSelectOtherValueAddedComponent, 0, 2)
        
        self.labelOtherFinalConsumptionComponent = QtGui.QLabel()
        self.labelOtherFinalConsumptionComponent.setText('Final consumption component:')
        self.layoutOther.addWidget(self.labelOtherFinalConsumptionComponent, 1, 0)
        
        self.lineEditOtherFinalConsumptionComponent = QtGui.QLineEdit()
        self.lineEditOtherFinalConsumptionComponent.setReadOnly(True)
        self.layoutOther.addWidget(self.lineEditOtherFinalConsumptionComponent, 1, 1)
        
        self.buttonSelectOtherFinalConsumptionComponent = QtGui.QPushButton()
        self.buttonSelectOtherFinalConsumptionComponent.setText('&Browse')
        self.layoutOther.addWidget(self.buttonSelectOtherFinalConsumptionComponent, 1, 2)
        
        self.labelOtherListOfEconomicSector = QtGui.QLabel()
        self.labelOtherListOfEconomicSector.setText('List of economic sector:')
        self.layoutOther.addWidget(self.labelOtherListOfEconomicSector, 2, 0)
        
        self.lineEditOtherListOfEconomicSector = QtGui.QLineEdit()
        self.lineEditOtherListOfEconomicSector.setReadOnly(True)
        self.layoutOther.addWidget(self.lineEditOtherListOfEconomicSector, 2, 1)
        
        self.buttonSelectOtherListOfEconomicSector = QtGui.QPushButton()
        self.buttonSelectOtherListOfEconomicSector.setText('&Browse')
        self.layoutOther.addWidget(self.buttonSelectOtherListOfEconomicSector, 2, 2)
        
        self.labelOtherFinancialUnit = QtGui.QLabel()
        self.labelOtherFinancialUnit.setText('Financial &unit:')
        self.layoutOther.addWidget(self.labelOtherFinancialUnit, 3, 0)
        
        self.lineEditOtherFinancialUnit = QtGui.QLineEdit()
        self.lineEditOtherFinancialUnit.setText('Million Rupiah')
        self.layoutOther.addWidget(self.lineEditOtherFinancialUnit, 3, 1)
        self.labelOtherFinancialUnit.setBuddy(self.lineEditOtherFinancialUnit)
        
        self.labelOtherAreaName = QtGui.QLabel()
        self.labelOtherAreaName.setText('&Area name:')
        self.layoutOther.addWidget(self.labelOtherAreaName, 4, 0)
        
        self.lineEditOtherAreaName = QtGui.QLineEdit()
        self.lineEditOtherAreaName.setText('area')
        self.layoutOther.addWidget(self.lineEditOtherAreaName, 4, 1)
        self.labelOtherAreaName.setBuddy(self.lineEditOtherAreaName)
        
        # Process tab button
        self.layoutButtonDescriptiveAnalysis = QtGui.QHBoxLayout()
        self.buttonProcessDescriptiveAnalysis = QtGui.QPushButton()
        self.buttonProcessDescriptiveAnalysis.setText('&Process')
        icon = QtGui.QIcon(':/ui/icons/iconActionHelp.png')
        self.buttonHelpTADescriptiveAnalysis = QtGui.QPushButton()
        self.buttonHelpTADescriptiveAnalysis.setIcon(icon)
        self.layoutButtonDescriptiveAnalysis.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonDescriptiveAnalysis.addWidget(self.buttonProcessDescriptiveAnalysis)
        self.layoutButtonDescriptiveAnalysis.addWidget(self.buttonHelpTADescriptiveAnalysis)
        
        # Template GroupBox
        self.groupBoxDescriptiveAnalysisTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxDescriptiveAnalysisTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxDescriptiveAnalysisTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxDescriptiveAnalysisTemplate.setLayout(self.layoutGroupBoxDescriptiveAnalysisTemplate)
        self.layoutDescriptiveAnalysisTemplateInfo = QtGui.QVBoxLayout()
        self.layoutDescriptiveAnalysisTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxDescriptiveAnalysisTemplate.addLayout(self.layoutDescriptiveAnalysisTemplateInfo)
        self.layoutGroupBoxDescriptiveAnalysisTemplate.addLayout(self.layoutDescriptiveAnalysisTemplate)
        
        self.labelLoadedDescriptiveAnalysisTemplate = QtGui.QLabel()
        self.labelLoadedDescriptiveAnalysisTemplate.setText('Loaded template:')
        self.layoutDescriptiveAnalysisTemplate.addWidget(self.labelLoadedDescriptiveAnalysisTemplate, 0, 0)
        
        self.loadedDescriptiveAnalysisTemplate = QtGui.QLabel()
        self.loadedDescriptiveAnalysisTemplate.setText('<None>')
        self.layoutDescriptiveAnalysisTemplate.addWidget(self.loadedDescriptiveAnalysisTemplate, 0, 1)
        
        self.labelDescriptiveAnalysisTemplate = QtGui.QLabel()
        self.labelDescriptiveAnalysisTemplate.setText('Template name:')
        self.layoutDescriptiveAnalysisTemplate.addWidget(self.labelDescriptiveAnalysisTemplate, 1, 0)
        
        self.comboBoxDescriptiveAnalysisTemplate = QtGui.QComboBox()
        self.comboBoxDescriptiveAnalysisTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxDescriptiveAnalysisTemplate.setDisabled(True)
        self.comboBoxDescriptiveAnalysisTemplate.addItem('No template found')
        self.layoutDescriptiveAnalysisTemplate.addWidget(self.comboBoxDescriptiveAnalysisTemplate, 1, 1)
        
        self.layoutButtonDescriptiveAnalysisTemplate = QtGui.QHBoxLayout()
        self.layoutButtonDescriptiveAnalysisTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadDescriptiveAnalysisTemplate = QtGui.QPushButton()
        self.buttonLoadDescriptiveAnalysisTemplate.setDisabled(True)
        self.buttonLoadDescriptiveAnalysisTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadDescriptiveAnalysisTemplate.setText('Load')
        self.buttonSaveDescriptiveAnalysisTemplate = QtGui.QPushButton()
        self.buttonSaveDescriptiveAnalysisTemplate.setDisabled(True)
        self.buttonSaveDescriptiveAnalysisTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveDescriptiveAnalysisTemplate.setText('Save')
        self.buttonSaveAsDescriptiveAnalysisTemplate = QtGui.QPushButton()
        self.buttonSaveAsDescriptiveAnalysisTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsDescriptiveAnalysisTemplate.setText('Save As')
        self.layoutButtonDescriptiveAnalysisTemplate.addWidget(self.buttonLoadDescriptiveAnalysisTemplate)
        self.layoutButtonDescriptiveAnalysisTemplate.addWidget(self.buttonSaveDescriptiveAnalysisTemplate)
        self.layoutButtonDescriptiveAnalysisTemplate.addWidget(self.buttonSaveAsDescriptiveAnalysisTemplate)
        self.layoutGroupBoxDescriptiveAnalysisTemplate.addLayout(self.layoutButtonDescriptiveAnalysisTemplate)
        
        # Place the GroupBoxes
        self.layoutContentDescriptiveAnalysis.addWidget(self.groupBoxSinglePeriod, 0, 0)
        self.layoutContentDescriptiveAnalysis.addWidget(self.groupBoxMultiplePeriod, 1, 0)
        self.layoutContentDescriptiveAnalysis.addWidget(self.groupBoxOther, 2, 0)
        self.layoutContentDescriptiveAnalysis.addLayout(self.layoutButtonDescriptiveAnalysis, 3, 0, 1, 2, QtCore.Qt.AlignRight)
        self.layoutContentDescriptiveAnalysis.addWidget(self.groupBoxDescriptiveAnalysisTemplate, 0, 1, 3, 1)
        self.layoutContentDescriptiveAnalysis.setColumnStretch(0, 3)
        self.layoutContentDescriptiveAnalysis.setColumnStretch(1, 1) # Smaller template column
        
        #***********************************************************
        # Setup 'Regional Economic Scenario Impact' tab
        #***********************************************************
        # Use QScrollArea
        ##self.layoutContentRegionalEconomicScenarioImpact = QtGui.QVBoxLayout()
        self.layoutContentRegionalEconomicScenarioImpact = QtGui.QGridLayout()
        self.contentRegionalEconomicScenarioImpact = QtGui.QWidget()
        self.contentRegionalEconomicScenarioImpact.setLayout(self.layoutContentRegionalEconomicScenarioImpact)
        self.scrollRegionalEconomicScenarioImpact = QtGui.QScrollArea()
        self.scrollRegionalEconomicScenarioImpact.setWidgetResizable(True);
        self.scrollRegionalEconomicScenarioImpact.setWidget(self.contentRegionalEconomicScenarioImpact)
        self.layoutTabRegionalEconomicScenarioImpact.addWidget(self.scrollRegionalEconomicScenarioImpact)
        
        # 'Type' GroupBox
        self.groupBoxRegionalEconomicScenarioImpactType = QtGui.QGroupBox('Scenario type')
        self.layoutGroupBoxRegionalEconomicScenarioImpactType = QtGui.QVBoxLayout()
        self.layoutGroupBoxRegionalEconomicScenarioImpactType.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxRegionalEconomicScenarioImpactType.setLayout(self.layoutGroupBoxRegionalEconomicScenarioImpactType)
        self.layoutRegionalEconomicScenarioImpactTypeInfo = QtGui.QVBoxLayout()
        self.layoutRegionalEconomicScenarioImpactType = QtGui.QGridLayout()
        self.layoutGroupBoxRegionalEconomicScenarioImpactType.addLayout(self.layoutRegionalEconomicScenarioImpactTypeInfo)
        self.layoutGroupBoxRegionalEconomicScenarioImpactType.addLayout(self.layoutRegionalEconomicScenarioImpactType)
        
        self.labelRegionalEconomicScenarioImpactTypeInfo = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactTypeInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutRegionalEconomicScenarioImpactTypeInfo.addWidget(self.labelRegionalEconomicScenarioImpactTypeInfo)
        
        self.checkBoxRegionalEconomicScenarioImpactFinalDemand = QtGui.QCheckBox('Final Demand Scenario')
        self.checkBoxRegionalEconomicScenarioImpactFinalDemand.setChecked(True)
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.checkBoxRegionalEconomicScenarioImpactFinalDemand, 0, 0)
        
        self.labelRegionalEconomicScenarioImpactFinalDemandChangeScenario = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactFinalDemandChangeScenario.setText('Final demand change scenario:')
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.labelRegionalEconomicScenarioImpactFinalDemandChangeScenario, 1, 0)
        
        self.lineEditRegionalEconomicScenarioImpactFinalDemandChangeScenario = QtGui.QLineEdit()
        self.lineEditRegionalEconomicScenarioImpactFinalDemandChangeScenario.setReadOnly(True)
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.lineEditRegionalEconomicScenarioImpactFinalDemandChangeScenario, 1, 1)
        
        self.buttonSelectRegionalEconomicScenarioImpactFinalDemandChangeScenario = QtGui.QPushButton()
        self.buttonSelectRegionalEconomicScenarioImpactFinalDemandChangeScenario.setText('&Browse')
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.buttonSelectRegionalEconomicScenarioImpactFinalDemandChangeScenario, 1, 2)
        
        self.checkBoxRegionalEconomicScenarioImpactGDP = QtGui.QCheckBox('GDP Scenario')
        self.checkBoxRegionalEconomicScenarioImpactGDP.setChecked(False)
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.checkBoxRegionalEconomicScenarioImpactGDP, 2, 0)
        
        self.labelRegionalEconomicScenarioImpactGDPChangeScenario = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactGDPChangeScenario.setText('GDP change scenario:')
        self.labelRegionalEconomicScenarioImpactGDPChangeScenario.setDisabled(True)
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.labelRegionalEconomicScenarioImpactGDPChangeScenario, 3, 0)
        
        self.lineEditRegionalEconomicScenarioImpactGDPChangeScenario = QtGui.QLineEdit()
        self.lineEditRegionalEconomicScenarioImpactGDPChangeScenario.setReadOnly(True)
        self.lineEditRegionalEconomicScenarioImpactGDPChangeScenario.setDisabled(True)
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.lineEditRegionalEconomicScenarioImpactGDPChangeScenario, 3, 1)
        
        self.buttonSelectRegionalEconomicScenarioImpactGDPChangeScenario = QtGui.QPushButton()
        self.buttonSelectRegionalEconomicScenarioImpactGDPChangeScenario.setText('&Browse')
        self.buttonSelectRegionalEconomicScenarioImpactGDPChangeScenario.setDisabled(True)
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.buttonSelectRegionalEconomicScenarioImpactGDPChangeScenario, 3, 2)
        
        # 'Parameters' GroupBox
        self.groupBoxRegionalEconomicScenarioImpactParameters = QtGui.QGroupBox('Parameters')
        self.layoutGroupBoxRegionalEconomicScenarioImpactParameters = QtGui.QVBoxLayout()
        self.layoutGroupBoxRegionalEconomicScenarioImpactParameters.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxRegionalEconomicScenarioImpactParameters.setLayout(self.layoutGroupBoxRegionalEconomicScenarioImpactParameters)
        self.layoutRegionalEconomicScenarioImpactParametersInfo = QtGui.QVBoxLayout()
        self.layoutRegionalEconomicScenarioImpactParameters = QtGui.QGridLayout()
        self.layoutGroupBoxRegionalEconomicScenarioImpactParameters.addLayout(self.layoutRegionalEconomicScenarioImpactParametersInfo)
        self.layoutGroupBoxRegionalEconomicScenarioImpactParameters.addLayout(self.layoutRegionalEconomicScenarioImpactParameters)
        
        self.labelRegionalEconomicScenarioImpactParametersInfo = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactParametersInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutRegionalEconomicScenarioImpactParametersInfo.addWidget(self.labelRegionalEconomicScenarioImpactParametersInfo)
        
        self.labelRegionalEconomicScenarioImpactIntermediateConsumptionMatrix = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactIntermediateConsumptionMatrix.setText('Intermediate consumption matrix:')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.labelRegionalEconomicScenarioImpactIntermediateConsumptionMatrix, 0, 0)
        
        self.lineEditRegionalEconomicScenarioImpactIntermediateConsumptionMatrix = QtGui.QLineEdit()
        self.lineEditRegionalEconomicScenarioImpactIntermediateConsumptionMatrix.setReadOnly(True)
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.lineEditRegionalEconomicScenarioImpactIntermediateConsumptionMatrix, 0, 1)
        
        self.buttonSelectRegionalEconomicScenarioImpactIntermediateConsumptionMatrix = QtGui.QPushButton()
        self.buttonSelectRegionalEconomicScenarioImpactIntermediateConsumptionMatrix.setText('&Browse')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.buttonSelectRegionalEconomicScenarioImpactIntermediateConsumptionMatrix, 0, 2)
        
        self.labelRegionalEconomicScenarioImpactValueAddedMatrix = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactValueAddedMatrix.setText('Value added matrix:')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.labelRegionalEconomicScenarioImpactValueAddedMatrix, 1, 0)
        
        self.lineEditRegionalEconomicScenarioImpactValueAddedMatrix = QtGui.QLineEdit()
        self.lineEditRegionalEconomicScenarioImpactValueAddedMatrix.setReadOnly(True)
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.lineEditRegionalEconomicScenarioImpactValueAddedMatrix, 1, 1)
        
        self.buttonSelectRegionalEconomicScenarioImpactValueAddedMatrix = QtGui.QPushButton()
        self.buttonSelectRegionalEconomicScenarioImpactValueAddedMatrix.setText('&Browse')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.buttonSelectRegionalEconomicScenarioImpactValueAddedMatrix, 1, 2)
        
        self.labelRegionalEconomicScenarioImpactFinalConsumptionMatrix = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactFinalConsumptionMatrix.setText('Final consumption matrix:')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.labelRegionalEconomicScenarioImpactFinalConsumptionMatrix, 2, 0)
        
        self.lineEditRegionalEconomicScenarioImpactFinalConsumptionMatrix = QtGui.QLineEdit()
        self.lineEditRegionalEconomicScenarioImpactFinalConsumptionMatrix.setReadOnly(True)
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.lineEditRegionalEconomicScenarioImpactFinalConsumptionMatrix, 2, 1)
        
        self.buttonSelectRegionalEconomicScenarioImpactFinalConsumptionMatrix = QtGui.QPushButton()
        self.buttonSelectRegionalEconomicScenarioImpactFinalConsumptionMatrix.setText('&Browse')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.buttonSelectRegionalEconomicScenarioImpactFinalConsumptionMatrix, 2, 2)
        
        self.labelRegionalEconomicScenarioImpactValueAddedComponent = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactValueAddedComponent.setText('Value added component:')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.labelRegionalEconomicScenarioImpactValueAddedComponent, 3, 0)
        
        self.lineEditRegionalEconomicScenarioImpactValueAddedComponent = QtGui.QLineEdit()
        self.lineEditRegionalEconomicScenarioImpactValueAddedComponent.setReadOnly(True)
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.lineEditRegionalEconomicScenarioImpactValueAddedComponent, 3, 1)
        
        self.buttonSelectRegionalEconomicScenarioImpactValueAddedComponent = QtGui.QPushButton()
        self.buttonSelectRegionalEconomicScenarioImpactValueAddedComponent.setText('&Browse')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.buttonSelectRegionalEconomicScenarioImpactValueAddedComponent, 3, 2)
        
        self.labelRegionalEconomicScenarioImpactFinalConsumptionComponent = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactFinalConsumptionComponent.setText('Final consumption component:')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.labelRegionalEconomicScenarioImpactFinalConsumptionComponent, 4, 0)
        
        self.lineEditRegionalEconomicScenarioImpactFinalConsumptionComponent = QtGui.QLineEdit()
        self.lineEditRegionalEconomicScenarioImpactFinalConsumptionComponent.setReadOnly(True)
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.lineEditRegionalEconomicScenarioImpactFinalConsumptionComponent, 4, 1)
        
        self.buttonSelectRegionalEconomicScenarioImpactFinalConsumptionComponent = QtGui.QPushButton()
        self.buttonSelectRegionalEconomicScenarioImpactFinalConsumptionComponent.setText('&Browse')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.buttonSelectRegionalEconomicScenarioImpactFinalConsumptionComponent, 4, 2)
        
        self.labelRegionalEconomicScenarioImpactListOfEconomicSector = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactListOfEconomicSector.setText('List of economic sector:')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.labelRegionalEconomicScenarioImpactListOfEconomicSector, 5, 0)
        
        self.lineEditRegionalEconomicScenarioImpactListOfEconomicSector = QtGui.QLineEdit()
        self.lineEditRegionalEconomicScenarioImpactListOfEconomicSector.setReadOnly(True)
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.lineEditRegionalEconomicScenarioImpactListOfEconomicSector, 5, 1)
        
        self.buttonSelectRegionalEconomicScenarioImpactListOfEconomicSector = QtGui.QPushButton()
        self.buttonSelectRegionalEconomicScenarioImpactListOfEconomicSector.setText('&Browse')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.buttonSelectRegionalEconomicScenarioImpactListOfEconomicSector, 5, 2)
        
        self.labelRegionalEconomicScenarioImpactLandDistributionMatrix = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactLandDistributionMatrix.setText('Land distribution matrix:')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.labelRegionalEconomicScenarioImpactLandDistributionMatrix, 6, 0)
        
        self.lineEditRegionalEconomicScenarioImpactLandDistributionMatrix = QtGui.QLineEdit()
        self.lineEditRegionalEconomicScenarioImpactLandDistributionMatrix.setReadOnly(True)
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.lineEditRegionalEconomicScenarioImpactLandDistributionMatrix, 6, 1)
        
        self.buttonSelectRegionalEconomicScenarioImpactLandDistributionMatrix = QtGui.QPushButton()
        self.buttonSelectRegionalEconomicScenarioImpactLandDistributionMatrix.setText('&Browse')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.buttonSelectRegionalEconomicScenarioImpactLandDistributionMatrix, 6, 2)
        
        self.labelRegionalEconomicScenarioImpactLandRequirementCoefficientMatrix = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactLandRequirementCoefficientMatrix.setText('Land requirement coefficient matrix:')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.labelRegionalEconomicScenarioImpactLandRequirementCoefficientMatrix, 7, 0)
        
        self.lineEditRegionalEconomicScenarioImpactLandRequirementCoefficientMatrix = QtGui.QLineEdit()
        self.lineEditRegionalEconomicScenarioImpactLandRequirementCoefficientMatrix.setReadOnly(True)
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.lineEditRegionalEconomicScenarioImpactLandRequirementCoefficientMatrix, 7, 1)
        
        self.buttonSelectRegionalEconomicScenarioImpactLandRequirementCoefficientMatrix = QtGui.QPushButton()
        self.buttonSelectRegionalEconomicScenarioImpactLandRequirementCoefficientMatrix.setText('&Browse')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.buttonSelectRegionalEconomicScenarioImpactLandRequirementCoefficientMatrix, 7, 2)
        
        self.labelRegionalEconomicScenarioImpactLandCoverComponent = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactLandCoverComponent.setText('Land cover component:')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.labelRegionalEconomicScenarioImpactLandCoverComponent, 8, 0)
        
        self.lineEditRegionalEconomicScenarioImpactLandCoverComponent = QtGui.QLineEdit()
        self.lineEditRegionalEconomicScenarioImpactLandCoverComponent.setReadOnly(True)
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.lineEditRegionalEconomicScenarioImpactLandCoverComponent, 8, 1)
        
        self.buttonSelectRegionalEconomicScenarioImpactLandCoverComponent = QtGui.QPushButton()
        self.buttonSelectRegionalEconomicScenarioImpactLandCoverComponent.setText('&Browse')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.buttonSelectRegionalEconomicScenarioImpactLandCoverComponent, 8, 2)
        
        self.labelRegionalEconomicScenarioImpactLabourRequirement = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactLabourRequirement.setText('Labour requirement:')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.labelRegionalEconomicScenarioImpactLabourRequirement, 9, 0)
        
        self.lineEditRegionalEconomicScenarioImpactLabourRequirement = QtGui.QLineEdit()
        self.lineEditRegionalEconomicScenarioImpactLabourRequirement.setReadOnly(True)
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.lineEditRegionalEconomicScenarioImpactLabourRequirement, 9, 1)
        
        self.buttonSelectRegionalEconomicScenarioImpactLabourRequirement = QtGui.QPushButton()
        self.buttonSelectRegionalEconomicScenarioImpactLabourRequirement.setText('&Browse')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.buttonSelectRegionalEconomicScenarioImpactLabourRequirement, 9, 2)
        
        self.labelRegionalEconomicScenarioImpactFinancialUnit = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactFinancialUnit.setText('Financial &unit:')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.labelRegionalEconomicScenarioImpactFinancialUnit, 10, 0)
        
        self.lineEditRegionalEconomicScenarioImpactFinancialUnit = QtGui.QLineEdit()
        self.lineEditRegionalEconomicScenarioImpactFinancialUnit.setText('Million Rupiah')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.lineEditRegionalEconomicScenarioImpactFinancialUnit, 10, 1)
        self.labelRegionalEconomicScenarioImpactFinancialUnit.setBuddy(self.lineEditRegionalEconomicScenarioImpactFinancialUnit)
        
        self.labelRegionalEconomicScenarioImpactAreaName = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactAreaName.setText('&Area name:')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.labelRegionalEconomicScenarioImpactAreaName, 11, 0)
        
        self.lineEditRegionalEconomicScenarioImpactAreaName = QtGui.QLineEdit()
        self.lineEditRegionalEconomicScenarioImpactAreaName.setText('area')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.lineEditRegionalEconomicScenarioImpactAreaName, 11, 1)
        self.labelRegionalEconomicScenarioImpactAreaName.setBuddy(self.lineEditRegionalEconomicScenarioImpactAreaName)
        
        self.labelRegionalEconomicScenarioImpactSpinBoxPeriod = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactSpinBoxPeriod.setText('&Period:')
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.labelRegionalEconomicScenarioImpactSpinBoxPeriod, 12, 0)
        
        self.spinBoxRegionalEconomicScenarioImpactPeriod = QtGui.QSpinBox()
        self.spinBoxRegionalEconomicScenarioImpactPeriod.setRange(1, 9999)
        self.spinBoxRegionalEconomicScenarioImpactPeriod.setValue(td.year)
        self.layoutRegionalEconomicScenarioImpactParameters.addWidget(self.spinBoxRegionalEconomicScenarioImpactPeriod, 12, 1)
        self.labelRegionalEconomicScenarioImpactSpinBoxPeriod.setBuddy(self.spinBoxRegionalEconomicScenarioImpactPeriod)
        
        # Process tab button
        self.layoutButtonRegionalEconomicScenarioImpact = QtGui.QHBoxLayout()
        self.buttonProcessRegionalEconomicScenarioImpact = QtGui.QPushButton()
        self.buttonProcessRegionalEconomicScenarioImpact.setText('&Process')
        self.buttonHelpTARegionalEconomicScenarioImpact = QtGui.QPushButton()
        self.buttonHelpTARegionalEconomicScenarioImpact.setIcon(icon)
        self.layoutButtonRegionalEconomicScenarioImpact.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonRegionalEconomicScenarioImpact.addWidget(self.buttonProcessRegionalEconomicScenarioImpact)
        self.layoutButtonRegionalEconomicScenarioImpact.addWidget(self.buttonHelpTARegionalEconomicScenarioImpact)
        
        # Template GroupBox
        self.groupBoxRegionalEconomicScenarioImpactTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxRegionalEconomicScenarioImpactTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxRegionalEconomicScenarioImpactTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxRegionalEconomicScenarioImpactTemplate.setLayout(self.layoutGroupBoxRegionalEconomicScenarioImpactTemplate)
        self.layoutRegionalEconomicScenarioImpactTemplateInfo = QtGui.QVBoxLayout()
        self.layoutRegionalEconomicScenarioImpactTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxRegionalEconomicScenarioImpactTemplate.addLayout(self.layoutRegionalEconomicScenarioImpactTemplateInfo)
        self.layoutGroupBoxRegionalEconomicScenarioImpactTemplate.addLayout(self.layoutRegionalEconomicScenarioImpactTemplate)
        
        self.labelLoadedRegionalEconomicScenarioImpactTemplate = QtGui.QLabel()
        self.labelLoadedRegionalEconomicScenarioImpactTemplate.setText('Loaded template:')
        self.layoutRegionalEconomicScenarioImpactTemplate.addWidget(self.labelLoadedRegionalEconomicScenarioImpactTemplate, 0, 0)
        
        self.loadedRegionalEconomicScenarioImpactTemplate = QtGui.QLabel()
        self.loadedRegionalEconomicScenarioImpactTemplate.setText('<None>')
        self.layoutRegionalEconomicScenarioImpactTemplate.addWidget(self.loadedRegionalEconomicScenarioImpactTemplate, 0, 1)
        
        self.labelRegionalEconomicScenarioImpactTemplate = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactTemplate.setText('Template name:')
        self.layoutRegionalEconomicScenarioImpactTemplate.addWidget(self.labelRegionalEconomicScenarioImpactTemplate, 1, 0)
        
        self.comboBoxRegionalEconomicScenarioImpactTemplate = QtGui.QComboBox()
        self.comboBoxRegionalEconomicScenarioImpactTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxRegionalEconomicScenarioImpactTemplate.setDisabled(True)
        self.comboBoxRegionalEconomicScenarioImpactTemplate.addItem('No template found')
        self.layoutRegionalEconomicScenarioImpactTemplate.addWidget(self.comboBoxRegionalEconomicScenarioImpactTemplate, 1, 1)
        
        self.layoutButtonRegionalEconomicScenarioImpactTemplate = QtGui.QHBoxLayout()
        self.layoutButtonRegionalEconomicScenarioImpactTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadRegionalEconomicScenarioImpactTemplate = QtGui.QPushButton()
        self.buttonLoadRegionalEconomicScenarioImpactTemplate.setDisabled(True)
        self.buttonLoadRegionalEconomicScenarioImpactTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadRegionalEconomicScenarioImpactTemplate.setText('Load')
        self.buttonSaveRegionalEconomicScenarioImpactTemplate = QtGui.QPushButton()
        self.buttonSaveRegionalEconomicScenarioImpactTemplate.setDisabled(True)
        self.buttonSaveRegionalEconomicScenarioImpactTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveRegionalEconomicScenarioImpactTemplate.setText('Save')
        self.buttonSaveAsRegionalEconomicScenarioImpactTemplate = QtGui.QPushButton()
        self.buttonSaveAsRegionalEconomicScenarioImpactTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsRegionalEconomicScenarioImpactTemplate.setText('Save As')
        self.layoutButtonRegionalEconomicScenarioImpactTemplate.addWidget(self.buttonLoadRegionalEconomicScenarioImpactTemplate)
        self.layoutButtonRegionalEconomicScenarioImpactTemplate.addWidget(self.buttonSaveRegionalEconomicScenarioImpactTemplate)
        self.layoutButtonRegionalEconomicScenarioImpactTemplate.addWidget(self.buttonSaveAsRegionalEconomicScenarioImpactTemplate)
        self.layoutGroupBoxRegionalEconomicScenarioImpactTemplate.addLayout(self.layoutButtonRegionalEconomicScenarioImpactTemplate)
        
        # Place the GroupBoxes
        self.layoutContentRegionalEconomicScenarioImpact.addWidget(self.groupBoxRegionalEconomicScenarioImpactType, 0, 0)
        self.layoutContentRegionalEconomicScenarioImpact.addWidget(self.groupBoxRegionalEconomicScenarioImpactParameters, 1, 0)
        self.layoutContentRegionalEconomicScenarioImpact.addLayout(self.layoutButtonRegionalEconomicScenarioImpact, 2, 0, 1, 2, QtCore.Qt.AlignRight)
        self.layoutContentRegionalEconomicScenarioImpact.addWidget(self.groupBoxRegionalEconomicScenarioImpactTemplate, 0, 1, 2, 1)
        self.layoutContentRegionalEconomicScenarioImpact.setColumnStretch(0, 3)
        self.layoutContentRegionalEconomicScenarioImpact.setColumnStretch(1, 1) # Smaller template column
        
        #***********************************************************
        # Setup 'Land Requirement Analysis' tab
        #***********************************************************
        # Use QScrollArea
        ##self.layoutContentLandRequirementAnalysis = QtGui.QVBoxLayout()
        self.layoutContentLandRequirementAnalysis = QtGui.QGridLayout()
        self.contentLandRequirementAnalysis = QtGui.QWidget()
        self.contentLandRequirementAnalysis.setLayout(self.layoutContentLandRequirementAnalysis)
        self.scrollLandRequirementAnalysis = QtGui.QScrollArea()
        self.scrollLandRequirementAnalysis.setWidgetResizable(True);
        self.scrollLandRequirementAnalysis.setWidget(self.contentLandRequirementAnalysis)
        self.layoutTabLandRequirementAnalysis.addWidget(self.scrollLandRequirementAnalysis)
        
        # Parameters 'GroupBox'
        self.groupBoxLandRequirementAnalysisParameters = QtGui.QGroupBox('Parameters')
        self.layoutGroupBoxLandRequirementAnalysisParameters = QtGui.QVBoxLayout()
        self.layoutGroupBoxLandRequirementAnalysisParameters.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLandRequirementAnalysisParameters.setLayout(self.layoutGroupBoxLandRequirementAnalysisParameters)
        self.layoutLandRequirementAnalysisParametersInfo = QtGui.QVBoxLayout()
        self.layoutLandRequirementAnalysisParameters = QtGui.QGridLayout()
        self.layoutGroupBoxLandRequirementAnalysisParameters.addLayout(self.layoutLandRequirementAnalysisParametersInfo)
        self.layoutGroupBoxLandRequirementAnalysisParameters.addLayout(self.layoutLandRequirementAnalysisParameters)
        
        self.labelLandRequirementAnalysisParametersInfo = QtGui.QLabel()
        self.labelLandRequirementAnalysisParametersInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutLandRequirementAnalysisParametersInfo.addWidget(self.labelLandRequirementAnalysisParametersInfo)
        
        self.labelLandRequirementAnalysisIntermediateConsumptionMatrix = QtGui.QLabel()
        self.labelLandRequirementAnalysisIntermediateConsumptionMatrix.setText('Intermediate consumption matrix:')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.labelLandRequirementAnalysisIntermediateConsumptionMatrix, 0, 0)
        
        self.lineEditLandRequirementAnalysisIntermediateConsumptionMatrix = QtGui.QLineEdit()
        self.lineEditLandRequirementAnalysisIntermediateConsumptionMatrix.setReadOnly(True)
        self.layoutLandRequirementAnalysisParameters.addWidget(self.lineEditLandRequirementAnalysisIntermediateConsumptionMatrix, 0, 1)
        
        self.buttonSelectLandRequirementAnalysisIntermediateConsumptionMatrix = QtGui.QPushButton()
        self.buttonSelectLandRequirementAnalysisIntermediateConsumptionMatrix.setText('&Browse')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.buttonSelectLandRequirementAnalysisIntermediateConsumptionMatrix, 0, 2)
        
        self.labelLandRequirementAnalysisValueAddedMatrix = QtGui.QLabel()
        self.labelLandRequirementAnalysisValueAddedMatrix.setText('Value added matrix:')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.labelLandRequirementAnalysisValueAddedMatrix, 1, 0)
        
        self.lineEditLandRequirementAnalysisValueAddedMatrix = QtGui.QLineEdit()
        self.lineEditLandRequirementAnalysisValueAddedMatrix.setReadOnly(True)
        self.layoutLandRequirementAnalysisParameters.addWidget(self.lineEditLandRequirementAnalysisValueAddedMatrix, 1, 1)
        
        self.buttonSelectLandRequirementAnalysisValueAddedMatrix = QtGui.QPushButton()
        self.buttonSelectLandRequirementAnalysisValueAddedMatrix.setText('&Browse')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.buttonSelectLandRequirementAnalysisValueAddedMatrix, 1, 2)
        
        self.labelLandRequirementAnalysisFinalConsumptionMatrix = QtGui.QLabel()
        self.labelLandRequirementAnalysisFinalConsumptionMatrix.setText('Final consumption matrix:')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.labelLandRequirementAnalysisFinalConsumptionMatrix, 2, 0)
        
        self.lineEditLandRequirementAnalysisFinalConsumptionMatrix = QtGui.QLineEdit()
        self.lineEditLandRequirementAnalysisFinalConsumptionMatrix.setReadOnly(True)
        self.layoutLandRequirementAnalysisParameters.addWidget(self.lineEditLandRequirementAnalysisFinalConsumptionMatrix, 2, 1)
        
        self.buttonSelectLandRequirementAnalysisFinalConsumptionMatrix = QtGui.QPushButton()
        self.buttonSelectLandRequirementAnalysisFinalConsumptionMatrix.setText('&Browse')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.buttonSelectLandRequirementAnalysisFinalConsumptionMatrix, 2, 2)
        
        self.labelLandRequirementAnalysisValueAddedComponent = QtGui.QLabel()
        self.labelLandRequirementAnalysisValueAddedComponent.setText('Value added component:')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.labelLandRequirementAnalysisValueAddedComponent, 3, 0)
        
        self.lineEditLandRequirementAnalysisValueAddedComponent = QtGui.QLineEdit()
        self.lineEditLandRequirementAnalysisValueAddedComponent.setReadOnly(True)
        self.layoutLandRequirementAnalysisParameters.addWidget(self.lineEditLandRequirementAnalysisValueAddedComponent, 3, 1)
        
        self.buttonSelectLandRequirementAnalysisValueAddedComponent = QtGui.QPushButton()
        self.buttonSelectLandRequirementAnalysisValueAddedComponent.setText('&Browse')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.buttonSelectLandRequirementAnalysisValueAddedComponent, 3, 2)
        
        self.labelLandRequirementAnalysisFinalConsumptionComponent = QtGui.QLabel()
        self.labelLandRequirementAnalysisFinalConsumptionComponent.setText('Final consumption component:')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.labelLandRequirementAnalysisFinalConsumptionComponent, 4, 0)
        
        self.lineEditLandRequirementAnalysisFinalConsumptionComponent = QtGui.QLineEdit()
        self.lineEditLandRequirementAnalysisFinalConsumptionComponent.setReadOnly(True)
        self.layoutLandRequirementAnalysisParameters.addWidget(self.lineEditLandRequirementAnalysisFinalConsumptionComponent, 4, 1)
        
        self.buttonSelectLandRequirementAnalysisFinalConsumptionComponent = QtGui.QPushButton()
        self.buttonSelectLandRequirementAnalysisFinalConsumptionComponent.setText('&Browse')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.buttonSelectLandRequirementAnalysisFinalConsumptionComponent, 4, 2)
        
        self.labelLandRequirementAnalysisListOfEconomicSector = QtGui.QLabel()
        self.labelLandRequirementAnalysisListOfEconomicSector.setText('List of economic sector:')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.labelLandRequirementAnalysisListOfEconomicSector, 5, 0)
        
        self.lineEditLandRequirementAnalysisListOfEconomicSector = QtGui.QLineEdit()
        self.lineEditLandRequirementAnalysisListOfEconomicSector.setReadOnly(True)
        self.layoutLandRequirementAnalysisParameters.addWidget(self.lineEditLandRequirementAnalysisListOfEconomicSector, 5, 1)
        
        self.buttonSelectLandRequirementAnalysisListOfEconomicSector = QtGui.QPushButton()
        self.buttonSelectLandRequirementAnalysisListOfEconomicSector.setText('&Browse')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.buttonSelectLandRequirementAnalysisListOfEconomicSector, 5, 2)
        
        self.labelLandRequirementAnalysisLandDistributionMatrix = QtGui.QLabel()
        self.labelLandRequirementAnalysisLandDistributionMatrix.setText('Land distribution matrix:')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.labelLandRequirementAnalysisLandDistributionMatrix, 6, 0)
        
        self.lineEditLandRequirementAnalysisLandDistributionMatrix = QtGui.QLineEdit()
        self.lineEditLandRequirementAnalysisLandDistributionMatrix.setReadOnly(True)
        self.layoutLandRequirementAnalysisParameters.addWidget(self.lineEditLandRequirementAnalysisLandDistributionMatrix, 6, 1)
        
        self.buttonSelectLandRequirementAnalysisLandDistributionMatrix = QtGui.QPushButton()
        self.buttonSelectLandRequirementAnalysisLandDistributionMatrix.setText('&Browse')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.buttonSelectLandRequirementAnalysisLandDistributionMatrix, 6, 2)
        
        self.labelLandRequirementAnalysisLandCoverComponent = QtGui.QLabel()
        self.labelLandRequirementAnalysisLandCoverComponent.setText('Land cover component:')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.labelLandRequirementAnalysisLandCoverComponent, 7, 0)
        
        self.lineEditLandRequirementAnalysisLandCoverComponent = QtGui.QLineEdit()
        self.lineEditLandRequirementAnalysisLandCoverComponent.setReadOnly(True)
        self.layoutLandRequirementAnalysisParameters.addWidget(self.lineEditLandRequirementAnalysisLandCoverComponent, 7, 1)
        
        self.buttonSelectLandRequirementAnalysisLandCoverComponent = QtGui.QPushButton()
        self.buttonSelectLandRequirementAnalysisLandCoverComponent.setText('&Browse')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.buttonSelectLandRequirementAnalysisLandCoverComponent, 7, 2)
        
        self.labelLandRequirementAnalysisLabourRequirement = QtGui.QLabel()
        self.labelLandRequirementAnalysisLabourRequirement.setText('Labour requirement:')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.labelLandRequirementAnalysisLabourRequirement, 8, 0)
        
        self.lineEditLandRequirementAnalysisLabourRequirement = QtGui.QLineEdit()
        self.lineEditLandRequirementAnalysisLabourRequirement.setReadOnly(True)
        self.layoutLandRequirementAnalysisParameters.addWidget(self.lineEditLandRequirementAnalysisLabourRequirement, 8, 1)
        
        self.buttonSelectLandRequirementAnalysisLabourRequirement = QtGui.QPushButton()
        self.buttonSelectLandRequirementAnalysisLabourRequirement.setText('&Browse')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.buttonSelectLandRequirementAnalysisLabourRequirement, 8, 2)
        
        self.labelLandRequirementAnalysisFinancialUnit = QtGui.QLabel()
        self.labelLandRequirementAnalysisFinancialUnit.setText('Financial &unit:')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.labelLandRequirementAnalysisFinancialUnit, 9, 0)
        
        self.lineEditLandRequirementAnalysisFinancialUnit = QtGui.QLineEdit()
        self.lineEditLandRequirementAnalysisFinancialUnit.setText('Million Rupiah')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.lineEditLandRequirementAnalysisFinancialUnit, 9, 1)
        
        self.labelLandRequirementAnalysisFinancialUnit.setBuddy(self.lineEditLandRequirementAnalysisFinancialUnit)
        
        self.labelLandRequirementAnalysisAreaName = QtGui.QLabel()
        self.labelLandRequirementAnalysisAreaName.setText('&Area name:')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.labelLandRequirementAnalysisAreaName, 10, 0)
        
        self.lineEditLandRequirementAnalysisAreaName = QtGui.QLineEdit()
        self.lineEditLandRequirementAnalysisAreaName.setText('area')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.lineEditLandRequirementAnalysisAreaName, 10, 1)
        self.labelLandRequirementAnalysisAreaName.setBuddy(self.lineEditLandRequirementAnalysisAreaName)
        
        self.labelLandRequirementAnalysisPeriod = QtGui.QLabel()
        self.labelLandRequirementAnalysisPeriod.setText('&Period:')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.labelLandRequirementAnalysisPeriod, 11, 0)
        
        self.spinBoxLandRequirementAnalysisPeriod = QtGui.QSpinBox()
        self.spinBoxLandRequirementAnalysisPeriod.setRange(1, 9999)
        self.spinBoxLandRequirementAnalysisPeriod.setValue(td.year)
        self.layoutLandRequirementAnalysisParameters.addWidget(self.spinBoxLandRequirementAnalysisPeriod, 11, 1)
        self.labelLandRequirementAnalysisPeriod.setBuddy(self.spinBoxLandRequirementAnalysisPeriod)
            
        # Process tab button
        self.layoutButtonLandRequirementAnalysis = QtGui.QHBoxLayout()
        self.buttonProcessLandRequirementAnalysis = QtGui.QPushButton()
        self.buttonProcessLandRequirementAnalysis.setText('&Process')
        self.buttonHelpTALandRequirementAnalysis = QtGui.QPushButton()
        self.buttonHelpTALandRequirementAnalysis.setIcon(icon)
        self.layoutButtonLandRequirementAnalysis.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonLandRequirementAnalysis.addWidget(self.buttonProcessLandRequirementAnalysis)
        self.layoutButtonLandRequirementAnalysis.addWidget(self.buttonHelpTALandRequirementAnalysis)
        
        # Template GroupBox
        self.groupBoxLandRequirementAnalysisTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxLandRequirementAnalysisTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxLandRequirementAnalysisTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLandRequirementAnalysisTemplate.setLayout(self.layoutGroupBoxLandRequirementAnalysisTemplate)
        self.layoutLandRequirementAnalysisTemplateInfo = QtGui.QVBoxLayout()
        self.layoutLandRequirementAnalysisTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxLandRequirementAnalysisTemplate.addLayout(self.layoutLandRequirementAnalysisTemplateInfo)
        self.layoutGroupBoxLandRequirementAnalysisTemplate.addLayout(self.layoutLandRequirementAnalysisTemplate)
        
        self.labelLoadedLandRequirementAnalysisTemplate = QtGui.QLabel()
        self.labelLoadedLandRequirementAnalysisTemplate.setText('Loaded template:')
        self.layoutLandRequirementAnalysisTemplate.addWidget(self.labelLoadedLandRequirementAnalysisTemplate, 0, 0)
        
        self.loadedLandRequirementAnalysisTemplate = QtGui.QLabel()
        self.loadedLandRequirementAnalysisTemplate.setText('<None>')
        self.layoutLandRequirementAnalysisTemplate.addWidget(self.loadedLandRequirementAnalysisTemplate, 0, 1)
        
        self.labelLandRequirementAnalysisTemplate = QtGui.QLabel()
        self.labelLandRequirementAnalysisTemplate.setText('Template name:')
        self.layoutLandRequirementAnalysisTemplate.addWidget(self.labelLandRequirementAnalysisTemplate, 1, 0)
        
        self.comboBoxLandRequirementAnalysisTemplate = QtGui.QComboBox()
        self.comboBoxLandRequirementAnalysisTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxLandRequirementAnalysisTemplate.setDisabled(True)
        self.comboBoxLandRequirementAnalysisTemplate.addItem('No template found')
        self.layoutLandRequirementAnalysisTemplate.addWidget(self.comboBoxLandRequirementAnalysisTemplate, 1, 1)
        
        self.layoutButtonLandRequirementAnalysisTemplate = QtGui.QHBoxLayout()
        self.layoutButtonLandRequirementAnalysisTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadLandRequirementAnalysisTemplate = QtGui.QPushButton()
        self.buttonLoadLandRequirementAnalysisTemplate.setDisabled(True)
        self.buttonLoadLandRequirementAnalysisTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadLandRequirementAnalysisTemplate.setText('Load')
        self.buttonSaveLandRequirementAnalysisTemplate = QtGui.QPushButton()
        self.buttonSaveLandRequirementAnalysisTemplate.setDisabled(True)
        self.buttonSaveLandRequirementAnalysisTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveLandRequirementAnalysisTemplate.setText('Save')
        self.buttonSaveAsLandRequirementAnalysisTemplate = QtGui.QPushButton()
        self.buttonSaveAsLandRequirementAnalysisTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsLandRequirementAnalysisTemplate.setText('Save As')
        self.layoutButtonLandRequirementAnalysisTemplate.addWidget(self.buttonLoadLandRequirementAnalysisTemplate)
        self.layoutButtonLandRequirementAnalysisTemplate.addWidget(self.buttonSaveLandRequirementAnalysisTemplate)
        self.layoutButtonLandRequirementAnalysisTemplate.addWidget(self.buttonSaveAsLandRequirementAnalysisTemplate)
        self.layoutGroupBoxLandRequirementAnalysisTemplate.addLayout(self.layoutButtonLandRequirementAnalysisTemplate)
        
        # Place the GroupBoxes
        self.layoutContentLandRequirementAnalysis.addWidget(self.groupBoxLandRequirementAnalysisParameters, 0, 0)
        self.layoutContentLandRequirementAnalysis.addLayout(self.layoutButtonLandRequirementAnalysis, 1, 0, 1, 2, QtCore.Qt.AlignRight)
        self.layoutContentLandRequirementAnalysis.addWidget(self.groupBoxLandRequirementAnalysisTemplate, 0, 1, 1, 1)
        self.layoutContentLandRequirementAnalysis.setColumnStretch(0, 3)
        self.layoutContentLandRequirementAnalysis.setColumnStretch(1, 1) # Smaller template column
        
        #***********************************************************
        # Setup 'Land Use Change Impact' tab
        #***********************************************************
        # Use QScrollArea
        ##self.layoutContentLandUseChangeImpact = QtGui.QVBoxLayout()
        self.layoutContentLandUseChangeImpact = QtGui.QGridLayout()
        self.contentLandUseChangeImpact = QtGui.QWidget()
        self.contentLandUseChangeImpact.setLayout(self.layoutContentLandUseChangeImpact)
        self.scrollLandUseChangeImpact = QtGui.QScrollArea()
        self.scrollLandUseChangeImpact.setWidgetResizable(True);
        self.scrollLandUseChangeImpact.setWidget(self.contentLandUseChangeImpact)
        self.layoutTabLandUseChangeImpact.addWidget(self.scrollLandUseChangeImpact)
        
        # Parameters 'GroupBox'
        self.groupBoxLandUseChangeImpactParameters = QtGui.QGroupBox('Parameters')
        self.layoutGroupBoxLandUseChangeImpactParameters = QtGui.QVBoxLayout()
        self.layoutGroupBoxLandUseChangeImpactParameters.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLandUseChangeImpactParameters.setLayout(self.layoutGroupBoxLandUseChangeImpactParameters)
        self.layoutLandUseChangeImpactParametersInfo = QtGui.QVBoxLayout()
        self.layoutLandUseChangeImpactParameters = QtGui.QGridLayout()
        self.layoutGroupBoxLandUseChangeImpactParameters.addLayout(self.layoutLandUseChangeImpactParametersInfo)
        self.layoutGroupBoxLandUseChangeImpactParameters.addLayout(self.layoutLandUseChangeImpactParameters)
        
        self.labelLandUseChangeImpactParametersInfo = QtGui.QLabel()
        self.labelLandUseChangeImpactParametersInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutLandUseChangeImpactParametersInfo.addWidget(self.labelLandUseChangeImpactParametersInfo)
        
        self.labelLandUseChangeImpactIntermediateConsumptionMatrix = QtGui.QLabel()
        self.labelLandUseChangeImpactIntermediateConsumptionMatrix.setText('Intermediate consumption matrix:')
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelLandUseChangeImpactIntermediateConsumptionMatrix, 0, 0)
        
        self.lineEditLandUseChangeImpactIntermediateConsumptionMatrix = QtGui.QLineEdit()
        self.lineEditLandUseChangeImpactIntermediateConsumptionMatrix.setReadOnly(True)
        self.layoutLandUseChangeImpactParameters.addWidget(self.lineEditLandUseChangeImpactIntermediateConsumptionMatrix, 0, 1)
        
        self.buttonSelectLandUseChangeImpactIntermediateConsumptionMatrix = QtGui.QPushButton()
        self.buttonSelectLandUseChangeImpactIntermediateConsumptionMatrix.setText('&Browse')
        self.layoutLandUseChangeImpactParameters.addWidget(self.buttonSelectLandUseChangeImpactIntermediateConsumptionMatrix, 0, 2)
        
        self.labelLandUseChangeImpactValueAddedMatrix = QtGui.QLabel()
        self.labelLandUseChangeImpactValueAddedMatrix.setText('Value added matrix:')
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelLandUseChangeImpactValueAddedMatrix, 1, 0)
        
        self.lineEditLandUseChangeImpactValueAddedMatrix = QtGui.QLineEdit()
        self.lineEditLandUseChangeImpactValueAddedMatrix.setReadOnly(True)
        self.layoutLandUseChangeImpactParameters.addWidget(self.lineEditLandUseChangeImpactValueAddedMatrix, 1, 1)
        
        self.buttonSelectLandUseChangeImpactValueAddedMatrix = QtGui.QPushButton()
        self.buttonSelectLandUseChangeImpactValueAddedMatrix.setText('&Browse')
        self.layoutLandUseChangeImpactParameters.addWidget(self.buttonSelectLandUseChangeImpactValueAddedMatrix, 1, 2)
        
        self.labelLandUseChangeImpactFinalConsumptionMatrix = QtGui.QLabel()
        self.labelLandUseChangeImpactFinalConsumptionMatrix.setText('Final consumption matrix:')
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelLandUseChangeImpactFinalConsumptionMatrix, 2, 0)
        
        self.lineEditLandUseChangeImpactFinalConsumptionMatrix = QtGui.QLineEdit()
        self.lineEditLandUseChangeImpactFinalConsumptionMatrix.setReadOnly(True)
        self.layoutLandUseChangeImpactParameters.addWidget(self.lineEditLandUseChangeImpactFinalConsumptionMatrix, 2, 1)
        
        self.buttonSelectLandUseChangeImpactFinalConsumptionMatrix = QtGui.QPushButton()
        self.buttonSelectLandUseChangeImpactFinalConsumptionMatrix.setText('&Browse')
        self.layoutLandUseChangeImpactParameters.addWidget(self.buttonSelectLandUseChangeImpactFinalConsumptionMatrix, 2, 2)
        
        self.labelLandUseChangeImpactValueAddedComponent = QtGui.QLabel()
        self.labelLandUseChangeImpactValueAddedComponent.setText('Value added component:')
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelLandUseChangeImpactValueAddedComponent, 3, 0)
        
        self.lineEditLandUseChangeImpactValueAddedComponent = QtGui.QLineEdit()
        self.lineEditLandUseChangeImpactValueAddedComponent.setReadOnly(True)
        self.layoutLandUseChangeImpactParameters.addWidget(self.lineEditLandUseChangeImpactValueAddedComponent, 3, 1)
        
        self.buttonSelectLandUseChangeImpactValueAddedComponent = QtGui.QPushButton()
        self.buttonSelectLandUseChangeImpactValueAddedComponent.setText('&Browse')
        self.layoutLandUseChangeImpactParameters.addWidget(self.buttonSelectLandUseChangeImpactValueAddedComponent, 3, 2)
        
        self.labelLandUseChangeImpactFinalConsumptionComponent = QtGui.QLabel()
        self.labelLandUseChangeImpactFinalConsumptionComponent.setText('Final consumption component:')
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelLandUseChangeImpactFinalConsumptionComponent, 4, 0)
        
        self.lineEditLandUseChangeImpactFinalConsumptionComponent = QtGui.QLineEdit()
        self.lineEditLandUseChangeImpactFinalConsumptionComponent.setReadOnly(True)
        self.layoutLandUseChangeImpactParameters.addWidget(self.lineEditLandUseChangeImpactFinalConsumptionComponent, 4, 1)
        
        self.buttonSelectLandUseChangeImpactFinalConsumptionComponent = QtGui.QPushButton()
        self.buttonSelectLandUseChangeImpactFinalConsumptionComponent.setText('&Browse')
        self.layoutLandUseChangeImpactParameters.addWidget(self.buttonSelectLandUseChangeImpactFinalConsumptionComponent, 4, 2)
        
        self.labelLandUseChangeImpactListOfEconomicSector = QtGui.QLabel()
        self.labelLandUseChangeImpactListOfEconomicSector.setText('List of economic sector:')
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelLandUseChangeImpactListOfEconomicSector, 5, 0)
        
        self.lineEditLandUseChangeImpactListOfEconomicSector = QtGui.QLineEdit()
        self.lineEditLandUseChangeImpactListOfEconomicSector.setReadOnly(True)
        self.layoutLandUseChangeImpactParameters.addWidget(self.lineEditLandUseChangeImpactListOfEconomicSector, 5, 1)
        
        self.buttonSelectLandUseChangeImpactListOfEconomicSector = QtGui.QPushButton()
        self.buttonSelectLandUseChangeImpactListOfEconomicSector.setText('&Browse')
        self.layoutLandUseChangeImpactParameters.addWidget(self.buttonSelectLandUseChangeImpactListOfEconomicSector, 5, 2)
        
        self.labelLandUseChangeImpactLandDistributionMatrix = QtGui.QLabel()
        self.labelLandUseChangeImpactLandDistributionMatrix.setText('Land distribution matrix:')
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelLandUseChangeImpactLandDistributionMatrix, 6, 0)
        
        self.lineEditLandUseChangeImpactLandDistributionMatrix = QtGui.QLineEdit()
        self.lineEditLandUseChangeImpactLandDistributionMatrix.setReadOnly(True)
        self.layoutLandUseChangeImpactParameters.addWidget(self.lineEditLandUseChangeImpactLandDistributionMatrix, 6, 1)
        
        self.buttonSelectLandUseChangeImpactLandDistributionMatrix = QtGui.QPushButton()
        self.buttonSelectLandUseChangeImpactLandDistributionMatrix.setText('&Browse')
        self.layoutLandUseChangeImpactParameters.addWidget(self.buttonSelectLandUseChangeImpactLandDistributionMatrix, 6, 2)
        
        self.labelLandUseChangeImpactLandRequirementCoefficientMatrix = QtGui.QLabel()
        self.labelLandUseChangeImpactLandRequirementCoefficientMatrix.setText('Land requirement coefficient matrix:')
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelLandUseChangeImpactLandRequirementCoefficientMatrix, 7, 0)
        
        self.lineEditLandUseChangeImpactLandRequirementCoefficientMatrix = QtGui.QLineEdit()
        self.lineEditLandUseChangeImpactLandRequirementCoefficientMatrix.setReadOnly(True)
        self.layoutLandUseChangeImpactParameters.addWidget(self.lineEditLandUseChangeImpactLandRequirementCoefficientMatrix, 7, 1)
        
        self.buttonSelectLandUseChangeImpactLandRequirementCoefficientMatrix = QtGui.QPushButton()
        self.buttonSelectLandUseChangeImpactLandRequirementCoefficientMatrix.setText('&Browse')
        self.layoutLandUseChangeImpactParameters.addWidget(self.buttonSelectLandUseChangeImpactLandRequirementCoefficientMatrix, 7, 2)
        
        self.labelLandUseChangeImpactLandCoverComponent = QtGui.QLabel()
        self.labelLandUseChangeImpactLandCoverComponent.setText('Land cover component:')
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelLandUseChangeImpactLandCoverComponent, 8, 0)
        
        self.lineEditLandUseChangeImpactLandCoverComponent = QtGui.QLineEdit()
        self.lineEditLandUseChangeImpactLandCoverComponent.setReadOnly(True)
        self.layoutLandUseChangeImpactParameters.addWidget(self.lineEditLandUseChangeImpactLandCoverComponent, 8, 1)
        
        self.buttonSelectLandUseChangeImpactLandCoverComponent = QtGui.QPushButton()
        self.buttonSelectLandUseChangeImpactLandCoverComponent.setText('&Browse')
        self.layoutLandUseChangeImpactParameters.addWidget(self.buttonSelectLandUseChangeImpactLandCoverComponent, 8, 2)
        
        self.labelLandUseChangeImpactLabourRequirement = QtGui.QLabel()
        self.labelLandUseChangeImpactLabourRequirement.setText('Labour requirement:')
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelLandUseChangeImpactLabourRequirement, 9, 0)
        
        self.lineEditLandUseChangeImpactLabourRequirement = QtGui.QLineEdit()
        self.lineEditLandUseChangeImpactLabourRequirement.setReadOnly(True)
        self.layoutLandUseChangeImpactParameters.addWidget(self.lineEditLandUseChangeImpactLabourRequirement, 9, 1)
        
        self.buttonSelectLandUseChangeImpactLabourRequirement = QtGui.QPushButton()
        self.buttonSelectLandUseChangeImpactLabourRequirement.setText('&Browse')
        self.layoutLandUseChangeImpactParameters.addWidget(self.buttonSelectLandUseChangeImpactLabourRequirement, 9, 2)
        
        self.labelLandUseChangeImpactFinancialUnit = QtGui.QLabel()
        self.labelLandUseChangeImpactFinancialUnit.setText('Financial &unit:')
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelLandUseChangeImpactFinancialUnit, 10, 0)
        
        self.lineEditLandUseChangeImpactFinancialUnit = QtGui.QLineEdit()
        self.lineEditLandUseChangeImpactFinancialUnit.setText('Million Rupiah')
        self.layoutLandUseChangeImpactParameters.addWidget(self.lineEditLandUseChangeImpactFinancialUnit, 10, 1)
        self.labelLandUseChangeImpactFinancialUnit.setBuddy(self.lineEditLandUseChangeImpactFinancialUnit)
        
        self.labelLandUseChangeImpactAreaName = QtGui.QLabel()
        self.labelLandUseChangeImpactAreaName.setText('&Area name:')
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelLandUseChangeImpactAreaName, 11, 0)
        
        self.lineEditLandUseChangeImpactAreaName = QtGui.QLineEdit()
        self.lineEditLandUseChangeImpactAreaName.setText('area')
        self.layoutLandUseChangeImpactParameters.addWidget(self.lineEditLandUseChangeImpactAreaName, 11, 1)
        self.labelLandUseChangeImpactAreaName.setBuddy(self.lineEditLandUseChangeImpactAreaName)
        
        self.labelLandUseChangeImpactPeriod = QtGui.QLabel()
        self.labelLandUseChangeImpactPeriod.setText('&Period:')
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelLandUseChangeImpactPeriod, 12, 0)
        
        self.spinBoxLandUseChangeImpactPeriod = QtGui.QSpinBox()
        self.spinBoxLandUseChangeImpactPeriod.setRange(1, 9999)
        self.spinBoxLandUseChangeImpactPeriod.setValue(td.year)
        self.layoutLandUseChangeImpactParameters.addWidget(self.spinBoxLandUseChangeImpactPeriod, 12, 1)
        self.labelLandUseChangeImpactPeriod.setBuddy(self.spinBoxLandUseChangeImpactPeriod)
        
        # Process tab button
        self.layoutButtonLandUseChangeImpact = QtGui.QHBoxLayout()
        self.buttonProcessLandUseChangeImpact = QtGui.QPushButton()
        self.buttonProcessLandUseChangeImpact.setText('&Process')
        self.buttonHelpTALandUseChangeImpact = QtGui.QPushButton()
        self.buttonHelpTALandUseChangeImpact.setIcon(icon)
        self.layoutButtonLandUseChangeImpact.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonLandUseChangeImpact.addWidget(self.buttonProcessLandUseChangeImpact)
        self.layoutButtonLandUseChangeImpact.addWidget(self.buttonHelpTALandUseChangeImpact)
        
        # Template GroupBox
        self.groupBoxLandUseChangeImpactTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxLandUseChangeImpactTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxLandUseChangeImpactTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLandUseChangeImpactTemplate.setLayout(self.layoutGroupBoxLandUseChangeImpactTemplate)
        self.layoutLandUseChangeImpactTemplateInfo = QtGui.QVBoxLayout()
        self.layoutLandUseChangeImpactTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxLandUseChangeImpactTemplate.addLayout(self.layoutLandUseChangeImpactTemplateInfo)
        self.layoutGroupBoxLandUseChangeImpactTemplate.addLayout(self.layoutLandUseChangeImpactTemplate)
        
        self.labelLoadedLandUseChangeImpactTemplate = QtGui.QLabel()
        self.labelLoadedLandUseChangeImpactTemplate.setText('Loaded template:')
        self.layoutLandUseChangeImpactTemplate.addWidget(self.labelLoadedLandUseChangeImpactTemplate, 0, 0)
        
        self.loadedLandUseChangeImpactTemplate = QtGui.QLabel()
        self.loadedLandUseChangeImpactTemplate.setText('<None>')
        self.layoutLandUseChangeImpactTemplate.addWidget(self.loadedLandUseChangeImpactTemplate, 0, 1)
        
        self.labelLandUseChangeImpactTemplate = QtGui.QLabel()
        self.labelLandUseChangeImpactTemplate.setText('Template name:')
        self.layoutLandUseChangeImpactTemplate.addWidget(self.labelLandUseChangeImpactTemplate, 1, 0)
        
        self.comboBoxLandUseChangeImpactTemplate = QtGui.QComboBox()
        self.comboBoxLandUseChangeImpactTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxLandUseChangeImpactTemplate.setDisabled(True)
        self.comboBoxLandUseChangeImpactTemplate.addItem('No template found')
        self.layoutLandUseChangeImpactTemplate.addWidget(self.comboBoxLandUseChangeImpactTemplate, 1, 1)
        
        self.layoutButtonLandUseChangeImpactTemplate = QtGui.QHBoxLayout()
        self.layoutButtonLandUseChangeImpactTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadLandUseChangeImpactTemplate = QtGui.QPushButton()
        self.buttonLoadLandUseChangeImpactTemplate.setDisabled(True)
        self.buttonLoadLandUseChangeImpactTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadLandUseChangeImpactTemplate.setText('Load')
        self.buttonSaveLandUseChangeImpactTemplate = QtGui.QPushButton()
        self.buttonSaveLandUseChangeImpactTemplate.setDisabled(True)
        self.buttonSaveLandUseChangeImpactTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveLandUseChangeImpactTemplate.setText('Save')
        self.buttonSaveAsLandUseChangeImpactTemplate = QtGui.QPushButton()
        self.buttonSaveAsLandUseChangeImpactTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsLandUseChangeImpactTemplate.setText('Save As')
        self.layoutButtonLandUseChangeImpactTemplate.addWidget(self.buttonLoadLandUseChangeImpactTemplate)
        self.layoutButtonLandUseChangeImpactTemplate.addWidget(self.buttonSaveLandUseChangeImpactTemplate)
        self.layoutButtonLandUseChangeImpactTemplate.addWidget(self.buttonSaveAsLandUseChangeImpactTemplate)
        self.layoutGroupBoxLandUseChangeImpactTemplate.addLayout(self.layoutButtonLandUseChangeImpactTemplate)
        
        # Place the GroupBoxes
        self.layoutContentLandUseChangeImpact.addWidget(self.groupBoxLandUseChangeImpactParameters, 0, 0)
        self.layoutContentLandUseChangeImpact.addLayout(self.layoutButtonLandUseChangeImpact, 1, 0, 1, 2, QtCore.Qt.AlignRight)
        self.layoutContentLandUseChangeImpact.addWidget(self.groupBoxLandUseChangeImpactTemplate, 0, 1, 1, 1)
        self.layoutContentLandUseChangeImpact.setColumnStretch(0, 3)
        self.layoutContentLandUseChangeImpact.setColumnStretch(1, 1) # Smaller template column

        
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
        self.setMinimumSize(700, 480)
        self.resize(parent.sizeHint())
    
    
    def showEvent(self, event):
        """Overload method that is called when the dialog widget is shown.
        
        Args:
            event (QShowEvent): the show widget event.
        """
        super(DialogLumensTA, self).showEvent(event)
    
    
    def closeEvent(self, event):
        """Overload method that is called when the dialog widget is closed.
        
        Args:
            event (QCloseEvent): the close widget event.
        """
        super(DialogLumensTA, self).closeEvent(event)
    
    
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
                'Load Template',
                'Do you want to load \'{0}\'?'.format(templateFile),
                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                QtGui.QMessageBox.No
            )
            
        if reply == QtGui.QMessageBox.Yes or fileName:
            self.loadTemplate('Abacus Opportunity Cost', templateFile)
    
    
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
            'Save Template',
            'Do you want save \'{0}\'?\nThis action will overwrite the template file.'.format(templateFile),
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
            QtGui.QMessageBox.No
        )
            
        if reply == QtGui.QMessageBox.Yes:
            self.saveTemplate('Abacus Opportunity Cost', templateFile)
            return True
        else:
            return False
    
    
    def handlerSaveAsAbacusOpportunityCostTemplate(self):
        """Slot method for saving a module template to a new file.
        """
        fileName, ok = QtGui.QInputDialog.getText(self, 'Save As', 'Enter a new template name:')
        fileSaved = False
        
        if ok:
            now = QtCore.QDateTime.currentDateTime().toString('yyyyMMdd-hhmmss')
            fileName = now + '__' + fileName + '.ini'
            
            if os.path.exists(os.path.join(self.settingsPath, fileName)):
                fileSaved = self.handlerSaveAbacusOpportunityCostTemplate(fileName)
            else:
                self.saveTemplate('Abacus Opportunity Cost', fileName)
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
                'Load Template',
                'Do you want to load \'{0}\'?'.format(templateFile),
                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                QtGui.QMessageBox.No
            )
            
        if reply == QtGui.QMessageBox.Yes or fileName:
            self.loadTemplate('Opportunity Cost Curve', templateFile)
    
    
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
            'Save Template',
            'Do you want save \'{0}\'?\nThis action will overwrite the template file.'.format(templateFile),
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
            QtGui.QMessageBox.No
        )
            
        if reply == QtGui.QMessageBox.Yes:
            self.saveTemplate('Opportunity Cost Curve', templateFile)
            return True
        else:
            return False
    
    
    def handlerSaveAsOpportunityCostCurveTemplate(self):
        """Slot method for saving a module template to a new file.
        """
        fileName, ok = QtGui.QInputDialog.getText(self, 'Save As', 'Enter a new template name:')
        fileSaved = False
        
        if ok:
            now = QtCore.QDateTime.currentDateTime().toString('yyyyMMdd-hhmmss')
            fileName = now + '__' + fileName + '.ini'
            
            if os.path.exists(os.path.join(self.settingsPath, fileName)):
                fileSaved = self.handlerSaveOpportunityCostCurveTemplate(fileName)
            else:
                self.saveTemplate('Opportunity Cost Curve', fileName)
                fileSaved = True
            
            self.loadTemplateFiles()
            
            # Load the newly saved template file
            if fileSaved:
                self.handlerLoadOpportunityCostCurveTemplate(fileName)
    
    
    def handlerSelectOCCCsvNPVTable(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select NPV Table', QtCore.QDir.homePath(), 'NPV Table (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditOCCCsvNPVTable.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectOCCOutputOpportunityCostDatabase(self):
        """Slot method for a file select dialog.
        """
        outputfile = unicode(QtGui.QFileDialog.getSaveFileName(
            self, 'Create/Select Opportunity Cost Database Output', QtCore.QDir.homePath(), 'Opportunity Cost Database (*{0})'.format(self.main.appSettings['selectDatabasefileExt'])))
        
        if outputfile:
            self.lineEditOCCOutputOpportunityCostDatabase.setText(outputfile)
            logging.getLogger(type(self).__name__).info('select output file: %s', outputfile)
    
    
    def handlerSelectOCCOutputOpportunityCostReport(self):
        """Slot method for a file select dialog.
        """
        outputfile = unicode(QtGui.QFileDialog.getSaveFileName(
            self, 'Create/Select Opportunity Cost Report Output', QtCore.QDir.homePath(), 'Opportunity Cost Report (*{0})'.format(self.main.appSettings['selectHTMLfileExt'])))
        
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
                'Load Template',
                'Do you want to load \'{0}\'?'.format(templateFile),
                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                QtGui.QMessageBox.No
            )
            
        if reply == QtGui.QMessageBox.Yes or fileName:
            self.loadTemplate('Opportunity Cost Map', templateFile)
    
    
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
            'Save Template',
            'Do you want save \'{0}\'?\nThis action will overwrite the template file.'.format(templateFile),
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
            QtGui.QMessageBox.No
        )
            
        if reply == QtGui.QMessageBox.Yes:
            self.saveTemplate('Opportunity Cost Map', templateFile)
            return True
        else:
            return False
    
    
    def handlerSaveAsOpportunityCostMapTemplate(self):
        """Slot method for saving a module template to a new file.
        """
        fileName, ok = QtGui.QInputDialog.getText(self, 'Save As', 'Enter a new template name:')
        fileSaved = False
        
        if ok:
            now = QtCore.QDateTime.currentDateTime().toString('yyyyMMdd-hhmmss')
            fileName = now + '__' + fileName + '.ini'
            
            if os.path.exists(os.path.join(self.settingsPath, fileName)):
                fileSaved = self.handlerSaveOpportunityCostMapTemplate(fileName)
            else:
                self.saveTemplate('Opportunity Cost Map', fileName)
                fileSaved = True
            
            self.loadTemplateFiles()
            
            # Load the newly saved template file
            if fileSaved:
                self.handlerLoadOpportunityCostMapTemplate(fileName)
    
    
    def handlerSelectOCMCsvProfitability(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Profitability Lookup Table', QtCore.QDir.homePath(), 'Profitability Lookup Table (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
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
    
