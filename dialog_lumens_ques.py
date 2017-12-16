#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, csv, datetime, glob
from qgis.core import *
from processing.tools import *
from PyQt4 import QtCore, QtGui

from utils import QPlainTextEditLogger
from dialog_lumens_base import DialogLumensBase
from dialog_lumens_viewer import DialogLumensViewer
import resource


class DialogLumensQUES(QtGui.QDialog, DialogLumensBase):
    """ LUMENS "QUES" module dialog class.
    """
    
    def loadTemplateFiles(self):
        """Method for loading the list of module template files inside the project folder.
        
        This method is also called to load the module template files in the main window dashboard tab.
        """
        templateFiles = [os.path.basename(name) for name in glob.glob(os.path.join(self.settingsPath, '*.ini')) if os.path.isfile(os.path.join(self.settingsPath, name))]
        
        if templateFiles:
            self.comboBoxPreQUESTemplate.clear()
            self.comboBoxPreQUESTemplate.addItems(sorted(templateFiles))
            self.comboBoxPreQUESTemplate.setEnabled(True)
            self.buttonLoadPreQUESTemplate.setEnabled(True)
            
            self.comboBoxQUESCTemplate.clear()
            self.comboBoxQUESCTemplate.addItems(sorted(templateFiles))
            self.comboBoxQUESCTemplate.setEnabled(True)
            self.buttonLoadQUESCTemplate.setEnabled(True)
            
            self.comboBoxQUESBTemplate.clear()
            self.comboBoxQUESBTemplate.addItems(sorted(templateFiles))
            self.comboBoxQUESBTemplate.setEnabled(True)
            self.buttonLoadQUESBTemplate.setEnabled(True)
            
            self.comboBoxHRUDefinitionTemplate.clear()
            self.comboBoxHRUDefinitionTemplate.addItems(sorted(templateFiles))
            self.comboBoxHRUDefinitionTemplate.setEnabled(True)
            self.buttonLoadHRUDefinitionTemplate.setEnabled(True)
            
            self.comboBoxWatershedModelEvaluationTemplate.clear()
            self.comboBoxWatershedModelEvaluationTemplate.addItems(sorted(templateFiles))
            self.comboBoxWatershedModelEvaluationTemplate.setEnabled(True)
            self.buttonLoadWatershedModelEvaluationTemplate.setEnabled(True)
            
            self.comboBoxWatershedIndicatorsTemplate.clear()
            self.comboBoxWatershedIndicatorsTemplate.addItems(sorted(templateFiles))
            self.comboBoxWatershedIndicatorsTemplate.setEnabled(True)
            self.buttonLoadWatershedIndicatorsTemplate.setEnabled(True)
            
            # MainWindow QUES dashboard templates
            self.main.comboBoxPreQUESTemplate.clear()
            self.main.comboBoxPreQUESTemplate.addItems(sorted(templateFiles))
            self.main.comboBoxPreQUESTemplate.setEnabled(True)
            
            self.main.comboBoxQUESCTemplate.clear()
            self.main.comboBoxQUESCTemplate.addItems(sorted(templateFiles))
            self.main.comboBoxQUESCTemplate.setEnabled(True)
            self.main.buttonProcessQUESCTemplate.setEnabled(True)
            
            self.main.comboBoxQUESBTemplate.clear()
            self.main.comboBoxQUESBTemplate.addItems(sorted(templateFiles))
            self.main.comboBoxQUESBTemplate.setEnabled(True)
            
            self.main.comboBoxHRUDefinitionTemplate.clear()
            self.main.comboBoxHRUDefinitionTemplate.addItems(sorted(templateFiles))
            self.main.comboBoxHRUDefinitionTemplate.setEnabled(True)
            
            self.main.comboBoxWatershedModelEvaluationTemplate.clear()
            self.main.comboBoxWatershedModelEvaluationTemplate.addItems(sorted(templateFiles))
            self.main.comboBoxWatershedModelEvaluationTemplate.setEnabled(True)
            
            self.main.comboBoxWatershedIndicatorsTemplate.clear()
            self.main.comboBoxWatershedIndicatorsTemplate.addItems(sorted(templateFiles))
            self.main.comboBoxWatershedIndicatorsTemplate.setEnabled(True)
        else:
            self.comboBoxPreQUESTemplate.setDisabled(True)
            self.buttonLoadPreQUESTemplate.setDisabled(True)
            
            self.comboBoxQUESCTemplate.setDisabled(True)
            self.buttonLoadQUESCTemplate.setDisabled(True)
            
            self.comboBoxQUESBTemplate.setDisabled(True)
            self.buttonLoadQUESBTemplate.setDisabled(True)
            
            self.comboBoxHRUDefinitionTemplate.setDisabled(True)
            self.buttonLoadHRUDefinitionTemplate.setDisabled(True)
            
            self.comboBoxWatershedModelEvaluationTemplate.setDisabled(True)
            self.buttonLoadWatershedModelEvaluationTemplate.setDisabled(True)
            
            self.comboBoxWatershedIndicatorsTemplate.setDisabled(True)
            self.buttonLoadWatershedIndicatorsTemplate.setDisabled(True)
            
            # MainWindow QUES dashboard templates
            self.main.comboBoxPreQUESTemplate.setDisabled(True)
            
            self.main.comboBoxQUESCTemplate.setDisabled(True)
            self.main.buttonProcessQUESCTemplate.setDisabled(True)
            
            self.main.comboBoxQUESBTemplate.setDisabled(True)
            self.main.buttonProcessQUESBTemplate.setDisabled(True)
            
            self.main.comboBoxHRUDefinitionTemplate.setDisabled(True)
            self.main.comboBoxWatershedModelEvaluationTemplate.setDisabled(True)
            self.main.comboBoxWatershedIndicatorsTemplate.setDisabled(True)
            self.main.buttonProcessQUESHTemplate.setDisabled(True)
            
    
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
        
        if tabName == 'Pre-QUES':
            dialogsToLoad = (
                'DialogLumensPreQUESLandcoverTrajectoriesAnalysis',
            )
            
            # start tab
            settings.beginGroup(tabName)
            
            # 'Pre-QUES' tab widgets
            # start dialog
            settings.beginGroup('DialogLumensPreQUESLandcoverTrajectoriesAnalysis')
            
            templateSettings['DialogLumensPreQUESLandcoverTrajectoriesAnalysis'] = {}
            templateSettings['DialogLumensPreQUESLandcoverTrajectoriesAnalysis']['landUse1'] = landUse1 = settings.value('landUse1')
            templateSettings['DialogLumensPreQUESLandcoverTrajectoriesAnalysis']['landUse2'] = landUse2 = settings.value('landUse2')
            templateSettings['DialogLumensPreQUESLandcoverTrajectoriesAnalysis']['landUseTable'] = landUseTable = settings.value('landUseTable')
            templateSettings['DialogLumensPreQUESLandcoverTrajectoriesAnalysis']['planningUnit'] = planningUnit = settings.value('planningUnit')
            templateSettings['DialogLumensPreQUESLandcoverTrajectoriesAnalysis']['analysisOption'] = analysisOption = settings.value('analysisOption')
            templateSettings['DialogLumensPreQUESLandcoverTrajectoriesAnalysis']['nodata'] = nodata = settings.value('nodata')
            
            if not returnTemplateSettings:
                if landUse1:
                    indexLandCoverLandUse1 = self.comboBoxPreQUESLandCoverLandUse1.findText(landUse1)
                    
                    if indexLandCoverLandUse1 != -1:
                        self.comboBoxPreQUESLandCoverLandUse1.setCurrentIndex(indexLandCoverLandUse1)
                
                if landUse2:
                    indexLandCoverLandUse2 = self.comboBoxPreQUESLandCoverLandUse2.findText(landUse2)
                    
                    if indexLandCoverLandUse2 != -1:
                        self.comboBoxPreQUESLandCoverLandUse2.setCurrentIndex(indexLandCoverLandUse2)
                
                if planningUnit:
                    indexLandCoverPlanningUnit = self.comboBoxPreQUESLandCoverPlanningUnit.findText(planningUnit)
                    
                    if indexLandCoverPlanningUnit != -1:
                        self.comboBoxPreQUESLandCoverPlanningUnit.setCurrentIndex(indexLandCoverPlanningUnit)
                
                if landUseTable:
                    indexLandCoverTable = self.comboBoxPreQUESLandCoverTable.findText(landUseTable)
                    
                    if indexLandCoverTable != -1:
                        self.comboBoxPreQUESLandCoverTable.setCurrentIndex(indexLandCoverTable)                    
                
                if analysisOption:
                    self.comboBoxLandCoverAnalysisOption.setCurrentIndex(int(analysisOption))
                  
                if nodata:
                    self.spinBoxPreQUESNodata.setValue(int(nodata))
                else:
                    self.spinBoxPreQUESNodata.setValue(0)
                
                self.currentPreQUESTemplate = templateFile
                self.loadedPreQUESTemplate.setText(templateFile)
                self.comboBoxPreQUESTemplate.setCurrentIndex(self.comboBoxPreQUESTemplate.findText(templateFile))
                self.buttonSavePreQUESTemplate.setEnabled(True)
            
            settings.endGroup()
            # /dialog
            
            settings.endGroup()
            # /tab
        elif tabName == 'QUES-C':
            dialogsToLoad = (
                'DialogLumensQUESCCarbonAccounting',
            )
            
            # start tab
            settings.beginGroup(tabName)
            
            # 'Carbon accounting' groupbox widgets
            # start dialog
            settings.beginGroup('DialogLumensQUESCCarbonAccounting')
            
            templateSettings['DialogLumensQUESCCarbonAccounting'] = {}
            templateSettings['DialogLumensQUESCCarbonAccounting']['landUse1'] = landUse1 = settings.value('landUse1')
            templateSettings['DialogLumensQUESCCarbonAccounting']['landUse2'] = landUse2 = settings.value('landUse2')
            templateSettings['DialogLumensQUESCCarbonAccounting']['carbonTable'] = carbonTable = settings.value('carbonTable')
            templateSettings['DialogLumensQUESCCarbonAccounting']['planningUnit'] = planningUnit = settings.value('planningUnit')
            templateSettings['DialogLumensQUESCCarbonAccounting']['nodata'] = nodata = settings.value('nodata')            
            
            if not returnTemplateSettings:
                if landUse1:
                    indexLandCoverLandUse1 = self.comboBoxCALandCoverLandUse1.findText(landUse1)
                    
                    if indexLandCoverLandUse1 != -1:
                        self.comboBoxCALandCoverLandUse1.setCurrentIndex(indexLandCoverLandUse1)
                
                if landUse2:
                    indexLandCoverLandUse2 = self.comboBoxCALandCoverLandUse2.findText(landUse2)
                    
                    if indexLandCoverLandUse2 != -1:
                        self.comboBoxCALandCoverLandUse2.setCurrentIndex(indexLandCoverLandUse2)
                
                if planningUnit:
                    indexLandCoverPlanningUnit = self.comboBoxCALandCoverPlanningUnit.findText(planningUnit)
                    
                    if indexLandCoverPlanningUnit != -1:
                        self.comboBoxCALandCoverPlanningUnit.setCurrentIndex(indexLandCoverPlanningUnit)
                
                if carbonTable:
                    indexCarbonTable = self.comboBoxCACarbonTable.findText(carbonTable)
                    
                    if indexCarbonTable != -1:
                        self.comboBoxCACarbonTable.setCurrentIndex(indexCarbonTable)                    
                        
                if nodata:
                    self.spinBoxCANoDataValue.setValue(int(nodata))
                else:
                    self.spinBoxCANoDataValue.setValue(0)
                    
                self.currentQUESCTemplate = templateFile
                self.loadedQUESCTemplate.setText(templateFile)
                self.comboBoxQUESCTemplate.setCurrentIndex(self.comboBoxQUESCTemplate.findText(templateFile))
                self.buttonSaveQUESCTemplate.setEnabled(True)
            
            settings.endGroup()
            # /dialog
                
            settings.endGroup()
            # /tab
        elif tabName == 'QUES-B':
            dialogsToLoad = (
                'DialogLumensQUESBAnalysis',
            )
            
            # start tab
            settings.beginGroup(tabName)
            
            # 'QUES-B' tab widgets
            # start dialog
            settings.beginGroup('DialogLumensQUESBAnalysis')
            
            templateSettings['DialogLumensQUESBAnalysis'] = {}
            templateSettings['DialogLumensQUESBAnalysis']['landUse1'] = landUse1 = settings.value('landUse1')
            templateSettings['DialogLumensQUESBAnalysis']['landUse2'] = landUse2 = settings.value('landUse2')
            templateSettings['DialogLumensQUESBAnalysis']['landUse3'] = landUse3 = settings.value('landUse3')
            templateSettings['DialogLumensQUESBAnalysis']['planningUnit'] = planningUnit = settings.value('planningUnit')
            templateSettings['DialogLumensQUESBAnalysis']['nodata'] = nodata = settings.value('nodata')
            templateSettings['DialogLumensQUESBAnalysis']['edgeContrast'] = edgeContrast = settings.value('edgeContrast')
            # templateSettings['DialogLumensQUESBAnalysis']['habitatLookup'] = habitatLookup = settings.value('habitatLookup')
            templateSettings['DialogLumensQUESBAnalysis']['windowShape'] = windowShape = settings.value('windowShape')
            templateSettings['DialogLumensQUESBAnalysis']['samplingWindowSize'] = samplingWindowSize = settings.value('samplingWindowSize')
            templateSettings['DialogLumensQUESBAnalysis']['samplingGridRes'] = samplingGridRes = settings.value('samplingGridRes')
            
            if not returnTemplateSettings:
                if landUse1:
                    indexLandCoverLandUse1 = self.comboBoxQUESBLandCoverLandUse1.findText(landUse1)
                    if indexLandCoverLandUse1 != -1:
                        self.comboBoxQUESBLandCoverLandUse1.setCurrentIndex(indexLandCoverLandUse1)
                if landUse2:
                    indexLandCoverLandUse2 = self.comboBoxQUESBLandCoverLandUse2.findText(landUse2)
                    if indexLandCoverLandUse2 != -1:
                        self.comboBoxQUESBLandCoverLandUse2.setCurrentIndex(indexLandCoverLandUse2)
                if landUse3:
                    indexLandCoverLandUse3 = self.comboBoxQUESBLandCoverLandUse3.findText(landUse3)
                    if indexLandCoverLandUse3 != -1:
                        self.comboBoxQUESBLandCoverLandUse3.setCurrentIndex(indexLandCoverLandUse3)                       
                if planningUnit:
                    indexPlanningUnit = self.comboBoxQUESBPlanningUnit.findText(planningUnit)
                    if indexPlanningUnit != -1:
                        self.comboBoxQUESBPlanningUnit.setCurrentIndex(indexPlanningUnit)
                if nodata:
                    self.spinBoxQUESBNodata.setValue(int(nodata))
                else:
                    self.spinBoxQUESBNodata.setValue(0)  
                if edgeContrast:
                    indexEdgeContrast = self.comboBoxQUESBEdgeContrast.findText(edgeContrast)
                    if indexEdgeContrast != -1:
                        self.comboBoxQUESBEdgeContrast.setCurrentIndex(indexEdgeContrast)                    
                # if habitatLookup:  
                #    pass
                if windowShape:
                    self.comboBoxQUESBWindowShapeOptions.setCurrentIndex(int(windowShape))                    
                if samplingWindowSize:
                    self.spinBoxQUESBSamplingWindowSize.setValue(int(samplingWindowSize))
                else:
                    self.spinBoxQUESBSamplingWindowSize.setValue(1000)
                if samplingGridRes:
                    self.spinBoxQUESBSamplingGridRes.setValue(int(samplingGridRes))
                else:
                    self.spinBoxQUESBSamplingGridRes.setValue(10000)                    

                
                self.currentQUESBTemplate = templateFile
                self.loadedQUESBTemplate.setText(templateFile)
                self.comboBoxQUESBTemplate.setCurrentIndex(self.comboBoxQUESBTemplate.findText(templateFile))
                self.buttonSaveQUESBTemplate.setEnabled(True)
            
            settings.endGroup()
            # /dialog
            
            settings.endGroup()
            # /tab
        elif tabName == 'Hydrological Response Unit Definition':
            dialogsToLoad = (
                'DialogLumensQUESHDominantHRU',
                'DialogLumensQUESHDominantLUSSL',
                'DialogLumensQUESHMultipleHRU',
            )
            
            # start tab
            settings.beginGroup(tabName)
            
            # 'Hydrological Response Unit Definition' tab widgets
            # start dialog
            settings.beginGroup('DialogLumensQUESHDominantHRU')
            
            templateSettings['DialogLumensQUESHDominantHRU'] = {}
            templateSettings['DialogLumensQUESHDominantHRU']['landUseMap'] = landUseMap = settings.value('landUseMap')
            templateSettings['DialogLumensQUESHDominantHRU']['soilMap'] = soilMap = settings.value('soilMap')
            templateSettings['DialogLumensQUESHDominantHRU']['slopeMap'] = slopeMap = settings.value('slopeMap')
            templateSettings['DialogLumensQUESHDominantHRU']['subcatchmentMap'] = subcatchmentMap = settings.value('subcatchmentMap')
            templateSettings['DialogLumensQUESHDominantHRU']['landUseClassification'] = landUseClassification = settings.value('landUseClassification')
            templateSettings['DialogLumensQUESHDominantHRU']['soilClassification'] = soilClassification = settings.value('soilClassification')
            templateSettings['DialogLumensQUESHDominantHRU']['slopeClassification'] = slopeClassification = settings.value('slopeClassification')
            templateSettings['DialogLumensQUESHDominantHRU']['areaName'] = areaName = settings.value('areaName')
            templateSettings['DialogLumensQUESHDominantHRU']['period'] = period = settings.value('period')
            
            if not returnTemplateSettings:
                if landUseMap and os.path.exists(landUseMap):
                    self.lineEditHRULandUseMap.setText(landUseMap)
                else:
                    self.lineEditHRULandUseMap.setText('')
                if soilMap and os.path.exists(soilMap):
                    self.lineEditHRUSoilMap.setText(soilMap)
                else:
                    self.lineEditHRUSoilMap.setText('')
                if subcatchmentMap and os.path.exists(subcatchmentMap):
                    self.lineEditHRUSubcatchmentMap.setText(subcatchmentMap)
                else:
                    self.lineEditHRUSubcatchmentMap.setText('')
                if landUseClassification and os.path.exists(landUseClassification):
                    self.lineEditHRULandUseClassification.setText(landUseClassification)
                else:
                    self.lineEditHRULandUseClassification.setText('')
                if soilClassification and os.path.exists(soilClassification):
                    self.lineEditHRUSoilClassification.setText(soilClassification)
                else:
                    self.lineEditHRUSoilClassification.setText('')
                if slopeClassification and os.path.exists(slopeClassification):
                    self.lineEditHRUSlopeClassification.setText(slopeClassification)
                else:
                    self.lineEditHRUSlopeClassification.setText('')
                if areaName:
                    self.lineEditHRUAreaName.setText(areaName)
                else:
                    self.lineEditHRUAreaName.setText('')
                if period:
                    self.spinBoxHRUPeriod.setValue(int(period))
                else:
                    self.spinBoxHRUPeriod.setValue(td.year)
            
            settings.endGroup()
            # /dialog
            
            # NOTE: DialogLumensQUESHDominantLUSSL has same fields as DialogLumensQUESHDominantHRU
            
            # start dialog
            settings.beginGroup('DialogLumensQUESHMultipleHRU')
            
            templateSettings['DialogLumensQUESHMultipleHRU'] = {}
            templateSettings['DialogLumensQUESHMultipleHRU']['landUseThreshold'] = landUseThreshold = settings.value('landUseThreshold')
            templateSettings['DialogLumensQUESHMultipleHRU']['soilThreshold'] = soilThreshold = settings.value('soilThreshold')
            templateSettings['DialogLumensQUESHMultipleHRU']['slopeThreshold'] = slopeThreshold = settings.value('slopeThreshold')
            
            if not returnTemplateSettings:
                if landUseThreshold:
                    self.spinBoxMultipleHRULandUseThreshold.setValue(int(landUseThreshold))
                else:
                    self.spinBoxMultipleHRULandUseThreshold.setValue(0)
                if soilThreshold:
                    self.spinBoxMultipleHRUSoilThreshold.setValue(int(soilThreshold))
                else:
                    self.spinBoxMultipleHRUSoilThreshold.setValue(0)
                if slopeThreshold:
                    self.spinBoxMultipleHRUSlopeThreshold.setValue(int(slopeThreshold))
                else:
                    self.spinBoxMultipleHRUSlopeThreshold.setValue(0)
                
            if not returnTemplateSettings:
                self.currentHRUDefinitionTemplate = templateFile
                self.loadedHRUDefinitionTemplate.setText(templateFile)
                self.comboBoxHRUDefinitionTemplate.setCurrentIndex(self.comboBoxHRUDefinitionTemplate.findText(templateFile))
                self.buttonSaveHRUDefinitionTemplate.setEnabled(True)
            
            settings.endGroup()
            # /dialog
            
            settings.endGroup()
            # /tab
        elif tabName == 'Watershed Model Evaluation':
            dialogsToLoad = (
                'DialogLumensQUESHWatershedModelEvaluation',
            )
            
            # start tab
            settings.beginGroup(tabName)
            
            # 'Watershed Model Evaluation' tab widgets
            # start dialog
            settings.beginGroup('DialogLumensQUESHWatershedModelEvaluation')
            
            templateSettings['DialogLumensQUESHWatershedModelEvaluation'] = {}
            templateSettings['DialogLumensQUESHWatershedModelEvaluation']['dateInitial'] = dateInitial = settings.value('dateInitial')
            templateSettings['DialogLumensQUESHWatershedModelEvaluation']['dateFinal'] = dateFinal = settings.value('dateFinal')
            templateSettings['DialogLumensQUESHWatershedModelEvaluation']['SWATModel'] = SWATModel = settings.value('SWATModel')
            templateSettings['DialogLumensQUESHWatershedModelEvaluation']['location'] = location = settings.value('location')
            templateSettings['DialogLumensQUESHWatershedModelEvaluation']['outletReachSubBasinID'] = outletReachSubBasinID = settings.value('outletReachSubBasinID')
            templateSettings['DialogLumensQUESHWatershedModelEvaluation']['observedDebitFile'] = observedDebitFile = settings.value('observedDebitFile')
            templateSettings['DialogLumensQUESHWatershedModelEvaluation']['outputWatershedModelEvaluation'] = outputWatershedModelEvaluation = settings.value('outputWatershedModelEvaluation')
            
            if not returnTemplateSettings:
                if dateInitial:
                    self.dateWatershedModelEvaluationDateInitial.setDate(QtCore.QDate.fromString(dateInitial), 'dd/MM/yyyy')
                else:
                    self.dateWatershedModelEvaluationDateInitial.setDate(QtCore.QDate.currentDate())
                if dateFinal:
                    self.dateWatershedModelEvaluationDateFinal.setDate(QtCore.QDate.fromString(dateFinal), 'dd/MM/yyyy')
                else:
                    self.dateWatershedModelEvaluationDateFinal.setDate(QtCore.QDate.currentDate())
                if SWATModel:
                    self.comboBoxWatershedModelEvaluationSWATModel.setCurrentIndex(self.comboBoxWatershedModelEvaluationSWATModel.findData(int(SWATModel)))
                if location:
                    self.lineEditWatershedModelEvaluationLocation.setText(location)
                else:
                    self.lineEditWatershedModelEvaluationLocation.setText('')
                if outletReachSubBasinID:
                    self.spinBoxWatershedModelEvaluationOutletReachSubBasinID.setValue(int(outletReachSubBasinID))
                else:
                    self.spinBoxWatershedModelEvaluationOutletReachSubBasinID.setValue(10)
                if observedDebitFile and os.path.exists(observedDebitFile):
                    self.lineEditWatershedModelEvaluationObservedDebitFile.setText(observedDebitFile)
                else:
                    self.lineEditWatershedModelEvaluationObservedDebitFile.setText('')
                if outputWatershedModelEvaluation:
                    self.lineEditOutputWatershedModelEvaluation.setText(outputWatershedModelEvaluation)
                else:
                    self.lineEditOutputWatershedModelEvaluation.setText('')
                
                self.currentWatershedModelEvaluationTemplate = templateFile
                self.loadedWatershedModelEvaluationTemplate.setText(templateFile)
                self.comboBoxWatershedModelEvaluationTemplate.setCurrentIndex(self.comboBoxWatershedModelEvaluationTemplate.findText(templateFile))
                self.buttonSaveWatershedModelEvaluationTemplate.setEnabled(True)
            
            settings.endGroup()
            # /dialog
            
            settings.endGroup()
            # /tab
        elif tabName == 'Watershed Indicators':
            dialogsToLoad = (
                'DialogLumensQUESHWatershedIndicators',
            )
            
            # start tab
            settings.beginGroup(tabName)
            
            # 'Watershed Model Evaluation' tab widgets
            # start dialog
            settings.beginGroup('DialogLumensQUESHWatershedIndicators')
            
            templateSettings['DialogLumensQUESHWatershedIndicators'] = {}
            templateSettings['DialogLumensQUESHWatershedIndicators']['SWATTXTINOUTDir'] = SWATTXTINOUTDir = settings.value('SWATTXTINOUTDir')
            templateSettings['DialogLumensQUESHWatershedIndicators']['dateInitial'] = dateInitial = settings.value('dateInitial')
            templateSettings['DialogLumensQUESHWatershedIndicators']['dateFinal'] = dateFinal = settings.value('dateFinal')
            templateSettings['DialogLumensQUESHWatershedIndicators']['subWatershedPolygon'] = subWatershedPolygon = settings.value('subWatershedPolygon')
            templateSettings['DialogLumensQUESHWatershedIndicators']['location'] = location = settings.value('location')
            templateSettings['DialogLumensQUESHWatershedIndicators']['subWatershedOutput'] = subWatershedOutput = settings.value('subWatershedOutput')
            templateSettings['DialogLumensQUESHWatershedIndicators']['outputInitialYearSubWatershedLevelIndicators'] = outputInitialYearSubWatershedLevelIndicators = settings.value('outputInitialYearSubWatershedLevelIndicators')
            templateSettings['DialogLumensQUESHWatershedIndicators']['outputFinalYearSubWatershedLevelIndicators'] = outputFinalYearSubWatershedLevelIndicators = settings.value('outputFinalYearSubWatershedLevelIndicators')
            
            if not returnTemplateSettings:
                if SWATTXTINOUTDir and os.path.isdir(SWATTXTINOUTDir):
                    self.lineEditWatershedIndicatorsSWATTXTINOUTDir.setText(SWATTXTINOUTDir)
                else:
                    self.lineEditWatershedIndicatorsSWATTXTINOUTDir.setText('')
                if dateInitial:
                    self.dateWatershedIndicatorsDateInitial.setDate(QtCore.QDate.fromString(dateInitial), 'dd/MM/yyyy')
                else:
                    self.dateWatershedIndicatorsDateInitial.setDate(QtCore.QDate.currentDate())
                if dateFinal:
                    self.dateWatershedIndicatorsDateFinal.setDate(QtCore.QDate.fromString(dateFinal), 'dd/MM/yyyy')
                else:
                    self.dateWatershedIndicatorsDateFinal.setDate(QtCore.QDate.currentDate())
                if subWatershedPolygon and os.path.exists(subWatershedPolygon):
                    self.lineEditWatershedIndicatorsSubWatershedPolygon.setText(subWatershedPolygon)
                else:
                    self.lineEditWatershedIndicatorsSubWatershedPolygon.setText('')
                if location:
                    self.lineEditWatershedIndicatorsLocation.setText(location)
                else:
                    self.lineEditWatershedIndicatorsLocation.setText('')
                if subWatershedOutput:
                    self.spinBoxWatershedIndicatorsSubWatershedOutputsetValue(int(subWatershedOutput))
                else:
                    self.spinBoxWatershedIndicatorsSubWatershedOutputsetValue.setValue(10)
                if outputInitialYearSubWatershedLevelIndicators:
                    self.lineEditWatershedIndicatorsOutputInitialYearSubWatershedLevelIndicators.setText(outputInitialYearSubWatershedLevelIndicators)
                else:
                    self.lineEditWatershedIndicatorsOutputInitialYearSubWatershedLevelIndicators.setText('')
                if outputFinalYearSubWatershedLevelIndicators:
                    self.lineEditWatershedIndicatorsOutputFinalYearSubWatershedLevelIndicators.setText(outputFinalYearSubWatershedLevelIndicators)
                else:
                    self.lineEditWatershedIndicatorsOutputFinalYearSubWatershedLevelIndicators.setText('')
                
                self.currentWatershedIndicatorsTemplate = templateFile
                self.loadedWatershedIndicatorsTemplate.setText(templateFile)
                self.comboBoxWatershedIndicatorsTemplate.setCurrentIndex(self.comboBoxWatershedIndicatorsTemplate.findText(templateFile))
                self.buttonSaveWatershedIndicatorsTemplate.setEnabled(True)
            
            settings.endGroup()
            # /dialog
            
            settings.endGroup()
            # /tab
        
        if returnTemplateSettings:
            return templateSettings
        else:
            # Log to history log
            logging.getLogger(self.historyLog).info('Loaded configuration: %s', templateFile)
    
    
    def checkForDuplicateTemplates(self, tabName, templateToSkip):
        """Method for checking whether the new template values to be saved already exists in a saved template file.
        
        Args:
            tabName (str): the tab to be checked.
            templateToSkip (str): the template file to skip (when saving an existing template file).
        """
        duplicateTemplate = None
        templateFiles = [os.path.basename(name) for name in glob.glob(os.path.join(self.settingsPath, '*.ini')) if os.path.isfile(os.path.join(self.settingsPath, name))]
        dialogsToLoad = None
        
        if tabName == 'Pre-QUES':
            dialogsToLoad = (
                'DialogLumensPreQUESLandcoverTrajectoriesAnalysis',
            )
        elif tabName == 'QUES-C':
            dialogsToLoad = (
                'DialogLumensQUESCCarbonAccounting',
            )
        elif tabName == 'QUES-B':
            dialogsToLoad = (
                'DialogLumensQUESBAnalysis',
            )
        elif tabName == 'Hydrological Response Unit Definition':
            dialogsToLoad = (
                'DialogLumensQUESHDominantHRU',
                'DialogLumensQUESHDominantLUSSL',
                'DialogLumensQUESHMultipleHRU',
            )
        elif tabName == 'Watershed Model Evaluation':
            dialogsToLoad = (
                'DialogLumensQUESHWatershedModelEvaluation',
            )
        elif tabName == 'Watershed Indicators':
            dialogsToLoad = (
                'DialogLumensQUESHWatershedIndicators',
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
                'The configuration you are about to save matches an existing configuration.\nDo you want to load \'{0}\' instead?'.format(duplicateTemplate),
                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                QtGui.QMessageBox.No
            )
            
            if reply == QtGui.QMessageBox.Yes:
                if tabName == 'Pre-QUES':
                    self.handlerLoadPreQUESTemplate(duplicateTemplate)
                elif tabName == 'QUES-C':
                    self.handlerLoadQUESCTemplate(duplicateTemplate)
                elif tabName == 'QUES-B':
                    self.handlerLoadQUESBTemplate(duplicateTemplate)
                elif tabName == 'Hydrological Response Unit Definition':
                    self.handlerLoadHRUDefinitionTemplate(duplicateTemplate)
                elif tabName == 'Watershed Model Evaluation':
                    self.handlerLoadWatershedModelEvaluationTemplate(duplicateTemplate)
                elif tabName == 'Watershed Indicators':
                    self.handlerLoadWatershedIndicatorsTemplate(duplicateTemplate)
                
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
            templateFilePath = os.path.join(self.main.appSettings['DialogLumensOpenDatabase']['projectFolder'], self.main.appSettings['folderQUES'], fileName)
            settings = QtCore.QSettings(templateFilePath, QtCore.QSettings.IniFormat)
            settings.setFallbacksEnabled(True) # only use ini files
            
            dialogsToSave = None
            
            if tabName == 'Pre-QUES':
                dialogsToSave = (
                    'DialogLumensPreQUESLandcoverTrajectoriesAnalysis',
                )
            elif tabName == 'QUES-C':
                dialogsToSave = (
                    'DialogLumensQUESCCarbonAccounting',
                )
            elif tabName == 'QUES-B':
                dialogsToSave = (
                    'DialogLumensQUESBAnalysis',
                )
            elif tabName == 'Hydrological Response Unit Definition':
                dialogsToSave = (
                    'DialogLumensQUESHDominantHRU',
                    'DialogLumensQUESHDominantLUSSL',
                    'DialogLumensQUESHMultipleHRU',
                )
            elif tabName == 'Watershed Model Evaluation':
                dialogsToSave = (
                    'DialogLumensQUESHWatershedModelEvaluation',
                )
            elif tabName == 'Watershed Indicators':
                dialogsToSave = (
                    'DialogLumensQUESHWatershedIndicators',
                )
            
            settings.beginGroup(tabName)
            for dialog in dialogsToSave:
                settings.beginGroup(dialog)
                for key, val in self.main.appSettings[dialog].iteritems():
                    settings.setValue(key, val)
                settings.endGroup()
            settings.endGroup()
            
            # Log to history log
            logging.getLogger(self.historyLog).info('Saved configuration: %s', fileName)
    
    
    def __init__(self, parent):
        super(DialogLumensQUES, self).__init__(parent)
        
        self.main = parent
        self.dialogTitle = 'QUES'
        self.checkBoxQUESCDatabaseCount = 0
        self.listOfQUESCDatabase = []
        self.settingsPath = os.path.join(self.main.appSettings['DialogLumensOpenDatabase']['projectFolder'], self.main.appSettings['folderQUES'])
        self.currentPreQUESTemplate = None
        self.currentQUESCTemplate = None
        self.currentQUESBTemplate = None
        self.currentHRUDefinitionTemplate = None
        self.currentWatershedModelEvaluationTemplate = None
        self.currentWatershedIndicatorsTemplate = None
        
        # Init logging
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        if self.main.appSettings['debug']:
            print 'DEBUG: DialogLumensQUES init'
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
        
        # 'Pre-QUES' tab buttons
        self.buttonProcessPreQUES.clicked.connect(self.handlerProcessPreQUES)
        self.buttonHelpPreQUES.clicked.connect(lambda:self.handlerDialogHelp('QUES'))
        self.buttonLoadPreQUESTemplate.clicked.connect(self.handlerLoadPreQUESTemplate)
        self.buttonSavePreQUESTemplate.clicked.connect(self.handlerSavePreQUESTemplate)
        self.buttonSaveAsPreQUESTemplate.clicked.connect(self.handlerSaveAsPreQUESTemplate)
        
        # 'QUES-C' tab checkboxes
        self.checkBoxCarbonAccounting.toggled.connect(self.toggleCarbonAccounting)
        self.checkBoxPeatlandCarbonAccounting.toggled.connect(self.togglePeatlandCarbonAccounting)
        self.checkBoxSummarizeMultiplePeriod.toggled.connect(self.toggleSummarizeMultiplePeriod)
        
        # 'QUES-C' tab buttons
        self.buttonProcessQUESC.clicked.connect(self.handlerProcessQUESC)
        self.buttonHelpQUESC.clicked.connect(lambda:self.handlerDialogHelp('QUES'))
        self.buttonLoadQUESCTemplate.clicked.connect(self.handlerLoadQUESCTemplate)
        self.buttonSaveQUESCTemplate.clicked.connect(self.handlerSaveQUESCTemplate)
        self.buttonSaveAsQUESCTemplate.clicked.connect(self.handlerSaveAsQUESCTemplate)
        
        # 'QUES-B' tab buttons
        self.buttonLoadLookupTableHabitat.clicked.connect(self.handlerLoadHabitatLookupTable)
        self.buttonProcessQUESB.clicked.connect(self.handlerProcessQUESB)
        self.buttonHelpQUESB.clicked.connect(lambda:self.handlerDialogHelp('QUES'))
        self.buttonLoadQUESBTemplate.clicked.connect(self.handlerLoadQUESBTemplate)
        self.buttonSaveQUESBTemplate.clicked.connect(self.handlerSaveQUESBTemplate)
        self.buttonSaveAsQUESBTemplate.clicked.connect(self.handlerSaveAsQUESBTemplate)
        
        # 'QUES-H' tab checkboxes
        self.checkBoxMultipleHRU.toggled.connect(self.toggleMultipleHRU)
        
        # 'QUES-H' HRU tab buttons
        self.buttonSelectHRULandUseMap.clicked.connect(self.handlerSelectHRULandUseMap)
        self.buttonSelectHRUSoilMap.clicked.connect(self.handlerSelectHRUSoilMap)
        self.buttonSelectHRUSlopeMap.clicked.connect(self.handlerSelectHRUSlopeMap)
        self.buttonSelectHRUSubcatchmentMap.clicked.connect(self.handlerSelectHRUSubcatchmentMap)
        self.buttonSelectHRULandUseClassification.clicked.connect(self.handlerSelectHRULandUseClassification)
        self.buttonSelectHRUSoilClassification.clicked.connect(self.handlerSelectHRUSoilClassification)
        self.buttonSelectHRUSlopeClassification.clicked.connect(self.handlerSelectHRUSlopeClassification)
        self.buttonProcessHRUDefinition.clicked.connect(self.handlerProcessQUESHHRUDefinition)
        self.buttonHelpQUESHHRUDefinition.clicked.connect(lambda:self.handlerDialogHelp('QUES'))
        self.buttonLoadHRUDefinitionTemplate.clicked.connect(self.handlerLoadHRUDefinitionTemplate)
        self.buttonSaveHRUDefinitionTemplate.clicked.connect(self.handlerSaveHRUDefinitionTemplate)
        self.buttonSaveAsHRUDefinitionTemplate.clicked.connect(self.handlerSaveAsHRUDefinitionTemplate)
        
        # 'QUES-H' Watershed Model Evaluation tab buttons
        self.buttonSelectWatershedModelEvaluationObservedDebitFile.clicked.connect(self.handlerSelectWatershedModelEvaluationObservedDebitFile)
        self.buttonSelectOutputWatershedModelEvaluation.clicked.connect(self.handlerSelectOutputWatershedModelEvaluation)
        self.buttonProcessWatershedModelEvaluation.clicked.connect(self.handlerProcessQUESHWatershedModelEvaluation)
        self.buttonHelpQUESHWatershedModelEvaluation.clicked.connect(lambda:self.handlerDialogHelp('QUES'))
        self.buttonLoadWatershedModelEvaluationTemplate.clicked.connect(self.handlerLoadWatershedModelEvaluationTemplate)
        self.buttonSaveWatershedModelEvaluationTemplate.clicked.connect(self.handlerSaveWatershedModelEvaluationTemplate)
        self.buttonSaveAsWatershedModelEvaluationTemplate.clicked.connect(self.handlerSaveAsWatershedModelEvaluationTemplate)
        
        # 'QUES-H' Watershed Indicators tab buttons
        self.buttonSelectWatershedIndicatorsSWATTXTINOUTDir.clicked.connect(self.handlerSelectWatershedIndicatorsSWATTXTINOUTDir)
        self.buttonSelectWatershedIndicatorsSubWatershedPolygon.clicked.connect(self.handlerSelectWatershedIndicatorsSubWatershedPolygon)
        self.buttonSelectWatershedIndicatorsOutputInitialYearSubWatershedLevelIndicators.clicked.connect(self.handlerSelectWatershedIndicatorsOutputInitialYearSubWatershedLevelIndicators)
        self.buttonSelectWatershedIndicatorsOutputFinalYearSubWatershedLevelIndicators.clicked.connect(self.handlerSelectWatershedIndicatorsOutputFinalYearSubWatershedLevelIndicators)
        self.buttonProcessWatershedIndicators.clicked.connect(self.handlerProcessQUESHWatershedIndicators)
        self.buttonHelpQUESHWatershedIndicators.clicked.connect(lambda:self.handlerDialogHelp('QUES'))
        self.buttonLoadWatershedIndicatorsTemplate.clicked.connect(self.handlerLoadWatershedIndicatorsTemplate)
        self.buttonSaveWatershedIndicatorsTemplate.clicked.connect(self.handlerSaveWatershedIndicatorsTemplate)
        self.buttonSaveAsWatershedIndicatorsTemplate.clicked.connect(self.handlerSaveAsWatershedIndicatorsTemplate)
        
    
    def setupUi(self, parent):
        """Method for building the dialog UI.
        
        Args:
            parent: the dialog's parent instance.
        """
        self.setStyleSheet('QDialog { background-color: rgb(225, 229, 237); } QMessageBox QLabel { color: #fff; }')
        self.dialogLayout = QtGui.QVBoxLayout()

        self.groupBoxQUESDialog = QtGui.QGroupBox('Quantification of Environmental Services')
        self.layoutGroupBoxQUESDialog = QtGui.QVBoxLayout()
        self.layoutGroupBoxQUESDialog.setAlignment(QtCore.Qt.AlignTop)
        self.groupBoxQUESDialog.setLayout(self.layoutGroupBoxQUESDialog)
        self.labelQUESDialogInfo = QtGui.QLabel()
        self.labelQUESDialogInfo.setText('\n')
        self.labelQUESDialogInfo.setWordWrap(True)
        self.layoutGroupBoxQUESDialog.addWidget(self.labelQUESDialogInfo)

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
        
        self.tabPreQUES = QtGui.QWidget()
        self.tabQUESC = QtGui.QWidget()
        self.tabQUESB = QtGui.QWidget()
        self.tabQUESH = QtGui.QWidget()
        self.tabReclassification = QtGui.QWidget()
        self.tabLog = QtGui.QWidget()
        
        self.tabWidget.addTab(self.tabPreQUES, 'Pre-QUES')
        self.tabWidget.addTab(self.tabQUESC, 'QUES-C')
        self.tabWidget.addTab(self.tabQUESB, 'QUES-B')
        self.tabWidget.addTab(self.tabQUESH, 'QUES-H')
        ##self.tabWidget.addTab(self.tabReclassification, 'Reclassification')
        self.tabWidget.addTab(self.tabLog, 'Log')
        
        ##self.layoutTabPreQUES = QtGui.QVBoxLayout()
        self.layoutTabPreQUES = QtGui.QGridLayout()
        ##self.layoutTabQUESC = QtGui.QVBoxLayout()
        self.layoutTabQUESC = QtGui.QGridLayout()
        ##self.layoutTabQUESB = QtGui.QVBoxLayout()
        self.layoutTabQUESB = QtGui.QGridLayout()
        self.layoutTabQUESH = QtGui.QVBoxLayout()
        self.layoutTabReclassification = QtGui.QVBoxLayout()
        self.layoutTabLog = QtGui.QVBoxLayout()
        
        self.tabPreQUES.setLayout(self.layoutTabPreQUES)
        self.tabQUESC.setLayout(self.layoutTabQUESC)
        self.tabQUESB.setLayout(self.layoutTabQUESB)
        self.tabQUESH.setLayout(self.layoutTabQUESH)
        self.tabReclassification.setLayout(self.layoutTabReclassification)
        self.tabLog.setLayout(self.layoutTabLog)

        self.dialogLayout.addWidget(self.groupBoxQUESDialog)
        self.dialogLayout.addWidget(self.tabWidget)
        
        #***********************************************************
        # Setup 'Pre-QUES' tab
        #***********************************************************
        # 'Land cover' GroupBox
        self.groupBoxLandCover = QtGui.QGroupBox('Parameterization')
        self.layoutGroupBoxLandCover = QtGui.QVBoxLayout()
        self.layoutGroupBoxLandCover.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLandCover.setLayout(self.layoutGroupBoxLandCover)
        
        self.layoutLandCoverInfo = QtGui.QVBoxLayout()
        self.labelLandCoverInfo = QtGui.QLabel()
        self.labelLandCoverInfo.setText('\n')
        self.labelLandCoverInfo.setWordWrap(True)
        self.layoutLandCoverInfo.addWidget(self.labelLandCoverInfo)
        
        self.layoutLandCoverOptions = QtGui.QGridLayout()
        self.layoutLandCoverOptions.setContentsMargins(0, 0, 0, 0)
        
        self.labelPreQUESLandCoverLandUse1 = QtGui.QLabel()
        self.labelPreQUESLandCoverLandUse1.setText('Earlier land use/cover:')
        self.layoutLandCoverOptions.addWidget(self.labelPreQUESLandCoverLandUse1, 0, 0)
        
        self.comboBoxPreQUESLandCoverLandUse1 = QtGui.QComboBox()
        self.comboBoxPreQUESLandCoverLandUse1.setDisabled(True)
        self.layoutLandCoverOptions.addWidget(self.comboBoxPreQUESLandCoverLandUse1, 0, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataLandUseCover, self.comboBoxPreQUESLandCoverLandUse1)
        
        self.labelPreQUESLandCoverLandUse2 = QtGui.QLabel()
        self.labelPreQUESLandCoverLandUse2.setText('Later land use/cover:')
        self.layoutLandCoverOptions.addWidget(self.labelPreQUESLandCoverLandUse2, 1, 0)
        
        self.comboBoxPreQUESLandCoverLandUse2 = QtGui.QComboBox()
        self.comboBoxPreQUESLandCoverLandUse2.setDisabled(True)
        self.layoutLandCoverOptions.addWidget(self.comboBoxPreQUESLandCoverLandUse2, 1, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataLandUseCover, self.comboBoxPreQUESLandCoverLandUse2)
        
        self.labelPreQUESLandCoverPlanningUnit = QtGui.QLabel()
        self.labelPreQUESLandCoverPlanningUnit.setText('Planning unit:')
        self.layoutLandCoverOptions.addWidget(self.labelPreQUESLandCoverPlanningUnit, 2, 0)
        
        self.comboBoxPreQUESLandCoverPlanningUnit = QtGui.QComboBox()
        self.comboBoxPreQUESLandCoverPlanningUnit.setDisabled(True)
        self.layoutLandCoverOptions.addWidget(self.comboBoxPreQUESLandCoverPlanningUnit, 2, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataPlanningUnit, self.comboBoxPreQUESLandCoverPlanningUnit)        
        
        self.labelPreQUESLandCoverTable = QtGui.QLabel()
        self.labelPreQUESLandCoverTable.setText('Land use/cover lookup table:')
        self.layoutLandCoverOptions.addWidget(self.labelPreQUESLandCoverTable, 3, 0)
        
        self.comboBoxPreQUESLandCoverTable = QtGui.QComboBox()
        self.comboBoxPreQUESLandCoverTable.setDisabled(True)
        self.layoutLandCoverOptions.addWidget(self.comboBoxPreQUESLandCoverTable, 3, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxPreQUESLandCoverTable) 
        
        self.labelLandCoverAnalysisOption = QtGui.QLabel()
        self.labelLandCoverAnalysisOption.setText('Analysis option:')
        self.layoutLandCoverOptions.addWidget(self.labelLandCoverAnalysisOption, 4, 0)
        
        analysisOptions = [
            'All analysis',
            'Dominant land use change',
            'Land use change dynamics',
            'Land use change trajectory',
        ]
        self.comboBoxLandCoverAnalysisOption = QtGui.QComboBox()
        self.comboBoxLandCoverAnalysisOption.addItems(analysisOptions)
        self.layoutLandCoverOptions.addWidget(self.comboBoxLandCoverAnalysisOption, 4, 1)
        
        self.labelPreQUESNodata = QtGui.QLabel()
        self.labelPreQUESNodata.setText('&No data value:')
        self.layoutLandCoverOptions.addWidget(self.labelPreQUESNodata, 5, 0)
        
        self.spinBoxPreQUESNodata = QtGui.QSpinBox()
        self.spinBoxPreQUESNodata.setRange(-9999, 9999)
        self.spinBoxPreQUESNodata.setValue(0)
        self.layoutLandCoverOptions.addWidget(self.spinBoxPreQUESNodata, 5, 1)
        self.labelPreQUESNodata.setBuddy(self.spinBoxPreQUESNodata)
        
        self.layoutGroupBoxLandCover.addLayout(self.layoutLandCoverInfo)
        self.layoutGroupBoxLandCover.addLayout(self.layoutLandCoverOptions)
        
        # Process tab button
        self.layoutButtonPreQUES = QtGui.QHBoxLayout()
        self.buttonProcessPreQUES = QtGui.QPushButton()
        self.buttonProcessPreQUES.setText('&Process')
        icon = QtGui.QIcon(':/ui/icons/iconActionHelp.png')
        self.buttonHelpPreQUES = QtGui.QPushButton()
        self.buttonHelpPreQUES.setIcon(icon)
        self.layoutButtonPreQUES.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonPreQUES.addWidget(self.buttonProcessPreQUES)
        self.layoutButtonPreQUES.addWidget(self.buttonHelpPreQUES)
        
        # Template GroupBox
        self.groupBoxPreQUESTemplate = QtGui.QGroupBox('Configuration')
        self.layoutGroupBoxPreQUESTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxPreQUESTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxPreQUESTemplate.setLayout(self.layoutGroupBoxPreQUESTemplate)
        self.layoutPreQUESTemplateInfo = QtGui.QVBoxLayout()
        self.layoutPreQUESTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxPreQUESTemplate.addLayout(self.layoutPreQUESTemplateInfo)
        self.layoutGroupBoxPreQUESTemplate.addLayout(self.layoutPreQUESTemplate)
        
        self.labelLoadedPreQUESTemplate = QtGui.QLabel()
        self.labelLoadedPreQUESTemplate.setText('Loaded configuration:')
        self.layoutPreQUESTemplate.addWidget(self.labelLoadedPreQUESTemplate, 0, 0)
        
        self.loadedPreQUESTemplate = QtGui.QLabel()
        self.loadedPreQUESTemplate.setText('<None>')
        self.layoutPreQUESTemplate.addWidget(self.loadedPreQUESTemplate, 0, 1)
        
        self.labelPreQUESTemplate = QtGui.QLabel()
        self.labelPreQUESTemplate.setText('Name:')
        self.layoutPreQUESTemplate.addWidget(self.labelPreQUESTemplate, 1, 0)
        
        self.comboBoxPreQUESTemplate = QtGui.QComboBox()
        self.comboBoxPreQUESTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxPreQUESTemplate.setDisabled(True)
        self.comboBoxPreQUESTemplate.addItem('No configuration found')
        self.layoutPreQUESTemplate.addWidget(self.comboBoxPreQUESTemplate, 1, 1)
        
        self.layoutButtonPreQUESTemplate = QtGui.QHBoxLayout()
        self.layoutButtonPreQUESTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadPreQUESTemplate = QtGui.QPushButton()
        self.buttonLoadPreQUESTemplate.setDisabled(True)
        self.buttonLoadPreQUESTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadPreQUESTemplate.setText('Load')
        self.buttonSavePreQUESTemplate = QtGui.QPushButton()
        self.buttonSavePreQUESTemplate.setDisabled(True)
        self.buttonSavePreQUESTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSavePreQUESTemplate.setText('Save')
        self.buttonSaveAsPreQUESTemplate = QtGui.QPushButton()
        self.buttonSaveAsPreQUESTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsPreQUESTemplate.setText('Save As')
        self.layoutButtonPreQUESTemplate.addWidget(self.buttonLoadPreQUESTemplate)
        self.layoutButtonPreQUESTemplate.addWidget(self.buttonSavePreQUESTemplate)
        self.layoutButtonPreQUESTemplate.addWidget(self.buttonSaveAsPreQUESTemplate)
        self.layoutGroupBoxPreQUESTemplate.addLayout(self.layoutButtonPreQUESTemplate)
        
        # Place the GroupBoxes
        self.layoutTabPreQUES.addWidget(self.groupBoxLandCover, 0, 0)
        self.layoutTabPreQUES.addLayout(self.layoutButtonPreQUES, 1, 0, 1, 2, QtCore.Qt.AlignRight)
        self.layoutTabPreQUES.addWidget(self.groupBoxPreQUESTemplate, 0, 1, 1, 1)
        self.layoutTabPreQUES.setColumnStretch(0, 3)
        self.layoutTabPreQUES.setColumnStretch(1, 1) # Smaller template column
        
        #***********************************************************
        # Setup 'QUES-C' tab
        #***********************************************************
        # 'Carbon accounting' GroupBox
        self.groupBoxCarbonAccounting = QtGui.QGroupBox('Carbon accounting')
        self.layoutGroupBoxCarbonAccounting = QtGui.QHBoxLayout()
        self.groupBoxCarbonAccounting.setLayout(self.layoutGroupBoxCarbonAccounting)
        self.layoutOptionsCarbonAccounting = QtGui.QVBoxLayout()
        self.layoutOptionsCarbonAccounting.setContentsMargins(5, 0, 5, 0)
        self.contentOptionsCarbonAccounting = QtGui.QWidget()
        self.contentOptionsCarbonAccounting.setLayout(self.layoutOptionsCarbonAccounting)
        self.layoutOptionsCarbonAccounting.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.checkBoxCarbonAccounting = QtGui.QCheckBox()
        self.checkBoxCarbonAccounting.setChecked(False)
        self.contentOptionsCarbonAccounting.setDisabled(True)
        self.layoutGroupBoxCarbonAccounting.addWidget(self.checkBoxCarbonAccounting)
        self.layoutGroupBoxCarbonAccounting.addWidget(self.contentOptionsCarbonAccounting)
        self.layoutGroupBoxCarbonAccounting.insertStretch(2,1)
        self.layoutGroupBoxCarbonAccounting.setAlignment(self.checkBoxCarbonAccounting, QtCore.Qt.AlignTop)
        self.layoutCarbonAccountingInfo = QtGui.QVBoxLayout()
        self.layoutCarbonAccounting = QtGui.QGridLayout()
        self.layoutOptionsCarbonAccounting.addLayout(self.layoutCarbonAccountingInfo)
        self.layoutOptionsCarbonAccounting.addLayout(self.layoutCarbonAccounting)
        
        self.labelCarbonAccountingInfo = QtGui.QLabel()
        self.labelCarbonAccountingInfo.setText('Emission from land use change\n')
        self.labelCarbonAccountingInfo.setWordWrap(True)
        self.layoutCarbonAccountingInfo.addWidget(self.labelCarbonAccountingInfo)

        self.labelCALandCoverLandUse1 = QtGui.QLabel()
        self.labelCALandCoverLandUse1.setText('Earlier land use/cover:')
        self.layoutCarbonAccounting.addWidget(self.labelCALandCoverLandUse1, 0, 0)
        
        self.comboBoxCALandCoverLandUse1 = QtGui.QComboBox()
        self.comboBoxCALandCoverLandUse1.setDisabled(True)
        self.layoutCarbonAccounting.addWidget(self.comboBoxCALandCoverLandUse1, 0, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataLandUseCover, self.comboBoxCALandCoverLandUse1)
        
        self.labelCALandCoverLandUse2 = QtGui.QLabel()
        self.labelCALandCoverLandUse2.setText('Later land use/cover:')
        self.layoutCarbonAccounting.addWidget(self.labelCALandCoverLandUse2, 1, 0)
        
        self.comboBoxCALandCoverLandUse2 = QtGui.QComboBox()
        self.comboBoxCALandCoverLandUse2.setDisabled(True)
        self.layoutCarbonAccounting.addWidget(self.comboBoxCALandCoverLandUse2, 1, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataLandUseCover, self.comboBoxCALandCoverLandUse2)
        
        self.labelCALandCoverPlanningUnit = QtGui.QLabel()
        self.labelCALandCoverPlanningUnit.setText('Planning unit:')
        self.layoutCarbonAccounting.addWidget(self.labelCALandCoverPlanningUnit, 2, 0)
        
        self.comboBoxCALandCoverPlanningUnit = QtGui.QComboBox()
        self.comboBoxCALandCoverPlanningUnit.setDisabled(True)
        self.layoutCarbonAccounting.addWidget(self.comboBoxCALandCoverPlanningUnit, 2, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataPlanningUnit, self.comboBoxCALandCoverPlanningUnit)        
        
        self.labelCACarbonTable = QtGui.QLabel()
        self.labelCACarbonTable.setText('Carbon stock lookup table:')
        self.layoutCarbonAccounting.addWidget(self.labelCACarbonTable, 3, 0)
        
        self.comboBoxCACarbonTable = QtGui.QComboBox()
        self.comboBoxCACarbonTable.setDisabled(True)
        self.layoutCarbonAccounting.addWidget(self.comboBoxCACarbonTable, 3, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxCACarbonTable) 
        
        self.labelCANoDataValue = QtGui.QLabel()
        self.labelCANoDataValue.setText('&No data value:')
        self.layoutCarbonAccounting.addWidget(self.labelCANoDataValue, 4, 0)
        
        self.spinBoxCANoDataValue = QtGui.QSpinBox()
        self.spinBoxCANoDataValue.setRange(-9999, 9999)
        self.spinBoxCANoDataValue.setValue(0)
        self.layoutCarbonAccounting.addWidget(self.spinBoxCANoDataValue, 4, 1)
        self.labelCANoDataValue.setBuddy(self.spinBoxCANoDataValue)
        
        # Peatland carbon accounting
        self.labelSpace = QtGui.QLabel()
        self.labelSpace.setText(' ')
        self.layoutCarbonAccounting.addWidget(self.labelSpace, 5, 0)
        
        self.labelcheckBoxPeatlandCarbonAccounting = QtGui.QLabel()
        self.labelcheckBoxPeatlandCarbonAccounting.setText('Include peat emission:')
        self.layoutCarbonAccounting.addWidget(self.labelcheckBoxPeatlandCarbonAccounting, 6, 0)
        
        self.checkBoxPeatlandCarbonAccounting = QtGui.QCheckBox()
        self.checkBoxPeatlandCarbonAccounting.setChecked(False)
        self.layoutCarbonAccounting.addWidget(self.checkBoxPeatlandCarbonAccounting, 6, 1)
        
        self.labelPeatlandMap = QtGui.QLabel()
        self.labelPeatlandMap.setText('Peat map:')
        self.layoutCarbonAccounting.addWidget(self.labelPeatlandMap, 7, 0)
        
        self.comboBoxPeatlandMap = QtGui.QComboBox()
        self.comboBoxPeatlandMap.setDisabled(True)
        self.layoutCarbonAccounting.addWidget(self.comboBoxPeatlandMap, 7, 1)
        
        self.labelPCACsvfile = QtGui.QLabel()
        self.labelPCACsvfile.setText('Peat emission lookup table:')
        self.layoutCarbonAccounting.addWidget(self.labelPCACsvfile, 8, 0)
        
        self.comboBoxPCACsvfile = QtGui.QComboBox()
        self.comboBoxPCACsvfile.setDisabled(True)
        self.layoutCarbonAccounting.addWidget(self.comboBoxPCACsvfile, 8, 1)
        
        # 'Summarize multiple period' GroupBox
        self.groupBoxSummarizeMultiplePeriod = QtGui.QGroupBox('Summarize multiple period')
        self.layoutGroupBoxSummarizeMultiplePeriod = QtGui.QHBoxLayout()
        self.groupBoxSummarizeMultiplePeriod.setLayout(self.layoutGroupBoxSummarizeMultiplePeriod)
        self.layoutOptionsSummarizeMultiplePeriod = QtGui.QVBoxLayout()
        self.layoutOptionsSummarizeMultiplePeriod.setContentsMargins(5, 0, 5, 0)
        self.contentOptionsSummarizeMultiplePeriod = QtGui.QWidget()
        self.contentOptionsSummarizeMultiplePeriod.setLayout(self.layoutOptionsSummarizeMultiplePeriod)
        self.layoutOptionsSummarizeMultiplePeriod.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.checkBoxSummarizeMultiplePeriod = QtGui.QCheckBox()
        self.checkBoxSummarizeMultiplePeriod.setChecked(False)
        self.contentOptionsSummarizeMultiplePeriod.setDisabled(True)
        self.layoutGroupBoxSummarizeMultiplePeriod.addWidget(self.checkBoxSummarizeMultiplePeriod)
        self.layoutGroupBoxSummarizeMultiplePeriod.addWidget(self.contentOptionsSummarizeMultiplePeriod)
        self.layoutGroupBoxSummarizeMultiplePeriod.insertStretch(2, 1)
        self.layoutGroupBoxSummarizeMultiplePeriod.setAlignment(self.checkBoxSummarizeMultiplePeriod, QtCore.Qt.AlignTop)
        self.layoutSummarizeMultiplePeriodInfo = QtGui.QVBoxLayout()
        self.layoutSummarizeMultiplePeriod = QtGui.QGridLayout()
        self.layoutOptionsSummarizeMultiplePeriod.addLayout(self.layoutSummarizeMultiplePeriodInfo)
        self.layoutOptionsSummarizeMultiplePeriod.addLayout(self.layoutSummarizeMultiplePeriod)
        
        self.labelSummarizeMultiplePeriodInfo = QtGui.QLabel()
        self.labelSummarizeMultiplePeriodInfo.setText('Calculate emission from multiple QUES-C database\n')
        self.labelSummarizeMultiplePeriodInfo.setWordWrap(True)
        self.layoutSummarizeMultiplePeriodInfo.addWidget(self.labelSummarizeMultiplePeriodInfo)
        
        self.populateQUESCDatabase()
        
        # Process tab button
        self.layoutButtonQUESC = QtGui.QHBoxLayout()
        self.buttonProcessQUESC = QtGui.QPushButton()
        self.buttonProcessQUESC.setText('&Process')
        self.buttonHelpQUESC = QtGui.QPushButton()
        self.buttonHelpQUESC.setIcon(icon)
        self.layoutButtonQUESC.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonQUESC.addWidget(self.buttonProcessQUESC)
        self.layoutButtonQUESC.addWidget(self.buttonHelpQUESC)
        
        # Template GroupBox
        self.groupBoxQUESCTemplate = QtGui.QGroupBox('Configuration')
        self.layoutGroupBoxQUESCTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxQUESCTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxQUESCTemplate.setLayout(self.layoutGroupBoxQUESCTemplate)
        self.layoutQUESCTemplateInfo = QtGui.QVBoxLayout()
        self.layoutQUESCTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxQUESCTemplate.addLayout(self.layoutQUESCTemplateInfo)
        self.layoutGroupBoxQUESCTemplate.addLayout(self.layoutQUESCTemplate)
        
        self.labelLoadedQUESCTemplate = QtGui.QLabel()
        self.labelLoadedQUESCTemplate.setText('Loaded configuration:')
        self.layoutQUESCTemplate.addWidget(self.labelLoadedQUESCTemplate, 0, 0)
        
        self.loadedQUESCTemplate = QtGui.QLabel()
        self.loadedQUESCTemplate.setText('<None>')
        self.layoutQUESCTemplate.addWidget(self.loadedQUESCTemplate, 0, 1)
        
        self.labelQUESCTemplate = QtGui.QLabel()
        self.labelQUESCTemplate.setText('Name:')
        self.layoutQUESCTemplate.addWidget(self.labelQUESCTemplate, 1, 0)
        
        self.comboBoxQUESCTemplate = QtGui.QComboBox()
        self.comboBoxQUESCTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxQUESCTemplate.setDisabled(True)
        self.comboBoxQUESCTemplate.addItem('No configuration found')
        self.layoutQUESCTemplate.addWidget(self.comboBoxQUESCTemplate, 1, 1)
        
        self.layoutButtonQUESCTemplate = QtGui.QHBoxLayout()
        self.layoutButtonQUESCTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadQUESCTemplate = QtGui.QPushButton()
        self.buttonLoadQUESCTemplate.setDisabled(True)
        self.buttonLoadQUESCTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadQUESCTemplate.setText('Load')
        self.buttonSaveQUESCTemplate = QtGui.QPushButton()
        self.buttonSaveQUESCTemplate.setDisabled(True)
        self.buttonSaveQUESCTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveQUESCTemplate.setText('Save')
        self.buttonSaveAsQUESCTemplate = QtGui.QPushButton()
        self.buttonSaveAsQUESCTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsQUESCTemplate.setText('Save As')
        self.layoutButtonQUESCTemplate.addWidget(self.buttonLoadQUESCTemplate)
        self.layoutButtonQUESCTemplate.addWidget(self.buttonSaveQUESCTemplate)
        self.layoutButtonQUESCTemplate.addWidget(self.buttonSaveAsQUESCTemplate)
        self.layoutGroupBoxQUESCTemplate.addLayout(self.layoutButtonQUESCTemplate)
        
        # Place the GroupBoxes
        self.layoutTabQUESC.addWidget(self.groupBoxCarbonAccounting, 0, 0)
        self.layoutTabQUESC.addWidget(self.groupBoxSummarizeMultiplePeriod, 1, 0)
        self.layoutTabQUESC.addLayout(self.layoutButtonQUESC, 2, 0, 1, 2, QtCore.Qt.AlignRight)
        self.layoutTabQUESC.addWidget(self.groupBoxQUESCTemplate, 0, 1, 2, 1)
        self.layoutTabQUESC.setColumnStretch(0, 3)
        self.layoutTabQUESC.setColumnStretch(1, 1) # Smaller template column
        
        #***********************************************************
        # Setup 'QUES-B' tab
        #***********************************************************
        # 'Parameters' GroupBox
        self.groupBoxQUESBParameters = QtGui.QGroupBox('Parameterization')
        self.layoutGroupBoxQUESBParameters = QtGui.QVBoxLayout()
        self.layoutGroupBoxQUESBParameters.setAlignment(QtCore.Qt.AlignTop)
        self.groupBoxQUESBParameters.setLayout(self.layoutGroupBoxQUESBParameters)
        self.layoutQUESBParametersInfo = QtGui.QVBoxLayout()
        self.layoutQUESBParameters = QtGui.QGridLayout()
        self.layoutGroupBoxQUESBParameters.addLayout(self.layoutQUESBParametersInfo)
        self.layoutGroupBoxQUESBParameters.addLayout(self.layoutQUESBParameters)
        
        self.labelQUESBParametersInfo = QtGui.QLabel()
        self.labelQUESBParametersInfo.setText('\n')
        self.labelQUESBParametersInfo.setWordWrap(True)
        self.layoutQUESBParametersInfo.addWidget(self.labelQUESBParametersInfo)

        self.labelQUESBLandCoverLandUse1 = QtGui.QLabel()
        self.labelQUESBLandCoverLandUse1.setText('Earlier land use/cover:')
        self.layoutQUESBParameters.addWidget(self.labelQUESBLandCoverLandUse1, 0, 0)

        self.comboBoxQUESBLandCoverLandUse1 = QtGui.QComboBox()
        self.comboBoxQUESBLandCoverLandUse1.setDisabled(True)
        self.layoutQUESBParameters.addWidget(self.comboBoxQUESBLandCoverLandUse1, 0, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataLandUseCover, self.comboBoxQUESBLandCoverLandUse1)

        self.labelQUESBLandCoverLandUse2 = QtGui.QLabel()
        self.labelQUESBLandCoverLandUse2.setText('Later land use/cover:')
        self.layoutQUESBParameters.addWidget(self.labelQUESBLandCoverLandUse2, 1, 0)

        self.comboBoxQUESBLandCoverLandUse2 = QtGui.QComboBox()
        self.comboBoxQUESBLandCoverLandUse2.setDisabled(True)
        self.layoutQUESBParameters.addWidget(self.comboBoxQUESBLandCoverLandUse2, 1, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataLandUseCover, self.comboBoxQUESBLandCoverLandUse2)

        self.labelQUESBLandCoverLandUse3 = QtGui.QLabel()
        self.labelQUESBLandCoverLandUse3.setText('Intact focal area:')
        self.layoutQUESBParameters.addWidget(self.labelQUESBLandCoverLandUse3, 2, 0)

        self.comboBoxQUESBLandCoverLandUse3 = QtGui.QComboBox()
        self.comboBoxQUESBLandCoverLandUse3.setDisabled(True)
        self.layoutQUESBParameters.addWidget(self.comboBoxQUESBLandCoverLandUse3, 2, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataLandUseCover, self.comboBoxQUESBLandCoverLandUse3)

        self.labelQUESBPlanningUnit = QtGui.QLabel()
        self.labelQUESBPlanningUnit.setText('Planning unit:')
        self.layoutQUESBParameters.addWidget(self.labelQUESBPlanningUnit, 3, 0)
        
        self.comboBoxQUESBPlanningUnit = QtGui.QComboBox()
        self.comboBoxQUESBPlanningUnit.setDisabled(True)
        self.layoutQUESBParameters.addWidget(self.comboBoxQUESBPlanningUnit, 3, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataPlanningUnit, self.comboBoxQUESBPlanningUnit)
        
        self.labelQUESBNodata = QtGui.QLabel()
        self.labelQUESBNodata.setText('No data value:')
        self.layoutQUESBParameters.addWidget(self.labelQUESBNodata, 4, 0)
        
        self.spinBoxQUESBNodata = QtGui.QSpinBox()
        self.spinBoxQUESBNodata.setRange(0, 999)
        self.spinBoxQUESBNodata.setValue(0)
        self.layoutQUESBParameters.addWidget(self.spinBoxQUESBNodata, 4, 1)
        
        self.labelQUESBEdgeContrast = QtGui.QLabel()
        self.labelQUESBEdgeContrast.setText('Edge contrast weight:')
        self.layoutQUESBParameters.addWidget(self.labelQUESBEdgeContrast, 5, 0)        
        
        self.comboBoxQUESBEdgeContrast = QtGui.QComboBox()
        self.comboBoxQUESBEdgeContrast.setDisabled(True)
        self.layoutQUESBParameters.addWidget(self.comboBoxQUESBEdgeContrast, 5, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxQUESBEdgeContrast)
        
        self.labelQUESBHabitat = QtGui.QLabel()
        self.labelQUESBHabitat.setText('Focal area class(es):')
        self.layoutQUESBParameters.addWidget(self.labelQUESBHabitat, 6, 0)
      
        self.comboBoxTableHabitat = QtGui.QComboBox()
        self.comboBoxTableHabitat.setDisabled(True)
        self.layoutQUESBParameters.addWidget(self.comboBoxTableHabitat, 6, 1)
        
        self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxTableHabitat)
        
        self.buttonLoadLookupTableHabitat = QtGui.QPushButton()
        self.buttonLoadLookupTableHabitat.setText('Load')
        self.layoutQUESBParameters.addWidget(self.buttonLoadLookupTableHabitat, 6, 2)
      
        self.tableHabitat = QtGui.QTableWidget()
        self.tableHabitat.setDisabled(True)
        self.tableHabitat.verticalHeader().setVisible(False)
        self.layoutQUESBParameters.addWidget(self.tableHabitat, 7, 0, 1, 3)
        
        self.groupBoxQUESBMovingWindow = QtGui.QGroupBox('Moving window')
        self.layoutGroupBoxMovingWindow = QtGui.QGridLayout()
        self.layoutGroupBoxMovingWindow.setAlignment(QtCore.Qt.AlignTop)
        self.groupBoxQUESBMovingWindow.setLayout(self.layoutGroupBoxMovingWindow)
        
        self.labelQUESBWindowShape = QtGui.QLabel()
        self.labelQUESBWindowShape.setText('Shape:')
        self.layoutGroupBoxMovingWindow.addWidget(self.labelQUESBWindowShape, 0, 0)
        
        WindowShapeOptions = [
            'Square',
            'Circle',
        ]
        self.comboBoxQUESBWindowShapeOptions = QtGui.QComboBox()
        self.comboBoxQUESBWindowShapeOptions.addItems(WindowShapeOptions)
        self.layoutGroupBoxMovingWindow.addWidget(self.comboBoxQUESBWindowShapeOptions, 0, 1)
        
        self.labelQUESBSamplingWindowSize = QtGui.QLabel()
        self.labelQUESBSamplingWindowSize.setText('Size:')
        self.layoutGroupBoxMovingWindow.addWidget(self.labelQUESBSamplingWindowSize, 1, 0)
        
        self.spinBoxQUESBSamplingWindowSize = QtGui.QSpinBox()
        self.spinBoxQUESBSamplingWindowSize.setRange(1, 9999)
        self.spinBoxQUESBSamplingWindowSize.setValue(1000)
        self.layoutGroupBoxMovingWindow.addWidget(self.spinBoxQUESBSamplingWindowSize, 1, 1)
        
        self.layoutQUESBParameters.addWidget(self.groupBoxQUESBMovingWindow, 8, 0, 1, 2)
        
        self.labelQUESBSamplingGridRes = QtGui.QLabel()
        self.labelQUESBSamplingGridRes.setText('Sampling grid size:')
        self.layoutQUESBParameters.addWidget(self.labelQUESBSamplingGridRes, 9, 0)
        
        self.spinBoxQUESBSamplingGridRes = QtGui.QSpinBox()
        self.spinBoxQUESBSamplingGridRes.setRange(1, 999999)
        self.spinBoxQUESBSamplingGridRes.setValue(10000)
        self.layoutQUESBParameters.addWidget(self.spinBoxQUESBSamplingGridRes, 9, 1)
        
        # Process tab button
        self.layoutButtonQUESB = QtGui.QHBoxLayout()
        self.buttonProcessQUESB = QtGui.QPushButton()
        self.buttonProcessQUESB.setText('&Process')
        self.buttonHelpQUESB = QtGui.QPushButton()
        self.buttonHelpQUESB.setIcon(icon)
        self.layoutButtonQUESB.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonQUESB.addWidget(self.buttonProcessQUESB)
        self.layoutButtonQUESB.addWidget(self.buttonHelpQUESB)
        
        # Template GroupBox
        self.groupBoxQUESBTemplate = QtGui.QGroupBox('Configuration')
        self.layoutGroupBoxQUESBTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxQUESBTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxQUESBTemplate.setLayout(self.layoutGroupBoxQUESBTemplate)
        self.layoutQUESBTemplateInfo = QtGui.QVBoxLayout()
        self.layoutQUESBTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxQUESBTemplate.addLayout(self.layoutQUESBTemplateInfo)
        self.layoutGroupBoxQUESBTemplate.addLayout(self.layoutQUESBTemplate)
        
        self.labelLoadedQUESBTemplate = QtGui.QLabel()
        self.labelLoadedQUESBTemplate.setText('Loaded configuration:')
        self.layoutQUESBTemplate.addWidget(self.labelLoadedQUESBTemplate, 0, 0)
        
        self.loadedQUESBTemplate = QtGui.QLabel()
        self.loadedQUESBTemplate.setText('<None>')
        self.layoutQUESBTemplate.addWidget(self.loadedQUESBTemplate, 0, 1)
        
        self.labelQUESBTemplate = QtGui.QLabel()
        self.labelQUESBTemplate.setText('Name:')
        self.layoutQUESBTemplate.addWidget(self.labelQUESBTemplate, 1, 0)
        
        self.comboBoxQUESBTemplate = QtGui.QComboBox()
        self.comboBoxQUESBTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxQUESBTemplate.setDisabled(True)
        self.comboBoxQUESBTemplate.addItem('No configuration found')
        self.layoutQUESBTemplate.addWidget(self.comboBoxQUESBTemplate, 1, 1)
        
        self.layoutButtonQUESBTemplate = QtGui.QHBoxLayout()
        self.layoutButtonQUESBTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadQUESBTemplate = QtGui.QPushButton()
        self.buttonLoadQUESBTemplate.setDisabled(True)
        self.buttonLoadQUESBTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadQUESBTemplate.setText('Load')
        self.buttonSaveQUESBTemplate = QtGui.QPushButton()
        self.buttonSaveQUESBTemplate.setDisabled(True)
        self.buttonSaveQUESBTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveQUESBTemplate.setText('Save')
        self.buttonSaveAsQUESBTemplate = QtGui.QPushButton()
        self.buttonSaveAsQUESBTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsQUESBTemplate.setText('Save As')
        self.layoutButtonQUESBTemplate.addWidget(self.buttonLoadQUESBTemplate)
        self.layoutButtonQUESBTemplate.addWidget(self.buttonSaveQUESBTemplate)
        self.layoutButtonQUESBTemplate.addWidget(self.buttonSaveAsQUESBTemplate)
        self.layoutGroupBoxQUESBTemplate.addLayout(self.layoutButtonQUESBTemplate)
        
        # Place the GroupBoxes
        self.layoutTabQUESB.addWidget(self.groupBoxQUESBParameters, 0, 0)
        self.layoutTabQUESB.addLayout(self.layoutButtonQUESB, 1, 0, 1, 2, QtCore.Qt.AlignRight)
        self.layoutTabQUESB.addWidget(self.groupBoxQUESBTemplate, 0, 1, 1, 1)
        self.layoutTabQUESB.setColumnStretch(0, 3)
        self.layoutTabQUESB.setColumnStretch(1, 1) # Smaller template column
        
        #***********************************************************
        # Setup 'QUES-H' tab
        #***********************************************************
        self.tabWidgetQUESH = QtGui.QTabWidget()
        QUESHTabWidgetStylesheet = """
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
        self.tabWidgetQUESH.setStyleSheet(QUESHTabWidgetStylesheet)
        
        self.tabWatershedDelineation = QtGui.QWidget()
        self.tabHRUDefinition = QtGui.QWidget()
        self.tabWatershedModelEvaluation = QtGui.QWidget()
        self.tabWatershedIndicators = QtGui.QWidget()
        
        ###self.tabWidgetQUESH.addTab(self.tabWatershedDelineation, 'Watershed Delineation')
        self.tabWidgetQUESH.addTab(self.tabHRUDefinition, 'HRU Definition')
        self.tabWidgetQUESH.addTab(self.tabWatershedModelEvaluation, 'Watershed Model Evaluation')
        self.tabWidgetQUESH.addTab(self.tabWatershedIndicators, 'Watershed Indicators')
        
        self.layoutTabQUESH.addWidget(self.tabWidgetQUESH)
        
        self.layoutTabWatershedDelineation = QtGui.QVBoxLayout()
        ##self.layoutTabHRUDefinition = QtGui.QVBoxLayout()
        self.layoutTabHRUDefinition = QtGui.QGridLayout()
        ##self.layoutTabWatershedModelEvaluation = QtGui.QVBoxLayout()
        self.layoutTabWatershedModelEvaluation = QtGui.QGridLayout()
        ##self.layoutTabWatershedIndicators = QtGui.QVBoxLayout()
        self.layoutTabWatershedIndicators = QtGui.QGridLayout()
        
        self.tabWatershedDelineation.setLayout(self.layoutTabWatershedDelineation)
        self.tabHRUDefinition.setLayout(self.layoutTabHRUDefinition)
        self.tabWatershedModelEvaluation.setLayout(self.layoutTabWatershedModelEvaluation)
        self.tabWatershedIndicators.setLayout(self.layoutTabWatershedIndicators)
        
        #***********************************************************
        # 'Watershed Delineation' sub tab
        #***********************************************************
        
        
        
        #***********************************************************
        # 'Hydrological Response Unit Definition' sub tab
        #***********************************************************
        # 'Functions' GroupBox
        self.groupBoxHRUFunctions = QtGui.QGroupBox('Functions')
        self.layoutGroupBoxHRUFunctions = QtGui.QVBoxLayout()
        self.layoutGroupBoxHRUFunctions.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxHRUFunctions.setLayout(self.layoutGroupBoxHRUFunctions)
        self.layoutHRUFunctionsInfo = QtGui.QVBoxLayout()
        self.layoutHRUFunctions = QtGui.QGridLayout()
        self.layoutGroupBoxHRUFunctions.addLayout(self.layoutHRUFunctionsInfo)
        self.layoutGroupBoxHRUFunctions.addLayout(self.layoutHRUFunctions)
        
        self.labelHRUFunctionsInfo = QtGui.QLabel()
        self.labelHRUFunctionsInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutHRUFunctionsInfo.addWidget(self.labelHRUFunctionsInfo)
        
        self.checkBoxDominantHRU = QtGui.QCheckBox('Dominant HRU')
        self.checkBoxDominantLUSSL = QtGui.QCheckBox('Dominant Land Use, Soil, and Slope')
        self.checkBoxMultipleHRU = QtGui.QCheckBox('Multiple HRU')
        
        self.layoutHRUFunctions.addWidget(self.checkBoxDominantHRU)
        self.layoutHRUFunctions.addWidget(self.checkBoxDominantLUSSL)
        self.layoutHRUFunctions.addWidget(self.checkBoxMultipleHRU)
        
        # 'Parameters' GroupBox
        self.groupBoxHRUParameters = QtGui.QGroupBox('Parameters')
        self.layoutGroupBoxHRUParameters = QtGui.QVBoxLayout()
        self.layoutGroupBoxHRUParameters.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxHRUParameters.setLayout(self.layoutGroupBoxHRUParameters)
        self.layoutHRUParametersInfo = QtGui.QVBoxLayout()
        self.layoutHRUParameters = QtGui.QGridLayout()
        self.layoutGroupBoxHRUParameters.addLayout(self.layoutHRUParametersInfo)
        self.layoutGroupBoxHRUParameters.addLayout(self.layoutHRUParameters)
        
        self.labelHRUParametersInfo = QtGui.QLabel()
        self.labelHRUParametersInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutHRUParametersInfo.addWidget(self.labelHRUParametersInfo)
        
        self.labelHRULandUseMap = QtGui.QLabel()
        self.labelHRULandUseMap.setText('Land use map:')
        self.layoutHRUParameters.addWidget(self.labelHRULandUseMap, 0, 0)
        
        self.lineEditHRULandUseMap = QtGui.QLineEdit()
        self.lineEditHRULandUseMap.setReadOnly(True)
        self.layoutHRUParameters.addWidget(self.lineEditHRULandUseMap, 0, 1)
        
        self.buttonSelectHRULandUseMap = QtGui.QPushButton()
        self.buttonSelectHRULandUseMap.setText('&Browse')
        self.layoutHRUParameters.addWidget(self.buttonSelectHRULandUseMap, 0, 2)
        
        self.labelHRUSoilMap = QtGui.QLabel()
        self.labelHRUSoilMap.setText('Soil map:')
        self.layoutHRUParameters.addWidget(self.labelHRUSoilMap, 1, 0)
        
        self.lineEditHRUSoilMap = QtGui.QLineEdit()
        self.lineEditHRUSoilMap.setReadOnly(True)
        self.layoutHRUParameters.addWidget(self.lineEditHRUSoilMap, 1, 1)
        
        self.buttonSelectHRUSoilMap = QtGui.QPushButton()
        self.buttonSelectHRUSoilMap.setText('&Browse')
        self.layoutHRUParameters.addWidget(self.buttonSelectHRUSoilMap, 1, 2)
        
        self.labelHRUSlopeMap = QtGui.QLabel()
        self.labelHRUSlopeMap.setText('Slope map:')
        self.layoutHRUParameters.addWidget(self.labelHRUSlopeMap, 2, 0)
        
        self.lineEditHRUSlopeMap = QtGui.QLineEdit()
        self.lineEditHRUSlopeMap.setReadOnly(True)
        self.layoutHRUParameters.addWidget(self.lineEditHRUSlopeMap, 2, 1)
        
        self.buttonSelectHRUSlopeMap = QtGui.QPushButton()
        self.buttonSelectHRUSlopeMap.setText('&Browse')
        self.layoutHRUParameters.addWidget(self.buttonSelectHRUSlopeMap, 2, 2)
        
        self.labelHRUSubcatchmentMap = QtGui.QLabel()
        self.labelHRUSubcatchmentMap.setText('Subcatchment map:')
        self.layoutHRUParameters.addWidget(self.labelHRUSubcatchmentMap, 3, 0)
        
        self.lineEditHRUSubcatchmentMap = QtGui.QLineEdit()
        self.lineEditHRUSubcatchmentMap.setReadOnly(True)
        self.layoutHRUParameters.addWidget(self.lineEditHRUSubcatchmentMap, 3, 1)
        
        self.buttonSelectHRUSubcatchmentMap = QtGui.QPushButton()
        self.buttonSelectHRUSubcatchmentMap.setText('&Browse')
        self.layoutHRUParameters.addWidget(self.buttonSelectHRUSubcatchmentMap, 3, 2)
        
        self.labelHRULandUseClassification = QtGui.QLabel()
        self.labelHRULandUseClassification.setText('Land use classification:')
        self.layoutHRUParameters.addWidget(self.labelHRULandUseClassification, 4, 0)
        
        self.lineEditHRULandUseClassification = QtGui.QLineEdit()
        self.lineEditHRULandUseClassification.setReadOnly(True)
        self.layoutHRUParameters.addWidget(self.lineEditHRULandUseClassification, 4, 1)
        
        self.buttonSelectHRULandUseClassification = QtGui.QPushButton()
        self.buttonSelectHRULandUseClassification.setText('&Browse')
        self.layoutHRUParameters.addWidget(self.buttonSelectHRULandUseClassification, 4, 2)
        
        self.labelHRUSoilClassification = QtGui.QLabel()
        self.labelHRUSoilClassification.setText('Soil classification:')
        self.layoutHRUParameters.addWidget(self.labelHRUSoilClassification, 5, 0)
        
        self.lineEditHRUSoilClassification = QtGui.QLineEdit()
        self.lineEditHRUSoilClassification.setReadOnly(True)
        self.layoutHRUParameters.addWidget(self.lineEditHRUSoilClassification, 5, 1)
        
        self.buttonSelectHRUSoilClassification = QtGui.QPushButton()
        self.buttonSelectHRUSoilClassification.setText('&Browse')
        self.layoutHRUParameters.addWidget(self.buttonSelectHRUSoilClassification, 5, 2)
        
        self.labelHRUSlopeClassification = QtGui.QLabel()
        self.labelHRUSlopeClassification.setText('Slope classification:')
        self.layoutHRUParameters.addWidget(self.labelHRUSlopeClassification, 6, 0)
        
        self.lineEditHRUSlopeClassification = QtGui.QLineEdit()
        self.lineEditHRUSlopeClassification.setReadOnly(True)
        self.layoutHRUParameters.addWidget(self.lineEditHRUSlopeClassification, 6, 1)
        
        self.buttonSelectHRUSlopeClassification = QtGui.QPushButton()
        self.buttonSelectHRUSlopeClassification.setText('&Browse')
        self.layoutHRUParameters.addWidget(self.buttonSelectHRUSlopeClassification, 6, 2)
        
        self.labelHRUAreaName = QtGui.QLabel()
        self.labelHRUAreaName.setText('&Area name:')
        self.layoutHRUParameters.addWidget(self.labelHRUAreaName, 7, 0)
        
        self.lineEditHRUAreaName = QtGui.QLineEdit()
        self.lineEditHRUAreaName.setText('areaname')
        self.layoutHRUParameters.addWidget(self.lineEditHRUAreaName, 7, 1)
        self.labelHRUAreaName.setBuddy(self.lineEditHRUAreaName)
        
        self.labelHRUPeriod = QtGui.QLabel()
        self.labelHRUPeriod.setText('Pe&riod:')
        self.layoutHRUParameters.addWidget(self.labelHRUPeriod, 8, 0)
        
        self.spinBoxHRUPeriod = QtGui.QSpinBox()
        self.spinBoxHRUPeriod.setRange(1, 9999)
        td = datetime.date.today()
        self.spinBoxHRUPeriod.setValue(td.year)
        self.layoutHRUParameters.addWidget(self.spinBoxHRUPeriod, 8, 1)
        self.labelHRUPeriod.setBuddy(self.spinBoxHRUPeriod)
        
        self.labelMultipleHRULandUseThreshold = QtGui.QLabel()
        self.labelMultipleHRULandUseThreshold.setDisabled(True)
        self.labelMultipleHRULandUseThreshold.setText('Land use &threshold:')
        self.layoutHRUParameters.addWidget(self.labelMultipleHRULandUseThreshold, 9, 0)
        
        self.spinBoxMultipleHRULandUseThreshold = QtGui.QSpinBox()
        self.spinBoxMultipleHRULandUseThreshold.setDisabled(True)
        self.spinBoxMultipleHRULandUseThreshold.setRange(0, 99999)
        self.spinBoxMultipleHRULandUseThreshold.setValue(0)
        self.layoutHRUParameters.addWidget(self.spinBoxMultipleHRULandUseThreshold, 9, 1)
        self.labelMultipleHRULandUseThreshold.setBuddy(self.spinBoxMultipleHRULandUseThreshold)
        
        self.labelMultipleHRUSoilThreshold = QtGui.QLabel()
        self.labelMultipleHRUSoilThreshold.setDisabled(True)
        self.labelMultipleHRUSoilThreshold.setText('Soil t&hreshold:')
        self.layoutHRUParameters.addWidget(self.labelMultipleHRUSoilThreshold, 10, 0)
        
        self.spinBoxMultipleHRUSoilThreshold = QtGui.QSpinBox()
        self.spinBoxMultipleHRUSoilThreshold.setDisabled(True)
        self.spinBoxMultipleHRUSoilThreshold.setRange(0, 99999)
        self.spinBoxMultipleHRUSoilThreshold.setValue(0)
        self.layoutHRUParameters.addWidget(self.spinBoxMultipleHRUSoilThreshold, 10, 1)
        self.labelMultipleHRUSoilThreshold.setBuddy(self.spinBoxMultipleHRUSoilThreshold)
        
        self.labelMultipleHRUSlopeThreshold = QtGui.QLabel()
        self.labelMultipleHRUSlopeThreshold.setDisabled(True)
        self.labelMultipleHRUSlopeThreshold.setText('Slope th&reshold:')
        self.layoutHRUParameters.addWidget(self.labelMultipleHRUSlopeThreshold, 11, 0)
        
        self.spinBoxMultipleHRUSlopeThreshold = QtGui.QSpinBox()
        self.spinBoxMultipleHRUSlopeThreshold.setDisabled(True)
        self.spinBoxMultipleHRUSlopeThreshold.setRange(0, 99999)
        self.spinBoxMultipleHRUSlopeThreshold.setValue(0)
        self.layoutHRUParameters.addWidget(self.spinBoxMultipleHRUSlopeThreshold, 11, 1)
        self.labelMultipleHRUSlopeThreshold.setBuddy(self.spinBoxMultipleHRUSlopeThreshold)
        
        # Process tab button
        self.layoutButtonHRUDefinition = QtGui.QHBoxLayout()
        self.buttonProcessHRUDefinition = QtGui.QPushButton()
        self.buttonProcessHRUDefinition.setText('&Process')
        self.buttonHelpQUESHHRUDefinition = QtGui.QPushButton()
        self.buttonHelpQUESHHRUDefinition.setIcon(icon)
        self.layoutButtonHRUDefinition.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonHRUDefinition.addWidget(self.buttonProcessHRUDefinition)
        self.layoutButtonHRUDefinition.addWidget(self.buttonHelpQUESHHRUDefinition)
        
        # Template GroupBox
        self.groupBoxHRUDefinitionTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxHRUDefinitionTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxHRUDefinitionTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxHRUDefinitionTemplate.setLayout(self.layoutGroupBoxHRUDefinitionTemplate)
        self.layoutHRUDefinitionTemplateInfo = QtGui.QVBoxLayout()
        self.layoutHRUDefinitionTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxHRUDefinitionTemplate.addLayout(self.layoutHRUDefinitionTemplateInfo)
        self.layoutGroupBoxHRUDefinitionTemplate.addLayout(self.layoutHRUDefinitionTemplate)
        
        self.labelLoadedHRUDefinitionTemplate = QtGui.QLabel()
        self.labelLoadedHRUDefinitionTemplate.setText('Loaded template:')
        self.layoutHRUDefinitionTemplate.addWidget(self.labelLoadedHRUDefinitionTemplate, 0, 0)
        
        self.loadedHRUDefinitionTemplate = QtGui.QLabel()
        self.loadedHRUDefinitionTemplate.setText('<None>')
        self.layoutHRUDefinitionTemplate.addWidget(self.loadedHRUDefinitionTemplate, 0, 1)
        
        self.labelHRUDefinitionTemplate = QtGui.QLabel()
        self.labelHRUDefinitionTemplate.setText('Template name:')
        self.layoutHRUDefinitionTemplate.addWidget(self.labelHRUDefinitionTemplate, 1, 0)
        
        self.comboBoxHRUDefinitionTemplate = QtGui.QComboBox()
        self.comboBoxHRUDefinitionTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxHRUDefinitionTemplate.setDisabled(True)
        self.comboBoxHRUDefinitionTemplate.addItem('No template found')
        self.layoutHRUDefinitionTemplate.addWidget(self.comboBoxHRUDefinitionTemplate, 1, 1)
        
        self.layoutButtonHRUDefinitionTemplate = QtGui.QHBoxLayout()
        self.layoutButtonHRUDefinitionTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadHRUDefinitionTemplate = QtGui.QPushButton()
        self.buttonLoadHRUDefinitionTemplate.setDisabled(True)
        self.buttonLoadHRUDefinitionTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadHRUDefinitionTemplate.setText('Load')
        self.buttonSaveHRUDefinitionTemplate = QtGui.QPushButton()
        self.buttonSaveHRUDefinitionTemplate.setDisabled(True)
        self.buttonSaveHRUDefinitionTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveHRUDefinitionTemplate.setText('Save')
        self.buttonSaveAsHRUDefinitionTemplate = QtGui.QPushButton()
        self.buttonSaveAsHRUDefinitionTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsHRUDefinitionTemplate.setText('Save As')
        self.layoutButtonHRUDefinitionTemplate.addWidget(self.buttonLoadHRUDefinitionTemplate)
        self.layoutButtonHRUDefinitionTemplate.addWidget(self.buttonSaveHRUDefinitionTemplate)
        self.layoutButtonHRUDefinitionTemplate.addWidget(self.buttonSaveAsHRUDefinitionTemplate)
        self.layoutGroupBoxHRUDefinitionTemplate.addLayout(self.layoutButtonHRUDefinitionTemplate)
        
        # Place the GroupBoxes
        self.layoutTabHRUDefinition.addWidget(self.groupBoxHRUFunctions, 0, 0)
        self.layoutTabHRUDefinition.addWidget(self.groupBoxHRUParameters, 1, 0)
        self.layoutTabHRUDefinition.addLayout(self.layoutButtonHRUDefinition, 2, 0, 1, 2, QtCore.Qt.AlignRight)
        self.layoutTabHRUDefinition.addWidget(self.groupBoxHRUDefinitionTemplate, 0, 1, 2, 1)
        self.layoutTabHRUDefinition.setColumnStretch(0, 3)
        self.layoutTabHRUDefinition.setColumnStretch(1, 1) # Smaller template column
        
        #***********************************************************
        # 'Watershed Model Evaluation' sub tab
        #***********************************************************
        # 'Parameters' GroupBox
        self.groupBoxWatershedModelEvaluationParameters = QtGui.QGroupBox('Parameters')
        self.layoutGroupBoxWatershedModelEvaluationParameters = QtGui.QVBoxLayout()
        self.layoutGroupBoxWatershedModelEvaluationParameters.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxWatershedModelEvaluationParameters.setLayout(self.layoutGroupBoxWatershedModelEvaluationParameters)
        self.layoutWatershedModelEvaluationParametersInfo = QtGui.QVBoxLayout()
        self.layoutWatershedModelEvaluationParameters = QtGui.QGridLayout()
        self.layoutGroupBoxWatershedModelEvaluationParameters.addLayout(self.layoutWatershedModelEvaluationParametersInfo)
        self.layoutGroupBoxWatershedModelEvaluationParameters.addLayout(self.layoutWatershedModelEvaluationParameters)
        
        self.labelWatershedModelEvaluationParametersInfo = QtGui.QLabel()
        self.labelWatershedModelEvaluationParametersInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutWatershedModelEvaluationParametersInfo.addWidget(self.labelWatershedModelEvaluationParametersInfo)
        
        self.labelWatershedModelEvaluationDateInitial = QtGui.QLabel()
        self.labelWatershedModelEvaluationDateInitial.setText('Initial date:')
        self.layoutWatershedModelEvaluationParameters.addWidget(self.labelWatershedModelEvaluationDateInitial, 0, 0)
        
        self.dateWatershedModelEvaluationDateInitial = QtGui.QDateEdit(QtCore.QDate.currentDate())
        self.dateWatershedModelEvaluationDateInitial.setCalendarPopup(True)
        self.dateWatershedModelEvaluationDateInitial.setDisplayFormat('dd/MM/yyyy')
        self.layoutWatershedModelEvaluationParameters.addWidget(self.dateWatershedModelEvaluationDateInitial, 0, 1)
        
        self.labelWatershedModelEvaluationDateFinal = QtGui.QLabel()
        self.labelWatershedModelEvaluationDateFinal.setText('Final date:')
        self.layoutWatershedModelEvaluationParameters.addWidget(self.labelWatershedModelEvaluationDateFinal, 1, 0)
        
        self.dateWatershedModelEvaluationDateFinal = QtGui.QDateEdit(QtCore.QDate.currentDate())
        self.dateWatershedModelEvaluationDateFinal.setCalendarPopup(True)
        self.dateWatershedModelEvaluationDateFinal.setDisplayFormat('dd/MM/yyyy')
        self.layoutWatershedModelEvaluationParameters.addWidget(self.dateWatershedModelEvaluationDateFinal, 1, 1)
        
        self.labelWatershedModelEvaluationSWATModel = QtGui.QLabel()
        self.labelWatershedModelEvaluationSWATModel.setText('SWAT &model:')
        self.layoutWatershedModelEvaluationParameters.addWidget(self.labelWatershedModelEvaluationSWATModel, 2, 0)
        
        SWATModel = {
            1: 'Skip',
            2: 'Run',
        }
        
        self.comboBoxWatershedModelEvaluationSWATModel = QtGui.QComboBox()
        
        for key, val in SWATModel.iteritems():
            self.comboBoxWatershedModelEvaluationSWATModel.addItem(val, key)
        
        self.layoutWatershedModelEvaluationParameters.addWidget(self.comboBoxWatershedModelEvaluationSWATModel, 2, 1)
        self.labelWatershedModelEvaluationSWATModel.setBuddy(self.comboBoxWatershedModelEvaluationSWATModel)
        
        self.labelWatershedModelEvaluationLocation = QtGui.QLabel()
        self.labelWatershedModelEvaluationLocation.setText('&Location:')
        self.layoutWatershedModelEvaluationParameters.addWidget(self.labelWatershedModelEvaluationLocation, 3, 0)
        
        self.lineEditWatershedModelEvaluationLocation = QtGui.QLineEdit()
        self.lineEditWatershedModelEvaluationLocation.setText('location')
        self.layoutWatershedModelEvaluationParameters.addWidget(self.lineEditWatershedModelEvaluationLocation, 3, 1)
        self.labelWatershedModelEvaluationLocation.setBuddy(self.lineEditWatershedModelEvaluationLocation)
        
        self.labelWatershedModelEvaluationOutletReachSubBasinID = QtGui.QLabel()
        self.labelWatershedModelEvaluationOutletReachSubBasinID.setText('Outlet reach/sub-basin ID:')
        self.layoutWatershedModelEvaluationParameters.addWidget(self.labelWatershedModelEvaluationOutletReachSubBasinID, 4, 0)
        
        self.spinBoxWatershedModelEvaluationOutletReachSubBasinID = QtGui.QSpinBox()
        self.spinBoxWatershedModelEvaluationOutletReachSubBasinID.setRange(1, 99999)
        self.spinBoxWatershedModelEvaluationOutletReachSubBasinID.setValue(10)
        self.layoutWatershedModelEvaluationParameters.addWidget(self.spinBoxWatershedModelEvaluationOutletReachSubBasinID, 4, 1)
        self.labelWatershedModelEvaluationOutletReachSubBasinID.setBuddy(self.spinBoxWatershedModelEvaluationOutletReachSubBasinID)
        
        self.labelWatershedModelEvaluationObservedDebitFile = QtGui.QLabel()
        self.labelWatershedModelEvaluationObservedDebitFile.setText('Observed debit file:')
        self.layoutWatershedModelEvaluationParameters.addWidget(self.labelWatershedModelEvaluationObservedDebitFile, 5, 0)
        
        self.lineEditWatershedModelEvaluationObservedDebitFile = QtGui.QLineEdit()
        self.lineEditWatershedModelEvaluationObservedDebitFile.setReadOnly(True)
        self.layoutWatershedModelEvaluationParameters.addWidget(self.lineEditWatershedModelEvaluationObservedDebitFile, 5, 1)
        
        self.buttonSelectWatershedModelEvaluationObservedDebitFile = QtGui.QPushButton()
        self.buttonSelectWatershedModelEvaluationObservedDebitFile.setText('&Browse')
        self.layoutWatershedModelEvaluationParameters.addWidget(self.buttonSelectWatershedModelEvaluationObservedDebitFile, 5, 2)
        
        # 'Output' GroupBox
        self.groupBoxWatershedModelEvaluationOutput = QtGui.QGroupBox('Output')
        self.layoutGroupBoxWatershedModelEvaluationOutput = QtGui.QVBoxLayout()
        self.layoutGroupBoxWatershedModelEvaluationOutput.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxWatershedModelEvaluationOutput.setLayout(self.layoutGroupBoxWatershedModelEvaluationOutput)
        self.layoutWatershedModelEvaluationOutputInfo = QtGui.QVBoxLayout()
        self.layoutWatershedModelEvaluationOutput = QtGui.QGridLayout()
        self.layoutGroupBoxWatershedModelEvaluationOutput.addLayout(self.layoutWatershedModelEvaluationOutputInfo)
        self.layoutGroupBoxWatershedModelEvaluationOutput.addLayout(self.layoutWatershedModelEvaluationOutput)
        
        self.labelWatershedModelEvaluationOutputInfo = QtGui.QLabel()
        self.labelWatershedModelEvaluationOutputInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutWatershedModelEvaluationOutputInfo.addWidget(self.labelWatershedModelEvaluationOutputInfo)
        
        self.labelOutputWatershedModelEvaluation = QtGui.QLabel()
        self.labelOutputWatershedModelEvaluation.setText('[Output] Watershed model evaluation:')
        self.layoutWatershedModelEvaluationOutput.addWidget(self.labelOutputWatershedModelEvaluation, 0, 0)
        
        self.lineEditOutputWatershedModelEvaluation = QtGui.QLineEdit()
        self.lineEditOutputWatershedModelEvaluation.setReadOnly(True)
        self.layoutWatershedModelEvaluationOutput.addWidget(self.lineEditOutputWatershedModelEvaluation, 0, 1)
        
        self.buttonSelectOutputWatershedModelEvaluation = QtGui.QPushButton()
        self.buttonSelectOutputWatershedModelEvaluation.setText('&Browse')
        self.layoutWatershedModelEvaluationOutput.addWidget(self.buttonSelectOutputWatershedModelEvaluation, 0, 2)
        
        # Process tab button
        self.layoutButtonWatershedModelEvaluation = QtGui.QHBoxLayout()
        self.buttonProcessWatershedModelEvaluation = QtGui.QPushButton()
        self.buttonProcessWatershedModelEvaluation.setText('&Process')
        self.buttonHelpQUESHWatershedModelEvaluation = QtGui.QPushButton()
        self.buttonHelpQUESHWatershedModelEvaluation.setIcon(icon)
        self.layoutButtonWatershedModelEvaluation.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonWatershedModelEvaluation.addWidget(self.buttonProcessWatershedModelEvaluation)
        self.layoutButtonWatershedModelEvaluation.addWidget(self.buttonHelpQUESHWatershedModelEvaluation)
        
        # Template GroupBox
        self.groupBoxWatershedModelEvaluationTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxWatershedModelEvaluationTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxWatershedModelEvaluationTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxWatershedModelEvaluationTemplate.setLayout(self.layoutGroupBoxWatershedModelEvaluationTemplate)
        self.layoutWatershedModelEvaluationTemplateInfo = QtGui.QVBoxLayout()
        self.layoutWatershedModelEvaluationTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxWatershedModelEvaluationTemplate.addLayout(self.layoutWatershedModelEvaluationTemplateInfo)
        self.layoutGroupBoxWatershedModelEvaluationTemplate.addLayout(self.layoutWatershedModelEvaluationTemplate)
        
        self.labelLoadedWatershedModelEvaluationTemplate = QtGui.QLabel()
        self.labelLoadedWatershedModelEvaluationTemplate.setText('Loaded template:')
        self.layoutWatershedModelEvaluationTemplate.addWidget(self.labelLoadedWatershedModelEvaluationTemplate, 0, 0)
        
        self.loadedWatershedModelEvaluationTemplate = QtGui.QLabel()
        self.loadedWatershedModelEvaluationTemplate.setText('<None>')
        self.layoutWatershedModelEvaluationTemplate.addWidget(self.loadedWatershedModelEvaluationTemplate, 0, 1)
        
        self.labelWatershedModelEvaluationTemplate = QtGui.QLabel()
        self.labelWatershedModelEvaluationTemplate.setText('Template name:')
        self.layoutWatershedModelEvaluationTemplate.addWidget(self.labelWatershedModelEvaluationTemplate, 1, 0)
        
        self.comboBoxWatershedModelEvaluationTemplate = QtGui.QComboBox()
        self.comboBoxWatershedModelEvaluationTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxWatershedModelEvaluationTemplate.setDisabled(True)
        self.comboBoxWatershedModelEvaluationTemplate.addItem('No template found')
        self.layoutWatershedModelEvaluationTemplate.addWidget(self.comboBoxWatershedModelEvaluationTemplate, 1, 1)
        
        self.layoutButtonWatershedModelEvaluationTemplate = QtGui.QHBoxLayout()
        self.layoutButtonWatershedModelEvaluationTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadWatershedModelEvaluationTemplate = QtGui.QPushButton()
        self.buttonLoadWatershedModelEvaluationTemplate.setDisabled(True)
        self.buttonLoadWatershedModelEvaluationTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadWatershedModelEvaluationTemplate.setText('Load')
        self.buttonSaveWatershedModelEvaluationTemplate = QtGui.QPushButton()
        self.buttonSaveWatershedModelEvaluationTemplate.setDisabled(True)
        self.buttonSaveWatershedModelEvaluationTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveWatershedModelEvaluationTemplate.setText('Save')
        self.buttonSaveAsWatershedModelEvaluationTemplate = QtGui.QPushButton()
        self.buttonSaveAsWatershedModelEvaluationTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsWatershedModelEvaluationTemplate.setText('Save As')
        self.layoutButtonWatershedModelEvaluationTemplate.addWidget(self.buttonLoadWatershedModelEvaluationTemplate)
        self.layoutButtonWatershedModelEvaluationTemplate.addWidget(self.buttonSaveWatershedModelEvaluationTemplate)
        self.layoutButtonWatershedModelEvaluationTemplate.addWidget(self.buttonSaveAsWatershedModelEvaluationTemplate)
        self.layoutGroupBoxWatershedModelEvaluationTemplate.addLayout(self.layoutButtonWatershedModelEvaluationTemplate)
        
        # Place the GroupBoxes
        self.layoutTabWatershedModelEvaluation.addWidget(self.groupBoxWatershedModelEvaluationParameters, 0, 0)
        self.layoutTabWatershedModelEvaluation.addWidget(self.groupBoxWatershedModelEvaluationOutput, 1, 0)
        self.layoutTabWatershedModelEvaluation.addLayout(self.layoutButtonWatershedModelEvaluation, 2, 0, 1, 2, QtCore.Qt.AlignRight)
        self.layoutTabWatershedModelEvaluation.addWidget(self.groupBoxWatershedModelEvaluationTemplate, 0, 1, 2, 1)
        self.layoutTabWatershedModelEvaluation.setColumnStretch(0, 3)
        self.layoutTabWatershedModelEvaluation.setColumnStretch(1, 1) # Smaller template column
        
        #***********************************************************
        # 'Watershed Indicators' sub tab
        #***********************************************************
        # 'Parameters' GroupBox
        self.groupBoxWatershedIndicatorsParameters = QtGui.QGroupBox('Parameters')
        self.layoutGroupBoxWatershedIndicatorsParameters = QtGui.QVBoxLayout()
        self.layoutGroupBoxWatershedIndicatorsParameters.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxWatershedIndicatorsParameters.setLayout(self.layoutGroupBoxWatershedIndicatorsParameters)
        self.layoutWatershedIndicatorsParametersInfo = QtGui.QVBoxLayout()
        self.layoutWatershedIndicatorsParameters = QtGui.QGridLayout()
        self.layoutGroupBoxWatershedIndicatorsParameters.addLayout(self.layoutWatershedIndicatorsParametersInfo)
        self.layoutGroupBoxWatershedIndicatorsParameters.addLayout(self.layoutWatershedIndicatorsParameters)
        
        self.labelWatershedIndicatorsParametersInfo = QtGui.QLabel()
        self.labelWatershedIndicatorsParametersInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutWatershedIndicatorsParametersInfo.addWidget(self.labelWatershedIndicatorsParametersInfo)
        
        self.labelWatershedIndicatorsSWATTXTINOUTDir = QtGui.QLabel()
        self.labelWatershedIndicatorsSWATTXTINOUTDir.setText('SWAT TXTINOUT directory:')
        self.layoutWatershedIndicatorsParameters.addWidget(self.labelWatershedIndicatorsSWATTXTINOUTDir, 0, 0)
        
        self.lineEditWatershedIndicatorsSWATTXTINOUTDir = QtGui.QLineEdit()
        self.lineEditWatershedIndicatorsSWATTXTINOUTDir.setReadOnly(True)
        self.layoutWatershedIndicatorsParameters.addWidget(self.lineEditWatershedIndicatorsSWATTXTINOUTDir, 0, 1)
        
        self.buttonSelectWatershedIndicatorsSWATTXTINOUTDir = QtGui.QPushButton()
        self.buttonSelectWatershedIndicatorsSWATTXTINOUTDir.setText('&Browse')
        self.layoutWatershedIndicatorsParameters.addWidget(self.buttonSelectWatershedIndicatorsSWATTXTINOUTDir, 0, 2)
        
        self.labelWatershedIndicatorsDateInitial = QtGui.QLabel()
        self.labelWatershedIndicatorsDateInitial.setText('Initial date:')
        self.layoutWatershedIndicatorsParameters.addWidget(self.labelWatershedIndicatorsDateInitial, 1, 0)
        
        self.dateWatershedIndicatorsDateInitial = QtGui.QDateEdit(QtCore.QDate.currentDate())
        self.dateWatershedIndicatorsDateInitial.setCalendarPopup(True)
        self.dateWatershedIndicatorsDateInitial.setDisplayFormat('dd/MM/yyyy')
        self.layoutWatershedIndicatorsParameters.addWidget(self.dateWatershedIndicatorsDateInitial, 1, 1)
        
        self.labelWatershedIndicatorsDateFinal = QtGui.QLabel()
        self.labelWatershedIndicatorsDateFinal.setText('Final date:')
        self.layoutWatershedIndicatorsParameters.addWidget(self.labelWatershedIndicatorsDateFinal, 2, 0)
        
        self.dateWatershedIndicatorsDateFinal = QtGui.QDateEdit(QtCore.QDate.currentDate())
        self.dateWatershedIndicatorsDateFinal.setCalendarPopup(True)
        self.dateWatershedIndicatorsDateFinal.setDisplayFormat('dd/MM/yyyy')
        self.layoutWatershedIndicatorsParameters.addWidget(self.dateWatershedIndicatorsDateFinal, 2, 1)
        
        self.labelWatershedIndicatorsSubWatershedPolygon = QtGui.QLabel()
        self.labelWatershedIndicatorsSubWatershedPolygon.setText('Sub watershed polygon:')
        self.layoutWatershedIndicatorsParameters.addWidget(self.labelWatershedIndicatorsSubWatershedPolygon, 3, 0)
        
        self.lineEditWatershedIndicatorsSubWatershedPolygon = QtGui.QLineEdit()
        self.lineEditWatershedIndicatorsSubWatershedPolygon.setReadOnly(True)
        self.layoutWatershedIndicatorsParameters.addWidget(self.lineEditWatershedIndicatorsSubWatershedPolygon, 3, 1)
        
        self.buttonSelectWatershedIndicatorsSubWatershedPolygon = QtGui.QPushButton()
        self.buttonSelectWatershedIndicatorsSubWatershedPolygon.setText('&Browse')
        self.layoutWatershedIndicatorsParameters.addWidget(self.buttonSelectWatershedIndicatorsSubWatershedPolygon, 3, 2)
        
        self.labelWatershedIndicatorsLocation = QtGui.QLabel()
        self.labelWatershedIndicatorsLocation.setText('&Location:')
        self.layoutWatershedIndicatorsParameters.addWidget(self.labelWatershedIndicatorsLocation, 4, 0)
        
        self.lineEditWatershedIndicatorsLocation = QtGui.QLineEdit()
        self.lineEditWatershedIndicatorsLocation.setText('location')
        self.layoutWatershedIndicatorsParameters.addWidget(self.lineEditWatershedIndicatorsLocation, 4, 1)
        self.labelWatershedIndicatorsLocation.setBuddy(self.lineEditWatershedIndicatorsLocation)
        
        self.labelWatershedIndicatorsSubWatershedOutput = QtGui.QLabel()
        self.labelWatershedIndicatorsSubWatershedOutput.setText('&Sub watershed output:')
        self.layoutWatershedIndicatorsParameters.addWidget(self.labelWatershedIndicatorsSubWatershedOutput, 5, 0)
        
        self.spinBoxWatershedIndicatorsSubWatershedOutput = QtGui.QSpinBox()
        self.spinBoxWatershedIndicatorsSubWatershedOutput.setRange(1, 99999)
        self.spinBoxWatershedIndicatorsSubWatershedOutput.setValue(10)
        self.layoutWatershedIndicatorsParameters.addWidget(self.spinBoxWatershedIndicatorsSubWatershedOutput, 5, 1)
        self.labelWatershedIndicatorsSubWatershedOutput.setBuddy(self.spinBoxWatershedIndicatorsSubWatershedOutput)
        
        # 'Output' GroupBox
        self.groupBoxWatershedIndicatorsOutput = QtGui.QGroupBox('Output')
        self.layoutGroupBoxWatershedIndicatorsOutput = QtGui.QVBoxLayout()
        self.layoutGroupBoxWatershedIndicatorsOutput.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxWatershedIndicatorsOutput.setLayout(self.layoutGroupBoxWatershedIndicatorsOutput)
        self.layoutWatershedIndicatorsOutputInfo = QtGui.QVBoxLayout()
        self.layoutWatershedIndicatorsOutput = QtGui.QGridLayout()
        self.layoutGroupBoxWatershedIndicatorsOutput.addLayout(self.layoutWatershedIndicatorsOutputInfo)
        self.layoutGroupBoxWatershedIndicatorsOutput.addLayout(self.layoutWatershedIndicatorsOutput)
        
        self.labelWatershedIndicatorsOutputInfo = QtGui.QLabel()
        self.labelWatershedIndicatorsOutputInfo.setText('Lorem ipsum dolor sit amet...\n')
        self.layoutWatershedIndicatorsOutputInfo.addWidget(self.labelWatershedIndicatorsOutputInfo)
        
        self.labelWatershedIndicatorsOutputInitialYearSubWatershedLevelIndicators = QtGui.QLabel()
        self.labelWatershedIndicatorsOutputInitialYearSubWatershedLevelIndicators.setText('[Output] Initial year sub watershed level indicators:')
        self.layoutWatershedIndicatorsOutput.addWidget(self.labelWatershedIndicatorsOutputInitialYearSubWatershedLevelIndicators, 0, 0)
        
        self.lineEditWatershedIndicatorsOutputInitialYearSubWatershedLevelIndicators = QtGui.QLineEdit()
        self.lineEditWatershedIndicatorsOutputInitialYearSubWatershedLevelIndicators.setReadOnly(True)
        self.layoutWatershedIndicatorsOutput.addWidget(self.lineEditWatershedIndicatorsOutputInitialYearSubWatershedLevelIndicators, 0, 1)
        
        self.buttonSelectWatershedIndicatorsOutputInitialYearSubWatershedLevelIndicators = QtGui.QPushButton()
        self.buttonSelectWatershedIndicatorsOutputInitialYearSubWatershedLevelIndicators.setText('&Browse')
        self.layoutWatershedIndicatorsOutput.addWidget(self.buttonSelectWatershedIndicatorsOutputInitialYearSubWatershedLevelIndicators, 0, 2)
        
        self.labelWatershedIndicatorsOutputFinalYearSubWatershedLevelIndicators = QtGui.QLabel()
        self.labelWatershedIndicatorsOutputFinalYearSubWatershedLevelIndicators.setText('[Output] Final year sub watershed level indicators:')
        self.layoutWatershedIndicatorsOutput.addWidget(self.labelWatershedIndicatorsOutputFinalYearSubWatershedLevelIndicators, 1, 0)
        
        self.lineEditWatershedIndicatorsOutputFinalYearSubWatershedLevelIndicators = QtGui.QLineEdit()
        self.lineEditWatershedIndicatorsOutputFinalYearSubWatershedLevelIndicators.setReadOnly(True)
        self.layoutWatershedIndicatorsOutput.addWidget(self.lineEditWatershedIndicatorsOutputFinalYearSubWatershedLevelIndicators, 1, 1)
        
        self.buttonSelectWatershedIndicatorsOutputFinalYearSubWatershedLevelIndicators = QtGui.QPushButton()
        self.buttonSelectWatershedIndicatorsOutputFinalYearSubWatershedLevelIndicators.setText('&Browse')
        self.layoutWatershedIndicatorsOutput.addWidget(self.buttonSelectWatershedIndicatorsOutputFinalYearSubWatershedLevelIndicators, 1, 2)
        
        # Process tab button
        self.layoutButtonWatershedIndicators = QtGui.QHBoxLayout()
        self.buttonProcessWatershedIndicators = QtGui.QPushButton()
        self.buttonProcessWatershedIndicators.setText('&Process')
        self.buttonHelpQUESHWatershedIndicators = QtGui.QPushButton()
        self.buttonHelpQUESHWatershedIndicators.setIcon(icon)
        self.layoutButtonWatershedIndicators.setAlignment(QtCore.Qt.AlignRight)
        self.layoutButtonWatershedIndicators.addWidget(self.buttonProcessWatershedIndicators)
        self.layoutButtonWatershedIndicators.addWidget(self.buttonHelpQUESHWatershedIndicators)
        
        # Template GroupBox
        self.groupBoxWatershedIndicatorsTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxWatershedIndicatorsTemplate = QtGui.QVBoxLayout()
        self.layoutGroupBoxWatershedIndicatorsTemplate.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxWatershedIndicatorsTemplate.setLayout(self.layoutGroupBoxWatershedIndicatorsTemplate)
        self.layoutWatershedIndicatorsTemplateInfo = QtGui.QVBoxLayout()
        self.layoutWatershedIndicatorsTemplate = QtGui.QGridLayout()
        self.layoutGroupBoxWatershedIndicatorsTemplate.addLayout(self.layoutWatershedIndicatorsTemplateInfo)
        self.layoutGroupBoxWatershedIndicatorsTemplate.addLayout(self.layoutWatershedIndicatorsTemplate)
        
        self.labelLoadedWatershedIndicatorsTemplate = QtGui.QLabel()
        self.labelLoadedWatershedIndicatorsTemplate.setText('Loaded template:')
        self.layoutWatershedIndicatorsTemplate.addWidget(self.labelLoadedWatershedIndicatorsTemplate, 0, 0)
        
        self.loadedWatershedIndicatorsTemplate = QtGui.QLabel()
        self.loadedWatershedIndicatorsTemplate.setText('<None>')
        self.layoutWatershedIndicatorsTemplate.addWidget(self.loadedWatershedIndicatorsTemplate, 0, 1)
        
        self.labelWatershedIndicatorsTemplate = QtGui.QLabel()
        self.labelWatershedIndicatorsTemplate.setText('Template name:')
        self.layoutWatershedIndicatorsTemplate.addWidget(self.labelWatershedIndicatorsTemplate, 1, 0)
        
        self.comboBoxWatershedIndicatorsTemplate = QtGui.QComboBox()
        self.comboBoxWatershedIndicatorsTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxWatershedIndicatorsTemplate.setDisabled(True)
        self.comboBoxWatershedIndicatorsTemplate.addItem('No template found')
        self.layoutWatershedIndicatorsTemplate.addWidget(self.comboBoxWatershedIndicatorsTemplate, 1, 1)
        
        self.layoutButtonWatershedIndicatorsTemplate = QtGui.QHBoxLayout()
        self.layoutButtonWatershedIndicatorsTemplate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.buttonLoadWatershedIndicatorsTemplate = QtGui.QPushButton()
        self.buttonLoadWatershedIndicatorsTemplate.setDisabled(True)
        self.buttonLoadWatershedIndicatorsTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonLoadWatershedIndicatorsTemplate.setText('Load')
        self.buttonSaveWatershedIndicatorsTemplate = QtGui.QPushButton()
        self.buttonSaveWatershedIndicatorsTemplate.setDisabled(True)
        self.buttonSaveWatershedIndicatorsTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveWatershedIndicatorsTemplate.setText('Save')
        self.buttonSaveAsWatershedIndicatorsTemplate = QtGui.QPushButton()
        self.buttonSaveAsWatershedIndicatorsTemplate.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.buttonSaveAsWatershedIndicatorsTemplate.setText('Save As')
        self.layoutButtonWatershedIndicatorsTemplate.addWidget(self.buttonLoadWatershedIndicatorsTemplate)
        self.layoutButtonWatershedIndicatorsTemplate.addWidget(self.buttonSaveWatershedIndicatorsTemplate)
        self.layoutButtonWatershedIndicatorsTemplate.addWidget(self.buttonSaveAsWatershedIndicatorsTemplate)
        self.layoutGroupBoxWatershedIndicatorsTemplate.addLayout(self.layoutButtonWatershedIndicatorsTemplate)
        
        # Place the GroupBoxes
        self.layoutTabWatershedIndicators.addWidget(self.groupBoxWatershedIndicatorsParameters, 0, 0)
        self.layoutTabWatershedIndicators.addWidget(self.groupBoxWatershedIndicatorsOutput, 1, 0)
        self.layoutTabWatershedIndicators.addLayout(self.layoutButtonWatershedIndicators, 2, 0, 1, 2, QtCore.Qt.AlignRight)
        self.layoutTabWatershedIndicators.addWidget(self.groupBoxWatershedIndicatorsTemplate, 0, 1, 2, 1)
        self.layoutTabWatershedIndicators.setColumnStretch(0, 3)
        self.layoutTabWatershedIndicators.setColumnStretch(1, 1) # Smaller template column
        
        
        #***********************************************************
        # Setup 'Reclassification' tab
        #***********************************************************
        
        
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
        self.setMinimumSize(700, 640)
        self.resize(parent.sizeHint())
    
    
    def showEvent(self, event):
        """Overload method that is called when the dialog widget is shown.
        
        Args:
            event (QShowEvent): the show widget event.
        """
        super(DialogLumensQUES, self).showEvent(event)
    
    
    def closeEvent(self, event):
        """Overload method that is called when the dialog widget is closed.
        
        Args:
            event (QCloseEvent): the close widget event.
        """
        super(DialogLumensQUES, self).closeEvent(event)
    
    
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
                checkBoxSummarizeMultiplePeriodQUESCDatabase = QtGui.QCheckBox()
                checkBoxSummarizeMultiplePeriodQUESCDatabase.setObjectName('checkBoxSummarizeMultiplePeriodQUESCDatabase_{0}'.format(str(self.checkBoxQUESCDatabaseCount)))
                checkBoxSummarizeMultiplePeriodQUESCDatabase.setText(name)
                layoutCheckBoxQUESCDatabase.addWidget(checkBoxSummarizeMultiplePeriodQUESCDatabase)
                checkBoxSummarizeMultiplePeriodQUESCDatabase.toggled.connect(self.toggleSummarizeMultiplePeriodQUESCDatabase)
        else:
            labelQUESCDatabaseSummarizeMultiplePeriod = QtGui.QLabel()
            labelQUESCDatabaseSummarizeMultiplePeriod.setText('\nNo QUES-C Database found!\n')
            layoutCheckBoxQUESCDatabase.addWidget(labelQUESCDatabaseSummarizeMultiplePeriod)

        self.layoutOptionsSummarizeMultiplePeriod.addLayout(layoutCheckBoxQUESCDatabase)
        
    
    #***********************************************************
    # 'QUES-C' tab QGroupBox toggle handlers
    #***********************************************************
    def toggleCarbonAccounting(self, checked):
        """Slot method for handling checkbox toggling.
        
        Args:
            checked (bool): the checkbox status.
        """
        if checked:
            self.contentOptionsCarbonAccounting.setEnabled(True)
        else:
            self.contentOptionsCarbonAccounting.setDisabled(True)
    
    
    def togglePeatlandCarbonAccounting(self, checked):
        """Slot method for handling checkbox toggling.
        
        Args:
            checked (bool): the checkbox status.
        """
        if checked:
            self.handlerPopulateNameFromLookupData(self.main.dataPlanningUnit, self.comboBoxPeatlandMap) 
            self.handlerPopulateNameFromLookupData(self.main.dataTable, self.comboBoxPCACsvfile)
        else:
            self.comboBoxPeatlandMap.setDisabled(True)
            self.comboBoxPCACsvfile.setDisabled(True)
    
    
    def toggleSummarizeMultiplePeriod(self, checked):
        """Slot method for handling checkbox toggling.
        
        Args:
            checked (bool): the checkbox status.
        """
        if checked:
            self.contentOptionsSummarizeMultiplePeriod.setEnabled(True)
        else:
            self.contentOptionsSummarizeMultiplePeriod.setDisabled(True)
            
            
    def toggleSummarizeMultiplePeriodQUESCDatabase(self, checked):
        """Slot method for handling checkbox toggling.

        Args:
            checked (bool): the checkbox status.
        """
        checkBoxSender = self.sender()
        objectName = checkBoxSender.objectName()
        checkBoxIndex = objectName.split('_')[1]

        checkBoxQUESCDatabase = self.contentOptionsSummarizeMultiplePeriod.findChild(QtGui.QCheckBox, 'checkBoxSummarizeMultiplePeriodQUESCDatabase_' + checkBoxIndex)
        checkBoxName = checkBoxQUESCDatabase.text()

        if checked:
            self.listOfQUESCDatabase.append(checkBoxName)
        else:
            self.listOfQUESCDatabase.remove(checkBoxName)            
    
    
    #***********************************************************
    # 'QUES-H' tab QGroupBox toggle handlers
    #***********************************************************
    def toggleMultipleHRU(self, checked):
        """Slot method for handling checkbox toggling.
        
        Args:
            checked (bool): the checkbox status.
        """
        if checked:
            self.labelMultipleHRULandUseThreshold.setEnabled(True)
            self.spinBoxMultipleHRULandUseThreshold.setEnabled(True)
            self.labelMultipleHRUSoilThreshold.setEnabled(True)
            self.spinBoxMultipleHRUSoilThreshold.setEnabled(True)
            self.labelMultipleHRUSlopeThreshold.setEnabled(True)
            self.spinBoxMultipleHRUSlopeThreshold.setEnabled(True)
        else:
            self.labelMultipleHRULandUseThreshold.setDisabled(True)
            self.spinBoxMultipleHRULandUseThreshold.setDisabled(True)
            self.labelMultipleHRUSoilThreshold.setDisabled(True)
            self.spinBoxMultipleHRUSoilThreshold.setDisabled(True)
            self.labelMultipleHRUSlopeThreshold.setDisabled(True)
            self.spinBoxMultipleHRUSlopeThreshold.setDisabled(True)
    
    
    #***********************************************************
    # 'Pre-QUES' tab QPushButton handlers
    #***********************************************************
    def handlerLoadPreQUESTemplate(self, fileName=None):
        """Slot method for loading a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.comboBoxPreQUESTemplate.currentText()
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
            self.loadTemplate('Pre-QUES', templateFile)
    
    
    def handlerSavePreQUESTemplate(self, fileName=None):
        """Slot method for saving a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.currentPreQUESTemplate
        
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
            self.saveTemplate('Pre-QUES', templateFile)
            return True
        else:
            return False
    
    
    def handlerSaveAsPreQUESTemplate(self):
        """Slot method for saving a module template to a new file.
        """
        fileName, ok = QtGui.QInputDialog.getText(self, 'Save As', 'Enter a new template name:')
        fileSaved = False
        
        if ok:
            now = QtCore.QDateTime.currentDateTime().toString('yyyyMMdd-hhmmss')
            fileName = now + '__' + fileName + '.ini'
            
            if os.path.exists(os.path.join(self.settingsPath, fileName)):
                fileSaved = self.handlerSavePreQUESTemplate(fileName)
            else:
                self.saveTemplate('Pre-QUES', fileName)
                fileSaved = True
            
            self.loadTemplateFiles()
            
            # Load the newly saved template file
            if fileSaved:
                self.handlerLoadPreQUESTemplate(fileName)
    

    #***********************************************************
    # 'QUES-C' tab QPushButton handlers
    #***********************************************************
    def handlerLoadQUESCTemplate(self, fileName=None):
        """Slot method for loading a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.comboBoxQUESCTemplate.currentText()
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
            self.loadTemplate('QUES-C', templateFile)
    
    
    def handlerSaveQUESCTemplate(self, fileName=None):
        """Slot method for saving a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.currentQUESCTemplate
        
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
            self.saveTemplate('QUES-C', templateFile)
            return True
        else:
            return False
    
    
    def handlerSaveAsQUESCTemplate(self):
        """Slot method for saving a module template to a new file.
        """
        fileName, ok = QtGui.QInputDialog.getText(self, 'Save As', 'Enter a new template name:')
        fileSaved = False
        
        if ok:
            now = QtCore.QDateTime.currentDateTime().toString('yyyyMMdd-hhmmss')
            fileName = now + '__' + fileName + '.ini'
            
            if os.path.exists(os.path.join(self.settingsPath, fileName)):
                fileSaved = self.handlerSaveQUESCTemplate(fileName)
            else:
                self.saveTemplate('QUES-C', fileName)
                fileSaved = True
            
            self.loadTemplateFiles()
            
            # Load the newly saved template file
            if fileSaved:
                self.handlerLoadQUESCTemplate(fileName)
    
    
    #***********************************************************
    # 'QUES-B' tab QPushButton handlers
    #***********************************************************
    def handlerLoadQUESBTemplate(self, fileName=None):
        """Slot method for loading a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.comboBoxQUESBTemplate.currentText()
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
            self.loadTemplate('QUES-B', templateFile)
    
    
    def handlerSaveQUESBTemplate(self, fileName=None):
        """Slot method for saving a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.currentQUESBTemplate
        
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
            self.saveTemplate('QUES-B', templateFile)
            return True
        else:
            return False
    
  
    def handlerSaveAsQUESBTemplate(self):
        """Slot method for saving a module template to a new file.
        """
        fileName, ok = QtGui.QInputDialog.getText(self, 'Save As', 'Enter a new template name:')
        fileSaved = False
        
        if ok:
            now = QtCore.QDateTime.currentDateTime().toString('yyyyMMdd-hhmmss')
            fileName = now + '__' + fileName + '.ini'
            
            if os.path.exists(os.path.join(self.settingsPath, fileName)):
                fileSaved = self.handlerSaveQUESBTemplate(fileName)
            else:
                self.saveTemplate('QUES-B', fileName)
                fileSaved = True
            
            self.loadTemplateFiles()
            
            # Load the newly saved template file
            if fileSaved:
                self.handlerLoadQUESBTemplate(fileName)
                
                
    def handlerLoadHabitatLookupTable(self):
        """Slot method for calling spesific planning unit lookup table and
           populating the reference mapping table from the selected reference data.
        """      
        activeProject = self.main.appSettings['DialogLumensOpenDatabase']['projectFile'].replace(os.path.sep, '/')
        selectedTableHabitat = self.comboBoxTableHabitat.currentText()
        costumTable = 0
        
        outputs = general.runalg(
            'r:toolsgetlut',
            activeProject,
            costumTable,
            selectedTableHabitat,
            None,
        )        
      
        outputKey = 'main_data'
        if outputs and outputKey in outputs:
            if os.path.exists(outputs[outputKey]):
                with open(outputs[outputKey], 'rb') as f:
                    reader = csv.reader(f)
                    next(reader)
                    
                    fields = ['ID', 'Focal area', 'Selection']
                        
                    self.tableHabitat.setColumnCount(len(fields))
                    self.tableHabitat.setHorizontalHeaderLabels(fields)
                        
                    tableHabitat = []
    
                    for row in reader:
                        dataRow = [QtGui.QTableWidgetItem(field) for field in row]
                        tableHabitat.append(dataRow)
                        
                    self.tableHabitat.setRowCount(len(tableHabitat))
                    
                    tableRow = 0
                    columnEnabled = 0
                    
                    for dataRow in tableHabitat:
                        tableColumn = 0
                        for fieldTableItem in dataRow:
                            fieldTableItem.setFlags(fieldTableItem.flags() & ~QtCore.Qt.ItemIsEnabled)
                            self.tableHabitat.setItem(tableRow, tableColumn, fieldTableItem)
                            self.tableHabitat.horizontalHeader().setResizeMode(tableColumn, QtGui.QHeaderView.ResizeToContents)
                            tableColumn += 1
                            
                        # Additional columns ('Enabled')
                        fieldEnabled = QtGui.QTableWidgetItem('Select')
                        fieldEnabled.setFlags(QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                        fieldEnabled.setCheckState(QtCore.Qt.Unchecked)
                        columnEnabled = tableColumn
                        self.tableHabitat.setItem(tableRow, tableColumn, fieldEnabled)
                        self.tableHabitat.horizontalHeader().setResizeMode(columnEnabled, QtGui.QHeaderView.ResizeToContents)
                        
                        tableRow += 1
                    
                    self.tableHabitat.setEnabled(True)    
                    
        
    #***********************************************************
    # 'QUES-H' Hydrological Response Unit Definition tab QPushButton handlers
    #***********************************************************
    def handlerLoadHRUDefinitionTemplate(self, fileName=None):
        """Slot method for loading a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.comboBoxHRUDefinitionTemplate.currentText()
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
            self.loadTemplate('Hydrological Response Unit Definition', templateFile)
    
    
    def handlerSaveHRUDefinitionTemplate(self, fileName=None):
        """Slot method for saving a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.currentHRUDefinitionTemplate
        
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
            self.saveTemplate('Hydrological Response Unit Definition', templateFile)
            return True
        else:
            return False
    
    
    def handlerSaveAsHRUDefinitionTemplate(self):
        """Slot method for saving a module template to a new file.
        """
        fileName, ok = QtGui.QInputDialog.getText(self, 'Save As', 'Enter a new template name:')
        fileSaved = False
        
        if ok:
            now = QtCore.QDateTime.currentDateTime().toString('yyyyMMdd-hhmmss')
            fileName = now + '__' + fileName + '.ini'
            
            if os.path.exists(os.path.join(self.settingsPath, fileName)):
                fileSaved = self.handlerSaveHRUDefinitionTemplate(fileName)
            else:
                self.saveTemplate('Hydrological Response Unit Definition', fileName)
                fileSaved = True
            
            self.loadTemplateFiles()
            
            # Load the newly saved template file
            if fileSaved:
                self.handlerLoadHRUDefinitionTemplate(fileName)
    
    
    def handlerSelectHRULandUseMap(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Use Map', QtCore.QDir.homePath(), 'Land Use Map (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditHRULandUseMap.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectHRUSoilMap(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Soil Map', QtCore.QDir.homePath(), 'Soil Map (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditHRUSoilMap.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectHRUSlopeMap(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Slope Map', QtCore.QDir.homePath(), 'Slope Map (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditHRUSlopeMap.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectHRUSubcatchmentMap(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Subcatchment Map', QtCore.QDir.homePath(), 'Subcatchment Map (*{0})'.format(self.main.appSettings['selectRasterfileExt'])))
        
        if file:
            self.lineEditHRUSubcatchmentMap.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectHRULandUseClassification(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Land Use Classification', QtCore.QDir.homePath(), 'Land Use Classification (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditHRULandUseClassification.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectHRUSoilClassification(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Soil Classification', QtCore.QDir.homePath(), 'Soil Classification (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditHRUSoilClassification.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectHRUSlopeClassification(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Slope Classification', QtCore.QDir.homePath(), 'Slope Classification (*{0})'.format(self.main.appSettings['selectCsvfileExt'])))
        
        if file:
            self.lineEditHRUSlopeClassification.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    #***********************************************************
    # 'QUES-H' Watershed Model Evaluation tab QPushButton handlers
    #***********************************************************
    def handlerLoadWatershedModelEvaluationTemplate(self, fileName=None):
        """Slot method for loading a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.comboBoxWatershedModelEvaluationTemplate.currentText()
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
            self.loadTemplate('Watershed Model Evaluation', templateFile)
    
    
    def handlerSaveWatershedModelEvaluationTemplate(self, fileName=None):
        """Slot method for saving a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.currentWatershedModelEvaluationTemplate
        
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
            self.saveTemplate('Watershed Model Evaluation', templateFile)
            return True
        else:
            return False
    
    
    def handlerSaveAsWatershedModelEvaluationTemplate(self):
        """Slot method for saving a module template to a new file.
        """
        fileName, ok = QtGui.QInputDialog.getText(self, 'Save As', 'Enter a new template name:')
        fileSaved = False
        
        if ok:
            now = QtCore.QDateTime.currentDateTime().toString('yyyyMMdd-hhmmss')
            fileName = now + '__' + fileName + '.ini'
            
            if os.path.exists(os.path.join(self.settingsPath, fileName)):
                fileSaved = self.handlerSaveWatershedModelEvaluationTemplate(fileName)
            else:
                self.saveTemplate('Watershed Model Evaluation', fileName)
                fileSaved = True
            
            self.loadTemplateFiles()
            
            # Load the newly saved template file
            if fileSaved:
                self.handlerLoadWatershedModelEvaluationTemplate(fileName)
    
    
    def handlerSelectWatershedModelEvaluationObservedDebitFile(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Observed Debit File', QtCore.QDir.homePath(), 'Observed Debit File (*{0})'.format(self.main.appSettings['selectDatabasefileExt'])))
        
        if file:
            self.lineEditWatershedModelEvaluationObservedDebitFile.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectOutputWatershedModelEvaluation(self):
        """Slot method for a file select dialog.
        """
        outputfile = unicode(QtGui.QFileDialog.getSaveFileName(
            self, 'Create/Select Watershed Model Evaluation Output', QtCore.QDir.homePath(), 'Watershed Model Evaluation (*{0})'.format(self.main.appSettings['selectDatabasefileExt'])))
        
        if outputfile:
            self.lineEditOutputWatershedModelEvaluation.setText(outputfile)
            logging.getLogger(type(self).__name__).info('select output file: %s', outputfile)
    
    
    #***********************************************************
    # 'QUES-H' Watershed Indicators tab QPushButton handlers
    #***********************************************************
    def handlerLoadWatershedIndicatorsTemplate(self, fileName=None):
        """Slot method for loading a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.comboBoxWatershedIndicatorsTemplate.currentText()
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
            self.loadTemplate('Watershed Indicators', templateFile)
    
    
    def handlerSaveWatershedIndicatorsTemplate(self, fileName=None):
        """Slot method for saving a module template.
        
        Args:
            fileName (str): the file name of the module template.
        """
        templateFile = self.currentWatershedIndicatorsTemplate
        
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
            self.saveTemplate('Watershed Indicators', templateFile)
            return True
        else:
            return False
    
    
    def handlerSaveAsWatershedIndicatorsTemplate(self):
        """Slot method for saving a module template to a new file.
        """
        fileName, ok = QtGui.QInputDialog.getText(self, 'Save As', 'Enter a new template name:')
        fileSaved = False
        
        if ok:
            now = QtCore.QDateTime.currentDateTime().toString('yyyyMMdd-hhmmss')
            fileName = now + '__' + fileName + '.ini'
            
            if os.path.exists(os.path.join(self.settingsPath, fileName)):
                fileSaved = self.handlerSaveWatershedIndicatorsTemplate(fileName)
            else:
                self.saveTemplate('Watershed Indicators', fileName)
                fileSaved = True
            
            self.loadTemplateFiles()
            
            # Load the newly saved template file
            if fileSaved:
                self.handlerLoadWatershedIndicatorsTemplate(fileName)
    
    
    def handlerSelectWatershedIndicatorsSWATTXTINOUTDir(self):
        """Slot method for a directory select dialog.
        """
        dir = unicode(QtGui.QFileDialog.getExistingDirectory(self, 'Select SWAT TXTINOUT Directory'))
        
        if dir:
            self.lineEditWatershedIndicatorsSWATTXTINOUTDir.setText(dir)
            logging.getLogger(type(self).__name__).info('select directory: %s', dir)
    
    
    def handlerSelectWatershedIndicatorsSubWatershedPolygon(self):
        """Slot method for a file select dialog.
        """
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Sub Watershed Polygon', QtCore.QDir.homePath(), 'Sub Watershed Polygon (*{0})'.format(self.main.appSettings['selectShapefileExt'])))
        
        if file:
            self.lineEditWatershedIndicatorsSubWatershedPolygon.setText(file)
            logging.getLogger(type(self).__name__).info('select file: %s', file)
    
    
    def handlerSelectWatershedIndicatorsOutputInitialYearSubWatershedLevelIndicators(self):
        """Slot method for a file select dialog.
        """
        outputfile = unicode(QtGui.QFileDialog.getSaveFileName(
            self, 'Create/Select Initial Year Sub Watershed Level Indicators Output', QtCore.QDir.homePath(), 'Initial Year Sub Watershed Level Indicators (*{0})'.format(self.main.appSettings['selectDatabasefileExt'])))
        
        if outputfile:
            self.lineEditWatershedIndicatorsOutputInitialYearSubWatershedLevelIndicators.setText(outputfile)
            logging.getLogger(type(self).__name__).info('select output file: %s', outputfile)
    
    
    def handlerSelectWatershedIndicatorsOutputFinalYearSubWatershedLevelIndicators(self):
        """Slot method for a file select dialog.
        """
        outputfile = unicode(QtGui.QFileDialog.getSaveFileName(
            self, 'Create/Select Final Year Sub Watershed Level Indicators Output', QtCore.QDir.homePath(), 'Final Year Sub Watershed Level Indicators (*{0})'.format(self.main.appSettings['selectDatabasefileExt'])))
        
        if outputfile:
            self.lineEditWatershedIndicatorsOutputFinalYearSubWatershedLevelIndicators.setText(outputfile)
            logging.getLogger(type(self).__name__).info('select output file: %s', outputfile)
    
    
    #***********************************************************
    # Process tabs
    #***********************************************************
    def setAppSettings(self):
        """Set the required values from the form widgets.
        """
        # 'Pre-QUES' tab fields
        self.main.appSettings['DialogLumensPreQUESLandcoverTrajectoriesAnalysis']['landUse1'] \
            = unicode(self.comboBoxPreQUESLandCoverLandUse1.currentText())
        self.main.appSettings['DialogLumensPreQUESLandcoverTrajectoriesAnalysis']['landUse2'] \
            = unicode(self.comboBoxPreQUESLandCoverLandUse2.currentText())
        self.main.appSettings['DialogLumensPreQUESLandcoverTrajectoriesAnalysis']['landUseTable'] \
            = unicode(self.comboBoxPreQUESLandCoverTable.currentText())
        self.main.appSettings['DialogLumensPreQUESLandcoverTrajectoriesAnalysis']['planningUnit'] \
            = unicode(self.comboBoxPreQUESLandCoverPlanningUnit.currentText())
        analysisOption = unicode(self.comboBoxLandCoverAnalysisOption.currentText())
        if analysisOption == 'All analysis':
            analysisOption = 0
        elif analysisOption == 'Dominant land use change':
            analysisOption = 1
        elif analysisOption == 'Land use change dynamics':
            analysisOption = 2
        else:
            analysisOption = 3
        self.main.appSettings['DialogLumensPreQUESLandcoverTrajectoriesAnalysis']['analysisOption'] \
            = analysisOption
        self.main.appSettings['DialogLumensPreQUESLandcoverTrajectoriesAnalysis']['nodata'] \
            = self.spinBoxPreQUESNodata.value()
        
        # 'QUES-C' Carbon Accounting groupbox fields
        self.main.appSettings['DialogLumensQUESCCarbonAccounting']['landUse1'] \
            = unicode(self.comboBoxCALandCoverLandUse1.currentText())
        self.main.appSettings['DialogLumensQUESCCarbonAccounting']['landUse2'] \
            = unicode(self.comboBoxCALandCoverLandUse2.currentText())
        self.main.appSettings['DialogLumensQUESCCarbonAccounting']['carbonTable'] \
            = unicode(self.comboBoxCACarbonTable.currentText())
        self.main.appSettings['DialogLumensQUESCCarbonAccounting']['planningUnit'] \
            = unicode(self.comboBoxCALandCoverPlanningUnit.currentText())
        self.main.appSettings['DialogLumensQUESCCarbonAccounting']['nodata'] \
            = self.spinBoxCANoDataValue.value()
        # self.main.appSettings['DialogLumensQUESCCarbonAccounting']['includePeat'] \
        #     = self.checkBoxPeatlandCarbonAccounting.value()            
        # self.main.appSettings['DialogLumensQUESCCarbonAccounting']['peat'] \
        #     = self.comboBoxPeatlandMap.currentText()
        # self.main.appSettings['DialogLumensQUESCCarbonAccounting']['peatTable'] \
        #     = self.comboBoxPCACsvfile.currentText()            
        
        # 'QUES-C' Peatland Carbon Accounting groupbox fields
        # self.main.appSettings['DialogLumensQUESCPeatlandCarbonAccounting']['csvfile'] = unicode(self.lineEditPCACsvfile.text())
        
        # 'QUES-C' Summarize Multiple Period groupbox fields
        # self.main.appSettings['DialogLumensQUESCSummarizeMultiplePeriod'][''] \ = None
        
        # 'QUES-B' tab fields
        self.main.appSettings['DialogLumensQUESBAnalysis']['landUse1'] \
            = unicode(self.comboBoxQUESBLandCoverLandUse1.currentText())
        self.main.appSettings['DialogLumensQUESBAnalysis']['landUse2'] \
            = unicode(self.comboBoxQUESBLandCoverLandUse2.currentText())
        self.main.appSettings['DialogLumensQUESBAnalysis']['landUse3'] \
            = unicode(self.comboBoxQUESBLandCoverLandUse3.currentText())
        self.main.appSettings['DialogLumensQUESBAnalysis']['planningUnit'] \
            = unicode(self.comboBoxQUESBPlanningUnit.currentText())
        self.main.appSettings['DialogLumensQUESBAnalysis']['nodata'] \
            = self.spinBoxQUESBNodata.value()
        self.main.appSettings['DialogLumensQUESBAnalysis']['edgeContrast'] \
            = unicode(self.comboBoxQUESBEdgeContrast.currentText())
        # self.main.appSettings['DialogLumensQUESBAnalysis']['habitatLookup'] \
        #     = unicode(self.comboBoxQUESBHabitat.currentText())            
        WindowShapeOptions = unicode(self.comboBoxQUESBWindowShapeOptions.currentText())
        if WindowShapeOptions == 'Square':
            WindowShapeOptions = 0
        else:
            WindowShapeOptions = 1    
        self.main.appSettings['DialogLumensQUESBAnalysis']['windowShape'] \
            = WindowShapeOptions
        self.main.appSettings['DialogLumensQUESBAnalysis']['samplingWindowSize'] \
            = self.spinBoxQUESBSamplingWindowSize.value()            
        self.main.appSettings['DialogLumensQUESBAnalysis']['samplingGridRes'] \
            = self.spinBoxQUESBSamplingGridRes.value()
        
        # 'QUES-H' Hydrological Response Unit Definition sub tab fields
        self.main.appSettings['DialogLumensQUESHDominantHRU']['landUseMap'] \
            = self.main.appSettings['DialogLumensQUESHDominantLUSSL']['LandUseMap'] \
            = self.main.appSettings['DialogLumensQUESHMultipleHRU']['landUseMap'] \
            = unicode(self.lineEditHRULandUseMap.text())
        self.main.appSettings['DialogLumensQUESHDominantHRU']['soilMap'] \
            = self.main.appSettings['DialogLumensQUESHDominantLUSSL']['soilMap'] \
            = self.main.appSettings['DialogLumensQUESHMultipleHRU']['soilMap'] \
            = unicode(self.lineEditHRUSoilMap.text())
        self.main.appSettings['DialogLumensQUESHDominantHRU']['slopeMap'] \
            = self.main.appSettings['DialogLumensQUESHDominantLUSSL']['slopeMap'] \
            = self.main.appSettings['DialogLumensQUESHMultipleHRU']['slopeMap'] \
            = unicode(self.lineEditHRUSlopeMap.text())
        self.main.appSettings['DialogLumensQUESHDominantHRU']['subcatchmentMap'] \
            = self.main.appSettings['DialogLumensQUESHDominantLUSSL']['subcatchmentMap'] \
            = self.main.appSettings['DialogLumensQUESHMultipleHRU']['subcatchmentMap'] \
            = unicode(self.lineEditHRUSubcatchmentMap.text())
        self.main.appSettings['DialogLumensQUESHDominantHRU']['landUseClassification'] \
            = self.main.appSettings['DialogLumensQUESHDominantLUSSL']['landUseClassification'] \
            = self.main.appSettings['DialogLumensQUESHMultipleHRU']['landUseClassification'] \
            = unicode(self.lineEditHRULandUseClassification.text())
        self.main.appSettings['DialogLumensQUESHDominantHRU']['soilClassification'] \
            = self.main.appSettings['DialogLumensQUESHDominantLUSSL']['soilClassification'] \
            = self.main.appSettings['DialogLumensQUESHMultipleHRU']['soilClassification'] \
            = unicode(self.lineEditHRUSoilClassification.text())
        self.main.appSettings['DialogLumensQUESHDominantHRU']['slopeClassification'] \
            = self.main.appSettings['DialogLumensQUESHDominantLUSSL']['slopeClassification'] \
            = self.main.appSettings['DialogLumensQUESHMultipleHRU']['slopeClassification'] \
            = unicode(self.lineEditHRUSlopeClassification.text())
        self.main.appSettings['DialogLumensQUESHDominantHRU']['areaName'] \
            = self.main.appSettings['DialogLumensQUESHDominantLUSSL']['areaName'] \
            = self.main.appSettings['DialogLumensQUESHMultipleHRU']['areaName'] \
            = unicode(self.lineEditHRUAreaName.text())
        self.main.appSettings['DialogLumensQUESHDominantHRU']['period'] \
            = self.main.appSettings['DialogLumensQUESHDominantLUSSL']['period'] \
            = self.main.appSettings['DialogLumensQUESHMultipleHRU']['period'] \
            = self.spinBoxHRUPeriod.value()
        self.main.appSettings['DialogLumensQUESHMultipleHRU']['landUseThreshold'] \
            = self.spinBoxMultipleHRULandUseThreshold.value()
        self.main.appSettings['DialogLumensQUESHMultipleHRU']['soilThreshold'] \
            = self.spinBoxMultipleHRUSoilThreshold.value()
        self.main.appSettings['DialogLumensQUESHMultipleHRU']['slopeThreshold'] \
            = self.spinBoxMultipleHRUSlopeThreshold.value()
        
        # 'QUES-H' Watershed Model Evaluation sub tab fields
        self.main.appSettings['DialogLumensQUESHWatershedModelEvaluation']['dateInitial'] = self.dateWatershedIndicatorsDateInitial.date().toString('dd/MM/yyyy')
        self.main.appSettings['DialogLumensQUESHWatershedModelEvaluation']['dateFinal'] = self.dateWatershedModelEvaluationDateFinal.date().toString('dd/MM/yyyy')
        self.main.appSettings['DialogLumensQUESHWatershedModelEvaluation']['SWATModel'] = self.comboBoxWatershedModelEvaluationSWATModel.itemData(self.comboBoxWatershedModelEvaluationSWATModel.currentIndex())
        self.main.appSettings['DialogLumensQUESHWatershedModelEvaluation']['location'] = unicode(self.lineEditWatershedModelEvaluationLocation.text())
        self.main.appSettings['DialogLumensQUESHWatershedModelEvaluation']['outletReachSubBasinID'] = self.spinBoxWatershedModelEvaluationOutletReachSubBasinID.value()
        self.main.appSettings['DialogLumensQUESHWatershedModelEvaluation']['observedDebitFile'] = unicode(self.lineEditWatershedModelEvaluationObservedDebitFile.text())
        
        outputWatershedModelEvaluation = unicode(self.lineEditOutputWatershedModelEvaluation.text())
        
        if not outputWatershedModelEvaluation:
            outputWatershedModelEvaluation = '__UNSET__'
        
        self.main.appSettings['DialogLumensQUESHWatershedModelEvaluation']['outputWatershedModelEvaluation'] = outputWatershedModelEvaluation
        
        # 'QUES-H' Watershed Indicators sub tab fields
        self.main.appSettings['DialogLumensQUESHWatershedIndicators']['SWATTXTINOUTDir'] = unicode(self.lineEditWatershedIndicatorsSWATTXTINOUTDir.text()).replace(os.path.sep, '/')
        self.main.appSettings['DialogLumensQUESHWatershedIndicators']['dateInitial'] = self.dateWatershedIndicatorsDateInitial.date().toString('dd/MM/yyyy')
        self.main.appSettings['DialogLumensQUESHWatershedIndicators']['dateFinal'] = self.dateWatershedIndicatorsDateFinal.date().toString('dd/MM/yyyy')
        self.main.appSettings['DialogLumensQUESHWatershedIndicators']['subWatershedPolygon'] = unicode(self.lineEditWatershedIndicatorsSubWatershedPolygon.text())
        self.main.appSettings['DialogLumensQUESHWatershedIndicators']['location'] = unicode(self.lineEditWatershedIndicatorsLocation.text())
        self.main.appSettings['DialogLumensQUESHWatershedIndicators']['subWatershedOutput'] = self.spinBoxWatershedIndicatorsSubWatershedOutput.value()
        
        outputInitialYearSubWatershedLevelIndicators = unicode(self.lineEditWatershedIndicatorsOutputInitialYearSubWatershedLevelIndicators.text())
        outputFinalYearSubWatershedLevelIndicators = unicode(self.lineEditWatershedIndicatorsOutputFinalYearSubWatershedLevelIndicators.text())
        
        if not outputInitialYearSubWatershedLevelIndicators:
            outputInitialYearSubWatershedLevelIndicators = '__UNSET__'
        
        if not outputFinalYearSubWatershedLevelIndicators:
            outputFinalYearSubWatershedLevelIndicators = '__UNSET__'
        
        self.main.appSettings['DialogLumensQUESHWatershedIndicators']['outputInitialYearSubWatershedLevelIndicators'] = outputInitialYearSubWatershedLevelIndicators
        self.main.appSettings['DialogLumensQUESHWatershedIndicators']['outputFinalYearSubWatershedLevelIndicators'] = outputFinalYearSubWatershedLevelIndicators
    
    
    def handlerProcessPreQUES(self):
        """Slot method to pass the form values and execute the "PreQUES" R algorithms.
        
        The "PreQUES" process calls the following algorithms:
        1. r:quespre
        """
        self.setAppSettings()
        
        formName = 'DialogLumensPreQUESLandcoverTrajectoriesAnalysis'
        algName = 'r:quespre'
        activeProject = self.main.appSettings['DialogLumensOpenDatabase']['projectFile'].replace(os.path.sep, '/')
        
        if self.validForm(formName):
            logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
            logging.getLogger(self.historyLog).info('alg start: %s' % formName)
            self.buttonProcessPreQUES.setDisabled(True)
            
            # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
            # self.main.setWindowState(QtCore.Qt.WindowMinimized)
            
            outputs = general.runalg(
                algName,
                activeProject,
                self.main.appSettings[formName]['landUse1'],
                self.main.appSettings[formName]['landUse2'],
                self.main.appSettings[formName]['planningUnit'],
                self.main.appSettings[formName]['landUseTable'],
                self.main.appSettings[formName]['analysisOption'],
                self.main.appSettings[formName]['nodata'],
                None, # statusoutput
            )
            
            # Display ROut file in debug mode
            if self.main.appSettings['debug']:
                dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                dialog.exec_()
            
            ##print outputs
            
            # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
            # self.main.setWindowState(QtCore.Qt.WindowActive)
            
            algSuccess = self.outputsMessageBox(algName, outputs, '', '')

            if algSuccess:
                self.main.loadAddedDataInfo()
            
            self.buttonProcessPreQUES.setEnabled(True)
            logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
            logging.getLogger(self.historyLog).info('alg end: %s' % formName)
    
    
    def handlerProcessQUESC(self):
        """Slot method to pass the form values and execute the "QUES-C" R algorithms.
        
        Depending on the checked groupbox, the "QUES-C" process calls the following algorithms:
        1. r:quescarbon
        2. r:summarizemultipleperiode
        """
        self.setAppSettings()
        activeProject = self.main.appSettings['DialogLumensOpenDatabase']['projectFile'].replace(os.path.sep, '/')
        
        if self.checkBoxCarbonAccounting.isChecked():
            formName = 'DialogLumensQUESCCarbonAccounting'
            algName = 'r:quescarbon'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                logging.getLogger(self.historyLog).info('alg start: %s' % formName)
                self.buttonProcessQUESC.setDisabled(True)
                
                # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                # self.main.setWindowState(QtCore.Qt.WindowMinimized)
                
                outputs = general.runalg(
                    algName,
                    activeProject,
                    self.main.appSettings[formName]['landUse1'],
                    self.main.appSettings[formName]['landUse2'],
                    self.main.appSettings[formName]['planningUnit'],
                    self.main.appSettings[formName]['carbonTable'],
                    self.main.appSettings[formName]['nodata'],
                    None,
                    None,
                )
                
                # Display ROut file in debug mode
                if self.main.appSettings['debug']:
                    dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                    dialog.exec_()
                
                ##print outputs
                
                # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
                # self.main.setWindowState(QtCore.Qt.WindowActive)
                
                algSuccess = self.outputsMessageBox(algName, outputs, '', '')

                if algSuccess:
                    self.main.loadAddedDataInfo()
                    outputKey = 'resultoutput'
                    if outputs and outputKey in outputs:
                        if os.path.exists(outputs[outputKey]):
                            with open(outputs[outputKey], 'rb') as f:
                                reader = csv.reader(f)
                                next(reader)
                                for path in reader:
                                    print path[0]
                                    self.main.addLayer(path[0])

                self.buttonProcessQUESC.setEnabled(True)
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
                logging.getLogger(self.historyLog).info('alg end: %s' % formName)


        if self.checkBoxPeatlandCarbonAccounting.isChecked():
            pass
          
        
        if self.checkBoxSummarizeMultiplePeriod.isChecked():
            if len(self.listOfQUESCDatabase) > 1:
                formName = 'DialogLumensQUESCSummarizeMultiplePeriod'
                algName = 'r:quessummarizeperiods'

                self.listOfQUESCDatabase.sort()
                QUESCDatabaseCsv = self.writeListCsv(self.listOfQUESCDatabase, True)

                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                logging.getLogger(self.historyLog).info('alg start: %s' % formName)
                self.buttonProcessQUESC.setDisabled(True)

                # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                # self.main.setWindowState(QtCore.Qt.WindowMinimized)

                outputs = general.runalg(
                    algName,
                    activeProject,
                    QUESCDatabaseCsv,
                    None,
                )

                # Display ROut file in debug mode
                if self.main.appSettings['debug']:
                    dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                    dialog.exec_()

                ##print outputs

                # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
                # self.main.setWindowState(QtCore.Qt.WindowActive)

                algSuccess = self.outputsMessageBox(algName, outputs, '', '')

                if algSuccess:
                    self.main.loadAddedDataInfo()

                self.buttonProcessQUESC.setEnabled(True)
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
                logging.getLogger(self.historyLog).info('alg end: %s' % formName)
            else:
                QtGui.QMessageBox.information(self, 'Summarize Multiple Period', 'Choose at least two QUES-C Database.')
                return
    
    
    def handlerProcessQUESB(self):
        """Slot method to pass the form values and execute the "QUES-B" R algorithm.
        
        The "QUES-B" process calls the following algorithm:
        1. r:quesbiodiv
        """
        self.setAppSettings()
        
        formName = 'DialogLumensQUESBAnalysis'
        algName = 'r:quesbiodiv'
        activeProject = self.main.appSettings['DialogLumensOpenDatabase']['projectFile'].replace(os.path.sep, '/')
        checkedEnabled = []
        
        numOfRow = self.tableHabitat.rowCount()
        numOfCol = self.tableHabitat.columnCount()
        for i in range(numOfRow):
            if self.tableHabitat.item(i, numOfCol - 1).checkState() == QtCore.Qt.Checked:
                checkedEnabled.append(self.tableHabitat.item(i, 0).text())
        
        if len(checkedEnabled) > 0:
            checkedEnabled.sort()
            checkedEnabledCsv = self.writeListCsv(checkedEnabled, True)
          
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                logging.getLogger(self.historyLog).info('alg start: %s' % formName)
                self.buttonProcessQUESB.setDisabled(True)
                
                # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                # self.main.setWindowState(QtCore.Qt.WindowMinimized)
                
                outputs = general.runalg(
                    algName,
                    activeProject,
                    self.main.appSettings[formName]['landUse1'],
                    self.main.appSettings[formName]['landUse2'],
                    self.main.appSettings[formName]['landUse3'],
                    self.main.appSettings[formName]['planningUnit'],
                    self.main.appSettings[formName]['nodata'],
                    checkedEnabledCsv,
                    self.main.appSettings[formName]['edgeContrast'],
                    self.main.appSettings[formName]['windowShape'],
                    self.main.appSettings[formName]['samplingWindowSize'],
                    self.main.appSettings[formName]['samplingGridRes'],
                    None,
                    None,
                )
                
                # Display ROut file in debug mode
                if self.main.appSettings['debug']:
                    dialog = DialogLumensViewer(self, 'DEBUG "{0}" ({1})'.format(algName, 'processing_script.r.Rout'), 'text', self.main.appSettings['ROutFile'])
                    dialog.exec_()
                
                ##print outputs
                
                # WORKAROUND: once MessageBarProgress is done, activate LUMENS window again
                # self.main.setWindowState(QtCore.Qt.WindowActive)
                
                algSuccess = self.outputsMessageBox(algName, outputs, '', '')
    
                if algSuccess:
                    self.main.loadAddedDataInfo()
                    outputKey = 'resultoutput'
                    if outputs and outputKey in outputs:
                        if os.path.exists(outputs[outputKey]):
                            with open(outputs[outputKey], 'rb') as f:
                                reader = csv.reader(f)
                                next(reader)
                                for path in reader:
                                    print path[0]
                                    self.main.addLayer(path[0])
                
                self.buttonProcessQUESB.setEnabled(True)
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
                logging.getLogger(self.historyLog).info('alg end: %s' % formName)
        else:
            QtGui.QMessageBox.information(self, self.dialogTitle, 'Please select focal area.')
            return
          
    
    def handlerProcessQUESHHRUDefinition(self):
        """Slot method to pass the form values and execute the "QUES-H HRU Definition" R algorithms.
        
        Depending on the checked groupbox, the "QUES-H HRU Definition" process calls the following algorithms:
        1. modeler:ques-h_dhru
        2. modeler:ques-h_dlussl
        3. modeler:ques-h_mhru
        """
        self.setAppSettings()
        
        if self.checkBoxDominantHRU.isChecked():
            formName = 'DialogLumensQUESHDominantHRU'
            algName = 'modeler:ques-h_dhru'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                logging.getLogger(self.historyLog).info('alg start: %s' % formName)
                self.buttonProcessHRUDefinition.setDisabled(True)
                
                # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                self.main.setWindowState(QtCore.Qt.WindowMinimized)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['landUseMap'],
                    self.main.appSettings[formName]['soilMap'],
                    self.main.appSettings[formName]['slopeMap'],
                    self.main.appSettings[formName]['subcatchmentMap'],
                    self.main.appSettings[formName]['landUseClassification'],
                    self.main.appSettings[formName]['soilClassification'],
                    self.main.appSettings[formName]['slopeClassification'],
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
                
                algSuccess = self.outputsMessageBox(algName, outputs, '', '')

                if algSuccess:
                    self.main.loadAddedDataInfo()
                
                self.buttonProcessHRUDefinition.setEnabled(True)
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
                logging.getLogger(self.historyLog).info('alg end: %s' % formName)
        
        if self.checkBoxDominantLUSSL.isChecked():
            formName = 'DialogLumensQUESHDominantLUSSL'
            algName = 'modeler:ques-h_dlussl'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                logging.getLogger(self.historyLog).info('alg start: %s' % formName)
                self.buttonProcessHRUDefinition.setDisabled(True)
                
                # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                self.main.setWindowState(QtCore.Qt.WindowMinimized)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['landUseMap'],
                    self.main.appSettings[formName]['soilMap'],
                    self.main.appSettings[formName]['slopeMap'],
                    self.main.appSettings[formName]['subcatchmentMap'],
                    self.main.appSettings[formName]['landUseClassification'],
                    self.main.appSettings[formName]['soilClassification'],
                    self.main.appSettings[formName]['slopeClassification'],
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
                
                algSuccess = self.outputsMessageBox(algName, outputs, '', '')

                if algSuccess:
                    self.main.loadAddedDataInfo()
                
                self.buttonProcessHRUDefinition.setEnabled(True)
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
                logging.getLogger(self.historyLog).info('alg end: %s' % formName)
        
        if self.checkBoxMultipleHRU.isChecked():
            formName = 'DialogLumensQUESHMultipleHRU'
            algName = 'modeler:ques-h_mhru'
            
            if self.validForm(formName):
                logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
                logging.getLogger(self.historyLog).info('alg start: %s' % formName)
                self.buttonProcessHRUDefinition.setDisabled(True)
                
                # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
                self.main.setWindowState(QtCore.Qt.WindowMinimized)
                
                outputs = general.runalg(
                    algName,
                    self.main.appSettings[formName]['landUseMap'],
                    self.main.appSettings[formName]['soilMap'],
                    self.main.appSettings[formName]['slopeMap'],
                    self.main.appSettings[formName]['subcatchmentMap'],
                    self.main.appSettings[formName]['landUseClassification'],
                    self.main.appSettings[formName]['soilClassification'],
                    self.main.appSettings[formName]['slopeClassification'],
                    self.main.appSettings[formName]['areaName'],
                    self.main.appSettings[formName]['period'],
                    self.main.appSettings[formName]['landUseThreshold'],
                    self.main.appSettings[formName]['soilThreshold'],
                    self.main.appSettings[formName]['slopeThreshold'],
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
                
                self.buttonProcessHRUDefinition.setEnabled(True)
                logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
                logging.getLogger(self.historyLog).info('alg end: %s' % formName)
    
    
    def handlerProcessQUESHWatershedModelEvaluation(self):
        """Slot method to pass the form values and execute the "QUES-H Watershed Model Evaluation" R algorithm.
        
        The "QUES-H Watershed Model Evaluation" process calls the following algorithm:
        1. modeler:ques-h_watershed_model_evaluation
        """
        self.setAppSettings()
        
        formName = 'DialogLumensQUESHWatershedModelEvaluation'
        algName = 'modeler:ques-h_watershed_model_evaluation'
        
        if self.validForm(formName):
            logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
            logging.getLogger(self.historyLog).info('alg start: %s' % formName)
            self.buttonProcessWatershedModelEvaluation.setDisabled(True)
            
            outputWatershedModelEvaluation = self.main.appSettings[formName]['outputWatershedModelEvaluation']
            
            if outputWatershedModelEvaluation == '__UNSET__':
                outputWatershedModelEvaluation = None
            
            # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
            self.main.setWindowState(QtCore.Qt.WindowMinimized)
            
            outputs = general.runalg(
                algName,
                self.main.appSettings[formName]['period1'],
                self.main.appSettings[formName]['period2'],
                self.main.appSettings[formName]['SWATModel'],
                self.main.appSettings[formName]['location'],
                self.main.appSettings[formName]['outletReachSubBasinID'],
                self.main.appSettings[formName]['observedDebitFile'],
                outputWatershedModelEvaluation,
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
            
            self.buttonProcessWatershedModelEvaluation.setEnabled(True)
            logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
            logging.getLogger(self.historyLog).info('alg end: %s' % formName)
    
    
    def handlerProcessQUESHWatershedIndicators(self):
        """Slot method to pass the form values and execute the "QUES-H Watershed Indicators" R algorithm.
        
        The "QUES-H Watershed Indicators" process calls the following algorithm:
        1. modeler:ques-h_watershed_indicators
        """
        self.setAppSettings()
        
        formName = 'DialogLumensQUESHWatershedIndicators'
        algName = 'modeler:ques-h_watershed_indicators'
        
        if self.validForm(formName):
            logging.getLogger(type(self).__name__).info('alg start: %s' % formName)
            logging.getLogger(self.historyLog).info('alg start: %s' % formName)
            self.buttonProcessWatershedIndicators.setDisabled(True)
            
            outputInitialYearSubWatershedLevelIndicators = self.main.appSettings[formName]['outputInitialYearSubWatershedLevelIndicators']
            outputFinalYearSubWatershedLevelIndicators = self.main.appSettings[formName]['outputFinalYearSubWatershedLevelIndicators']
            
            if outputInitialYearSubWatershedLevelIndicators == '__UNSET__':
                outputInitialYearSubWatershedLevelIndicators = None
            
            if outputFinalYearSubWatershedLevelIndicators == '__UNSET__':
                outputFinalYearSubWatershedLevelIndicators = None
            
            # WORKAROUND: minimize LUMENS so MessageBarProgress does not show under LUMENS
            self.main.setWindowState(QtCore.Qt.WindowMinimized)
            
            outputs = general.runalg(
                algName,
                self.main.appSettings[formName]['SWATTXTINOUTDir'],
                self.main.appSettings[formName]['dateInitial'],
                self.main.appSettings[formName]['dateFinal'],
                self.main.appSettings[formName]['subWatershedPolygon'],
                self.main.appSettings[formName]['location'],
                self.main.appSettings[formName]['subWatershedOutput'],
                outputInitialYearSubWatershedLevelIndicators,
                outputFinalYearSubWatershedLevelIndicators,
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
            
            self.buttonProcessWatershedIndicators.setEnabled(True)
            logging.getLogger(type(self).__name__).info('alg end: %s' % formName)
            logging.getLogger(self.historyLog).info('alg end: %s' % formName)
    
