#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging

from qgis.core import *
from qgis.gui import *
from PyQt4 import QtCore, QtGui

from utils import is_number
from dialog_lumens_viewer import DialogLumensViewer


class DialogLayerProperties(QtGui.QDialog):
    """LUMENS dialog class for editing layer properties. 
    """
    
    def __init__(self, layer, parent):
        """Constructor method for initializing a LUMENS layer properties dialog window instance.
        
        Args:
            layer (QgsVectorLayer): a vector layer instance.
            parent: the dialog's parent instance.
        """
        super(DialogLayerProperties, self).__init__(parent)
        self.layer = layer
        self.main = parent
        self.dialogTitle = 'LUMENS Layer Properties - ' + self.layer.name()
        self.layerSymbolFillColor = self.styleCategorizedColor = self.styleGraduatedColor = self.styleRuleBasedColor = self.labelColor = QtGui.QColor(109, 54, 141) # purple
        
        if self.main.appSettings['debug']:
            print 'DEBUG: DialogLayerProperties init'
            self.logger = logging.getLogger(type(self).__name__)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            fh = logging.FileHandler(os.path.join(self.main.appSettings['appDir'], 'logs', type(self).__name__ + '.log'))
            fh.setFormatter(formatter)
            self.logger.addHandler(ch)
            self.logger.addHandler(fh)
            self.logger.setLevel(logging.DEBUG)
        
        self.setupUi(self)
        
        self.loadLayerSettings()
        
        self.buttonAddStyleCategorized.clicked.connect(self.handlerAddStyleCategorized)
        self.buttonAddStyleGraduated.clicked.connect(self.handlerAddStyleGraduated)
        self.buttonAddStyleRuleBased.clicked.connect(self.handlerAddStyleRuleBased)
        self.buttonDeleteStyleCategorized.clicked.connect(self.handlerDeleteStyleCategorized)
        self.buttonDeleteStyleGraduated.clicked.connect(self.handlerDeleteStyleGraduated)
        self.buttonDeleteStyleRuleBased.clicked.connect(self.handlerDeleteStyleRuleBased)
        self.buttonDeleteAllStyleCategorized.clicked.connect(self.handlerDeleteAllStyleCategorized)
        self.buttonDeleteAllStyleGraduated.clicked.connect(self.handlerDeleteAllStyleGraduated)
        self.buttonDeleteAllStyleRuleBased.clicked.connect(self.handlerDeleteAllStyleRuleBased)
        self.sliderLayerTransparency.sliderMoved.connect(self.handlerSliderLayerTransparencyMoved)
        self.spinBoxLayerTransparency.valueChanged.connect(self.handlerSpinBoxLayerTransparencyValueChanged)
        self.buttonLayerSymbolFillColor.clicked.connect(self.handlerSelectFillColor)
        self.buttonStyleCategorizedFillColor.clicked.connect(self.handlerSelectFillColor)
        self.buttonStyleGraduatedFillColor.clicked.connect(self.handlerSelectFillColor)
        self.buttonStyleRuleBasedFillColor.clicked.connect(self.handlerSelectFillColor)
        self.buttonExpressionBuilderDialog.clicked.connect(self.handlerExpressionBuilderDialog)
        self.buttonLabelColor.clicked.connect(self.handlerSelectLabelColor)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonApply.clicked.connect(self.applyStyle)
        self.buttonLayerPropertiesHelp.clicked.connect(self.handlerLayerPropertiesHelp)
    
    
    def setupUi(self, parent):
        """Method for building the dialog UI.
        
        Args:
            parent: the dialog's parent instance.
        """
        self.dialogLayout = QtGui.QVBoxLayout()
        
        self.groupBoxLayerStyle = QtGui.QGroupBox('Style')
        self.layoutGroupBoxLayerStyle = QtGui.QVBoxLayout()
        self.layoutGroupBoxLayerStyle.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLayerStyle.setLayout(self.layoutGroupBoxLayerStyle)
        
        self.layoutLayerStyleInfo = QtGui.QVBoxLayout()
        self.layoutLayerStyle = QtGui.QVBoxLayout()
        self.layoutGroupBoxLayerStyle.addLayout(self.layoutLayerStyleInfo)
        
        # styleTypes = ['Single', 'Categorized', 'Graduated', 'Rule-based']
        self.layoutGroupBoxLayerStyle.addLayout(self.layoutLayerStyle)
        
        self.groupBoxLayerTransparency = QtGui.QGroupBox('Transparency')
        self.layoutGroupBoxLayerTransparency = QtGui.QGridLayout()
        self.groupBoxLayerTransparency.setLayout(self.layoutGroupBoxLayerTransparency)
        
        self.styleTabWidget = QtGui.QTabWidget()
        self.styleTabWidget.setTabPosition(QtGui.QTabWidget.North)
        
        # Style tabs
        self.tabStyleSingle = QtGui.QWidget()
        self.layoutGroupBoxStyleSingle = QtGui.QGridLayout()
        self.layoutGroupBoxStyleSingle.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.tabStyleSingle.setLayout(self.layoutGroupBoxStyleSingle)
        
        self.tabStyleCategorized = QtGui.QWidget()
        self.layoutGroupBoxStyleCategorized = QtGui.QGridLayout()
        self.layoutGroupBoxStyleCategorized.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.tabStyleCategorized.setLayout(self.layoutGroupBoxStyleCategorized)
        
        self.tabStyleGraduated = QtGui.QWidget()
        self.layoutGroupBoxStyleGraduated = QtGui.QGridLayout()
        self.layoutGroupBoxStyleGraduated.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.tabStyleGraduated.setLayout(self.layoutGroupBoxStyleGraduated)
        
        self.tabStyleRuleBased = QtGui.QWidget()
        self.layoutGroupBoxStyleRuleBased = QtGui.QGridLayout()
        self.layoutGroupBoxStyleRuleBased.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.tabStyleRuleBased.setLayout(self.layoutGroupBoxStyleRuleBased)
        
        self.styleTabWidget.addTab(self.tabStyleSingle, 'Single')
        self.styleTabWidget.addTab(self.tabStyleCategorized, 'Categorized')
        self.styleTabWidget.addTab(self.tabStyleGraduated, 'Graduated')
        # self.styleTabWidget.addTab(self.tabStyleRuleBased, 'Rule-based')
        
        self.layoutLayerStyle.addWidget(self.groupBoxLayerTransparency)
        self.layoutLayerStyle.addWidget(self.styleTabWidget)
        
        self.labelLayerStyleInfo = QtGui.QLabel()
        self.labelLayerStyleInfo.setText('\n')
        # self.labelLayerStyleInfo.setWordWrap(True)
        self.layoutLayerStyleInfo.addWidget(self.labelLayerStyleInfo)
        
        # Transparency groupbox widgets
        self.labelLayerTransparency = QtGui.QLabel()
        self.labelLayerTransparency.setText('Layer Transparency:')
        self.layoutGroupBoxLayerTransparency.addWidget(self.labelLayerTransparency, 0, 0)
        
        self.sliderLayerTransparency = QtGui.QSlider()
        self.sliderLayerTransparency.setRange(0, 100)
        self.sliderLayerTransparency.setOrientation(QtCore.Qt.Horizontal)
        self.layoutGroupBoxLayerTransparency.addWidget(self.sliderLayerTransparency, 0, 1)
        
        self.spinBoxLayerTransparency = QtGui.QSpinBox()
        self.spinBoxLayerTransparency.setRange(0, 100)
        self.layoutGroupBoxLayerTransparency.addWidget(self.spinBoxLayerTransparency, 0, 2)
        
        # Single style groupbox widgets
        self.labelLayerSymbolFillColor = QtGui.QLabel()
        self.labelLayerSymbolFillColor.setText('Fill color:')
        self.layoutGroupBoxStyleSingle.addWidget(self.labelLayerSymbolFillColor, 0, 0)
        
        self.buttonLayerSymbolFillColor = QtGui.QPushButton()
        self.buttonLayerSymbolFillColor.setObjectName('buttonLayerSymbolFillColor')
        self.buttonLayerSymbolFillColor.setFixedWidth(50)
        self.buttonLayerSymbolFillColor.setStyleSheet('background-color: {0};'.format(self.layerSymbolFillColor.name()))
        self.layoutGroupBoxStyleSingle.addWidget(self.buttonLayerSymbolFillColor, 0, 1)
        
        # Categorized style groupbox widgets
        self.labelStyleCategorizedAttribute = QtGui.QLabel()
        self.labelStyleCategorizedAttribute.setText('Attribute:')
        self.layoutGroupBoxStyleCategorized.addWidget(self.labelStyleCategorizedAttribute, 0, 0)
        
        self.comboBoxStyleCategorizedAttribute = QtGui.QComboBox()
        self.comboBoxStyleCategorizedAttribute.setDisabled(True)
        self.layoutGroupBoxStyleCategorized.addWidget(self.comboBoxStyleCategorizedAttribute, 0, 1)
        
        self.labelStyleCategorizedFillColor = QtGui.QLabel()
        self.labelStyleCategorizedFillColor.setText('Fill color:')
        self.layoutGroupBoxStyleCategorized.addWidget(self.labelStyleCategorizedFillColor, 1, 0)
        
        self.buttonStyleCategorizedFillColor = QtGui.QPushButton()
        self.buttonStyleCategorizedFillColor.setObjectName('buttonStyleCategorizedFillColor')
        self.buttonStyleCategorizedFillColor.setFixedWidth(50)
        self.buttonStyleCategorizedFillColor.setStyleSheet('background-color: {0};'.format(self.styleCategorizedColor.name()))
        self.layoutGroupBoxStyleCategorized.addWidget(self.buttonStyleCategorizedFillColor, 1, 1)
        
        self.labelStyleCategorizedValue = QtGui.QLabel()
        self.labelStyleCategorizedValue.setText('Value:')
        self.layoutGroupBoxStyleCategorized.addWidget(self.labelStyleCategorizedValue, 2, 0)
        
        self.lineEditStyleCategorizedValue = QtGui.QLineEdit()
        self.layoutGroupBoxStyleCategorized.addWidget(self.lineEditStyleCategorizedValue, 2, 1)
        
        self.labelStyleCategorizedLabel = QtGui.QLabel()
        self.labelStyleCategorizedLabel.setText('Label:')
        self.layoutGroupBoxStyleCategorized.addWidget(self.labelStyleCategorizedLabel, 3, 0)
        
        self.lineEditStyleCategorizedLabel = QtGui.QLineEdit()
        self.layoutGroupBoxStyleCategorized.addWidget(self.lineEditStyleCategorizedLabel, 3, 1)
        
        self.layoutButtonStyleCategorized = QtGui.QHBoxLayout()
        self.layoutButtonStyleCategorized.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.layoutButtonStyleCategorized.setSpacing(10)
        
        self.buttonAddStyleCategorized = QtGui.QPushButton()
        self.buttonAddStyleCategorized.setText('Add')
        self.buttonAddStyleCategorized.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.layoutButtonStyleCategorized.addWidget(self.buttonAddStyleCategorized)
        
        self.buttonDeleteStyleCategorized = QtGui.QPushButton()
        self.buttonDeleteStyleCategorized.setText('Delete')
        self.buttonDeleteStyleCategorized.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.layoutButtonStyleCategorized.addWidget(self.buttonDeleteStyleCategorized)
        
        self.buttonDeleteAllStyleCategorized = QtGui.QPushButton()
        self.buttonDeleteAllStyleCategorized.setText('Delete All')
        self.buttonDeleteAllStyleCategorized.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.layoutButtonStyleCategorized.addWidget(self.buttonDeleteAllStyleCategorized)
        
        self.layoutGroupBoxStyleCategorized.addLayout(self.layoutButtonStyleCategorized, 4, 1)
        
        self.tableStyleCategorized = QtGui.QTableWidget()
        headersTableStyleCategorized = ['Color', 'Value', 'Label']
        self.tableStyleCategorized.setColumnCount(len(headersTableStyleCategorized))
        self.tableStyleCategorized.setHorizontalHeaderLabels(headersTableStyleCategorized)
        self.tableStyleCategorized.verticalHeader().setVisible(False)
        self.layoutGroupBoxStyleCategorized.addWidget(self.tableStyleCategorized, 5, 0, 1, 2)
        
        # Graduated style groupbox widgets
        self.labelStyleGraduatedAttribute = QtGui.QLabel()
        self.labelStyleGraduatedAttribute.setText('Attribute:')
        self.layoutGroupBoxStyleGraduated.addWidget(self.labelStyleGraduatedAttribute, 0, 0)
        
        self.comboBoxStyleGraduatedAttribute = QtGui.QComboBox()
        self.comboBoxStyleGraduatedAttribute.setDisabled(True)
        self.layoutGroupBoxStyleGraduated.addWidget(self.comboBoxStyleGraduatedAttribute, 0, 1)
        
        self.labelStyleGraduatedFillColor = QtGui.QLabel()
        self.labelStyleGraduatedFillColor.setText('Fill color:')
        self.layoutGroupBoxStyleGraduated.addWidget(self.labelStyleGraduatedFillColor, 1, 0)
        
        self.buttonStyleGraduatedFillColor = QtGui.QPushButton()
        self.buttonStyleGraduatedFillColor.setObjectName('buttonStyleGraduatedFillColor')
        self.buttonStyleGraduatedFillColor.setFixedWidth(50)
        self.buttonStyleGraduatedFillColor.setStyleSheet('background-color: {0};'.format(self.styleGraduatedColor.name()))
        self.layoutGroupBoxStyleGraduated.addWidget(self.buttonStyleGraduatedFillColor, 1, 1)
        
        self.labelStyleGraduatedLowerValue = QtGui.QLabel()
        self.labelStyleGraduatedLowerValue.setText('Lower value:')
        self.layoutGroupBoxStyleGraduated.addWidget(self.labelStyleGraduatedLowerValue, 2, 0)
        
        self.lineEditStyleGraduatedLowerValue = QtGui.QLineEdit()
        self.layoutGroupBoxStyleGraduated.addWidget(self.lineEditStyleGraduatedLowerValue, 2, 1)
        
        self.labelStyleGraduatedUpperValue = QtGui.QLabel()
        self.labelStyleGraduatedUpperValue.setText('Upper value:')
        self.layoutGroupBoxStyleGraduated.addWidget(self.labelStyleGraduatedUpperValue, 3, 0)
        
        self.lineEditStyleGraduatedUpperValue = QtGui.QLineEdit()
        self.layoutGroupBoxStyleGraduated.addWidget(self.lineEditStyleGraduatedUpperValue, 3, 1)
        
        self.labelStyleGraduatedLabel = QtGui.QLabel()
        self.labelStyleGraduatedLabel.setText('Label:')
        self.layoutGroupBoxStyleGraduated.addWidget(self.labelStyleGraduatedLabel, 4, 0)
        
        self.lineEditStyleGraduatedLabel = QtGui.QLineEdit()
        self.layoutGroupBoxStyleGraduated.addWidget(self.lineEditStyleGraduatedLabel, 4, 1)
        
        self.layoutButtonStyleGraduated = QtGui.QHBoxLayout()
        self.layoutButtonStyleGraduated.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.layoutButtonStyleGraduated.setSpacing(10)
        
        self.buttonAddStyleGraduated = QtGui.QPushButton()
        self.buttonAddStyleGraduated.setText('Add')
        self.buttonAddStyleGraduated.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.layoutButtonStyleGraduated.addWidget(self.buttonAddStyleGraduated)
        
        self.buttonDeleteStyleGraduated = QtGui.QPushButton()
        self.buttonDeleteStyleGraduated.setText('Delete')
        self.buttonDeleteStyleGraduated.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.layoutButtonStyleGraduated.addWidget(self.buttonDeleteStyleGraduated)
        
        self.buttonDeleteAllStyleGraduated = QtGui.QPushButton()
        self.buttonDeleteAllStyleGraduated.setText('Delete All')
        self.buttonDeleteAllStyleGraduated.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.layoutButtonStyleGraduated.addWidget(self.buttonDeleteAllStyleGraduated)
        
        self.layoutGroupBoxStyleGraduated.addLayout(self.layoutButtonStyleGraduated, 5, 1)
        
        self.tableStyleGraduated = QtGui.QTableWidget()
        headersTableStyleGraduated = ['Color', 'Value', 'Label']
        self.tableStyleGraduated.setColumnCount(len(headersTableStyleGraduated))
        self.tableStyleGraduated.setHorizontalHeaderLabels(headersTableStyleGraduated)
        self.tableStyleGraduated.verticalHeader().setVisible(False)
        self.layoutGroupBoxStyleGraduated.addWidget(self.tableStyleGraduated, 6, 0, 1, 2)
        
        # Rule-based style groupbox widgets
        self.labelStyleRuleBasedFillColor = QtGui.QLabel()
        self.labelStyleRuleBasedFillColor.setText('Fill color:')
        self.layoutGroupBoxStyleRuleBased.addWidget(self.labelStyleRuleBasedFillColor, 0, 0)
        
        self.buttonStyleRuleBasedFillColor = QtGui.QPushButton()
        self.buttonStyleRuleBasedFillColor.setObjectName('buttonStyleRuleBasedFillColor')
        self.buttonStyleRuleBasedFillColor.setFixedWidth(50)
        self.buttonStyleRuleBasedFillColor.setStyleSheet('background-color: {0};'.format(self.styleRuleBasedColor.name()))
        self.layoutGroupBoxStyleRuleBased.addWidget(self.buttonStyleRuleBasedFillColor, 0, 1)
        
        self.labelStyleRuleBasedLabel = QtGui.QLabel()
        self.labelStyleRuleBasedLabel.setText('Label:')
        self.layoutGroupBoxStyleRuleBased.addWidget(self.labelStyleRuleBasedLabel, 1, 0)
        
        self.lineEditStyleRuleBasedLabel = QtGui.QLineEdit()
        self.layoutGroupBoxStyleRuleBased.addWidget(self.lineEditStyleRuleBasedLabel, 1, 1)
        
        self.labelStyleRuleBasedRule = QtGui.QLabel()
        self.labelStyleRuleBasedRule.setText('Rule:')
        self.layoutGroupBoxStyleRuleBased.addWidget(self.labelStyleRuleBasedRule, 2, 0)
        
        self.layoutRuleBasedRule = QtGui.QHBoxLayout()
        self.layoutRuleBasedRule.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.layoutRuleBasedRule.setSpacing(10)
        
        self.lineEditStyleRuleBasedRule = QtGui.QLineEdit()
        self.layoutGroupBoxStyleRuleBased.addLayout(self.layoutRuleBasedRule, 2, 1)
        self.layoutRuleBasedRule.addWidget(self.lineEditStyleRuleBasedRule)
        
        self.buttonExpressionBuilderDialog = QtGui.QPushButton()
        self.buttonExpressionBuilderDialog.setText('...')
        self.layoutRuleBasedRule.addWidget(self.buttonExpressionBuilderDialog)
        
        self.labelStyleRuleBasedMinScale = QtGui.QLabel()
        self.labelStyleRuleBasedMinScale.setText('Min scale:')
        self.layoutGroupBoxStyleRuleBased.addWidget(self.labelStyleRuleBasedMinScale, 3, 0)
        
        self.lineEditStyleRuleBasedMinScale = QtGui.QLineEdit()
        self.layoutGroupBoxStyleRuleBased.addWidget(self.lineEditStyleRuleBasedMinScale, 3, 1)
        
        self.labelStyleRuleBasedMaxScale = QtGui.QLabel()
        self.labelStyleRuleBasedMaxScale.setText('Max scale:')
        self.layoutGroupBoxStyleRuleBased.addWidget(self.labelStyleRuleBasedMaxScale, 4, 0)
        
        self.lineEditStyleRuleBasedMaxScale = QtGui.QLineEdit()
        self.layoutGroupBoxStyleRuleBased.addWidget(self.lineEditStyleRuleBasedMaxScale, 4, 1)
        
        self.layoutButtonStyleRuleBased = QtGui.QHBoxLayout()
        self.layoutButtonStyleRuleBased.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.layoutButtonStyleRuleBased.setSpacing(10)
        
        self.buttonAddStyleRuleBased = QtGui.QPushButton()
        self.buttonAddStyleRuleBased.setText('Add')
        self.buttonAddStyleRuleBased.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.layoutButtonStyleRuleBased.addWidget(self.buttonAddStyleRuleBased)
        
        self.buttonDeleteStyleRuleBased = QtGui.QPushButton()
        self.buttonDeleteStyleRuleBased.setText('Delete')
        self.buttonDeleteStyleRuleBased.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.layoutButtonStyleRuleBased.addWidget(self.buttonDeleteStyleRuleBased)
        
        self.buttonDeleteAllStyleRuleBased = QtGui.QPushButton()
        self.buttonDeleteAllStyleRuleBased.setText('Delete All')
        self.buttonDeleteAllStyleRuleBased.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.layoutButtonStyleRuleBased.addWidget(self.buttonDeleteAllStyleRuleBased)
        
        self.layoutGroupBoxStyleRuleBased.addLayout(self.layoutButtonStyleRuleBased, 5, 1)
        
        self.tableStyleRuleBased = QtGui.QTableWidget()
        headersTableStyleRuleBased = ['Color', 'Label', 'Rule', 'Min Scale', 'Max Scale']
        self.tableStyleRuleBased.setColumnCount(len(headersTableStyleRuleBased))
        self.tableStyleRuleBased.setHorizontalHeaderLabels(headersTableStyleRuleBased)
        self.tableStyleRuleBased.verticalHeader().setVisible(False)
        self.layoutGroupBoxStyleRuleBased.addWidget(self.tableStyleRuleBased, 6, 0, 1, 2)
        
        ######################################################################
        
        self.groupBoxLayerLabel = QtGui.QGroupBox('Label')
        self.layoutGroupBoxLayerLabel = QtGui.QVBoxLayout()
        self.layoutGroupBoxLayerLabel.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBoxLayerLabel.setLayout(self.layoutGroupBoxLayerLabel)
        self.layoutLayerLabelInfo = QtGui.QVBoxLayout()
        self.layoutLayerLabel = QtGui.QGridLayout()
        self.layoutGroupBoxLayerLabel.addLayout(self.layoutLayerLabelInfo)
        self.layoutGroupBoxLayerLabel.addLayout(self.layoutLayerLabel)
        
        self.labelLayerLabelInfo = QtGui.QLabel()
        self.labelLayerLabelInfo.setText('\n')
        self.layoutLayerLabelInfo.addWidget(self.labelLayerLabelInfo)
        
        self.labelLayerLabelEnabled = QtGui.QLabel()
        self.labelLayerLabelEnabled.setText('Enable label:')
        self.layoutLayerLabel.addWidget(self.labelLayerLabelEnabled, 0, 0)
        
        self.checkBoxLayerLabelEnabled = QtGui.QCheckBox()
        self.checkBoxLayerLabelEnabled.setChecked(False)
        self.layoutLayerLabel.addWidget(self.checkBoxLayerLabelEnabled, 0, 1)
        self.labelLayerLabelEnabled.setBuddy(self.checkBoxLayerLabelEnabled)
        
        self.labelLayerLabelAttribute = QtGui.QLabel()
        self.labelLayerLabelAttribute.setText('Label attribute:')
        self.layoutLayerLabel.addWidget(self.labelLayerLabelAttribute, 1, 0)
        
        self.comboBoxLayerAttribute = QtGui.QComboBox()
        self.comboBoxLayerAttribute.setDisabled(True)
        self.layoutLayerLabel.addWidget(self.comboBoxLayerAttribute, 1, 1)
        
        self.labelLayerLabelSize = QtGui.QLabel()
        self.labelLayerLabelSize.setText('Label size (points):')
        self.layoutLayerLabel.addWidget(self.labelLayerLabelSize, 2, 0)
        
        self.spinBoxLabelSize = QtGui.QSpinBox()
        self.spinBoxLabelSize.setRange(1, 100)
        self.spinBoxLabelSize.setValue(9)
        self.layoutLayerLabel.addWidget(self.spinBoxLabelSize, 2, 1)
        self.labelLayerLabelSize.setBuddy(self.spinBoxLabelSize)
        
        self.labelLayerLabelColor = QtGui.QLabel()
        self.labelLayerLabelColor.setText('Label color:')
        self.layoutLayerLabel.addWidget(self.labelLayerLabelColor, 3, 0)
        
        self.buttonLabelColor = QtGui.QPushButton()
        self.buttonLabelColor.setFixedWidth(50)
        self.buttonLabelColor.setStyleSheet('background-color: {0};'.format(self.labelColor.name()))
        self.layoutLayerLabel.addWidget(self.buttonLabelColor, 3, 1)
        
        self.layoutButtonBox = QtGui.QHBoxLayout()
        self.layoutButtonBox.setAlignment(QtCore.Qt.AlignRight)
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Cancel)
        self.buttonApply = QtGui.QPushButton()
        self.buttonApply.setText('Apply')
        icon = QtGui.QIcon(':/ui/icons/iconActionHelp.png')
        self.buttonLayerPropertiesHelp = QtGui.QPushButton()
        self.buttonLayerPropertiesHelp.setIcon(icon)
        self.layoutButtonBox.addWidget(self.buttonBox)
        self.layoutButtonBox.addWidget(self.buttonApply)
        self.layoutButtonBox.addWidget(self.buttonLayerPropertiesHelp)
        
        self.dialogLayout.addWidget(self.groupBoxLayerStyle)
        self.dialogLayout.addWidget(self.groupBoxLayerLabel)
        self.dialogLayout.addLayout(self.layoutButtonBox)
        
        self.setLayout(self.dialogLayout)
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(600, 700)
        #self.resize(parent.sizeHint())
    
    
    def loadLayerSettings(self):
        """Method for loading the layer settings and updating the form widgets.
        """
        # Get layer attributes
        provider = self.layer.dataProvider()
        
        if not provider.isValid():
            logging.getLogger(type(self).__name__).error('invalid layer')
            return
        
        attributes = []
        numericAttributes = []
        
        for field in provider.fields():
            attributes.append(field.name())
            fieldType = field.type()
            if fieldType == QtCore.QVariant.Int or fieldType == QtCore.QVariant.Double:
                numericAttributes.append(field.name())
        
        self.comboBoxLayerAttribute.clear()
        self.comboBoxLayerAttribute.addItems(sorted(attributes))
        self.comboBoxLayerAttribute.setEnabled(True)
        
        self.comboBoxStyleCategorizedAttribute.clear()
        self.comboBoxStyleCategorizedAttribute.addItems(sorted(attributes))
        self.comboBoxStyleCategorizedAttribute.setEnabled(True)
        
        # Disable graduated style tab if there are no numeric attributes
        if numericAttributes:
            self.comboBoxStyleGraduatedAttribute.clear()
            self.comboBoxStyleGraduatedAttribute.addItems(sorted(numericAttributes))
            self.comboBoxStyleGraduatedAttribute.setEnabled(True)
        else:
            self.tabStyleGraduated.setDisabled(True)
        
        # Get layer transparency setting
        self.sliderLayerTransparency.setValue(self.layer.layerTransparency())
        self.spinBoxLayerTransparency.setValue(self.layer.layerTransparency())
        
        # Get layer symbol fill color
        symbols = self.layer.rendererV2().symbols()
        self.layerSymbolFillColor = self.styleCategorizedColor = self.styleGraduatedColor = self.styleRuleBasedColor = symbols[0].color()
        
        # Load layer renderer settings
        renderer = self.layer.rendererV2()
        
        if isinstance(renderer, QgsSingleSymbolRendererV2):
            symbols = renderer.symbols()
            self.layerSymbolFillColor = symbols[0].color()
            self.buttonLayerSymbolFillColor.setStyleSheet('background-color: {0};'.format(self.layerSymbolFillColor.name()))
        elif isinstance(renderer, QgsCategorizedSymbolRendererV2):
            categories = renderer.categories()
            for category in categories:
                color = category.symbol().color()
                value = str(category.value())
                label = category.label()
                self.addStyleCategorized(color, value, label)
                self.styleCategorizedColor = color
                self.buttonStyleCategorizedFillColor.setStyleSheet('background-color: {0};'.format(self.styleCategorizedColor.name()))
            attribute = renderer.classAttribute()
            self.comboBoxStyleCategorizedAttribute.setCurrentIndex(self.comboBoxStyleCategorizedAttribute.findText(attribute))
        elif isinstance(renderer, QgsGraduatedSymbolRendererV2):
            ranges = renderer.ranges()
            for range in ranges:
                color = range.symbol().color()
                lowerValue = range.lowerValue()
                upperValue = range.upperValue()
                label = range.label()
                self.addStyleGraduated(color, lowerValue, upperValue, label)
                self.styleGraduatedColor = color
                self.buttonStyleGraduatedFillColor.setStyleSheet('background-color: {0};'.format(self.styleGraduatedColor.name()))
            attribute = renderer.classAttribute()
            self.comboBoxStyleGraduatedAttribute.setCurrentIndex(self.comboBoxStyleGraduatedAttribute.findText(attribute))
        elif isinstance(renderer, QgsRuleBasedRendererV2):
            rootRule = renderer.rootRule()
            rules = rootRule.children()
            for aRule in rules:
                color = aRule.symbol().color()
                rule = aRule.filterExpression()
                label = aRule.label()
                minScale = aRule.scaleMinDenom()
                maxScale = aRule.scaleMaxDenom()
                self.addStyleRuleBased(color, rule, minScale, maxScale, label)
                self.styleRuleBasedColor = color
                self.buttonStyleRuleBasedFillColor.setStyleSheet('background-color: {0};'.format(self.styleRuleBasedColor.name()))
        
        # Get layer label settings
        self.p = QgsPalLayerSettings()
        self.p.readFromLayer(self.layer)
        
        if self.p.enabled:
            self.checkBoxLayerLabelEnabled.setChecked(True)
            self.comboBoxLayerAttribute.setCurrentIndex(self.comboBoxLayerAttribute.findText(self.p.fieldName))
            self.spinBoxLabelSize.setValue(self.p.textFont.pointSize())
            self.labelColor = self.p.textColor
            self.buttonLabelColor.setStyleSheet('background-color: {0};'.format(self.labelColor.name()))
            
    
    def addStyleCategorized(self, color, value, label):
        """Method for adding a categorized style to the table widget.
        """
        newValue = QtGui.QTableWidgetItem(value)
        newLabel = QtGui.QTableWidgetItem(label)
        newColor = QtGui.QTableWidgetItem('')
        newColor.setBackgroundColor(color)
        newColor.setFlags(newColor.flags() & ~QtCore.Qt.ItemIsEditable)
        newValue.setFlags(newValue.flags() & ~QtCore.Qt.ItemIsEditable)
        newLabel.setFlags(newLabel.flags() & ~QtCore.Qt.ItemIsEditable)
        currentRowCount = self.tableStyleCategorized.rowCount()
        self.tableStyleCategorized.insertRow(currentRowCount)
        self.tableStyleCategorized.setItem(currentRowCount, 0, newColor)
        self.tableStyleCategorized.setItem(currentRowCount, 1, newValue)
        self.tableStyleCategorized.setItem(currentRowCount, 2, newLabel)
    
    
    def addStyleGraduated(self, color, lowerValue, upperValue, label):
        """Method for adding a graduated style to the table widget.
        """
        if not lowerValue or not upperValue:
            return
        elif not is_number(lowerValue) or not is_number(upperValue):
            return
        elif float(upperValue) - float(lowerValue) < 0:
            return
        newValue = QtGui.QTableWidgetItem("{0} - {1}".format(str(lowerValue), str(upperValue)))
        newLabel = QtGui.QTableWidgetItem(label)
        newColor = QtGui.QTableWidgetItem('')
        newColor.setBackgroundColor(color)
        newColor.setFlags(newColor.flags() & ~QtCore.Qt.ItemIsEditable)
        newValue.setFlags(newValue.flags() & ~QtCore.Qt.ItemIsEditable)
        newLabel.setFlags(newLabel.flags() & ~QtCore.Qt.ItemIsEditable)
        currentRowCount = self.tableStyleGraduated.rowCount()
        self.tableStyleGraduated.insertRow(currentRowCount)
        self.tableStyleGraduated.setItem(currentRowCount, 0, newColor)
        self.tableStyleGraduated.setItem(currentRowCount, 1, newValue)
        self.tableStyleGraduated.setItem(currentRowCount, 2, newLabel)
    
    
    def addStyleRuleBased(self, color, rule, minScale, maxScale, label):
        """Method for adding a rule-based style to the table widget.
        """
        newLabel = QtGui.QTableWidgetItem(label)
        newRule = QtGui.QTableWidgetItem(rule)
        newMinScale = QtGui.QTableWidgetItem(minScale)
        newMaxScale = QtGui.QTableWidgetItem(maxScale)
        newColor = QtGui.QTableWidgetItem('')
        newColor.setBackgroundColor(color)
        newColor.setFlags(newColor.flags() & ~QtCore.Qt.ItemIsEditable)
        newLabel.setFlags(newLabel.flags() & ~QtCore.Qt.ItemIsEditable)
        newRule.setFlags(newRule.flags() & ~QtCore.Qt.ItemIsEditable)
        newMinScale.setFlags(newMinScale.flags() & ~QtCore.Qt.ItemIsEditable)
        newMaxScale.setFlags(newMaxScale.flags() & ~QtCore.Qt.ItemIsEditable)
        currentRowCount = self.tableStyleRuleBased.rowCount()
        self.tableStyleRuleBased.insertRow(currentRowCount)
        self.tableStyleRuleBased.setItem(currentRowCount, 0, newColor)
        self.tableStyleRuleBased.setItem(currentRowCount, 1, newLabel)
        self.tableStyleRuleBased.setItem(currentRowCount, 2, newRule)
        self.tableStyleRuleBased.setItem(currentRowCount, 3, newMinScale)
        self.tableStyleRuleBased.setItem(currentRowCount, 4, newMaxScale)
    
    
    #***********************************************************
    # 'Layer Properties' QPushButton handlers
    #***********************************************************
    def handlerSliderLayerTransparencyMoved(self, newPosition):
        """Slot method when the transparency slider is moved.
        
        Args:
            newPosition (int): the new position on the slider.
        """
        self.spinBoxLayerTransparency.setValue(newPosition)
    
    
    def handlerSpinBoxLayerTransparencyValueChanged(self, newValue):
        """Slot method when the transparency spinbox value is changed.
        
        Args:
            newValue (int): the new spinbox value.
        """
        self.sliderLayerTransparency.setValue(newValue)
    
    
    def handlerSelectFillColor(self):
        """Slot method when the fill color button is clicked.
        """
        dialog = QtGui.QColorDialog(self.layerSymbolFillColor)
        
        if dialog.exec_():
            selectedColor = dialog.selectedColor()
            sender = self.sender()
            if sender.objectName() == 'buttonLayerSymbolFillColor':
                self.layerSymbolFillColor = selectedColor
            elif sender.objectName() == 'buttonStyleCategorizedFillColor':
                self.styleCategorizedColor = selectedColor
            elif sender.objectName() == 'buttonStyleGraduatedFillColor':
                self.styleGraduatedColor = selectedColor
            elif sender.objectName() == 'buttonStyleRuleBasedFillColor':
                self.styleRuleBasedColor = selectedColor
            sender.setStyleSheet('background-color: {0};'.format(selectedColor.name()))
    
    
    def handlerExpressionBuilderDialog(self):
        """Slot method for showing the QGIS expression builder dialog.
        """
        dialog = QgsExpressionBuilderDialog(self.layer)
        if dialog.exec_():
            self.lineEditStyleRuleBasedRule.setText(dialog.expressionText())
    
    
    def handlerSelectLabelColor(self):
        """Slot method when the label color button is clicked.
        """
        dialog = QtGui.QColorDialog(self.labelColor)
        
        if dialog.exec_():
            self.labelColor = dialog.selectedColor()
            self.buttonLabelColor.setStyleSheet('background-color: {0};'.format(self.labelColor.name()))
    
    
    def handlerAddStyleCategorized(self):
        """Slot method for adding a categorized style.
        """
        value = QtGui.QTableWidgetItem(self.lineEditStyleCategorizedValue.text())
        label = QtGui.QTableWidgetItem(self.lineEditStyleCategorizedLabel.text())
        color = self.styleCategorizedColor
        self.addStyleCategorized(color, value, label)
        self.lineEditStyleCategorizedValue.setText('')
        self.lineEditStyleCategorizedLabel.setText('')
    
    
    def handlerAddStyleGraduated(self):
        """Slot method for adding a graduated style.
        """
        lowerValue = self.lineEditStyleGraduatedLowerValue.text()
        upperValue = self.lineEditStyleGraduatedUpperValue.text()
        label = self.lineEditStyleGraduatedLabel.text()
        color = self.styleGraduatedColor
        self.addStyleGraduated(color, lowerValue, upperValue, label)
        self.lineEditStyleGraduatedLowerValue.setText('')
        self.lineEditStyleGraduatedUpperValue.setText('')
        self.lineEditStyleGraduatedLabel.setText('')
    
    
    def handlerAddStyleRuleBased(self):
        """Slot method for adding a rule-based style.
        """
        label = self.lineEditStyleRuleBasedLabel.text()
        rule = self.lineEditStyleRuleBasedRule.text()
        minScale = self.lineEditStyleRuleBasedMinScale.text()
        maxScale = self.lineEditStyleRuleBasedMaxScale.text()
        color = self.styleRuleBasedColor
        self.addStyleRuleBased(color, rule, minScale, maxScale, label)
        self.lineEditStyleRuleBasedLabel.setText('')
        self.lineEditStyleRuleBasedRule.setText('')
        self.lineEditStyleRuleBasedMinScale.setText('')
        self.lineEditStyleRuleBasedMaxScale.setText('')
    
    
    def handlerDeleteStyleCategorized(self):
        """Slot method for deleting a categorized style.
        """
        currentRow = self.tableStyleCategorized.currentRow()
        self.tableStyleCategorized.removeRow(currentRow)
    
    
    def handlerDeleteAllStyleCategorized(self):
        """Slot method for deleting all categorized styles.
        """
        reply = QtGui.QMessageBox.question(
            self,
            'Delete All',
            'Do you want to delete all?',
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.Cancel,
            QtGui.QMessageBox.Cancel
        )
        
        if reply == QtGui.QMessageBox.Yes:
            self.tableStyleCategorized.setRowCount(0)
        elif reply == QtGui.QMessageBox.Cancel:
            pass
    
    
    def handlerDeleteStyleGraduated(self):
        """Slot method for deleting a graduated style.
        """
        currentRow = self.tableStyleGraduated.currentRow()
        self.tableStyleGraduated.removeRow(currentRow)
    
    
    def handlerDeleteAllStyleGraduated(self):
        """Slot method for deleting all graduated styles.
        """
        reply = QtGui.QMessageBox.question(
            self,
            'Delete All',
            'Do you want to delete all?',
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.Cancel,
            QtGui.QMessageBox.Cancel
        )
        
        if reply == QtGui.QMessageBox.Yes:
            self.tableStyleGraduated.setRowCount(0)
        elif reply == QtGui.QMessageBox.Cancel:
            pass
    
    
    def handlerDeleteStyleRuleBased(self):
        """Slot method for deleting a rule-based style.
        """
        currentRow = self.tableStyleRuleBased.currentRow()
        self.tableStyleRuleBased.removeRow(currentRow)
    
    
    def handlerDeleteAllStyleRuleBased(self):
        """Slot method for deleting all rule-based styles.
        """
        reply = QtGui.QMessageBox.question(
            self,
            'Delete All',
            'Do you want to delete all?',
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.Cancel,
            QtGui.QMessageBox.Cancel
        )
        
        if reply == QtGui.QMessageBox.Yes:
            self.tableStyleRuleBased.setRowCount(0)
        elif reply == QtGui.QMessageBox.Cancel:
            pass


    def handlerLayerPropertiesHelp(self):
        """Slot method for opening the dialog html help document.
        """
        filePath = os.path.join(self.main.appSettings['appDir'], self.main.appSettings['folderHelp'], self.main.appSettings['helpDialogLayerPropertiesFile'])
        
        if os.path.exists(filePath):
            dialog = DialogLumensViewer(self, 'LUMENS Help - {0}'.format('Layer Properties'), 'html', filePath)
            dialog.exec_()
        else:
            QtGui.QMessageBox.critical(self, 'LUMENS Help Not Found', "Unable to open '{0}'.".format(filePath))
            
    
    #***********************************************************
    # Process dialog
    #***********************************************************
    def applyStyle(self):
        """Overload method when the dialog is accepted.
        """
        # Process layer transparency setting
        self.layer.setLayerTransparency(self.sliderLayerTransparency.value())
        
        index = self.styleTabWidget.currentIndex()
        styleType = self.styleTabWidget.tabText(index)
        
        if styleType == 'Single':
            # Process layer symbol fill color
            symbol = QgsFillSymbolV2.createSimple({})
            symbol.setColor(self.layerSymbolFillColor)
            renderer = QgsSingleSymbolRendererV2(symbol)
            self.layer.setRendererV2(renderer)
        elif styleType == 'Categorized':
            # Process categorized symbol for layer
            categories = []
            for tableRow in range(0, self.tableStyleCategorized.rowCount()):
                color = self.tableStyleCategorized.item(tableRow, 0).backgroundColor()
                value = self.tableStyleCategorized.item(tableRow, 1).text()
                label = self.tableStyleCategorized.item(tableRow, 2).text()
                symbol = QgsFillSymbolV2.createSimple({})
                symbol.setColor(color)
                categories.append(QgsRendererCategoryV2(value, symbol, label))
            if categories:
                renderer = QgsCategorizedSymbolRendererV2('', categories)
                renderer.setClassAttribute(self.comboBoxStyleCategorizedAttribute.currentText())
                self.layer.setRendererV2(renderer)
        elif styleType == 'Graduated':
            # Process graduated symbol for layer
            ranges = []
            for tableRow in range(0, self.tableStyleGraduated.rowCount()):
                color = self.tableStyleGraduated.item(tableRow, 0).backgroundColor()
                value = self.tableStyleGraduated.item(tableRow, 1).text()
                values = value.split(' - ')
                lowerValue = float(values[0])
                upperValue = float(values[1])
                label = self.tableStyleGraduated.item(tableRow, 2).text()
                symbol = QgsFillSymbolV2.createSimple({})
                symbol.setColor(color)
                ranges.append(QgsRendererRangeV2(lowerValue, upperValue, symbol, label))
            if ranges:
                renderer = QgsGraduatedSymbolRendererV2('', ranges)
                renderer.setClassAttribute(self.comboBoxStyleGraduatedAttribute.currentText())
                self.layer.setRendererV2(renderer)
        elif styleType == 'Rule-based':
            # Process rule-based symbol for layer
            defaultSymbol = QgsSymbolV2.defaultSymbol(self.layer.geometryType())
            renderer = QgsRuleBasedRendererV2(defaultSymbol)
            rootRule = renderer.rootRule()
            defaultRule = rootRule.children()[0]
            for tableRow in range(0, self.tableStyleRuleBased.rowCount()):
                color = self.tableStyleRuleBased.item(tableRow, 0).backgroundColor()
                label = self.tableStyleRuleBased.item(tableRow, 1).text()
                rule = self.tableStyleRuleBased.item(tableRow, 2).text()
                minScale = self.tableStyleRuleBased.item(tableRow, 3).text()
                maxScale = self.tableStyleRuleBased.item(tableRow, 4).text()
                symbol = QgsFillSymbolV2.createSimple({})
                symbol.setColor(color)
                newRule = defaultRule.clone()
                newRule.setSymbol(symbol)
                newRule.setLabel(label)
                newRule.setFilterExpression(rule)
                if is_number(minScale):
                    newRule.setScaleMinDenom(int(minScale))
                if is_number(maxScale):
                    newRule.setScaleMaxDenom(int(maxScale))
                rootRule.appendChild(newRule)
            rootRule.removeChildAt(0)
            self.layer.setRendererV2(renderer)
                
        
        # Process layer label settings
        if self.checkBoxLayerLabelEnabled.isChecked():
            self.p.enabled = True
            
            self.p.fieldName = self.comboBoxLayerAttribute.currentText()
            self.p.placement = QgsPalLayerSettings.OverPoint
            self.p.displayAll = True
            self.p.textFont.setPointSize(self.spinBoxLabelSize.value())
            self.p.textColor = self.labelColor
            self.p.quadOffset = QgsPalLayerSettings.QuadrantBelow
            self.p.yOffset = 1
            self.p.labelOffsetInMapUnits = False
        else:
            self.p.enabled = False
        
        self.p.writeToLayer(self.layer)
        
        # Finally fresh the MapCanvas and close the dialog
        self.main.mapCanvas.refresh()
        
        
    def accept(self):
        """Overload method when the dialog is accepted.
        """
        self.applyStyle()
        QtGui.QDialog.accept(self)
        
    
    def reject(self):
        """Overload method when the dialog is rejected/closed.
        """
        QtGui.QDialog.reject(self)
    
