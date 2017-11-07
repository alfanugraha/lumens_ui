#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, platform, sys, logging, subprocess, argparse, csv, zipfile, tempfile

from qgis.core import *
from qgis.gui import *
from PyQt4 import QtGui, QtCore, QtXml, QtWebKit

import resource

QgsApplication.setPrefixPath(os.environ['QGIS_PREFIX'], True) # The True value is important
QgsApplication.initQgis()

app = QtGui.QApplication(sys.argv)

splashImage = QtGui.QPixmap('ui/images/splashbw.png')
splashScreen = QtGui.QSplashScreen(splashImage, QtCore.Qt.WindowStaysOnTopHint)
splashScreen.setMask(splashImage.mask())
splashScreen.show()

# Get an iface object
canvas = QgsMapCanvas()
from processing.tests.qgis_interface import QgisInterface
iface = QgisInterface(canvas) # causes ERROR 4

# Initialize the Processing plugin passing an iface object
from processing.ProcessingPlugin import ProcessingPlugin
plugin = ProcessingPlugin(iface)

##import processing
from processing.core.ProcessingConfig import ProcessingConfig
from processing.core.Processing import Processing
ProcessingConfig.setSettingValue('ACTIVATE_R', True) # R provider is not activated by default
ProcessingConfig.setSettingValue('R_FOLDER', os.environ['RPATH'])
ProcessingConfig.setSettingValue('R_LIBS_USER', os.environ['RLIBS'])
ProcessingConfig.setSettingValue('R_SCRIPTS_FOLDER', os.environ['RSCRIPTS'])
ProcessingConfig.setSettingValue('R_USE64', True)
Processing.initialize()
from processing.tools import *

from utils import QPlainTextEditLogger, DetailedMessageBox

# Import LUMENS dialog classes here
from dialog_layer_attribute_dualview import DialogLayerAttributeDualView
from dialog_layer_attribute_table import DialogLayerAttributeTable
from dialog_layer_properties import DialogLayerProperties
from dialog_lumens_viewer import DialogLumensViewer

from dialog_lumens_createdatabase import DialogLumensCreateDatabase
from dialog_lumens_adddata import DialogLumensAddData

from dialog_lumens_pur import DialogLumensPUR
from dialog_lumens_ques import DialogLumensQUES
from dialog_lumens_ta_opportunitycost import DialogLumensTAOpportunityCost
from dialog_lumens_ta_regionaleconomy import DialogLumensTARegionalEconomy
from dialog_lumens_sciendo import DialogLumensSCIENDO


#############################################################################

__version__ = '1.0.0'

