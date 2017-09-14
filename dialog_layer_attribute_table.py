#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from qgis.core import *
from qgis.gui import *
from PyQt4 import QtCore, QtGui


class DialogLayerAttributeTable(QtGui.QDialog):
    """Dialog class for showing the attribute table of a vector layer.
    """
    
    def __init__(self, vectorLayer, parent):
        """Constructor method for initializing a layer attribute table dialog window instance.
        
        Args:
            vectorLayer (QgsVectorLayer): a vector layer instance.
            parent: the dialog's parent instance.
        """
        super(DialogLayerAttributeTable, self).__init__(parent)
        
        self.vectorLayer = vectorLayer
        self.main = parent
        self.dialogTitle = 'Attribute Table - ' + self.vectorLayer.name() + ' - Total Features: ' + str(self.vectorLayer.featureCount())
        self.featureDeleted = False
        
        self.setupUi(self)
        
        # Initialize the Attribute Table View
        self.vectorLayerCache = QgsVectorLayerCache(self.vectorLayer, self.vectorLayer.featureCount())
        self.attributeTableModel = QgsAttributeTableModel(self.vectorLayerCache)
        self.attributeTableModel.loadLayer()
        self.attributeTableFilterModel = QgsAttributeTableFilterModel(self.main.mapCanvas, self.attributeTableModel)
        self.attributeTableView.setModel(self.attributeTableFilterModel)
        
        self.actionToggleEditLayer.triggered.connect(self.handlerToggleEditLayer)
        self.actionDeleteSelectedFeature.triggered.connect(self.handlerDeleteSelectedFeature)
        self.actionExpressionBuilderDialog.triggered.connect(self.handlerExpressionBuilderDialog)
    
    
    def setupUi(self, parent):
        """Method for building the dialog UI.
        
        Args:
            parent: the dialog's parent instance.
        """
        self.dialogLayout = QtGui.QVBoxLayout(parent)
        
        self.toolBar = QtGui.QToolBar(self)
        self.dialogLayout.addWidget(self.toolBar)
        
        icon = QtGui.QIcon(':/ui/icons/iconActionToggleEdit.png')
        self.actionToggleEditLayer = QtGui.QAction(icon, 'Toggle Edit Layer', self)
        self.actionToggleEditLayer.setCheckable(True)
        self.toolBar.addAction(self.actionToggleEditLayer)
        
        icon = QtGui.QIcon(':/ui/icons/iconActionDelete.png')
        self.actionDeleteSelectedFeature = QtGui.QAction(icon, 'Delete Selected Feature', self)
        self.actionDeleteSelectedFeature.setDisabled(True)
        self.toolBar.addAction(self.actionDeleteSelectedFeature)
        
        icon = QtGui.QIcon(':/ui/icons/iconActionFeatureSelectExpression.png')
        self.actionExpressionBuilderDialog = QtGui.QAction(icon, 'Select Features By Expression', self)
        self.toolBar.addAction(self.actionExpressionBuilderDialog)
        
        self.attributeTableView = QgsAttributeTableView()
        
        self.dialogLayout.addWidget(self.attributeTableView)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(700, 500)
        self.resize(parent.sizeHint())
    
    
    def closeEvent(self, event):
        """Overload method that is called when the dialog widget is closed.
        
        Args:
            event (QCloseEvent): the close widget event.
        """
        reply = self.confirmSaveLayer()
        
        if reply == QtGui.QMessageBox.Save:
            # If a row was selected in the attribute table, remove the selection on the vector layer
            self.vectorLayer.removeSelection()
            event.accept()
        elif reply == QtGui.QMessageBox.No:
            self.vectorLayer.removeSelection()
            event.accept()
        elif reply == QtGui.QMessageBox.Cancel:
            event.ignore()
        elif reply == None:
            # Click toggle edit button => close dialog => (layer was not modified)
            self.vectorLayer.rollBack()
            self.vectorLayer.setReadOnly()
            self.vectorLayer.removeSelection()
    
    
    def confirmSaveLayer(self):
        """Method for confirming saving the changes made to the layer.
        """
        reply = None
        
        if self.vectorLayer.isModified() or self.featureDeleted:
            reply = QtGui.QMessageBox.question(
                self,
                'Save Layer Changes',
                'Do you want to save the changes made to layer {0}?'.format(self.vectorLayer.name()),
                QtGui.QMessageBox.Save|QtGui.QMessageBox.No|QtGui.QMessageBox.Cancel,
                QtGui.QMessageBox.Cancel
            )
            
            if reply == QtGui.QMessageBox.Save:
                if self.featureDeleted:
                    self.deleteFeatures()
                self.vectorLayer.commitChanges() # save changes to layer
                self.vectorLayer.setReadOnly()
                self.main.mapCanvas.refresh()
            elif reply == QtGui.QMessageBox.No:
                self.vectorLayer.rollBack()
                self.vectorLayer.setReadOnly()
            elif reply == QtGui.QMessageBox.Cancel:
                pass
            
        return reply
    
    
    def deleteFeatures(self):
        """Method for deleting vector layer features (table rows that are set hidden).
        """
        for tableRow in range(0, self.attributeTableView.model().rowCount()):
            if self.attributeTableView.isRowHidden(tableRow):
                featureId = self.attributeTableModel.rowToId(tableRow)
                self.vectorLayer.deleteFeature(featureId)
    
    
    def handlerDeleteSelectedFeature(self):
        """Slot method for marking (hiding) a selected feature in the attribute table to be deleted.
        """
        deletedRow = None
        deletedRow = self.attributeTableView.currentIndex()
        #self.attributeTableModel.removeRow(self.attributeTableView.currentIndex().row())
        reply = QtGui.QMessageBox.question(
            self,
            'Delete Feature',
            'Do you want to delete feature {0}?'.format(deletedRow.row()),
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
            QtGui.QMessageBox.No
        )
        if reply == QtGui.QMessageBox.Yes:
            self.featureDeleted = True # Flag that a feature has been deleted
            self.attributeTableView.hideRow(deletedRow.row()) # Just hide the row
    
    
    def handlerToggleEditLayer(self):
        """Slot method when the edit layer button is clicked.
        """
        if self.actionToggleEditLayer.isChecked():
            self.vectorLayer.setReadOnly(False)
            self.vectorLayer.startEditing()
            self.actionDeleteSelectedFeature.setEnabled(True)
        else:
            self.actionDeleteSelectedFeature.setDisabled(True)
            reply = self.confirmSaveLayer()
            
            if reply == QtGui.QMessageBox.Cancel:
                self.actionToggleEditLayer.setChecked(True) # Keep toggle edit button checked
                self.actionDeleteSelectedFeature.setEnabled(True)
            elif reply == None:
                # Click toggle edit button => select one feature => click toggle edit button => (layer was not modified)
                self.vectorLayer.rollBack()
                self.vectorLayer.setReadOnly()
    
    
    def handlerExpressionBuilderDialog(self):
        """Slot method for showing the QGIS expression builder dialog.
        """
        dialog = QgsExpressionBuilderDialog(self.vectorLayer)
        dialog.exec_()
