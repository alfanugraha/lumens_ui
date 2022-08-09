#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, sys, logging, subprocess, tempfile
from qgis.core import *
from qgis.gui import *

# from qgis.PyQt.QtCore import *
# from qgis.PyQt.QtWidgets import *
# from qgis.PyQt.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5.QtWebKitWidgets import QWebView

import resource

QgsApplication.setPrefixPath(os.environ['QGIS_PREFIX_PATH'], True) # The True value is important
qgs = QgsApplication([], False)
qgs.initQgis()

app = QApplication(sys.argv)

splashImage = QPixmap('ui/images/splashbw.png')
splashScreen = QSplashScreen(splashImage, Qt.WindowStaysOnTopHint)
splashScreen.setMask(splashImage.mask())
splashScreen.show()

# import qgis.processing
# ##import processing
from core.ProcessingConfig import ProcessingConfig
from core.Processing import Processing
ProcessingConfig.setSettingValue('ACTIVATE_R', True) # R provider is not activated by default
ProcessingConfig.setSettingValue('R_FOLDER', os.environ['RPATH'])
ProcessingConfig.setSettingValue('R_LIBS_USER', os.environ['RLIBS'])
ProcessingConfig.setSettingValue('RSCRIPTS_FOLDER', os.environ['RSCRIPTS'])
ProcessingConfig.setSettingValue('R_USE64', os.environ['R_USE64'])
Processing.initialize()
from tools.system import *

from utils import QPlainTextEditLogger

# Import LUMENS dialog classes here
from dialog_lumens_createdatabase import DialogLumensCreateDatabase

from dialog_lumens_pur import DialogLumensPUR
from dialog_lumens_ques import DialogLumensQUES
from dialog_lumens_ta import DialogLumensTA
from dialog_lumens_sciendo import DialogLumensSCIENDO

from menu_factory import MenuFactory