class MainWindow(QtGui.QMainWindow):
    """The main window class of LUMENS application.
    
    Attributes:
        openDialogs (list): a list to reference opened dialog windows.
        recentProjects (list): a list of previously opened LUMENS project files.
        qgsLayerList (dict): a dict of QgsVectorLayer and QgsRasterLayer instances in the layer list.
        layerListModel (QStandardItemModel): the model for the layer list on the sidebar.
        dataLandUseCover, dataPlanningUnit, dataFactor, dataTable (dict): info about added data.
    """
    
    def __init__(self, parent=None):
        """Constructor method for initializing the LUMENS main window instance.
        
        Global application settings "appSettings" is declared in this method. The global settings
        holds the input field parameters for each of the module dialogs. LUMENS main window signal
        handlers are also declared here.
        
        Args:
            parent: the main window's parent instance.
        """
        super(MainWindow, self).__init__(parent)
        
        # Default settings for each LUMENS dialog, the class attributes reflect their R algorithm input fields
        self.appSettings = {
            'debug': False,
            'appDir': os.path.dirname(os.path.realpath(__file__)),
            'appSettingsFile': 'settings.ini',
            'ROutFile': os.path.join(system.userFolder(), 'processing_script.r.Rout'),
            'guideFile': 'guide.pdf',
            'helpLUMENSFile': 'index.html',
            'helpDialogPURFile': 'index_pur.html',
            'helpDialogQUESFile': 'index_ques.html',
            'helpDialogTAFile': 'index_ta.html',
            'helpDialogSCIENDOFile': 'index_sciendo.html',
            'dataDir': 'data',
            'basemapDir': 'basemap',
            'vectorDir': 'vector',
            'defaultBasemapFile': 'basemap.tif',
            'defaultBasemapFilePath': '',
            'defaultVectorFile': 'landmarks.shp',
            'defaultVectorFilePath': '',
            'defaultHabitatLookupTable': '',
            'selectQgsProjectfileExt': '.qgs',
            'selectShapefileExt': '.shp',
            'selectRasterfileExt': '.tif',
            'selectCsvfileExt': '.csv',
            'selectProjectfileExt': '.lpj',
            'selectZipfileExt': '.zip',
            'selectDatabasefileExt': '.dbf',
            'selectHTMLfileExt': '.html',
            'selectTextfileExt': '.txt',
            'selectCarfileExt': '.car',
            'defaultExtent': QgsRectangle(95, -11, 140, 11), # Southeast Asia extent
            'defaultCRS': 4326, # EPSG 4326 - WGS 84
            'dataMappingFile': '',
            'folderPUR': 'PUR', # Used for template path
            'folderQUES': 'QUES',
            'folderTA': 'TA',
            'folderSCIENDO': 'SCIENDO',
            'folderHelp': 'help',
            'folderTemp': os.path.join(tempfile.gettempdir(), 'LUMENS'),
            'acceptedDocumentFormats': ('.doc', 'docx', '.rtf', '.xls', '.xlsx', '.txt', '.log', '.csv'),
            'acceptedWebFormats': ('.html', '.htm'),
            'acceptedSpatialFormats': ('.shp', '.tif'),
            
            'DialogFeatureSelectExpression': { # OBSOLETE
                'expression': '',
            },
            'DialogLumensCreateDatabase': {
                'projectName': '',
                'outputFolder': '',
                'shapefile': '',
                'shapefileAttr': '',
                'projectDescription': '',
                'projectLocation': '',
                'projectProvince': '',
                'projectCountry': '',
                'projectSpatialRes': '',
                'dissolvedShapefile': '', # New field
            },
            'DialogLumensOpenDatabase': { # OBSOLETE
                'projectFile': '',
                'projectFolder': '',
            },
            'DialogLumensAddLandcoverRaster': {
                'rasterfile': '',
                'period': '',
                'description': '',
            },
            'DialogLumensAddPeatData': {
                'rasterfile': '',
                'description': '',
            },
            'DialogLumensAddFactorData': {
                'rasterfile': '',
                'description': '',
            },
            'DialogLumensAddPlanningUnitData': {
                'rasterfile': '',
                'csvfile': '',
                'description': '',
            },
            'DialogLumensPUR': {
                'shapefile': '',
                'shapefileAttr': '',
                'dataTitle': '',
                'referenceClasses': '',
                'referenceMapping': '',
                'planningUnits': '',
            },
            'DialogLumensPURCreateReferenceData': {
                'shapefile': '',
                'shapefileAttr': '',
                'dataTitle': '',
            },
            'DialogLumensPURPreparePlanningUnit': {
                'shapefile': '',
                'shapefileAttr': '',
                'planningUnitTitle': '',
                'planningUnitType': '',
            },
            'DialogLumensPURReconcilePlanningUnit': {
                'outputFile': '',
            },
            'DialogLumensPURFinalization': {
                'shapefile': '',
            },
            'DialogLumensPreQUESLandcoverChangeAnalysis': {
                'csvfile': '',
                'option': '',
                'nodata': '',
            },
            'DialogLumensPreQUESLandcoverTrajectoriesAnalysis': {
                'landUse1': '',
                'landUse2': '',
                'planningUnit': '',
                'landUseTable': '',
                'analysisOption': '',
                'nodata': '',
            },
            'DialogLumensQUESCCarbonAccounting': {
                'landUse1': '',
                'landUse2': '',
                'planningUnit': '',
                'carbonTable': '',
                'nodata': '',
            },
            'DialogLumensQUESCPeatlandCarbonAccounting': {
                'csvfile': '',
            },
            'DialogLumensQUESCSummarizeMultiplePeriod': {
                'checkbox': '',
            },
            'DialogLumensQUESBAnalysis': {
                'planningUnit': '',
                'samplingGridRes': '',
                'samplingWindowSize': '',
                'windowShape': '',
                'nodata': '',
                'edgeContrast': '',
                'habitatLookup': '',
            },
            'DialogLumensQUESHWatershedModelEvaluation': {
                'dateInitial': '',
                'dateFinal': '',
                'SWATModel': '',
                'location': '',
                'outletReachSubBasinID': '',
                'observedDebitFile': '',
                'outputWatershedModelEvaluation': '',
            },
            'DialogLumensQUESHWatershedIndicators': {
                'SWATTXTINOUTDir': '',
                'dateInitial': '',
                'dateFinal': '',
                'subWatershedPolygon': '',
                'location': '',
                'subWatershedOutput': '',
                'outputInitialYearSubWatershedLevelIndicators': '',
                'outputFinalYearSubWatershedLevelIndicators': '',
            },
            'DialogLumensQUESHDominantHRU': {
                'landUseMap': '',
                'soilMap': '',
                'slopeMap': '',
                'subcatchmentMap': '',
                'landUseClassification': '',
                'soilClassification': '',
                'slopeClassification': '',
                'areaName': '',
                'period': '',
            },
            'DialogLumensQUESHDominantLUSSL': {
                'landUseMap': '',
                'soilMap': '',
                'slopeMap': '',
                'subcatchmentMap': '',
                'landUseClassification': '',
                'soilClassification': '',
                'slopeClassification': '',
                'areaName': '',
                'period': '',
            },
            'DialogLumensQUESHMultipleHRU': {
                'landUseMap': '',
                'soilMap': '',
                'slopeMap': '',
                'subcatchmentMap': '',
                'landUseClassification': '',
                'soilClassification': '',
                'slopeClassification': '',
                'areaName': '',
                'period': '',
                'landUseThreshold': '',
                'soilThreshold': '',
                'slopeThreshold': '',
            },
            'DialogLumensTAAbacusOpportunityCostCurve': {
                'projectFile': '',
            },
            'DialogLumensTAOpportunityCostCurve': {
                'csvNPVTable': '',
                'costThreshold': '',
                'outputOpportunityCostDatabase': '',
                'outputOpportunityCostReport': '',
            },
            'DialogLumensTAOpportunityCostMap': {
                'csvProfitability': '',
            },
            'DialogLumensTARegionalEconomySingleIODescriptiveAnalysis': {
                'intermediateConsumptionMatrix': '',
                'valueAddedMatrix': '',
                'finalConsumptionMatrix': '',
                'valueAddedComponent': '',
                'finalConsumptionComponent': '',
                'listOfEconomicSector': '',
                'labourRequirement': '',
                'financialUnit': '',
                'areaName': '',
                'period': '',
            },
            'DialogLumensTARegionalEconomyTimeSeriesIODescriptiveAnalysis': {
                'intermediateConsumptionMatrixP1': '',
                'intermediateConsumptionMatrixP2': '',
                'valueAddedMatrixP1': '',
                'valueAddedMatrixP2': '',
                'finalConsumptionMatrixP1': '',
                'finalConsumptionMatrixP2': '',
                'valueAddedComponent': '',
                'finalConsumptionComponent': '',
                'listOfEconomicSector': '',
                'labourRequirementP1': '',
                'labourRequirementP2': '',
                'financialUnit': '',
                'areaName': '',
                'period1': '',
                'period2': '',
            },
            'DialogLumensTARegionalEconomyLandDistributionRequirementAnalysis': {
                'intermediateConsumptionMatrix': '',
                'valueAddedMatrix': '',
                'finalConsumptionMatrix': '',
                'valueAddedComponent': '',
                'finalConsumptionComponent': '',
                'listOfEconomicSector': '',
                'landDistributionMatrix': '',
                'landCoverComponent': '',
                'labourRequirement': '',
                'financialUnit': '',
                'areaName': '',
                'period': '',
            },
            'DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis': {
                'intermediateConsumptionMatrix': '',
                'valueAddedMatrix': '',
                'finalConsumptionMatrix': '',
                'valueAddedComponent': '',
                'finalConsumptionComponent': '',
                'listOfEconomicSector': '',
                'landDistributionMatrix': '',
                'landRequirementCoefficientMatrix': '',
                'landCoverComponent': '',
                'labourRequirement': '',
                'financialUnit': '',
                'areaName': '',
                'period': '',
            },
            'DialogLumensTARegionalEconomyFinalDemandChangeMultiplierAnalysis': {
                'intermediateConsumptionMatrix': '',
                'valueAddedMatrix': '',
                'finalConsumptionMatrix': '',
                'valueAddedComponent': '',
                'finalConsumptionComponent': '',
                'listOfEconomicSector': '',
                'landDistributionMatrix': '',
                'landRequirementCoefficientMatrix': '',
                'landCoverComponent': '',
                'labourRequirement': '',
                'financialUnit': '',
                'areaName': '',
                'period': '',
                'finalDemandChangeScenario': '',
            },
            'DialogLumensTARegionalEconomyGDPChangeMultiplierAnalysis': {
                'intermediateConsumptionMatrix': '',
                'valueAddedMatrix': '',
                'finalConsumptionMatrix': '',
                'valueAddedComponent': '',
                'finalConsumptionComponent': '',
                'listOfEconomicSector': '',
                'landDistributionMatrix': '',
                'landRequirementCoefficientMatrix': '',
                'landCoverComponent': '',
                'labourRequirement': '',
                'gdpChangeScenario': '',
                'financialUnit': '',
                'areaName': '',
                'period': '',
            },
            'DialogLumensSCIENDOHistoricalBaselineProjection': {
                'QUESCDatabase': '',
                'iteration': '',
            },
            'DialogLumensSCIENDOHistoricalBaselineAnnualProjection': {
                'iteration': '',
            },
            'DialogLumensSCIENDODriversAnalysis': {
                'landUseCoverChangeDrivers': '',
                'landUseCoverChangeType': '',
            },
            'DialogLumensSCIENDOBuildScenario': {
                'historicalBaselineCar': '',
            },
            'DialogLumensSCIENDOCalculateTransitionMatrix': {
                'factorsDir': '',
                'landUseLookup': '',
                'baseYear': '',
                'location': '',
            },
            'DialogLumensSCIENDOCreateRasterCube': {
                'factorsDir': '',
                'landUseLookup': '',
                'baseYear': '',
                'location': '',
            },
            'DialogLumensSCIENDOCalculateWeightofEvidence': {
                'factorsDir': '',
                'landUseLookup': '',
                'baseYear': '',
                'location': '',
            },
            'DialogLumensSCIENDOSimulateLandUseChange': {
                'factorsDir': '',
                'landUseLookup': '',
                'baseYear': '',
                'location': '',
            },
            'DialogLumensSCIENDOSimulateWithScenario': {
                'factorsDir': '',
                'landUseLookup': '',
                'baseYear': '',
                'location': '',
            },
            'DialogLumensToolsREDDAbacusSP': { # OBSOLETE
                'carfile': '',
            },
        }
        
        self.appSettings['defaultBasemapFilePath'] = os.path.join(self.appSettings['appDir'], self.appSettings['dataDir'], self.appSettings['basemapDir'], self.appSettings['defaultBasemapFile'])
        self.appSettings['defaultVectorFilePath'] = os.path.join(self.appSettings['appDir'], self.appSettings['dataDir'], self.appSettings['vectorDir'], self.appSettings['defaultVectorFile'])
        
        # For keeping track of open dialogs
        self.openDialogs = []
        
        # Recently opened LUMENS project databases
        self.recentProjects = []
        
        # For keeping track of data added to the project
        self.dataLandUseCover = {}
        self.dataPlanningUnit = {}
        self.dataFactor = {}
        self.dataTable = {}
        
        # Process app arguments
        parser = argparse.ArgumentParser(description="LUMENS (Land Use Planning for Multiple Enviromental Services)")
        parser.add_argument('--debug', action='store_true', help='Show the logging widget')
        parser.add_argument('--lpj', help='Open LUMENS project file')
        
        args = parser.parse_args()
        
        if args.debug:
            self.appSettings['debug'] = True
        
        # Load the app settings
        self.loadSettings()
        
        # Build the mainwindow UI!
        self.setupUi()
        
        if args.debug:
            # Init the logger for mainwindow
            self.logger = logging.getLogger(type(self).__name__)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            fh = logging.FileHandler(os.path.join(self.appSettings['appDir'], 'logs', type(self).__name__ + '.log'))
            fh.setFormatter(formatter)
            self.log_box.setFormatter(formatter)
            self.logger.addHandler(ch)
            self.logger.addHandler(fh)
            self.logger.addHandler(self.log_box)
            self.logger.setLevel(logging.DEBUG)

        self.installEventFilter(self)
        
        # File menu updating
        self.fileMenu.aboutToShow.connect(self.updateFileMenu)
        
        # For holding QgsVectorLayer/QgsRasterLayer objects
        self.qgsLayerList = dict()
        
        # PyQT model+view for layers list
        self.layerListModel = QtGui.QStandardItemModel(self.layerListView)
        ##self.layerListModel.setSupportedDragActions(QtCore.Qt.MoveAction)
        self.layerListView.setModel(self.layerListModel)
        
        self.layerListView.clicked.connect(self.handlerSelectLayer)
        self.layerListModel.itemChanged.connect(self.handlerCheckLayer)
        
        # For checking drop events
        ##self.layerListView.viewport().installEventFilter(self)
        
        # Project treeview doubleclick item handling
        self.projectTreeView.doubleClicked.connect(self.handlerDoubleClickProjectTree)

        if args.lpj:
            self.lumensOpenDatabase(args.lpj)
        
        # App action handlers
        self.actionQuit.triggered.connect(self.close)
        self.actionToggleToolbar.triggered.connect(self.handlerToggleToolbar)
        self.actionToggleDialogToolbar.triggered.connect(self.handlerToggleDialogToolbar)
        self.actionZoomIn.triggered.connect(self.handlerZoomIn)
        self.actionZoomOut.triggered.connect(self.handlerZoomOut)
        self.actionZoomFull.triggered.connect(self.handlerZoomFull)
        self.actionZoomLayer.triggered.connect(self.handlerZoomLayer)
        self.actionZoomSelected.triggered.connect(self.handlerZoomSelected)
        self.actionPanSelected.triggered.connect(self.handlerPanSelected)
        self.actionPan.triggered.connect(self.handlerSetPanMode)
        self.actionSelect.triggered.connect(self.handlerSetSelectMode)
        self.actionInfo.triggered.connect(self.handlerSetInfoMode)
        self.actionAddLayer.triggered.connect(self.handlerAddLayer)
        self.actionDeleteLayer.triggered.connect(self.handlerDeleteLayer)
        self.actionRefresh.triggered.connect(self.handlerRefresh)
        self.mapCanvas.zoomLastStatusChanged.connect(self.handlerZoomLastStatus)
        self.mapCanvas.zoomNextStatusChanged.connect(self.handlerZoomNextStatus)
        self.mapCanvas.xyCoordinates.connect(self.handlerUpdateCoordinates)
        self.actionZoomLast.triggered.connect(self.handlerZoomLast)
        self.actionZoomNext.triggered.connect(self.handlerZoomNext)
        self.actionLayerAttributeTable.triggered.connect(self.handlerLayerAttributeTable)
        self.actionLayerAttributeEditor.triggered.connect(self.handlerLayerAttributeEditor)
        self.actionFeatureSelectExpression.triggered.connect(self.handlerFeatureSelectExpression)
        self.actionLayerProperties.triggered.connect(self.handlerLayerProperties)
        self.layerListView.customContextMenuRequested.connect(self.handlerLayerItemContextMenu)
        self.customContextMenuRequested.connect(self.handlerMainWindowContextMenu)
        
        # Dashboard tab
        self.radioQUESHHRUDefinition.toggled.connect(lambda:self.handlerToggleQUESH(self.radioQUESHHRUDefinition))
        self.radioQUESHWatershedModelEvaluation.toggled.connect(lambda:self.handlerToggleQUESH(self.radioQUESHWatershedModelEvaluation))
        self.radioQUESHWatershedIndicators.toggled.connect(lambda:self.handlerToggleQUESH(self.radioQUESHWatershedIndicators))
        self.radioQUESHHRUDefinition.click()
        self.radioTAOpportunityCostAbacus.toggled.connect(lambda:self.handlerToggleTAOpportunityCost(self.radioTAOpportunityCostAbacus))
        self.radioTAOpportunityCostCurve.toggled.connect(lambda:self.handlerToggleTAOpportunityCost(self.radioTAOpportunityCostCurve))
        self.radioTAOpportunityCostMap.toggled.connect(lambda:self.handlerToggleTAOpportunityCost(self.radioTAOpportunityCostMap))
        self.radioTAOpportunityCostAbacus.click()
        self.radioTARegionalEconomyDescriptiveAnalysis.toggled.connect(lambda:self.handlerToggleTARegionalEconomy(self.radioTARegionalEconomyDescriptiveAnalysis))
        self.radioTARegionalEconomyRegionalEconomicScenarioImpact.toggled.connect(lambda:self.handlerToggleTARegionalEconomy(self.radioTARegionalEconomyRegionalEconomicScenarioImpact))
        self.radioTARegionalEconomyLandRequirementAnalysis.toggled.connect(lambda:self.handlerToggleTARegionalEconomy(self.radioTARegionalEconomyLandRequirementAnalysis))
        self.radioTARegionalEconomyLandUseChangeImpact.toggled.connect(lambda:self.handlerToggleTARegionalEconomy(self.radioTARegionalEconomyLandUseChangeImpact))
        self.radioTARegionalEconomyDescriptiveAnalysis.click()
        
        # LUMENS action handlers
        # Database menu
        self.actionDialogLumensCreateDatabase.triggered.connect(self.handlerDialogLumensCreateDatabase)
        self.actionLumensOpenDatabase.triggered.connect(self.handlerLumensOpenDatabase)
        self.actionLumensCloseDatabase.triggered.connect(self.handlerLumensCloseDatabase)
        self.actionLumensExportDatabase.triggered.connect(self.handlerLumensExportDatabase)
        self.actionDialogLumensAddData.triggered.connect(self.handlerDialogLumensAddData)
        self.actionLumensDeleteData.triggered.connect(self.handlerLumensDeleteData)
        self.actionLumensDatabaseStatus.triggered.connect(self.handlerLumensDatabaseStatus)
        
        # PUR menu
        self.actionDialogLumensPUR.triggered.connect(self.handlerDialogLumensPUR)
        
        # QUES menu
        self.actionDialogLumensQUES.triggered.connect(self.handlerDialogLumensQUES)
        
        # TA menu
        self.actionDialogLumensTAOpportunityCost.triggered.connect(self.handlerDialogLumensTAOpportunityCost)
        self.actionDialogLumensTARegionalEconomy.triggered.connect(self.handlerDialogLumensTARegionalEconomy)
        
        # SCIENDO menu
        self.actionDialogLumensSCIENDO.triggered.connect(self.handlerDialogLumensSCIENDO)
        
        # Dashboard tab QPushButtons
        self.buttonProcessPURTemplate.clicked.connect(self.handlerProcessPURTemplate)
        self.buttonConfigurePUR.clicked.connect(self.handlerDialogLumensPUR)
        self.buttonProcessPreQUESTemplate.clicked.connect(self.handlerProcessPreQUESTemplate)
        self.buttonConfigurePreQUES.clicked.connect(lambda:self.handlerDialogLumensQUES('Pre-QUES'))
        self.buttonProcessQUESCTemplate.clicked.connect(self.handlerProcessQUESCTemplate)
        self.buttonConfigureQUESC.clicked.connect(lambda:self.handlerDialogLumensQUES('QUES-C'))
        self.buttonProcessQUESBTemplate.clicked.connect(self.handlerProcessQUESBTemplate)
        self.buttonConfigureQUESB.clicked.connect(lambda:self.handlerDialogLumensQUES('QUES-B'))
        self.buttonProcessQUESHTemplate.clicked.connect(self.handlerProcessQUESHTemplate)
        self.buttonConfigureQUESH.clicked.connect(lambda:self.handlerDialogLumensQUES('QUES-H'))
        self.buttonProcessTAOpportunityCostTemplate.clicked.connect(self.handlerProcessTAOpportunityCostTemplate)
        self.buttonConfigureTAOpportunityCost.clicked.connect(self.handlerDialogLumensTAOpportunityCost)
        self.buttonProcessTARegionalEconomyTemplate.clicked.connect(self.handlerProcessTARegionalEconomyTemplate)
        self.buttonConfigureTARegionalEconomy.clicked.connect(self.handlerDialogLumensTARegionalEconomy)
        self.buttonProcessSCIENDOLowEmissionDevelopmentAnalysisTemplate.clicked.connect(self.handlerProcessSCIENDOLowEmissionDevelopmentAnalysisTemplate)
        self.buttonConfigureSCIENDOLowEmissionDevelopmentAnalysis.clicked.connect(lambda:self.handlerDialogLumensSCIENDO('Low Emission Development Analysis'))
        self.buttonProcessSCIENDOLandUseChangeModelingTemplate.clicked.connect(self.handlerProcessSCIENDOLandUseChangeModelingTemplate)
        self.buttonConfigureSCIENDOLandUseChangeModeling.clicked.connect(lambda:self.handlerDialogLumensSCIENDO('Land Use Change Modeling'))
        
        # About menu
        #self.actionDialogLumensGuide.triggered.connect(self.handlerDialogLumensGuide)
        self.actionDialogLumensHelp.triggered.connect(self.handlerDialogLumensHelp)
        self.actionDialogLumensAbout.triggered.connect(self.handlerDialogLumensAbout)
    
    
    def setupUi(self):
        """Method for building the LUMENS main window UI.
        
        List of UI elements declared here:
        1. Menubar (and menus)
        2. Toolbar
        3. Statusbar
        4. Active project
        5. Sidebar tabs (layer list, dashboard, project tree)
        6. Body content splitter (between sidebar and map canvas)
        7. Main content splitter (between body content and scrolling log)
        8. Scrolling log (only visible in debug mode)
        9. QgsMapCanvas instance
        10. Map tools
        """
        self.windowTitle = 'LUMENS v {0} {1}'
        self.setWindowTitle(self.windowTitle.format(__version__, ''))

        self.centralWidget = QtGui.QWidget(self)
        self.centralWidget.setStyleSheet('QWidget { background-color: rgb(225, 229, 237); }')
        self.centralWidget.setMinimumSize(1024, 600)
        self.setCentralWidget(self.centralWidget)
        
        # Custom context menu when clicking on main window
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        
        # Create the default menus
        self.menubar = self.menuBar()
        self.fileMenu = self.menubar.addMenu('&File')
        self.viewMenu = self.menubar.addMenu('&View')
        self.modeMenu = self.menubar.addMenu('&Mode')
        self.databaseMenu = self.menubar.addMenu('&Database')
        self.purMenu = self.menubar.addMenu('&PUR')
        self.quesMenu = self.menubar.addMenu('&QUES')
        self.taMenu = self.menubar.addMenu('&TA')
        self.sciendoMenu = self.menubar.addMenu('&SCIENDO')
        self.aboutMenu = self.menubar.addMenu('&About')
        
        # 20160601: the menu bar must be hidden
        self.actionToggleMenubar = QtGui.QAction('Menu bar', self)
        self.actionToggleMenubar.setShortcut('f11')
        self.actionToggleMenubar.setCheckable(True)
        self.actionToggleMenubar.setChecked(True)
        self.actionToggleMenubar.triggered.connect(self.handlerToggleMenuBar)
        self.actionToggleMenubar.trigger()
        
        # Floating toolbar
        self.toolBar = QtGui.QToolBar(self)
        self.toolBar.setStyleSheet('QToolBar { background-color: rgb(225, 229, 237); } QToolButton { color: rgb(173, 185, 202); }')
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)
        self.toolBar.setOrientation(QtCore.Qt.Vertical)
        self.toolBar.setAllowedAreas(QtCore.Qt.LeftToolBarArea)
        
        self.dialogToolBar = QtGui.QToolBar(self)
        self.dialogToolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.dialogToolBar.setIconSize(QtCore.QSize(50, 50))
        self.dialogToolBar.setMovable(False)
        self.dialogToolBar.setStyleSheet('QToolBar { background: url(./ui/images/logo.png) right no-repeat; padding: 10px; background-color: rgb(225, 229, 237); } QToolButton { color: rgb(173, 185, 202); }')
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.dialogToolBar)
        
        self.statusBar = QtGui.QStatusBar(self)
        self.statusBar.setStyleSheet('QStatusBar { background-color: rgb(225, 229, 237); }')
        self.statusBar.setSizeGripEnabled(False)
        
        self.labelMapCanvasCoordinate = QtGui.QLabel(self)
        self.labelMapCanvasCoordinate.setStyleSheet('QLabel { margin-right: 10px; color: rgb(173, 185, 202); }')
        self.labelMapCanvasCoordinate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        
        self.statusBar.addPermanentWidget(self.labelMapCanvasCoordinate)
        self.setStatusBar(self.statusBar)
        
        # Create the actions and assigned them to the menus
        self.actionQuit = QtGui.QAction('Quit', self)
        self.actionQuit.setShortcut(QtGui.QKeySequence.Quit)
        
        self.actionToggleDialogToolbar = QtGui.QAction('Top Toolbar', self)
        self.actionToggleDialogToolbar.setCheckable(True)
        self.actionToggleDialogToolbar.setChecked(True)
        
        self.actionToggleToolbar = QtGui.QAction('Map Toolbar', self)
        self.actionToggleToolbar.setCheckable(True)
        self.actionToggleToolbar.setChecked(True)
        
        icon = QtGui.QIcon(':/ui/icons/iconActionZoomIn.png')
        self.actionZoomIn = QtGui.QAction(icon, 'Zoom In', self)
        self.actionZoomIn.setShortcut(QtGui.QKeySequence.ZoomIn)

        icon = QtGui.QIcon(':/ui/icons/iconActionZoomOut.png')
        self.actionZoomOut = QtGui.QAction(icon, 'Zoom Out', self)
        self.actionZoomOut.setShortcut(QtGui.QKeySequence.ZoomOut)

        icon = QtGui.QIcon(':/ui/icons/iconActionPan.png')
        self.actionPan = QtGui.QAction(icon, 'Pan', self)
        self.actionPan.setShortcut('Ctrl+1')
        self.actionPan.setCheckable(True)
        
        icon = QtGui.QIcon(':/ui/icons/iconActionSelect.png')
        self.actionSelect = QtGui.QAction(icon, 'Select', self)
        self.actionSelect.setShortcut('Ctrl+2')
        self.actionSelect.setCheckable(True)
        
        icon = QtGui.QIcon(':/ui/icons/iconActionInfo.png')
        self.actionInfo = QtGui.QAction(icon, 'Info', self)
        self.actionInfo.setShortcut('Ctrl+3')
        self.actionInfo.setCheckable(True)
        
        icon = QtGui.QIcon(':/ui/icons/iconActionAdd.png')
        self.actionAddLayer = QtGui.QAction(icon, 'Add Layer', self)
        
        icon = QtGui.QIcon(':/ui/icons/iconActionDelete.png')
        self.actionDeleteLayer = QtGui.QAction(icon, 'Delete Layer', self)
        self.actionDeleteLayer.setDisabled(True)
        
        icon = QtGui.QIcon(':/ui/icons/iconActionRefresh.png')
        self.actionRefresh = QtGui.QAction(icon, 'Refresh', self)
        self.actionRefresh.setShortcut('Ctrl+R')
        
        icon = QtGui.QIcon(':/ui/icons/iconActionZoomFull.png')
        self.actionZoomFull = QtGui.QAction(icon, 'Zoom Full', self)
        self.actionZoomFull.setShortcut('Ctrl+F')
        
        icon = QtGui.QIcon(':/ui/icons/iconActionZoomLayer.png')
        self.actionZoomLayer = QtGui.QAction(icon, 'Zoom to Layer', self)
        self.actionZoomLayer.setShortcut('Ctrl+L')
        self.actionZoomLayer.setDisabled(True)
        
        icon = QtGui.QIcon(':/ui/icons/iconActionZoomSelected.png')
        self.actionZoomSelected = QtGui.QAction(icon, 'Zoom to Selected', self)
        self.actionZoomSelected.setShortcut('Ctrl+S')
        self.actionZoomSelected.setDisabled(True)
        
        icon = QtGui.QIcon(':/ui/icons/iconActionPanSelected.png')
        self.actionPanSelected = QtGui.QAction(icon, 'Pan to Selected', self)
        self.actionPanSelected.setShortcut('Ctrl+P')
        self.actionPanSelected.setDisabled(True)
        
        icon = QtGui.QIcon(':/ui/icons/iconActionZoomLast.png')
        self.actionZoomLast = QtGui.QAction(icon, 'Zoom Last', self)
        self.actionZoomLast.setShortcut('Ctrl+,')
        self.actionZoomLast.setDisabled(True)
        
        icon = QtGui.QIcon(':/ui/icons/iconActionZoomNext.png')
        self.actionZoomNext = QtGui.QAction(icon, 'Zoom Next', self)
        self.actionZoomNext.setShortcut('Ctrl+.')
        self.actionZoomNext.setDisabled(True)
        
        icon = QtGui.QIcon(':/ui/icons/iconActionLayerAttributeTable.png')
        self.actionLayerAttributeTable = QtGui.QAction(icon, 'Layer Attribute Table', self)
        self.actionLayerAttributeTable.setShortcut('Ctrl+T')
        self.actionLayerAttributeTable.setDisabled(True)
        
        icon = QtGui.QIcon(':/ui/icons/iconActionToggleEdit.png')
        self.actionLayerAttributeEditor = QtGui.QAction(icon, 'Layer Attribute Editor', self)
        self.actionLayerAttributeEditor.setShortcut('Ctrl+A')
        self.actionLayerAttributeEditor.setDisabled(True)
        
        icon = QtGui.QIcon(':/ui/icons/iconActionFeatureSelectExpression.png')
        self.actionFeatureSelectExpression = QtGui.QAction(icon, 'Select Features By Expression', self)
        self.actionFeatureSelectExpression.setShortcut('Ctrl+E')
        self.actionFeatureSelectExpression.setDisabled(True)
        
        icon = QtGui.QIcon(':/ui/icons/iconActionLayerProperties.png')
        self.actionLayerProperties = QtGui.QAction(icon, 'Layer Properties', self)
        self.actionLayerProperties.setDisabled(True)
        
        self.fileMenu.addAction(self.actionQuit)
        
        self.addAction(self.actionToggleMenubar)
        
        self.modeMenu.addAction(self.actionPan)
        self.modeMenu.addAction(self.actionSelect)
        self.modeMenu.addAction(self.actionInfo)
        
        self.toolBar.addAction(self.actionAddLayer)
        self.toolBar.addAction(self.actionDeleteLayer)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionZoomIn)
        self.toolBar.addAction(self.actionZoomOut)
        self.toolBar.addAction(self.actionPanSelected)
        self.toolBar.addAction(self.actionZoomFull)
        self.toolBar.addAction(self.actionZoomLayer)
        self.toolBar.addAction(self.actionZoomSelected)
        self.toolBar.addAction(self.actionZoomLast)
        self.toolBar.addAction(self.actionZoomNext)
        self.toolBar.addAction(self.actionRefresh)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionLayerAttributeTable)
        self.toolBar.addAction(self.actionLayerAttributeEditor)
        self.toolBar.addAction(self.actionFeatureSelectExpression)
        self.toolBar.addAction(self.actionLayerProperties)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPan)
        self.toolBar.addAction(self.actionSelect)
        self.toolBar.addAction(self.actionInfo)
        
        # Database menu
        icon = QtGui.QIcon(':/ui/icons/iconActionDialogCreateLumensDatabase.png')
        self.actionDialogLumensCreateDatabase = QtGui.QAction(icon, 'Create LUMENS database', self)
        icon = QtGui.QIcon(':/ui/icons/iconActionLumensOpenDatabase.png')
        self.actionLumensOpenDatabase = QtGui.QAction(icon, 'Open LUMENS database', self)
        icon = QtGui.QIcon(':/ui/icons/iconActionLumensCloseDatabase.png')
        self.actionLumensCloseDatabase = QtGui.QAction(icon, 'Close LUMENS database', self)
        icon = QtGui.QIcon(':/ui/icons/iconActionLumensExportDatabase.png')
        self.actionLumensExportDatabase = QtGui.QAction(icon, 'Export LUMENS database', self)
        icon = QtGui.QIcon(':/ui/icons/iconActionDialogLumensAddData.png')
        self.actionDialogLumensAddData = QtGui.QAction(icon, 'Add data to LUMENS database', self)
        icon = QtGui.QIcon(':/ui/icons/iconActionLumensDeleteData.png')
        self.actionLumensDeleteData = QtGui.QAction(icon, 'Delete LUMENS data', self)
        icon = QtGui.QIcon(':/ui/icons/iconActionLumensDatabaseStatus.png')
        self.actionLumensDatabaseStatus = QtGui.QAction(icon, 'LUMENS database status', self)
        
        self.databaseMenu.addAction(self.actionDialogLumensCreateDatabase)
        self.databaseMenu.addAction(self.actionLumensOpenDatabase)
        self.databaseMenu.addAction(self.actionLumensCloseDatabase)
        self.databaseMenu.addAction(self.actionLumensExportDatabase)
        self.databaseMenu.addAction(self.actionDialogLumensAddData)
        self.databaseMenu.addAction(self.actionLumensDeleteData)
        self.databaseMenu.addAction(self.actionLumensDatabaseStatus)
        
        # PUR menu
        icon = QtGui.QIcon(':/ui/icons/iconActionDialogLumensPUR.png')
        self.actionDialogLumensPUR = QtGui.QAction(icon, 'Planning Unit Reconciliation', self)
        self.actionDialogLumensPUR.setIconText('PUR')
        
        self.purMenu.addAction(self.actionDialogLumensPUR)
        
        # QUES menu
        icon = QtGui.QIcon(':/ui/icons/iconActionDialogLumensQUES.png')
        self.actionDialogLumensQUES = QtGui.QAction(icon, 'Quantification Environmental Services', self)
        self.actionDialogLumensQUES.setIconText('QUES')
        
        self.quesMenu.addAction(self.actionDialogLumensQUES)
        
        # TA menu
        icon = QtGui.QIcon(':/ui/icons/iconActionDialogLumensTA.png')
        self.actionDialogLumensTAOpportunityCost = QtGui.QAction(icon, 'Trade-off Analysis [Opportunity Cost]', self)
        self.actionDialogLumensTARegionalEconomy = QtGui.QAction(icon, 'Trade-off Analysis [Regional Economy]', self)
        self.actionDialogLumensTAOpportunityCost.setIconText('TA')
        
        self.taMenu.addAction(self.actionDialogLumensTAOpportunityCost)
        self.taMenu.addAction(self.actionDialogLumensTARegionalEconomy)
        
        # SCIENDO menu
        icon = QtGui.QIcon(':/ui/icons/iconActionDialogLumensSCIENDO.png')
        self.actionDialogLumensSCIENDO = QtGui.QAction(icon, 'SCIENDO', self)
        self.actionDialogLumensSCIENDO.setIconText('SCIENDO')
        
        self.sciendoMenu.addAction(self.actionDialogLumensSCIENDO)
        
        # About menu
        icon = QtGui.QIcon(':/ui/icons/iconActionHelp.png')
        ##self.actionDialogLumensGuide = QtGui.QAction(icon, 'Open Guide', self)
        self.actionDialogLumensHelp = QtGui.QAction(icon, 'Open Help', self)
        self.actionDialogLumensAbout = QtGui.QAction('About LUMENS', self)
        
        ##self.aboutMenu.addAction(self.actionDialogLumensGuide)
        self.aboutMenu.addAction(self.actionDialogLumensHelp)
        self.aboutMenu.addSeparator()
        self.aboutMenu.addAction(self.actionDialogLumensAbout)
        
        # Dialog toolbar
        self.dialogToolBar.addAction(self.actionDialogLumensPUR)
        self.dialogToolBar.addAction(self.actionDialogLumensQUES)
        self.dialogToolBar.addAction(self.actionDialogLumensTAOpportunityCost)
        self.dialogToolBar.addAction(self.actionDialogLumensSCIENDO)
        ##self.dialogToolBar.addSeparator()
        
        # Create the app window layouts
        self.layoutActiveProject = QtGui.QHBoxLayout()
        self.labelActiveProject = QtGui.QLabel(self)
        self.labelActiveProject.setText('Active project:')
        self.labelActiveProject.setStyleSheet('QLabel { color: rgb(95, 98, 102); }')
        self.layoutActiveProject.addWidget(self.labelActiveProject)
        
        self.lineEditActiveProject = QtGui.QLineEdit(self)
        self.lineEditActiveProject.setReadOnly(True)
        self.lineEditActiveProject.setStyleSheet('QLineEdit { background-color: rgb(244, 248, 252); }')
        self.layoutActiveProject.addWidget(self.lineEditActiveProject)
        
        self.layerListView = QtGui.QListView(self)
        self.layerListView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        ##self.layerListView.setMovement(QtGui.QListView.Snap)
        self.layerListView.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.layerListView.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.layerListView.setDragDropOverwriteMode(False)
        self.layerListView.setAcceptDrops(True)
        self.layerListView.setDropIndicatorShown(True)
        self.layerListView.setDragEnabled(True)
        ##self.layerListView.setFixedWidth(200)
        
        self.layerListView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        
        self.projectModel = QtGui.QFileSystemModel()
        self.projectModel.setRootPath(QtCore.QDir.rootPath())
        
        self.projectTreeView = QtGui.QTreeView()
        self.projectTreeView.setModel(self.projectModel)
        self.projectTreeView.setRootIndex(self.projectModel.index(QtCore.QDir.rootPath()))
        self.projectTreeView.hideColumn(1) # Hide all columns except name
        self.projectTreeView.hideColumn(2)
        self.projectTreeView.hideColumn(3)
        
        self.sidebarTabWidget = QtGui.QTabWidget()
        sidebarTabWidgetStylesheet = """
        QTabWidget::pane {
            border: none;
            background-color: rgb(244, 248, 252);
        }
        QTabBar::tab {
            background-color: rgb(174, 176, 178);
            color: rgb(95, 98, 102);
            height: 50px; 
            width: 100px;
            font-size: 14px;
        }
        QTabBar::tab:selected, QTabBar::tab:hover {
            background-color: rgb(244, 248, 252);
            color: rgb(56, 65, 73);
        }
        QTabBar::tab::selected{
            font: bold;
        }
        """
        self.sidebarTabWidget.setStyleSheet(sidebarTabWidgetStylesheet)
        self.sidebarTabWidget.setTabPosition(QtGui.QTabWidget.North)
        
        self.dashboardTabWidget = QtGui.QTabWidget()
        
        self.tabLayers = QtGui.QWidget()
        self.tabDatabase = QtGui.QWidget()
        self.tabDatabase.setStyleSheet('QWidget{ background-color: rgb(244, 248, 252); }')
        # self.tabDashboard = QtGui.QWidget()
        #self.tabProject = QtGui.QWidget()
        self.tabHelp = QtGui.QWidget()
        self.tabHelp.setStyleSheet('QWidget{ background-color: rgb(244, 248, 252); }')
        
        self.layoutTabLayers = QtGui.QVBoxLayout()
        self.layoutTabDatabase = QtGui.QVBoxLayout()
        self.layoutTabDatabase.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        # self.layoutTabDashboard = QtGui.QVBoxLayout()
        #self.layoutTabProject = QtGui.QVBoxLayout()
        self.layoutTabHelp = QtGui.QVBoxLayout()
        
        self.tabLayers.setLayout(self.layoutTabLayers)
        self.tabDatabase.setLayout(self.layoutTabDatabase)
        # self.tabDashboard.setLayout(self.layoutTabDashboard)
        #self.tabProject.setLayout(self.layoutTabProject)
        self.tabHelp.setLayout(self.layoutTabHelp)
        
        #***********************************************************
        # Setup 'Dashboard' tab => 'Templates' tab
        #***********************************************************
        self.tabDashboardPUR = QtGui.QWidget()
        self.tabDashboardPUR.setStyleSheet('QWidget{ background-color: rgb(244, 248, 252); }')
        self.tabDashboardQUES = QtGui.QWidget()
        self.tabDashboardTA = QtGui.QWidget()
        self.tabDashboardSCIENDO = QtGui.QWidget()
        
        self.layoutDashboardPUR = QtGui.QGridLayout()
        self.layoutDashboardQUES = QtGui.QVBoxLayout()
        self.layoutDashboardTA = QtGui.QVBoxLayout()
        self.layoutDashboardSCIENDO = QtGui.QVBoxLayout()
        
        self.layoutDashboardPUR.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.layoutDashboardQUES.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.layoutDashboardTA.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.layoutDashboardSCIENDO.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        
        self.tabDashboardPUR.setLayout(self.layoutDashboardPUR)
        self.tabDashboardQUES.setLayout(self.layoutDashboardQUES)
        self.tabDashboardTA.setLayout(self.layoutDashboardTA)
        self.tabDashboardSCIENDO.setLayout(self.layoutDashboardSCIENDO)
        
        # 20160601: move module tab to top level
        #self.dashboardTabWidget.addTab(self.tabDashboardPUR, 'PUR')
        #self.dashboardTabWidget.addTab(self.tabDashboardQUES, 'QUES')
        #self.dashboardTabWidget.addTab(self.tabDashboardTA, 'TA')
        #self.dashboardTabWidget.addTab(self.tabDashboardSCIENDO, 'SCIENDO')
        self.sidebarTabWidget.addTab(self.tabLayers, 'Project') # Formerly 'Layers'
        self.sidebarTabWidget.addTab(self.tabDatabase, 'Database')
        self.sidebarTabWidget.addTab(self.tabDashboardPUR, 'PUR')
        self.sidebarTabWidget.addTab(self.tabDashboardQUES, 'QUES')
        self.sidebarTabWidget.addTab(self.tabDashboardTA, 'TA')
        self.sidebarTabWidget.addTab(self.tabDashboardSCIENDO, 'SCIENDO')
        #self.sidebarTabWidget.addTab(self.tabDashboard, 'Templates') # Formerly 'Dashboard'
        #self.sidebarTabWidget.addTab(self.tabProject, 'Project')
        self.sidebarTabWidget.addTab(self.tabHelp, 'Help')

        # QUES sub tabs
        self.QUESTabWidget = QtGui.QTabWidget()
        QUESTabWidgetStylesheet = """
        QTabWidget QWidget { 
            background-color: rgb(217, 229, 252);
            color: rgb(95, 98, 102);
        }
        QTabBar::tab {
            background-color: rgb(244, 248, 252);
            height: 50px; 
            width: 120px;            
        }
        QTabBar::tab:selected, QTabBar::tab:hover {
            background-color: rgb(217, 229, 252);
            font: bold;
        }
        """
        self.QUESTabWidget.setStyleSheet(QUESTabWidgetStylesheet)
        self.QUESTabWidget.setTabPosition(QtGui.QTabWidget.North)
        
        self.subtabPreQUES = QtGui.QWidget()
        self.subtabQUESC = QtGui.QWidget()
        self.subtabQUESB = QtGui.QWidget()
        self.subtabQUESH = QtGui.QWidget()
        
        self.layoutSubtabPreQUES = QtGui.QGridLayout()
        self.layoutSubtabQUESC = QtGui.QGridLayout()
        self.layoutSubtabQUESB = QtGui.QGridLayout()
        self.layoutSubtabQUESH = QtGui.QGridLayout()
        
        self.layoutSubtabPreQUES.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.layoutSubtabQUESC.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.layoutSubtabQUESB.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.layoutSubtabQUESH.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        
        self.subtabPreQUES.setLayout(self.layoutSubtabPreQUES)
        self.subtabQUESC.setLayout(self.layoutSubtabQUESC)
        self.subtabQUESB.setLayout(self.layoutSubtabQUESB)
        self.subtabQUESH.setLayout(self.layoutSubtabQUESH)
        
        icon = QtGui.QIcon(':/ui/icons/iconSubtabPreQUES.png')
        self.QUESTabWidget.addTab(self.subtabPreQUES, icon, ' Pre-QUES')
        icon = QtGui.QIcon(':/ui/icons/iconSubtabQUESC.png')
        self.QUESTabWidget.addTab(self.subtabQUESC, icon, 'QUES-C')
        icon = QtGui.QIcon(':/ui/icons/iconSubtabQUESB.png')
        self.QUESTabWidget.addTab(self.subtabQUESB, icon, 'QUES-B')
        icon = QtGui.QIcon(':/ui/icons/iconSubtabQUESH.png')
        self.QUESTabWidget.addTab(self.subtabQUESH, icon, 'QUES-H')
        
        self.layoutDashboardQUES.addWidget(self.QUESTabWidget)
        
        # TA sub tabs
        self.TATabWidget = QtGui.QTabWidget()
        TATabWidgetStylesheet = """
        QTabWidget QWidget { 
            background-color: rgb(217, 229, 252);
            color: rgb(95, 98, 102);
        }
        QTabBar::tab {
            background-color: rgb(244, 248, 252);
            height: 50px; 
            width: 200px;             
        }
        QTabBar::tab:selected, QTabBar::tab:hover {
            background-color: rgb(217, 229, 252);
            font: bold;
        }
        """
        self.TATabWidget.setStyleSheet(TATabWidgetStylesheet)
        self.TATabWidget.setTabPosition(QtGui.QTabWidget.North)
        
        self.subtabTAOpportunityCost = QtGui.QWidget()
        self.subtabTARegionalEconomy = QtGui.QWidget()
        
        self.layoutSubtabTAOpportunityCost = QtGui.QVBoxLayout()
        self.layoutSubtabTARegionalEconomy = QtGui.QVBoxLayout()
        
        self.layoutSubtabTAOpportunityCost.setAlignment(QtCore.Qt.AlignTop)
        self.layoutSubtabTARegionalEconomy.setAlignment(QtCore.Qt.AlignTop)
        
        self.subtabTAOpportunityCost.setLayout(self.layoutSubtabTAOpportunityCost)
        self.subtabTARegionalEconomy.setLayout(self.layoutSubtabTARegionalEconomy)
        
        self.TATabWidget.addTab(self.subtabTAOpportunityCost, 'Opportunity Cost')
        self.TATabWidget.addTab(self.subtabTARegionalEconomy, 'Regional Economy')
        
        self.layoutDashboardTA.addWidget(self.TATabWidget)
        
        # SCIENDO sub tabs
        self.SCIENDOTabWidget = QtGui.QTabWidget()
        SCIENDOTabWidgetStylesheet = """
        QTabWidget QWidget { 
            background-color: rgb(217, 229, 252);
            color: rgb(95, 98, 102);
        }
        QTabBar::tab {
            background-color: rgb(244, 248, 252);
            height: 50px; 
            width: 280px;             
        }
        QTabBar::tab:selected, QTabBar::tab:hover {
            background-color: rgb(217, 229, 252);
            font: bold;
        }
        """
        self.SCIENDOTabWidget.setStyleSheet(SCIENDOTabWidgetStylesheet)
        self.SCIENDOTabWidget.setTabPosition(QtGui.QTabWidget.North)
        
        self.subtabSCIENDOLowEmissionDevelopmentAnalysis = QtGui.QWidget()
        self.subtabSCIENDOLandUseChangeModeling = QtGui.QWidget()
        
        self.layoutSubtabSCIENDOLowEmissionDevelopmentAnalysis = QtGui.QVBoxLayout()
        self.layoutSubtabSCIENDOLandUseChangeModeling = QtGui.QVBoxLayout()
        
        self.layoutSubtabSCIENDOLowEmissionDevelopmentAnalysis.setAlignment(QtCore.Qt.AlignTop)
        self.layoutSubtabSCIENDOLandUseChangeModeling.setAlignment(QtCore.Qt.AlignTop)
        
        self.subtabSCIENDOLowEmissionDevelopmentAnalysis.setLayout(self.layoutSubtabSCIENDOLowEmissionDevelopmentAnalysis)
        self.subtabSCIENDOLandUseChangeModeling.setLayout(self.layoutSubtabSCIENDOLandUseChangeModeling)
        
        self.SCIENDOTabWidget.addTab(self.subtabSCIENDOLowEmissionDevelopmentAnalysis, 'Low Emission Development Analysis')
        self.SCIENDOTabWidget.addTab(self.subtabSCIENDOLandUseChangeModeling, 'Land Use Change Modeling')
        
        self.layoutDashboardSCIENDO.addWidget(self.SCIENDOTabWidget)
        
        # PUR dashboard widgets
        self.groupBoxPURTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxPURTemplate = QtGui.QVBoxLayout()
        self.groupBoxPURTemplate.setLayout(self.layoutGroupBoxPURTemplate)
        
        self.layoutPURTemplate = QtGui.QHBoxLayout()
        
        # PUR template
        self.labelPURTemplate = QtGui.QLabel()
        self.labelPURTemplate.setText('Template name:')
        self.layoutPURTemplate.addWidget(self.labelPURTemplate)
        
        self.comboBoxPURTemplate = QtGui.QComboBox()
        self.comboBoxPURTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxPURTemplate.setDisabled(True)
        self.comboBoxPURTemplate.addItem('No template found')
        self.layoutPURTemplate.addWidget(self.comboBoxPURTemplate)
        
        self.layoutGroupBoxPURTemplate.addLayout(self.layoutPURTemplate)
        
        self.buttonProcessPURTemplate = QtGui.QPushButton()
        self.buttonProcessPURTemplate.setText('Process')
        self.buttonProcessPURTemplate.setDisabled(True)
        
        self.buttonConfigurePUR = QtGui.QPushButton()
        icon = QtGui.QIcon(':/ui/icons/iconActionConfigure.png')
        self.buttonConfigurePUR.setIcon(icon)
        self.buttonConfigurePUR.setText('Configure')
        self.buttonConfigurePUR.setDisabled(True)
        
        self.layoutDashboardPUR.addWidget(self.groupBoxPURTemplate)
        self.layoutDashboardPUR.addWidget(self.buttonProcessPURTemplate)
        self.layoutDashboardPUR.addWidget(self.buttonConfigurePUR)
        
        #####################################################################
        
        # Pre-QUES sub tab dashboard widgets
        self.groupBoxPreQUESTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxPreQUESTemplate = QtGui.QVBoxLayout()
        self.groupBoxPreQUESTemplate.setLayout(self.layoutGroupBoxPreQUESTemplate)
        
        self.layoutPreQUESTemplate = QtGui.QHBoxLayout()
        
        # Pre-QUES template
        self.labelPreQUESTemplate = QtGui.QLabel()
        self.labelPreQUESTemplate.setText('Template name:')
        self.layoutPreQUESTemplate.addWidget(self.labelPreQUESTemplate)
        
        self.comboBoxPreQUESTemplate = QtGui.QComboBox()
        self.comboBoxPreQUESTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxPreQUESTemplate.setDisabled(True)
        self.comboBoxPreQUESTemplate.addItem('No template found')
        self.layoutPreQUESTemplate.addWidget(self.comboBoxPreQUESTemplate)
        
        self.layoutGroupBoxPreQUESTemplate.addLayout(self.layoutPreQUESTemplate)
        
        self.buttonProcessPreQUESTemplate = QtGui.QPushButton()
        self.buttonProcessPreQUESTemplate.setText('Process')
        self.buttonProcessPreQUESTemplate.setDisabled(True)
        
        self.buttonConfigurePreQUES = QtGui.QPushButton()
        icon = QtGui.QIcon(':/ui/icons/iconActionConfigure.png')
        self.buttonConfigurePreQUES.setIcon(icon)
        self.buttonConfigurePreQUES.setText('Configure')
        self.buttonConfigurePreQUES.setDisabled(True)
        
        self.layoutSubtabPreQUES.addWidget(self.groupBoxPreQUESTemplate)
        self.layoutSubtabPreQUES.addWidget(self.buttonProcessPreQUESTemplate)
        self.layoutSubtabPreQUES.addWidget(self.buttonConfigurePreQUES)
        
        #####################################################################
        
        # QUES-C sub tab dashboard widgets
        self.groupBoxQUESCFeatures = QtGui.QGroupBox('Features')
        self.layoutGroupBoxQUESCFeatures = QtGui.QVBoxLayout()
        self.groupBoxQUESCFeatures.setLayout(self.layoutGroupBoxQUESCFeatures)
        
        self.labelQUESCFeaturesInfo = QtGui.QLabel()
        self.labelQUESCFeaturesInfo.setText('Lorem ipsum dolor sit amet...')
        self.layoutGroupBoxQUESCFeatures.addWidget(self.labelQUESCFeaturesInfo)
        
        self.checkBoxQUESCCarbonAccounting = QtGui.QCheckBox('Carbon Accounting')
        self.checkBoxQUESCPeatlandCarbonAccounting = QtGui.QCheckBox('Peatland Carbon Accounting')
        self.checkBoxQUESCSummarizeMultiplePeriod = QtGui.QCheckBox('Summarize Multiple Period')
        
        self.layoutGroupBoxQUESCFeatures.addWidget(self.checkBoxQUESCCarbonAccounting)
        self.layoutGroupBoxQUESCFeatures.addWidget(self.checkBoxQUESCPeatlandCarbonAccounting)
        self.layoutGroupBoxQUESCFeatures.addWidget(self.checkBoxQUESCSummarizeMultiplePeriod)
        
        self.groupBoxQUESCTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxQUESCTemplate = QtGui.QVBoxLayout()
        self.groupBoxQUESCTemplate.setLayout(self.layoutGroupBoxQUESCTemplate)
        
        self.layoutQUESCTemplate = QtGui.QHBoxLayout()
        
        # QUES-C template
        self.labelQUESCTemplate = QtGui.QLabel()
        self.labelQUESCTemplate.setText('Template name:')
        self.layoutQUESCTemplate.addWidget(self.labelQUESCTemplate)
        
        self.comboBoxQUESCTemplate = QtGui.QComboBox()
        self.comboBoxQUESCTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxQUESCTemplate.setDisabled(True)
        self.comboBoxQUESCTemplate.addItem('No template found')
        self.layoutQUESCTemplate.addWidget(self.comboBoxQUESCTemplate)
        
        self.layoutGroupBoxQUESCTemplate.addLayout(self.layoutQUESCTemplate)
        
        self.buttonProcessQUESCTemplate = QtGui.QPushButton()
        self.buttonProcessQUESCTemplate.setText('Process')
        self.buttonProcessQUESCTemplate.setDisabled(True)
        
        self.buttonConfigureQUESC = QtGui.QPushButton()
        icon = QtGui.QIcon(':/ui/icons/iconActionConfigure.png')
        self.buttonConfigureQUESC.setIcon(icon)
        self.buttonConfigureQUESC.setText('Configure')
        self.buttonConfigureQUESC.setDisabled(True)
        
        self.layoutSubtabQUESC.addWidget(self.groupBoxQUESCFeatures)
        self.layoutSubtabQUESC.addWidget(self.groupBoxQUESCTemplate)
        self.layoutSubtabQUESC.addWidget(self.buttonProcessQUESCTemplate)
        self.layoutSubtabQUESC.addWidget(self.buttonConfigureQUESC)
        
        #####################################################################
        
        # QUES-B sub tab dashboard widgets
        self.groupBoxQUESBTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxQUESBTemplate = QtGui.QVBoxLayout()
        self.groupBoxQUESBTemplate.setLayout(self.layoutGroupBoxQUESBTemplate)
        
        self.layoutQUESBTemplate = QtGui.QHBoxLayout()
        
        # QUES-B template
        self.labelQUESBTemplate = QtGui.QLabel()
        self.labelQUESBTemplate.setText('Template name:')
        self.layoutQUESBTemplate.addWidget(self.labelQUESBTemplate)
        
        self.comboBoxQUESBTemplate = QtGui.QComboBox()
        self.comboBoxQUESBTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxQUESBTemplate.setDisabled(True)
        self.comboBoxQUESBTemplate.addItem('No template found')
        self.layoutQUESBTemplate.addWidget(self.comboBoxQUESBTemplate)
        
        self.layoutGroupBoxQUESBTemplate.addLayout(self.layoutQUESBTemplate)
        
        self.buttonProcessQUESBTemplate = QtGui.QPushButton()
        self.buttonProcessQUESBTemplate.setText('Process')
        self.buttonProcessQUESBTemplate.setDisabled(True)
        
        self.buttonConfigureQUESB = QtGui.QPushButton()
        icon = QtGui.QIcon(':/ui/icons/iconActionConfigure.png')
        self.buttonConfigureQUESB.setIcon(icon)
        self.buttonConfigureQUESB.setText('Configure')
        self.buttonConfigureQUESB.setDisabled(True)
        
        self.layoutSubtabQUESB.addWidget(self.groupBoxQUESBTemplate)
        self.layoutSubtabQUESB.addWidget(self.buttonProcessQUESBTemplate)
        self.layoutSubtabQUESB.addWidget(self.buttonConfigureQUESB)
        
        #####################################################################
        
        # QUES-H sub tab dashboard widgets
        self.groupBoxQUESHFeatures = QtGui.QGroupBox('Features')
        self.layoutGroupBoxQUESHFeatures = QtGui.QVBoxLayout()
        self.groupBoxQUESHFeatures.setLayout(self.layoutGroupBoxQUESHFeatures)
        
        self.labelQUESHFeaturesInfo = QtGui.QLabel()
        self.labelQUESHFeaturesInfo.setText('Lorem ipsum dolor sit amet...')
        self.layoutGroupBoxQUESHFeatures.addWidget(self.labelQUESHFeaturesInfo)
        
        self.radioQUESHHRUDefinition = QtGui.QRadioButton('Hydrological Response Unit Definition')
        self.radioQUESHWatershedModelEvaluation = QtGui.QRadioButton('Watershed Model Evaluation')
        self.radioQUESHWatershedIndicators = QtGui.QRadioButton('Watershed Indicators')
        
        self.layoutGroupBoxQUESHFeatures.addWidget(self.radioQUESHHRUDefinition)
        self.layoutGroupBoxQUESHFeatures.addWidget(self.radioQUESHWatershedModelEvaluation)
        self.layoutGroupBoxQUESHFeatures.addWidget(self.radioQUESHWatershedIndicators)
        
        self.groupBoxHRUDefinitionFunction = QtGui.QGroupBox('Function')
        self.layoutGroupBoxHRUDefinitionFunction = QtGui.QVBoxLayout()
        self.groupBoxHRUDefinitionFunction.setLayout(self.layoutGroupBoxHRUDefinitionFunction)
        
        self.labelHRUDefinitionFunction = QtGui.QLabel()
        self.labelHRUDefinitionFunction.setText('Lorem ipsum dolot sit amet...')
        self.layoutGroupBoxHRUDefinitionFunction.addWidget(self.labelHRUDefinitionFunction)
        
        self.checkBoxHRUDefinitionDominantHRU = QtGui.QCheckBox('Dominant HRU')
        self.checkBoxHRUDefinitionDominantHRU.setChecked(False)
        self.checkBoxHRUDefinitionDominantLUSSL = QtGui.QCheckBox('Dominant Land Use, Soil, and Slope')
        self.checkBoxHRUDefinitionDominantLUSSL.setChecked(False)
        self.checkBoxHRUDefinitionMultipleHRU = QtGui.QCheckBox('Multiple HRU')
        self.checkBoxHRUDefinitionMultipleHRU.setChecked(False)
        
        self.layoutGroupBoxHRUDefinitionFunction.addWidget(self.checkBoxHRUDefinitionDominantHRU)
        self.layoutGroupBoxHRUDefinitionFunction.addWidget(self.checkBoxHRUDefinitionDominantLUSSL)
        self.layoutGroupBoxHRUDefinitionFunction.addWidget(self.checkBoxHRUDefinitionMultipleHRU)
        self.groupBoxHRUDefinitionFunction.setDisabled(True)
        
        self.groupBoxQUESHTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxQUESHTemplate = QtGui.QVBoxLayout()
        self.groupBoxQUESHTemplate.setLayout(self.layoutGroupBoxQUESHTemplate)
        
        self.layoutQUESHHRUDefinitionTemplate = QtGui.QHBoxLayout()
        self.layoutQUESHWatershedModelEvaluationTemplate = QtGui.QHBoxLayout()
        self.layoutQUESHWatershedIndicatorsTemplate = QtGui.QHBoxLayout()
        
        # 'HRU Definition' template
        self.labelHRUDefinitionTemplate = QtGui.QLabel()
        self.labelHRUDefinitionTemplate.setText('Template name:')
        self.layoutQUESHHRUDefinitionTemplate.addWidget(self.labelHRUDefinitionTemplate)
        
        self.comboBoxHRUDefinitionTemplate = QtGui.QComboBox()
        self.comboBoxHRUDefinitionTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxHRUDefinitionTemplate.setDisabled(True)
        self.comboBoxHRUDefinitionTemplate.addItem('No template found')
        self.layoutQUESHHRUDefinitionTemplate.addWidget(self.comboBoxHRUDefinitionTemplate)
        
        # 'Watershed Model Evaluation' template
        self.labelWatershedModelEvaluationTemplate = QtGui.QLabel()
        self.labelWatershedModelEvaluationTemplate.setText('Template name:')
        self.layoutQUESHWatershedModelEvaluationTemplate.addWidget(self.labelWatershedModelEvaluationTemplate)
        
        self.comboBoxWatershedModelEvaluationTemplate = QtGui.QComboBox()
        self.comboBoxWatershedModelEvaluationTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxWatershedModelEvaluationTemplate.setDisabled(True)
        self.comboBoxWatershedModelEvaluationTemplate.addItem('No template found')
        self.layoutQUESHWatershedModelEvaluationTemplate.addWidget(self.comboBoxWatershedModelEvaluationTemplate)
        
        # 'Watershed Indicators' template
        self.labelWatershedIndicatorsTemplate = QtGui.QLabel()
        self.labelWatershedIndicatorsTemplate.setText('Template name:')
        self.layoutQUESHWatershedIndicatorsTemplate.addWidget(self.labelWatershedIndicatorsTemplate)
        
        self.comboBoxWatershedIndicatorsTemplate = QtGui.QComboBox()
        self.comboBoxWatershedIndicatorsTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxWatershedIndicatorsTemplate.setDisabled(True)
        self.comboBoxWatershedIndicatorsTemplate.addItem('No template found')
        self.layoutQUESHWatershedIndicatorsTemplate.addWidget(self.comboBoxWatershedIndicatorsTemplate)
        
        self.layoutGroupBoxQUESHTemplate.addLayout(self.layoutQUESHHRUDefinitionTemplate)
        self.layoutGroupBoxQUESHTemplate.addLayout(self.layoutQUESHWatershedModelEvaluationTemplate)
        self.layoutGroupBoxQUESHTemplate.addLayout(self.layoutQUESHWatershedIndicatorsTemplate)
        
        # Hide the templates first until a feature is selected
        for i in range(self.layoutQUESHHRUDefinitionTemplate.count()):
            item = self.layoutQUESHHRUDefinitionTemplate.itemAt(i)
            item.widget().setVisible(False)
        
        for i in range(self.layoutQUESHWatershedModelEvaluationTemplate.count()):
            item = self.layoutQUESHWatershedModelEvaluationTemplate.itemAt(i)
            item.widget().setVisible(False)
        
        for i in range(self.layoutQUESHWatershedIndicatorsTemplate.count()):
            item = self.layoutQUESHWatershedIndicatorsTemplate.itemAt(i)
            item.widget().setVisible(False)
        
        self.buttonProcessQUESHTemplate = QtGui.QPushButton()
        self.buttonProcessQUESHTemplate.setText('Process')
        self.buttonProcessQUESHTemplate.setDisabled(True)
        
        self.buttonConfigureQUESH = QtGui.QPushButton()
        icon = QtGui.QIcon(':/ui/icons/iconActionConfigure.png')
        self.buttonConfigureQUESH.setIcon(icon)
        self.buttonConfigureQUESH.setText('Configure')
        self.buttonConfigureQUESH.setDisabled(True)
        
        self.layoutSubtabQUESH.addWidget(self.groupBoxQUESHFeatures)
        self.layoutSubtabQUESH.addWidget(self.groupBoxHRUDefinitionFunction)
        self.layoutSubtabQUESH.addWidget(self.groupBoxQUESHTemplate)
        self.layoutSubtabQUESH.addWidget(self.buttonProcessQUESHTemplate)
        self.layoutSubtabQUESH.addWidget(self.buttonConfigureQUESH)
        
        #####################################################################
        
        # TA 'Opportunity Cost' sub tab dashboard widgets
        self.groupBoxTAOpportunityCostFeatures = QtGui.QGroupBox('Features')
        self.layoutGroupBoxTAOpportunityCostFeatures = QtGui.QVBoxLayout()
        self.groupBoxTAOpportunityCostFeatures.setLayout(self.layoutGroupBoxTAOpportunityCostFeatures)
        
        self.labelTAOpportunityCostFeaturesInfo = QtGui.QLabel()
        self.labelTAOpportunityCostFeaturesInfo.setText('Lorem ipsum dolor sit amet...')
        self.layoutGroupBoxTAOpportunityCostFeatures.addWidget(self.labelTAOpportunityCostFeaturesInfo)
        
        self.radioTAOpportunityCostAbacus = QtGui.QRadioButton('Abacus Opportunity Cost')
        self.radioTAOpportunityCostCurve = QtGui.QRadioButton('Opportunity Cost Curve')
        self.radioTAOpportunityCostMap = QtGui.QRadioButton('Opportunity Cost Map')
        
        self.layoutGroupBoxTAOpportunityCostFeatures.addWidget(self.radioTAOpportunityCostAbacus)
        self.layoutGroupBoxTAOpportunityCostFeatures.addWidget(self.radioTAOpportunityCostCurve)
        self.layoutGroupBoxTAOpportunityCostFeatures.addWidget(self.radioTAOpportunityCostMap)
        
        self.groupBoxTAOpportunityCostTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxTAOpportunityCostTemplate = QtGui.QVBoxLayout()
        self.groupBoxTAOpportunityCostTemplate.setLayout(self.layoutGroupBoxTAOpportunityCostTemplate)
        
        self.layoutTAAbacusOpportunityCostTemplate = QtGui.QHBoxLayout()
        self.layoutTAOpportunityCostCurveTemplate = QtGui.QHBoxLayout()
        self.layoutTAOpportunityCostMapTemplate = QtGui.QHBoxLayout()
        
        # TA 'Abacus Opportunity Cost' template
        self.labelAbacusOpportunityCostTemplate = QtGui.QLabel()
        self.labelAbacusOpportunityCostTemplate.setText('Template name:')
        self.layoutTAAbacusOpportunityCostTemplate.addWidget(self.labelAbacusOpportunityCostTemplate)
        
        self.comboBoxAbacusOpportunityCostTemplate = QtGui.QComboBox()
        self.comboBoxAbacusOpportunityCostTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxAbacusOpportunityCostTemplate.setDisabled(True)
        self.comboBoxAbacusOpportunityCostTemplate.addItem('No template found')
        self.layoutTAAbacusOpportunityCostTemplate.addWidget(self.comboBoxAbacusOpportunityCostTemplate)
        
        # TA 'Opportunity Cost Curve' template
        self.labelOpportunityCostCurveTemplate = QtGui.QLabel()
        self.labelOpportunityCostCurveTemplate.setText('Template name:')
        self.layoutTAOpportunityCostCurveTemplate.addWidget(self.labelOpportunityCostCurveTemplate)
        
        self.comboBoxOpportunityCostCurveTemplate = QtGui.QComboBox()
        self.comboBoxOpportunityCostCurveTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxOpportunityCostCurveTemplate.setDisabled(True)
        self.comboBoxOpportunityCostCurveTemplate.addItem('No template found')
        self.layoutTAOpportunityCostCurveTemplate.addWidget(self.comboBoxOpportunityCostCurveTemplate)
        
        # TA 'Opportunity Cost Map' template
        self.labelOpportunityCostMapTemplate = QtGui.QLabel()
        self.labelOpportunityCostMapTemplate.setText('Template name:')
        self.layoutTAOpportunityCostMapTemplate.addWidget(self.labelOpportunityCostMapTemplate)
        
        self.comboBoxOpportunityCostMapTemplate = QtGui.QComboBox()
        self.comboBoxOpportunityCostMapTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxOpportunityCostMapTemplate.setDisabled(True)
        self.comboBoxOpportunityCostMapTemplate.addItem('No template found')
        self.layoutTAOpportunityCostMapTemplate.addWidget(self.comboBoxOpportunityCostMapTemplate)
        
        self.layoutGroupBoxTAOpportunityCostTemplate.addLayout(self.layoutTAAbacusOpportunityCostTemplate)
        self.layoutGroupBoxTAOpportunityCostTemplate.addLayout(self.layoutTAOpportunityCostCurveTemplate)
        self.layoutGroupBoxTAOpportunityCostTemplate.addLayout(self.layoutTAOpportunityCostMapTemplate)
        
        # Hide the templates first until a feature is selected
        for i in range(self.layoutTAAbacusOpportunityCostTemplate.count()):
            item = self.layoutTAAbacusOpportunityCostTemplate.itemAt(i)
            item.widget().setVisible(False)
        
        for i in range(self.layoutTAOpportunityCostCurveTemplate.count()):
            item = self.layoutTAOpportunityCostCurveTemplate.itemAt(i)
            item.widget().setVisible(False)
        
        for i in range(self.layoutTAOpportunityCostMapTemplate.count()):
            item = self.layoutTAOpportunityCostMapTemplate.itemAt(i)
            item.widget().setVisible(False)
        
        self.buttonProcessTAOpportunityCostTemplate = QtGui.QPushButton()
        self.buttonProcessTAOpportunityCostTemplate.setText('Process')
        self.buttonProcessTAOpportunityCostTemplate.setDisabled(True)
        
        self.buttonConfigureTAOpportunityCost = QtGui.QPushButton()
        icon = QtGui.QIcon(':/ui/icons/iconActionConfigure.png')
        self.buttonConfigureTAOpportunityCost.setIcon(icon)
        self.buttonConfigureTAOpportunityCost.setText('Configure')
        self.buttonConfigureTAOpportunityCost.setDisabled(True)
        
        self.layoutSubtabTAOpportunityCost.addWidget(self.groupBoxTAOpportunityCostFeatures)
        self.layoutSubtabTAOpportunityCost.addWidget(self.groupBoxTAOpportunityCostTemplate)
        self.layoutSubtabTAOpportunityCost.addWidget(self.buttonProcessTAOpportunityCostTemplate)
        self.layoutSubtabTAOpportunityCost.addWidget(self.buttonConfigureTAOpportunityCost)
        
        #####################################################################
        
        # TA 'Regional Economy' sub tab dashboard widgets
        self.groupBoxTARegionalEconomyFeatures = QtGui.QGroupBox('Features')
        self.layoutGroupBoxTARegionalEconomyFeatures = QtGui.QVBoxLayout()
        self.groupBoxTARegionalEconomyFeatures.setLayout(self.layoutGroupBoxTARegionalEconomyFeatures)
        
        self.labelTARegionalEconomyFeaturesInfo = QtGui.QLabel()
        self.labelTARegionalEconomyFeaturesInfo.setText('Lorem ipsum dolor sit amet...')
        self.layoutGroupBoxTARegionalEconomyFeatures.addWidget(self.labelTARegionalEconomyFeaturesInfo)
        
        self.radioTARegionalEconomyDescriptiveAnalysis = QtGui.QRadioButton('Descriptive Analysis of Regional Economy')
        self.radioTARegionalEconomyRegionalEconomicScenarioImpact = QtGui.QRadioButton('Regional Economic Scenario Impact')
        self.radioTARegionalEconomyLandRequirementAnalysis = QtGui.QRadioButton('Land Requirement Analysis')
        self.radioTARegionalEconomyLandUseChangeImpact = QtGui.QRadioButton('Land Use Change Impact')
        
        self.layoutGroupBoxTARegionalEconomyFeatures.addWidget(self.radioTARegionalEconomyDescriptiveAnalysis)
        self.layoutGroupBoxTARegionalEconomyFeatures.addWidget(self.radioTARegionalEconomyRegionalEconomicScenarioImpact)
        self.layoutGroupBoxTARegionalEconomyFeatures.addWidget(self.radioTARegionalEconomyLandRequirementAnalysis)
        self.layoutGroupBoxTARegionalEconomyFeatures.addWidget(self.radioTARegionalEconomyLandUseChangeImpact)
        
        self.groupBoxDescriptiveAnalysisPeriod = QtGui.QGroupBox('Period')
        self.layoutGroupBoxDescriptiveAnalysisPeriod = QtGui.QVBoxLayout()
        self.groupBoxDescriptiveAnalysisPeriod.setLayout(self.layoutGroupBoxDescriptiveAnalysisPeriod)
        
        self.labelDescriptiveAnalysisPeriod = QtGui.QLabel()
        self.labelDescriptiveAnalysisPeriod.setText('Lorem ipsum dolot sit amet...')
        self.layoutGroupBoxDescriptiveAnalysisPeriod.addWidget(self.labelDescriptiveAnalysisPeriod)
        
        self.checkBoxDescriptiveAnalysisMultiplePeriod = QtGui.QCheckBox('Multiple Period')
        self.checkBoxDescriptiveAnalysisMultiplePeriod.setChecked(False)
        
        self.layoutGroupBoxDescriptiveAnalysisPeriod.addWidget(self.checkBoxDescriptiveAnalysisMultiplePeriod)
        self.groupBoxDescriptiveAnalysisPeriod.setDisabled(True)
        
        self.groupBoxRegionalEconomicScenarioImpactType = QtGui.QGroupBox('Scenario type')
        self.layoutGroupBoxRegionalEconomicScenarioImpactType = QtGui.QVBoxLayout()
        self.groupBoxRegionalEconomicScenarioImpactType.setLayout(self.layoutGroupBoxRegionalEconomicScenarioImpactType)
        
        self.labelRegionalEconomicScenarioImpactType = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactType.setText('Lorem ipsum dolot sit amet...')
        self.layoutGroupBoxRegionalEconomicScenarioImpactType.addWidget(self.labelRegionalEconomicScenarioImpactType)
        
        self.checkBoxRegionalEconomicScenarioImpactFinalDemand = QtGui.QCheckBox('Final Demand Scenario')
        self.checkBoxRegionalEconomicScenarioImpactFinalDemand.setChecked(True)
        self.checkBoxRegionalEconomicScenarioImpactGDP = QtGui.QCheckBox('GDP Scenario')
        self.checkBoxRegionalEconomicScenarioImpactGDP.setChecked(False)
        
        self.layoutGroupBoxRegionalEconomicScenarioImpactType.addWidget(self.checkBoxRegionalEconomicScenarioImpactFinalDemand)
        self.layoutGroupBoxRegionalEconomicScenarioImpactType.addWidget(self.checkBoxRegionalEconomicScenarioImpactGDP)
        self.groupBoxRegionalEconomicScenarioImpactType.setDisabled(True)
        
        self.groupBoxTARegionalEconomyTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxTARegionalEconomyTemplate = QtGui.QVBoxLayout()
        self.groupBoxTARegionalEconomyTemplate.setLayout(self.layoutGroupBoxTARegionalEconomyTemplate)
        
        self.layoutTARegionalEconomyDescriptiveAnalysisTemplate = QtGui.QHBoxLayout()
        self.layoutTARegionalEconomyRegionalEconomicScenarioImpactTemplate = QtGui.QHBoxLayout()
        self.layoutTARegionalEconomyLandRequirementAnalysisTemplate = QtGui.QHBoxLayout()
        self.layoutTARegionalEconomyLandUseChangeImpactTemplate = QtGui.QHBoxLayout()
        
        # 'Descriptive Analysis' template
        self.labelDescriptiveAnalysisTemplate = QtGui.QLabel()
        self.labelDescriptiveAnalysisTemplate.setText('Template name:')
        self.layoutTARegionalEconomyDescriptiveAnalysisTemplate.addWidget(self.labelDescriptiveAnalysisTemplate)
        
        self.comboBoxDescriptiveAnalysisTemplate = QtGui.QComboBox()
        self.comboBoxDescriptiveAnalysisTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxDescriptiveAnalysisTemplate.setDisabled(True)
        self.comboBoxDescriptiveAnalysisTemplate.addItem('No template found')
        self.layoutTARegionalEconomyDescriptiveAnalysisTemplate.addWidget(self.comboBoxDescriptiveAnalysisTemplate)
        
        # 'Regional Economic Scenario Impact' template
        self.labelRegionalEconomicScenarioImpactTemplate = QtGui.QLabel()
        self.labelRegionalEconomicScenarioImpactTemplate.setText('Template name:')
        self.layoutTARegionalEconomyRegionalEconomicScenarioImpactTemplate.addWidget(self.labelRegionalEconomicScenarioImpactTemplate)
        
        self.comboBoxRegionalEconomicScenarioImpactTemplate = QtGui.QComboBox()
        self.comboBoxRegionalEconomicScenarioImpactTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxRegionalEconomicScenarioImpactTemplate.setDisabled(True)
        self.comboBoxRegionalEconomicScenarioImpactTemplate.addItem('No template found')
        self.layoutTARegionalEconomyRegionalEconomicScenarioImpactTemplate.addWidget(self.comboBoxRegionalEconomicScenarioImpactTemplate)
        
        # 'Land Requirement Analysis' template
        self.labelLandRequirementAnalysisTemplate = QtGui.QLabel()
        self.labelLandRequirementAnalysisTemplate.setText('Template name:')
        self.layoutTARegionalEconomyLandRequirementAnalysisTemplate.addWidget(self.labelLandRequirementAnalysisTemplate)
        
        self.comboBoxLandRequirementAnalysisTemplate = QtGui.QComboBox()
        self.comboBoxLandRequirementAnalysisTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxLandRequirementAnalysisTemplate.setDisabled(True)
        self.comboBoxLandRequirementAnalysisTemplate.addItem('No template found')
        self.layoutTARegionalEconomyLandRequirementAnalysisTemplate.addWidget(self.comboBoxLandRequirementAnalysisTemplate)
        
        # 'Land Use Change Impact Analysis' template
        self.labelLandUseChangeImpactTemplate = QtGui.QLabel()
        self.labelLandUseChangeImpactTemplate.setText('Template name:')
        self.layoutTARegionalEconomyLandUseChangeImpactTemplate.addWidget(self.labelLandUseChangeImpactTemplate)
        
        self.comboBoxLandUseChangeImpactTemplate = QtGui.QComboBox()
        self.comboBoxLandUseChangeImpactTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxLandUseChangeImpactTemplate.setDisabled(True)
        self.comboBoxLandUseChangeImpactTemplate.addItem('No template found')
        self.layoutTARegionalEconomyLandUseChangeImpactTemplate.addWidget(self.comboBoxLandUseChangeImpactTemplate)
        
        self.layoutGroupBoxTARegionalEconomyTemplate.addLayout(self.layoutTARegionalEconomyDescriptiveAnalysisTemplate)
        self.layoutGroupBoxTARegionalEconomyTemplate.addLayout(self.layoutTARegionalEconomyRegionalEconomicScenarioImpactTemplate)
        self.layoutGroupBoxTARegionalEconomyTemplate.addLayout(self.layoutTARegionalEconomyLandRequirementAnalysisTemplate)
        self.layoutGroupBoxTARegionalEconomyTemplate.addLayout(self.layoutTARegionalEconomyLandUseChangeImpactTemplate)
        
        # Hide the templates first until a feature is selected
        for i in range(self.layoutTARegionalEconomyDescriptiveAnalysisTemplate.count()):
            item = self.layoutTARegionalEconomyDescriptiveAnalysisTemplate.itemAt(i)
            item.widget().setVisible(False)
        
        for i in range(self.layoutTARegionalEconomyRegionalEconomicScenarioImpactTemplate.count()):
            item = self.layoutTARegionalEconomyRegionalEconomicScenarioImpactTemplate.itemAt(i)
            item.widget().setVisible(False)
        
        for i in range(self.layoutTARegionalEconomyLandRequirementAnalysisTemplate.count()):
            item = self.layoutTARegionalEconomyLandRequirementAnalysisTemplate.itemAt(i)
            item.widget().setVisible(False)
        
        for i in range(self.layoutTARegionalEconomyLandUseChangeImpactTemplate.count()):
            item = self.layoutTARegionalEconomyLandUseChangeImpactTemplate.itemAt(i)
            item.widget().setVisible(False)
        
        self.buttonProcessTARegionalEconomyTemplate = QtGui.QPushButton()
        self.buttonProcessTARegionalEconomyTemplate.setText('Process')
        self.buttonProcessTARegionalEconomyTemplate.setDisabled(True)
        
        self.buttonConfigureTARegionalEconomy = QtGui.QPushButton()
        icon = QtGui.QIcon(':/ui/icons/iconActionConfigure.png')
        self.buttonConfigureTARegionalEconomy.setIcon(icon)
        self.buttonConfigureTARegionalEconomy.setText('Configure')
        self.buttonConfigureTARegionalEconomy.setDisabled(True)
        
        self.layoutSubtabTARegionalEconomy.addWidget(self.groupBoxTARegionalEconomyFeatures)
        self.layoutSubtabTARegionalEconomy.addWidget(self.groupBoxDescriptiveAnalysisPeriod)
        self.layoutSubtabTARegionalEconomy.addWidget(self.groupBoxRegionalEconomicScenarioImpactType)
        self.layoutSubtabTARegionalEconomy.addWidget(self.groupBoxTARegionalEconomyTemplate)
        self.layoutSubtabTARegionalEconomy.addWidget(self.buttonProcessTARegionalEconomyTemplate)
        self.layoutSubtabTARegionalEconomy.addWidget(self.buttonConfigureTARegionalEconomy)
        
        #####################################################################
        
        # SCIENDO 'Low Emission Development Analysis' sub tab dashboard widgets
        self.groupBoxSCIENDOLowEmissionDevelopmentAnalysisFeatures = QtGui.QGroupBox('Features')
        self.layoutGroupBoxSCIENDOLowEmissionDevelopmentAnalysisFeatures = QtGui.QVBoxLayout()
        self.groupBoxSCIENDOLowEmissionDevelopmentAnalysisFeatures.setLayout(self.layoutGroupBoxSCIENDOLowEmissionDevelopmentAnalysisFeatures)
        
        self.labelSCIENDOLowEmissionDevelopmentAnalysisFeaturesInfo = QtGui.QLabel()
        self.labelSCIENDOLowEmissionDevelopmentAnalysisFeaturesInfo.setText('Lorem ipsum dolor sit amet...')
        self.layoutGroupBoxSCIENDOLowEmissionDevelopmentAnalysisFeatures.addWidget(self.labelSCIENDOLowEmissionDevelopmentAnalysisFeaturesInfo)
        
        self.checkBoxSCIENDOHistoricalBaselineProjection = QtGui.QCheckBox('Historical Baseline Projection')
        self.checkBoxSCIENDOHistoricalBaselineAnnualProjection = QtGui.QCheckBox('Historical Baseline Annual Projection')
        self.checkBoxSCIENDODriversAnalysis = QtGui.QCheckBox('Drivers Analysis')
        self.checkBoxSCIENDOBuildScenario = QtGui.QCheckBox('Build Scenario')
        
        self.layoutGroupBoxSCIENDOLowEmissionDevelopmentAnalysisFeatures.addWidget(self.checkBoxSCIENDOHistoricalBaselineProjection)
        self.layoutGroupBoxSCIENDOLowEmissionDevelopmentAnalysisFeatures.addWidget(self.checkBoxSCIENDOHistoricalBaselineAnnualProjection)
        self.layoutGroupBoxSCIENDOLowEmissionDevelopmentAnalysisFeatures.addWidget(self.checkBoxSCIENDODriversAnalysis)
        self.layoutGroupBoxSCIENDOLowEmissionDevelopmentAnalysisFeatures.addWidget(self.checkBoxSCIENDOBuildScenario)
        
        self.groupBoxSCIENDOLowEmissionDevelopmentAnalysisTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxSCIENDOLowEmissionDevelopmentAnalysisTemplate = QtGui.QVBoxLayout()
        self.groupBoxSCIENDOLowEmissionDevelopmentAnalysisTemplate.setLayout(self.layoutGroupBoxSCIENDOLowEmissionDevelopmentAnalysisTemplate)
        
        self.layoutSCIENDOLowEmissionDevelopmentAnalysisTemplate = QtGui.QHBoxLayout()
        
        # 'Low Emission Development Analysis' template
        self.labelLowEmissionDevelopmentAnalysisTemplate = QtGui.QLabel()
        self.labelLowEmissionDevelopmentAnalysisTemplate.setText('Template name:')
        self.layoutSCIENDOLowEmissionDevelopmentAnalysisTemplate.addWidget(self.labelLowEmissionDevelopmentAnalysisTemplate)
        
        self.comboBoxLowEmissionDevelopmentAnalysisTemplate = QtGui.QComboBox()
        self.comboBoxLowEmissionDevelopmentAnalysisTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxLowEmissionDevelopmentAnalysisTemplate.setDisabled(True)
        self.comboBoxLowEmissionDevelopmentAnalysisTemplate.addItem('No template found')
        self.layoutSCIENDOLowEmissionDevelopmentAnalysisTemplate.addWidget(self.comboBoxLowEmissionDevelopmentAnalysisTemplate)
        
        self.layoutGroupBoxSCIENDOLowEmissionDevelopmentAnalysisTemplate.addLayout(self.layoutSCIENDOLowEmissionDevelopmentAnalysisTemplate)
        
        self.buttonProcessSCIENDOLowEmissionDevelopmentAnalysisTemplate = QtGui.QPushButton()
        self.buttonProcessSCIENDOLowEmissionDevelopmentAnalysisTemplate.setText('Process')
        self.buttonProcessSCIENDOLowEmissionDevelopmentAnalysisTemplate.setDisabled(True)
        
        self.buttonConfigureSCIENDOLowEmissionDevelopmentAnalysis = QtGui.QPushButton()
        icon = QtGui.QIcon(':/ui/icons/iconActionConfigure.png')
        self.buttonConfigureSCIENDOLowEmissionDevelopmentAnalysis.setIcon(icon)
        self.buttonConfigureSCIENDOLowEmissionDevelopmentAnalysis.setText('Configure')
        self.buttonConfigureSCIENDOLowEmissionDevelopmentAnalysis.setDisabled(True)
        
        self.layoutSubtabSCIENDOLowEmissionDevelopmentAnalysis.addWidget(self.groupBoxSCIENDOLowEmissionDevelopmentAnalysisFeatures)
        self.layoutSubtabSCIENDOLowEmissionDevelopmentAnalysis.addWidget(self.groupBoxSCIENDOLowEmissionDevelopmentAnalysisTemplate)
        self.layoutSubtabSCIENDOLowEmissionDevelopmentAnalysis.addWidget(self.buttonProcessSCIENDOLowEmissionDevelopmentAnalysisTemplate)
        self.layoutSubtabSCIENDOLowEmissionDevelopmentAnalysis.addWidget(self.buttonConfigureSCIENDOLowEmissionDevelopmentAnalysis)
        
        #####################################################################
        
        # SCIENDO 'Land Use Change Modeling' sub tab dashboard widgets
        self.groupBoxSCIENDOLandUseChangeModelingFeatures = QtGui.QGroupBox('Features')
        self.layoutGroupBoxSCIENDOLandUseChangeModelingFeatures = QtGui.QVBoxLayout()
        self.groupBoxSCIENDOLandUseChangeModelingFeatures.setLayout(self.layoutGroupBoxSCIENDOLandUseChangeModelingFeatures)
        
        self.labelSCIENDOLandUseChangeModelingFeaturesInfo = QtGui.QLabel()
        self.labelSCIENDOLandUseChangeModelingFeaturesInfo.setText('Lorem ipsum dolor sit amet...')
        self.layoutGroupBoxSCIENDOLandUseChangeModelingFeatures.addWidget(self.labelSCIENDOLandUseChangeModelingFeaturesInfo)
        
        self.checkBoxSCIENDOCreateRasterCubeOfFactors = QtGui.QCheckBox('Create Raster Cube of Factors')
        self.checkBoxSCIENDOCalculateTransitionMatrix = QtGui.QCheckBox('Calculate Transition Matrix')
        # self.checkBoxSCIENDOCalculateWeightOfEvidence = QtGui.QCheckBox('Calculate Weight of Evidence')
        self.checkBoxSCIENDOSimulateLandUseChange = QtGui.QCheckBox('Simulate Land Use Change')
        self.checkBoxSCIENDOSimulateWithScenario = QtGui.QCheckBox('Simulate With Scenario')
        
        self.layoutGroupBoxSCIENDOLandUseChangeModelingFeatures.addWidget(self.checkBoxSCIENDOCreateRasterCubeOfFactors)
        self.layoutGroupBoxSCIENDOLandUseChangeModelingFeatures.addWidget(self.checkBoxSCIENDOCalculateTransitionMatrix)
        # self.layoutGroupBoxSCIENDOLandUseChangeModelingFeatures.addWidget(self.checkBoxSCIENDOCalculateWeightOfEvidence)
        self.layoutGroupBoxSCIENDOLandUseChangeModelingFeatures.addWidget(self.checkBoxSCIENDOSimulateLandUseChange)
        self.layoutGroupBoxSCIENDOLandUseChangeModelingFeatures.addWidget(self.checkBoxSCIENDOSimulateWithScenario)
        
        self.groupBoxSCIENDOLandUseChangeModelingTemplate = QtGui.QGroupBox('Template')
        self.layoutGroupBoxSCIENDOLandUseChangeModelingTemplate = QtGui.QVBoxLayout()
        self.groupBoxSCIENDOLandUseChangeModelingTemplate.setLayout(self.layoutGroupBoxSCIENDOLandUseChangeModelingTemplate)
        
        self.layoutSCIENDOLandUseChangeModelingTemplate = QtGui.QHBoxLayout()
        
        # 'Land Use Change Modeling' template
        self.labelLandUseChangeModelingTemplate = QtGui.QLabel()
        self.labelLandUseChangeModelingTemplate.setText('Template name:')
        self.layoutSCIENDOLandUseChangeModelingTemplate.addWidget(self.labelLandUseChangeModelingTemplate)
        
        self.comboBoxLandUseChangeModelingTemplate = QtGui.QComboBox()
        self.comboBoxLandUseChangeModelingTemplate.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.comboBoxLandUseChangeModelingTemplate.setDisabled(True)
        self.comboBoxLandUseChangeModelingTemplate.addItem('No template found')
        self.layoutSCIENDOLandUseChangeModelingTemplate.addWidget(self.comboBoxLandUseChangeModelingTemplate)
        
        self.layoutGroupBoxSCIENDOLandUseChangeModelingTemplate.addLayout(self.layoutSCIENDOLandUseChangeModelingTemplate)
        
        self.buttonProcessSCIENDOLandUseChangeModelingTemplate = QtGui.QPushButton()
        self.buttonProcessSCIENDOLandUseChangeModelingTemplate.setText('Process')
        self.buttonProcessSCIENDOLandUseChangeModelingTemplate.setDisabled(True)
        
        self.buttonConfigureSCIENDOLandUseChangeModeling = QtGui.QPushButton()
        icon = QtGui.QIcon(':/ui/icons/iconActionConfigure.png')
        self.buttonConfigureSCIENDOLandUseChangeModeling.setIcon(icon)
        self.buttonConfigureSCIENDOLandUseChangeModeling.setText('Configure')
        self.buttonConfigureSCIENDOLandUseChangeModeling.setDisabled(True)
        
        self.layoutSubtabSCIENDOLandUseChangeModeling.addWidget(self.groupBoxSCIENDOLandUseChangeModelingFeatures)
        self.layoutSubtabSCIENDOLandUseChangeModeling.addWidget(self.groupBoxSCIENDOLandUseChangeModelingTemplate)
        self.layoutSubtabSCIENDOLandUseChangeModeling.addWidget(self.buttonProcessSCIENDOLandUseChangeModelingTemplate)
        self.layoutSubtabSCIENDOLandUseChangeModeling.addWidget(self.buttonConfigureSCIENDOLandUseChangeModeling)
        
        #***********************************************************
        # End 'Dashboard' tab setup
        #***********************************************************
        
        self.groupBoxProjectLayers = QtGui.QGroupBox('Layers')
        self.layoutGroupBoxProjectLayers = QtGui.QHBoxLayout()
        self.groupBoxProjectLayers.setLayout(self.layoutGroupBoxProjectLayers)
        
        self.groupBoxProjectExplore = QtGui.QGroupBox('Explore')
        self.layoutGroupBoxProjectExplore = QtGui.QVBoxLayout()
        self.groupBoxProjectExplore.setLayout(self.layoutGroupBoxProjectExplore)
        
        #self.layoutTabLayers.addWidget(self.layerListView)
        #self.layoutTabLayers.addWidget(self.projectTreeView)
        self.layoutGroupBoxProjectLayers.addWidget(self.layerListView)
        self.layoutGroupBoxProjectExplore.addWidget(self.projectTreeView)
        self.layoutTabLayers.addWidget(self.groupBoxProjectLayers)
        self.layoutTabLayers.addWidget(self.groupBoxProjectExplore)
        #self.layoutTabDashboard.addWidget(self.dashboardTabWidget)
        #self.layoutTabProject.addWidget(self.projectTreeView)
        
        self.layersToolBar = QtGui.QToolBar(self)
        self.layersToolBar.setOrientation(QtCore.Qt.Vertical)
        self.layersToolBar.addAction(self.actionAddLayer)
        self.layersToolBar.addAction(self.actionLayerAttributeTable)
        self.layersToolBar.addAction(self.actionLayerAttributeEditor)
        self.layersToolBar.addAction(self.actionLayerProperties)
        self.layersToolBar.addAction(self.actionDeleteLayer)
        self.layoutGroupBoxProjectLayers.addWidget(self.layersToolBar)
        
        self.databaseToolBar = QtGui.QToolBar(self)
        self.databaseToolBar.setIconSize(QtCore.QSize(32, 32))
        self.databaseToolBar.addAction(self.actionDialogLumensCreateDatabase)
        self.databaseToolBar.addAction(self.actionLumensOpenDatabase)
        self.databaseToolBar.addAction(self.actionLumensCloseDatabase)
        self.databaseToolBar.addAction(self.actionLumensExportDatabase)
        self.databaseToolBar.addAction(self.actionDialogLumensAddData)
        self.databaseToolBar.addAction(self.actionLumensDeleteData)
        self.databaseToolBar.addAction(self.actionLumensDatabaseStatus)
        self.databaseToolBar.setStyleSheet('QToolBar QToolButton::hover{ background-color: rgb(225, 229, 237); }')
        self.layoutTabDatabase.addWidget(self.databaseToolBar)
        
        self.webContentDatabaseStatus = QtWebKit.QWebView(self)
        
        self.groupBoxDatabaseStatus = QtGui.QGroupBox('Database status')
        self.layoutGroupBoxDatabaseStatus = QtGui.QVBoxLayout()
        self.groupBoxDatabaseStatus.setLayout(self.layoutGroupBoxDatabaseStatus)
        self.layoutTabDatabase.addWidget(self.groupBoxDatabaseStatus)
        self.layoutGroupBoxDatabaseStatus.addWidget(self.webContentDatabaseStatus)
        
        # Floating sidebar
        self.sidebarDockWidget = QtGui.QDockWidget('Dashboard', self) # Formerly 'Sidebar'
        self.sidebarDockWidget.setContentsMargins(5, 10, 5, 5)
        self.sidebarDockWidget.setFeatures(self.sidebarDockWidget.features() & QtGui.QDockWidget.AllDockWidgetFeatures)
        self.sidebarDockWidget.setWidget(self.sidebarTabWidget)
        self.sidebarDockWidget.setStyleSheet('QDockWidget { background-color: rgb(225, 229, 237); } QToolBar { border: none; }') # Remove border for all child QToolBar in sidebar
        self.sidebarDockWidget.setFloating(True)
        self.sidebarDockWidget.setMinimumHeight(520)
        self.sidebarDockWidgetAction = self.sidebarDockWidget.toggleViewAction()
        
        # Add view menu
        self.viewMenu.addAction(self.actionToggleMenubar)
        self.viewMenu.addAction(self.sidebarDockWidgetAction)
        self.viewMenu.addAction(self.actionToggleDialogToolbar)
        self.viewMenu.addAction(self.actionToggleToolbar)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.actionZoomIn)
        self.viewMenu.addAction(self.actionZoomOut)
        self.viewMenu.addAction(self.actionPanSelected)
        self.viewMenu.addAction(self.actionZoomFull)
        self.viewMenu.addAction(self.actionZoomLayer)
        self.viewMenu.addAction(self.actionZoomSelected)
        self.viewMenu.addAction(self.actionZoomLast)
        self.viewMenu.addAction(self.actionZoomNext)
        self.viewMenu.addAction(self.actionRefresh)        
        
        # LayoutBody holds the map canvas widget
        self.layoutBody = QtGui.QHBoxLayout()
        self.layoutBody.setContentsMargins(0, 0, 0, 0)
        self.layoutBody.setAlignment(QtCore.Qt.AlignLeft)
        
        # Vertical layout for widgets: splitterMain (map canvas widget, log widget), then active project
        self.layoutMain = QtGui.QVBoxLayout()
        # Reduce gap with statusbar
        self.layoutMain.setContentsMargins(5, 5, 5, 0)
        
        self.contentBody = QtGui.QWidget()
        self.contentBody.setLayout(self.layoutBody)
        
        self.log_box = QPlainTextEditLogger(self)
        self.log_box.widget.setStyleSheet('QPlainTextEdit { color: rgb(225, 229, 237); }')
        # Show the logging widget only in debug mode
        if not self.appSettings['debug']:
            self.log_box.widget.setVisible(False)
        
        # splitterMain vertically (top down, not left right) splits the map canvas widget and log widget
        self.splitterMain = QtGui.QSplitter(self)
        self.splitterMain.setOrientation(QtCore.Qt.Vertical)
        self.splitterMain.addWidget(self.contentBody)
        self.splitterMain.addWidget(self.log_box.widget)
        # Don't collapse contentBody (mapCanvas)
        self.splitterMain.setCollapsible(0, False)
        self.splitterMain.setSizes([550, 50])
        
        self.layoutMain.addWidget(self.splitterMain)
        self.layoutMain.addLayout(self.layoutActiveProject)
        
        self.centralWidget.setLayout(self.layoutMain)
        
        # Initialize the mapcanvas and map tools
        # Enable on the fly CRS projection
        # Use PAL labeling engine
        self.mapCanvas = QgsMapCanvas()
        self.mapCanvas.useImageToRender(False)
        self.mapCanvas.mapRenderer().setProjectionsEnabled(True)
        self.mapCanvas.mapRenderer().setDestinationCrs(QgsCoordinateReferenceSystem(self.appSettings['defaultCRS'], QgsCoordinateReferenceSystem.EpsgCrsId))
        labelingEngine = QgsPalLabeling()
        self.mapCanvas.mapRenderer().setLabelingEngine(labelingEngine)
        self.mapCanvas.setCanvasColor(QtCore.Qt.white)
        self.mapCanvas.enableAntiAliasing(True)
        
        # Initialize the map tools and assign to the related action
        self.panTool = PanTool(self.mapCanvas)
        self.panTool.setAction(self.actionPan)
        
        self.selectTool = SelectTool(self)
        self.selectTool.setAction(self.actionSelect)

        self.infoTool = InfoTool(self)
        self.infoTool.setAction(self.actionInfo)
        
        # Causes mainwindow size to fill screen ignoring setMinimumSize()
        ##self.resize(self.sizeHint())
    
    
    def resizeEvent(self, event):
        """Overload method that is called when the window is resized.
        
        Places floating widgets relative to the parent window.
        
        Args:
            event (QEvent): the resize event that is triggered.
        """
        parentPosition = self.mapToGlobal(QtCore.QPoint(0, 0))
        
        yMargin = 100
        
        # Near top left
        self.toolBar.show()
        
        # Near top right
        self.sidebarDockWidget.move(parentPosition.x() + self.width() - self.sidebarDockWidget.width() - 35, parentPosition.y() + yMargin)
        
        super(MainWindow, self).resizeEvent(event)
    
    
    def eventFilter(self, source, event):
        """Overload method that is called on defined events.
        
        This method is called every time on the defined events in the LUMENS main window.
        
        Args:
            source (QObject): the source widget of the event.
            event (QEvent): the event that is triggered.
        """
        if event.type() == QtCore.QEvent.WindowActivate:
            print 'widget window has gained focus'
            if not self.appSettings['DialogLumensOpenDatabase']['projectFile']:
                self.actionLumensCloseDatabase.setDisabled(True)
                self.lumensDisableMenus()
            else:
                self.lumensEnableMenus()
        elif event.type() == QtCore.QEvent.WindowDeactivate:
            print 'widget window has lost focus'
        elif event.type() == QtCore.QEvent.FocusIn:
            print 'widget has gained keyboard focus'
        elif event.type() == QtCore.QEvent.FocusOut:
            print 'widget has lost keyboard focus'
        elif event.type() == QtCore.QEvent.Drop and source == self.layerListView.viewport():
            self.handlerDropLayer()
        
        return False
    
    
    def closeEvent(self, event):
        """Save LUMENS application settings on window close event.
        
        Method that is called on main window closing. Stores the "recentProjects" list
        to the default .ini settings file in the app directory.
        """
        settings = QtCore.QSettings(self.appSettings['appSettingsFile'], QtCore.QSettings.IniFormat)
        settings.setFallbacksEnabled(True) # only use ini files
        settings.setValue('recentProjects', self.recentProjects)
    
    
    def addRecentProject(self, projectFile):
        """Add a project file to the "recentProjects" list.
        
        Method that is called when a LUMENS project file (*.lpj) is opened. Limited to 10
        recently opened projects.
        
        Args:
            projectFile (str): a file path to a LUMENS project file.
        """
        if projectFile is None:
            return
        if projectFile not in self.recentProjects:
            self.recentProjects.insert(0, projectFile)
            while len(self.recentProjects) > 10:
                self.recentProjects.pop()
    
    
    def loadSettings(self):
        """Load LUMENS application settings from the default settings file
        
        Loads the values from the default .ini settings file in the app directory.
        """
        settings = QtCore.QSettings(self.appSettings['appSettingsFile'], QtCore.QSettings.IniFormat)
        settings.setFallbacksEnabled(True) # only use ini files
        recentProjects = settings.value('recentProjects')
        if recentProjects:
            self.recentProjects = recentProjects
    
    
    def updateFileMenu(self):
        """Slot method for updating the visible actions in the file menu.
        
        Updating is perform each time the file menu is clicked.
        """
        recentProjects = []
        
        self.fileMenu.clear()
        
        # Populate file menu with recently opened project databases
        for projectFile in self.recentProjects:
            if os.path.exists(projectFile):
                recentProjects.append(projectFile)
        
        if recentProjects:
            self.fileMenu.addSeparator()
            
            for i, projectFile in enumerate(recentProjects):
                action = QtGui.QAction('&{0} {1}'.format(i + 1, os.path.basename(projectFile)), self)
                action.setData(projectFile)
                action.triggered.connect(self.lumensOpenDatabase)
                self.fileMenu.addAction(action)
            
            self.fileMenu.addSeparator()
        
        self.fileMenu.addAction(self.actionQuit)
    
    
    def openDialog(self, DialogClass, tabName='', showDialog=True):
        """Method for opening and keeping track of opened module dialogs instances.
        
        Open and keep track of already opened dialog instances instead of creating new ones.
        This allow input fields that have been set to persist when the dialog window is reopened.
        
        Args:
            DialogClass (str): class name of the dialog.
            showDialog (bool): show the dialog or return the dialog instance instead.
        """
        dialog = None
        
        for dlg in self.openDialogs:
            if isinstance(dlg, DialogClass):
                dialog = dlg
                break
        
        if not dialog:
            dialog = DialogClass(self)
            self.openDialogs.append(dialog)
        
        if showDialog:
            if tabName:
                if tabName == 'Pre-QUES':
                    dialog.tabWidget.setCurrentWidget(dialog.tabPreQUES)
                elif tabName == 'QUES-C':
                    dialog.tabWidget.setCurrentWidget(dialog.tabQUESC)
                elif tabName == 'QUES-B':
                    dialog.tabWidget.setCurrentWidget(dialog.tabQUESB)
                elif tabName == 'QUES-H':
                    dialog.tabWidget.setCurrentWidget(dialog.tabQUESH)
                elif tabName == 'Abacus Opportunity Cost':
                    dialog.tabWidget.setCurrentWidget(dialog.tabAbacusOpportunityCost)
                elif tabName == 'Opportunity Cost Curve':
                    dialog.tabWidget.setCurrentWidget(dialog.tabOpportunityCostCurve)
                elif tabName == 'Opportunity Cost Map':
                    dialog.tabWidget.setCurrentWidget(dialog.tabOpportunityCostMap)
                elif tabName == 'Descriptive Analysis of Regional Economy':
                    dialog.tabWidget.setCurrentWidget(dialog.tabDescriptiveAnalysis)
                elif tabName == 'Regional Economic Scenario Impact':
                    dialog.tabWidget.setCurrentWidget(dialog.tabRegionalEconomicScenarioImpact)
                elif tabName == 'Land Requirement Analysis':
                    dialog.tabWidget.setCurrentWidget(dialog.tabLandRequirementAnalysis)
                elif tabName == 'Land Use Change Impact':
                    dialog.tabWidget.setCurrentWidget(dialog.tabLandUseChangeImpact)
                elif tabName == 'Low Emission Development Analysis':
                    dialog.tabWidget.setCurrentWidget(dialog.tabLowEmissionDevelopmentAnalysis)
                elif tabName == 'Land Use Change Modeling':
                    dialog.tabWidget.setCurrentWidget(dialog.tabLandUseChangeModeling)
            dialog.exec_()
        else:
            return dialog
    
    
    def closeDialogs(self):
        """Method for closing all opened dialogs and mark for deletion by Qt.
        
        All dialogs in "openDialogs" list are marked for deletion and cleared.
        This is called when a LUMENS project is closed.
        """
        for dlg in self.openDialogs:
            dlg.deleteLater()
        
        self.openDialogs = []
    
    
    def lumensEnableMenus(self):
        """Method for enabling menus that require an open LUMENS project.
        """
        # Database menu
        self.actionLumensCloseDatabase.setEnabled(True)
        self.actionLumensExportDatabase.setEnabled(True)
        self.actionLumensDatabaseStatus.setEnabled(True)
        self.actionLumensDeleteData.setEnabled(True)
        self.actionDialogLumensAddData.setEnabled(True)
        
        # PUR menu
        self.actionDialogLumensPUR.setEnabled(True)
        self.buttonConfigurePUR.setEnabled(True)
        
        # QUES menu
        self.actionDialogLumensQUES.setEnabled(True)
        self.buttonConfigurePreQUES.setEnabled(True)
        self.buttonConfigureQUESC.setEnabled(True)
        self.buttonConfigureQUESB.setEnabled(True)
        self.buttonConfigureQUESH.setEnabled(True)
        
        # TA menu
        self.actionDialogLumensTAOpportunityCost.setEnabled(True)
        self.actionDialogLumensTARegionalEconomy.setEnabled(True)
        self.buttonConfigureTAOpportunityCost.setEnabled(True)
        self.buttonConfigureTARegionalEconomy.setEnabled(True)
        
        # SCIENDO menu
        self.actionDialogLumensSCIENDO.setEnabled(True)
        self.buttonConfigureSCIENDOLowEmissionDevelopmentAnalysis.setEnabled(True)
        self.buttonConfigureSCIENDOLandUseChangeModeling.setEnabled(True)
    
    
    def lumensDisableMenus(self):
        """Method for disabling menus that require an open LUMENS project.
        """
        # Database menu
        self.actionLumensExportDatabase.setDisabled(True)
        self.actionLumensDatabaseStatus.setDisabled(True)
        self.actionDialogLumensAddData.setDisabled(True)
        self.actionLumensDeleteData.setDisabled(True)
        
        # PUR menu
        self.actionDialogLumensPUR.setDisabled(True)
        self.buttonConfigurePUR.setDisabled(True)
        
        # QUES menu
        self.actionDialogLumensQUES.setDisabled(True)
        self.buttonConfigureQUESC.setDisabled(True)
        self.buttonConfigureQUESB.setDisabled(True)
        self.buttonConfigureQUESH.setDisabled(True)
        
        # TA menu
        self.actionDialogLumensTAOpportunityCost.setDisabled(True)
        self.actionDialogLumensTARegionalEconomy.setDisabled(True)
        self.buttonConfigureTAOpportunityCost.setDisabled(True)
        self.buttonConfigureTARegionalEconomy.setDisabled(True)
        
        # SCIENDO menu
        self.actionDialogLumensSCIENDO.setDisabled(True)
        self.buttonConfigureSCIENDOLowEmissionDevelopmentAnalysis.setDisabled(True)
        self.buttonConfigureSCIENDOLandUseChangeModeling.setDisabled(True)
    
    
    def loadModuleTemplates(self):
        """Method for loading the list of all the module templates of a LUMENS project.
        
        Module template files exist in the module subfolder of the project folder.
        This is called when a LUMENS project is opened so that the module
        templates are listed on the main window's dashboard tab.
        """
        dialogLumensPUR = self.openDialog(DialogLumensPUR, showDialog=False)
        dialogLumensQUES = self.openDialog(DialogLumensQUES, showDialog=False)
        dialogLumensTAOpportunityCost = self.openDialog(DialogLumensTAOpportunityCost, showDialog=False)
        dialogLumensTARegionalEconomy = self.openDialog(DialogLumensTARegionalEconomy, showDialog=False)
        dialogLumensSCIENDO = self.openDialog(DialogLumensSCIENDO, showDialog=False)
        
        dialogLumensPUR.loadTemplateFiles()
        dialogLumensQUES.loadTemplateFiles()
        dialogLumensTAOpportunityCost.loadTemplateFiles()
        dialogLumensTARegionalEconomy.loadTemplateFiles()
        dialogLumensSCIENDO.loadTemplateFiles()
    
    
    def clearModuleTemplates(self):
        """Method for clearing the list of all modules templates on the main window's dashboard tab.
        
        This is called when a LUMENS project is closed.
        """
        # PUR
        self.comboBoxPURTemplate.clear()
        self.comboBoxPURTemplate.addItem('No template found')
        self.comboBoxPURTemplate.setDisabled(True)
        
        # QUES
        self.comboBoxPreQUESTemplate.clear()
        self.comboBoxPreQUESTemplate.addItem('No template found')
        self.comboBoxPreQUESTemplate.setDisabled(True)
        
        self.comboBoxQUESCTemplate.clear()
        self.comboBoxQUESCTemplate.addItem('No template found')
        self.comboBoxQUESCTemplate.setDisabled(True)
        
        self.comboBoxQUESBTemplate.clear()
        self.comboBoxQUESBTemplate.addItem('No template found')
        self.comboBoxQUESBTemplate.setDisabled(True)
        
        self.comboBoxHRUDefinitionTemplate.clear()
        self.comboBoxHRUDefinitionTemplate.addItem('No template found')
        self.comboBoxHRUDefinitionTemplate.setDisabled(True)
        
        self.comboBoxWatershedModelEvaluationTemplate.clear()
        self.comboBoxWatershedModelEvaluationTemplate.addItem('No template found')
        self.comboBoxWatershedModelEvaluationTemplate.setDisabled(True)
        
        self.comboBoxWatershedIndicatorsTemplate.clear()
        self.comboBoxWatershedIndicatorsTemplate.addItem('No template found')
        self.comboBoxWatershedIndicatorsTemplate.setDisabled(True)
        
        # TA
        self.comboBoxAbacusOpportunityCostTemplate.clear()
        self.comboBoxAbacusOpportunityCostTemplate.addItem('No template found')
        self.comboBoxAbacusOpportunityCostTemplate.setDisabled(True)
        
        self.comboBoxOpportunityCostCurveTemplate.clear()
        self.comboBoxOpportunityCostCurveTemplate.addItem('No template found')
        self.comboBoxOpportunityCostCurveTemplate.setDisabled(True)
        
        self.comboBoxOpportunityCostMapTemplate.clear()
        self.comboBoxOpportunityCostMapTemplate.addItem('No template found')
        self.comboBoxOpportunityCostMapTemplate.setDisabled(True)
        
        self.comboBoxDescriptiveAnalysisTemplate.clear()
        self.comboBoxDescriptiveAnalysisTemplate.addItem('No template found')
        self.comboBoxDescriptiveAnalysisTemplate.setDisabled(True)
        
        self.comboBoxRegionalEconomicScenarioImpactTemplate.clear()
        self.comboBoxRegionalEconomicScenarioImpactTemplate.addItem('No template found')
        self.comboBoxRegionalEconomicScenarioImpactTemplate.setDisabled(True)
        
        self.comboBoxLandRequirementAnalysisTemplate.clear()
        self.comboBoxLandRequirementAnalysisTemplate.addItem('No template found')
        self.comboBoxLandRequirementAnalysisTemplate.setDisabled(True)
        
        self.comboBoxLandUseChangeImpactTemplate.clear()
        self.comboBoxLandUseChangeImpactTemplate.addItem('No template found')
        self.comboBoxLandUseChangeImpactTemplate.setDisabled(True)
        
        # SCIENDO
        self.comboBoxLowEmissionDevelopmentAnalysisTemplate.clear()
        self.comboBoxLowEmissionDevelopmentAnalysisTemplate.addItem('No template found')
        self.comboBoxLowEmissionDevelopmentAnalysisTemplate.setDisabled(True)
        
        self.comboBoxLandUseChangeModelingTemplate.clear()
        self.comboBoxLandUseChangeModelingTemplate.addItem('No template found')
        self.comboBoxLandUseChangeModelingTemplate.setDisabled(True)
        
    
    def lumensLoadQgsProjectLayers(self, qgsProject):
        """Method for loading layers defined in a QGIS project file to the layer list.
        
        Args:
            qgsProject (str): a file path to a QGIS project file (*.qgs).
        """
        xml = file(qgsProject).read()
        doc = QtXml.QDomDocument()
        doc.setContent(xml)
        mapLayers = doc.elementsByTagName('maplayer')
        
        layerFiles = []
        
        if mapLayers.count():
            for i in range(mapLayers.count()):
                mapLayer = mapLayers.at(i)
                if mapLayer.isElement():
                    dataSource = mapLayer.firstChildElement('datasource')
                    layerFile = dataSource.text()
                    if os.path.exists(layerFile):
                        layerFiles.append(layerFile)
        
        if len(layerFiles):
            reply = QtGui.QMessageBox.question(
                self,
                'Load QGIS Project Layers',
                'Do you want to load the layers in the QGIS project?',
                QtGui.QMessageBox.Yes|QtGui.QMessageBox.Cancel,
                QtGui.QMessageBox.Cancel
            )
            
            if reply == QtGui.QMessageBox.Yes:
                self.sidebarTabWidget.setCurrentWidget(self.tabLayers)
                for layerFile in layerFiles:
                    self.addLayer(layerFile)
    
    
    def loadAddedDataInfo(self):
        """Method for loading the list of added data.
        
        Looks in the DATA dir of the currently open project.
        """
        self.clearAddedDataInfo()
        
        csvDataLandUseCover = os.path.join(self.appSettings['folderTemp'], 'csv_land_use_cover.csv')
        csvDataPlanningUnit = os.path.join(self.appSettings['folderTemp'], 'csv_planning_unit.csv')
        csvDataFactor = os.path.join(self.appSettings['folderTemp'], 'csv_factor_data.csv')
        csvDataTable = os.path.join(self.appSettings['folderTemp'], 'csv_lookup_table.csv')
        
        if os.path.exists(csvDataLandUseCover):
            with open(csvDataLandUseCover, 'rb') as f:
              reader = csv.reader(f)
              
              # Skip header row
              headerRow = reader.next()
              headerColumns = [str(column) for column in headerRow]
              
              dataLandUseCover = {}
              
              for row in reader:
                  dataLandUseCover[row[0]] = {
                      'RST_DATA': row[0],
                      'RST_NAME': row[1],
                      'PERIOD': row[2],
                      'LUT_NAME': row[3],
                  }
                  
              self.dataLandUseCover = dataLandUseCover
        
        if os.path.exists(csvDataPlanningUnit):
            with open(csvDataPlanningUnit, 'rb') as f:
              reader = csv.reader(f)
              
              # Skip header row
              headerRow = reader.next()
              headerColumns = [str(column) for column in headerRow]
              
              dataPlanningUnit = {}
              
              for row in reader:
                  dataPlanningUnit[row[0]] = {
                      'RST_DATA': row[0],
                      'RST_NAME': row[1],
                      'LUT_NAME': row[2],
                  }
              
              self.dataPlanningUnit = dataPlanningUnit
        
        if os.path.exists(csvDataFactor):
            with open(csvDataFactor, 'rb') as f:
              reader = csv.reader(f)
              
              # Skip header row
              headerRow = reader.next()
              headerColumns = [str(column) for column in headerRow]
              
              dataFactor = {}
              
              for row in reader:
                  dataFactor[row[0]] = {
                      'RST_DATA': row[0],
                      'RST_NAME': row[1],
                  }
              
              self.dataFactor = dataFactor
      
        if os.path.exists(csvDataTable):
            with open(csvDataTable, 'rb') as f:
              reader = csv.reader(f)
              
              # Skip header row
              headerRow = reader.next()
              headerColumns = [str(column) for column in headerRow]
              
              dataTable = {}
              
              for row in reader:
                  dataTable[row[0]] = {
                      'TBL_DATA': row[0],
                      'TBL_NAME': row[1],
                  }
              
              self.dataTable = dataTable
    
    
    def clearAddedDataInfo(self):
        """Method for clearing the list of added data info.
        
        This is called when a LUMENS project is closed.
        """
        self.dataLandUseCover = {}
        self.dataPlanningUnit = {}
        self.dataFactor = {}
        self.dataTable = {}
    
    
    def lumensOpenDatabase(self, lumensDatabase=False):
        """Method for opening a LUMENS project database.
        
        Opens a LUMENS project database file (*.lpj) using "r:lumensopendatabase" R algorithm.
        This is called when opening a recent project from the file menu or the "Open LUMENS database" menu.
        When a LUMENS project is opened, menus that depend on an open project will be enabled and all
        of the project's module templates will be listed on the main window's dashboard tab.
        
        Args:
            lumensDatabase (bool): if False then open the LUMENS project from the "recentProjects" list.
        """
        if lumensDatabase is False: # Recent projects
            action = self.sender()
            if isinstance(action, QtGui.QAction):
                lumensDatabase = unicode(action.data())
            else:
                return
        
        # Close the currently opened database first
        if self.appSettings['DialogLumensOpenDatabase']['projectFile']:
            self.lumensCloseDatabase()
        
        logging.getLogger(type(self).__name__).info('start: LUMENS Open Database')
        self.actionLumensOpenDatabase.setDisabled(True)
        
        outputs = general.runalg(
            'r:dbopen',
            lumensDatabase.replace(os.path.sep, '/'),
            None
        )
        
        if outputs:
            ##print outputs
            self.addLayer(outputs['overview'])
            
            self.appSettings['DialogLumensOpenDatabase']['projectFile'] = lumensDatabase
            self.appSettings['DialogLumensOpenDatabase']['projectFolder'] = projectFolder = os.path.dirname(lumensDatabase)
            
            self.lineEditActiveProject.setText(os.path.normpath(lumensDatabase))
            self.projectTreeView.setRootIndex(self.projectModel.index(self.appSettings['DialogLumensOpenDatabase']['projectFolder']))
            self.addRecentProject(lumensDatabase)
            
            # Keep track of added data stored in the open project's DATA dir
            self.loadAddedDataInfo()
            
            # Load all module templates in the open project
            self.loadModuleTemplates()
            
            # Enable the menus
            self.lumensEnableMenus()
        
        self.actionLumensOpenDatabase.setEnabled(True)
        logging.getLogger(type(self).__name__).info('end: LUMENS Open Database')


    def lumensImportDatabase(self, workingDir, lumensDatabase):
        """Method for importing an archived LUMENS project database  
        
        Imports an archived LUMENS project using "r:dbimport" R algorithm.
        An archived file can be obtained from export database function. It will be 
        imported lpj file and the folder DATA which are previously generated from other
        process to selected new working directory.
        
        
        Args:
            zipFile: an archived file (.zip)
            workingDir: new working directory to be imported
        """
        logging.getLogger(type(self).__name__).info('start: LUMENS Import Database')
        self.actionLumensOpenDatabase.setDisabled(True)
        
        outputs = general.runalg(
            'r:dbimport',
            zipFile.replace(os.path.sep, '/'),
            workingDir.replace(os.path.sep, '/'),
            None,
            None,
        )
        
        self.actionLumensOpenDatabase.setEnabled(True)
        logging.getLogger(type(self).__name__).info('end: LUMENS Import Database') 
        
        return outputs
        
        
    def lumensExportDatabase(self):
        """Method for exporting a LUMENS project database

        Export a whole directory, subdirectory, project files, database
        and archive into a zip file
        """
        logging.getLogger(type(self).__name__).info('start: LUMENS Export Database')

        general.runalg('r:dbexport', self.appSettings['DialogLumensOpenDatabase']['projectFile'].replace(os.path.sep, '/'))

        logging.getLogger(type(self).__name__).info('end: LUMENS Export Database')        

    
    def lumensCloseDatabase(self):
        """Method for closing a LUMENS project database.
        
        Closes an open LUMENS project using "modeler:lumens_close_database" R algorithm.
        When a LUMENS project is closed, menus that depend on an open project will be disabled and all
        of the project's module templates will be unlisted from the main window's dashboard tab.
        """
        logging.getLogger(type(self).__name__).info('start: LUMENS Close Database')
        self.actionLumensCloseDatabase.setDisabled(True)
        
        outputs = general.runalg(
            'r:dbclose',
            self.appSettings['DialogLumensOpenDatabase']['projectFile'].replace(os.path.sep, '/')
        )        
        
        self.appSettings['DialogLumensOpenDatabase']['projectFile'] = ''
        self.appSettings['DialogLumensOpenDatabase']['projectFolder'] = ''
        
        self.lineEditActiveProject.clear()
        self.projectTreeView.setRootIndex(self.projectModel.index(QtCore.QDir.rootPath()))
        
        # Unset everything
        self.closeDialogs()
        self.clearModuleTemplates()
        self.clearAddedDataInfo()
        self.lumensDisableMenus()
        
        logging.getLogger(type(self).__name__).info('end: LUMENS Close Database')
    
    
    def lumensDatabaseStatus(self):
        """Method for display the project database stats in a popup dialog.
        
        Shows the database status of the current active LUMENS project in a
        dialog window using the "r:lumensdatabasestatus" R algorithm.
        """
        logging.getLogger(type(self).__name__).info('start: lumensdatabasestatus')
        self.actionLumensDatabaseStatus.setDisabled(True)
        
        outputs = general.runalg('r:dbstatus', self.appSettings['DialogLumensOpenDatabase']['projectFile'].replace(os.path.sep, '/'), None)
        
        if outputs:
            self.webContentDatabaseStatus.load(QtCore.QUrl.fromLocalFile(os.path.join(self.appSettings['DialogLumensOpenDatabase']['projectFolder'], "status_LUMENS_database.html")))
            #dialog = DialogLumensViewer(self, 'Database Status', 'csv', outputs['database_status'])
            #dialog = DialogLumensViewer(self, 'Database Status', 'html', os.path.join(self.appSettings['DialogLumensOpenDatabase']['projectFolder'], "status_LUMENS_database.html"))
            #dialog.exec_()
        
        self.actionLumensDatabaseStatus.setEnabled(True)
        logging.getLogger(type(self).__name__).info('end: lumensdatabasestatus')
    
    
    def lumensDeleteData(self):
        """Method for calling the "r:lumensdeletedata" R algorithm.
        """
        logging.getLogger(type(self).__name__).info('start: lumensdeletedata')
        self.actionLumensDeleteData.setDisabled(True)
        
        outputs = general.runalg('r:lumensdeletedata')
        
        self.loadAddedDataInfo()
        
        self.actionLumensDeleteData.setEnabled(True)
        logging.getLogger(type(self).__name__).info('end: lumensdeletedata')
    
    
    def checkDefaultBasemap(self):
        """Method for checking the default basemap file.
        """
        if os.path.isfile(self.appSettings['defaultBasemapFilePath']):
            return True
        else:
            return False
    
    
    def checkDefaultVector(self):
        """Method for checking the default vector file.
        """
        if os.path.isfile(self.appSettings['defaultVectorFilePath']):
            return True
        else:
            return False
    
    
    def loadDefaultLayers(self):
        """Replaces loadMap(), load the display default basemap layer on the map canvas.
        """
        self.addLayer(self.appSettings['defaultBasemapFilePath'])
        self.mapCanvas.setExtent(self.appSettings['defaultExtent'])
        self.layoutBody.addWidget(self.mapCanvas)
    
    
    def loadMapCanvas(self):
        """Method for adding the map canvas widget to main window's body content.
        """
        self.mapCanvas.setExtent(self.appSettings['defaultExtent'])
        self.layoutBody.addWidget(self.mapCanvas)
    
    
    def loadMap(self):
        """OBSOLETE DEBUG on-the-fly projection
        """
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(cur_dir, 'data', 'basemap', 'basemap.tif')
        self.basemap_layer = QgsRasterLayer(filename, 'basemap')
        QgsMapLayerRegistry.instance().addMapLayer(self.basemap_layer)
        
        filename = os.path.join(cur_dir, 'data', 'vector', 'Paser_rtrwp2014_utm50s.shp')
        self.landmark_layer = QgsVectorLayer(filename, 'landmarks', 'ogr')
        QgsMapLayerRegistry.instance().addMapLayer(self.landmark_layer)

        self.mapCanvas.setExtent(self.appSettings['defaultExtent'])
        
        layers = []
        
        layers.append(QgsMapCanvasLayer(self.landmark_layer))
        layers.append(QgsMapCanvasLayer(self.basemap_layer))
        
        self.mapCanvas.setLayerSet(layers)
        
        self.layoutBody.addWidget(self.mapCanvas)
    
    
    def addLayer(self, layerFile):
        """Method for adding a spatial format file to the layer list and show it on the map canvas.
        
        Adds a spatial format file (vector or raster) to the layer list and show it as a new layer on the
        top level of the map canvas. All layers on the layer list are unique, no duplicate files can be added.
        A reference to the QgsVectorLayer or QgsRasterLayer instance is also maintained in "qgsLayerList".
        
        Args:
            layerFile (str): a file path to a spatial  format file (having a file extesion of .shp or .tif).
        """
        if os.path.isfile(layerFile):
            layerName = os.path.basename(layerFile)
            
            # Check for existing layers with same file name
            existingLayerItems = self.layerListModel.findItems(layerName)
                
            for existingLayerItem in existingLayerItems:
                existingLayerData = existingLayerItem.data()
                if os.path.abspath(layerFile) == os.path.abspath(existingLayerData['layerFile']):
                    QtGui.QMessageBox.warning(self, 'Duplicate Layer', 'Layer "{0}" has already been added.\nPlease select another file.'.format(layerName))
                    return
            
            layer = None
            layerType = None
            fileExt = os.path.splitext(layerName)[1].lower()
            
            if  fileExt == '.shp':
                layerType = 'vector'
                layer = QgsVectorLayer(layerFile, layerName, 'ogr')
            elif fileExt == '.tif':
                layerType = 'raster'
                layer = QgsRasterLayer(layerFile, layerName)
            
            if not layer.isValid():
                print 'ERROR: Invalid layer!'
                return
            
            layerItemData = {
                'layerFile': layerFile,
                'layerName': layerName,
                'layerType': layerType,
                'layer': layerName,
            }
            
            # Can't keep raster/vector object in layerItemData because of object copy error upon drag-drop
            self.qgsLayerList[layerName] = layer
            
            layerItem = QtGui.QStandardItem(layerName)
            layerItem.setData(layerItemData)
            layerItem.setToolTip(layerFile)
            layerItem.setEditable(False)
            layerItem.setCheckable(True)
            layerItem.setDragEnabled(True)
            layerItem.setDropEnabled(False)
            layerItem.setCheckState(QtCore.Qt.Checked)
            ##self.layerListModel.appendRow(layerItem)
            self.layerListModel.insertRow(0, layerItem) # Insert new layers at top of list
            
            QgsMapLayerRegistry.instance().addMapLayer(self.qgsLayerList[layerName])
            # FIX 20151118:
            # since on-the-fly CRS reprojection is enabled no need to set layer CRS
            # setting canvas extent to layer extent causes canvas to turn blank
            self.qgsLayerList[layerName].setCrs(QgsCoordinateReferenceSystem(self.appSettings['defaultCRS'], QgsCoordinateReferenceSystem.EpsgCrsId))
            self.mapCanvas.setExtent(self.qgsLayerList[layerName].extent())
            self.showVisibleLayers()
    
    
    def getSelectedLayerData(self):
        """Method for getting the layer item data of the currently selected layer on the layer list.
        """
        layerItemIndex = self.layerListView.selectedIndexes()[0]
        layerItem = self.layerListModel.itemFromIndex(layerItemIndex)
        layerItemData = layerItem.data()
        return layerItemData
    
    
    def printDebugInfo(self):
        """Method for printing debug info to the logger.
        """
        layerItemData = self.getSelectedLayerData()
        
        logging.getLogger(type(self).__name__).info('DEBUG INFO ===================================')
        logging.getLogger(type(self).__name__).info('MapCanvas layer count: ' + str(self.mapCanvas.layerCount()))
        logging.getLogger(type(self).__name__).info('MapCanvas destination CRS: ' + self.mapCanvas.mapRenderer().destinationCrs().authid())
        logging.getLogger(type(self).__name__).info('On-the-fly projection enabled: ' + str(self.mapCanvas.hasCrsTransformEnabled()))
        logging.getLogger(type(self).__name__).info('Selected layer CRS: ' + self.qgsLayerList[layerItemData['layer']].crs().authid())
    
    
    def showVisibleLayers(self):
        """Find checked layers in "layerListModel" and add them to the map canvas layerset.
        """
        layers = []
        i = 0
        
        while self.layerListModel.item(i):
            layerItem = self.layerListModel.item(i)
            layerItemData = layerItem.data()
            
            if layerItem.checkState():
                layers.append(QgsMapCanvasLayer(self.qgsLayerList[layerItemData['layer']]))
                
                logging.getLogger(type(self).__name__).info('showing layer: %s', layerItem.text())
            
            i += 1
        
        if i > 0:
            logging.getLogger(type(self).__name__).info('===========================================')
        
        self.mapCanvas.setLayerSet(layers)
    
    
    def handlerLayerItemContextMenu(self, pos):
        """Method for constructing the custom context menu when clicking on a layer item on the layer list.
        
        Args:
            pos (QPoint): the coordinate of the click.
        """
        self.contextMenu = QtGui.QMenu()
        self.contextMenu.addAction(self.actionPanSelected)
        self.contextMenu.addAction(self.actionZoomLayer)
        self.contextMenu.addAction(self.actionZoomSelected)
        self.contextMenu.addAction(self.actionLayerAttributeTable)
        self.contextMenu.addAction(self.actionLayerAttributeEditor)
        self.contextMenu.addAction(self.actionFeatureSelectExpression)
        self.contextMenu.addAction(self.actionDeleteLayer)
        self.contextMenu.addAction(self.actionLayerProperties)
        
        parentPosition = self.layerListView.mapToGlobal(QtCore.QPoint(0, 0))
        self.contextMenu.move(parentPosition + pos)
        self.contextMenu.show()
    
    
    def handlerMainWindowContextMenu(self, pos):
        """Method for constructing the custom context menu when clicking on the main window.
        
        Args:
            pos (QPoint): the coordinate of the click.
        """
        self.contextMenu = QtGui.QMenu()
        self.contextMenu.addAction(self.actionToggleMenubar)
        self.contextMenu.addAction(self.sidebarDockWidgetAction)
        self.contextMenu.addAction(self.actionToggleDialogToolbar)
        self.contextMenu.addAction(self.actionToggleToolbar)
        
        parentPosition = self.mapToGlobal(QtCore.QPoint(0, 0))
        self.contextMenu.move(parentPosition + pos)
        self.contextMenu.show()
    
    
    def handlerProcessPURTemplate(self):
        """Slot method for processing a template.
        """
        templateFile = self.comboBoxPURTemplate.currentText()
        
        reply = QtGui.QMessageBox.question(
            self,
            'Process Template',
            'Do you want to process \'{0}\'?'.format(templateFile),
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
            QtGui.QMessageBox.No
        )
        
        if reply == QtGui.QMessageBox.Yes:
            self.buttonProcessPURTemplate.setDisabled(True)
            
            dialogLumensPUR = self.openDialog(DialogLumensPUR, showDialog=False)
            dialogLumensPUR.loadTemplate('Setup', templateFile)
            dialogLumensPUR.handlerProcessSetup()
            
            self.buttonProcessPURTemplate.setEnabled(True)
    
    
    def handlerProcessPreQUESTemplate(self):
        """Slot method for processing a template.
        """
        templateFile = self.comboBoxPreQUESTemplate.currentText()
        
        reply = QtGui.QMessageBox.question(
            self,
            'Process Template',
            'Do you want to process \'{0}\'?'.format(templateFile),
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
            QtGui.QMessageBox.No
        )
        
        if reply == QtGui.QMessageBox.Yes:
            self.buttonProcessPreQUESTemplate.setDisabled(True)
            
            dialogLumensQUES = self.openDialog(DialogLumensQUES, showDialog=False)
            dialogLumensQUES.loadTemplate('Pre-QUES', templateFile)
            dialogLumensQUES.handlerProcessPreQUES()
            
            self.buttonProcessPreQUESTemplate.setEnabled(True)
    
    
    def handlerProcessQUESCTemplate(self):
        """Slot method for processing a template.
        """
        templateFile = self.comboBoxQUESCTemplate.currentText()
        
        reply = QtGui.QMessageBox.question(
            self,
            'Process Template',
            'Do you want to process \'{0}\'?'.format(templateFile),
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
            QtGui.QMessageBox.No
        )
        
        if reply == QtGui.QMessageBox.Yes:
            self.buttonProcessQUESCTemplate.setDisabled(True)
            
            dialogLumensQUES = self.openDialog(DialogLumensQUES, showDialog=False)
            dialogLumensQUES.loadTemplate('QUES-C', templateFile)
            
            # Update the checkbox status in the dialog too
            if self.checkBoxQUESCCarbonAccounting.isChecked():
                dialogLumensQUES.checkBoxCarbonAccounting.setChecked(True)
            
            if self.checkBoxQUESCPeatlandCarbonAccounting.isChecked():
                dialogLumensQUES.checkBoxPeatlandCarbonAccounting.setChecked(True)
            
            if self.checkBoxQUESCSummarizeMultiplePeriod.isChecked():
                dialogLumensQUES.checkBoxSummarizeMultiplePeriod.setChecked(True)
            
            dialogLumensQUES.handlerProcessQUESC()
            
            self.buttonProcessQUESCTemplate.setEnabled(True)
    
    
    def handlerProcessQUESBTemplate(self):
        """Slot method for processing a template.
        """
        templateFile = self.comboBoxQUESBTemplate.currentText()
        
        reply = QtGui.QMessageBox.question(
            self,
            'Process Template',
            'Do you want to process \'{0}\'?'.format(templateFile),
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
            QtGui.QMessageBox.No
        )
        
        if reply == QtGui.QMessageBox.Yes:
            self.buttonProcessQUESBTemplate.setDisabled(True)
            
            dialogLumensQUES = self.openDialog(DialogLumensQUES, showDialog=False)
            dialogLumensQUES.loadTemplate('QUES-B', templateFile)
            dialogLumensQUES.handlerProcessQUESB()
            
            self.buttonProcessQUESBTemplate.setEnabled(True)
    
    
    def handlerProcessQUESHTemplate(self):
        """Slot method for processing a template.
        """
        templateFile = None
        tabName = None
        QUESHHRUDefinition = QUESHWatershedModelEvaluation = QUESHWatershedIndicators = False
        
        if radioQUESHHRUDefinition.isChecked():
            QUESHHRUDefinition = True
            tabName = 'Hydrological Response Unit Definition'
            templateFile = self.comboBoxHRUDefinitionTemplate.currentText()
        elif radioQUESHWatershedModelEvaluation.isChecked():
            QUESHWatershedModelEvaluation = True
            tabName = 'Watershed Model Evaluation'
            templateFile = self.comboBoxWatershedModelEvaluationTemplate.currentText()
        elif radioQUESHWatershedIndicators.isChecked():
            QUESHWatershedIndicators = True
            tabName = 'Watershed Indicators'
            templateFile = self.comboBoxWatershedIndicatorsTemplate.currentText()
        
        reply = QtGui.QMessageBox.question(
            self,
            'Process Template',
            'Do you want to process \'{0}\'?'.format(templateFile),
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
            QtGui.QMessageBox.No
        )
        
        if reply == QtGui.QMessageBox.Yes:
            self.buttonProcessQUESHTemplate.setDisabled(True)
            
            dialogLumensQUES = self.openDialog(DialogLumensQUES, showDialog=False)
            dialogLumensQUES.loadTemplate(tabName, templateFile)
            
            if QUESHHRUDefinition:
                # Update the checkbox status in the dialog too
                if self.checkBoxHRUDefinitionDominantHRU.isChecked():
                    dialogLumensQUES.checkBoxDominantHRU.setChecked(True)
                
                if self.checkBoxHRUDefinitionDominantLUSSL.isChecked():
                    dialogLumensQUES.checkBoxDominantLUSSL.setChecked(True)
                
                if self.checkBoxHRUDefinitionMultipleHRU.isChecked():
                    dialogLumensQUES.checkBoxMultipleHRU.setChecked(True)
            
                dialogLumensQUES.handlerProcessQUESHHRUDefinition()
            elif QUESHWatershedModelEvaluation:
                dialogLumensQUES.handlerProcessQUESHWatershedModelEvaluation()
            elif QUESHWatershedIndicators:
                dialogLumensQUES.handlerProcessQUESHWatershedIndicators()
            
            self.buttonProcessQUESHTemplate.setEnabled(True)
    
    
    def handlerProcessTAOpportunityCostTemplate(self):
        """Slot method for processing a template.
        """
        templateFile = None
        tabName = None
        TAAbacusOpportunityCost = TAOpportunityCostCurve = TAOpportunityCostMap = False
        
        if self.radioTAOpportunityCostAbacus.isChecked():
            TAAbacusOpportunityCost = True
            tabName = 'Abacus Opportunity Cost'
            templateFile = self.comboBoxAbacusOpportunityCostTemplate.currentText()
        elif self.radioTAOpportunityCostCurve.isChecked():
            TAOpportunityCostCurve = True
            tabName = 'Opportunity Cost Curve'
            templateFile = self.comboBoxOpportunityCostCurveTemplate.currentText()
        elif self.radioTAOpportunityCostMap.isChecked():
            TAOpportunityCostMap = True
            tabName = 'Opportunity Cost Map'
            templateFile = self.comboBoxOpportunityCostMapTemplate.currentText()
        
        reply = QtGui.QMessageBox.question(
            self,
            'Process Template',
            'Do you want to process \'{0}\'?'.format(templateFile),
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
            QtGui.QMessageBox.No
        )
        
        if reply == QtGui.QMessageBox.Yes:
            self.buttonProcessTAOpportunityCostTemplate.setDisabled(True)
            
            dialogLumensTA = self.openDialog(DialogLumensTAOpportunityCost, showDialog=False)
            dialogLumensTA.loadTemplate(tabName, templateFile)
            
            if TAAbacusOpportunityCost:
                dialogLumensTA.handlerProcessAbacusOpportunityCost()
            elif QUESHWatershedModelEvaluation:
                dialogLumensTA.handlerProcessOpportunityCostCurve()
            elif QUESHWatershedIndicators:
                dialogLumensTA.handlerProcessOpportunityCostMap()
            
            self.buttonProcessTAOpportunityCostTemplate.setEnabled(True)
        
    
    def handlerProcessTARegionalEconomyTemplate(self):
        """Slot method for processing a template.
        """
        templateFile = None
        tabName = None
        TADescriptiveAnalysis = TARegionalEconomicScenarioImpact = TALandRequirementAnalysis = TALandUseChangeImpact = False
        
        if self.radioTARegionalEconomyDescriptiveAnalysis.isChecked():
            TADescriptiveAnalysis = True
            tabName = 'Descriptive Analysis of Regional Economy'
            templateFile = self.comboBoxDescriptiveAnalysisTemplate.currentText()
        elif self.radioTARegionalEconomyRegionalEconomicScenarioImpact.isChecked():
            TARegionalEconomicScenarioImpact = True
            tabName = 'Regional Economic Scenario Impact'
            templateFile = self.comboBoxRegionalEconomicScenarioImpactTemplate.currentText()
        elif self.radioTARegionalEconomyLandRequirementAnalysis.isChecked():
            TALandRequirementAnalysis = True
            tabName = 'Land Requirement Analysis'
            templateFile = self.comboBoxLandRequirementAnalysisTemplate.currentText()
        elif self.radioTARegionalEconomyLandUseChangeImpact.isChecked():
            TALandUseChangeImpact = True
            tabName = 'Land Use Change Impact'
            templateFile = self.comboBoxLandUseChangeImpactTemplate.currentText()
        
        reply = QtGui.QMessageBox.question(
            self,
            'Process Template',
            'Do you want to process \'{0}\'?'.format(templateFile),
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
            QtGui.QMessageBox.No
        )
        
        if reply == QtGui.QMessageBox.Yes:
            self.buttonProcessTARegionalEconomyTemplate.setDisabled(True)
            
            dialogLumensTA = self.openDialog(DialogLumensTARegionalEconomy, showDialog=False)
            dialogLumensTA.loadTemplate(tabName, templateFile)
            
            if TADescriptiveAnalysis:
                # Update the checkbox status in the dialog too
                if self.checkBoxDescriptiveAnalysisMultiplePeriod.isChecked():
                    dialogLumensTA.checkBoxMultiplePeriod.setChecked(True)
                
                dialogLumensTA.handlerProcessDescriptiveAnalysis()
            elif TARegionalEconomicScenarioImpact:
                # Update the checkbox status in the dialog too
                if self.checkBoxRegionalEconomicScenarioImpactFinalDemand.isChecked():
                    dialogLumensTA.checkBoxRegionalEconomicScenarioImpactFinalDemand.setChecked(True)
                
                if self.checkBoxRegionalEconomicScenarioImpactGDP.isChecked():
                    dialogLumensTA.checkBoxRegionalEconomicScenarioImpactGDP.setChecked(True)
            
                dialogLumensTA.handlerProcessRegionalEconomicScenarioImpact()
            elif TALandRequirementAnalysis:
                dialogLumensTA.handlerProcessLandRequirementAnalysis()
            elif TALandUseChangeImpact:
                dialogLumensTA.handlerProcessLandUseChangeImpact()
            
            self.buttonProcessTARegionalEconomyTemplate.setEnabled(True)
    
    
    def handlerProcessSCIENDOLowEmissionDevelopmentAnalysisTemplate(self):
        """Slot method for processing a template.
        """
        templateFile = self.comboBoxLowEmissionDevelopmentAnalysisTemplate.currentText()
        
        reply = QtGui.QMessageBox.question(
            self,
            'Process Template',
            'Do you want to process \'{0}\'?'.format(templateFile),
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
            QtGui.QMessageBox.No
        )
        
        if reply == QtGui.QMessageBox.Yes:
            self.buttonProcessSCIENDOLowEmissionDevelopmentAnalysisTemplate.setDisabled(True)
            
            dialogLumensSCIENDO = self.openDialog(DialogLumensSCIENDO, showDialog=False)
            DialogLumensSCIENDO.loadTemplate('Low Emission Development Analysis', templateFile)
            
            # Update the checkbox status in the dialog too
            if self.checkBoxSCIENDOHistoricalBaselineProjection.isChecked():
                dialogLumensSCIENDO.checkBoxHistoricalBaselineProjection.setChecked(True)
            
            if self.checkBoxSCIENDOHistoricalBaselineAnnualProjection.isChecked():
                dialogLumensSCIENDO.checkBoxHistoricalBaselineAnnualProjection.setChecked(True)
            
            if self.checkBoxSCIENDODriversAnalysis.isChecked():
                dialogLumensSCIENDO.checkBoxDriversAnalysis.setChecked(True)
            
            if self.checkBoxSCIENDOBuildScenario.isChecked():
                dialogLumensSCIENDO.checkBoxBuildScenario.setChecked(True)
            
            dialogLumensSCIENDO.handlerProcessLowEmissionDevelopmentAnalysis()
            
            self.buttonProcessSCIENDOLowEmissionDevelopmentAnalysisTemplate.setEnabled(True)
    
    
    def handlerProcessSCIENDOLandUseChangeModelingTemplate(self):
        """Slot method for processing a template.
        """
        templateFile = self.comboBoxLandUseChangeModelingTemplate.currentText()
        
        reply = QtGui.QMessageBox.question(
            self,
            'Process Template',
            'Do you want to process \'{0}\'?'.format(templateFile),
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
            QtGui.QMessageBox.No
        )
        
        if reply == QtGui.QMessageBox.Yes:
            self.buttonProcessSCIENDOLandUseChangeModelingTemplate.setDisabled(True)
            
            dialogLumensSCIENDO = self.openDialog(DialogLumensSCIENDO, showDialog=False)
            DialogLumensSCIENDO.loadTemplate('Land Use Change Modeling', templateFile)
            
            # Update the checkbox status in the dialog too
            if self.checkBoxSCIENDOCreateRasterCubeOfFactors.isChecked():
                dialogLumensSCIENDO.checkBoxCreateRasterCubeOfFactors.setChecked(True)
            
            if self.checkBoxSCIENDOCalculateTransitionMatrix.isChecked():
                dialogLumensSCIENDO.checkBoxCalculateTransitionMatrix.setChecked(True)
            
            # if self.checkBoxSCIENDOCalculateWeightOfEvidence.isChecked():
            #     dialogLumensSCIENDO.checkBoxCalculateWeightOfEvidence.setChecked(True)
            
            if self.checkBoxSCIENDOSimulateLandUseChange.isChecked():
                dialogLumensSCIENDO.checkBoxSimulateLandUseChange.setChecked(True)
            
            if self.checkBoxSCIENDOSimulateWithScenario.isChecked():
                dialogLumensSCIENDO.checkBoxSimulateWithScenario.setChecked(True)
            
            dialogLumensSCIENDO.handlerProcessLandUseChangeModeling()
            
            self.buttonProcessSCIENDOLandUseChangeModelingTemplate.setEnabled(True)
    
    
    def handlerToggleQUESH(self, radio):
        """Slot method for toggling a radio button.
        
        Args:
            radio (QRadioButton): the clicked radio button.
        """
        for i in range(self.layoutQUESHHRUDefinitionTemplate.count()):
            item = self.layoutQUESHHRUDefinitionTemplate.itemAt(i)
            item.widget().setVisible(False)
    
        for i in range(self.layoutQUESHWatershedModelEvaluationTemplate.count()):
            item = self.layoutQUESHWatershedModelEvaluationTemplate.itemAt(i)
            item.widget().setVisible(False)
        
        for i in range(self.layoutQUESHWatershedIndicatorsTemplate.count()):
            item = self.layoutQUESHWatershedIndicatorsTemplate.itemAt(i)
            item.widget().setVisible(False)
        
        self.groupBoxHRUDefinitionFunction.setDisabled(True)
        
        if radio.text() == 'Hydrological Response Unit Definition':
            if radio.isChecked():
                self.groupBoxHRUDefinitionFunction.setDisabled(False)
                
                for i in range(self.layoutQUESHHRUDefinitionTemplate.count()):
                    item = self.layoutQUESHHRUDefinitionTemplate.itemAt(i)
                    item.widget().setVisible(True)
        elif radio.text() == 'Watershed Model Evaluation':
            if radio.isChecked():
                for i in range(self.layoutQUESHWatershedModelEvaluationTemplate.count()):
                    item = self.layoutQUESHWatershedModelEvaluationTemplate.itemAt(i)
                    item.widget().setVisible(True)
        elif radio.text() == 'Watershed Indicators':
            if radio.isChecked():
                for i in range(self.layoutQUESHWatershedIndicatorsTemplate.count()):
                    item = self.layoutQUESHWatershedIndicatorsTemplate.itemAt(i)
                    item.widget().setVisible(True)
        
    
    def handlerToggleTAOpportunityCost(self, radio):
        """Slot method for toggling a radio button.
        
        Args:
            radio (QRadioButton): the clicked radio button.
        """
        for i in range(self.layoutTAAbacusOpportunityCostTemplate.count()):
            item = self.layoutTAAbacusOpportunityCostTemplate.itemAt(i)
            item.widget().setVisible(False)
    
        for i in range(self.layoutTAOpportunityCostCurveTemplate.count()):
            item = self.layoutTAOpportunityCostCurveTemplate.itemAt(i)
            item.widget().setVisible(False)
        
        for i in range(self.layoutTAOpportunityCostMapTemplate.count()):
            item = self.layoutTAOpportunityCostMapTemplate.itemAt(i)
            item.widget().setVisible(False)
        
        if radio.text() == 'Abacus Opportunity Cost':
            if radio.isChecked():
                for i in range(self.layoutTAAbacusOpportunityCostTemplate.count()):
                    item = self.layoutTAAbacusOpportunityCostTemplate.itemAt(i)
                    item.widget().setVisible(True)
        elif radio.text() == 'Opportunity Cost Curve':
            if radio.isChecked():
                for i in range(self.layoutTAOpportunityCostCurveTemplate.count()):
                    item = self.layoutTAOpportunityCostCurveTemplate.itemAt(i)
                    item.widget().setVisible(True)
        elif radio.text() == 'Opportunity Cost Map':
            if radio.isChecked():
                for i in range(self.layoutTAOpportunityCostMapTemplate.count()):
                    item = self.layoutTAOpportunityCostMapTemplate.itemAt(i)
                    item.widget().setVisible(True)
    
    
    def handlerToggleTARegionalEconomy(self, radio):
        """Slot method for toggling a radio button.
        
        Args:
            radio (QRadioButton): the clicked radio button.
        """
        for i in range(self.layoutTARegionalEconomyDescriptiveAnalysisTemplate.count()):
            item = self.layoutTARegionalEconomyDescriptiveAnalysisTemplate.itemAt(i)
            item.widget().setVisible(False)
    
        for i in range(self.layoutTARegionalEconomyRegionalEconomicScenarioImpactTemplate.count()):
            item = self.layoutTARegionalEconomyRegionalEconomicScenarioImpactTemplate.itemAt(i)
            item.widget().setVisible(False)
        
        for i in range(self.layoutTARegionalEconomyLandRequirementAnalysisTemplate.count()):
            item = self.layoutTARegionalEconomyLandRequirementAnalysisTemplate.itemAt(i)
            item.widget().setVisible(False)
        
        for i in range(self.layoutTARegionalEconomyLandUseChangeImpactTemplate.count()):
            item = self.layoutTARegionalEconomyLandUseChangeImpactTemplate.itemAt(i)
            item.widget().setVisible(False)
            
        self.groupBoxDescriptiveAnalysisPeriod.setDisabled(True)
        self.groupBoxRegionalEconomicScenarioImpactType.setDisabled(True)
        
        if radio.text() == 'Descriptive Analysis of Regional Economy':
            if radio.isChecked():
                self.groupBoxDescriptiveAnalysisPeriod.setDisabled(False)
                
                for i in range(self.layoutTARegionalEconomyDescriptiveAnalysisTemplate.count()):
                    item = self.layoutTARegionalEconomyDescriptiveAnalysisTemplate.itemAt(i)
                    item.widget().setVisible(True)
        elif radio.text() == 'Regional Economic Scenario Impact':
            if radio.isChecked():
                self.groupBoxRegionalEconomicScenarioImpactType.setDisabled(False)
                
                for i in range(self.layoutTARegionalEconomyRegionalEconomicScenarioImpactTemplate.count()):
                    item = self.layoutTARegionalEconomyRegionalEconomicScenarioImpactTemplate.itemAt(i)
                    item.widget().setVisible(True)
        elif radio.text() == 'Land Requirement Analysis':
            if radio.isChecked():
                for i in range(self.layoutTARegionalEconomyLandRequirementAnalysisTemplate.count()):
                    item = self.layoutTARegionalEconomyLandRequirementAnalysisTemplate.itemAt(i)
                    item.widget().setVisible(True)
        elif radio.text() == 'Land Use Change Impact':
            if radio.isChecked():
                for i in range(self.layoutTARegionalEconomyLandUseChangeImpactTemplate.count()):
                    item = self.layoutTARegionalEconomyLandUseChangeImpactTemplate.itemAt(i)
                    item.widget().setVisible(True)
    
    
    def handlerDialogLumensCreateDatabase(self):
        """Slot method for opening a dialog window.
        """
        self.openDialog(DialogLumensCreateDatabase)
    
    
    def handlerLumensOpenDatabase(self):
        """Slot method for a file select dialog to open a LUMENS .lpj project database file.
        """
        lumensDatabase = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select LUMENS Database', QtCore.QDir.homePath(), 'LUMENS Database (*{0});;LUMENS Archive (*{1})'
                .format(self.appSettings['selectProjectfileExt'], self.appSettings['selectZipfileExt'])))
        
        lumensDatabaseName, lumensDatabaseExt = os.path.splitext(lumensDatabase)
        
        if lumensDatabase:
            logging.getLogger(type(self).__name__).info('select LUMENS database: %s', lumensDatabase)
            
            if lumensDatabaseExt == self.appSettings['selectZipfileExt'] and zipfile.is_zipfile(lumensDatabase):
                workingDir = unicode(QtGui.QFileDialog.getExistingDirectory(self, 'Select Working Directory'))
                if workingDir:
                    logging.getLogger(type(self).__name__).info('select new working directory: %s', workingDir)
                    outputs = self.lumensImportDatabase(lumensDatabase, workingDir)
                else:
                    print 'ERROR: Invalid working directory!'
                    return
            else:
                print 'ERROR: Invalid archived LUMENS file!'
                return
              
            self.lumensOpenDatabase(outputs['proj.file'])
            
            
    def handlerLumensDeleteData(self):
        """Slot method for triggering the delete data operation.
        """
        self.lumensDeleteData()
    
    
    def handlerLumensCloseDatabase(self):
        """Slot method for triggering the close database operation.
        """
        self.lumensCloseDatabase()
    
    
    def handlerLumensDatabaseStatus(self):
        """Slot method for triggering the show database status operation.
        """
        self.lumensDatabaseStatus()
    
    
    def handlerDialogLumensAddData(self):
        """Slot method for opening a dialog window.
        """
        self.openDialog(DialogLumensAddData)
    
    
    def handlerLumensExportDatabase(self):
        """Slot method for opening a dialog window.
        """
        self.lumensExportDatabase()
    
    
    def handlerDialogLumensPUR(self):
        """Slot method for opening a dialog window.
        """
        self.openDialog(DialogLumensPUR)
    
    
    def handlerDialogLumensQUES(self, tabName=''):
        """Slot method for opening a dialog window.
        """
        self.openDialog(DialogLumensQUES, tabName=tabName)
    
    
    def handlerDialogLumensTAOpportunityCost(self):
        """Slot method for opening a dialog window.
        """
        tabName = ''
        if self.radioTAOpportunityCostAbacus.isChecked():
            tabName = 'Abacus Opportunity Cost'
        elif self.radioTAOpportunityCostCurve.isChecked():
            tabName = 'Opportunity Cost Curve'
        elif self.radioTAOpportunityCostMap.isChecked():
            tabName = 'Opportunity Cost Map'
        self.openDialog(DialogLumensTAOpportunityCost, tabName=tabName)
    
    
    def handlerDialogLumensTARegionalEconomy(self):
        """Slot method for opening a dialog window.
        """
        tabName = ''
        if self.radioTARegionalEconomyDescriptiveAnalysis.isChecked():
            tabName = 'Descriptive Analysis of Regional Economy'
        elif self.radioTARegionalEconomyRegionalEconomicScenarioImpact.isChecked():
            tabName = 'Regional Economic Scenario Impact'
        elif self.radioTARegionalEconomyLandRequirementAnalysis.isChecked():
            tabName = 'Land Requirement Analysis'
        elif self.radioTARegionalEconomyLandUseChangeImpact.isChecked():
            tabName = 'Land Use Change Impact'
        self.openDialog(DialogLumensTARegionalEconomy, tabName=tabName)
    
    
    def handlerDialogLumensSCIENDO(self, tabName=''):
        """Slot method for opening a dialog window.
        """
        self.openDialog(DialogLumensSCIENDO, tabName=tabName)
    
    
    def handlerDialogLumensHelp(self):
        """Slot method for opening the LUMENS html help document.
        """
        filePath = os.path.join(self.appSettings['appDir'], self.appSettings['folderHelp'], self.appSettings['helpLUMENSFile'])
        
        if os.path.exists(filePath):
            dialog = DialogLumensViewer(self, 'LUMENS Help', 'html', filePath)
            dialog.exec_()
        else:
            QtGui.QMessageBox.critical(self, 'LUMENS Help Not Found', "Unable to open '{0}'.".format(filePath))
    
    
    def handlerDialogLumensGuide(self):
        """Slot method for opening the LUMENS application guide document in the app directory.
        
        OBSOLETE replaced by LUMENS Help.
        """
        filePath = os.path.join(self.appSettings['appDir'], self.appSettings['guideFile'])
        
        if os.path.exists(filePath):
            if sys.platform == 'win32':
                os.startfile(filePath) # Open the document file in Windows
        else:
            QtGui.QMessageBox.critical(self, 'LUMENS Guide Not Found', "Unable to open '{0}'.".format(filePath))
    
    
    def handlerDialogLumensAbout(self):
        """Slot method for showing the LUMENS application About info.
        """
        QtGui.QMessageBox.about(self, 'LUMENS',
            """<b>LUMENS</b> v {0}
            <p>Copyright &copy; 2015-2016 ICRAF. 
            All rights reserved.
            <p>Python {1} - Qt {2} - PyQt {3} on {4}""".format(
            __version__, platform.python_version(),
            QtCore.QT_VERSION_STR, QtCore.PYQT_VERSION_STR,
            platform.system()))
    
    
    def handlerToggleMenuBar(self):
      """Slot method for toggling the menu bar visibility.
      """
      if not self.actionToggleMenubar.isChecked():
          self.menubar.setVisible(False)
          self.setWindowTitle(self.windowTitle.format(__version__, '- press F11 to show menu bar'))
      else:
          self.menubar.setVisible(True)
          self.setWindowTitle(self.windowTitle.format(__version__, ''))
    
    
    def handlerToggleToolbar(self):
        """Slot method for toggling the toolbar visibility.
        """
        if not self.actionToggleToolbar.isChecked():
            self.toolBar.setVisible(False)
        else:
            self.toolBar.setVisible(True)
    
    
    def handlerToggleDialogToolbar(self):
        """Slot method for toggling the top dialog toolbar visibility.
        """
        if not self.actionToggleDialogToolbar.isChecked():
            self.dialogToolBar.setVisible(False)
        else:
            self.dialogToolBar.setVisible(True)
    
    
    def handlerZoomIn(self):
        """Slot method for zoom in action on the map canvas.
        """
        self.mapCanvas.zoomIn()
    
    
    def handlerZoomOut(self):
        """Slot method for zoom out action on the map canvas.
        """
        self.mapCanvas.zoomOut()
    
    
    def handlerZoomFull(self):
        """Slot method for zoom to full extent action on the map canvas.
        """
        self.mapCanvas.zoomToFullExtent()
    
    
    def handlerZoomLayer(self):
        """Slot method for zoom in action to the selected layer.
        """
        layerItemData = self.getSelectedLayerData()
        
        ##self.mapCanvas.setExtent(self.qgsLayerList[layerItemData['layer']].extent())
        ##self.mapCanvas.refresh()
        
        # HACK to fix blank map canvas from 2 lines above
        if layerItemData['layerType'] == 'vector':
            self.qgsLayerList[layerItemData['layer']].selectAll()
            self.mapCanvas.zoomToSelected()
            self.qgsLayerList[layerItemData['layer']].removeSelection()
    
    
    def handlerZoomSelected(self):
        """Slot method for zooming to the selected features in a layer.
        """
        layerItemData = self.getSelectedLayerData()
        
        if layerItemData['layerType'] == 'vector':
            self.mapCanvas.setCurrentLayer(self.qgsLayerList[layerItemData['layer']])
            self.mapCanvas.zoomToSelected()
    
    
    def handlerPanSelected(self):
        """Slot method for panning to the selected layer.
        """
        layerItemData = self.getSelectedLayerData()
        
        if layerItemData['layerType'] == 'vector':
            self.mapCanvas.setCurrentLayer(self.qgsLayerList[layerItemData['layer']])
            
            # HACK to get panToSelected working (select 1 feature first)
            layerFeatures = self.qgsLayerList[layerItemData['layer']].getFeatures()
            
            for feature in layerFeatures:
                self.qgsLayerList[layerItemData['layer']].setSelectedFeatures([feature.id()])
                break
            
            self.mapCanvas.panToSelected()
            self.qgsLayerList[layerItemData['layer']].removeSelection()
    
    
    def handlerSetPanMode(self):
        """Slot method to set the desired map tool for the map canvas.
        """
        self.actionPan.setChecked(True)
        self.actionSelect.setChecked(False)
        self.actionInfo.setChecked(False)
        self.mapCanvas.setMapTool(self.panTool)
    
    
    def handlerSetSelectMode(self):
        """Slot method to set the desired map tool for the map canvas.
        """
        self.actionSelect.setChecked(True)
        self.actionPan.setChecked(False)
        self.actionInfo.setChecked(False)
        self.mapCanvas.setMapTool(self.selectTool)
    
    
    def handlerSetInfoMode(self):
        """Slot method to set the desired map tool for the map canvas.
        """
        self.actionInfo.setChecked(True)
        self.actionPan.setChecked(False)
        self.actionSelect.setChecked(False)
        self.mapCanvas.setMapTool(self.infoTool)
    
    
    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def handlerSelectLayer(self, layerItemIndex):
        """Slot method that is called when a layer item in the "layerListModel" is selected.
        
        Args:
            layerItemIndex (QModelIndex): the model index position of the selected layer item.
        """
        self.actionDeleteLayer.setEnabled(True)
        
        # Check if selected layer is a vector
        layerItem = self.layerListModel.itemFromIndex(layerItemIndex)
        layerItemData = layerItem.data()
        self.mapCanvas.setCurrentLayer(self.qgsLayerList[layerItemData['layer']])
        
        if layerItemData['layerType'] == 'vector':
            self.actionPanSelected.setEnabled(True)
            self.actionZoomLayer.setEnabled(True)
            self.actionZoomSelected.setEnabled(True)
            self.actionLayerAttributeTable.setEnabled(True)
            self.actionLayerAttributeEditor.setEnabled(True)
            self.actionFeatureSelectExpression.setEnabled(True)
            self.actionLayerProperties.setEnabled(True)
        else:
            self.actionPanSelected.setDisabled(True)
            self.actionZoomLayer.setDisabled(True)
            self.actionZoomSelected.setDisabled(True)
            self.actionLayerAttributeTable.setDisabled(True)
            self.actionLayerAttributeEditor.setDisabled(True)
            self.actionFeatureSelectExpression.setDisabled(True)
            self.actionLayerProperties.setDisabled(True)
        
        if self.appSettings['debug']:
            self.printDebugInfo()
    
    
    def handlerLayerAttributeTable(self):
        """Slot method for opening the layer attribute table dialog.
        """
        layerItemData = self.getSelectedLayerData()
        
        # Try using QGIS's attribute widget
        dialog = DialogLayerAttributeTable(self.qgsLayerList[layerItemData['layer']], self)
        dialog.exec_()
    
    
    def handlerLayerAttributeEditor(self):
        """Slot method for opening the layer attribute editor.
        """
        layerItemData = self.getSelectedLayerData()
        
        # Try using QGIS's attribute widget
        dialog = DialogLayerAttributeDualView(self.qgsLayerList[layerItemData['layer']], self)
        dialog.exec_()
    
    
    def handlerFeatureSelectExpression(self):
        """Slot method for opening the layer feature selection dialog.
        """
        layerItemData = self.getSelectedLayerData()
        
        # Try using QGIS's select feature dialog
        dialog = QgsExpressionSelectionDialog(self.qgsLayerList[layerItemData['layer']], '', self)
        dialog.exec_()
    
    
    def handlerLayerProperties(self):
        """Slot method for opening the layer properties dialog.
        """
        layerItemData = self.getSelectedLayerData()
        dialog = DialogLayerProperties(self.qgsLayerList[layerItemData['layer']], self)
        dialog.exec_()
    
    
    def handlerDoubleClickProjectTree(self, index):
        """Slot method when a double click event is triggered from the project tree.
        
        Upon double clicking a file in the project tree, try to process the file
        if it is supported.
        
        Args:
            index (QModelIndex): the model index position of the selected file.
        """
        indexItem = self.projectTreeView.model().index(index.row(), 0, index.parent())

        # Path or filename selected
        fileName = self.projectTreeView.model().fileName(indexItem)
        # Full path/filename selected
        filePath = self.projectTreeView.model().filePath(indexItem)
        
        ext = os.path.splitext(filePath)[-1].lower()
        
        if ext in self.appSettings['acceptedDocumentFormats']:
            if sys.platform == 'win32':
                os.startfile(filePath) # Open the document file in Windows
        elif ext in self.appSettings['acceptedSpatialFormats']:
            self.addLayer(filePath) # Add the spatial data file to the layer list
        elif ext == self.appSettings['selectQgsProjectfileExt']:
            self.lumensLoadQgsProjectLayers(filePath)
        elif ext in self.appSettings['acceptedWebFormats']: # Open web documents in internal viewer
            dialog = DialogLumensViewer(self, os.path.basename(filePath), 'html', filePath)
            dialog.exec_()
    
    
    def handlerDropLayer(self):
        """Slot method to handle dropping a layer in the layer list.
        """
        pass
    
    
    def handlerCheckLayer(self, layerItem):
        """Slot method for handling when the layer items in the layer list are reordered or un/checked.
        
        Args:
            layerItem (QStandardItem): the layer item being manipulated.
        """
        ##print 'DEBUG rowcount'
        ##print self.layerListModel.rowCount()
        
        # WORKAROUND for drag and drop reordering causing (count + 1) items in model
        QtCore.QTimer.singleShot(1, self.showVisibleLayers)
        
        """
        layerData = layerItem.data()
        if layerItem.checkState():
            QtGui.QMessageBox.information(self, 'Layer', 'Checked ' + layerData['layerName'])
        else:
            QtGui.QMessageBox.information(self, 'Layer', 'Unchecked ' + layerData['layerName'])
        """
    
    
    def handlerAddLayer(self):
        """Slot method for a file select dialog to add a spatial file to the layer list.
        """
        layerFormats = [self.appSettings['selectShapefileExt'], self.appSettings['selectRasterfileExt']]
        filterFormats = ' '.join(['*' + ext for ext in layerFormats])
        
        file = unicode(QtGui.QFileDialog.getOpenFileName(
            self, 'Select Vector/Raster File', QtCore.QDir.homePath(), 'Vector/Raster File ({0})'.format(filterFormats)))
        
        if file:
            self.addLayer(file)
    
    
    def handlerDeleteLayer(self):
        """Slot method for handling when a layer is deleted from the layer list.
        """
        layerItemIndex = self.layerListView.selectedIndexes()[0]
        layerItemData = self.getSelectedLayerData()
        del self.qgsLayerList[layerItemData['layer']]
        ##QtGui.QMessageBox.information(self, 'Layer', layerItemData)
        self.layerListModel.removeRow(layerItemIndex.row())
        
        self.showVisibleLayers()
        
        # No more layer items in the layer list
        if not self.layerListModel.rowCount():
            self.actionDeleteLayer.setDisabled(True)
            self.actionPanSelected.setDisabled(True)
            self.actionZoomLayer.setDisabled(True)
            self.actionZoomSelected.setDisabled(True)
            self.actionLayerAttributeTable.setDisabled(True)
            self.actionLayerAttributeEditor.setDisabled(True)
            self.actionFeatureSelectExpression.setDisabled(True)
            self.actionLayerProperties.setDisabled(True)
            return
        
        # Check type of next selected item
        layerItemData = self.getSelectedLayerData()
        
        if layerItemData['layerType'] == 'vector':
            self.actionPanSelected.setEnabled(True)
            self.actionZoomLayer.setEnabled(True)
            self.actionZoomSelected.setEnabled(True)
            self.actionLayerAttributeTable.setEnabled(True)
            self.actionLayerAttributeEditor.setEnabled(True)
            self.actionFeatureSelectExpression.setEnabled(True)
            self.actionLayerProperties.setEnabled(True)
        else:
            self.actionPanSelected.setDisabled(True)
            self.actionZoomLayer.setDisabled(True)
            self.actionZoomSelected.setDisabled(True)
            self.actionLayerAttributeTable.setDisabled(True)
            self.actionLayerAttributeEditor.setDisabled(True)
            self.actionFeatureSelectExpression.setDisabled(True)
            self.actionLayerProperties.setDisabled(True)
    
    
    def handlerRefresh(self):
        """Slot method for refreshing the map canvas.
        """
        self.mapCanvas.refresh()
    
    
    def handlerZoomLast(self):
        """Slot method for zooming to the previous extent on the map canvas.
        """
        self.mapCanvas.zoomToPreviousExtent()
    
    
    def handlerZoomNext(self):
        """Slot method for zooming to the next extent on the map canvas.
        """
        self.mapCanvas.zoomToNextExtent()
    
    
    def handlerZoomLastStatus(self, status):
        """Slot method to handle when the previous zoom extent is available.
        """
        if status:
            self.actionZoomLast.setEnabled(True)
        else:
            self.actionZoomLast.setDisabled(True)
    
    
    def handlerZoomNextStatus(self, status):
        """Slot method to handle when the next zoom extent is available.
        """
        if status:
            self.actionZoomNext.setEnabled(True)
        else:
            self.actionZoomNext.setDisabled(True)
    
    
    def handlerUpdateCoordinates(self, point):
        """Slot method for updating the map coordinates on the cursor position.
        
        Args:
            point (QgsPoint): the map point on the cursor position.
        """
        if self.mapCanvas.mapUnits() == QGis.DegreesMinutesSeconds:
            self.labelMapCanvasCoordinate.setText(point.toDegreesMinutesSeconds(3))
        else:
            print self.labelMapCanvasCoordinate.setText(point.toString(3))


