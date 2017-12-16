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
            
            # RE Templates
            self.comboBoxDescriptiveAnalysisTemplate.clear()
            self.comboBoxDescriptiveAnalysisTemplate.addItems(sorted(templateFiles))
            self.comboBoxDescriptiveAnalysisTemplate.setEnabled(True)
            self.buttonLoadDescriptiveAnalysisTemplate.setEnabled(True)
            
            self.comboBoxRegionalEconomicScenarioImpactTemplate.clear()
            self.comboBoxRegionalEconomicScenarioImpactTemplate.addItems(sorted(templateFiles))
            self.comboBoxRegionalEconomicScenarioImpactTemplate.setEnabled(True)
            self.buttonLoadRegionalEconomicScenarioImpactTemplate.setEnabled(True)
            
            self.comboBoxLandRequirementAnalysisTemplate.clear()
            self.comboBoxLandRequirementAnalysisTemplate.addItems(sorted(templateFiles))
            self.comboBoxLandRequirementAnalysisTemplate.setEnabled(True)
            self.buttonLoadLandRequirementAnalysisTemplate.setEnabled(True)
            
            self.comboBoxLandUseChangeImpactTemplate.clear()
            self.comboBoxLandUseChangeImpactTemplate.addItems(sorted(templateFiles))
            self.comboBoxLandUseChangeImpactTemplate.setEnabled(True)
            self.buttonLoadLandUseChangeImpactTemplate.setEnabled(True)
            
            # MainWindow TA Regional Economy dashboard templates
            self.main.comboBoxDescriptiveAnalysisTemplate.clear()
            self.main.comboBoxDescriptiveAnalysisTemplate.addItems(sorted(templateFiles))
            self.main.comboBoxDescriptiveAnalysisTemplate.setEnabled(True)
            
            self.main.comboBoxRegionalEconomicScenarioImpactTemplate.clear()
            self.main.comboBoxRegionalEconomicScenarioImpactTemplate.addItems(sorted(templateFiles))
            self.main.comboBoxRegionalEconomicScenarioImpactTemplate.setEnabled(True)
            
            self.main.comboBoxLandRequirementAnalysisTemplate.clear()
            self.main.comboBoxLandRequirementAnalysisTemplate.addItems(sorted(templateFiles))
            self.main.comboBoxLandRequirementAnalysisTemplate.setEnabled(True)
            
            self.main.comboBoxLandUseChangeImpactTemplate.clear()
            self.main.comboBoxLandUseChangeImpactTemplate.addItems(sorted(templateFiles))
            self.main.comboBoxLandUseChangeImpactTemplate.setEnabled(True)
            
            self.main.buttonProcessTARegionalEconomyTemplate.setEnabled(True)
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
            
            # RE templates
            self.comboBoxDescriptiveAnalysisTemplate.setDisabled(True)
            self.buttonLoadDescriptiveAnalysisTemplate.setDisabled(True)
            
            self.comboBoxRegionalEconomicScenarioImpactTemplate.setDisabled(True)
            self.buttonLoadRegionalEconomicScenarioImpactTemplate.setDisabled(True)
            
            self.comboBoxLandRequirementAnalysisTemplate.setDisabled(True)
            self.buttonLoadLandRequirementAnalysisTemplate.setDisabled(True)
            
            self.comboBoxLandUseChangeImpactTemplate.setDisabled(True)
            self.buttonLoadLandUseChangeImpactTemplate.setDisabled(True)
            
            # MainWindow TA Regional Economy dashboard templates
            self.main.comboBoxDescriptiveAnalysisTemplate.setDisabled(True)
            
            self.main.comboBoxRegionalEconomicScenarioImpactTemplate.setDisabled(True)
            
            self.main.comboBoxLandRequirementAnalysisTemplate.setDisabled(True)
            
            self.main.comboBoxLandUseChangeImpactTemplate.setDisabled(True)
        
    
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
                if csvNPVTable:
                    indexCsvNPVTable = self.comboBoxOCCCsvNPVTable.findText(csvNPVTable)
                    if indexCsvNPVTable != -1:
                        self.comboBoxOCCCsvNPVTable.setCurrentIndex(indexCsvNPVTable)              
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
                if csvProfitability:
                    indexCsvProfitability = self.comboBoxOCMCsvProfitability.findText(csvProfitability)
                    if indexCsvProfitability != -1:
                        self.comboBoxOCMCsvProfitability.setCurrentIndex(indexCsvProfitability)                    
                
                self.currentOpportunityCostMapTemplate = templateFile
                self.loadedOpportunityCostMapTemplate.setText(templateFile)
                self.comboBoxOpportunityCostMapTemplate.setCurrentIndex(self.comboBoxOpportunityCostMapTemplate.findText(templateFile))
                self.buttonSaveOpportunityCostMapTemplate.setEnabled(True)
            
            settings.endGroup()
            # /dialog
            
            settings.endGroup()
            # /tab
        elif tabName == 'Descriptive analysis':
            dialogsToLoad = (
                'DialogLumensTARegionalEconomySingleIODescriptiveAnalysis',
            )
            
            # start tab
            settings.beginGroup(tabName)
            
            # 'Descriptive analysis' tab widgets
            # start dialog
            settings.beginGroup('DialogLumensTARegionalEconomySingleIODescriptiveAnalysis')
            
            templateSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis'] = {}
            templateSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['intermediateConsumptionMatrix'] = intermediateConsumptionMatrix = settings.value('intermediateConsumptionMatrix')
            templateSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['valueAddedMatrix'] = valueAddedMatrix = settings.value('valueAddedMatrix')
            templateSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['finalConsumptionMatrix'] = finalConsumptionMatrix = settings.value('finalConsumptionMatrix')
            templateSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['valueAddedComponent'] = valueAddedComponent = settings.value('valueAddedComponent')
            templateSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['finalConsumptionComponent'] = finalConsumptionComponent = settings.value('finalConsumptionComponent')
            templateSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['listOfEconomicSector'] = listOfEconomicSector = settings.value('listOfEconomicSector')
            templateSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['labourRequirement'] = labourRequirement = settings.value('labourRequirement')
            templateSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['financialUnit'] = financialUnit = settings.value('financialUnit')
            templateSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['areaName'] = areaName = settings.value('areaName')
            templateSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['year'] = year = settings.value('year')
            if not returnTemplateSettings:
                if year:
                    self.spinBoxSinglePeriod.setValue(int(year))
                else:
                    self.spinBoxSinglePeriod.setValue(td.year)
                if intermediateConsumptionMatrix:
                    indexIntermediateConsumptionMatrix = self.comboBoxSingleIntermediateConsumptionMatrix.findText(intermediateConsumptionMatrix)
                    if indexIntermediateConsumptionMatrix != -1:
                        self.comboBoxSingleIntermediateConsumptionMatrix.setCurrentIndex(indexIntermediateConsumptionMatrix)
                if valueAddedMatrix:
                    indexValueAddedMatrix = self.comboBoxRegionalEconomicScenarioImpactFinalDemandChangeScenario.findText(valueAddedMatrix)
                    if indexValueAddedMatrix != -1:
                        self.comboBoxRegionalEconomicScenarioImpactFinalDemandChangeScenario.setCurrentIndex(indexValueAddedMatrix)
                if finalConsumptionMatrix:
                    indexFinalConsumptionMatrix = self.comboBoxRegionalEconomicScenarioImpactFinalDemandChangeScenario.findText(finalConsumptionMatrix)
                    if indexFinalConsumptionMatrix != -1:
                        self.comboBoxRegionalEconomicScenarioImpactFinalDemandChangeScenario.setCurrentIndex(indexFinalConsumptionMatrix)
                if valueAddedComponent:
                    indexValueAddedComponent = self.comboBoxRegionalEconomicScenarioImpactFinalDemandChangeScenario.findText(valueAddedComponent)
                    if indexValueAddedComponent != -1:
                        self.comboBoxRegionalEconomicScenarioImpactFinalDemandChangeScenario.setCurrentIndex(indexValueAddedComponent)
                if finalConsumptionComponent:
                    indexFinalConsumptionComponent = self.comboBoxRegionalEconomicScenarioImpactFinalDemandChangeScenario.findText(finalConsumptionComponent)
                    if indexFinalConsumptionComponent != -1:
                        self.comboBoxRegionalEconomicScenarioImpactFinalDemandChangeScenario.setCurrentIndex(indexFinalConsumptionComponent)
                if listOfEconomicSector:
                    indexListOfEconomicSector = self.comboBoxRegionalEconomicScenarioImpactFinalDemandChangeScenario.findText(listOfEconomicSector)
                    if indexListOfEconomicSector != -1:
                        self.comboBoxRegionalEconomicScenarioImpactFinalDemandChangeScenario.setCurrentIndex(indexListOfEconomicSector)
                if labourRequirement:
                    indexLabourRequirement = self.comboBoxRegionalEconomicScenarioImpactFinalDemandChangeScenario.findText(labourRequirement)
                    if indexLabourRequirement != -1:
                        self.comboBoxRegionalEconomicScenarioImpactFinalDemandChangeScenario.setCurrentIndex(indexLabourRequirement)
                if financialUnit:
                    self.lineEditOtherFinancialUnit.setText(financialUnit)
                else:
                    self.lineEditOtherFinancialUnit.setText('')
                if areaName:
                    self.lineEditOtherAreaName.setText(areaName)
                else:
                    self.lineEditOtherAreaName.setText('')
                
                self.currentDescriptiveAnalysisTemplate = templateFile
                self.loadedDescriptiveAnalysisTemplate.setText(templateFile)
                self.comboBoxDescriptiveAnalysisTemplate.setCurrentIndex(self.comboBoxDescriptiveAnalysisTemplate.findText(templateFile))
                self.buttonSaveDescriptiveAnalysisTemplate.setEnabled(True)
            
            settings.endGroup()
            # /dialog
            
            settings.endGroup()
            # /tab            
        elif tabName == 'Land requirement analysis':
            dialogsToLoad = (
                'DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis',
            )
            
            # start tab
            settings.beginGroup(tabName)
            
            # 'Land requirement analysis' tab widgets
            # start dialog
            settings.beginGroup('DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis')
            
            templateSettings['DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis'] = {}
            templateSettings['DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis']['landUseCover'] = landUseCover = settings.value('landUseCover')
            templateSettings['DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis']['landRequirementTable'] = landRequirementTable = settings.value('landRequirementTable')
            templateSettings['DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis']['descriptiveAnalysisOutput'] = descriptiveAnalysisOutput = settings.value('descriptiveAnalysisOutput')
            
            if not returnTemplateSettings:
                comboBoxLandRequirementAnalysisLandUseCover
                if landUseCover:
                    indexLandUseCover = self.comboBoxLandRequirementAnalysisLandUseCover.findText(landRequirementTable)
                    if indexLandUseCover != -1:
                        self.comboBoxLandRequirementAnalysisLandUseCover.setCurrentIndex(indexLandUseCover)
                if landRequirementTable:
                    indexLandRequirementTable = self.comboBoxLandRequirementAnalysisLookupTable.findText(landRequirementTable)
                    if indexLandRequirementTable != -1:
                        self.comboBoxLandRequirementAnalysisLookupTable.setCurrentIndex(indexLandRequirementTable)
                if descriptiveAnalysisOutput and os.path.exists(descriptiveAnalysisOutput):
                    self.lineEditLandRequirementAnalysisDescriptiveOutput.setText(csvProfitability)
                else:
                    self.lineEditLandRequirementAnalysisDescriptiveOutput.setText('')
                
                self.currentLandRequirementAnalysisTemplate = templateFile
                self.loadedLandRequirementAnalysisTemplate.setText(templateFile)
                self.comboBoxLandRequirementAnalysisTemplate.setCurrentIndex(self.comboBoxLandRequirementAnalysisTemplate.findText(templateFile))
                self.buttonSaveLandRequirementAnalysisTemplate.setEnabled(True)
            
            settings.endGroup()
            # /dialog
            
            settings.endGroup()
            # /tab            
        elif tabName == 'Regional economy scenario':
            dialogsToLoad = (
                'DialogLumensTARegionalEconomyScenario',
            )
            
            # start tab
            settings.beginGroup(tabName)
            
            # 'Regional economy scenario' tab widgets
            # start dialog
            settings.beginGroup('DialogLumensTARegionalEconomyScenario')
            
            templateSettings['DialogLumensTARegionalEconomyScenario'] = {}
            templateSettings['DialogLumensTARegionalEconomyScenario']['landRequirement'] = landRequirement = settings.value('landRequirement')
            templateSettings['DialogLumensTARegionalEconomyScenario']['finalDemandChangeScenario'] = finalDemandChangeScenario = settings.value('finalDemandChangeScenario')
            templateSettings['DialogLumensTARegionalEconomyScenario']['gdpChangeScenario'] = gdpChangeScenario = settings.value('gdpChangeScenario')
            
            if not returnTemplateSettings:
                if landRequirement and os.path.exists(landRequirement):
                    self.lineEditRegionalEconomicScenarioLandRequirement.setText(landRequirement)
                else:
                    self.lineEditRegionalEconomicScenarioLandRequirement.setText('')
                if finalDemandChangeScenario:
                    indexFinalDemandChangeScenario = self.comboBoxRegionalEconomicScenarioImpactFinalDemandChangeScenario.findText(finalDemandChangeScenario)
                    if indexFinalDemandChangeScenario != -1:
                        self.comboBoxRegionalEconomicScenarioImpactFinalDemandChangeScenario.setCurrentIndex(indexFinalDemandChangeScenario)
                if gdpChangeScenario:
                    indexGdpChangeScenario = self.comboBoxRegionalEconomicScenarioImpactGDPChangeScenario.findText(gdpChangeScenario)
                    if indexLandUseCover != -1:
                        self.comboBoxRegionalEconomicScenarioImpactGDPChangeScenario.setCurrentIndex(indexGdpChangeScenario)         
                    
                self.currentRegionalEconomicScenarioImpactTemplate = templateFile
                self.loadedRegionalEconomicScenarioImpactTemplate.setText(templateFile)
                self.comboBoxRegionalEconomicScenarioImpactTemplate.setCurrentIndex(self.comboBoxRegionalEconomicScenarioImpactTemplate.findText(templateFile))
                self.buttonSaveRegionalEconomicScenarioImpactTemplate.setEnabled(True)
            
            settings.endGroup()
            # /dialog
            
            settings.endGroup()
            # /tab            
        elif tabName == 'Land use scenario':
            dialogsToLoad = (
                'DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis',
            ) 
        
            # start tab
            settings.beginGroup(tabName)
            
            # 'Land use scenario' tab widgets
            # start dialog
            settings.beginGroup('DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis')
            
            templateSettings['DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis'] = {}
            templateSettings['DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis']['landRequirement'] = landRequirement = settings.value('landRequirement')
            templateSettings['DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis']['landUseCover'] = landUseCover = settings.value('landUseCover')
            
            if not returnTemplateSettings:
                if landRequirement and os.path.exists(landRequirement):
                    self.lineEditLandUseChangeLandRequirement.setText(landRequirement)
                else:
                    self.lineEditLandUseChangeLandRequirement.setText('')
                if landUseCover:
                    indexLandUseCover = self.comboBoxSelectLandUseChangeMap.findText(landUseCover)
                    if indexLandUseCover != -1:
                        self.comboBoxSelectLandUseChangeMap.setCurrentIndex(indexLandUseCover)    
                
                self.currentLandUseChangeImpactTemplate = templateFile
                self.loadedLandUseChangeImpactTemplate.setText(templateFile)
                self.comboBoxLandUseChangeImpactTemplate.setCurrentIndex(self.comboBoxLandUseChangeImpactTemplate.findText(templateFile))
                self.buttonSaveLandUseChangeImpactTemplate.setEnabled(True)
            
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
        elif tabName == 'Descriptive analysis':
            dialogsToSave = (
                'DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis',
            )
        elif tabName == 'Land requirement analysis':
            dialogsToSave = (
                'DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis',
            )
        elif tabName == 'Regional economy scenario':
            dialogsToSave = (
                'DialogLumensTARegionalEconomyScenario',
            )
        elif tabName == 'Land use scenario':
            dialogsToSave = (
                'DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis',
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
                'Load Existing Configuration',
                'The configuration you are about to save matches an existing template.\nDo you want to load \'{0}\' instead?'.format(duplicateTemplate),
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
                elif tabName == 'Descriptive analysis':
                    self.handlerLoadDescriptiveAnalysisTemplate(duplicateTemplate)
                elif tabName == 'Land requirement analysis':
                    self.handlerLoadLandRequirementAnalysisTemplate(duplicateTemplate)
                elif tabName == 'Regional economy scenario':
                    self.handlerLoadRegionalEconomicScenarioImpactTemplate(duplicateTemplate)
                elif tabName == 'Land use scenario':
                    self.handlerLoadLandUseChangeImpactTemplate(duplicateTemplate)
                    
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
            elif tabName == 'Descriptive analysis':
                dialogsToSave = (
                    'DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis',
                )
            elif tabName == 'Land requirement analysis':
                dialogsToSave = (
                    'DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis',
                )
            elif tabName == 'Regional economy scenario':
                dialogsToSave = (
                    'DialogLumensTARegionalEconomyScenario',
                )
            elif tabName == 'Land use scenario':
                dialogsToSave = (
                    'DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis',
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
        self.dialogTitle = 'TA'
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
        self.buttonSelectOCCOutputOpportunityCostDatabase.clicked.connect(self.handlerSelectOCCOutputOpportunityCostDatabase)
        self.buttonSelectOCCOutputOpportunityCostReport.clicked.connect(self.handlerSelectOCCOutputOpportunityCostReport)
        self.buttonProcessOpportunityCostCurve.clicked.connect(self.handlerProcessOpportunityCostCurve)
        self.buttonHelpTAOpportunityCostCurve.clicked.connect(lambda:self.handlerDialogHelp('TA'))
        self.buttonLoadOpportunityCostCurveTemplate.clicked.connect(self.handlerLoadOpportunityCostCurveTemplate)
        self.buttonSaveOpportunityCostCurveTemplate.clicked.connect(self.handlerSaveOpportunityCostCurveTemplate)
        self.buttonSaveAsOpportunityCostCurveTemplate.clicked.connect(self.handlerSaveAsOpportunityCostCurveTemplate)
        
        # 'Opportunity Cost Map' tab buttons
        self.buttonProcessOpportunityCostMap.clicked.connect(self.handlerProcessOpportunityCostMap)
        self.buttonHelpTAOpportunityCostMap.clicked.connect(lambda:self.handlerDialogHelp('TA'))
        self.buttonLoadOpportunityCostMapTemplate.clicked.connect(self.handlerLoadOpportunityCostMapTemplate)
        self.buttonSaveOpportunityCostMapTemplate.clicked.connect(self.handlerSaveOpportunityCostMapTemplate)
        self.buttonSaveAsOpportunityCostMapTemplate.clicked.connect(self.handlerSaveAsOpportunityCostMapTemplate)
        
        # 'Descriptive Analysis' tab buttons
        self.buttonProcessDescriptiveAnalysis.clicked.connect(self.handlerProcessDescriptiveAnalysis)
        
        # 'Land Requirement Analysis' tab buttons
        self.buttonSelectLandRequirementAnalysisDescriptiveOutput.clicked.connect(self.handlerSelectLandRequirementAnalysisDescriptiveOutput)
        self.buttonProcessLandRequirementAnalysis.clicked.connect(self.handlerProcessLandRequirementAnalysis)
        
        # 'Regional Economy Scenario' tab buttons
        self.buttonSelectRegionalEconomicScenarioLandRequirement.clicked.connect(self.handlerSelectRegionalEconomicScenarioLandRequirement)
        self.buttonProcessRegionalEconomicScenarioImpact.clicked.connect(self.handlerProcessRegionalEconomicScenarioImpact)
        
        # 'Land Use Scenario' tab buttons
        self.buttonSelectLandUseChangeLandRequirement.clicked.connect(self.handlerSelectLandUseChangeLandRequirement)
        self.buttonProcessLandUseChangeImpact.clicked.connect(self.handlerProcessLandUseChangeImpact)
        
    
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
            width: 200px;
        }
        QTabBar::tab:selected, QTabBar::tab:hover {
            background-color: rgb(249, 237, 243);
            font: bold;
        }
        """        
        self.tabWidgetOpportunityCost.setStyleSheet(OpportunityCostTabWidgetStylesheet)
        
        self.tabAbacusOpportunityCost = QtGui.QWidget()
        self.tabOpportunityCostCurve = QtGui.QWidget()
        self.tabOpportunityCostMap = QtGui.QWidget()
        
        # self.tabWidgetOpportunityCost.addTab(self.tabAbacusOpportunityCost, 'Abacus Opportunity Cost')
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
        self.groupBoxOCCParameters = QtGui.QGroupBox('Parameterization')
        self.layoutGroupBoxOCCParameters = QtGui.QVBoxLayout()
        self.layoutGroupBoxOCCParameters.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxOCCParameters.setLayout(self.layoutGroupBoxOCCParameters)
        self.layoutOCCParametersInfo = QtGui.QVBoxLayout()
        self.layoutOCCParameters = QtGui.QGridLayout()
        self.layoutGroupBoxOCCParameters.addLayout(self.layoutOCCParametersInfo)
        self.layoutGroupBoxOCCParameters.addLayout(self.layoutOCCParameters)
        
        self.labelOCCParametersInfo = QtGui.QLabel()
        self.labelOCCParametersInfo.setText('\n')
        self.layoutOCCParametersInfo.addWidget(self.labelOCCParametersInfo)
        
        self.labelOCCCsvNPVTable = QtGui.QLabel(parent)
        self.labelOCCCsvNPVTable.setText('Profitability lookup table:')
        self.layoutOCCParameters.addWidget(self.labelOCCCsvNPVTable, 0, 0)
        
        self.comboBoxOCCCsvNPVTable = QtGui.QComboBox()
        self.comboBoxOCCCsvNPVTable.setDisabled(True)
        self.layoutOCCParameters.addWidget(self.comboBoxOCCCsvNPVTable, 0, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxOCCCsvNPVTable)
        
        self.labelOCCCostThreshold = QtGui.QLabel()
        self.labelOCCCostThreshold.setText('Cost threshold:')
        self.layoutOCCParameters.addWidget(self.labelOCCCostThreshold, 1, 0)
        
        self.spinBoxOCCCostThreshold = QtGui.QSpinBox()
        self.spinBoxOCCCostThreshold.setValue(5)
        self.layoutOCCParameters.addWidget(self.spinBoxOCCCostThreshold, 1, 1)
        
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
        self.groupBoxOpportunityCostCurveTemplate = QtGui.QGroupBox('Configuration')
        self.layoutGroupBoxOpportunityCostCurveTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxOpportunityCostCurveTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxOpportunityCostCurveTemplate.setLayout(self.layoutGroupBoxOpportunityCostCurveTemplate)
        self.layoutOpportunityCostCurveTemplateInfo = QtGui.QVBoxLayout()
        self.layoutOpportunityCostCurveTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxOpportunityCostCurveTemplate.addLayout(self.layoutOpportunityCostCurveTemplateInfo)
        self.layoutGroupBoxOpportunityCostCurveTemplate.addLayout(self.layoutOpportunityCostCurveTemplate)
        
        self.labelLoadedOpportunityCostCurveTemplate = QtGui.QLabel()
        self.labelLoadedOpportunityCostCurveTemplate.setText('Loaded configuration:')
        self.layoutOpportunityCostCurveTemplate.addWidget(self.labelLoadedOpportunityCostCurveTemplate, 0, 0)
        
        self.loadedOpportunityCostCurveTemplate = QtGui.QLabel()
        self.loadedOpportunityCostCurveTemplate.setText('<None>')
        self.layoutOpportunityCostCurveTemplate.addWidget(self.loadedOpportunityCostCurveTemplate, 0, 1)
        
        self.labelOpportunityCostCurveTemplate = QtGui.QLabel()
        self.labelOpportunityCostCurveTemplate.setText('Name:')
        self.layoutOpportunityCostCurveTemplate.addWidget(self.labelOpportunityCostCurveTemplate, 1, 0)
        
        self.comboBoxOpportunityCostCurveTemplate = QtGui.QComboBox()
        self.comboBoxOpportunityCostCurveTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxOpportunityCostCurveTemplate.setDisabled(True)
        self.comboBoxOpportunityCostCurveTemplate.addItem('No configuration found')
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
        self.groupBoxOCMParameters = QtGui.QGroupBox('Parameterization')
        self.layoutGroupBoxOCMParameters = QtGui.QVBoxLayout()
        self.layoutGroupBoxOCMParameters.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxOCMParameters.setLayout(self.layoutGroupBoxOCMParameters)
        self.layoutOCMParametersInfo = QtGui.QVBoxLayout()
        self.layoutOCMParameters = QtGui.QGridLayout()
        self.layoutGroupBoxOCMParameters.addLayout(self.layoutOCMParametersInfo)
        self.layoutGroupBoxOCMParameters.addLayout(self.layoutOCMParameters)
        
        self.labelOCMParametersInfo = QtGui.QLabel()
        self.labelOCMParametersInfo.setText('\n')
        self.layoutOCMParametersInfo.addWidget(self.labelOCMParametersInfo)
        
        self.labelOCMCsvProfitability = QtGui.QLabel(parent)
        self.labelOCMCsvProfitability.setText('Profitability lookup table:')
        self.layoutOCMParameters.addWidget(self.labelOCMCsvProfitability, 0, 0)
        
        self.comboBoxOCMCsvProfitability = QtGui.QComboBox()
        self.comboBoxOCMCsvProfitability.setDisabled(True)
        self.layoutOCMParameters.addWidget(self.comboBoxOCMCsvProfitability, 0, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxOCMCsvProfitability)
        
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
        self.groupBoxOpportunityCostMapTemplate = QtGui.QGroupBox('Configuration')
        self.layoutGroupBoxOpportunityCostMapTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxOpportunityCostMapTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxOpportunityCostMapTemplate.setLayout(self.layoutGroupBoxOpportunityCostMapTemplate)
        self.layoutOpportunityCostMapTemplateInfo = QtGui.QVBoxLayout()
        self.layoutOpportunityCostMapTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxOpportunityCostMapTemplate.addLayout(self.layoutOpportunityCostMapTemplateInfo)
        self.layoutGroupBoxOpportunityCostMapTemplate.addLayout(self.layoutOpportunityCostMapTemplate)
        
        self.labelLoadedOpportunityCostMapTemplate = QtGui.QLabel()
        self.labelLoadedOpportunityCostMapTemplate.setText('Loaded configuration:')
        self.layoutOpportunityCostMapTemplate.addWidget(self.labelLoadedOpportunityCostMapTemplate, 0, 0)
        
        self.loadedOpportunityCostMapTemplate = QtGui.QLabel()
        self.loadedOpportunityCostMapTemplate.setText('<None>')
        self.layoutOpportunityCostMapTemplate.addWidget(self.loadedOpportunityCostMapTemplate, 0, 1)
        
        self.labelOpportunityCostMapTemplate = QtGui.QLabel()
        self.labelOpportunityCostMapTemplate.setText('Name:')
        self.layoutOpportunityCostMapTemplate.addWidget(self.labelOpportunityCostMapTemplate, 1, 0)
        
        self.comboBoxOpportunityCostMapTemplate = QtGui.QComboBox()
        self.comboBoxOpportunityCostMapTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxOpportunityCostMapTemplate.setDisabled(True)
        self.comboBoxOpportunityCostMapTemplate.addItem('No configuration found')
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
            width: 200px;
        }
        QTabBar::tab:selected, QTabBar::tab:hover {
            background-color: rgb(249, 237, 243);
            font: bold;
        }
        """
        self.tabWidgetRegionalEconomy.setStyleSheet(RegionalEconomyTabWidgetStylesheet)

        # self.tabInputOutputTable = QtGui.QWidget()
        self.tabDescriptiveAnalysis = QtGui.QWidget()
        self.tabRegionalEconomicScenarioImpact = QtGui.QWidget()
        self.tabLandRequirementAnalysis = QtGui.QWidget()
        self.tabLandUseChangeImpact = QtGui.QWidget()
        
        # self.tabWidgetRegionalEconomy.addTab(self.tabInputOutputTable, 'Input-Output Table')
        self.tabWidgetRegionalEconomy.addTab(self.tabDescriptiveAnalysis, 'Descriptive analysis')
        self.tabWidgetRegionalEconomy.addTab(self.tabLandRequirementAnalysis, 'Land requirement analysis')
        self.tabWidgetRegionalEconomy.addTab(self.tabRegionalEconomicScenarioImpact, 'Regional economy scenario')
        self.tabWidgetRegionalEconomy.addTab(self.tabLandUseChangeImpact, 'Land use scenario')
        
        self.layoutTabRegionalEconomy.addWidget(self.tabWidgetRegionalEconomy)
      
        # self.layoutTabInputOutputTable = QtGui.QGridLayout()
        self.layoutTabDescriptiveAnalysis = QtGui.QGridLayout()
        self.layoutTabRegionalEconomicScenarioImpact = QtGui.QGridLayout()
        self.layoutTabLandRequirementAnalysis = QtGui.QGridLayout()
        self.layoutTabLandUseChangeImpact = QtGui.QGridLayout()
      
        # self.tabInputOutputTable.setLayout(self.layoutTabInputOutputTable)
        self.tabDescriptiveAnalysis.setLayout(self.layoutTabDescriptiveAnalysis)
        self.tabRegionalEconomicScenarioImpact.setLayout(self.layoutTabRegionalEconomicScenarioImpact)
        self.tabLandRequirementAnalysis.setLayout(self.layoutTabLandRequirementAnalysis)
        self.tabLandUseChangeImpact.setLayout(self.layoutTabLandUseChangeImpact)
        
        #***********************************************************
        # Setup 'Descriptive Analysis' tab
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
        self.groupBoxSinglePeriod = QtGui.QGroupBox('Initialize')
        self.layoutGroupBoxSinglePeriod = QtGui.QVBoxLayout()
        self.layoutGroupBoxSinglePeriod.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxSinglePeriod.setLayout(self.layoutGroupBoxSinglePeriod)
        self.layoutSinglePeriodInfo = QtGui.QVBoxLayout()
        self.layoutSinglePeriod = QtGui.QGridLayout()
        self.layoutGroupBoxSinglePeriod.addLayout(self.layoutSinglePeriodInfo)
        self.layoutGroupBoxSinglePeriod.addLayout(self.layoutSinglePeriod)
        
        self.labelSinglePeriodInfo = QtGui.QLabel()
        self.labelSinglePeriodInfo.setText('\n')
        self.layoutSinglePeriodInfo.addWidget(self.labelSinglePeriodInfo)
        
        self.labelSingleIntermediateConsumptionMatrix = QtGui.QLabel()
        self.labelSingleIntermediateConsumptionMatrix.setText('Intermediate consumption matrix:')
        self.layoutSinglePeriod.addWidget(self.labelSingleIntermediateConsumptionMatrix, 0, 0)
        
        self.comboBoxSingleIntermediateConsumptionMatrix = QtGui.QComboBox()
        self.comboBoxSingleIntermediateConsumptionMatrix.setDisabled(True)
        self.layoutSinglePeriod.addWidget(self.comboBoxSingleIntermediateConsumptionMatrix, 0, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxSingleIntermediateConsumptionMatrix)
        
        self.labelSingleValueAddedMatrix = QtGui.QLabel()
        self.labelSingleValueAddedMatrix.setText('Value added matrix:')
        self.layoutSinglePeriod.addWidget(self.labelSingleValueAddedMatrix, 1, 0)
        
        self.comboBoxSingleValueAddedMatrix = QtGui.QComboBox()
        self.comboBoxSingleValueAddedMatrix.setDisabled(True)
        self.layoutSinglePeriod.addWidget(self.comboBoxSingleValueAddedMatrix, 1, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxSingleValueAddedMatrix)
        
        self.labelSingleFinalConsumptionMatrix = QtGui.QLabel()
        self.labelSingleFinalConsumptionMatrix.setText('Final consumption matrix:')
        self.layoutSinglePeriod.addWidget(self.labelSingleFinalConsumptionMatrix, 2, 0)
        
        self.comboBoxSingleFinalConsumptionMatrix = QtGui.QComboBox()
        self.comboBoxSingleFinalConsumptionMatrix.setDisabled(True)
        self.layoutSinglePeriod.addWidget(self.comboBoxSingleFinalConsumptionMatrix, 2, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxSingleFinalConsumptionMatrix)
        
        self.labelOtherValueAddedComponent = QtGui.QLabel()
        self.labelOtherValueAddedComponent.setText('Value added component:')
        self.layoutSinglePeriod.addWidget(self.labelOtherValueAddedComponent, 3, 0)
        
        self.comboBoxOtherValueAddedComponent = QtGui.QComboBox()
        self.comboBoxOtherValueAddedComponent.setDisabled(True)
        self.layoutSinglePeriod.addWidget(self.comboBoxOtherValueAddedComponent, 3, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxOtherValueAddedComponent)
        
        self.labelOtherFinalConsumptionComponent = QtGui.QLabel()
        self.labelOtherFinalConsumptionComponent.setText('Final consumption component:')
        self.layoutSinglePeriod.addWidget(self.labelOtherFinalConsumptionComponent, 4, 0)
        
        self.comboBoxOtherFinalConsumptionComponent = QtGui.QComboBox()
        self.comboBoxOtherFinalConsumptionComponent.setDisabled(True)
        self.layoutSinglePeriod.addWidget(self.comboBoxOtherFinalConsumptionComponent, 4, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxOtherFinalConsumptionComponent)
        
        self.labelOtherListOfEconomicSector = QtGui.QLabel()
        self.labelOtherListOfEconomicSector.setText('List of economic sector:')
        self.layoutSinglePeriod.addWidget(self.labelOtherListOfEconomicSector, 5, 0)
        
        self.comboBoxOtherListOfEconomicSector = QtGui.QComboBox()
        self.comboBoxOtherListOfEconomicSector.setDisabled(True)
        self.layoutSinglePeriod.addWidget(self.comboBoxOtherListOfEconomicSector, 5, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxOtherListOfEconomicSector)

        self.labelSingleLabourRequirement = QtGui.QLabel()
        self.labelSingleLabourRequirement.setText('Labour requirement:')
        self.layoutSinglePeriod.addWidget(self.labelSingleLabourRequirement, 6, 0)
        
        self.comboBoxSingleLabourRequirement = QtGui.QComboBox()
        self.comboBoxSingleLabourRequirement.setDisabled(True)
        self.layoutSinglePeriod.addWidget(self.comboBoxSingleLabourRequirement, 6, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxSingleLabourRequirement)
        
        self.labelOtherFinancialUnit = QtGui.QLabel()
        self.labelOtherFinancialUnit.setText('Financial &unit:')
        self.layoutSinglePeriod.addWidget(self.labelOtherFinancialUnit, 7, 0)
        
        self.lineEditOtherFinancialUnit = QtGui.QLineEdit()
        self.lineEditOtherFinancialUnit.setText('Million Rupiah')
        self.layoutSinglePeriod.addWidget(self.lineEditOtherFinancialUnit, 7, 1)
        self.labelOtherFinancialUnit.setBuddy(self.lineEditOtherFinancialUnit)
        
        self.labelOtherAreaName = QtGui.QLabel()
        self.labelOtherAreaName.setText('&Area name:')
        self.layoutSinglePeriod.addWidget(self.labelOtherAreaName, 8, 0)
        
        self.lineEditOtherAreaName = QtGui.QLineEdit()
        self.lineEditOtherAreaName.setText('area')
        self.layoutSinglePeriod.addWidget(self.lineEditOtherAreaName, 8, 1)
        self.labelOtherAreaName.setBuddy(self.lineEditOtherAreaName)
        
        self.labelSinglePeriod = QtGui.QLabel()
        self.labelSinglePeriod.setText('&Year:')
        self.layoutSinglePeriod.addWidget(self.labelSinglePeriod, 9, 0)
        
        self.spinBoxSinglePeriod = QtGui.QSpinBox()
        self.spinBoxSinglePeriod.setRange(1, 9999)
        td = datetime.date.today()
        self.spinBoxSinglePeriod.setValue(td.year)
        self.layoutSinglePeriod.addWidget(self.spinBoxSinglePeriod, 9, 1)
        self.labelSinglePeriod.setBuddy(self.spinBoxSinglePeriod)        
        
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
        self.groupBoxDescriptiveAnalysisTemplate = QtGui.QGroupBox('Configuration')
        self.layoutGroupBoxDescriptiveAnalysisTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxDescriptiveAnalysisTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxDescriptiveAnalysisTemplate.setLayout(self.layoutGroupBoxDescriptiveAnalysisTemplate)
        self.layoutDescriptiveAnalysisTemplateInfo = QtGui.QVBoxLayout()
        self.layoutDescriptiveAnalysisTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxDescriptiveAnalysisTemplate.addLayout(self.layoutDescriptiveAnalysisTemplateInfo)
        self.layoutGroupBoxDescriptiveAnalysisTemplate.addLayout(self.layoutDescriptiveAnalysisTemplate)
        
        self.labelLoadedDescriptiveAnalysisTemplate = QtGui.QLabel()
        self.labelLoadedDescriptiveAnalysisTemplate.setText('Loaded configuration:')
        self.layoutDescriptiveAnalysisTemplate.addWidget(self.labelLoadedDescriptiveAnalysisTemplate, 0, 0)
        
        self.loadedDescriptiveAnalysisTemplate = QtGui.QLabel()
        self.loadedDescriptiveAnalysisTemplate.setText('<None>')
        self.layoutDescriptiveAnalysisTemplate.addWidget(self.loadedDescriptiveAnalysisTemplate, 0, 1)
        
        self.labelDescriptiveAnalysisTemplate = QtGui.QLabel()
        self.labelDescriptiveAnalysisTemplate.setText('Name:')
        self.layoutDescriptiveAnalysisTemplate.addWidget(self.labelDescriptiveAnalysisTemplate, 1, 0)
        
        self.comboBoxDescriptiveAnalysisTemplate = QtGui.QComboBox()
        self.comboBoxDescriptiveAnalysisTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxDescriptiveAnalysisTemplate.setDisabled(True)
        self.comboBoxDescriptiveAnalysisTemplate.addItem('No configuration found')
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
        self.layoutContentDescriptiveAnalysis.addLayout(self.layoutButtonDescriptiveAnalysis, 3, 0, 1, 2, QtCore.Qt.AlignRight)
        self.layoutContentDescriptiveAnalysis.addWidget(self.groupBoxDescriptiveAnalysisTemplate, 0, 1, 3, 1)
        self.layoutContentDescriptiveAnalysis.setColumnStretch(0, 3)
        self.layoutContentDescriptiveAnalysis.setColumnStretch(1, 1) # Smaller template column
        
        
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
        self.groupBoxLandRequirementAnalysisParameters = QtGui.QGroupBox('Parameterization')
        self.layoutGroupBoxLandRequirementAnalysisParameters = QtGui.QVBoxLayout()
        self.layoutGroupBoxLandRequirementAnalysisParameters.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLandRequirementAnalysisParameters.setLayout(self.layoutGroupBoxLandRequirementAnalysisParameters)
        self.layoutLandRequirementAnalysisParametersInfo = QtGui.QVBoxLayout()
        self.layoutLandRequirementAnalysisParameters = QtGui.QGridLayout()
        self.layoutGroupBoxLandRequirementAnalysisParameters.addLayout(self.layoutLandRequirementAnalysisParametersInfo)
        self.layoutGroupBoxLandRequirementAnalysisParameters.addLayout(self.layoutLandRequirementAnalysisParameters)
        
        self.labelLandRequirementAnalysisParametersInfo = QtGui.QLabel()
        self.labelLandRequirementAnalysisParametersInfo.setText('\n')
        self.layoutLandRequirementAnalysisParametersInfo.addWidget(self.labelLandRequirementAnalysisParametersInfo)
        
        self.labelLandRequirementAnalysisLandUseCover = QtGui.QLabel()
        self.labelLandRequirementAnalysisLandUseCover.setText('Current land cover map:')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.labelLandRequirementAnalysisLandUseCover, 0, 0)
        
        self.comboBoxLandRequirementAnalysisLandUseCover = QtGui.QComboBox()
        self.comboBoxLandRequirementAnalysisLandUseCover.setDisabled(True)
        self.layoutLandRequirementAnalysisParameters.addWidget(self.comboBoxLandRequirementAnalysisLandUseCover, 0, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataLandUseCover, self.comboBoxLandRequirementAnalysisLandUseCover)
        
        self.labelLandRequirementAnalysisLookupTable = QtGui.QLabel()
        self.labelLandRequirementAnalysisLookupTable.setText('Land requirement lookup table:')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.labelLandRequirementAnalysisLookupTable, 1, 0)
        
        self.comboBoxLandRequirementAnalysisLookupTable = QtGui.QComboBox()
        self.comboBoxLandRequirementAnalysisLookupTable.setDisabled(True)
        self.layoutLandRequirementAnalysisParameters.addWidget(self.comboBoxLandRequirementAnalysisLookupTable, 1, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxLandRequirementAnalysisLookupTable)
        
        self.labelLandRequirementAnalysisDescriptiveOutput = QtGui.QLabel()
        self.labelLandRequirementAnalysisDescriptiveOutput.setText('Descriptive analysis output:')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.labelLandRequirementAnalysisDescriptiveOutput, 2, 0)
        
        self.lineEditLandRequirementAnalysisDescriptiveOutput = QtGui.QLineEdit()
        self.lineEditLandRequirementAnalysisDescriptiveOutput.setReadOnly(True)
        self.layoutLandRequirementAnalysisParameters.addWidget(self.lineEditLandRequirementAnalysisDescriptiveOutput, 2, 1)
        
        self.buttonSelectLandRequirementAnalysisDescriptiveOutput = QtGui.QPushButton()
        self.buttonSelectLandRequirementAnalysisDescriptiveOutput.setText('&Browse')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.buttonSelectLandRequirementAnalysisDescriptiveOutput, 2, 2)
        
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
        self.groupBoxLandRequirementAnalysisTemplate = QtGui.QGroupBox('Configuration')
        self.layoutGroupBoxLandRequirementAnalysisTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxLandRequirementAnalysisTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLandRequirementAnalysisTemplate.setLayout(self.layoutGroupBoxLandRequirementAnalysisTemplate)
        self.layoutLandRequirementAnalysisTemplateInfo = QtGui.QVBoxLayout()
        self.layoutLandRequirementAnalysisTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxLandRequirementAnalysisTemplate.addLayout(self.layoutLandRequirementAnalysisTemplateInfo)
        self.layoutGroupBoxLandRequirementAnalysisTemplate.addLayout(self.layoutLandRequirementAnalysisTemplate)
        
        self.labelLoadedLandRequirementAnalysisTemplate = QtGui.QLabel()
        self.labelLoadedLandRequirementAnalysisTemplate.setText('Loaded configuration:')
        self.layoutLandRequirementAnalysisTemplate.addWidget(self.labelLoadedLandRequirementAnalysisTemplate, 0, 0)
        
        self.loadedLandRequirementAnalysisTemplate = QtGui.QLabel()
        self.loadedLandRequirementAnalysisTemplate.setText('<None>')
        self.layoutLandRequirementAnalysisTemplate.addWidget(self.loadedLandRequirementAnalysisTemplate, 0, 1)
        
        self.labelLandRequirementAnalysisTemplate = QtGui.QLabel()
        self.labelLandRequirementAnalysisTemplate.setText('Name:')
        self.layoutLandRequirementAnalysisTemplate.addWidget(self.labelLandRequirementAnalysisTemplate, 1, 0)
        
        self.comboBoxLandRequirementAnalysisTemplate = QtGui.QComboBox()
        self.comboBoxLandRequirementAnalysisTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxLandRequirementAnalysisTemplate.setDisabled(True)
        self.comboBoxLandRequirementAnalysisTemplate.addItem('No configuration found')
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
        # Setup 'Regional Economic Scenario' tab
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
        self.labelRegionalEconomicScenarioImpactTypeInfo.setText('\n')
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.labelRegionalEconomicScenarioImpactTypeInfo)        
        
        self.labelRegionalEconomicScenarioLandRequirement = QtGui.QLabel()
        self.labelRegionalEconomicScenarioLandRequirement.setText('Land requirement:')
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.labelRegionalEconomicScenarioLandRequirement, 0, 0)
        
        self.lineEditRegionalEconomicScenarioLandRequirement = QtGui.QLineEdit()
        self.lineEditRegionalEconomicScenarioLandRequirement.setReadOnly(True)
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.lineEditRegionalEconomicScenarioLandRequirement, 0, 1)
        
        self.buttonSelectRegionalEconomicScenarioLandRequirement = QtGui.QPushButton()
        self.buttonSelectRegionalEconomicScenarioLandRequirement.setText('&Browse')
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.buttonSelectRegionalEconomicScenarioLandRequirement, 0, 2)        
        
        self.checkBoxRegionalEconomicScenarioImpactFinalDemand = QtGui.QCheckBox('Final demand scenario')
        self.checkBoxRegionalEconomicScenarioImpactFinalDemand.setChecked(True)
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.checkBoxRegionalEconomicScenarioImpactFinalDemand, 1, 0)
        
        self.labelRegionalEconomicScenarioImpactFinalDemandChangeScenario = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactFinalDemandChangeScenario.setText('Final demand lookup table:')
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.labelRegionalEconomicScenarioImpactFinalDemandChangeScenario, 2, 0)
        
        self.comboBoxRegionalEconomicScenarioImpactFinalDemandChangeScenario = QtGui.QComboBox()
        self.comboBoxRegionalEconomicScenarioImpactFinalDemandChangeScenario.setDisabled(True)
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.comboBoxRegionalEconomicScenarioImpactFinalDemandChangeScenario, 2, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxRegionalEconomicScenarioImpactFinalDemandChangeScenario)
        
        self.checkBoxRegionalEconomicScenarioImpactGDP = QtGui.QCheckBox('GDP Scenario')
        self.checkBoxRegionalEconomicScenarioImpactGDP.setChecked(False)
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.checkBoxRegionalEconomicScenarioImpactGDP, 3, 0)
        
        self.labelRegionalEconomicScenarioImpactGDPChangeScenario = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactGDPChangeScenario.setText('GDP lookup table:')
        self.labelRegionalEconomicScenarioImpactGDPChangeScenario.setDisabled(True)
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.labelRegionalEconomicScenarioImpactGDPChangeScenario, 4, 0)
        
        self.comboBoxRegionalEconomicScenarioImpactGDPChangeScenario = QtGui.QComboBox()
        self.comboBoxRegionalEconomicScenarioImpactGDPChangeScenario.setDisabled(True)
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.comboBoxRegionalEconomicScenarioImpactGDPChangeScenario, 4, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxRegionalEconomicScenarioImpactGDPChangeScenario)
        
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
        self.groupBoxRegionalEconomicScenarioImpactTemplate = QtGui.QGroupBox('Configuration')
        self.layoutGroupBoxRegionalEconomicScenarioImpactTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxRegionalEconomicScenarioImpactTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxRegionalEconomicScenarioImpactTemplate.setLayout(self.layoutGroupBoxRegionalEconomicScenarioImpactTemplate)
        self.layoutRegionalEconomicScenarioImpactTemplateInfo = QtGui.QVBoxLayout()
        self.layoutRegionalEconomicScenarioImpactTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxRegionalEconomicScenarioImpactTemplate.addLayout(self.layoutRegionalEconomicScenarioImpactTemplateInfo)
        self.layoutGroupBoxRegionalEconomicScenarioImpactTemplate.addLayout(self.layoutRegionalEconomicScenarioImpactTemplate)
        
        self.labelLoadedRegionalEconomicScenarioImpactTemplate = QtGui.QLabel()
        self.labelLoadedRegionalEconomicScenarioImpactTemplate.setText('Loaded configuration:')
        self.layoutRegionalEconomicScenarioImpactTemplate.addWidget(self.labelLoadedRegionalEconomicScenarioImpactTemplate, 0, 0)
        
        self.loadedRegionalEconomicScenarioImpactTemplate = QtGui.QLabel()
        self.loadedRegionalEconomicScenarioImpactTemplate.setText('<None>')
        self.layoutRegionalEconomicScenarioImpactTemplate.addWidget(self.loadedRegionalEconomicScenarioImpactTemplate, 0, 1)
        
        self.labelRegionalEconomicScenarioImpactTemplate = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactTemplate.setText('Name:')
        self.layoutRegionalEconomicScenarioImpactTemplate.addWidget(self.labelRegionalEconomicScenarioImpactTemplate, 1, 0)
        
        self.comboBoxRegionalEconomicScenarioImpactTemplate = QtGui.QComboBox()
        self.comboBoxRegionalEconomicScenarioImpactTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxRegionalEconomicScenarioImpactTemplate.setDisabled(True)
        self.comboBoxRegionalEconomicScenarioImpactTemplate.addItem('No configuration found')
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
        self.layoutContentRegionalEconomicScenarioImpact.addLayout(self.layoutButtonRegionalEconomicScenarioImpact, 2, 0, 1, 2, QtCore.Qt.AlignRight)
        self.layoutContentRegionalEconomicScenarioImpact.addWidget(self.groupBoxRegionalEconomicScenarioImpactTemplate, 0, 1, 2, 1)
        self.layoutContentRegionalEconomicScenarioImpact.setColumnStretch(0, 3)
        self.layoutContentRegionalEconomicScenarioImpact.setColumnStretch(1, 1) # Smaller template column

        
        #***********************************************************
        # Setup 'Land Use Scenario' tab
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
        self.groupBoxLandUseChangeImpactParameters = QtGui.QGroupBox('Parameterization')
        self.layoutGroupBoxLandUseChangeImpactParameters = QtGui.QVBoxLayout()
        self.layoutGroupBoxLandUseChangeImpactParameters.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLandUseChangeImpactParameters.setLayout(self.layoutGroupBoxLandUseChangeImpactParameters)
        self.layoutLandUseChangeImpactParametersInfo = QtGui.QVBoxLayout()
        self.layoutLandUseChangeImpactParameters = QtGui.QGridLayout()
        self.layoutGroupBoxLandUseChangeImpactParameters.addLayout(self.layoutLandUseChangeImpactParametersInfo)
        self.layoutGroupBoxLandUseChangeImpactParameters.addLayout(self.layoutLandUseChangeImpactParameters)
        
        self.labelLandUseChangeImpactParametersInfo = QtGui.QLabel()
        self.labelLandUseChangeImpactParametersInfo.setText('\n')
        self.layoutLandUseChangeImpactParametersInfo.addWidget(self.labelLandUseChangeImpactParametersInfo)
        
        self.labelLandUseChangeLandRequirement = QtGui.QLabel()
        self.labelLandUseChangeLandRequirement.setText('Land requirement:')
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelLandUseChangeLandRequirement, 0, 0)
        
        self.lineEditLandUseChangeLandRequirement = QtGui.QLineEdit()
        self.lineEditLandUseChangeLandRequirement.setReadOnly(True)
        self.layoutLandUseChangeImpactParameters.addWidget(self.lineEditLandUseChangeLandRequirement, 0, 1)
        
        self.buttonSelectLandUseChangeLandRequirement = QtGui.QPushButton()
        self.buttonSelectLandUseChangeLandRequirement.setText('&Browse')
        self.layoutLandUseChangeImpactParameters.addWidget(self.buttonSelectLandUseChangeLandRequirement, 0, 2)
        
        self.labelSelectLandUseChangeMap = QtGui.QLabel()
        self.labelSelectLandUseChangeMap.setText('Projected land cover map:')
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelSelectLandUseChangeMap, 1, 0)
        
        self.comboBoxSelectLandUseChangeMap = QtGui.QComboBox()
        self.comboBoxSelectLandUseChangeMap.setDisabled(True)
        self.layoutLandUseChangeImpactParameters.addWidget(self.comboBoxSelectLandUseChangeMap, 1, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataLandUseCover, self.comboBoxSelectLandUseChangeMap)
        
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
        self.groupBoxLandUseChangeImpactTemplate = QtGui.QGroupBox('Configuration')
        self.layoutGroupBoxLandUseChangeImpactTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxLandUseChangeImpactTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLandUseChangeImpactTemplate.setLayout(self.layoutGroupBoxLandUseChangeImpactTemplate)
        self.layoutLandUseChangeImpactTemplateInfo = QtGui.QVBoxLayout()
        self.layoutLandUseChangeImpactTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxLandUseChangeImpactTemplate.addLayout(self.layoutLandUseChangeImpactTemplateInfo)
        self.layoutGroupBoxLandUseChangeImpactTemplate.addLayout(self.layoutLandUseChangeImpactTemplate)
        
        self.labelLoadedLandUseChangeImpactTemplate = QtGui.QLabel()
        self.labelLoadedLandUseChangeImpactTemplate.setText('Loaded configuration:')
        self.layoutLandUseChangeImpactTemplate.addWidget(self.labelLoadedLandUseChangeImpactTemplate, 0, 0)
        
        self.loadedLandUseChangeImpactTemplate = QtGui.QLabel()
        self.loadedLandUseChangeImpactTemplate.setText('<None>')
        self.layoutLandUseChangeImpactTemplate.addWidget(self.loadedLandUseChangeImpactTemplate, 0, 1)
        
        self.labelLandUseChangeImpactTemplate = QtGui.QLabel()
        self.labelLandUseChangeImpactTemplate.setText('Name:')
        self.layoutLandUseChangeImpactTemplate.addWidget(self.labelLandUseChangeImpactTemplate, 1, 0)
        
        self.comboBoxLandUseChangeImpactTemplate = QtGui.QComboBox()
        self.comboBoxLandUseChangeImpactTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxLandUseChangeImpactTemplate.setDisabled(True)
        self.comboBoxLandUseChangeImpactTemplate.addItem('No configuration found')
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
        self.setMinimumSize(1024,700)
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
    
    
    #***********************************************************
    # 'Descriptive Analysis of Regional Economy' tab QPushButton handlers
    #***********************************************************    
    def handlerSelectLandRequirementAnalysisDescriptiveOutput(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Descriptive Analysis Output', QtCore.QDir.homePath(), 'Descriptive Analysis Output (*{0})'.format(self.main.appSettings['selectLdbasefileExt'])))
        
        if file:
            self.lineEditLandRequirementAnalysisDescriptiveOutput.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
            
            
    #***********************************************************
    # 'Regional Economy Scenario' tab QPushButton handlers
    #***********************************************************    
    def handlerSelectRegionalEconomicScenarioLandRequirement(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Requirement File', QtCore.QDir.homePath(), 'Land Requirement (*{0})'.format(self.main.appSettings['selectLdbasefileExt'])))
        
        if file:
            self.lineEditRegionalEconomicScenarioLandRequirement.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)            


    #***********************************************************
    # 'Land Use Scenario' tab QPushButton handlers
    #***********************************************************    
    def handlerSelectLandUseChangeLandRequirement(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Requirement File', QtCore.QDir.homePath(), 'Land Requirement (*{0})'.format(self.main.appSettings['selectLdbasefileExt'])))
        
        if file:
            self.lineEditLandUseChangeLandRequirement.setText(file)
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
        self.main.appSettings['DialogLumensTAOpportunityCostCurve']['csvNPVTable'] = unicode(self.comboBoxOCCCsvNPVTable.currentText())
        self.main.appSettings['DialogLumensTAOpportunityCostCurve']['costThreshold'] = self.spinBoxOCCCostThreshold.value()
        
        outputOpportunityCostDatabase = unicode(self.lineEditOCCOutputOpportunityCostDatabase.text())
        outputOpportunityCostReport = unicode(self.lineEditOCCOutputOpportunityCostReport.text())
        
        if not outputOpportunityCostDatabase:
            self.main.appSettings['DialogLumensTAOpportunityCostCurve']['outputOpportunityCostDatabase'] = '__UNSET__'
        
        if not outputOpportunityCostReport:
            self.main.appSettings['DialogLumensTAOpportunityCostCurve']['outputOpportunityCostReport'] = '__UNSET__'
        
        # 'Opportunity Cost Map' tab fields
        self.main.appSettings['DialogLumensTAOpportunityCostMap']['csvProfitability'] = unicode(self.comboBoxOCMCsvProfitability.currentText())
        
        # 'Descriptive Analysis' tab fields
        self.main.appSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['year'] \
            = self.spinBoxSinglePeriod.value()
        self.main.appSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['intermediateConsumptionMatrix'] \
            = unicode(self.comboBoxSingleIntermediateConsumptionMatrix.currentText())
        self.main.appSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['valueAddedMatrix'] \
            = unicode(self.comboBoxSingleValueAddedMatrix.currentText())
        self.main.appSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['finalConsumptionMatrix'] \
            = unicode(self.comboBoxSingleFinalConsumptionMatrix.currentText())
        self.main.appSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['labourRequirement'] \
            = unicode(self.comboBoxSingleLabourRequirement.currentText())
        self.main.appSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['valueAddedComponent'] \
            = unicode(self.comboBoxOtherValueAddedComponent.currentText())
        self.main.appSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['finalConsumptionComponent'] \
            = unicode(self.comboBoxOtherFinalConsumptionComponent.currentText())
        self.main.appSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['listOfEconomicSector'] \
            = unicode(self.comboBoxOtherListOfEconomicSector.currentText())
        self.main.appSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['financialUnit'] \
            = unicode(self.lineEditOtherFinancialUnit.text())
        self.main.appSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['areaName'] \
            = unicode(self.lineEditOtherAreaName.text())
        
        # 'Land Requirement' tab fields
        self.main.appSettings['DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis']['landUseCover'] \
            = unicode(self.comboBoxLandRequirementAnalysisLandUseCover.currentText()) 
        self.main.appSettings['DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis']['landRequirementTable'] \
            = unicode(self.comboBoxLandRequirementAnalysisLookupTable.currentText())
        self.main.appSettings['DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis']['descriptiveAnalysisOutput'] \
            = unicode(self.lineEditLandRequirementAnalysisDescriptiveOutput.text())
        
        # 'Regional Economy Scenario' tab fields
        self.main.appSettings['DialogLumensTARegionalEconomyScenario']['landRequirement'] \
            = unicode(self.lineEditRegionalEconomicScenarioLandRequirement.text())        
        self.main.appSettings['DialogLumensTARegionalEconomyScenario']['finalDemandChangeScenario'] \
            = unicode(self.comboBoxRegionalEconomicScenarioImpactFinalDemandChangeScenario.currentText())
        self.main.appSettings['DialogLumensTARegionalEconomyScenario']['gdpChangeScenario'] \
            = unicode(self.comboBoxRegionalEconomicScenarioImpactGDPChangeScenario.currentText())        
        
        # 'Land Use Scenario' tab fields
        self.main.appSettings['DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis']['landRequirement'] \
            = unicode(self.lineEditLandUseChangeLandRequirement.text())
        self.main.appSettings['DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis']['landUseCover'] \
            = unicode(self.comboBoxSelectLandUseChangeMap.currentText())        
        
    
    def handlerProcessAbacusOpportunityCost(self):
        """Slot method to pass the form values and execute the "TA Abacus Opportunity Cost" R algorithm.
        
        The "TA Abacus Opportunity Cost" process calls the following algorithm:
        1. r:ta_opcost_abacus
        """
        self.setAppSettings()
        
        formName = 'DialogLumensTAAbacusOpportunityCostCurve'
        algName = 'r:taopcostabacus'
        
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
        1. r:ta_opcost_curve
        """
        self.setAppSettings()
        
        formName = 'DialogLumensTAOpportunityCostCurve'
        algName = 'r:taopcostcurve'
        
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
        1. r:ta_opcost_map
        """
        self.setAppSettings()
        
        formName = 'DialogLumensTAOpportunityCostMap'
        algName = 'r:taopcostmap'
        
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
    

    def handlerProcessDescriptiveAnalysis(self):
        """Slot method to pass the form values and execute the "TA Descriptive Analysis of Regional Economy" R algorithms.
        
        "TA Descriptive Analysis of Regional Economy" process calls the following algorithms:
        1. r:ta_re_singleio_descriptive
        """
        self.setAppSettings()
        
        formName = 'DialogLumensTARegionalEconomySingleIODescriptiveAnalysis'
        algName = 'r:taresingleiodescriptive'
        activeProject = self.main.appSettings['DialogLumensOpenDatabase']['projectFile'].replace(os.path.sep, '/')
        
        if self.validForm(formName):
            logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
            logging.getLogger(self.historyLog).info('alg start: %s' % formName)
            self.buttonProcessDescriptiveAnalysis.setDisabled(True)
            
            # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
            self.main.setWindowState(QtCore.Qt.WindowMinimized)
            
            outputs = general.runalg(
                algName,
                activeProject,
                self.main.appSettings[formName]['intermediateConsumptionMatrix'],
                self.main.appSettings[formName]['valueAddedMatrix'],
                self.main.appSettings[formName]['finalConsumptionMatrix'],
                self.main.appSettings[formName]['valueAddedComponent'],
                self.main.appSettings[formName]['finalConsumptionComponent'],
                self.main.appSettings[formName]['listOfEconomicSector'],
                self.main.appSettings[formName]['labourRequirement'],
                self.main.appSettings[formName]['financialUnit'],
                self.main.appSettings[formName]['areaName'],
                self.main.appSettings[formName]['year'],
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
            
            self.buttonProcessDescriptiveAnalysis.setEnabled(True)
            logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
            logging.getLogger(self.historyLog).info('alg end: %s' % formName)
        
      
    def handlerProcessLandRequirementAnalysis(self):
        """Slot method to pass the form values and execute the "TA Land Requirement Analysis" R algorithm.
        
        The "TA Land Requirement Analysis" process calls the following algorithm:
        1. r:ta_re_ld_lr
        """
        self.setAppSettings()
        
        formName = 'DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis'
        algName = 'r:tareldlr'
        activeProject = self.main.appSettings['DialogLumensOpenDatabase']['projectFile'].replace(os.path.sep, '/')
        
        if self.validForm(formName):
            logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
            logging.getLogger(self.historyLog).info('alg start: %s' % formName)
            self.buttonProcessLandRequirementAnalysis.setDisabled(True)
            
            # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
            self.main.setWindowState(QtCore.Qt.WindowMinimized)
            
            outputs = general.runalg(
                algName,
                activeProject,
                self.main.appSettings[formName]['landUseCover'],
                self.main.appSettings[formName]['landRequirementTable'],
                self.main.appSettings[formName]['descriptiveAnalysisOutput'],
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
            
            self.buttonProcessLandRequirementAnalysis.setEnabled(True)
            logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
            logging.getLogger(self.historyLog).info('alg end: %s' % formName)
      
    def handlerProcessRegionalEconomicScenarioImpact(self):
        """Slot method to pass the form values and execute the "TA Regional Economic Scenario Impact" R algorithms.
        
        Depending on the checked groupbox, the "TA Regional Economic Scenario Impact" process calls the following algorithms:
        1. r:ta_re_finaldemand
        2. r:ta_re_gdp
        """
        self.setAppSettings()
        
        if self.checkBoxRegionalEconomicScenarioImpactFinalDemand.isChecked():
            formName = 'DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis'
            algName = 'r:tarefinaldemand'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                logging.getLogger(self.historyLog).info('alg start: %s' % formName)
                self.buttonProcessRegionalEconomicScenarioImpact.setDisabled(True)
                
                # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                self.main.setWindowState(QtCore.Qt.WindowMinimized)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['landRequirement'],
                    self.main.appSettings[formName]['finalDemandChangeScenario'],
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
                
                self.buttonProcessRegionalEconomicScenarioImpact.setEnabled(True)
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
                logging.getLogger(self.historyLog).info('alg end: %s' % formName)
        
        if self.checkBoxRegionalEconomicScenarioImpactGDP.isChecked():
            formName = 'DialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis'
            algName = 'r:taregdp'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                logging.getLogger(self.historyLog).info('alg start: %s' % formName)
                self.buttonProcessRegionalEconomicScenarioImpact.setDisabled(True)
                
                # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                self.main.setWindowState(QtCore.Qt.WindowMinimized)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['areaName'],
                    self.main.appSettings[formName]['gdpChangeScenario'],
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
                
                self.buttonProcessRegionalEconomicScenarioImpact.setEnabled(True)
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
                logging.getLogger(self.historyLog).info('alg end: %s' % formName)
    
      
    def handlerProcessLandUseChangeImpact(self):
        """Slot method to pass the form values and execute the "TA Land Use Change Impact" R algorithm.
        
        The "TA Land Use Change Impact" process calls the following algorithm:
        1. r:ta_re_luc_impact
        """
        self.setAppSettings()
        
        formName = 'DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis'
        algName = 'r:tarelucimpact'
        
        if self.validForm(formName):
            logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
            logging.getLogger(self.historyLog).info('alg start: %s' % formName)
            self.buttonProcessLandUseChangeImpact.setDisabled(True)
            
            # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
            self.main.setWindowState(QtCore.Qt.WindowMinimized)
            
            outputs = general.runalg(
                algName,
                self.main.appSettings[formName]['landRequirement'],
                self.main.appSettings[formName]['landUseCover'],
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
            
            self.buttonProcessLandUseChangeImpact.setEnabled(True)
            logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
            logging.getLogger(self.historyLog).info('alg end: %s' % formName)
    
        