__version__ = '2.0.0'

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.appSettings = {
            'debug': False,
            'appDir': os.path.dirname(os.path.realpath(__file__)),
            'appSettingsFile': 'settings.ini',
            'ROutFile': os.path.join(userFolder(), 'processing_script.r.Rout'),
            'selectShapefileExt': '.shp',
            'selectRasterfileExt': '.tif',
            'selectProjectFileExt': '.lpj',
            'langDir': 'lang',
            'dataDir': 'data',
            'basemapDir': 'basemap',
            'vectorDir': 'vector',
            'defaultLanguage': 'en',
            'defaultLanguageProperties': '',
            'defaultBasemapFile': 'basemap.tif',
            'defaultBasemapFilePath': '', #data/basemap/lu00_48s_100m.tif
            'defaultVectorFile': 'landmarks.shp',
            'defaultVectorFilePath': '',
            'defaultHabitatLookupTable': '',
            'selectQgsProjectfileExt': '.qgs',
            'selectShapefileExt': '.shp',
            'selectRasterfileExt': '.tif',
            'selectCsvfileExt': '.csv',
            'selectProjectfileExt': '.lpj',
            'selectZipfileExt': '.lpa',
            'selectDatabasefileExt': '.dbf',
            'selectHTMLfileExt': '.html',
            'selectTextfileExt': '.txt',
            'selectCarfileExt': '.car',
            'selectLdbasefileExt': '.ldb',
            'defaultExtent': QgsRectangle(95, -11, 140, 11), # Southeast Asia extent
            'defaultCRS': "EPSG:4326", # EPSG 4326 - WGS 84
            'folderPUR': 'PUR',
            'folderQUES': 'QUES',
            'folderTA': 'TA',
            'folderSCIENDO': 'SCIENDO',
            'folderTemp': os.path.join(tempfile.gettempdir(), 'LUMENS'),
            'acceptedDocumentFormats': ('.doc', 'docx', '.rtf', '.xls', '.xlsx', '.txt', '.log', '.csv'),
            'acceptedWebFormats': ('.html', '.htm'),
            'acceptedSpatialFormats': ('.shp', '.tif'),
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
                'dissolvedShapefile': '', 
            },
            'DialogLumensOpenDatabase': {
                'projectFile': '',
                'projectFolder': '',
            },
            'DialogLumensAddLandcoverRaster': {
                'rasterfile': '',
                'period': '',
                'description': '',
            },
            'DialogLumensAddPeat': {
                'rasterfile': '',
                'description': '',
            },
            'DialogLumensPUR': {
                'referenceData': '',
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
                #'includePeat': '',
            },
            'DialogLumensQUESCPeatlandCarbonAccounting': {
                'landUse1': '',
                'landUse2': '',
                'planningUnit': '',
                'carbonTable': '',
                'nodata': '',
                #'includePeat': '',
                'peat': '',
                # 'peatCell': '',
                'peatTable': '',
            },
            # 'DialogLumensQUESCSummarizeMultiplePeriod': { '': '', },
            'DialogLumensQUESBAnalysis': {
                'landUse1': '',
                'landUse2': '',
                'landUse3': '',
                'planningUnit': '',
                'nodata': '',
                'edgeContrast': '',
                # 'habitatLookup': '',
                'windowShape': '',
                'samplingWindowSize': '',
                'adjacentOnly': '',
                'samplingGridRes': '',
            },
            'DialogLumensTAAbacusOpportunityCostCurve': {
                'projectFile': '',
            },
            'DialogLumensTAOpportunityCostCurve': {
                'csvNPVTable': '',
                'QUESCDatabase': '',
                'costThreshold': '',
            },
            'DialogLumensTAOpportunityCostMap': {
                'landUse1': '',
                'landUse2': '',
                'planningUnit': '',
                'carbon': '',
                'csvProfitability': '',
                'nodata': '',
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
                'year': '',
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
                'landUseCover': '',
                'landRequirementTable': '',
                'descriptiveAnalysisOutput': '',
            },
            'DialogLumensTARegionalEconomyScenario': {
                'landRequirement': '',
                'finalDemandChangeScenario': '',
                'gdpChangeScenario': '',
            },
            'DialogLumensTAImpactofLandUsetoRegionalEconomyIndicatorAnalysis': {
                'landRequirement': '',
                'landUseCover': '',
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
                'landUse1': '',
                'landUse2': '',
                'planningUnit': '',
            },
            'DialogLumensSCIENDOCreateRasterCube': {
                'simulationIndex': '',
                'factorsDir': '',
            },
            'DialogLumensSCIENDOCalculateWeightofEvidence': {
                'simulationIndex': '',
                'landUseLookup': '',
            },
            'DialogLumensSCIENDOSimulateLandUseChange': {
                'simulationIndex': '',
                'iteration': '',
            },
            'DialogLumensSCIENDOSimulateWithScenario': {
                'factorsDir': '',
                'landUseLookup': '',
                'baseYear': '',
                'location': '',
            },
        }

        self.openDialogs = []

        # For keeping track of data added to the project
        self.dataLandUseCover = {}
        self.dataPlanningUnit = {}
        self.dataFactor = {}
        self.dataTable = {}

        self.appSettings['defaultLanguageProperties'] = os.path.join(self.appSettings['langDir'], 'lang_' + self.appSettings['defaultLanguage'] + '.properties')
        MenuFactory.setMenuProperties(self.appSettings['defaultLanguageProperties'], self.appSettings['defaultLanguage'])   
         
        # Build the mainwindow UI!
        self.setupUi()

        # For holding QgsVectorLayer/QgsRasterLayer objects
        self.qgsLayerList = dict()

        # PyQT model+view for layers list
        self.layerListModel = QStandardItemModel(self.layerListView)
        ##self.layerListModel.setSupportedDragActions(QtCore.Qt.MoveAction)
        self.layerListView.setModel(self.layerListModel)

        # LUMENS action handlers
        # Database menu
        self.actionDialogLumensCreateDatabase.triggered.connect(self.handlerDialogLumensCreateDatabase)
        # self.actionLumensOpenDatabase.triggered.connect(self.handlerLumensOpenDatabase)
        # self.actionLumensCloseDatabase.triggered.connect(self.handlerLumensCloseDatabase)
        # self.actionLumensExportDatabase.triggered.connect(self.handlerLumensExportDatabase)
        # self.actionDialogLumensAddData.triggered.connect(self.handlerDialogLumensAddData)
        # self.actionLumensDeleteData.triggered.connect(self.handlerLumensDeleteData)
        # self.actionLumensDatabaseStatus.triggered.connect(self.handlerLumensDatabaseStatus)
        
        # PUR menu
        self.actionDialogLumensPUR.triggered.connect(self.handlerDialogLumensPUR)
        
        # QUES menu
        self.actionDialogLumensQUES.triggered.connect(self.handlerDialogLumensQUES)
        
        # TA menu
        self.actionDialogLumensTA.triggered.connect(self.handlerDialogLumensTA)
        # self.actionDialogLumensTAOpportunityCost.triggered.connect(self.handlerDialogLumensTAOpportunityCost)
        # self.actionDialogLumensTARegionalEconomy.triggered.connect(self.handlerDialogLumensTARegionalEconomy)
        
        # SCIENDO menu
        self.actionDialogLumensSCIENDO.triggered.connect(self.handlerDialogLumensSCIENDO)

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
        self.windowTitle = 'LUMENS v{0} {1}'
        self.setWindowTitle(self.windowTitle.format(__version__, ''))

        self.centralWidget = QWidget(self)
        self.centralWidget.setStyleSheet('QWidget { background-color: rgb(225, 229, 237); }')
        self.centralWidget.setMinimumSize(1024, 600)
        self.setCentralWidget(self.centralWidget)

        # Custom context menu when clicking on main window
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        # Create the default menus
        self.menubar = self.menuBar()
        self.fileMenu = self.menubar.addMenu('&' + MenuFactory.getLabel(MenuFactory.FILE_TITLE))
        self.viewMenu = self.menubar.addMenu('&' + MenuFactory.getLabel(MenuFactory.VIEW_TITLE))
        self.modeMenu = self.menubar.addMenu('&' + MenuFactory.getLabel(MenuFactory.MODE_PAN))
        # self.toolsMenu = self.menubar.addMenu(MenuFactory.getLabel(MenuFactory.TOOLS_TITLE))
        self.databaseMenu = self.menubar.addMenu('&' + MenuFactory.getLabel(MenuFactory.DATABASE_TITLE))
        self.purMenu = self.menubar.addMenu('&PUR')
        self.quesMenu = self.menubar.addMenu('&QUES')
        self.taMenu = self.menubar.addMenu('&TA')
        self.sciendoMenu = self.menubar.addMenu('&SCIENDO')
        self.helpMenu = self.menubar.addMenu(MenuFactory.getLabel(MenuFactory.HELP_TITLE))

        # The menu bar must be hidden
        self.actionToggleMenubar = QAction(MenuFactory.getLabel(MenuFactory.VIEW_MENU_BAR), self) 
        self.actionToggleMenubar.setShortcut('F11')
        self.actionToggleMenubar.setCheckable(True)
        self.actionToggleMenubar.setChecked(False)
        # self.actionToggleMenubar.triggered.connect(self.handlerToggleMenuBar)
        # self.actionToggleMenubar.trigger()

        # Left floating toolbar for map
        self.toolBar = QToolBar(self)
        self.toolBar.setStyleSheet('QToolBar { background-color: rgb(225, 229, 237); } QToolButton { color: rgb(173, 185, 202); }')
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)
        self.toolBar.setOrientation(QtCore.Qt.Vertical)
        self.toolBar.setAllowedAreas(QtCore.Qt.LeftToolBarArea)
        
        self.dialogToolBar = QToolBar(self)
        self.dialogToolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.dialogToolBar.setIconSize(QtCore.QSize(50, 50))
        self.dialogToolBar.setMovable(False)
        self.dialogToolBar.setStyleSheet('QToolBar { background: url(./ui/images/logo.png) right no-repeat; padding: 10px; background-color: rgb(225, 229, 237); } QToolButton { color: rgb(95, 98, 102); }')
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.dialogToolBar)

        self.statusBar = QStatusBar(self)
        self.statusBar.setStyleSheet('QStatusBar { background-color: rgb(225, 229, 237); }')
        self.statusBar.setSizeGripEnabled(False)

        self.labelMapCanvasCoordinate = QLabel(self)
        self.labelMapCanvasCoordinate.setStyleSheet('QLabel { margin-right: 10px; color: rgb(173, 185, 202); }')
        self.labelMapCanvasCoordinate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.labelMapCanvasCoordinate.setVisible(False)
        
        self.statusBar.addPermanentWidget(self.labelMapCanvasCoordinate)
        self.setStatusBar(self.statusBar)

        # Create the actions and assigned them to the menus
        self.actionQuit = QAction(MenuFactory.getLabel(MenuFactory.FILE_QUIT), self)
        self.actionQuit.setShortcut(QKeySequence.Quit)
        
        self.actionToggleDialogToolbar = QAction(MenuFactory.getLabel(MenuFactory.VIEW_TOP_TOOLBAR), self)
        self.actionToggleDialogToolbar.setCheckable(True)
        self.actionToggleDialogToolbar.setChecked(True)
        
        self.actionToggleToolbar = QAction(MenuFactory.getLabel(MenuFactory.VIEW_MAP_TOOLBAR), self)
        self.actionToggleToolbar.setCheckable(True)
        self.actionToggleToolbar.setChecked(True)
        
        icon = QIcon(':/ui/icons/iconActionZoomIn.png')
        self.actionZoomIn = QAction(icon, MenuFactory.getLabel(MenuFactory.APP_ZOOM_IN), self)
        self.actionZoomIn.setShortcut(QKeySequence.ZoomIn)

        icon = QIcon(':/ui/icons/iconActionZoomOut.png')
        self.actionZoomOut = QAction(icon, MenuFactory.getLabel(MenuFactory.APP_ZOOM_OUT), self)
        self.actionZoomOut.setShortcut(QKeySequence.ZoomOut)

        icon = QIcon(':/ui/icons/iconActionPan.png')
        self.actionPan = QAction(icon, MenuFactory.getLabel(MenuFactory.APP_PAN), self)
        self.actionPan.setShortcut('Ctrl+1')
        self.actionPan.setCheckable(True)
        
        icon = QIcon(':/ui/icons/iconActionSelect.png')
        self.actionSelect = QAction(icon, MenuFactory.getLabel(MenuFactory.APP_SELECT), self)
        self.actionSelect.setShortcut('Ctrl+2')
        self.actionSelect.setCheckable(True)
        
        icon = QIcon(':/ui/icons/iconActionInfo.png')
        self.actionInfo = QAction(icon, MenuFactory.getLabel(MenuFactory.APP_INFO), self)
        self.actionInfo.setShortcut('Ctrl+3')
        self.actionInfo.setCheckable(True)
        
        icon = QIcon(':/ui/icons/iconActionAdd.png')
        self.actionAddLayer = QAction(icon, MenuFactory.getLabel(MenuFactory.APP_ADD_LAYER), self)
        
        icon = QIcon(':/ui/icons/iconActionDelete.png')
        self.actionDeleteLayer = QAction(icon, MenuFactory.getLabel(MenuFactory.APP_DELETE_LAYER), self)
        self.actionDeleteLayer.setDisabled(True)
        
        icon = QIcon(':/ui/icons/iconActionTableEditor.png')
        self.actionTableEditor = QAction(icon, MenuFactory.getLabel(MenuFactory.APP_TABLE_EDITOR), self)
        self.actionTableEditor.setDisabled(True)
        
        icon = QIcon(':/ui/icons/iconActionRefresh.png')
        self.actionRefresh = QAction(icon, MenuFactory.getLabel(MenuFactory.APP_REFRESH), self)
        self.actionRefresh.setShortcut('Ctrl+R')
        
        icon = QIcon(':/ui/icons/iconActionZoomFull.png')
        self.actionZoomFull = QAction(icon, MenuFactory.getLabel(MenuFactory.APP_ZOOM_FULL), self)
        self.actionZoomFull.setShortcut('Ctrl+F')
        
        icon = QIcon(':/ui/icons/iconActionZoomLayer.png')
        self.actionZoomLayer = QAction(icon, MenuFactory.getLabel(MenuFactory.APP_ZOOM_TO_LAYER), self)
        self.actionZoomLayer.setShortcut('Ctrl+L')
        self.actionZoomLayer.setDisabled(True)
        
        icon = QIcon(':/ui/icons/iconActionZoomSelected.png')
        self.actionZoomSelected = QAction(icon, MenuFactory.getLabel(MenuFactory.APP_ZOOM_TO_SELECTED), self)
        self.actionZoomSelected.setShortcut('Ctrl+S')
        self.actionZoomSelected.setDisabled(True)
        
        icon = QIcon(':/ui/icons/iconActionPanSelected.png')
        self.actionPanSelected = QAction(icon, MenuFactory.getLabel(MenuFactory.APP_PAN_TO_SELECTED), self)
        self.actionPanSelected.setShortcut('Ctrl+P')
        self.actionPanSelected.setDisabled(True)
        
        icon = QIcon(':/ui/icons/iconActionZoomLast.png')
        self.actionZoomLast = QAction(icon, MenuFactory.getLabel(MenuFactory.APP_ZOOM_LAST), self)
        self.actionZoomLast.setShortcut('Ctrl+,')
        self.actionZoomLast.setDisabled(True)
        
        icon = QIcon(':/ui/icons/iconActionZoomNext.png')
        self.actionZoomNext = QAction(icon, MenuFactory.getLabel(MenuFactory.APP_ZOOM_NEXT), self)
        self.actionZoomNext.setShortcut('Ctrl+.')
        self.actionZoomNext.setDisabled(True)
        
        icon = QIcon(':/ui/icons/iconActionLayerAttributeTable.png')
        self.actionLayerAttributeTable = QAction(icon, MenuFactory.getLabel(MenuFactory.APP_LAYER_ATTRIBUTE_TABLE), self)
        self.actionLayerAttributeTable.setShortcut('Ctrl+T')
        self.actionLayerAttributeTable.setDisabled(True)
        
        icon = QIcon(':/ui/icons/iconActionToggleEdit.png')
        self.actionLayerAttributeEditor = QAction(icon, MenuFactory.getLabel(MenuFactory.APP_LAYER_ATTRIBUTE_EDITOR), self)
        self.actionLayerAttributeEditor.setShortcut('Ctrl+A')
        self.actionLayerAttributeEditor.setDisabled(True)
        
        icon = QIcon(':/ui/icons/iconActionFeatureSelectExpression.png')
        self.actionFeatureSelectExpression = QAction(icon, MenuFactory.getLabel(MenuFactory.APP_SELECT_FEATURES_BY_EXPRESSION), self)
        self.actionFeatureSelectExpression.setShortcut('Ctrl+E')
        self.actionFeatureSelectExpression.setDisabled(True)
        
        icon = QIcon(':/ui/icons/iconActionLayerProperties.png')
        self.actionLayerProperties = QAction(icon, MenuFactory.getLabel(MenuFactory.APP_LAYER_PROPERTIES), self)
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
        icon = QIcon(':/ui/icons/iconActionDialogCreateLumensDatabase.png')
        self.actionDialogLumensCreateDatabase = QAction(icon, MenuFactory.getLabel(MenuFactory.APP_PROJ_NEW), self)
        icon = QIcon(':/ui/icons/iconActionLumensOpenDatabase.png')
        self.actionLumensOpenDatabase = QAction(icon, MenuFactory.getLabel(MenuFactory.APP_PROJ_OPEN), self)
        icon = QIcon(':/ui/icons/iconActionLumensCloseDatabase.png')
        self.actionLumensCloseDatabase = QAction(icon, MenuFactory.getLabel(MenuFactory.APP_PROJ_CLOSE), self)
        icon = QIcon(':/ui/icons/iconActionLumensExportDatabase.png')
        self.actionLumensExportDatabase = QAction(icon, MenuFactory.getLabel(MenuFactory.APP_PROJ_EXPORT), self)
        icon = QIcon(':/ui/icons/iconActionDialogLumensAddData.png')
        self.actionDialogLumensAddData = QAction(icon, MenuFactory.getLabel(MenuFactory.APP_PROJ_ADD_DATA), self)
        icon = QIcon(':/ui/icons/iconActionLumensDeleteData.png')
        self.actionLumensDeleteData = QAction(icon, MenuFactory.getLabel(MenuFactory.APP_PROJ_REMOVE_DATA), self)
        icon = QIcon(':/ui/icons/iconActionLumensDatabaseStatus.png')
        self.actionLumensDatabaseStatus = QAction(icon, MenuFactory.getLabel(MenuFactory.APP_PROJ_STATUS), self)
        
        self.databaseMenu.addAction(self.actionDialogLumensCreateDatabase)
        self.databaseMenu.addAction(self.actionLumensOpenDatabase)
        self.databaseMenu.addAction(self.actionLumensCloseDatabase)
        self.databaseMenu.addAction(self.actionLumensExportDatabase)
        self.databaseMenu.addAction(self.actionDialogLumensAddData)
        self.databaseMenu.addAction(self.actionLumensDeleteData)
        self.databaseMenu.addAction(self.actionLumensDatabaseStatus)
        self.databaseMenu.menuAction().setVisible(False)

        # PUR menu
        icon = QIcon(':/ui/icons/iconActionDialogLumensPUR.png')
        self.actionDialogLumensPUR = QAction(icon, MenuFactory.getLabel(MenuFactory.PUR_TITLE), self)
        self.actionDialogLumensPUR.setIconText('PUR')
        
        self.purMenu.addAction(self.actionDialogLumensPUR)
        self.purMenu.menuAction().setVisible(False)

        # QUES menu
        icon = QIcon(':/ui/icons/iconActionDialogLumensQUES.png')
        self.actionDialogLumensQUES = QAction(icon, MenuFactory.getLabel(MenuFactory.QUES_TITLE), self)
        self.actionDialogLumensQUES.setIconText('QUES')
        
        self.quesMenu.addAction(self.actionDialogLumensQUES)
        self.quesMenu.menuAction().setVisible(False)
        
        # TA menu
        icon = QIcon(':/ui/icons/iconActionDialogLumensTA.png')
        self.actionDialogLumensTAOpportunityCost = QAction(icon, MenuFactory.getLabel(MenuFactory.TAOPCOST_TITLE), self)
        self.actionDialogLumensTARegionalEconomy = QAction(icon, MenuFactory.getLabel(MenuFactory.TAREGECO_TITLE), self)
        self.actionDialogLumensTAOpportunityCost.setIconText('TA')
        
        self.actionDialogLumensTA = QAction(icon, MenuFactory.getDescription(MenuFactory.TA_TITLE), self)
        self.actionDialogLumensTA.setIconText('TA')
        
        self.taMenu.addAction(self.actionDialogLumensTAOpportunityCost)
        self.taMenu.addAction(self.actionDialogLumensTARegionalEconomy)
        self.taMenu.menuAction().setVisible(False)
        
        # SCIENDO menu
        icon = QIcon(':/ui/icons/iconActionDialogLumensSCIENDO.png')
        self.actionDialogLumensSCIENDO = QAction(icon, MenuFactory.getDescription(MenuFactory.SCIENDO_TITLE), self)
        self.actionDialogLumensSCIENDO.setIconText('SCIENDO')
        
        self.sciendoMenu.addAction(self.actionDialogLumensSCIENDO)
        self.sciendoMenu.menuAction().setVisible(False)

        # Tools menu
        # self.actionDialogLumensToolsPivot = QtGui.QAction(MenuFactory.getLabel(MenuFactory.TOOLS_PIVOT_TABLE), self)
        # self.toolsMenu.addAction(self.actionDialogLumensToolsPivot)
        
        # Help menu
        icon = QIcon(':/ui/icons/iconActionHelp.png')
        ##self.actionDialogLumensGuide = QAction(icon, 'Open Guide', self)
        self.actionDialogLumensHelp = QAction(icon, MenuFactory.getLabel(MenuFactory.HELP_OPEN_HELP), self)
        self.actionDialogLumensAbout = QAction(MenuFactory.getLabel(MenuFactory.HELP_ABOUT_LUMENS), self)
        
        ##self.helpMenu.addAction(self.actionDialogLumensGuide)
        self.helpMenu.addAction(self.actionDialogLumensHelp)
        self.helpMenu.addSeparator()
        self.helpMenu.addAction(self.actionDialogLumensAbout)

        # Dialog toolbar
        self.dialogToolBar.addAction(self.actionDialogLumensPUR)
        self.dialogToolBar.addAction(self.actionDialogLumensQUES)
        self.dialogToolBar.addAction(self.actionDialogLumensTA)
        self.dialogToolBar.addAction(self.actionDialogLumensSCIENDO)

        self.layoutActiveProject = QHBoxLayout()
        self.labelActiveProject = QLabel(self)
        self.labelActiveProject.setText(MenuFactory.getLabel(MenuFactory.APP_ACTIVE_PROJECT) + ':')
        self.labelActiveProject.setStyleSheet('QLabel { color: rgb(95, 98, 102); }')
        self.layoutActiveProject.addWidget(self.labelActiveProject)

        self.lineEditActiveProject = QLineEdit(self)
        self.lineEditActiveProject.setReadOnly(True)
        self.lineEditActiveProject.setStyleSheet('QLineEdit { background-color: rgb(244, 248, 252); }')
        self.layoutActiveProject.addWidget(self.lineEditActiveProject)

        self.layerListView = QListView(self)
        self.layerListView.setSelectionMode(QAbstractItemView.SingleSelection)
        ##self.layerListView.setMovement(QtGui.QListView.Snap)
        self.layerListView.setDragDropMode(QAbstractItemView.InternalMove)
        self.layerListView.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.layerListView.setDragDropOverwriteMode(False)
        self.layerListView.setAcceptDrops(True)
        self.layerListView.setDropIndicatorShown(True)
        self.layerListView.setDragEnabled(True)
        ##self.layerListView.setFixedWidth(200)

        self.layerListView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        #***********************************************************
        # 'Dashboard' setup
        #***********************************************************

        self.projectModel = QFileSystemModel()
        self.projectModel.setRootPath(QDir.rootPath())
        
        self.projectTreeView = QTreeView()
        self.projectTreeView.setModel(self.projectModel)
        self.projectTreeView.setRootIndex(self.projectModel.index(QDir.rootPath()))
        self.projectTreeView.hideColumn(1) # Hide all columns except name
        self.projectTreeView.hideColumn(2)
        self.projectTreeView.hideColumn(3)

        self.sidebarTabWidget = QTabWidget()
        sidebarTabWidgetStylesheet = """
        QTabWidget::pane {
            border: none;
            background-color: rgb(244, 248, 252);
        }
        QTabBar::tab {
            background-color: rgb(174, 176, 178);
            color: rgb(95, 98, 102);
            height: 40px; 
            width: 100px;
        }
        QTabBar::tab:selected, QTabBar::tab:hover {
            background-color: rgb(244, 248, 252);
            color: rgb(56, 65, 73);
        }
        QTabBar::tab:selected{
            font: bold;
        }
        """
        self.sidebarTabWidget.setStyleSheet(sidebarTabWidgetStylesheet)
        self.sidebarTabWidget.setTabPosition(QTabWidget.North)

        self.tabLayers = QWidget()
        self.tabDatabase = QWidget()
        self.tabDatabase.setStyleSheet('QWidget{ background-color: rgb(244, 248, 252); }')        

        self.layoutTabLayers = QVBoxLayout()
        self.layoutTabDatabase = QVBoxLayout()

        self.tabLayers.setLayout(self.layoutTabLayers)
        self.tabDatabase.setLayout(self.layoutTabDatabase)

        # Move module tab to top level
        self.sidebarTabWidget.addTab(self.tabLayers, MenuFactory.getLabel(MenuFactory.APP_BROWSER)) 
        self.sidebarTabWidget.addTab(self.tabDatabase, MenuFactory.getLabel(MenuFactory.APP_PROJ))

        self.groupBoxProjectLayers = QGroupBox(MenuFactory.getLabel(MenuFactory.APP_LAYERS))
        self.layoutGroupBoxProjectLayers = QHBoxLayout()
        self.groupBoxProjectLayers.setLayout(self.layoutGroupBoxProjectLayers)
        
        self.groupBoxProjectExplore = QGroupBox(MenuFactory.getLabel(MenuFactory.APP_EXPLORE))
        self.layoutGroupBoxProjectExplore = QVBoxLayout()
        self.groupBoxProjectExplore.setLayout(self.layoutGroupBoxProjectExplore)

        self.layoutGroupBoxProjectLayers.addWidget(self.layerListView)
        self.layoutGroupBoxProjectExplore.addWidget(self.projectTreeView)
        self.layoutTabLayers.addWidget(self.groupBoxProjectLayers)
        self.layoutTabLayers.addWidget(self.groupBoxProjectExplore)        

        self.layersToolBar = QToolBar(self)
        self.layersToolBar.setOrientation(QtCore.Qt.Vertical)
        self.layersToolBar.addAction(self.actionAddLayer)
        self.layersToolBar.addAction(self.actionLayerAttributeTable)
        self.layersToolBar.addAction(self.actionLayerAttributeEditor)
        self.layersToolBar.addAction(self.actionLayerProperties)
        self.layersToolBar.addAction(self.actionDeleteLayer)
        self.layersToolBar.addAction(self.actionTableEditor)
        self.layoutGroupBoxProjectLayers.addWidget(self.layersToolBar)

        self.databaseToolBar = QToolBar(self)
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

        self.webContentDatabaseStatus = QWebView(self)

        self.groupBoxDatabaseStatus = QGroupBox(MenuFactory.getLabel(MenuFactory.APP_PROJ_STATUS))
        self.layoutGroupBoxDatabaseStatus = QVBoxLayout()
        self.groupBoxDatabaseStatus.setLayout(self.layoutGroupBoxDatabaseStatus)
        self.layoutTabDatabase.addWidget(self.groupBoxDatabaseStatus)
        self.layoutGroupBoxDatabaseStatus.addWidget(self.webContentDatabaseStatus)  

        # Floating dashboard
        self.sidebarDockWidget = QDockWidget(MenuFactory.getLabel(MenuFactory.VIEW_DASHBOARD), self) 
        self.sidebarDockWidget.setContentsMargins(5, 10, 5, 5)
        self.sidebarDockWidget.setFeatures(self.sidebarDockWidget.features() & QDockWidget.AllDockWidgetFeatures)
        self.sidebarDockWidget.setWidget(self.sidebarTabWidget)
        self.sidebarDockWidget.setStyleSheet('QDockWidget { background-color: rgb(225, 229, 237); } QToolBar { border: none; }') # Remove border for all child QToolBar in sidebar
        # self.sidebarDockWidget.setFloating(True) 
        self.sidebarDockWidgetAction = self.sidebarDockWidget.toggleViewAction()

        self.addDockWidget(Qt.RightDockWidgetArea, self.sidebarDockWidget)

        # Add VIEW menu
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
        self.layoutBody = QHBoxLayout()
        self.layoutBody.setContentsMargins(0, 0, 0, 0)
        self.layoutBody.setAlignment(QtCore.Qt.AlignLeft)

        # Vertical layout for widgets: splitterMain (map canvas widget, log widget), then active project
        self.layoutMain = QVBoxLayout()
        # Reduce gap with statusbar
        self.layoutMain.setContentsMargins(5, 5, 5, 0)
        
        self.contentBody = QWidget()
        self.contentBody.setLayout(self.layoutBody)

        self.log_box = QPlainTextEditLogger(self)
        self.log_box.widget.setStyleSheet('QPlainTextEdit { color: rgb(225, 229, 237); }')
        # # Show the logging widget only in debug mode
        # if not self.appSettings['debug']:
        #     self.log_box.widget.setVisible(False)

        # splitterMain vertically (top down, not left right) splits the map canvas widget and log widget
        self.splitterMain = QSplitter(self)
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
        self.mapCanvas.setDestinationCrs(QgsCoordinateReferenceSystem(self.appSettings['defaultCRS']))
        # labelingEngine = QgsPalLabeling()
        # self.mapCanvas.mapRenderer().setLabelingEngine(labelingEngine)
        # self.mapCanvas.setCanvasColor(QtCore.Qt.white)
        # self.mapCanvas.enableAntiAliasing(True)

        # Initialize the map tools and assign to the related action
        # self.panTool = PanTool(self.mapCanvas)
        # self.panTool.setAction(self.actionPan)
        
        # self.selectTool = SelectTool(self)
        # self.selectTool.setAction(self.actionSelect)

        # self.infoTool = InfoTool(self)
        # self.infoTool.setAction(self.actionInfo)

        # Causes mainwindow size to fill screen ignoring setMinimumSize()
        ##self.resize(self.sizeHint())


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


    def handlerDialogLumensCreateDatabase(self):
        """Slot method for opening a dialog window.
        """
        self.openDialog(DialogLumensCreateDatabase)


    def handlerDialogLumensPUR(self):
        """Slot method for opening a dialog window.
        """
        self.openDialog(DialogLumensPUR)        


    def handlerDialogLumensQUES(self, tabName=''):
        """Slot method for opening a dialog window.
        """
        self.openDialog(DialogLumensQUES, tabName=tabName)        


    def handlerDialogLumensTA(self):
        """Slot method for opening a dialog window.
        """
        self.openDialog(DialogLumensTA)        


    def handlerDialogLumensSCIENDO(self, tabName=''):
        """Slot method for opening a dialog window.
        """
        self.openDialog(DialogLumensSCIENDO, tabName=tabName)        


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
                    QMessageBox.warning(self, 'Duplicate Layer', 'Layer "{0}" has already been added.\nPlease select another file.'.format(layerName))
                    return
            
            layer = None
            layerType = None
            fileExt = os.path.splitext(layerName)[1].lower()
            
            if  fileExt == '.shp' or fileExt == '.dbf':
                layerType = 'vector'
                layer = QgsVectorLayer(layerFile, layerName, 'ogr')
            elif fileExt == '.tif':
                layerType = 'raster'
                layer = QgsRasterLayer(layerFile, layerName)
            
            if not layer.isValid():
                print('ERROR: Invalid layer!')
                return
            
            layerItemData = {
                'layerFile': layerFile,
                'layerName': layerName,
                'layerType': layerType,
                'layer': layerName,
            }
            
            # Can't keep raster/vector object in layerItemData because of object copy error upon drag-drop
            self.qgsLayerList[layerName] = layer
            
            layerItem = QStandardItem(layerName)
            layerItem.setData(layerItemData)
            layerItem.setToolTip(layerFile)
            layerItem.setEditable(False)
            layerItem.setCheckable(True)
            layerItem.setDragEnabled(True)
            layerItem.setDropEnabled(False)
            layerItem.setCheckState(QtCore.Qt.Checked)
            ##self.layerListModel.appendRow(layerItem)
            self.layerListModel.insertRow(0, layerItem) # Insert new layers at top of list
            
            QgsProject.instance().addMapLayer(self.qgsLayerList[layerName])
            # since on-the-fly CRS reprojection is enabled no need to set layer CRS
            # setting canvas extent to layer extent causes canvas to turn blank
            self.qgsLayerList[layerName].setCrs(QgsCoordinateReferenceSystem(self.appSettings['defaultCRS']))
            self.mapCanvas.setExtent(self.qgsLayerList[layerName].extent())
            # self.showVisibleLayers()

    def showVisibleLayers(self):
        """Find checked layers in "layerListModel" and add them to the map canvas layerset.
        """
        layers = []
        i = 0
        
        while self.layerListModel.item(i):
            layerItem = self.layerListModel.item(i)
            layerItemData = layerItem.data()
            
            if layerItem.checkState():
                layers.append(QgsProject.instance().layerTreeRoot().findLayer(self.qgsLayerList[layerItemData['layer']]).setItemVisibilityChecked(False)) 
                
                logging.getLogger(type(self).__name__).info('showing layer: %s', layerItem.text())
            
            i += 1
        
        if i > 0:
            logging.getLogger(type(self).__name__).info('===========================================')
        
        self.mapCanvas.setLayers(layers) #setLayerSet ??

    def checkDefaultBasemap(self):
        """Method for checking the default basemap file.
        """
        if os.path.isfile(self.appSettings['defaultBasemapFilePath']):
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
    #     ##window.loadMap() # DEBUG on-the-fly projection
    else:
        window.loadMapCanvas()
    
    # Pan mode by default
    # window.handlerSetPanMode()
    
    app.setWindowIcon(QIcon('ui/icons/app.ico'))
    app.exec_()
    app.deleteLater()
    
    qgs.exitQgis()

#############################################################################

if __name__ == "__main__":
    main()
    