#############################################################################


class SelectTool(QgsMapToolIdentify):
    """QgsMapTool subclass for handling select mode on the map canvas.
    """
    
    def __init__(self, window):
        QgsMapToolIdentify.__init__(self, window.mapCanvas)
        self.window = window
        self.setCursor(QtCore.Qt.ArrowCursor)
    
    
    def canvasReleaseEvent(self, event):
        """
        """
        found_features = self.identify(event.x(), event.y(), self.TopDownStopAtFirst, self.VectorLayer)
        if len(found_features) > 0:
            layer = found_features[0].mLayer
            feature = found_features[0].mFeature
            geometry = feature.geometry()

            if event.modifiers() & QtCore.Qt.ShiftModifier:
                layer.select(feature.id())
            else:
                layer.setSelectedFeatures([feature.id()])
        else:
            for layerName, layer in self.window.qgsLayerList.iteritems():
                if layer.type() == QgsMapLayer.VectorLayer:
                    layer.removeSelection()


#############################################################################


class InfoTool(QgsMapToolIdentify):
    """QgsMapTool subclass for handling the info mode on the map canvas.
    """
    
    def __init__(self, window):
        QgsMapToolIdentify.__init__(self, window.mapCanvas)
        self.window = window
    
    
    def canvasReleaseEvent(self, event):
        """
        """
        found_features = self.identify(event.x(), event.y(), self.TopDownStopAtFirst, self.VectorLayer)
        
        if len(found_features) > 0:
            layer = found_features[0].mLayer
            feature = found_features[0].mFeature
            geometry = feature.geometry()
            
            info = []
            
            layerDataProvider = layer.dataProvider()
            
            if not layerDataProvider.isValid():
                print 'ERROR: Invalid data provider!'
                return
            
            for field in layerDataProvider.fields():
                info.append(field.name() + ':\t' + str(feature.attribute(field.name())))
            
            msgBoxFeatureInfo = DetailedMessageBox(self.window)
            msgBoxFeatureInfo.setWindowTitle('Feature Info')
            msgBoxFeatureInfo.setText(layer.name())
            msgBoxFeatureInfo.setDetailedText("\n".join(info))
            ##msgBoxFeatureInfo.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
            ##msgBoxFeatureInfo.setSizeGripEnabled(True)
            msgBoxFeatureInfo.exec_()


