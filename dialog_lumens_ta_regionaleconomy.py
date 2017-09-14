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


class DialogLumensTARegionalEconomy(QtGui.QDialog, DialogLumensBase):
    """LUMENS "TA Regional Economy" module dialog class.
    """
    
    def loadTemplateFiles(self):
        """Method for loading the list of module template files inside the project folder.
        
        This method is also called to load the module template files in the main window dashboard tab.
        """
        templateFiles = [os.path.basename(name) for name in glob.glob(os.path.join(self.settingsPath, '*.ini')) if os.path.isfile(os.path.join(self.settingsPath, name))]
        
        if templateFiles:
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
        
        if tabName == 'Descriptive Analysis of Regional Economy':
            dialogsToLoad = (
                'DialogLumensTARegionalEconomySingleIODescriptiveAnalysis',
                'DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis',
            )
            
            # start tab
            settings.beginGroup(tabName)
            
            # 'Single period' groupbox widgets
            # start dialog
            settings.beginGroup('DialogLumensTARegionalEconomySingleIODescriptiveAnalysis')
            
            templateSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis'] = {}
            templateSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['period'] = period = settings.value('period')
            templateSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['intermediateConsumptionMatrix'] = intermediateConsumptionMatrix = settings.value('intermediateConsumptionMatrix')
            templateSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['valueAddedMatrix'] = valueAddedMatrix = settings.value('valueAddedMatrix')
            templateSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['finalConsumptionMatrix'] = finalConsumptionMatrix = settings.value('finalConsumptionMatrix')
            templateSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['labourRequirement'] = labourRequirement = settings.value('labourRequirement')
            
            if not returnTemplateSettings:
                if period:
                    self.spinBoxSinglePeriod.setValue(int(period))
                else:
                    self.spinBoxSinglePeriod.setValue(td.year)
                if intermediateConsumptionMatrix and os.path.exists(intermediateConsumptionMatrix):
                    self.lineEditSingleIntermediateConsumptionMatrix.setText(intermediateConsumptionMatrix)
                else:
                    self.lineEditSingleIntermediateConsumptionMatrix.setText('')
                if valueAddedMatrix and os.path.exists(valueAddedMatrix):
                    self.lineEditSingleValueAddedMatrix.setText(valueAddedMatrix)
                else:
                    self.lineEditSingleValueAddedMatrix.setText('')
                if finalConsumptionMatrix and os.path.exists(finalConsumptionMatrix):
                    self.lineEditSingleFinalConsumptionMatrix.setText(finalConsumptionMatrix)
                else:
                    self.lineEditSingleFinalConsumptionMatrix.setText('')
                if labourRequirement and os.path.exists(labourRequirement):
                    self.lineEditSingleLabourRequirement.setText(labourRequirement)
                else:
                    self.lineEditSingleLabourRequirement.setText('')
            
            settings.endGroup()
            # /dialog
            
            # 'Multiple period' groupbox widgets
            # start dialog
            settings.beginGroup('DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis')
            
            templateSettings['DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis'] = {}
            templateSettings['DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis']['period2'] = period2 = settings.value('period2')
            templateSettings['DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis']['intermediateConsumptionMatrixP2'] = intermediateConsumptionMatrixP2 = settings.value('intermediateConsumptionMatrixP2')
            templateSettings['DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis']['valueAddedMatrixP2'] = valueAddedMatrixP2 = settings.value('valueAddedMatrixP2')
            templateSettings['DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis']['finalConsumptionMatrixP2'] = finalConsumptionMatrixP2 = settings.value('finalConsumptionMatrixP2')
            templateSettings['DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis']['labourRequirementP2'] = labourRequirementP2 = settings.value('labourRequirementP2')
            templateSettings['DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis']['valueAddedComponent'] = valueAddedComponent = settings.value('valueAddedComponent')
            templateSettings['DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis']['finalConsumptionComponent'] = finalConsumptionComponent = settings.value('finalConsumptionComponent')
            templateSettings['DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis']['listOfEconomicSector'] = listOfEconomicSector = settings.value('listOfEconomicSector')
            templateSettings['DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis']['financialUnit'] = financialUnit = settings.value('financialUnit')
            templateSettings['DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis']['areaName'] = areaName = settings.value('areaName')
            
            if not returnTemplateSettings:
                if period2:
                    self.spinBoxMultiplePeriod.setValue(int(period2))
                else:
                    self.spinBoxMultiplePeriod.setValue(td.year)
                if intermediateConsumptionMatrixP2 and os.path.exists(intermediateConsumptionMatrixP2):
                    self.lineEditMultipleIntermediateConsumptionMatrix.setText(intermediateConsumptionMatrixP2)
                else:
                    self.lineEditMultipleIntermediateConsumptionMatrix.setText('')
                if valueAddedMatrixP2 and os.path.exists(valueAddedMatrixP2):
                    self.lineEditMultipleValueAddedMatrix.setText(valueAddedMatrixP2)
                else:
                    self.lineEditMultipleValueAddedMatrix.setText('')
                if finalConsumptionMatrixP2 and os.path.exists(finalConsumptionMatrixP2):
                    self.lineEditMultipleFinalConsumptionMatrix.setText(finalConsumptionMatrixP2)
                else:
                    self.lineEditMultipleFinalConsumptionMatrix.setText('')
                if labourRequirementP2 and os.path.exists(labourRequirementP2):
                    self.lineEditMultipleLabourRequirement.setText(labourRequirementP2)
                else:
                    self.lineEditMultipleLabourRequirement.setText('')
                if valueAddedComponent and os.path.exists(valueAddedComponent):
                    self.lineEditOtherValueAddedComponent.setText(valueAddedComponent)
                else:
                    self.lineEditOtherValueAddedComponent.setText('')
                if finalConsumptionComponent and os.path.exists(finalConsumptionComponent):
                    self.lineEditOtherFinalConsumptionComponent.setText(finalConsumptionComponent)
                else:
                    self.lineEditOtherFinalConsumptionComponent.setText('')
                if listOfEconomicSector and os.path.exists(listOfEconomicSector):
                    self.lineEditOtherListOfEconomicSector.setText(listOfEconomicSector)
                else:
                    self.lineEditOtherListOfEconomicSector.setText('')
                if financialUnit:
                    self.lineEditOtherFinancialUnit.setText(financialUnit)
                else:
                    self.lineEditOtherFinancialUnit.setText('')
                if areaName:
                    self.lineEditOtherAreaName.setText(areaName)
                else:
                    self.lineEditOtherAreaName.setText('')
            
            if not returnTemplateSettings:
                self.currentDescriptiveAnalysisTemplate = templateFile
                self.loadedDescriptiveAnalysisTemplate.setText(templateFile)
                self.comboBoxDescriptiveAnalysisTemplate.setCurrentIndex(self.comboBoxDescriptiveAnalysisTemplate.findText(templateFile))
                self.buttonSaveDescriptiveAnalysisTemplate.setEnabled(True)
            
            settings.endGroup()
            # /dialog
            
            settings.endGroup()
            # /tab
        elif tabName == 'Regional Economic Scenario Impact':
            dialogsToLoad = (
                'DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis',
                'DialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis',
            )
            
            # start tab
            settings.beginGroup(tabName)
            
            # 'Final Demand Scenario' widgets
            # start dialog
            settings.beginGroup('DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis')
            
            templateSettings['DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis'] = {}
            templateSettings['DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis']['finalDemandChangeScenario'] = finalDemandChangeScenario = settings.value('finalDemandChangeScenario')
            templateSettings['DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis']['intermediateConsumptionMatrix'] = intermediateConsumptionMatrix = settings.value('intermediateConsumptionMatrix')
            templateSettings['DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis']['valueAddedMatrix'] = valueAddedMatrix = settings.value('valueAddedMatrix')
            templateSettings['DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis']['finalConsumptionMatrix'] = finalConsumptionMatrix = settings.value('finalConsumptionMatrix')
            templateSettings['DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis']['valueAddedComponent'] = valueAddedComponent = settings.value('valueAddedComponent')
            templateSettings['DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis']['finalConsumptionComponent'] = finalConsumptionComponent = settings.value('finalConsumptionComponent')
            templateSettings['DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis']['listOfEconomicSector'] = listOfEconomicSector = settings.value('listOfEconomicSector')
            templateSettings['DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis']['landDistributionMatrix'] = landDistributionMatrix = settings.value('landDistributionMatrix')
            templateSettings['DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis']['landRequirementCoefficientMatrix'] = landRequirementCoefficientMatrix = settings.value('landRequirementCoefficientMatrix')
            templateSettings['DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis']['landCoverComponent'] = landCoverComponent = settings.value('landCoverComponent')
            templateSettings['DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis']['labourRequirement'] = labourRequirement = settings.value('labourRequirement')
            templateSettings['DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis']['financialUnit'] = financialUnit = settings.value('financialUnit')
            templateSettings['DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis']['areaName'] = areaName = settings.value('areaName')
            templateSettings['DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis']['period'] = period = settings.value('period')
            
            if not returnTemplateSettings:
                if finalDemandChangeScenario and os.path.exists(finalDemandChangeScenario):
                    self.lineEditRegionalEconomicScenarioImpactFinalDemandChangeScenario.setText(finalDemandChangeScenario)
                else:
                    self.lineEditRegionalEconomicScenarioImpactFinalDemandChangeScenario.setText('')
                if intermediateConsumptionMatrix and os.path.exists(intermediateConsumptionMatrix):
                    self.lineEditRegionalEconomicScenarioImpactIntermediateConsumptionMatrix.setText(intermediateConsumptionMatrix)
                else:
                    self.lineEditRegionalEconomicScenarioImpactIntermediateConsumptionMatrix.setText('')
                if valueAddedMatrix and os.path.exists(valueAddedMatrix):
                    self.lineEditRegionalEconomicScenarioImpactValueAddedMatrix.setText(valueAddedMatrix)
                else:
                    self.lineEditRegionalEconomicScenarioImpactValueAddedMatrix.setText('')
                if finalConsumptionMatrix and os.path.exists(finalConsumptionMatrix):
                    self.lineEditRegionalEconomicScenarioImpactFinalConsumptionMatrix.setText(finalConsumptionMatrix)
                else:
                    self.lineEditRegionalEconomicScenarioImpactFinalConsumptionMatrix.setText('')
                if valueAddedComponent and os.path.exists(valueAddedComponent):
                    self.lineEditRegionalEconomicScenarioImpactValueAddedComponent.setText(valueAddedComponent)
                else:
                    self.lineEditRegionalEconomicScenarioImpactValueAddedComponent.setText('')
                if finalConsumptionComponent and os.path.exists(finalConsumptionComponent):
                    self.lineEditRegionalEconomicScenarioImpactFinalConsumptionComponent.setText(finalConsumptionComponent)
                else:
                    self.lineEditRegionalEconomicScenarioImpactFinalConsumptionComponent.setText('')
                if listOfEconomicSector and os.path.exists(listOfEconomicSector):
                    self.lineEditRegionalEconomicScenarioImpactListOfEconomicSector.setText(listOfEconomicSector)
                else:
                    self.lineEditRegionalEconomicScenarioImpactListOfEconomicSector.setText('')
                
                if landDistributionMatrix and os.path.exists(landDistributionMatrix):
                    self.lineEditRegionalEconomicScenarioImpactLandDistributionMatrix.setText(landDistributionMatrix)
                else:
                    self.lineEditRegionalEconomicScenarioImpactLandDistributionMatrix.setText('')
                if landRequirementCoefficientMatrix and os.path.exists(landRequirementCoefficientMatrix):
                    self.lineEditRegionalEconomicScenarioImpactLandRequirementCoefficientMatrix.setText(landRequirementCoefficientMatrix)
                else:
                    self.lineEditRegionalEconomicScenarioImpactLandRequirementCoefficientMatrix.setText('')
                if landCoverComponent and os.path.exists(landCoverComponent):
                    self.lineEditRegionalEconomicScenarioImpactLandCoverComponent.setText(landCoverComponent)
                else:
                    self.lineEditRegionalEconomicScenarioImpactLandCoverComponent.setText('')
                if labourRequirement and os.path.exists(labourRequirement):
                    self.lineEditRegionalEconomicScenarioImpactLabourRequirement.setText(labourRequirement)
                else:
                    self.lineEditRegionalEconomicScenarioImpactLabourRequirement.setText('')
                if financialUnit:
                    self.lineEditRegionalEconomicScenarioImpactFinancialUnit.setText(financialUnit)
                else:
                    self.lineEditRegionalEconomicScenarioImpactFinancialUnit.setText('')
                if areaName:
                    self.lineEditRegionalEconomicScenarioImpactAreaName.setText(areaName)
                else:
                    self.lineEditRegionalEconomicScenarioImpactAreaName.setText('')
                if period:
                    self.spinBoxRegionalEconomicScenarioImpactPeriod.setValue(int(period))
                else:
                    self.spinBoxRegionalEconomicScenarioImpactPeriod.setValue(td.year)
            
            settings.endGroup()
            # /dialog
            
            # 'GDP Scenario' widgets
            # start dialog
            settings.beginGroup('DialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis')
            
            templateSettings['DialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis'] = {}
            templateSettings['DialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis']['gdpChangeScenario'] = gdpChangeScenario = settings.value('gdpChangeScenario')
            
            if not returnTemplateSettings:
                if gdpChangeScenario and os.path.exists(gdpChangeScenario):
                    self.lineEditRegionalEconomicScenarioImpactGDPChangeScenario.setText(gdpChangeScenario)
                else:
                    self.lineEditRegionalEconomicScenarioImpactGDPChangeScenario.setText('')
            
            if not returnTemplateSettings:
                self.currentRegionalEconomicScenarioImpactTemplate = templateFile
                self.loadedRegionalEconomicScenarioImpactTemplate.setText(templateFile)
                self.comboBoxRegionalEconomicScenarioImpactTemplate.setCurrentIndex(self.comboBoxRegionalEconomicScenarioImpactTemplate.findText(templateFile))
                self.buttonSaveRegionalEconomicScenarioImpactTemplate.setEnabled(True)
            
            settings.endGroup()
            # /dialog
            
            settings.endGroup()
            # /tab
        elif tabName == 'Land Requirement Analysis':
            dialogsToLoad = (
                'DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis',
            )
            
            # start tab
            settings.beginGroup(tabName)
            
            # 'Land Requirement Analysis' widgets
            # start dialog
            settings.beginGroup('DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis')
            
            templateSettings['DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis'] = {}
            templateSettings['DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis']['intermediateConsumptionMatrix'] = intermediateConsumptionMatrix = settings.value('intermediateConsumptionMatrix')
            templateSettings['DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis']['valueAddedMatrix'] = valueAddedMatrix = settings.value('valueAddedMatrix')
            templateSettings['DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis']['finalConsumptionMatrix'] = finalConsumptionMatrix = settings.value('finalConsumptionMatrix')
            templateSettings['DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis']['valueAddedComponent'] = valueAddedComponent = settings.value('valueAddedComponent')
            templateSettings['DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis']['finalConsumptionComponent'] = finalConsumptionComponent = settings.value('finalConsumptionComponent')
            templateSettings['DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis']['listOfEconomicSector'] = listOfEconomicSector = settings.value('listOfEconomicSector')
            templateSettings['DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis']['landDistributionMatrix'] = landDistributionMatrix = settings.value('landDistributionMatrix')
            templateSettings['DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis']['landCoverComponent'] = landCoverComponent = settings.value('landCoverComponent')
            templateSettings['DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis']['labourRequirement'] = labourRequirement = settings.value('labourRequirement')
            templateSettings['DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis']['financialUnit'] = financialUnit = settings.value('financialUnit')
            templateSettings['DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis']['areaName'] = areaName = settings.value('areaName')
            templateSettings['DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis']['period'] = period = settings.value('period')
            
            if not returnTemplateSettings:
                if intermediateConsumptionMatrix and os.path.exists(intermediateConsumptionMatrix):
                    self.lineEditLandRequirementAnalysisIntermediateConsumptionMatrix.setText(intermediateConsumptionMatrix)
                else:
                    self.lineEditLandRequirementAnalysisIntermediateConsumptionMatrix.setText('')
                if valueAddedMatrix and os.path.exists(valueAddedMatrix):
                    self.lineEditLandRequirementAnalysisValueAddedMatrix.setText(valueAddedMatrix)
                else:
                    self.lineEditLandRequirementAnalysisValueAddedMatrix.setText('')
                if finalConsumptionMatrix and os.path.exists(finalConsumptionMatrix):
                    self.lineEditLandRequirementAnalysisFinalConsumptionMatrix.setText(finalConsumptionMatrix)
                else:
                    self.lineEditLandRequirementAnalysisFinalConsumptionMatrix.setText('')
                if valueAddedComponent and os.path.exists(valueAddedComponent):
                    self.lineEditLandRequirementAnalysisValueAddedComponent.setText(valueAddedComponent)
                else:
                    self.lineEditLandRequirementAnalysisValueAddedComponent.setText('')
                if finalConsumptionComponent and os.path.exists(finalConsumptionComponent):
                    self.lineEditLandRequirementAnalysisFinalConsumptionComponent.setText(finalConsumptionComponent)
                else:
                    self.lineEditLandRequirementAnalysisFinalConsumptionComponent.setText('')
                if listOfEconomicSector and os.path.exists(listOfEconomicSector):
                    self.lineEditLandRequirementAnalysisListOfEconomicSector.setText(listOfEconomicSector)
                else:
                    self.lineEditLandRequirementAnalysisListOfEconomicSector.setText('')
                if landDistributionMatrix and os.path.exists(landDistributionMatrix):
                    self.lineEditLandRequirementAnalysisLandDistributionMatrix.setText(landDistributionMatrix)
                else:
                    self.lineEditLandRequirementAnalysisLandDistributionMatrix.setText('')
                if landCoverComponent and os.path.exists(landCoverComponent):
                    self.lineEditLandRequirementAnalysisLandCoverComponent.setText(landCoverComponent)
                else:
                    self.lineEditLandRequirementAnalysisLandCoverComponent.setText('')
                if labourRequirement and os.path.exists(labourRequirement):
                    self.lineEditLandRequirementAnalysisLabourRequirement.setText(labourRequirement)
                else:
                    self.lineEditLandRequirementAnalysisLabourRequirement.setText('')
                if financialUnit:
                    self.lineEditLandRequirementAnalysisFinancialUnit.setText(financialUnit)
                else:
                    self.lineEditLandRequirementAnalysisFinancialUnit.setText('')
                if areaName:
                    self.lineEditLandRequirementAnalysisAreaName.setText(areaName)
                else:
                    self.lineEditLandRequirementAnalysisAreaName.setText('')
                if period:
                    self.spinBoxLandRequirementAnalysisPeriod.setValue(int(period))
                else:
                    self.spinBoxLandRequirementAnalysisPeriod.setValue(td.year)
                
                self.currentLandRequirementAnalysisTemplate = templateFile
                self.loadedLandRequirementAnalysisTemplate.setText(templateFile)
                self.comboBoxLandRequirementAnalysisTemplate.setCurrentIndex(self.comboBoxLandRequirementAnalysisTemplate.findText(templateFile))
                self.buttonSaveLandRequirementAnalysisTemplate.setEnabled(True)
            
            settings.endGroup()
            # /dialog
            
            settings.endGroup()
            # /tab
        elif tabName == 'Land Use Change Impact':
            dialogsToLoad = (
                'DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis',
            )
            
            # start tab
            settings.beginGroup(tabName)
            
            # 'Land Use Change Impact' widgets
            # start dialog
            settings.beginGroup('DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis')
            
            templateSettings['DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis'] = {}
            templateSettings['DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis']['intermediateConsumptionMatrix'] = intermediateConsumptionMatrix = settings.value('intermediateConsumptionMatrix')
            templateSettings['DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis']['valueAddedMatrix'] = valueAddedMatrix = settings.value('valueAddedMatrix')
            templateSettings['DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis']['finalConsumptionMatrix'] = finalConsumptionMatrix = settings.value('finalConsumptionMatrix')
            templateSettings['DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis']['valueAddedComponent'] = valueAddedComponent = settings.value('valueAddedComponent')
            templateSettings['DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis']['finalConsumptionComponent'] = finalConsumptionComponent = settings.value('finalConsumptionComponent')
            templateSettings['DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis']['listOfEconomicSector'] = listOfEconomicSector = settings.value('listOfEconomicSector')
            templateSettings['DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis']['landDistributionMatrix'] = landDistributionMatrix = settings.value('landDistributionMatrix')
            templateSettings['DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis']['landRequirementCoefficientMatrix'] = landRequirementCoefficientMatrix = settings.value('landRequirementCoefficientMatrix')
            templateSettings['DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis']['landCoverComponent'] = landCoverComponent = settings.value('landCoverComponent')
            templateSettings['DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis']['labourRequirement'] = labourRequirement = settings.value('labourRequirement')
            templateSettings['DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis']['financialUnit'] = financialUnit = settings.value('financialUnit')
            templateSettings['DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis']['areaName'] = areaName = settings.value('areaName')
            templateSettings['DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis']['period'] = period = settings.value('period')
            
            if not returnTemplateSettings:
                if intermediateConsumptionMatrix and os.path.exists(intermediateConsumptionMatrix):
                    self.lineEditLandUseChangeImpactIntermediateConsumptionMatrix.setText(intermediateConsumptionMatrix)
                else:
                    self.lineEditLandUseChangeImpactIntermediateConsumptionMatrix.setText('')
                if valueAddedMatrix and os.path.exists(valueAddedMatrix):
                    self.lineEditLandUseChangeImpactValueAddedMatrix.setText(valueAddedMatrix)
                else:
                    self.lineEditLandUseChangeImpactValueAddedMatrix.setText('')
                if finalConsumptionMatrix and os.path.exists(finalConsumptionMatrix):
                    self.lineEditLandUseChangeImpactFinalConsumptionMatrix.setText(finalConsumptionMatrix)
                else:
                    self.lineEditLandUseChangeImpactFinalConsumptionMatrix.setText('')
                if valueAddedComponent and os.path.exists(valueAddedComponent):
                    self.lineEditLandUseChangeImpactValueAddedComponent.setText(valueAddedComponent)
                else:
                    self.lineEditLandUseChangeImpactValueAddedComponent.setText('')
                if finalConsumptionComponent and os.path.exists(finalConsumptionComponent):
                    self.lineEditLandUseChangeImpactFinalConsumptionComponent.setText(finalConsumptionComponent)
                else:
                    self.lineEditLandUseChangeImpactFinalConsumptionComponent.setText('')
                if listOfEconomicSector and os.path.exists(listOfEconomicSector):
                    self.lineEditLandUseChangeImpactListOfEconomicSector.setText(listOfEconomicSector)
                else:
                    self.lineEditLandUseChangeImpactListOfEconomicSector.setText('')
                if landDistributionMatrix and os.path.exists(landDistributionMatrix):
                    self.lineEditLandUseChangeImpactLandDistributionMatrix.setText(landDistributionMatrix)
                else:
                    self.lineEditLandUseChangeImpactLandDistributionMatrix.setText('')
                if landRequirementCoefficientMatrix and os.path.exists(landRequirementCoefficientMatrix):
                    self.lineEditLandUseChangeImpactLandRequirementCoefficientMatrix.setText(landRequirementCoefficientMatrix)
                else:
                    self.lineEditLandUseChangeImpactLandRequirementCoefficientMatrix.setText('')
                if landCoverComponent and os.path.exists(landCoverComponent):
                    self.lineEditLandUseChangeImpactLandCoverComponent.setText(landCoverComponent)
                else:
                    self.lineEditLandUseChangeImpactLandCoverComponent.setText('')
                if labourRequirement and os.path.exists(labourRequirement):
                    self.lineEditLandUseChangeImpactLabourRequirement.setText(labourRequirement)
                else:
                    self.lineEditLandUseChangeImpactLabourRequirement.setText('')
                if financialUnit:
                    self.lineEditLandUseChangeImpactFinancialUnit.setText(financialUnit)
                else:
                    self.lineEditLandUseChangeImpactFinancialUnit.setText('')
                if areaName:
                    self.lineEditLandUseChangeImpactAreaName.setText(areaName)
                else:
                    self.lineEditLandUseChangeImpactAreaName.setText('')
                if period:
                    self.spinBoxLandUseChangeImpactPeriod.setValue(int(period))
                else:
                    self.spinBoxLandUseChangeImpactPeriod.setValue(td.year)
                
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
        
        if tabName == 'Descriptive Analysis of Regional Economy':
            dialogsToLoad = (
                'DialogLumensTARegionalEconomySingleIODescriptiveAnalysis',
                'DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis',
            )
        elif tabName == 'Regional Economic Scenario Impact':
            dialogsToLoad = (
                'DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis',
                'DialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis',
            )
        elif tabName == 'Land Requirement Analysis':
            dialogsToLoad = (
                'DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis',
            )
        elif tabName == 'Land Use Change Impact':
            dialogsToLoad = (
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
                'Load Existing Template',
                'The template you are about to save matches an existing template.\nDo you want to load \'{0}\' instead?'.format(duplicateTemplate),
                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                QtGui.QMessageBox.No
            )
            
            if reply == QtGui.QMessageBox.Yes:
                if tabName == 'Descriptive Analysis of Regional Economy':
                    self.handlerLoadDescriptiveAnalysisTemplate(duplicateTemplate)
                elif tabName == 'Regional Economic Scenario Impact':
                    self.handlerLoadRegionalEconomicScenarioImpactTemplate(duplicateTemplate)
                elif tabName == 'Land Requirement Analysis':
                    self.handlerLoadLandRequirementAnalysisTemplate(duplicateTemplate)
                elif tabName == 'Land Use Change Impact':
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
            
            if tabName == 'Descriptive Analysis of Regional Economy':
                dialogsToSave = (
                    'DialogLumensTARegionalEconomySingleIODescriptiveAnalysis',
                    'DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis',
                )
            elif tabName == 'Regional Economic Scenario Impact':
                dialogsToSave = (
                    'DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis',
                    'DialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis',
                )
            elif tabName == 'Land Requirement Analysis':
                dialogsToSave = (
                    'DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis',
                )
            elif tabName == 'Land Use Change Impact':
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
        super(DialogLumensTARegionalEconomy, self).__init__(parent)
        
        self.main = parent
        self.dialogTitle = 'LUMENS Trade-Off Analysis [Regional Economy]'
        self.settingsPath = os.path.join(self.main.appSettings['DialogLumensOpenDatabase']['projectFolder'], self.main.appSettings['folderTA'])
        self.currentDescriptiveAnalysisTemplate = None
        self.currentRegionalEconomicScenarioImpactTemplate = None
        self.currentLandRequirementAnalysisTemplate = None
        self.currentLandUseChangeImpactTemplate = None
        
        # Init logging
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        if self.main.appSettings['debug']:
            print 'DEBUG: DialogLumensTARegionalEconomy init'
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
        
        # 'Initialize' tab button
        self.buttonNextInitialize.clicked.connect(self.handlerGenerateInputOutputTable)
        
        # 'Descriptive Analysis of Regional Economy' tab checkbox
        self.checkBoxMultiplePeriod.toggled.connect(self.toggleMultiplePeriod)
        
        # 'Descriptive Analysis of Regional Economy' tab buttons
        self.buttonSelectSingleIntermediateConsumptionMatrix.clicked.connect(self.handlerSelectSingleIntermediateConsumptionMatrix)
        self.buttonSelectSingleValueAddedMatrix.clicked.connect(self.handlerSelectSingleValueAddedMatrix)
        self.buttonSelectSingleFinalConsumptionMatrix.clicked.connect(self.handlerSelectSingleFinalConsumptionMatrix)
        self.buttonSelectSingleLabourRequirement.clicked.connect(self.handlerSelectSingleLabourRequirement)
        self.buttonSelectMultipleIntermediateConsumptionMatrix.clicked.connect(self.handlerSelectMultipleIntermediateConsumptionMatrix)
        self.buttonSelectMultipleValueAddedMatrix.clicked.connect(self.handlerSelectMultipleValueAddedMatrix)
        self.buttonSelectMultipleFinalConsumptionMatrix.clicked.connect(self.handlerSelectMultipleFinalConsumptionMatrix)
        self.buttonSelectMultipleLabourRequirement.clicked.connect(self.handlerSelectMultipleLabourRequirement)
        self.buttonSelectOtherValueAddedComponent.clicked.connect(self.handlerSelectOtherValueAddedComponent)
        self.buttonSelectOtherFinalConsumptionComponent.clicked.connect(self.handlerSelectOtherFinalConsumptionComponent)
        self.buttonSelectOtherListOfEconomicSector.clicked.connect(self.handlerSelectOtherListOfEconomicSector)
        self.buttonProcessDescriptiveAnalysis.clicked.connect(self.handlerProcessDescriptiveAnalysis)
        self.buttonHelpTADescriptiveAnalysis.clicked.connect(lambda:self.handlerDialogHelp('TA'))
        self.buttonLoadDescriptiveAnalysisTemplate.clicked.connect(self.handlerLoadDescriptiveAnalysisTemplate)
        self.buttonSaveDescriptiveAnalysisTemplate.clicked.connect(self.handlerSaveDescriptiveAnalysisTemplate)
        self.buttonSaveAsDescriptiveAnalysisTemplate.clicked.connect(self.handlerSaveAsDescriptiveAnalysisTemplate)
        
        # 'Regional Economic Scenario Impact' tab checkboxes
        self.checkBoxRegionalEconomicScenarioImpactFinalDemand.toggled.connect(lambda:self.toggleRegionalEconomicScenarioImpactType(self.checkBoxRegionalEconomicScenarioImpactFinalDemand))
        self.checkBoxRegionalEconomicScenarioImpactGDP.toggled.connect(lambda:self.toggleRegionalEconomicScenarioImpactType(self.checkBoxRegionalEconomicScenarioImpactGDP))
        
        # 'Regional Economic Scenario Impact' tab buttons
        self.buttonSelectRegionalEconomicScenarioImpactFinalDemandChangeScenario.clicked.connect(self.handlerSelectRegionalEconomicScenarioImpactFinalDemandChangeScenario)
        self.buttonSelectRegionalEconomicScenarioImpactGDPChangeScenario.clicked.connect(self.handlerSelectRegionalEconomicScenarioImpactGDPChangeScenario)
        self.buttonSelectRegionalEconomicScenarioImpactIntermediateConsumptionMatrix.clicked.connect(self.handlerSelectRegionalEconomicScenarioImpactIntermediateConsumptionMatrix)
        self.buttonSelectRegionalEconomicScenarioImpactValueAddedMatrix.clicked.connect(self.handlerSelectRegionalEconomicScenarioImpactValueAddedMatrix)
        self.buttonSelectRegionalEconomicScenarioImpactFinalConsumptionMatrix.clicked.connect(self.handlerSelectRegionalEconomicScenarioImpactFinalConsumptionMatrix)
        self.buttonSelectRegionalEconomicScenarioImpactValueAddedComponent.clicked.connect(self.handlerSelectRegionalEconomicScenarioImpactValueAddedComponent)
        self.buttonSelectRegionalEconomicScenarioImpactFinalConsumptionComponent.clicked.connect(self.handlerSelectRegionalEconomicScenarioImpactFinalConsumptionComponent)
        self.buttonSelectRegionalEconomicScenarioImpactListOfEconomicSector.clicked.connect(self.handlerSelectRegionalEconomicScenarioImpactListOfEconomicSector)
        self.buttonSelectRegionalEconomicScenarioImpactLandDistributionMatrix.clicked.connect(self.handlerSelectRegionalEconomicScenarioImpactLandDistributionMatrix)
        self.buttonSelectRegionalEconomicScenarioImpactLandRequirementCoefficientMatrix.clicked.connect(self.handlerSelectRegionalEconomicScenarioImpactLandRequirementCoefficientMatrix)
        self.buttonSelectRegionalEconomicScenarioImpactLandCoverComponent.clicked.connect(self.handlerSelectRegionalEconomicScenarioImpactLandCoverComponent)
        self.buttonSelectRegionalEconomicScenarioImpactLabourRequirement.clicked.connect(self.handlerSelectRegionalEconomicScenarioImpactLabourRequirement)
        self.buttonProcessRegionalEconomicScenarioImpact.clicked.connect(self.handlerProcessRegionalEconomicScenarioImpact)
        self.buttonHelpTARegionalEconomicScenarioImpact.clicked.connect(lambda:self.handlerDialogHelp('TA'))
        self.buttonLoadRegionalEconomicScenarioImpactTemplate.clicked.connect(self.handlerLoadRegionalEconomicScenarioImpactTemplate)
        self.buttonSaveRegionalEconomicScenarioImpactTemplate.clicked.connect(self.handlerSaveRegionalEconomicScenarioImpactTemplate)
        self.buttonSaveAsRegionalEconomicScenarioImpactTemplate.clicked.connect(self.handlerSaveAsRegionalEconomicScenarioImpactTemplate)
        
        # 'Land Requirement Analysis' tab buttons
        self.buttonSelectLandRequirementAnalysisIntermediateConsumptionMatrix.clicked.connect(self.handlerSelectLandRequirementAnalysisIntermediateConsumptionMatrix)
        self.buttonSelectLandRequirementAnalysisValueAddedMatrix.clicked.connect(self.handlerSelectLandRequirementAnalysisValueAddedMatrix)
        self.buttonSelectLandRequirementAnalysisFinalConsumptionMatrix.clicked.connect(self.handlerSelectLandRequirementAnalysisFinalConsumptionMatrix)
        self.buttonSelectLandRequirementAnalysisValueAddedComponent.clicked.connect(self.handlerSelectLandRequirementAnalysisValueAddedComponent)
        self.buttonSelectLandRequirementAnalysisFinalConsumptionComponent.clicked.connect(self.handlerSelectLandRequirementAnalysisFinalConsumptionComponent)
        self.buttonSelectLandRequirementAnalysisListOfEconomicSector.clicked.connect(self.handlerSelectLandRequirementAnalysisListOfEconomicSector)
        self.buttonSelectLandRequirementAnalysisLandDistributionMatrix.clicked.connect(self.handlerSelectLandRequirementAnalysisLandDistributionMatrix)
        self.buttonSelectLandRequirementAnalysisLandCoverComponent.clicked.connect(self.handlerSelectLandRequirementAnalysisLandCoverComponent)
        self.buttonSelectLandRequirementAnalysisLabourRequirement.clicked.connect(self.handlerSelectLandRequirementAnalysisLabourRequirement)
        self.buttonProcessLandRequirementAnalysis.clicked.connect(self.handlerProcessLandRequirementAnalysis)
        self.buttonHelpTALandRequirementAnalysis.clicked.connect(lambda:self.handlerDialogHelp('TA'))
        self.buttonLoadLandRequirementAnalysisTemplate.clicked.connect(self.handlerLoadLandRequirementAnalysisTemplate)
        self.buttonSaveLandRequirementAnalysisTemplate.clicked.connect(self.handlerSaveLandRequirementAnalysisTemplate)
        self.buttonSaveAsLandRequirementAnalysisTemplate.clicked.connect(self.handlerSaveAsLandRequirementAnalysisTemplate)
        
        # 'Land Use Change Impact' tab buttons
        self.buttonSelectLandUseChangeImpactIntermediateConsumptionMatrix.clicked.connect(self.handlerSelectLandUseChangeImpactIntermediateConsumptionMatrix)
        self.buttonSelectLandUseChangeImpactValueAddedMatrix.clicked.connect(self.handlerSelectLandUseChangeImpactValueAddedMatrix)
        self.buttonSelectLandUseChangeImpactFinalConsumptionMatrix.clicked.connect(self.handlerSelectLandUseChangeImpactFinalConsumptionMatrix)
        self.buttonSelectLandUseChangeImpactValueAddedComponent.clicked.connect(self.handlerSelectLandUseChangeImpactValueAddedComponent)
        self.buttonSelectLandUseChangeImpactFinalConsumptionComponent.clicked.connect(self.handlerSelectLandUseChangeImpactFinalConsumptionComponent)
        self.buttonSelectLandUseChangeImpactListOfEconomicSector.clicked.connect(self.handlerSelectLandUseChangeImpactListOfEconomicSector)
        self.buttonSelectLandUseChangeImpactLandDistributionMatrix.clicked.connect(self.handlerSelectLandUseChangeImpactLandDistributionMatrix)
        self.buttonSelectLandUseChangeImpactLandRequirementCoefficientMatrix.clicked.connect(self.handlerSelectLandUseChangeImpactLandRequirementCoefficientMatrix)
        self.buttonSelectLandUseChangeImpactLandCoverComponent.clicked.connect(self.handlerSelectLandUseChangeImpactLandCoverComponent)
        self.buttonSelectLandUseChangeImpactLabourRequirement.clicked.connect(self.handlerSelectLandUseChangeImpactLabourRequirement)
        self.buttonProcessLandUseChangeImpact.clicked.connect(self.handlerProcessLandUseChangeImpact)
        self.buttonHelpTALandUseChangeImpact.clicked.connect(lambda:self.handlerDialogHelp('TA'))
        self.buttonLoadLandUseChangeImpactTemplate.clicked.connect(self.handlerLoadLandUseChangeImpactTemplate)
        self.buttonSaveLandUseChangeImpactTemplate.clicked.connect(self.handlerSaveLandUseChangeImpactTemplate)
        self.buttonSaveAsLandUseChangeImpactTemplate.clicked.connect(self.handlerSaveAsLandUseChangeImpactTemplate)
        
    
    def setupUi(self, parent):
        """Method for building the dialog UI.
        
        Args:
            parent: the dialog's parent instance.
        """
        self.setStyleSheet('QDialog { background-color: #222; }')
        self.dialogLayout = QtGui.QVBoxLayout()
        self.tabWidget = QtGui.QTabWidget()
        tabWidgetStylesheet = """
        QTabWidget::pane {
            border: none;
            background-color: #fff;
        }
        QTabBar::tab {
            background-color: #222;
            color: #fff;
        }
        QTabBar::tab:selected, QTabBar::tab:hover {
            background-color: #fff;
            color: #000;
        }
        """
        self.tabWidget.setStyleSheet(tabWidgetStylesheet)
        
        self.tabInitRegionalEconomyParameterTable = QtGui.QWidget()
        self.tabInputOutputTable = QtGui.QWidget()
        self.tabDescriptiveAnalysis = QtGui.QWidget()
        self.tabRegionalEconomicScenarioImpact = QtGui.QWidget()
        self.tabLandRequirementAnalysis = QtGui.QWidget()
        self.tabLandUseChangeImpact = QtGui.QWidget()
        self.tabLog = QtGui.QWidget()
        
        self.tabWidget.addTab(self.tabInitRegionalEconomyParameterTable, 'Initialize')
        self.tabWidget.addTab(self.tabInputOutputTable, 'Input-Output Table')
        self.tabWidget.addTab(self.tabDescriptiveAnalysis, 'Descriptive Analysis of Regional Economy')
        self.tabWidget.addTab(self.tabRegionalEconomicScenarioImpact, 'Regional Economic Scenario Impact')
        self.tabWidget.addTab(self.tabLandRequirementAnalysis, 'Land Requirement Analysis')
        self.tabWidget.addTab(self.tabLandUseChangeImpact, 'Land Use Change Impact')
        self.tabWidget.addTab(self.tabLog, 'Log')
        
        #self.tabWidget.setTabEnabled(1, False)
        
        self.layoutTabInitRegionalEconomyParameterTable = QtGui.QGridLayout()
        self.layoutTabInputOutputTable = QtGui.QGridLayout()
        ##self.layoutTabDescriptiveAnalysis = QtGui.QVBoxLayout()
        self.layoutTabDescriptiveAnalysis = QtGui.QGridLayout()
        ##self.layoutTabRegionalEconomicScenarioImpact = QtGui.QVBoxLayout()
        self.layoutTabRegionalEconomicScenarioImpact = QtGui.QGridLayout()
        ##self.layoutTabLandRequirementAnalysis = QtGui.QVBoxLayout()
        self.layoutTabLandRequirementAnalysis = QtGui.QGridLayout()
        ##self.layoutTabLandUseChangeImpact = QtGui.QVBoxLayout()
        self.layoutTabLandUseChangeImpact = QtGui.QGridLayout()
        self.layoutTabLog = QtGui.QVBoxLayout()
        
        self.tabInitRegionalEconomyParameterTable.setLayout(self.layoutTabInitRegionalEconomyParameterTable)
        self.tabInputOutputTable.setLayout(self.layoutTabInputOutputTable)
        self.tabDescriptiveAnalysis.setLayout(self.layoutTabDescriptiveAnalysis)
        self.tabRegionalEconomicScenarioImpact.setLayout(self.layoutTabRegionalEconomicScenarioImpact)
        self.tabLandRequirementAnalysis.setLayout(self.layoutTabLandRequirementAnalysis)
        self.tabLandUseChangeImpact.setLayout(self.layoutTabLandUseChangeImpact)
        self.tabLog.setLayout(self.layoutTabLog)
        
        self.dialogLayout.addWidget(self.tabWidget)
        
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
        self.labelHistoryLogInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutHistoryLogInfo.addWidget(self.labelHistoryLogInfo)
        
        self.log_box = QPlainTextEditLogger(self)
        self.layoutHistoryLog.addWidget(self.log_box.widget)
        
        self.layoutTabLog.addWidget(self.groupBoxHistoryLog)
        
        
        self.setLayout(self.dialogLayout)
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(1024, 800)
        self.resize(parent.sizeHint())
    
    
    def showEvent(self, event):
        """Overload method that is called when the dialog widget is shown.
        
        Args:
            event (QShowEvent): the show widget event.
        """
        super(DialogLumensTARegionalEconomy, self).showEvent(event)
    
    
    def closeEvent(self, event):
        """Overload method that is called when the dialog widget is closed.
        
        Args:
            event (QCloseEvent): the close widget event.
        """
        super(DialogLumensTARegionalEconomy, self).closeEvent(event)
    
    
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
    
    
    def toggleMultiplePeriod(self, checked):
        """Slot method for handling checkbox toggling.
        
        Args:
            checked (bool): the checkbox status.
        """
        if checked:
            self.contentOptionsMultiplePeriod.setEnabled(True)
        else:
            self.contentOptionsMultiplePeriod.setDisabled(True)
    
    
    def toggleRegionalEconomicScenarioImpactType(self, widget):
        """Slot method for handling checkbox toggling.
        
        Args:
            widget (QCheckBox): the checked widget.
        """
        if widget.text() == 'Final Demand Scenario':
            if widget.isChecked():
                self.labelRegionalEconomicScenarioImpactFinalDemandChangeScenario.setEnabled(True)
                self.lineEditRegionalEconomicScenarioImpactFinalDemandChangeScenario.setEnabled(True)
                self.buttonSelectRegionalEconomicScenarioImpactFinalDemandChangeScenario.setEnabled(True)
            else:
                self.labelRegionalEconomicScenarioImpactFinalDemandChangeScenario.setDisabled(True)
                self.lineEditRegionalEconomicScenarioImpactFinalDemandChangeScenario.setDisabled(True)
                self.buttonSelectRegionalEconomicScenarioImpactFinalDemandChangeScenario.setDisabled(True)
        elif widget.text() == 'GDP Scenario':
            if widget.isChecked():
                self.labelRegionalEconomicScenarioImpactGDPChangeScenario.setEnabled(True)
                self.lineEditRegionalEconomicScenarioImpactGDPChangeScenario.setEnabled(True)
                self.buttonSelectRegionalEconomicScenarioImpactGDPChangeScenario.setEnabled(True)
            else:
                self.labelRegionalEconomicScenarioImpactGDPChangeScenario.setDisabled(True)
                self.lineEditRegionalEconomicScenarioImpactGDPChangeScenario.setDisabled(True)
                self.buttonSelectRegionalEconomicScenarioImpactGDPChangeScenario.setDisabled(True)
    

    #***********************************************************
    # 'Initialize' tab QPushButton handlers
    #***********************************************************
    def handlerGenerateInputOutputTable(self):
        
      
        self.tabWidget.setCurrentWidget(self.tabInputOutputTable)
    
    
    #***********************************************************
    # 'Descriptive Analysis of Regional Economy' tab QPushButton handlers
    #***********************************************************
    def handlerLoadDescriptiveAnalysisTemplate(self, fileName=None):
        """Slot method for loading a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.comboBoxDescriptiveAnalysisTemplate.currentText()
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
            self.loadTemplate('Descriptive Analysis of Regional Economy', templateFile)
    
    
    def handlerSaveDescriptiveAnalysisTemplate(self, fileName=None):
        """Slot method for saving a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.currentDescriptiveAnalysisTemplate
        
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
            self.saveTemplate('Descriptive Analysis of Regional Economy', templateFile)
            return True
        else:
            return False
    
    
    def handlerSaveAsDescriptiveAnalysisTemplate(self):
        """Slot method for saving a module template to a new file.
        """
        fileName, ok = QtGui.QInputDialog.getText(self, 'Save As', 'Enter a new template name:')
        fileSaved = False
        
        if ok:
            now = QtCore.QDateTime.currentDateTime().toString('yyyyMMdd-hhmmss')
            fileName = now + '__' + fileName + '.ini'
            
            if os.path.exists(os.path.join(self.settingsPath, fileName)):
                fileSaved = self.handlerSaveDescriptiveAnalysisTemplate(fileName)
            else:
                self.saveTemplate('Descriptive Analysis of Regional Economy', fileName)
                fileSaved = True
            
            self.loadTemplateFiles()
            
            # Load the newly saved template file
            if fileSaved:
                self.handlerLoadDescriptiveAnalysisTemplate(fileName)
    
    
    def handlerSelectSingleIntermediateConsumptionMatrix(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Intermediate Consumption Matrix', QtCore.QDir.homePath(), 'Intermediate Consumption Matrix (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditSingleIntermediateConsumptionMatrix.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectSingleValueAddedMatrix(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Value Added Matrix', QtCore.QDir.homePath(), 'Value Added Matrix (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditSingleValueAddedMatrix.setText(file) 
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectSingleFinalConsumptionMatrix(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Final Consumption Matrix', QtCore.QDir.homePath(), 'Final Consumption Matrix (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditSingleFinalConsumptionMatrix.setText(file) 
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectSingleLabourRequirement(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Labour Requirement', QtCore.QDir.homePath(), 'Labour Requirement (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditSingleLabourRequirement.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectOtherValueAddedComponent(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Value Added Component', QtCore.QDir.homePath(), 'Value Added Component (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditOtherValueAddedComponent.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectOtherFinalConsumptionComponent(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Final Consumption Component', QtCore.QDir.homePath(), 'Final Consumption Component (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditOtherFinalConsumptionComponent.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectOtherListOfEconomicSector(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select List of Economic Sector', QtCore.QDir.homePath(), 'List of Economic Sector (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditOtherListOfEconomicSector.setText(file) 
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectMultipleIntermediateConsumptionMatrix(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Intermediate Consumption Matrix', QtCore.QDir.homePath(), 'Intermediate Consumption Matrix (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditMultipleIntermediateConsumptionMatrix.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectMultipleValueAddedMatrix(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Value Added Matrix', QtCore.QDir.homePath(), 'Value Added Matrix (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditMultipleValueAddedMatrix.setText(file) 
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectMultipleFinalConsumptionMatrix(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Final Consumption Matrix', QtCore.QDir.homePath(), 'Final Consumption Matrix (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditMultipleFinalConsumptionMatrix.setText(file) 
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectMultipleLabourRequirement(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Labour Requirement', QtCore.QDir.homePath(), 'Labour Requirement (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditMultipleLabourRequirement.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    #***********************************************************
    # 'Regional Economic Impact Scenario' tab QPushButton handlers
    #***********************************************************
    def handlerLoadRegionalEconomicScenarioImpactTemplate(self, fileName=None):
        """Slot method for loading a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.comboBoxRegionalEconomicScenarioImpactTemplate.currentText()
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
            self.loadTemplate('Regional Economic Scenario Impact', templateFile)
    
    
    def handlerSaveRegionalEconomicScenarioImpactTemplate(self, fileName=None):
        """Slot method for saving a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.currentRegionalEconomicScenarioImpactTemplate
        
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
            self.saveTemplate('Regional Economic Scenario Impact', templateFile)
            return True
        else:
            return False
    
    
    def handlerSaveAsRegionalEconomicScenarioImpactTemplate(self):
        """Slot method for saving a module template to a new file.
        """
        fileName, ok = QtGui.QInputDialog.getText(self, 'Save As', 'Enter a new template name:')
        fileSaved = False
        
        if ok:
            now = QtCore.QDateTime.currentDateTime().toString('yyyyMMdd-hhmmss')
            fileName = now + '__' + fileName + '.ini'
            
            if os.path.exists(os.path.join(self.settingsPath, fileName)):
                fileSaved = self.handlerSaveRegionalEconomicScenarioImpactTemplate(fileName)
            else:
                self.saveTemplate('Regional Economic Scenario Impact', fileName)
                fileSaved = True
            
            self.loadTemplateFiles()
            
            # Load the newly saved template file
            if fileSaved:
                self.handlerLoadRegionalEconomicScenarioImpactTemplate(fileName)
    
    
    def handlerSelectRegionalEconomicScenarioImpactFinalDemandChangeScenario(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Final Demand Change Scenario', QtCore.QDir.homePath(), 'Final Demand Change Scenario (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditRegionalEconomicScenarioImpactFinalDemandChangeScenario.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectRegionalEconomicScenarioImpactGDPChangeScenario(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select GDP Change Scenario', QtCore.QDir.homePath(), 'Final Demand Change Scenario (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditRegionalEconomicScenarioImpactGDPChangeScenario.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectRegionalEconomicScenarioImpactIntermediateConsumptionMatrix(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Intermediate Consumption Matrix', QtCore.QDir.homePath(), 'Intermediate Consumption Matrix (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditRegionalEconomicScenarioImpactIntermediateConsumptionMatrix.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectRegionalEconomicScenarioImpactValueAddedMatrix(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Value Added Matrix', QtCore.QDir.homePath(), 'Value Added Matrix (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditRegionalEconomicScenarioImpactValueAddedMatrix.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectRegionalEconomicScenarioImpactFinalConsumptionMatrix(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Final Consumption Matrix', QtCore.QDir.homePath(), 'Final Consumption Matrix (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditRegionalEconomicScenarioImpactFinalConsumptionMatrix.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectRegionalEconomicScenarioImpactValueAddedComponent(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Value Added Component', QtCore.QDir.homePath(), 'Value Added Component (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditRegionalEconomicScenarioImpactValueAddedComponent.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectRegionalEconomicScenarioImpactFinalConsumptionComponent(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Final Consumption Component', QtCore.QDir.homePath(), 'Final Consumption Component (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditRegionalEconomicScenarioImpactFinalConsumptionComponent.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectRegionalEconomicScenarioImpactListOfEconomicSector(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select List of Economic Sector', QtCore.QDir.homePath(), 'List of Economic Sector (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditRegionalEconomicScenarioImpactListOfEconomicSector.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectRegionalEconomicScenarioImpactLandDistributionMatrix(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Distribution Matrix', QtCore.QDir.homePath(), 'Land Distribution Matrix (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditRegionalEconomicScenarioImpactLandDistributionMatrix.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectRegionalEconomicScenarioImpactLandRequirementCoefficientMatrix(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Requirement Coefficient Matrix', QtCore.QDir.homePath(), 'Land Requirement Coefficient Matrix (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditRegionalEconomicScenarioImpactLandRequirementCoefficientMatrix.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectRegionalEconomicScenarioImpactLandCoverComponent(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Cover Component', QtCore.QDir.homePath(), 'Land Cover Component (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditRegionalEconomicScenarioImpactLandCoverComponent.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectRegionalEconomicScenarioImpactLabourRequirement(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Labour Requirement', QtCore.QDir.homePath(), 'Labour Requirement (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditRegionalEconomicScenarioImpactLabourRequirement.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    #***********************************************************
    # 'Land Requirement Analysis' tab QPushButton handlers
    #***********************************************************
    def handlerLoadLandRequirementAnalysisTemplate(self, fileName=None):
        """Slot method for loading a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.comboBoxLandRequirementAnalysisTemplate.currentText()
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
            self.loadTemplate('Land Requirement Analysis', templateFile)
    
    
    def handlerSaveLandRequirementAnalysisTemplate(self, fileName=None):
        """Slot method for saving a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.currentLandRequirementAnalysisTemplate
        
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
            self.saveTemplate('Land Requirement Analysis', templateFile)
            return True
        else:
            return False
    
    
    def handlerSaveAsLandRequirementAnalysisTemplate(self):
        """Slot method for saving a module template to a new file.
        """
        fileName, ok = QtGui.QInputDialog.getText(self, 'Save As', 'Enter a new template name:')
        fileSaved = False
        
        if ok:
            now = QtCore.QDateTime.currentDateTime().toString('yyyyMMdd-hhmmss')
            fileName = now + '__' + fileName + '.ini'
            
            if os.path.exists(os.path.join(self.settingsPath, fileName)):
                fileSaved = self.handlerSaveLandRequirementAnalysisTemplate(fileName)
            else:
                self.saveTemplate('Land Requirement Analysis', fileName)
                fileSaved = True
            
            self.loadTemplateFiles()
            
            # Load the newly saved template file
            if fileSaved:
                self.handlerLoadLandRequirementAnalysisTemplate(fileName)
    
    
    def handlerSelectLandRequirementAnalysisIntermediateConsumptionMatrix(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Intermediate Consumption Matrix', QtCore.QDir.homePath(), 'Intermediate Consumption Matrix (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditLandRequirementAnalysisIntermediateConsumptionMatrix.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectLandRequirementAnalysisValueAddedMatrix(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Value Added Matrix', QtCore.QDir.homePath(), 'Value Added Matrix (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditLandRequirementAnalysisValueAddedMatrix.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectLandRequirementAnalysisFinalConsumptionMatrix(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Final Consumption Matrix', QtCore.QDir.homePath(), 'Final Consumption Matrix (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditLandRequirementAnalysisFinalConsumptionMatrix.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectLandRequirementAnalysisValueAddedComponent(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Value Added Component', QtCore.QDir.homePath(), 'Value Added Component (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditLandRequirementAnalysisValueAddedComponent.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectLandRequirementAnalysisFinalConsumptionComponent(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Final Consumption Component', QtCore.QDir.homePath(), 'Final Consumption Component (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditLandRequirementAnalysisFinalConsumptionComponent.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectLandRequirementAnalysisListOfEconomicSector(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select List of Economic Sector', QtCore.QDir.homePath(), 'List of Economic Sector (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditLandRequirementAnalysisListOfEconomicSector.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectLandRequirementAnalysisLandDistributionMatrix(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Distribution Matrix', QtCore.QDir.homePath(), 'Land Distribution Matrix (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditLandRequirementAnalysisLandDistributionMatrix.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectLandRequirementAnalysisLandCoverComponent(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Cover Component', QtCore.QDir.homePath(), 'Land Cover Component (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditLandRequirementAnalysisLandCoverComponent.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectLandRequirementAnalysisLabourRequirement(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Labour Requirement', QtCore.QDir.homePath(), 'Labour Requirement (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditLandRequirementAnalysisLabourRequirement.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    #***********************************************************
    # 'Land Use Change Impact' tab QPushButton handlers
    #***********************************************************
    def handlerLoadLandUseChangeImpactTemplate(self, fileName=None):
        """Slot method for loading a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.comboBoxLandUseChangeImpactTemplate.currentText()
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
            self.loadTemplate('Land Use Change Impact', templateFile)
    
    
    def handlerSaveLandUseChangeImpactTemplate(self, fileName=None):
        """Slot method for saving a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.currentLandUseChangeImpactTemplate
        
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
            self.saveTemplate('Land Use Change Impact', templateFile)
            return True
        else:
            return False
    
    
    def handlerSaveAsLandUseChangeImpactTemplate(self):
        """Slot method for saving a module template to a new file.
        """
        fileName, ok = QtGui.QInputDialog.getText(self, 'Save As', 'Enter a new template name:')
        fileSaved = False
        
        if ok:
            now = QtCore.QDateTime.currentDateTime().toString('yyyyMMdd-hhmmss')
            fileName = now + '__' + fileName + '.ini'
            
            if os.path.exists(os.path.join(self.settingsPath, fileName)):
                fileSaved = self.handlerSaveLandUseChangeImpactTemplate(fileName)
            else:
                self.saveTemplate('Land Use Change Impact', fileName)
                fileSaved = True
            
            self.loadTemplateFiles()
            
            # Load the newly saved template file
            if fileSaved:
                self.handlerLoadLandUseChangeImpactTemplate(fileName)
    
    
    def handlerSelectLandUseChangeImpactIntermediateConsumptionMatrix(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Intermediate Consumption Matrix', QtCore.QDir.homePath(), 'Intermediate Consumption Matrix (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditLandUseChangeImpactIntermediateConsumptionMatrix.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectLandUseChangeImpactValueAddedMatrix(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Value Added Matrix', QtCore.QDir.homePath(), 'Value Added Matrix (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditLandUseChangeImpactValueAddedMatrix.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectLandUseChangeImpactFinalConsumptionMatrix(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Final Consumption Matrix', QtCore.QDir.homePath(), 'Final Consumption Matrix (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditLandUseChangeImpactFinalConsumptionMatrix.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectLandUseChangeImpactValueAddedComponent(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Value Added Component', QtCore.QDir.homePath(), 'Value Added Component (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditLandUseChangeImpactValueAddedComponent.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectLandUseChangeImpactFinalConsumptionComponent(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Final Consumption Component', QtCore.QDir.homePath(), 'Final Consumption Component (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditLandUseChangeImpactFinalConsumptionComponent.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectLandUseChangeImpactListOfEconomicSector(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select List of Economic Sector', QtCore.QDir.homePath(), 'List of Economic Sector (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditLandUseChangeImpactListOfEconomicSector.setText(file)
            
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectLandUseChangeImpactLandDistributionMatrix(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Distribution Matrix', QtCore.QDir.homePath(), 'Land Distribution Matrix (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditLandUseChangeImpactLandDistributionMatrix.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectLandUseChangeImpactLandRequirementCoefficientMatrix(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Requirement Coefficient Matrix', QtCore.QDir.homePath(), 'Land Requirement Coefficient Matrix (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditLandUseChangeImpactLandRequirementCoefficientMatrix.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectLandUseChangeImpactLandCoverComponent(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Cover Component', QtCore.QDir.homePath(), 'Land Cover Component (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditLandUseChangeImpactLandCoverComponent.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectLandUseChangeImpactLabourRequirement(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Labour Requirement', QtCore.QDir.homePath(), 'Labour Requirement (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditLandUseChangeImpactLabourRequirement.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    #***********************************************************
    # Process tabs
    #***********************************************************
    def setAppSettings(self):
        """Set the required values from the form widgets.
        """
        # 'Descriptive Analysis of Regional Economy' tab fields
        self.main.appSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['period'] \
            = self.main.appSettings['DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis']['period1'] \
            = self.spinBoxSinglePeriod.value()
        self.main.appSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['intermediateConsumptionMatrix'] \
            = self.main.appSettings['DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis']['intermediateConsumptionMatrixP1'] \
            = unicode(self.lineEditSingleIntermediateConsumptionMatrix.text())
        self.main.appSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['valueAddedMatrix'] \
            = self.main.appSettings['DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis']['valueAddedMatrixP1'] \
            = unicode(self.lineEditSingleValueAddedMatrix.text())
        self.main.appSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['finalConsumptionMatrix'] \
            = self.main.appSettings['DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis']['finalConsumptionMatrixP1'] \
            = unicode(self.lineEditSingleFinalConsumptionMatrix.text())
        self.main.appSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['labourRequirement'] \
            = self.main.appSettings['DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis']['labourRequirementP1'] \
            = unicode(self.lineEditSingleLabourRequirement.text())
        
        self.main.appSettings['DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis']['period2'] \
            = self.spinBoxMultiplePeriod.value()
        self.main.appSettings['DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis']['intermediateConsumptionMatrixP2'] \
            = unicode(self.lineEditMultipleIntermediateConsumptionMatrix.text())
        self.main.appSettings['DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis']['valueAddedMatrixP2'] \
            = unicode(self.lineEditMultipleValueAddedMatrix.text())
        self.main.appSettings['DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis']['finalConsumptionMatrixP2'] \
            = unicode(self.lineEditMultipleFinalConsumptionMatrix.text())
        self.main.appSettings['DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis']['labourRequirementP2'] \
            = unicode(self.lineEditMultipleLabourRequirement.text())
        
        self.main.appSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['valueAddedComponent'] \
            = self.main.appSettings['DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis']['valueAddedComponent'] \
            = unicode(self.lineEditOtherValueAddedComponent.text())
        self.main.appSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['finalConsumptionComponent'] \
            = self.main.appSettings['DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis']['finalConsumptionComponent'] \
            = unicode(self.lineEditOtherFinalConsumptionComponent.text())
        self.main.appSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['listOfEconomicSector'] \
            = self.main.appSettings['DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis']['listOfEconomicSector'] \
            = unicode(self.lineEditOtherListOfEconomicSector.text())
        self.main.appSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['financialUnit'] \
            = self.main.appSettings['DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis']['financialUnit'] \
            = unicode(self.lineEditOtherFinancialUnit.text())
        self.main.appSettings['DialogLumensTARegionalEconomySingleIODescriptiveAnalysis']['areaName'] \
            = self.main.appSettings['DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis']['areaName'] \
            = unicode(self.lineEditOtherAreaName.text())
        
        # 'Regional Economic Scenario Impact' tab fields
        self.main.appSettings['DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis']['intermediateConsumptionMatrix'] \
            = self.main.appSettings['DialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis']['intermediateConsumptionMatrix'] \
            = unicode(self.lineEditRegionalEconomicScenarioImpactIntermediateConsumptionMatrix.text())
        self.main.appSettings['DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis']['valueAddedMatrix'] \
            = self.main.appSettings['DialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis']['valueAddedMatrix'] \
            = unicode(self.lineEditRegionalEconomicScenarioImpactValueAddedMatrix.text())
        self.main.appSettings['DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis']['finalConsumptionMatrix'] \
            = self.main.appSettings['DialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis']['finalConsumptionMatrix'] \
            = unicode(self.lineEditRegionalEconomicScenarioImpactFinalConsumptionMatrix.text())
        self.main.appSettings['DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis']['valueAddedComponent'] \
            = self.main.appSettings['DialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis']['valueAddedComponent'] \
            = unicode(self.lineEditRegionalEconomicScenarioImpactValueAddedComponent.text())
        self.main.appSettings['DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis']['finalConsumptionComponent'] \
            = self.main.appSettings['DialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis']['finalConsumptionComponent'] \
            = unicode(self.lineEditRegionalEconomicScenarioImpactFinalConsumptionComponent.text())
        self.main.appSettings['DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis']['listOfEconomicSector'] \
            = self.main.appSettings['DialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis']['listOfEconomicSector'] \
            = unicode(self.lineEditRegionalEconomicScenarioImpactListOfEconomicSector.text())
        self.main.appSettings['DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis']['landDistributionMatrix'] \
            = self.main.appSettings['DialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis']['landDistributionMatrix'] \
            = unicode(self.lineEditRegionalEconomicScenarioImpactLandDistributionMatrix.text())
        self.main.appSettings['DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis']['landRequirementCoefficientMatrix'] \
            = self.main.appSettings['DialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis']['landRequirementCoefficientMatrix'] \
            = unicode(self.lineEditRegionalEconomicScenarioImpactLandRequirementCoefficientMatrix.text())
        self.main.appSettings['DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis']['landCoverComponent'] \
            = self.main.appSettings['DialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis']['landCoverComponent'] \
            = unicode(self.lineEditRegionalEconomicScenarioImpactLandCoverComponent.text())
        self.main.appSettings['DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis']['financialUnit'] \
            = self.main.appSettings['DialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis']['financialUnit'] \
            = unicode(self.lineEditRegionalEconomicScenarioImpactFinancialUnit.text())
        self.main.appSettings['DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis']['areaName'] \
            = self.main.appSettings['DialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis']['areaName'] \
            = unicode(self.lineEditRegionalEconomicScenarioImpactAreaName.text())
        self.main.appSettings['DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis']['period'] \
            = self.main.appSettings['DialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis']['period'] \
            = self.spinBoxRegionalEconomicScenarioImpactPeriod.value()
        self.main.appSettings['DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis']['finalDemandChangeScenario'] \
            = unicode(self.lineEditRegionalEconomicScenarioImpactFinalDemandChangeScenario.text())
        self.main.appSettings['DialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis']['gdpChangeScenario'] \
            = unicode(self.lineEditRegionalEconomicScenarioImpactGDPChangeScenario.text())
        
        # 'Land Requirement Analysis' tab fields
        self.main.appSettings['DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis']['intermediateConsumptionMatrix'] \
            = unicode(self.lineEditLandRequirementAnalysisIntermediateConsumptionMatrix.text())
        self.main.appSettings['DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis']['valueAddedMatrix'] \
            = unicode(self.lineEditLandRequirementAnalysisValueAddedMatrix.text())
        self.main.appSettings['DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis']['finalConsumptionMatrix'] \
            = unicode(self.lineEditLandRequirementAnalysisFinalConsumptionMatrix.text())
        self.main.appSettings['DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis']['valueAddedComponent'] \
            = unicode(self.lineEditLandRequirementAnalysisValueAddedComponent.text())
        self.main.appSettings['DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis']['finalConsumptionComponent'] \
            = unicode(self.lineEditLandRequirementAnalysisFinalConsumptionComponent.text())
        self.main.appSettings['DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis']['listOfEconomicSector'] \
            = unicode(self.lineEditLandRequirementAnalysisListOfEconomicSector.text())
        self.main.appSettings['DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis']['landDistributionMatrix'] \
            = unicode(self.lineEditLandRequirementAnalysisLandDistributionMatrix.text())
        self.main.appSettings['DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis']['landCoverComponent'] \
            = unicode(self.lineEditLandRequirementAnalysisLandCoverComponent.text())
        self.main.appSettings['DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis']['labourRequirement'] \
            = unicode(self.lineEditLandRequirementAnalysisLabourRequirement.text())
        self.main.appSettings['DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis']['financialUnit'] \
            = unicode(self.lineEditLandRequirementAnalysisFinancialUnit.text())
        self.main.appSettings['DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis']['areaName'] \
            = unicode(self.lineEditLandRequirementAnalysisAreaName.text())
        self.main.appSettings['DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis']['period'] \
            = self.spinBoxLandRequirementAnalysisPeriod.value()
        
        # 'Land Use Change Impact' tab fields
        self.main.appSettings['DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis']['intermediateConsumptionMatrix'] \
            = unicode(self.lineEditLandUseChangeImpactIntermediateConsumptionMatrix.text())
        self.main.appSettings['DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis']['valueAddedMatrix'] \
            = unicode(self.lineEditLandUseChangeImpactValueAddedMatrix.text())
        self.main.appSettings['DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis']['finalConsumptionMatrix'] \
            = unicode(self.lineEditLandUseChangeImpactFinalConsumptionMatrix.text())
        self.main.appSettings['DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis']['valueAddedComponent'] \
            = unicode(self.lineEditLandUseChangeImpactValueAddedComponent.text())
        self.main.appSettings['DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis']['finalConsumptionComponent'] \
            = unicode(self.lineEditLandUseChangeImpactFinalConsumptionComponent.text())
        self.main.appSettings['DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis']['listOfEconomicSector'] \
            = unicode(self.lineEditLandUseChangeImpactListOfEconomicSector.text())
        self.main.appSettings['DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis']['landDistributionMatrix'] \
            = unicode(self.lineEditLandUseChangeImpactLandDistributionMatrix.text())
        self.main.appSettings['DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis']['landRequirementCoefficientMatrix'] \
            = unicode(self.lineEditLandUseChangeImpactLandRequirementCoefficientMatrix.text())
        self.main.appSettings['DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis']['landCoverComponent'] \
            = unicode(self.lineEditLandUseChangeImpactLandCoverComponent.text())
        self.main.appSettings['DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis']['labourRequirement'] \
            = unicode(self.lineEditLandUseChangeImpactLabourRequirement.text())
        self.main.appSettings['DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis']['financialUnit'] \
            = unicode(self.lineEditLandUseChangeImpactFinancialUnit.text())
        self.main.appSettings['DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis']['areaName'] \
            = unicode(self.lineEditLandUseChangeImpactAreaName.text())
        self.main.appSettings['DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis']['period'] \
            = self.spinBoxLandUseChangeImpactPeriod.value()
    
    
    def handlerProcessDescriptiveAnalysis(self):
        """Slot method to pass the form values and execute the "TA Descriptive Analysis of Regional Economy" R algorithms.
        
        Depending on the checked groupbox, the "TA Descriptive Analysis of Regional Economy" process calls the following algorithms:
        1. modeler:ta_reg_io_da
        2. modeler:ta_reg_ts_io
        """
        self.setAppSettings()
        
        formName = 'DialogLumensTARegionalEconomySingleIODescriptiveAnalysis'
        algName = 'modeler:ta_reg_io_da'
        
        if self.validForm(formName):
            logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
            logging.getLogger(self.historyLog).info('alg start: %s' % formName)
            self.buttonProcessDescriptiveAnalysis.setDisabled(True)
            
            # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
            self.main.setWindowState(QtCore.Qt.WindowMinimized)
            
            outputs = general.runalg(
                algName,
                self.main.appSettings[formName]['intermediateConsumptionMatrix'],
                self.main.appSettings[formName]['valueAddedMatrix'],
                self.main.appSettings[formName]['finalConsumptionMatrix'],
                self.main.appSettings[formName]['valueAddedComponent'],
                self.main.appSettings[formName]['finalConsumptionComponent'],
                self.main.appSettings[formName]['listOfEconomicSector'],
                self.main.appSettings[formName]['labourRequirement'],
                self.main.appSettings[formName]['financialUnit'],
                self.main.appSettings[formName]['areaName'],
                self.main.appSettings[formName]['period'],
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
        
        # Run multiple period if checked
        if self.checkBoxMultiplePeriod.isChecked():
            formName = 'DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis'
            algName = 'modeler:ta_reg_ts_io'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                logging.getLogger(self.historyLog).info('alg start: %s' % formName)
                self.buttonProcessDescriptiveAnalysis.setDisabled(True)
                
                # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                self.main.setWindowState(QtCore.Qt.WindowMinimized)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['intermediateConsumptionMatrixP1'],
                    self.main.appSettings[formName]['intermediateConsumptionMatrixP2'],
                    self.main.appSettings[formName]['valueAddedMatrixP1'],
                    self.main.appSettings[formName]['valueAddedMatrixP2'],
                    self.main.appSettings[formName]['finalConsumptionMatrixP1'],
                    self.main.appSettings[formName]['finalConsumptionMatrixP2'],
                    self.main.appSettings[formName]['valueAddedComponent'],
                    self.main.appSettings[formName]['finalConsumptionComponent'],
                    self.main.appSettings[formName]['listOfEconomicSector'],
                    self.main.appSettings[formName]['labourRequirementP1'],
                    self.main.appSettings[formName]['labourRequirementP2'],
                    self.main.appSettings[formName]['financialUnit'],
                    self.main.appSettings[formName]['areaName'],
                    self.main.appSettings[formName]['period1'],
                    self.main.appSettings[formName]['period2'],
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
    
    
    def handlerProcessRegionalEconomicScenarioImpact(self):
        """Slot method to pass the form values and execute the "TA Regional Economic Scenario Impact" R algorithms.
        
        Depending on the checked groupbox, the "TA Regional Economic Scenario Impact" process calls the following algorithms:
        1. modeler:ta_reg_luc_5a_lcc_fd
        2. modeler:ta_reg_luc_5a_lcc_gdp
        """
        self.setAppSettings()
        
        if self.checkBoxRegionalEconomicScenarioImpactFinalDemand.isChecked():
            formName = 'DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis'
            algName = 'modeler:ta_reg_luc_5a_lcc_fd'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                logging.getLogger(self.historyLog).info('alg start: %s' % formName)
                self.buttonProcessRegionalEconomicScenarioImpact.setDisabled(True)
                
                # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                self.main.setWindowState(QtCore.Qt.WindowMinimized)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['intermediateConsumptionMatrix'],
                    self.main.appSettings[formName]['valueAddedMatrix'],
                    self.main.appSettings[formName]['finalConsumptionMatrix'],
                    self.main.appSettings[formName]['valueAddedComponent'],
                    self.main.appSettings[formName]['finalConsumptionComponent'],
                    self.main.appSettings[formName]['listOfEconomicSector'],
                    self.main.appSettings[formName]['landDistributionMatrix'],
                    self.main.appSettings[formName]['landRequirementCoefficientMatrix'],
                    self.main.appSettings[formName]['landCoverComponent'],
                    self.main.appSettings[formName]['labourRequirement'],
                    self.main.appSettings[formName]['financialUnit'],
                    self.main.appSettings[formName]['areaName'],
                    self.main.appSettings[formName]['period'],
                    self.main.appSettings[formName]['finalDemandChangeScenario'],
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
            algName = 'modeler:ta_reg_luc_5a_lcc_gdp'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                logging.getLogger(self.historyLog).info('alg start: %s' % formName)
                self.buttonProcessRegionalEconomicScenarioImpact.setDisabled(True)
                
                # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                self.main.setWindowState(QtCore.Qt.WindowMinimized)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['intermediateConsumptionMatrix'],
                    self.main.appSettings[formName]['valueAddedMatrix'],
                    self.main.appSettings[formName]['finalConsumptionMatrix'],
                    self.main.appSettings[formName]['valueAddedComponent'],
                    self.main.appSettings[formName]['finalConsumptionComponent'],
                    self.main.appSettings[formName]['listOfEconomicSector'],
                    self.main.appSettings[formName]['landDistributionMatrix'],
                    self.main.appSettings[formName]['landRequirementCoefficientMatrix'],
                    self.main.appSettings[formName]['landCoverComponent'],
                    self.main.appSettings[formName]['labourRequirement'],
                    self.main.appSettings[formName]['gdpChangeScenario'],
                    self.main.appSettings[formName]['financialUnit'],
                    self.main.appSettings[formName]['areaName'],
                    self.main.appSettings[formName]['period'],
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
    
    
    def handlerProcessLandRequirementAnalysis(self):
        """Slot method to pass the form values and execute the "TA Land Requirement Analysis" R algorithm.
        
        The "TA Land Requirement Analysis" process calls the following algorithm:
        1. modeler:ta_reg_ld_lr
        """
        self.setAppSettings()
        
        formName = 'DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis'
        algName = 'modeler:ta_reg_ld_lr'
        
        if self.validForm(formName):
            logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
            logging.getLogger(self.historyLog).info('alg start: %s' % formName)
            self.buttonProcessDescriptiveAnalysis.setDisabled(True)
            
            # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
            self.main.setWindowState(QtCore.Qt.WindowMinimized)
            
            outputs = general.runalg(
                algName,
                self.main.appSettings[formName]['intermediateConsumptionMatrix'],
                self.main.appSettings[formName]['valueAddedMatrix'],
                self.main.appSettings[formName]['finalConsumptionMatrix'],
                self.main.appSettings[formName]['valueAddedComponent'],
                self.main.appSettings[formName]['finalConsumptionComponent'],
                self.main.appSettings[formName]['listOfEconomicSector'],
                self.main.appSettings[formName]['landDistributionMatrix'],
                self.main.appSettings[formName]['landCoverComponent'],
                self.main.appSettings[formName]['labourRequirement'],
                self.main.appSettings[formName]['financialUnit'],
                self.main.appSettings[formName]['areaName'],
                self.main.appSettings[formName]['period'],
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
    
    
    def handlerProcessLandUseChangeImpact(self):
        """Slot method to pass the form values and execute the "TA Land Use Change Impact" R algorithm.
        
        The "TA Land Use Change Impact" process calls the following algorithm:
        1. modeler:ta_reg_luc_gdp_lcc
        """
        self.setAppSettings()
        
        formName = 'DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis'
        algName = 'modeler:ta_reg_luc_gdp_lcc'
        
        if self.validForm(formName):
            logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
            logging.getLogger(self.historyLog).info('alg start: %s' % formName)
            self.buttonProcessDescriptiveAnalysis.setDisabled(True)
            
            # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
            self.main.setWindowState(QtCore.Qt.WindowMinimized)
            
            outputs = general.runalg(
                algName,
                self.main.appSettings[formName]['intermediateConsumptionMatrix'],
                self.main.appSettings[formName]['valueAddedMatrix'],
                self.main.appSettings[formName]['finalConsumptionMatrix'],
                self.main.appSettings[formName]['valueAddedComponent'],
                self.main.appSettings[formName]['finalConsumptionComponent'],
                self.main.appSettings[formName]['listOfEconomicSector'],
                self.main.appSettings[formName]['landDistributionMatrix'],
                self.main.appSettings[formName]['landRequirementCoefficientMatrix'],
                self.main.appSettings[formName]['landCoverComponent'],
                self.main.appSettings[formName]['labourRequirement'],
                self.main.appSettings[formName]['financialUnit'],
                self.main.appSettings[formName]['areaName'],
                self.main.appSettings[formName]['period'],
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
    
