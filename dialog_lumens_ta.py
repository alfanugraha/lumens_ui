#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, datetime, glob
from qgis.core import *
# from processing.tools import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from utils import QPlainTextEditLogger
from dialog_lumens_base import DialogLumensBase
from dialog_lumens_viewer import DialogLumensViewer
import resource

from menu_factory import MenuFactory

class DialogLumensTA(QDialog): # DialogLumensBase
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
        settings = QSettings(templateFilePath, QSettings.IniFormat)
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
        elif tabName == MenuFactory.getLabel(MenuFactory.TAREGECO_DESCRIPTIVE_ANALYSIS):
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
        elif tabName == MenuFactory.getLabel(MenuFactory.TAREGECO_LAND_REQUIREMENT_ANALYSIS):
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
        elif tabName == MenuFactory.getLabel(MenuFactory.TAREGECO_REGIONAL_ECONOMY_SCENARIO):
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
        elif tabName == MenuFactory.getLabel(MenuFactory.TAREGECO_LAND_USE_SCENARIO):
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
        elif tabName == MenuFactory.getLabel(MenuFactory.TAREGECO_DESCRIPTIVE_ANALYSIS):
            dialogsToSave = (
                'DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis',
            )
        elif tabName == MenuFactory.getLabel(MenuFactory.TAREGECO_LAND_REQUIREMENT_ANALYSIS):
            dialogsToSave = (
                'DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis',
            )
        elif tabName == MenuFactory.getLabel(MenuFactory.TAREGECO_REGIONAL_ECONOMY_SCENARIO):
            dialogsToSave = (
                'DialogLumensTARegionalEconomyScenario',
            )
        elif tabName == MenuFactory.getLabel(MenuFactory.TAREGECO_LAND_USE_SCENARIO):
            dialogsToSave = (
                'DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis',
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
            reply = QMessageBox.question(
                self,
                MenuFactory.getLabel(MenuFactory.CONF_LOAD_EXISTING_CONFIGURATION),
                MenuFactory.getDescription(MenuFactory.CONF_LOAD_EXISTING_CONFIGURATION) + ' \'{0}\'?'.format(duplicateTemplate),
                QMessageBox.Yes|QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                if tabName == MenuFactory.getLabel(MenuFactory.TAOPCOST_ABACUS_OPPORTUNITY_COST):
                    self.handlerLoadAbacusOpportunityCostTemplate(duplicateTemplate)
                elif tabName == MenuFactory.getLabel(MenuFactory.TAOPCOST_OPPORTUNITY_COST_CURVE):
                    self.handlerLoadOpportunityCostCurveTemplate(duplicateTemplate)
                elif tabName == MenuFactory.getLabel(MenuFactory.TAOPCOST_OPPORTUNITY_COST_MAP):
                    self.handlerLoadOpportunityCostMapTemplate(duplicateTemplate)
                elif tabName == MenuFactory.getLabel(MenuFactory.TAREGECO_DESCRIPTIVE_ANALYSIS):
                    self.handlerLoadDescriptiveAnalysisTemplate(duplicateTemplate)
                elif tabName == MenuFactory.getLabel(MenuFactory.TAREGECO_LAND_REQUIREMENT_ANALYSIS):
                    self.handlerLoadLandRequirementAnalysisTemplate(duplicateTemplate)
                elif tabName == MenuFactory.getLabel(MenuFactory.TAREGECO_REGIONAL_ECONOMY_SCENARIO):
                    self.handlerLoadRegionalEconomicScenarioImpactTemplate(duplicateTemplate)
                elif tabName == MenuFactory.getLabel(MenuFactory.TAREGECO_LAND_USE_SCENARIO):
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
            settings = QSettings(templateFilePath, QSettings.IniFormat)
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
            elif tabName == MenuFactory.getLabel(MenuFactory.TAREGECO_DESCRIPTIVE_ANALYSIS):
                dialogsToSave = (
                    'DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis',
                )
            elif tabName == MenuFactory.getLabel(MenuFactory.TAREGECO_LAND_REQUIREMENT_ANALYSIS):
                dialogsToSave = (
                    'DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis',
                )
            elif tabName == MenuFactory.getLabel(MenuFactory.TAREGECO_REGIONAL_ECONOMY_SCENARIO):
                dialogsToSave = (
                    'DialogLumensTARegionalEconomyScenario',
                )
            elif tabName == MenuFactory.getLabel(MenuFactory.TAREGECO_LAND_USE_SCENARIO):
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
            print('DEBUG: DialogLumensTA init')
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
        
        # 'Abacus Opportunity Cost' tab buttons
        self.buttonSelectAOCProjectFile.clicked.connect(self.handlerSelectAOCProjectFile)
        self.buttonProcessAbacusOpportunityCost.clicked.connect(self.handlerProcessAbacusOpportunityCost)
        self.buttonHelpTAAbacusOpportunityCost.clicked.connect(lambda:self.handlerDialogHelp('TA'))
        self.buttonLoadAbacusOpportunityCostTemplate.clicked.connect(self.handlerLoadAbacusOpportunityCostTemplate)
        self.buttonSaveAbacusOpportunityCostTemplate.clicked.connect(self.handlerSaveAbacusOpportunityCostTemplate)
        self.buttonSaveAsAbacusOpportunityCostTemplate.clicked.connect(self.handlerSaveAsAbacusOpportunityCostTemplate)
        
        # 'Opportunity Cost Curve' tab buttons
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
        self.dialogLayout = QVBoxLayout()

        self.groupBoxTADialog = QGroupBox(MenuFactory.getDescription(MenuFactory.TA_TITLE))
        self.layoutGroupBoxTADialog = QVBoxLayout()
        self.layoutGroupBoxTADialog.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.groupBoxTADialog.setLayout(self.layoutGroupBoxTADialog)
        self.labelTADialogInfo = QLabel()
        self.labelTADialogInfo.setText('\n')
        self.labelTADialogInfo.setWordWrap(True)
        self.layoutGroupBoxTADialog.addWidget(self.labelTADialogInfo)

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
        
        self.tabOpportunityCost = QWidget()
        self.tabRegionalEconomy = QWidget()
        self.tabLog = QWidget()
        
        self.tabWidget.addTab(self.tabOpportunityCost, MenuFactory.getLabel(MenuFactory.TAOPCOST_TITLE))
        self.tabWidget.addTab(self.tabRegionalEconomy, MenuFactory.getLabel(MenuFactory.TAREGECO_TITLE))
        self.tabWidget.addTab(self.tabLog, MenuFactory.getLabel(MenuFactory.TA_LOG))
        
        self.layoutTabOpportunityCost = QVBoxLayout()
        self.layoutTabRegionalEconomy = QVBoxLayout()
        self.layoutTabLog = QVBoxLayout()
        
        self.tabOpportunityCost.setLayout(self.layoutTabOpportunityCost)
        self.tabRegionalEconomy.setLayout(self.layoutTabRegionalEconomy)
        self.tabLog.setLayout(self.layoutTabLog)

        self.dialogLayout.addWidget(self.groupBoxTADialog)
        self.dialogLayout.addWidget(self.tabWidget)
        
        
        #***********************************************************
        # Setup 'Opportunity Cost' tab
        #***********************************************************
        self.tabWidgetOpportunityCost = QTabWidget()
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
        
        self.tabAbacusOpportunityCost = QWidget()
        self.tabOpportunityCostCurve = QWidget()
        self.tabOpportunityCostMap = QWidget()
        
        # self.tabWidgetOpportunityCost.addTab(self.tabAbacusOpportunityCost, MenuFactory.getLabel(MenuFactory.TAOPCOST_ABACUS_OPPORTUNITY_COST))
        self.tabWidgetOpportunityCost.addTab(self.tabOpportunityCostCurve, MenuFactory.getLabel(MenuFactory.TAOPCOST_OPPORTUNITY_COST_CURVE))
        self.tabWidgetOpportunityCost.addTab(self.tabOpportunityCostMap, MenuFactory.getLabel(MenuFactory.TAOPCOST_OPPORTUNITY_COST_MAP))
        
        self.layoutTabOpportunityCost.addWidget(self.tabWidgetOpportunityCost)
        
        self.layoutTabAbacusOpportunityCost = QGridLayout()
        self.layoutTabOpportunityCostCurve = QGridLayout()
        self.layoutTabOpportunityCostMap = QGridLayout()
        
        self.tabAbacusOpportunityCost.setLayout(self.layoutTabAbacusOpportunityCost)
        self.tabOpportunityCostCurve.setLayout(self.layoutTabOpportunityCostCurve)
        self.tabOpportunityCostMap.setLayout(self.layoutTabOpportunityCostMap)
        
        #***********************************************************
        # Setup 'Abacus opportunity cost' tab
        #***********************************************************
        # 'Other' GroupBox
        self.groupBoxOther = QGroupBox(MenuFactory.getLabel(MenuFactory.TAOPCOST_OTHER))
        self.layoutGroupBoxOther = QVBoxLayout()
        self.layoutGroupBoxOther.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.groupBoxOther.setLayout(self.layoutGroupBoxOther)
        self.layoutOtherInfo = QVBoxLayout()
        self.layoutOther = QGridLayout()
        self.layoutGroupBoxOther.addLayout(self.layoutOtherInfo)
        self.layoutGroupBoxOther.addLayout(self.layoutOther)
        
        self.labelOtherInfo = QLabel()
        self.labelOtherInfo.setText(MenuFactory.getDescription(MenuFactory.TAOPCOST_OTHER))
        self.layoutOtherInfo.addWidget(self.labelOtherInfo)
        
        self.labelAOCProjectFile = QLabel(parent)
        self.labelAOCProjectFile.setText(MenuFactory.getLabel(MenuFactory.TAOPCOST_ABACUS_PROJECT_FILE) + ':')
        self.layoutOther.addWidget(self.labelAOCProjectFile, 0, 0)
        
        self.lineEditAOCProjectFile = QLineEdit(parent)
        self.lineEditAOCProjectFile.setReadOnly(True)
        self.layoutOther.addWidget(self.lineEditAOCProjectFile, 0, 1)
        
        self.buttonSelectAOCProjectFile = QPushButton(parent)
        self.buttonSelectAOCProjectFile.setText('&' + MenuFactory.getLabel(MenuFactory.TAOPCOST_ABACUS_BROWSE))
        self.layoutOther.addWidget(self.buttonSelectAOCProjectFile, 0, 2)
        
        # Process tab button
        self.layoutButtonAbacusOpportunityCost = QHBoxLayout()
        self.buttonProcessAbacusOpportunityCost = QPushButton()
        self.buttonProcessAbacusOpportunityCost.setText('&' + MenuFactory.getLabel(MenuFactory.TAOPCOST_ABACUS_PROCESS))
        icon = QIcon(':/ui/icons/iconActionHelp.png')
        self.buttonHelpTAAbacusOpportunityCost = QPushButton()
        self.buttonHelpTAAbacusOpportunityCost.setIcon(icon)
        self.layoutButtonAbacusOpportunityCost.setAlignment(Qt.AlignRight)
        self.layoutButtonAbacusOpportunityCost.addWidget(self.buttonProcessAbacusOpportunityCost)
        self.layoutButtonAbacusOpportunityCost.addWidget(self.buttonHelpTAAbacusOpportunityCost)
        
        # Template GroupBox
        self.groupBoxAbacusOpportunityCostTemplate = QGroupBox(MenuFactory.getLabel(MenuFactory.CONF_TEMPLATE))
        self.layoutGroupBoxAbacusOpportunityCostTemplate = QVBoxLayout()
        self.layoutGroupBoxAbacusOpportunityCostTemplate.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.groupBoxAbacusOpportunityCostTemplate.setLayout(self.layoutGroupBoxAbacusOpportunityCostTemplate)
        self.layoutAbacusOpportunityCostTemplateInfo = QVBoxLayout()
        self.layoutAbacusOpportunityCostTemplate = QGridLayout()
        self.layoutGroupBoxAbacusOpportunityCostTemplate.addLayout(self.layoutAbacusOpportunityCostTemplateInfo)
        self.layoutGroupBoxAbacusOpportunityCostTemplate.addLayout(self.layoutAbacusOpportunityCostTemplate)
        
        self.labelLoadedAbacusOpportunityCostTemplate = QLabel()
        self.labelLoadedAbacusOpportunityCostTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_LOADED_TEMPLATE) + ':')
        self.layoutAbacusOpportunityCostTemplate.addWidget(self.labelLoadedAbacusOpportunityCostTemplate, 0, 0)
        
        self.loadedAbacusOpportunityCostTemplate = QLabel()
        self.loadedAbacusOpportunityCostTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NONE))
        self.layoutAbacusOpportunityCostTemplate.addWidget(self.loadedAbacusOpportunityCostTemplate, 0, 1)
        
        self.labelAbacusOpportunityCostTemplate = QLabel()
        self.labelAbacusOpportunityCostTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_TEMPLATE_NAME) + ':')
        self.layoutAbacusOpportunityCostTemplate.addWidget(self.labelAbacusOpportunityCostTemplate, 1, 0)
        
        self.comboBoxAbacusOpportunityCostTemplate = QComboBox()
        self.comboBoxAbacusOpportunityCostTemplate.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.comboBoxAbacusOpportunityCostTemplate.setDisabled(True)
        self.comboBoxAbacusOpportunityCostTemplate.addItem(MenuFactory.getLabel(MenuFactory.CONF_NO_TEMPLATE_FOUND))
        self.layoutAbacusOpportunityCostTemplate.addWidget(self.comboBoxAbacusOpportunityCostTemplate, 1, 1)
        
        self.layoutButtonAbacusOpportunityCostTemplate = QHBoxLayout()
        self.layoutButtonAbacusOpportunityCostTemplate.setAlignment(Qt.AlignRight|Qt.AlignTop)
        self.buttonLoadAbacusOpportunityCostTemplate = QPushButton()
        self.buttonLoadAbacusOpportunityCostTemplate.setDisabled(True)
        self.buttonLoadAbacusOpportunityCostTemplate.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.buttonLoadAbacusOpportunityCostTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_LOAD))
        self.buttonSaveAbacusOpportunityCostTemplate = QPushButton()
        self.buttonSaveAbacusOpportunityCostTemplate.setDisabled(True)
        self.buttonSaveAbacusOpportunityCostTemplate.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.buttonSaveAbacusOpportunityCostTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_SAVE))
        self.buttonSaveAsAbacusOpportunityCostTemplate = QPushButton()
        self.buttonSaveAsAbacusOpportunityCostTemplate.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.buttonSaveAsAbacusOpportunityCostTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_SAVE_AS))
        self.layoutButtonAbacusOpportunityCostTemplate.addWidget(self.buttonLoadAbacusOpportunityCostTemplate)
        self.layoutButtonAbacusOpportunityCostTemplate.addWidget(self.buttonSaveAbacusOpportunityCostTemplate)
        self.layoutButtonAbacusOpportunityCostTemplate.addWidget(self.buttonSaveAsAbacusOpportunityCostTemplate)
        self.layoutGroupBoxAbacusOpportunityCostTemplate.addLayout(self.layoutButtonAbacusOpportunityCostTemplate)
        
        # Place the GroupBoxes
        self.layoutTabAbacusOpportunityCost.addWidget(self.groupBoxOther, 0, 0)
        self.layoutTabAbacusOpportunityCost.addLayout(self.layoutButtonAbacusOpportunityCost, 1, 0, 1, 2, Qt.AlignRight)
        self.layoutTabAbacusOpportunityCost.addWidget(self.groupBoxAbacusOpportunityCostTemplate, 0, 1, 1, 1)
        self.layoutTabAbacusOpportunityCost.setColumnStretch(0, 3)
        self.layoutTabAbacusOpportunityCost.setColumnStretch(1, 1) # Smaller template column
        
        #***********************************************************
        # Setup 'Opportunity cost curve' sub tab
        #***********************************************************
        # 'Parameters' GroupBox
        self.groupBoxOCCParameters = QGroupBox(MenuFactory.getLabel(MenuFactory.TAOPCOST_PARAMETERIZATION))
        self.layoutGroupBoxOCCParameters = QVBoxLayout()
        self.layoutGroupBoxOCCParameters.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.groupBoxOCCParameters.setLayout(self.layoutGroupBoxOCCParameters)
        self.layoutOCCParametersInfo = QVBoxLayout()
        self.layoutOCCParameters = QGridLayout()
        self.layoutGroupBoxOCCParameters.addLayout(self.layoutOCCParametersInfo)
        self.layoutGroupBoxOCCParameters.addLayout(self.layoutOCCParameters)
        
        self.labelOCCParametersInfo = QLabel()
        self.labelOCCParametersInfo.setText('\n')
        self.layoutOCCParametersInfo.addWidget(self.labelOCCParametersInfo)
        
        self.labelOCCCsvNPVTable = QLabel(parent)
        self.labelOCCCsvNPVTable.setText(MenuFactory.getLabel(MenuFactory.TAOPCOST_PROFITABILITY_LOOKUP_TABLE) + ':')
        self.layoutOCCParameters.addWidget(self.labelOCCCsvNPVTable, 0, 0)
        
        self.comboBoxOCCCsvNPVTable = QComboBox()
        self.comboBoxOCCCsvNPVTable.setDisabled(True)
        self.layoutOCCParameters.addWidget(self.comboBoxOCCCsvNPVTable, 0, 1)
        
        # self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxOCCCsvNPVTable)
        DialogLumensBase.handlerPopulateNameFromLookupData(parent, self.main.dataTable, self.comboBoxOCCCsvNPVTable)

        self.labelOCCQUESCDatabase = QLabel(parent)
        self.labelOCCQUESCDatabase.setText(MenuFactory.getLabel(MenuFactory.TAOPCOST_QUESC_DATABASE) + ':')
        self.layoutOCCParameters.addWidget(self.labelOCCQUESCDatabase, 1, 0)
        
        self.comboBoxOCCQUESCDatabase = QComboBox()
        self.comboBoxOCCQUESCDatabase.setDisabled(True)
        self.layoutOCCParameters.addWidget(self.comboBoxOCCQUESCDatabase, 1, 1)
        
        # self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxOCCQUESCDatabase)
        DialogLumensBase.handlerPopulateNameFromLookupData(parent, self.main.dataTable, self.comboBoxOCCQUESCDatabase)
        
        self.labelOCCCostThreshold = QLabel()
        self.labelOCCCostThreshold.setText(MenuFactory.getLabel(MenuFactory.TAOPCOST_COST_THRESHOLD) + ':')
        self.layoutOCCParameters.addWidget(self.labelOCCCostThreshold, 2, 0)
        
        self.spinBoxOCCCostThreshold = QSpinBox()
        self.spinBoxOCCCostThreshold.setValue(5)
        self.layoutOCCParameters.addWidget(self.spinBoxOCCCostThreshold, 2, 1)
        
        # Process tab button
        self.layoutButtonOpportunityCostCurve = QHBoxLayout()
        self.buttonProcessOpportunityCostCurve = QPushButton()
        self.buttonProcessOpportunityCostCurve.setText('&' + MenuFactory.getLabel(MenuFactory.TA_PROCESS))
        self.buttonHelpTAOpportunityCostCurve = QPushButton()
        self.buttonHelpTAOpportunityCostCurve.setIcon(icon)
        self.layoutButtonOpportunityCostCurve.setAlignment(Qt.AlignRight)
        self.layoutButtonOpportunityCostCurve.addWidget(self.buttonProcessOpportunityCostCurve)
        self.layoutButtonOpportunityCostCurve.addWidget(self.buttonHelpTAOpportunityCostCurve)
        
        # Template GroupBox
        self.groupBoxOpportunityCostCurveTemplate = QGroupBox(MenuFactory.getLabel(MenuFactory.CONF_TITLE))
        self.layoutGroupBoxOpportunityCostCurveTemplate = QVBoxLayout()
        self.layoutGroupBoxOpportunityCostCurveTemplate.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.groupBoxOpportunityCostCurveTemplate.setLayout(self.layoutGroupBoxOpportunityCostCurveTemplate)
        self.layoutOpportunityCostCurveTemplateInfo = QVBoxLayout()
        self.layoutOpportunityCostCurveTemplate = QGridLayout()
        self.layoutGroupBoxOpportunityCostCurveTemplate.addLayout(self.layoutOpportunityCostCurveTemplateInfo)
        self.layoutGroupBoxOpportunityCostCurveTemplate.addLayout(self.layoutOpportunityCostCurveTemplate)
        
        self.labelLoadedOpportunityCostCurveTemplate = QLabel()
        self.labelLoadedOpportunityCostCurveTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_LOADED_CONFIGURATION) + ':')
        self.layoutOpportunityCostCurveTemplate.addWidget(self.labelLoadedOpportunityCostCurveTemplate, 0, 0)
        
        self.loadedOpportunityCostCurveTemplate = QLabel()
        self.loadedOpportunityCostCurveTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NONE))
        self.layoutOpportunityCostCurveTemplate.addWidget(self.loadedOpportunityCostCurveTemplate, 0, 1)
        
        self.labelOpportunityCostCurveTemplate = QLabel()
        self.labelOpportunityCostCurveTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NAME) + ':')
        self.layoutOpportunityCostCurveTemplate.addWidget(self.labelOpportunityCostCurveTemplate, 1, 0)
        
        self.comboBoxOpportunityCostCurveTemplate = QComboBox()
        self.comboBoxOpportunityCostCurveTemplate.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.comboBoxOpportunityCostCurveTemplate.setDisabled(True)
        self.comboBoxOpportunityCostCurveTemplate.addItem(MenuFactory.getLabel(MenuFactory.CONF_NO_FOUND))
        self.layoutOpportunityCostCurveTemplate.addWidget(self.comboBoxOpportunityCostCurveTemplate, 1, 1)
        
        self.layoutButtonOpportunityCostCurveTemplate = QHBoxLayout()
        self.layoutButtonOpportunityCostCurveTemplate.setAlignment(Qt.AlignRight|Qt.AlignTop)
        self.buttonLoadOpportunityCostCurveTemplate = QPushButton()
        self.buttonLoadOpportunityCostCurveTemplate.setDisabled(True)
        self.buttonLoadOpportunityCostCurveTemplate.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.buttonLoadOpportunityCostCurveTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_LOAD))
        self.buttonSaveOpportunityCostCurveTemplate = QPushButton()
        self.buttonSaveOpportunityCostCurveTemplate.setDisabled(True)
        self.buttonSaveOpportunityCostCurveTemplate.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.buttonSaveOpportunityCostCurveTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_SAVE))
        self.buttonSaveAsOpportunityCostCurveTemplate = QPushButton()
        self.buttonSaveAsOpportunityCostCurveTemplate.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.buttonSaveAsOpportunityCostCurveTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_SAVE_AS))
        self.layoutButtonOpportunityCostCurveTemplate.addWidget(self.buttonLoadOpportunityCostCurveTemplate)
        self.layoutButtonOpportunityCostCurveTemplate.addWidget(self.buttonSaveOpportunityCostCurveTemplate)
        self.layoutButtonOpportunityCostCurveTemplate.addWidget(self.buttonSaveAsOpportunityCostCurveTemplate)
        self.layoutGroupBoxOpportunityCostCurveTemplate.addLayout(self.layoutButtonOpportunityCostCurveTemplate)
        
        # Place the GroupBoxes
        self.layoutTabOpportunityCostCurve.addWidget(self.groupBoxOCCParameters, 0, 0)
        self.layoutTabOpportunityCostCurve.addLayout(self.layoutButtonOpportunityCostCurve, 1, 0, 1, 2, Qt.AlignRight)
        self.layoutTabOpportunityCostCurve.addWidget(self.groupBoxOpportunityCostCurveTemplate, 0, 1, 1, 1)
        self.layoutTabOpportunityCostCurve.setColumnStretch(0, 3)
        self.layoutTabOpportunityCostCurve.setColumnStretch(1, 1) # Smaller template column
        
        ##self.layoutTabOpportunityCostCurve.insertStretch(2, 1)
        
        ##self.layoutTabOpportunityCostCurve.setStretchFactor(self.groupBoxOCCParameters, 4)
        
        
        #***********************************************************
        # Setup 'Opportunity cost map' sub tab
        #***********************************************************
        # 'Parameters' GroupBox
        self.groupBoxOCMParameters = QGroupBox(MenuFactory.getLabel(MenuFactory.TAOPCOST_PARAMETERIZATION))
        self.layoutGroupBoxOCMParameters = QVBoxLayout()
        self.layoutGroupBoxOCMParameters.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.groupBoxOCMParameters.setLayout(self.layoutGroupBoxOCMParameters)
        self.layoutOCMParametersInfo = QVBoxLayout()
        self.layoutOCMParameters = QGridLayout()
        self.layoutGroupBoxOCMParameters.addLayout(self.layoutOCMParametersInfo)
        self.layoutGroupBoxOCMParameters.addLayout(self.layoutOCMParameters)
        
        self.labelOCMParametersInfo = QLabel()
        self.labelOCMParametersInfo.setText('\n')
        self.layoutOCMParametersInfo.addWidget(self.labelOCMParametersInfo)

        self.labelOCMLandCoverLandUse1 = QLabel()
        self.labelOCMLandCoverLandUse1.setText(MenuFactory.getLabel(MenuFactory.TAOPCOST_EARLIER_LAND_USE_COVER) + ':')
        self.layoutOCMParameters.addWidget(self.labelOCMLandCoverLandUse1, 0, 0)
        
        self.comboBoxOCMLandCoverLandUse1 = QComboBox()
        self.comboBoxOCMLandCoverLandUse1.setDisabled(True)
        self.layoutOCMParameters.addWidget(self.comboBoxOCMLandCoverLandUse1, 0, 1)
        
        # self.handlerPopulateNameFromLookupData(self.main.dataLandUseCover, self.comboBoxOCMLandCoverLandUse1)
        DialogLumensBase.handlerPopulateNameFromLookupData(parent, self.main.dataLandUseCover, self.comboBoxOCMLandCoverLandUse1)
        
        self.labelOCMLandCoverLandUse2 = QLabel()
        self.labelOCMLandCoverLandUse2.setText(MenuFactory.getLabel(MenuFactory.TAOPCOST_LATER_LAND_USE_COVER) + ':')
        self.layoutOCMParameters.addWidget(self.labelOCMLandCoverLandUse2, 1, 0)
        
        self.comboBoxOCMLandCoverLandUse2 = QComboBox()
        self.comboBoxOCMLandCoverLandUse2.setDisabled(True)
        self.layoutOCMParameters.addWidget(self.comboBoxOCMLandCoverLandUse2, 1, 1)
        
        # self.handlerPopulateNameFromLookupData(self.main.dataLandUseCover, self.comboBoxOCMLandCoverLandUse2)
        DialogLumensBase.handlerPopulateNameFromLookupData(parent, self.main.dataLandUseCover, self.comboBoxOCMLandCoverLandUse2)
        
        self.labelOCMLandCoverPlanningUnit = QLabel()
        self.labelOCMLandCoverPlanningUnit.setText(MenuFactory.getLabel(MenuFactory.TAOPCOST_PLANNING_UNIT) + ':')
        self.layoutOCMParameters.addWidget(self.labelOCMLandCoverPlanningUnit, 2, 0)
        
        self.comboBoxOCMLandCoverPlanningUnit = QComboBox()
        self.comboBoxOCMLandCoverPlanningUnit.setDisabled(True)
        self.layoutOCMParameters.addWidget(self.comboBoxOCMLandCoverPlanningUnit, 2, 1)
        
        # self.handlerPopulateNameFromLookupData(self.main.dataPlanningUnit, self.comboBoxOCMLandCoverPlanningUnit)   
        DialogLumensBase.handlerPopulateNameFromLookupData(parent, self.main.dataPlanningUnit, self.comboBoxOCMLandCoverPlanningUnit)     
        
        self.labelOCMCarbonTable = QLabel()
        self.labelOCMCarbonTable.setText(MenuFactory.getLabel(MenuFactory.TAOPCOST_CARBON_STOCK_LOOKUP_TABLE) + ':')
        self.layoutOCMParameters.addWidget(self.labelOCMCarbonTable, 3, 0)
        
        self.comboBoxOCMCarbonTable = QComboBox()
        self.comboBoxOCMCarbonTable.setDisabled(True)
        self.layoutOCMParameters.addWidget(self.comboBoxOCMCarbonTable, 3, 1)
        
        # self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxOCMCarbonTable) 
        DialogLumensBase.handlerPopulateNameFromLookupData(parent, self.main.dataTable, self.comboBoxOCMCarbonTable)   
        
        self.labelOCMCsvProfitability = QLabel(parent)
        self.labelOCMCsvProfitability.setText(MenuFactory.getLabel(MenuFactory.TAOPCOST_PROFITABILITY_LOOKUP_TABLE) + ':')
        self.layoutOCMParameters.addWidget(self.labelOCMCsvProfitability, 4, 0)
        
        self.comboBoxOCMCsvProfitability = QComboBox()
        self.comboBoxOCMCsvProfitability.setDisabled(True)
        self.layoutOCMParameters.addWidget(self.comboBoxOCMCsvProfitability, 4, 1)
        
        # self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxOCMCsvProfitability)        
        DialogLumensBase.handlerPopulateNameFromLookupData(parent, self.main.dataTable, self.comboBoxOCMCsvProfitability) 
        
        self.labelOCMNoDataValue = QLabel()
        self.labelOCMNoDataValue.setText(MenuFactory.getLabel(MenuFactory.TAOPCOST_NO_DATA_VALUE) + ':')
        self.layoutOCMParameters.addWidget(self.labelOCMNoDataValue, 5, 0)
        
        self.spinBoxOCMNoDataValue = QSpinBox()
        self.spinBoxOCMNoDataValue.setRange(-9999, 9999)
        self.spinBoxOCMNoDataValue.setValue(0)
        self.layoutOCMParameters.addWidget(self.spinBoxOCMNoDataValue, 5, 1)
        self.labelOCMNoDataValue.setBuddy(self.spinBoxOCMNoDataValue)
        

        # Process tab button
        self.layoutButtonOpportunityCostMap = QHBoxLayout()
        self.buttonProcessOpportunityCostMap = QPushButton()
        self.buttonProcessOpportunityCostMap.setText(MenuFactory.getLabel(MenuFactory.TA_PROCESS))
        self.buttonHelpTAOpportunityCostMap = QPushButton()
        self.buttonHelpTAOpportunityCostMap.setIcon(icon)
        self.layoutButtonOpportunityCostMap.setAlignment(Qt.AlignRight)
        self.layoutButtonOpportunityCostMap.addWidget(self.buttonProcessOpportunityCostMap)
        self.layoutButtonOpportunityCostMap.addWidget(self.buttonHelpTAOpportunityCostMap)
        
        # Template GroupBox
        self.groupBoxOpportunityCostMapTemplate = QGroupBox(MenuFactory.getLabel(MenuFactory.CONF_TITLE))
        self.layoutGroupBoxOpportunityCostMapTemplate = QVBoxLayout()
        self.layoutGroupBoxOpportunityCostMapTemplate.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.groupBoxOpportunityCostMapTemplate.setLayout(self.layoutGroupBoxOpportunityCostMapTemplate)
        self.layoutOpportunityCostMapTemplateInfo = QVBoxLayout()
        self.layoutOpportunityCostMapTemplate = QGridLayout()
        self.layoutGroupBoxOpportunityCostMapTemplate.addLayout(self.layoutOpportunityCostMapTemplateInfo)
        self.layoutGroupBoxOpportunityCostMapTemplate.addLayout(self.layoutOpportunityCostMapTemplate)
        
        self.labelLoadedOpportunityCostMapTemplate = QLabel()
        self.labelLoadedOpportunityCostMapTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_LOADED_CONFIGURATION) + ':')
        self.layoutOpportunityCostMapTemplate.addWidget(self.labelLoadedOpportunityCostMapTemplate, 0, 0)
        
        self.loadedOpportunityCostMapTemplate = QLabel()
        self.loadedOpportunityCostMapTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NONE))
        self.layoutOpportunityCostMapTemplate.addWidget(self.loadedOpportunityCostMapTemplate, 0, 1)
        
        self.labelOpportunityCostMapTemplate = QLabel()
        self.labelOpportunityCostMapTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NAME) + ':')
        self.layoutOpportunityCostMapTemplate.addWidget(self.labelOpportunityCostMapTemplate, 1, 0)
        
        self.comboBoxOpportunityCostMapTemplate = QComboBox()
        self.comboBoxOpportunityCostMapTemplate.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.comboBoxOpportunityCostMapTemplate.setDisabled(True)
        self.comboBoxOpportunityCostMapTemplate.addItem(MenuFactory.getLabel(MenuFactory.CONF_NO_FOUND))
        self.layoutOpportunityCostMapTemplate.addWidget(self.comboBoxOpportunityCostMapTemplate, 1, 1)
        
        self.layoutButtonOpportunityCostMapTemplate = QHBoxLayout()
        self.layoutButtonOpportunityCostMapTemplate.setAlignment(Qt.AlignRight|Qt.AlignTop)
        self.buttonLoadOpportunityCostMapTemplate = QPushButton()
        self.buttonLoadOpportunityCostMapTemplate.setDisabled(True)
        self.buttonLoadOpportunityCostMapTemplate.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.buttonLoadOpportunityCostMapTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_LOAD))
        self.buttonSaveOpportunityCostMapTemplate = QPushButton()
        self.buttonSaveOpportunityCostMapTemplate.setDisabled(True)
        self.buttonSaveOpportunityCostMapTemplate.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.buttonSaveOpportunityCostMapTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_SAVE))
        self.buttonSaveAsOpportunityCostMapTemplate = QPushButton()
        self.buttonSaveAsOpportunityCostMapTemplate.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.buttonSaveAsOpportunityCostMapTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_SAVE_AS))
        self.layoutButtonOpportunityCostMapTemplate.addWidget(self.buttonLoadOpportunityCostMapTemplate)
        self.layoutButtonOpportunityCostMapTemplate.addWidget(self.buttonSaveOpportunityCostMapTemplate)
        self.layoutButtonOpportunityCostMapTemplate.addWidget(self.buttonSaveAsOpportunityCostMapTemplate)
        self.layoutGroupBoxOpportunityCostMapTemplate.addLayout(self.layoutButtonOpportunityCostMapTemplate)
        
        # Place the GroupBoxes
        self.layoutTabOpportunityCostMap.addWidget(self.groupBoxOCMParameters, 0, 0)
        self.layoutTabOpportunityCostMap.addLayout(self.layoutButtonOpportunityCostMap, 1, 0, 1, 2, Qt.AlignRight)
        self.layoutTabOpportunityCostMap.addWidget(self.groupBoxOpportunityCostMapTemplate, 0, 1, 1, 1)
        self.layoutTabOpportunityCostMap.setColumnStretch(0, 3)
        self.layoutTabOpportunityCostMap.setColumnStretch(1, 1) # Smaller template column
        
        
        #***********************************************************
        # Setup 'Regional Economy' tab
        #***********************************************************
        self.tabWidgetRegionalEconomy = QTabWidget()
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

        # self.tabInputOutputTable = QWidget()
        self.tabDescriptiveAnalysis = QWidget()
        self.tabRegionalEconomicScenarioImpact = QWidget()
        self.tabLandRequirementAnalysis = QWidget()
        self.tabLandUseChangeImpact = QWidget()
        
        # self.tabWidgetRegionalEconomy.addTab(self.tabInputOutputTable, 'Input-Output Table')
        self.tabWidgetRegionalEconomy.addTab(self.tabDescriptiveAnalysis, MenuFactory.getLabel(MenuFactory.TAREGECO_DESCRIPTIVE_ANALYSIS))
        self.tabWidgetRegionalEconomy.addTab(self.tabLandRequirementAnalysis, MenuFactory.getLabel(MenuFactory.TAREGECO_LAND_REQUIREMENT_ANALYSIS))
        self.tabWidgetRegionalEconomy.addTab(self.tabRegionalEconomicScenarioImpact, MenuFactory.getLabel(MenuFactory.TAREGECO_REGIONAL_ECONOMY_SCENARIO))
        self.tabWidgetRegionalEconomy.addTab(self.tabLandUseChangeImpact, MenuFactory.getLabel(MenuFactory.TAREGECO_LAND_USE_SCENARIO))
        
        self.layoutTabRegionalEconomy.addWidget(self.tabWidgetRegionalEconomy)
      
        # self.layoutTabInputOutputTable = QGridLayout()
        self.layoutTabDescriptiveAnalysis = QGridLayout()
        self.layoutTabRegionalEconomicScenarioImpact = QGridLayout()
        self.layoutTabLandRequirementAnalysis = QGridLayout()
        self.layoutTabLandUseChangeImpact = QGridLayout()
      
        # self.tabInputOutputTable.setLayout(self.layoutTabInputOutputTable)
        self.tabDescriptiveAnalysis.setLayout(self.layoutTabDescriptiveAnalysis)
        self.tabRegionalEconomicScenarioImpact.setLayout(self.layoutTabRegionalEconomicScenarioImpact)
        self.tabLandRequirementAnalysis.setLayout(self.layoutTabLandRequirementAnalysis)
        self.tabLandUseChangeImpact.setLayout(self.layoutTabLandUseChangeImpact)
        
        #***********************************************************
        # Setup 'Descriptive Analysis' tab
        #***********************************************************
        # Use QScrollArea
        ##self.layoutContentDescriptiveAnalysis = QVBoxLayout()
        self.layoutContentDescriptiveAnalysis = QGridLayout()
        self.contentDescriptiveAnalysis = QWidget()
        self.contentDescriptiveAnalysis.setLayout(self.layoutContentDescriptiveAnalysis)
        self.scrollDescriptiveAnalysis = QScrollArea()
        self.scrollDescriptiveAnalysis.setWidgetResizable(True);
        self.scrollDescriptiveAnalysis.setWidget(self.contentDescriptiveAnalysis)
        self.layoutTabDescriptiveAnalysis.addWidget(self.scrollDescriptiveAnalysis)
        
        # 'Single period' GroupBox
        self.groupBoxSinglePeriod = QGroupBox(MenuFactory.getLabel(MenuFactory.TAREGECO_INITIALIZE))
        self.layoutGroupBoxSinglePeriod = QVBoxLayout()
        self.layoutGroupBoxSinglePeriod.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.groupBoxSinglePeriod.setLayout(self.layoutGroupBoxSinglePeriod)
        self.layoutSinglePeriodInfo = QVBoxLayout()
        self.layoutSinglePeriod = QGridLayout()
        self.layoutGroupBoxSinglePeriod.addLayout(self.layoutSinglePeriodInfo)
        self.layoutGroupBoxSinglePeriod.addLayout(self.layoutSinglePeriod)
        
        self.labelSinglePeriodInfo = QLabel()
        self.labelSinglePeriodInfo.setText('\n')
        self.layoutSinglePeriodInfo.addWidget(self.labelSinglePeriodInfo)
        
        self.labelSingleIntermediateConsumptionMatrix = QLabel()
        self.labelSingleIntermediateConsumptionMatrix.setText(MenuFactory.getLabel(MenuFactory.TAREGECO_INTERMEDIATE_CONSUMPTION_MATRIX) + ':')
        self.layoutSinglePeriod.addWidget(self.labelSingleIntermediateConsumptionMatrix, 0, 0)
        
        self.comboBoxSingleIntermediateConsumptionMatrix = QComboBox()
        self.comboBoxSingleIntermediateConsumptionMatrix.setDisabled(True)
        self.layoutSinglePeriod.addWidget(self.comboBoxSingleIntermediateConsumptionMatrix, 0, 1)
        
        # self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxSingleIntermediateConsumptionMatrix)
        DialogLumensBase.handlerPopulateNameFromLookupData(parent, self.main.dataTable, self.comboBoxSingleIntermediateConsumptionMatrix)  
        
        self.labelSingleValueAddedMatrix = QLabel()
        self.labelSingleValueAddedMatrix.setText(MenuFactory.getLabel(MenuFactory.TAREGECO_VALUE_ADDED_MATRIX) + ':')
        self.layoutSinglePeriod.addWidget(self.labelSingleValueAddedMatrix, 1, 0)
        
        self.comboBoxSingleValueAddedMatrix = QComboBox()
        self.comboBoxSingleValueAddedMatrix.setDisabled(True)
        self.layoutSinglePeriod.addWidget(self.comboBoxSingleValueAddedMatrix, 1, 1)
        
        # self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxSingleValueAddedMatrix)
        DialogLumensBase.handlerPopulateNameFromLookupData(parent, self.main.dataTable, self.comboBoxSingleValueAddedMatrix)  
        
        self.labelSingleFinalConsumptionMatrix = QLabel()
        self.labelSingleFinalConsumptionMatrix.setText(MenuFactory.getLabel(MenuFactory.TAREGECO_FINAL_CONSUMPTION_MATRIX) + ':')
        self.layoutSinglePeriod.addWidget(self.labelSingleFinalConsumptionMatrix, 2, 0)
        
        self.comboBoxSingleFinalConsumptionMatrix = QComboBox()
        self.comboBoxSingleFinalConsumptionMatrix.setDisabled(True)
        self.layoutSinglePeriod.addWidget(self.comboBoxSingleFinalConsumptionMatrix, 2, 1)
        
        # self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxSingleFinalConsumptionMatrix)
        DialogLumensBase.handlerPopulateNameFromLookupData(parent, self.main.dataTable, self.comboBoxSingleFinalConsumptionMatrix)  
        
        
        self.labelOtherValueAddedComponent = QLabel()
        self.labelOtherValueAddedComponent.setText(MenuFactory.getLabel(MenuFactory.TAREGECO_VALUE_ADDED_COMPONENT) + ':')
        self.layoutSinglePeriod.addWidget(self.labelOtherValueAddedComponent, 3, 0)
        
        self.comboBoxOtherValueAddedComponent = QComboBox()
        self.comboBoxOtherValueAddedComponent.setDisabled(True)
        self.layoutSinglePeriod.addWidget(self.comboBoxOtherValueAddedComponent, 3, 1)
        
        # self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxOtherValueAddedComponent)
        DialogLumensBase.handlerPopulateNameFromLookupData(parent, self.main.dataTable, self.comboBoxOtherValueAddedComponent)  
        
        self.labelOtherFinalConsumptionComponent = QLabel()
        self.labelOtherFinalConsumptionComponent.setText(MenuFactory.getLabel(MenuFactory.TAREGECO_FINAL_CONSUMPTION_COMPONENT) + ':')
        self.layoutSinglePeriod.addWidget(self.labelOtherFinalConsumptionComponent, 4, 0)
        
        self.comboBoxOtherFinalConsumptionComponent = QComboBox()
        self.comboBoxOtherFinalConsumptionComponent.setDisabled(True)
        self.layoutSinglePeriod.addWidget(self.comboBoxOtherFinalConsumptionComponent, 4, 1)
        
        # self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxOtherFinalConsumptionComponent)
        DialogLumensBase.handlerPopulateNameFromLookupData(parent, self.main.dataTable, self.comboBoxOtherFinalConsumptionComponent)  
        
        self.labelOtherListOfEconomicSector = QLabel()
        self.labelOtherListOfEconomicSector.setText(MenuFactory.getLabel(MenuFactory.TAREGECO_LIST_OF_ECONOMIC_SECTOR) + ':')
        self.layoutSinglePeriod.addWidget(self.labelOtherListOfEconomicSector, 5, 0)
        
        self.comboBoxOtherListOfEconomicSector = QComboBox()
        self.comboBoxOtherListOfEconomicSector.setDisabled(True)
        self.layoutSinglePeriod.addWidget(self.comboBoxOtherListOfEconomicSector, 5, 1)
        
        # self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxOtherListOfEconomicSector)
        DialogLumensBase.handlerPopulateNameFromLookupData(parent, self.main.dataTable, self.comboBoxOtherListOfEconomicSector)  

        self.labelSingleLabourRequirement = QLabel()
        self.labelSingleLabourRequirement.setText(MenuFactory.getLabel(MenuFactory.TAREGECO_LABOUR_REQUIREMENT) + ':')
        self.layoutSinglePeriod.addWidget(self.labelSingleLabourRequirement, 6, 0)
        
        self.comboBoxSingleLabourRequirement = QComboBox()
        self.comboBoxSingleLabourRequirement.setDisabled(True)
        self.layoutSinglePeriod.addWidget(self.comboBoxSingleLabourRequirement, 6, 1)
        
        # self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxSingleLabourRequirement)
        DialogLumensBase.handlerPopulateNameFromLookupData(parent, self.main.dataTable, self.comboBoxSingleLabourRequirement)  
        
        self.labelOtherFinancialUnit = QLabel()
        self.labelOtherFinancialUnit.setText(MenuFactory.getLabel(MenuFactory.TAREGECO_FINANCIAL_UNIT) + ':')
        self.layoutSinglePeriod.addWidget(self.labelOtherFinancialUnit, 7, 0)
        
        self.lineEditOtherFinancialUnit = QLineEdit()
        self.lineEditOtherFinancialUnit.setText(MenuFactory.getLabel(MenuFactory.TAREGECO_CURRENCY))
        self.layoutSinglePeriod.addWidget(self.lineEditOtherFinancialUnit, 7, 1)
        self.labelOtherFinancialUnit.setBuddy(self.lineEditOtherFinancialUnit)
        
        self.labelOtherAreaName = QLabel()
        self.labelOtherAreaName.setText(MenuFactory.getLabel(MenuFactory.TAREGECO_AREA_NAME) + ':')
        self.layoutSinglePeriod.addWidget(self.labelOtherAreaName, 8, 0)
        
        self.lineEditOtherAreaName = QLineEdit()
        self.lineEditOtherAreaName.setText(MenuFactory.getLabel(MenuFactory.TAREGECO_AREA))
        self.layoutSinglePeriod.addWidget(self.lineEditOtherAreaName, 8, 1)
        self.labelOtherAreaName.setBuddy(self.lineEditOtherAreaName)
        
        self.labelSinglePeriod = QLabel()
        self.labelSinglePeriod.setText(MenuFactory.getLabel(MenuFactory.TAREGECO_YEAR) + ':')
        self.layoutSinglePeriod.addWidget(self.labelSinglePeriod, 9, 0)
        
        self.spinBoxSinglePeriod = QSpinBox()
        self.spinBoxSinglePeriod.setRange(1, 9999)
        td = datetime.date.today()
        self.spinBoxSinglePeriod.setValue(td.year)
        self.layoutSinglePeriod.addWidget(self.spinBoxSinglePeriod, 9, 1)
        self.labelSinglePeriod.setBuddy(self.spinBoxSinglePeriod)        
        
        # Process tab button
        self.layoutButtonDescriptiveAnalysis = QHBoxLayout()
        self.buttonProcessDescriptiveAnalysis = QPushButton()
        self.buttonProcessDescriptiveAnalysis.setText('&' + MenuFactory.getLabel(MenuFactory.TAREGECO_LAND_USE_SCENARIO))
        icon = QIcon(':/ui/icons/iconActionHelp.png')
        self.buttonHelpTADescriptiveAnalysis = QPushButton()
        self.buttonHelpTADescriptiveAnalysis.setIcon(icon)
        self.layoutButtonDescriptiveAnalysis.setAlignment(Qt.AlignRight)
        self.layoutButtonDescriptiveAnalysis.addWidget(self.buttonProcessDescriptiveAnalysis)
        self.layoutButtonDescriptiveAnalysis.addWidget(self.buttonHelpTADescriptiveAnalysis)
        
        # Template GroupBox
        self.groupBoxDescriptiveAnalysisTemplate = QGroupBox(MenuFactory.getLabel(MenuFactory.CONF_TITLE))
        self.layoutGroupBoxDescriptiveAnalysisTemplate = QVBoxLayout()
        self.layoutGroupBoxDescriptiveAnalysisTemplate.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.groupBoxDescriptiveAnalysisTemplate.setLayout(self.layoutGroupBoxDescriptiveAnalysisTemplate)
        self.layoutDescriptiveAnalysisTemplateInfo = QVBoxLayout()
        self.layoutDescriptiveAnalysisTemplate = QGridLayout()
        self.layoutGroupBoxDescriptiveAnalysisTemplate.addLayout(self.layoutDescriptiveAnalysisTemplateInfo)
        self.layoutGroupBoxDescriptiveAnalysisTemplate.addLayout(self.layoutDescriptiveAnalysisTemplate)
        
        self.labelLoadedDescriptiveAnalysisTemplate = QLabel()
        self.labelLoadedDescriptiveAnalysisTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_LOADED_CONFIGURATION) + ':')
        self.layoutDescriptiveAnalysisTemplate.addWidget(self.labelLoadedDescriptiveAnalysisTemplate, 0, 0)
        
        self.loadedDescriptiveAnalysisTemplate = QLabel()
        self.loadedDescriptiveAnalysisTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NONE))
        self.layoutDescriptiveAnalysisTemplate.addWidget(self.loadedDescriptiveAnalysisTemplate, 0, 1)
        
        self.labelDescriptiveAnalysisTemplate = QLabel()
        self.labelDescriptiveAnalysisTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NAME) + ':')
        self.layoutDescriptiveAnalysisTemplate.addWidget(self.labelDescriptiveAnalysisTemplate, 1, 0)
        
        self.comboBoxDescriptiveAnalysisTemplate = QComboBox()
        self.comboBoxDescriptiveAnalysisTemplate.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.comboBoxDescriptiveAnalysisTemplate.setDisabled(True)
        self.comboBoxDescriptiveAnalysisTemplate.addItem(MenuFactory.getLabel(MenuFactory.CONF_NO_FOUND))
        self.layoutDescriptiveAnalysisTemplate.addWidget(self.comboBoxDescriptiveAnalysisTemplate, 1, 1)
        
        self.layoutButtonDescriptiveAnalysisTemplate = QHBoxLayout()
        self.layoutButtonDescriptiveAnalysisTemplate.setAlignment(Qt.AlignRight|Qt.AlignTop)
        self.buttonLoadDescriptiveAnalysisTemplate = QPushButton()
        self.buttonLoadDescriptiveAnalysisTemplate.setDisabled(True)
        self.buttonLoadDescriptiveAnalysisTemplate.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.buttonLoadDescriptiveAnalysisTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_LOAD))
        self.buttonSaveDescriptiveAnalysisTemplate = QPushButton()
        self.buttonSaveDescriptiveAnalysisTemplate.setDisabled(True)
        self.buttonSaveDescriptiveAnalysisTemplate.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.buttonSaveDescriptiveAnalysisTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_SAVE))
        self.buttonSaveAsDescriptiveAnalysisTemplate = QPushButton()
        self.buttonSaveAsDescriptiveAnalysisTemplate.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.buttonSaveAsDescriptiveAnalysisTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_SAVE_AS))
        self.layoutButtonDescriptiveAnalysisTemplate.addWidget(self.buttonLoadDescriptiveAnalysisTemplate)
        self.layoutButtonDescriptiveAnalysisTemplate.addWidget(self.buttonSaveDescriptiveAnalysisTemplate)
        self.layoutButtonDescriptiveAnalysisTemplate.addWidget(self.buttonSaveAsDescriptiveAnalysisTemplate)
        self.layoutGroupBoxDescriptiveAnalysisTemplate.addLayout(self.layoutButtonDescriptiveAnalysisTemplate)
        
        # Place the GroupBoxes
        self.layoutContentDescriptiveAnalysis.addWidget(self.groupBoxSinglePeriod, 0, 0)
        self.layoutContentDescriptiveAnalysis.addLayout(self.layoutButtonDescriptiveAnalysis, 3, 0, 1, 2, Qt.AlignRight)
        self.layoutContentDescriptiveAnalysis.addWidget(self.groupBoxDescriptiveAnalysisTemplate, 0, 1, 3, 1)
        self.layoutContentDescriptiveAnalysis.setColumnStretch(0, 3)
        self.layoutContentDescriptiveAnalysis.setColumnStretch(1, 1) # Smaller template column
        
        
        #***********************************************************
        # Setup 'Land Requirement Analysis' tab
        #***********************************************************
        # Use QScrollArea
        ##self.layoutContentLandRequirementAnalysis = QVBoxLayout()
        self.layoutContentLandRequirementAnalysis = QGridLayout()
        self.contentLandRequirementAnalysis = QWidget()
        self.contentLandRequirementAnalysis.setLayout(self.layoutContentLandRequirementAnalysis)
        self.scrollLandRequirementAnalysis = QScrollArea()
        self.scrollLandRequirementAnalysis.setWidgetResizable(True);
        self.scrollLandRequirementAnalysis.setWidget(self.contentLandRequirementAnalysis)
        self.layoutTabLandRequirementAnalysis.addWidget(self.scrollLandRequirementAnalysis)
        
        # Parameters 'GroupBox'
        self.groupBoxLandRequirementAnalysisParameters = QGroupBox(MenuFactory.getLabel(MenuFactory.TAOPCOST_PARAMETERIZATION))
        self.layoutGroupBoxLandRequirementAnalysisParameters = QVBoxLayout()
        self.layoutGroupBoxLandRequirementAnalysisParameters.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.groupBoxLandRequirementAnalysisParameters.setLayout(self.layoutGroupBoxLandRequirementAnalysisParameters)
        self.layoutLandRequirementAnalysisParametersInfo = QVBoxLayout()
        self.layoutLandRequirementAnalysisParameters = QGridLayout()
        self.layoutGroupBoxLandRequirementAnalysisParameters.addLayout(self.layoutLandRequirementAnalysisParametersInfo)
        self.layoutGroupBoxLandRequirementAnalysisParameters.addLayout(self.layoutLandRequirementAnalysisParameters)
        
        self.labelLandRequirementAnalysisParametersInfo = QLabel()
        self.labelLandRequirementAnalysisParametersInfo.setText('\n')
        self.layoutLandRequirementAnalysisParametersInfo.addWidget(self.labelLandRequirementAnalysisParametersInfo)
        
        self.labelLandRequirementAnalysisLandUseCover = QLabel()
        self.labelLandRequirementAnalysisLandUseCover.setText(MenuFactory.getLabel(MenuFactory.TAREGECO_CURRENT_LAND_COVER_MAP) + ':')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.labelLandRequirementAnalysisLandUseCover, 0, 0)
        
        self.comboBoxLandRequirementAnalysisLandUseCover = QComboBox()
        self.comboBoxLandRequirementAnalysisLandUseCover.setDisabled(True)
        self.layoutLandRequirementAnalysisParameters.addWidget(self.comboBoxLandRequirementAnalysisLandUseCover, 0, 1)
        
        # self.handlerPopulateNameFromLookupData(self.main.dataLandUseCover, self.comboBoxLandRequirementAnalysisLandUseCover)
        DialogLumensBase.handlerPopulateNameFromLookupData(parent, self.main.dataLandUseCover, self.comboBoxLandRequirementAnalysisLandUseCover)  
        
        self.labelLandRequirementAnalysisLookupTable = QLabel()
        self.labelLandRequirementAnalysisLookupTable.setText(MenuFactory.getLabel(MenuFactory.TAREGECO_LAND_REQUIREMENT_LOOKUP_TABLE) + ':')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.labelLandRequirementAnalysisLookupTable, 1, 0)
        
        self.comboBoxLandRequirementAnalysisLookupTable = QComboBox()
        self.comboBoxLandRequirementAnalysisLookupTable.setDisabled(True)
        self.layoutLandRequirementAnalysisParameters.addWidget(self.comboBoxLandRequirementAnalysisLookupTable, 1, 1)
        
        # self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxLandRequirementAnalysisLookupTable)
        DialogLumensBase.handlerPopulateNameFromLookupData(parent, self.main.dataTable, self.comboBoxLandRequirementAnalysisLookupTable)  
        
        self.labelLandRequirementAnalysisDescriptiveOutput = QLabel()
        self.labelLandRequirementAnalysisDescriptiveOutput.setText(MenuFactory.getLabel(MenuFactory.TAREGECO_DESCRIPTIVE_ANALYSIS_OUTPUT) + ':')
        self.layoutLandRequirementAnalysisParameters.addWidget(self.labelLandRequirementAnalysisDescriptiveOutput, 2, 0)
        
        self.lineEditLandRequirementAnalysisDescriptiveOutput = QLineEdit()
        self.lineEditLandRequirementAnalysisDescriptiveOutput.setReadOnly(True)
        self.layoutLandRequirementAnalysisParameters.addWidget(self.lineEditLandRequirementAnalysisDescriptiveOutput, 2, 1)
        
        self.buttonSelectLandRequirementAnalysisDescriptiveOutput = QPushButton()
        self.buttonSelectLandRequirementAnalysisDescriptiveOutput.setText(MenuFactory.getLabel(MenuFactory.TA_BROWSE))
        self.layoutLandRequirementAnalysisParameters.addWidget(self.buttonSelectLandRequirementAnalysisDescriptiveOutput, 2, 2)
        
        # Process tab button
        self.layoutButtonLandRequirementAnalysis = QHBoxLayout()
        self.buttonProcessLandRequirementAnalysis = QPushButton()
        self.buttonProcessLandRequirementAnalysis.setText(MenuFactory.getLabel(MenuFactory.TA_PROCESS))
        self.buttonHelpTALandRequirementAnalysis = QPushButton()
        self.buttonHelpTALandRequirementAnalysis.setIcon(icon)
        self.layoutButtonLandRequirementAnalysis.setAlignment(Qt.AlignRight)
        self.layoutButtonLandRequirementAnalysis.addWidget(self.buttonProcessLandRequirementAnalysis)
        self.layoutButtonLandRequirementAnalysis.addWidget(self.buttonHelpTALandRequirementAnalysis)
        
        # Template GroupBox
        self.groupBoxLandRequirementAnalysisTemplate = QGroupBox(MenuFactory.getLabel(MenuFactory.CONF_TITLE))
        self.layoutGroupBoxLandRequirementAnalysisTemplate = QVBoxLayout()
        self.layoutGroupBoxLandRequirementAnalysisTemplate.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.groupBoxLandRequirementAnalysisTemplate.setLayout(self.layoutGroupBoxLandRequirementAnalysisTemplate)
        self.layoutLandRequirementAnalysisTemplateInfo = QVBoxLayout()
        self.layoutLandRequirementAnalysisTemplate = QGridLayout()
        self.layoutGroupBoxLandRequirementAnalysisTemplate.addLayout(self.layoutLandRequirementAnalysisTemplateInfo)
        self.layoutGroupBoxLandRequirementAnalysisTemplate.addLayout(self.layoutLandRequirementAnalysisTemplate)
        
        self.labelLoadedLandRequirementAnalysisTemplate = QLabel()
        self.labelLoadedLandRequirementAnalysisTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_LOADED_CONFIGURATION) + ':')
        self.layoutLandRequirementAnalysisTemplate.addWidget(self.labelLoadedLandRequirementAnalysisTemplate, 0, 0)
        
        self.loadedLandRequirementAnalysisTemplate = QLabel()
        self.loadedLandRequirementAnalysisTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NONE))
        self.layoutLandRequirementAnalysisTemplate.addWidget(self.loadedLandRequirementAnalysisTemplate, 0, 1)
        
        self.labelLandRequirementAnalysisTemplate = QLabel()
        self.labelLandRequirementAnalysisTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NAME) + ':')
        self.layoutLandRequirementAnalysisTemplate.addWidget(self.labelLandRequirementAnalysisTemplate, 1, 0)
        
        self.comboBoxLandRequirementAnalysisTemplate = QComboBox()
        self.comboBoxLandRequirementAnalysisTemplate.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.comboBoxLandRequirementAnalysisTemplate.setDisabled(True)
        self.comboBoxLandRequirementAnalysisTemplate.addItem(MenuFactory.getLabel(MenuFactory.CONF_NO_FOUND))
        self.layoutLandRequirementAnalysisTemplate.addWidget(self.comboBoxLandRequirementAnalysisTemplate, 1, 1)
        
        self.layoutButtonLandRequirementAnalysisTemplate = QHBoxLayout()
        self.layoutButtonLandRequirementAnalysisTemplate.setAlignment(Qt.AlignRight|Qt.AlignTop)
        self.buttonLoadLandRequirementAnalysisTemplate = QPushButton()
        self.buttonLoadLandRequirementAnalysisTemplate.setDisabled(True)
        self.buttonLoadLandRequirementAnalysisTemplate.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.buttonLoadLandRequirementAnalysisTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_LOAD))
        self.buttonSaveLandRequirementAnalysisTemplate = QPushButton()
        self.buttonSaveLandRequirementAnalysisTemplate.setDisabled(True)
        self.buttonSaveLandRequirementAnalysisTemplate.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.buttonSaveLandRequirementAnalysisTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_SAVE))
        self.buttonSaveAsLandRequirementAnalysisTemplate = QPushButton()
        self.buttonSaveAsLandRequirementAnalysisTemplate.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.buttonSaveAsLandRequirementAnalysisTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_SAVE_AS))
        self.layoutButtonLandRequirementAnalysisTemplate.addWidget(self.buttonLoadLandRequirementAnalysisTemplate)
        self.layoutButtonLandRequirementAnalysisTemplate.addWidget(self.buttonSaveLandRequirementAnalysisTemplate)
        self.layoutButtonLandRequirementAnalysisTemplate.addWidget(self.buttonSaveAsLandRequirementAnalysisTemplate)
        self.layoutGroupBoxLandRequirementAnalysisTemplate.addLayout(self.layoutButtonLandRequirementAnalysisTemplate)
        
        # Place the GroupBoxes
        self.layoutContentLandRequirementAnalysis.addWidget(self.groupBoxLandRequirementAnalysisParameters, 0, 0)
        self.layoutContentLandRequirementAnalysis.addLayout(self.layoutButtonLandRequirementAnalysis, 1, 0, 1, 2, Qt.AlignRight)
        self.layoutContentLandRequirementAnalysis.addWidget(self.groupBoxLandRequirementAnalysisTemplate, 0, 1, 1, 1)
        self.layoutContentLandRequirementAnalysis.setColumnStretch(0, 3)
        self.layoutContentLandRequirementAnalysis.setColumnStretch(1, 1) # Smaller template column


        #***********************************************************
        # Setup 'Regional Economic Scenario' tab
        #***********************************************************
        # Use QScrollArea
        ##self.layoutContentRegionalEconomicScenarioImpact = QVBoxLayout()
        self.layoutContentRegionalEconomicScenarioImpact = QGridLayout()
        self.contentRegionalEconomicScenarioImpact = QWidget()
        self.contentRegionalEconomicScenarioImpact.setLayout(self.layoutContentRegionalEconomicScenarioImpact)
        self.scrollRegionalEconomicScenarioImpact = QScrollArea()
        self.scrollRegionalEconomicScenarioImpact.setWidgetResizable(True);
        self.scrollRegionalEconomicScenarioImpact.setWidget(self.contentRegionalEconomicScenarioImpact)
        self.layoutTabRegionalEconomicScenarioImpact.addWidget(self.scrollRegionalEconomicScenarioImpact)
        
        # 'Type' GroupBox
        self.groupBoxRegionalEconomicScenarioImpactType = QGroupBox(MenuFactory.getLabel(MenuFactory.TAREGECO_SCENARIO_TYPE))
        self.layoutGroupBoxRegionalEconomicScenarioImpactType = QVBoxLayout()
        self.layoutGroupBoxRegionalEconomicScenarioImpactType.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.groupBoxRegionalEconomicScenarioImpactType.setLayout(self.layoutGroupBoxRegionalEconomicScenarioImpactType)
        self.layoutRegionalEconomicScenarioImpactTypeInfo = QVBoxLayout()
        self.layoutRegionalEconomicScenarioImpactType = QGridLayout()
        self.layoutGroupBoxRegionalEconomicScenarioImpactType.addLayout(self.layoutRegionalEconomicScenarioImpactTypeInfo)
        self.layoutGroupBoxRegionalEconomicScenarioImpactType.addLayout(self.layoutRegionalEconomicScenarioImpactType)
        
        self.labelRegionalEconomicScenarioImpactTypeInfo = QLabel()
        self.labelRegionalEconomicScenarioImpactTypeInfo.setText('\n')
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.labelRegionalEconomicScenarioImpactTypeInfo)        
        
        self.labelRegionalEconomicScenarioLandRequirement = QLabel()
        self.labelRegionalEconomicScenarioLandRequirement.setText(MenuFactory.getLabel(MenuFactory.TAREGECO_LAND_REQUIREMENT))
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.labelRegionalEconomicScenarioLandRequirement, 0, 0)
        
        self.lineEditRegionalEconomicScenarioLandRequirement = QLineEdit()
        self.lineEditRegionalEconomicScenarioLandRequirement.setReadOnly(True)
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.lineEditRegionalEconomicScenarioLandRequirement, 0, 1)
        
        self.buttonSelectRegionalEconomicScenarioLandRequirement = QPushButton()
        self.buttonSelectRegionalEconomicScenarioLandRequirement.setText(MenuFactory.getLabel(MenuFactory.TA_BROWSE))
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.buttonSelectRegionalEconomicScenarioLandRequirement, 0, 2)        
        
        self.checkBoxRegionalEconomicScenarioImpactFinalDemand = QCheckBox(MenuFactory.getLabel(MenuFactory.TAREGECO_FINAL_DEMAND_SCENARIO))
        self.checkBoxRegionalEconomicScenarioImpactFinalDemand.setChecked(True)
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.checkBoxRegionalEconomicScenarioImpactFinalDemand, 1, 0)
        
        self.labelRegionalEconomicScenarioImpactFinalDemandChangeScenario = QLabel()
        self.labelRegionalEconomicScenarioImpactFinalDemandChangeScenario.setText(MenuFactory.getLabel(MenuFactory.TAREGECO_FINAL_DEMAND_LOOKUP_TABLE) + ':')
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.labelRegionalEconomicScenarioImpactFinalDemandChangeScenario, 2, 0)
        
        self.comboBoxRegionalEconomicScenarioImpactFinalDemandChangeScenario = QComboBox()
        self.comboBoxRegionalEconomicScenarioImpactFinalDemandChangeScenario.setDisabled(True)
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.comboBoxRegionalEconomicScenarioImpactFinalDemandChangeScenario, 2, 1)
        
        # self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxRegionalEconomicScenarioImpactFinalDemandChangeScenario)
        DialogLumensBase.handlerPopulateNameFromLookupData(parent, self.main.dataTable, self.comboBoxRegionalEconomicScenarioImpactFinalDemandChangeScenario)  
        
        self.checkBoxRegionalEconomicScenarioImpactGDP = QCheckBox(MenuFactory.getLabel(MenuFactory.TAREGECO_GDP_SCENARIO))
        self.checkBoxRegionalEconomicScenarioImpactGDP.setChecked(False)
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.checkBoxRegionalEconomicScenarioImpactGDP, 3, 0)
        
        self.labelRegionalEconomicScenarioImpactGDPChangeScenario = QLabel()
        self.labelRegionalEconomicScenarioImpactGDPChangeScenario.setText(MenuFactory.getLabel(MenuFactory.TAREGECO_GDP_LOOKUP))
        self.labelRegionalEconomicScenarioImpactGDPChangeScenario.setDisabled(True)
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.labelRegionalEconomicScenarioImpactGDPChangeScenario, 4, 0)
        
        self.comboBoxRegionalEconomicScenarioImpactGDPChangeScenario = QComboBox()
        self.comboBoxRegionalEconomicScenarioImpactGDPChangeScenario.setDisabled(True)
        self.layoutRegionalEconomicScenarioImpactType.addWidget(self.comboBoxRegionalEconomicScenarioImpactGDPChangeScenario, 4, 1)
        
        # self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxRegionalEconomicScenarioImpactGDPChangeScenario)
        DialogLumensBase.handlerPopulateNameFromLookupData(parent, self.main.dataTable, self.comboBoxRegionalEconomicScenarioImpactGDPChangeScenario)  
        
        # Process tab button
        self.layoutButtonRegionalEconomicScenarioImpact = QHBoxLayout()
        self.buttonProcessRegionalEconomicScenarioImpact = QPushButton()
        self.buttonProcessRegionalEconomicScenarioImpact.setText(MenuFactory.getLabel(MenuFactory.TA_PROCESS))
        self.buttonHelpTARegionalEconomicScenarioImpact = QPushButton()
        self.buttonHelpTARegionalEconomicScenarioImpact.setIcon(icon)
        self.layoutButtonRegionalEconomicScenarioImpact.setAlignment(Qt.AlignRight)
        self.layoutButtonRegionalEconomicScenarioImpact.addWidget(self.buttonProcessRegionalEconomicScenarioImpact)
        self.layoutButtonRegionalEconomicScenarioImpact.addWidget(self.buttonHelpTARegionalEconomicScenarioImpact)
        
        # Template GroupBox
        self.groupBoxRegionalEconomicScenarioImpactTemplate = QGroupBox(MenuFactory.getLabel(MenuFactory.CONF_TITLE))
        self.layoutGroupBoxRegionalEconomicScenarioImpactTemplate = QVBoxLayout()
        self.layoutGroupBoxRegionalEconomicScenarioImpactTemplate.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.groupBoxRegionalEconomicScenarioImpactTemplate.setLayout(self.layoutGroupBoxRegionalEconomicScenarioImpactTemplate)
        self.layoutRegionalEconomicScenarioImpactTemplateInfo = QVBoxLayout()
        self.layoutRegionalEconomicScenarioImpactTemplate = QGridLayout()
        self.layoutGroupBoxRegionalEconomicScenarioImpactTemplate.addLayout(self.layoutRegionalEconomicScenarioImpactTemplateInfo)
        self.layoutGroupBoxRegionalEconomicScenarioImpactTemplate.addLayout(self.layoutRegionalEconomicScenarioImpactTemplate)
        
        self.labelLoadedRegionalEconomicScenarioImpactTemplate = QLabel()
        self.labelLoadedRegionalEconomicScenarioImpactTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_LOADED_CONFIGURATION) + ':')
        self.layoutRegionalEconomicScenarioImpactTemplate.addWidget(self.labelLoadedRegionalEconomicScenarioImpactTemplate, 0, 0)
        
        self.loadedRegionalEconomicScenarioImpactTemplate = QLabel()
        self.loadedRegionalEconomicScenarioImpactTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NONE))
        self.layoutRegionalEconomicScenarioImpactTemplate.addWidget(self.loadedRegionalEconomicScenarioImpactTemplate, 0, 1)
        
        self.labelRegionalEconomicScenarioImpactTemplate = QLabel()
        self.labelRegionalEconomicScenarioImpactTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NAME) + ':')
        self.layoutRegionalEconomicScenarioImpactTemplate.addWidget(self.labelRegionalEconomicScenarioImpactTemplate, 1, 0)
        
        self.comboBoxRegionalEconomicScenarioImpactTemplate = QComboBox()
        self.comboBoxRegionalEconomicScenarioImpactTemplate.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.comboBoxRegionalEconomicScenarioImpactTemplate.setDisabled(True)
        self.comboBoxRegionalEconomicScenarioImpactTemplate.addItem(MenuFactory.getLabel(MenuFactory.CONF_NO_FOUND))
        self.layoutRegionalEconomicScenarioImpactTemplate.addWidget(self.comboBoxRegionalEconomicScenarioImpactTemplate, 1, 1)
        
        self.layoutButtonRegionalEconomicScenarioImpactTemplate = QHBoxLayout()
        self.layoutButtonRegionalEconomicScenarioImpactTemplate.setAlignment(Qt.AlignRight|Qt.AlignTop)
        self.buttonLoadRegionalEconomicScenarioImpactTemplate = QPushButton()
        self.buttonLoadRegionalEconomicScenarioImpactTemplate.setDisabled(True)
        self.buttonLoadRegionalEconomicScenarioImpactTemplate.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.buttonLoadRegionalEconomicScenarioImpactTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_LOAD))
        self.buttonSaveRegionalEconomicScenarioImpactTemplate = QPushButton()
        self.buttonSaveRegionalEconomicScenarioImpactTemplate.setDisabled(True)
        self.buttonSaveRegionalEconomicScenarioImpactTemplate.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.buttonSaveRegionalEconomicScenarioImpactTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_SAVE))
        self.buttonSaveAsRegionalEconomicScenarioImpactTemplate = QPushButton()
        self.buttonSaveAsRegionalEconomicScenarioImpactTemplate.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.buttonSaveAsRegionalEconomicScenarioImpactTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_SAVE_AS))
        self.layoutButtonRegionalEconomicScenarioImpactTemplate.addWidget(self.buttonLoadRegionalEconomicScenarioImpactTemplate)
        self.layoutButtonRegionalEconomicScenarioImpactTemplate.addWidget(self.buttonSaveRegionalEconomicScenarioImpactTemplate)
        self.layoutButtonRegionalEconomicScenarioImpactTemplate.addWidget(self.buttonSaveAsRegionalEconomicScenarioImpactTemplate)
        self.layoutGroupBoxRegionalEconomicScenarioImpactTemplate.addLayout(self.layoutButtonRegionalEconomicScenarioImpactTemplate)
        
        # Place the GroupBoxes
        self.layoutContentRegionalEconomicScenarioImpact.addWidget(self.groupBoxRegionalEconomicScenarioImpactType, 0, 0)
        self.layoutContentRegionalEconomicScenarioImpact.addLayout(self.layoutButtonRegionalEconomicScenarioImpact, 2, 0, 1, 2, Qt.AlignRight)
        self.layoutContentRegionalEconomicScenarioImpact.addWidget(self.groupBoxRegionalEconomicScenarioImpactTemplate, 0, 1, 2, 1)
        self.layoutContentRegionalEconomicScenarioImpact.setColumnStretch(0, 3)
        self.layoutContentRegionalEconomicScenarioImpact.setColumnStretch(1, 1) # Smaller template column

        
        #***********************************************************
        # Setup 'Land Use Scenario' tab
        #***********************************************************
        # Use QScrollArea
        ##self.layoutContentLandUseChangeImpact = QVBoxLayout()
        self.layoutContentLandUseChangeImpact = QGridLayout()
        self.contentLandUseChangeImpact = QWidget()
        self.contentLandUseChangeImpact.setLayout(self.layoutContentLandUseChangeImpact)
        self.scrollLandUseChangeImpact = QScrollArea()
        self.scrollLandUseChangeImpact.setWidgetResizable(True);
        self.scrollLandUseChangeImpact.setWidget(self.contentLandUseChangeImpact)
        self.layoutTabLandUseChangeImpact.addWidget(self.scrollLandUseChangeImpact)
        
        # Parameters 'GroupBox'
        self.groupBoxLandUseChangeImpactParameters = QGroupBox(MenuFactory.getLabel(MenuFactory.TAOPCOST_PARAMETERIZATION))
        self.layoutGroupBoxLandUseChangeImpactParameters = QVBoxLayout()
        self.layoutGroupBoxLandUseChangeImpactParameters.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.groupBoxLandUseChangeImpactParameters.setLayout(self.layoutGroupBoxLandUseChangeImpactParameters)
        self.layoutLandUseChangeImpactParametersInfo = QVBoxLayout()
        self.layoutLandUseChangeImpactParameters = QGridLayout()
        self.layoutGroupBoxLandUseChangeImpactParameters.addLayout(self.layoutLandUseChangeImpactParametersInfo)
        self.layoutGroupBoxLandUseChangeImpactParameters.addLayout(self.layoutLandUseChangeImpactParameters)
        
        self.labelLandUseChangeImpactParametersInfo = QLabel()
        self.labelLandUseChangeImpactParametersInfo.setText('\n')
        self.layoutLandUseChangeImpactParametersInfo.addWidget(self.labelLandUseChangeImpactParametersInfo)
        
        self.labelLandUseChangeLandRequirement = QLabel()
        self.labelLandUseChangeLandRequirement.setText(MenuFactory.getLabel(MenuFactory.TAREGECO_LAND_REQUIREMENT))
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelLandUseChangeLandRequirement, 0, 0)
        
        self.lineEditLandUseChangeLandRequirement = QLineEdit()
        self.lineEditLandUseChangeLandRequirement.setReadOnly(True)
        self.layoutLandUseChangeImpactParameters.addWidget(self.lineEditLandUseChangeLandRequirement, 0, 1)
        
        self.buttonSelectLandUseChangeLandRequirement = QPushButton()
        self.buttonSelectLandUseChangeLandRequirement.setText(MenuFactory.getLabel(MenuFactory.TA_BROWSE))
        self.layoutLandUseChangeImpactParameters.addWidget(self.buttonSelectLandUseChangeLandRequirement, 0, 2)
        
        self.labelSelectLandUseChangeMap = QLabel()
        self.labelSelectLandUseChangeMap.setText(MenuFactory.getLabel(MenuFactory.TAREGECO_PROJECTED_LAND_COVER_MAP) + ':')
        self.layoutLandUseChangeImpactParameters.addWidget(self.labelSelectLandUseChangeMap, 1, 0)
        
        self.comboBoxSelectLandUseChangeMap = QComboBox()
        self.comboBoxSelectLandUseChangeMap.setDisabled(True)
        self.layoutLandUseChangeImpactParameters.addWidget(self.comboBoxSelectLandUseChangeMap, 1, 1)
        
        # self.handlerPopulateNameFromLookupData(self.main.dataLandUseCover, self.comboBoxSelectLandUseChangeMap)
        DialogLumensBase.handlerPopulateNameFromLookupData(parent, self.main.dataLandUseCover, self.comboBoxSelectLandUseChangeMap)  
        
        # Process tab button
        self.layoutButtonLandUseChangeImpact = QHBoxLayout()
        self.buttonProcessLandUseChangeImpact = QPushButton()
        self.buttonProcessLandUseChangeImpact.setText(MenuFactory.getLabel(MenuFactory.TA_PROCESS))
        self.buttonHelpTALandUseChangeImpact = QPushButton()
        self.buttonHelpTALandUseChangeImpact.setIcon(icon)
        self.layoutButtonLandUseChangeImpact.setAlignment(Qt.AlignRight)
        self.layoutButtonLandUseChangeImpact.addWidget(self.buttonProcessLandUseChangeImpact)
        self.layoutButtonLandUseChangeImpact.addWidget(self.buttonHelpTALandUseChangeImpact)
        
        # Template GroupBox
        self.groupBoxLandUseChangeImpactTemplate = QGroupBox(MenuFactory.getLabel(MenuFactory.CONF_TITLE))
        self.layoutGroupBoxLandUseChangeImpactTemplate = QVBoxLayout()
        self.layoutGroupBoxLandUseChangeImpactTemplate.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.groupBoxLandUseChangeImpactTemplate.setLayout(self.layoutGroupBoxLandUseChangeImpactTemplate)
        self.layoutLandUseChangeImpactTemplateInfo = QVBoxLayout()
        self.layoutLandUseChangeImpactTemplate = QGridLayout()
        self.layoutGroupBoxLandUseChangeImpactTemplate.addLayout(self.layoutLandUseChangeImpactTemplateInfo)
        self.layoutGroupBoxLandUseChangeImpactTemplate.addLayout(self.layoutLandUseChangeImpactTemplate)
        
        self.labelLoadedLandUseChangeImpactTemplate = QLabel()
        self.labelLoadedLandUseChangeImpactTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_LOADED_CONFIGURATION) + ':')
        self.layoutLandUseChangeImpactTemplate.addWidget(self.labelLoadedLandUseChangeImpactTemplate, 0, 0)
        
        self.loadedLandUseChangeImpactTemplate = QLabel()
        self.loadedLandUseChangeImpactTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NONE))
        self.layoutLandUseChangeImpactTemplate.addWidget(self.loadedLandUseChangeImpactTemplate, 0, 1)
        
        self.labelLandUseChangeImpactTemplate = QLabel()
        self.labelLandUseChangeImpactTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_NAME) + ':')
        self.layoutLandUseChangeImpactTemplate.addWidget(self.labelLandUseChangeImpactTemplate, 1, 0)
        
        self.comboBoxLandUseChangeImpactTemplate = QComboBox()
        self.comboBoxLandUseChangeImpactTemplate.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.comboBoxLandUseChangeImpactTemplate.setDisabled(True)
        self.comboBoxLandUseChangeImpactTemplate.addItem(MenuFactory.getLabel(MenuFactory.CONF_NO_FOUND))
        self.layoutLandUseChangeImpactTemplate.addWidget(self.comboBoxLandUseChangeImpactTemplate, 1, 1)
        
        self.layoutButtonLandUseChangeImpactTemplate = QHBoxLayout()
        self.layoutButtonLandUseChangeImpactTemplate.setAlignment(Qt.AlignRight|Qt.AlignTop)
        self.buttonLoadLandUseChangeImpactTemplate = QPushButton()
        self.buttonLoadLandUseChangeImpactTemplate.setDisabled(True)
        self.buttonLoadLandUseChangeImpactTemplate.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.buttonLoadLandUseChangeImpactTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_LOAD))
        self.buttonSaveLandUseChangeImpactTemplate = QPushButton()
        self.buttonSaveLandUseChangeImpactTemplate.setDisabled(True)
        self.buttonSaveLandUseChangeImpactTemplate.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.buttonSaveLandUseChangeImpactTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_SAVE))
        self.buttonSaveAsLandUseChangeImpactTemplate = QPushButton()
        self.buttonSaveAsLandUseChangeImpactTemplate.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.buttonSaveAsLandUseChangeImpactTemplate.setText(MenuFactory.getLabel(MenuFactory.CONF_SAVE_AS))
        self.layoutButtonLandUseChangeImpactTemplate.addWidget(self.buttonLoadLandUseChangeImpactTemplate)
        self.layoutButtonLandUseChangeImpactTemplate.addWidget(self.buttonSaveLandUseChangeImpactTemplate)
        self.layoutButtonLandUseChangeImpactTemplate.addWidget(self.buttonSaveAsLandUseChangeImpactTemplate)
        self.layoutGroupBoxLandUseChangeImpactTemplate.addLayout(self.layoutButtonLandUseChangeImpactTemplate)
        
        # Place the GroupBoxes
        self.layoutContentLandUseChangeImpact.addWidget(self.groupBoxLandUseChangeImpactParameters, 0, 0)
        self.layoutContentLandUseChangeImpact.addLayout(self.layoutButtonLandUseChangeImpact, 1, 0, 1, 2, Qt.AlignRight)
        self.layoutContentLandUseChangeImpact.addWidget(self.groupBoxLandUseChangeImpactTemplate, 0, 1, 1, 1)
        self.layoutContentLandUseChangeImpact.setColumnStretch(0, 3)
        self.layoutContentLandUseChangeImpact.setColumnStretch(1, 1) # Smaller template column

        
        #***********************************************************
        # Setup 'Log' tab
        #***********************************************************
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
            self.log_box.widget.verticalScrollBar().triggerAction(QAbstractSlider.SliderToMaximum)
    
    
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
            reply = QMessageBox.question(
                self,
                MenuFactory.getLabel(MenuFactory.CONF_LOAD_TEMPLATE),
                MenuFactory.getDescription(MenuFactory.CONF_LOAD_TEMPLATE) + ' \'{0}\'?'.format(templateFile),
                QMessageBox.Yes|QMessageBox.No,
                QMessageBox.No
            )
            
        if reply == QMessageBox.Yes or fileName:
            self.loadTemplate(MenuFactory.getLabel(MenuFactory.TAOPCOST_ABACUS_OPPORTUNITY_COST), templateFile)
    
    
    def handlerSaveAbacusOpportunityCostTemplate(self, fileName=None):
        """Slot method for saving a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.currentAbacusOpportunityCostTemplate
        
        if fileName:
            templateFile = fileName
        
        reply = QMessageBox.question(
            self,
            MenuFactory.getLabel(MenuFactory.CONF_SAVE_TEMPLATE),
            MenuFactory.getDescription(MenuFactory.CONF_SAVE_TEMPLATE),
            QMessageBox.Yes|QMessageBox.No,
            QMessageBox.No
        )
            
        if reply == QMessageBox.Yes:
            self.saveTemplate(MenuFactory.getLabel(MenuFactory.TAOPCOST_ABACUS_OPPORTUNITY_COST), templateFile)
            return True
        else:
            return False
    
    
    def handlerSaveAsAbacusOpportunityCostTemplate(self):
        """Slot method for saving a module template to a new file.
        """
        fileName, ok = QInputDialog.getText(self, MenuFactory.getLabel(MenuFactory.CONF_SAVE_AS), MenuFactory.getDescription(MenuFactory.CONF_SAVE_AS) + ':')
        fileSaved = False
        
        if ok:
            now = QDateTime.currentDateTime().toString('yyyyMMdd-hhmmss')
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
        file = unicode(QFileDialog.getOpenFileName(
            self, MenuFactory.getLabel(MenuFactory.MSG_TA_SELECT_PROJECT_FILE), QDir.homePath(), MenuFactory.getDescription(MenuFactory.MSG_TA_SELECT_PROJECT_FILE) + ' (*{0})'.format(self.main.appSettings['selectCarfileExt'])))
        
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
            reply = QMessageBox.question(
                self,
                MenuFactory.getLabel(MenuFactory.CONF_LOAD_TEMPLATE),
                MenuFactory.getDescription(MenuFactory.CONF_LOAD_TEMPLATE) + ' \'{0}\'?'.format(templateFile),
                QMessageBox.Yes|QMessageBox.No,
                QMessageBox.No
            )
            
        if reply == QMessageBox.Yes or fileName:
            self.loadTemplate(MenuFactory.getLabel(MenuFactory.TAOPCOST_OPPORTUNITY_COST_CURVE), templateFile)
    
    
    def handlerSaveOpportunityCostCurveTemplate(self, fileName=None):
        """Slot method for saving a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.currentOpportunityCostCurveTemplate
        
        if fileName:
            templateFile = fileName
        
        reply = QMessageBox.question(
            self,
            MenuFactory.getLabel(MenuFactory.CONF_SAVE_TEMPLATE),
            MenuFactory.getDescription(MenuFactory.CONF_SAVE_TEMPLATE),
            QMessageBox.Yes|QMessageBox.No,
            QMessageBox.No
        )
            
        if reply == QMessageBox.Yes:
            self.saveTemplate(MenuFactory.getLabel(MenuFactory.TAOPCOST_OPPORTUNITY_COST_CURVE), templateFile)
            return True
        else:
            return False
    
    
    def handlerSaveAsOpportunityCostCurveTemplate(self):
        """Slot method for saving a module template to a new file.
        """
        fileName, ok = QInputDialog.getText(self, MenuFactory.getLabel(MenuFactory.CONF_SAVE_AS), MenuFactory.getDescription(MenuFactory.CONF_SAVE_AS) + ':')
        fileSaved = False
        
        if ok:
            now = QDateTime.currentDateTime().toString('yyyyMMdd-hhmmss')
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
            reply = QMessageBox.question(
                self,
                MenuFactory.getLabel(MenuFactory.CONF_LOAD_TEMPLATE),
                MenuFactory.getDescription(MenuFactory.CONF_LOAD_TEMPLATE) + ' \'{0}\'?'.format(templateFile),
                QMessageBox.Yes|QMessageBox.No,
                QMessageBox.No
            )
            
        if reply == QMessageBox.Yes or fileName:
            self.loadTemplate(MenuFactory.getLabel(MenuFactory.TAOPCOST_OPPORTUNITY_COST_MAP), templateFile)
    
    
    def handlerSaveOpportunityCostMapTemplate(self, fileName=None):
        """Slot method for saving a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.currentOpportunityCostMapTemplate
        
        if fileName:
            templateFile = fileName
        
        reply = QMessageBox.question(
            self,
            MenuFactory.getLabel(MenuFactory.CONF_SAVE_TEMPLATE),
            MenuFactory.getDescription(MenuFactory.CONF_SAVE_TEMPLATE),
            QMessageBox.Yes|QMessageBox.No,
            QMessageBox.No
        )
            
        if reply == QMessageBox.Yes:
            self.saveTemplate(MenuFactory.getLabel(MenuFactory.TAOPCOST_OPPORTUNITY_COST_MAP), templateFile)
            return True
        else:
            return False
    
    
    def handlerSaveAsOpportunityCostMapTemplate(self):
        """Slot method for saving a module template to a new file.
        """
        fileName, ok = QInputDialog.getText(self, MenuFactory.getLabel(MenuFactory.CONF_SAVE_AS), MenuFactory.getDescription(MenuFactory.CONF_SAVE_AS) + ':')
        fileSaved = False
        
        if ok:
            now = QDateTime.currentDateTime().toString('yyyyMMdd-hhmmss')
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
    
    
    #***********************************************************
    # 'Descriptive Analysis of Regional Economy' tab QPushButton handlers
    #***********************************************************    
    def handlerSelectLandRequirementAnalysisDescriptiveOutput(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QFileDialog.getOpenFileName(
            self, MenuFactory.getLabel(MenuFactory.MSG_TA_SELECT_DESCRIPTIVE_ANALYSIS_OUTPUT), QDir.homePath(),  MenuFactory.getDescription(MenuFactory.MSG_TA_SELECT_DESCRIPTIVE_ANALYSIS_OUTPUT) + ' (*{0})'.format(self.main.appSettings['selectLdbasefileExt'])))
        
        if file:
            self.lineEditLandRequirementAnalysisDescriptiveOutput.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
            
            
    #***********************************************************
    # 'Regional Economy Scenario' tab QPushButton handlers
    #***********************************************************    
    def handlerSelectRegionalEconomicScenarioLandRequirement(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QFileDialog.getOpenFileName(
            self, MenuFactory.getLabel(MenuFactory.MSG_TA_SELECT_LAND_REQUIREMENT), QDir.homePath(), MenuFactory.getDescription(MenuFactory.MSG_TA_SELECT_LAND_REQUIREMENT) + ' (*{0})'.format(self.main.appSettings['selectLdbasefileExt'])))
        
        if file:
            self.lineEditRegionalEconomicScenarioLandRequirement.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)            


    #***********************************************************
    # 'Land Use Scenario' tab QPushButton handlers
    #***********************************************************    
    def handlerSelectLandUseChangeLandRequirement(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QFileDialog.getOpenFileName(
            self, MenuFactory.getLabel(MenuFactory.MSG_TA_SELECT_LAND_REQUIREMENT), QDir.homePath(), MenuFactory.getDescription(MenuFactory.MSG_TA_SELECT_LAND_REQUIREMENT) + ' (*{0})'.format(self.main.appSettings['selectLdbasefileExt'])))
        
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
        self.main.appSettings['DialogLumensTAOpportunityCostCurve']['QUESCDatabase'] = self.comboBoxOCCQUESCDatabase.currentText()
        self.main.appSettings['DialogLumensTAOpportunityCostCurve']['costThreshold'] = self.spinBoxOCCCostThreshold.value()
        
        # outputOpportunityCostDatabase = unicode(self.lineEditOCCOutputOpportunityCostDatabase.text())
        # outputOpportunityCostReport = unicode(self.lineEditOCCOutputOpportunityCostReport.text())
 
        # if not outputOpportunityCostDatabase:
        #     self.main.appSettings['DialogLumensTAOpportunityCostCurve']['outputOpportunityCostDatabase'] = '__UNSET__'
        # 
        # if not outputOpportunityCostReport:
        #     self.main.appSettings['DialogLumensTAOpportunityCostCurve']['outputOpportunityCostReport'] = '__UNSET__'
        
        # 'Opportunity Cost Map' tab fields
        self.main.appSettings['DialogLumensTAOpportunityCostMap']['landUse1'] = unicode(self.comboBoxOCMLandCoverLandUse1.currentText())
        self.main.appSettings['DialogLumensTAOpportunityCostMap']['landUse1'] = unicode(self.comboBoxOCMLandCoverLandUse2.currentText())
        self.main.appSettings['DialogLumensTAOpportunityCostMap']['plannigUnit'] = unicode(self.comboBoxOCMLandCoverPlanningUnit.currentText())
        self.main.appSettings['DialogLumensTAOpportunityCostMap']['carbon'] = unicode(self.comboBoxOCMCarbonTable.currentText())
        self.main.appSettings['DialogLumensTAOpportunityCostMap']['csvProfitability'] = unicode(self.comboBoxOCMCsvProfitability.currentText())
        self.main.appSettings['DialogLumensTAOpportunityCostMap']['nodata'] = self.spinBoxOCMNoDataValue.value()
        
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
            self.main.setWindowState(Qt.WindowMinimized)
            
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
            self.main.setWindowState(Qt.WindowActive)
            
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
        activeProject = self.main.appSettings['DialogLumensOpenDatabase']['projectFile'].replace(os.path.sep, '/')
        
        if self.validForm(formName):
            logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
            logging.getLogger(self.historyLog).info('alg start: %s' % formName)
            self.buttonProcessOpportunityCostCurve.setDisabled(True)
            
            # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
            self.main.setWindowState(Qt.WindowMinimized)
            
            outputs = general.runalg(
                algName,
                activeProject,
                self.main.appSettings[formName]['csvNPVTable'],
                self.main.appSettings[formName]['QUESCDatabase'],
                self.main.appSettings[formName]['costThreshold'],
                None,
            )
            
            # Display ROut file in debug mode
            if self.main.appSettings['debug']:
                dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                dialog.exec_()
            
            ##print outputs
            
            # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
            self.main.setWindowState(Qt.WindowActive)
            
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
        activeProject = self.main.appSettings['DialogLumensOpenDatabase']['projectFile'].replace(os.path.sep, '/')
        
        if self.validForm(formName):
            logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
            logging.getLogger(self.historyLog).info('alg start: %s' % formName)
            self.buttonProcessOpportunityCostMap.setDisabled(True)
            
            # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
            self.main.setWindowState(Qt.WindowMinimized)
            
            outputs = general.runalg(
                algName,
                activeProject,
                self.main.appSettings[formName]['landUse1'],
                self.main.appSettings[formName]['landUse2'],
                self.main.appSettings[formName]['plannigUnit'],
                self.main.appSettings[formName]['carbon'],
                self.main.appSettings[formName]['csvProfitability'],
                self.main.appSettings[formName]['nodata'],
                None,
            )
            
            # Display ROut file in debug mode
            if self.main.appSettings['debug']:
                dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                dialog.exec_()
            
            ##print outputs
            
            # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
            self.main.setWindowState(Qt.WindowActive)
            
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
            self.main.setWindowState(Qt.WindowMinimized)
            
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
            self.main.setWindowState(Qt.WindowActive)
            
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
            self.main.setWindowState(Qt.WindowMinimized)
            
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
            self.main.setWindowState(Qt.WindowActive)
            
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
                self.main.setWindowState(Qt.WindowMinimized)
                
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
                self.main.setWindowState(Qt.WindowActive)
                
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
                self.main.setWindowState(Qt.WindowMinimized)
                
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
                self.main.setWindowState(Qt.WindowActive)
                
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
            self.main.setWindowState(Qt.WindowMinimized)
            
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
            self.main.setWindowState(Qt.WindowActive)
            
            self.outputsMessageBox(algName, outputs, '', '')
            
            self.buttonProcessLandUseChangeImpact.setEnabled(True)
            logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
            logging.getLogger(self.historyLog).info('alg end: %s' % formName)
    
        