#############################################################################


class PanTool(QgsMapTool):
    """QgsMapTool subclass for handling the pan mode on the map canvas.
    """
    
    def __init__(self, mapCanvas):
        QgsMapTool.__init__(self, mapCanvas)
        self.setCursor(QtCore.Qt.OpenHandCursor)
        self.dragging = False
    
    
    def canvasMoveEvent(self, event):
        """
        """
        if event.buttons() == QtCore.Qt.LeftButton:
            self.dragging = True
            self.canvas().panAction(event)
    
    
    def canvasReleaseEvent(self, event):
        """
        """
        if event.button() == QtCore.Qt.LeftButton and self.dragging:
            self.canvas().panActionEnd(event.pos())
            self.dragging = False


#############################################################################


def main():
    """LUMENS application main entry point.
    """
    
    window = MainWindow()
    window.showMaximized()
    splashScreen.finish(window)
    window.raise_()
    
    if window.checkDefaultBasemap():
        window.loadDefaultLayers()
        ##window.loadMap() # DEBUG on-the-fly projection
    else:
        window.loadMapCanvas()
    
    # Pan mode by default
    window.handlerSetPanMode()
    
    app.setWindowIcon(QtGui.QIcon('ui/icons/app.ico'))
    app.exec_()
    app.deleteLater()
    
    QgsApplication.exitQgis()


#############################################################################


if __name__ == "__main__":
    main()

