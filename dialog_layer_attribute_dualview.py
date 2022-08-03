#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from qgis.core import *
from qgis.gui import *
from PyQt5 import QtCore, QtGui

from menu_factory import MenuFactory

class DialogLayerAttributeDualView(QtGui.QDialog):
    """Dialog class for showing the attribute table of a vector layer.
    """
    
    def __init__(self, vectorLayer, parent):
        """Constructor method for initializing a layer attribute dialog window instance.
        
        Args:
            vectorLayer (QgsVectorLayer): a vector layer instance.
            parent: the dialog's parent instance.
        """
        super(DialogLayerAttributeDualView, self).__init__(parent)
        
        self.vectorLayer = vectorLayer
        self.main = parent
        self.dialogTitle = MenuFactory.getLabel(MenuFactory.APP_ATTRIBUTE_EDITOR) + ' - ' + self.vectorLayer.name()
        
        self.setupUi(self)
        
        self.dualView.init(self.vectorLayer, self.main.mapCanvas, QgsDistanceArea())
        self.dualView.setView(QgsDualView.AttributeEditor)
        
        self.actionToggleEditLayer.triggered.connect(self.handlerToggleEditLayer)
    
    
    def setupUi(self, parent):
        """Method for building the dialog UI.
        
        Args:
            parent: the dialog's parent instance.
        """
        self.dialogLayout = QtGui.QVBoxLayout(parent)
        
        self.toolBar = QtGui.QToolBar(self)
        self.dialogLayout.addWidget(self.toolBar)
        
        icon = QtGui.QIcon(':/ui/icons/iconActionToggleEdit.png')
        self.actionToggleEditLayer = QtGui.QAction(icon, MenuFactory.getLabel(MenuFactory.APP_TOGGLE_EDIT_LAYER), self)
        self.actionToggleEditLayer.setCheckable(True)
        self.toolBar.addAction(self.actionToggleEditLayer)
        
        self.dualView = QgsDualView()
        self.dialogLayout.addWidget(self.dualView)
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(600, 400)
        self.resize(parent.sizeHint())
    
    
    def closeEvent(self, event):
        """Overload method that is called when the dialog widget is closed.
        
        Args:
            event (QCloseEvent): the close widget event.
        """
        ##super(DialogLayerAttributeDualView, self).closeEvent(event)
        
        reply = self.confirmSaveLayer()
        
        if reply == QtGui.QMessageBox.Save:
            event.accept()
        elif reply == QtGui.QMessageBox.No:
            event.accept()
        elif reply == QtGui.QMessageBox.Cancel:
            event.ignore()
        elif reply == None:
            # Click toggle edit button => close dialog => (layer was not modified)
            self.vectorLayer.rollBack()
            self.vectorLayer.setReadOnly()
    
    
    def confirmSaveLayer(self):
        """Method for confirming saving the changes made to the layer.
        """
        reply = None
        
        if self.vectorLayer.isModified():
            reply = QtGui.QMessageBox.question(
                self,
                MenuFactory.getLabel(MenuFactory.MSG_APP_SAVE_LAYER),
                MenuFactory.getDescription(MenuFactory.MSG_APP_SAVE_LAYER) + ' {0}?'.format(self.vectorLayer.name()),
                QtGui.QMessageBox.Save|QtGui.QMessageBox.No|QtGui.QMessageBox.Cancel,
                QtGui.QMessageBox.Cancel
            )
            
            if reply == QtGui.QMessageBox.Save:
                self.vectorLayer.commitChanges() # save changes to layer
                self.vectorLayer.setReadOnly()
            elif reply == QtGui.QMessageBox.No:
                self.vectorLayer.rollBack()
                self.vectorLayer.setReadOnly()
            elif reply == QtGui.QMessageBox.Cancel:
                pass
            
        return reply
    
    
    def handlerToggleEditLayer(self):
        """Slot method when the edit layer button is clicked.
        """
        if self.actionToggleEditLayer.isChecked():
            self.vectorLayer.setReadOnly(False)
            self.vectorLayer.startEditing()
        else:
            reply = self.confirmSaveLayer()
            
            print reply
            
            if reply == QtGui.QMessageBox.Cancel:
                self.actionToggleEditLayer.setChecked(True) # Keep toggle edit button checked
            elif reply == None:
                # Click toggle edit button => select one feature => click toggle edit button => (layer was not modified)
                self.vectorLayer.rollBack()
                self.vectorLayer.setReadOnly()
