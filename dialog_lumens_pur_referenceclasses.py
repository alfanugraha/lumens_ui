#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging
from PyQt4 import QtCore, QtGui
import resource


class DialogLumensPURReferenceClasses(QtGui.QDialog):
    """LUMENS dialog class for PUR reference classes edit window.
    
    Attributes:
        referenceClasses (dict): a dict of a reference classes. The dict key is the ID while the value is the title.
        tableRowCount (int): the number of rows in the reference class table.
    """
    
    def __init__(self, parent):
        """Constructor method for initializing a LUMENS PUR Reference Classes dialog window instance.
        
        Args:
            parent: the main window's parent instance.
        """
        super(DialogLumensPURReferenceClasses, self).__init__(parent)
        print 'DEBUG: DialogLumensPURReferenceClasses init'
        
        self.main = parent
        self.dialogTitle = 'Edit Reference Classes'
        self.tableRowCount = 0
        self.referenceClasses = {}
        
        self.setupUi(self)
        self.initReferenceClassesTable()
        
        self.buttonAddRow.clicked.connect(self.handlerButtonAddRow)
        self.buttonBox.accepted.connect(self.handlerButtonSave)
        self.buttonBox.rejected.connect(self.handlerButtonCancel)
        self.buttonPURReferenceClassesHelp.clicked.connect(self.handlerPURReferenceClassesHelp)
    
    
    def setupUi(self, parent):
        """Method for building the dialog UI.
        
        Args:
            parent: the dialog's parent instance.
        """
        self.dialogLayout = QtGui.QVBoxLayout()
        
        # 'Setup planning unit' GroupBox
        self.groupBoxEditReferenceClasses = QtGui.QGroupBox('Reference classes')
        self.layoutGroupBoxEditReferenceClasses = QtGui.QVBoxLayout()
        self.groupBoxEditReferenceClasses.setLayout(self.layoutGroupBoxEditReferenceClasses)
        self.dialogLayout.addWidget(self.groupBoxEditReferenceClasses)
        
        self.contentButtonEditReferenceClasses = QtGui.QWidget()
        self.layoutButtonEditReferenceClasses = QtGui.QHBoxLayout()
        self.layoutButtonEditReferenceClasses.setContentsMargins(0, 0, 0, 0)
        self.contentButtonEditReferenceClasses.setLayout(self.layoutButtonEditReferenceClasses)
        self.layoutButtonEditReferenceClasses.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.buttonAddRow = QtGui.QPushButton()
        self.buttonAddRow.setText('Add reference class')
        self.buttonAddRow.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.layoutButtonEditReferenceClasses.addWidget(self.buttonAddRow)
        
        self.layoutContentGroupBoxEditReferenceClasses = QtGui.QVBoxLayout()
        self.layoutContentGroupBoxEditReferenceClasses.setContentsMargins(5, 5, 5, 5)
        self.contentGroupBoxEditReferenceClasses = QtGui.QWidget()
        self.contentGroupBoxEditReferenceClasses.setLayout(self.layoutContentGroupBoxEditReferenceClasses)
        self.scrollEditReferenceClasses = QtGui.QScrollArea()
        self.scrollEditReferenceClasses.setWidgetResizable(True);
        self.scrollEditReferenceClasses.setWidget(self.contentGroupBoxEditReferenceClasses)
        self.layoutEditReferenceClassesInfo = QtGui.QVBoxLayout()
        self.labelEditReferenceClassesInfo = QtGui.QLabel()
        self.labelEditReferenceClassesInfo.setText('\n')
        self.labelEditReferenceClassesInfo.setWordWrap(True)
        self.layoutEditReferenceClassesInfo.addWidget(self.labelEditReferenceClassesInfo)
        
        self.layoutButtonBox = QtGui.QHBoxLayout()
        self.layoutButtonBox.setAlignment(QtCore.Qt.AlignRight)
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Save|QtGui.QDialogButtonBox.Cancel)
        icon = QtGui.QIcon(':/ui/icons/iconActionHelp.png')
        self.buttonPURReferenceClassesHelp = QtGui.QPushButton()
        self.buttonPURReferenceClassesHelp.setIcon(icon)
        self.layoutButtonBox.addWidget(self.buttonBox)
        self.layoutButtonBox.addWidget(self.buttonPURReferenceClassesHelp)
        
        self.layoutGroupBoxEditReferenceClasses.addLayout(self.layoutEditReferenceClassesInfo)
        self.layoutGroupBoxEditReferenceClasses.addWidget(self.contentButtonEditReferenceClasses)
        self.layoutGroupBoxEditReferenceClasses.addWidget(self.scrollEditReferenceClasses)
        self.dialogLayout.addLayout(self.layoutButtonBox)
        
        self.layoutTableReferenceClasses = QtGui.QVBoxLayout()
        self.layoutTableReferenceClasses.setAlignment(QtCore.Qt.AlignTop)
        self.layoutContentGroupBoxEditReferenceClasses.addLayout(self.layoutTableReferenceClasses)
        
        self.setLayout(self.dialogLayout)
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(400, 300)
        self.resize(parent.sizeHint())
    
    
    def getReferenceClasses(self):
        """Method for returning the reference classes dict.
        """
        return self.referenceClasses
    
    
    def initReferenceClassesTable(self):
        """Method for loading the current PUR reference classes.
        """
        referenceClasses = self.main.referenceClasses
        
        if referenceClasses:
            for key, val in referenceClasses.iteritems():
                self.addRow(key, val)
    
    
    def showEvent(self, event):
        """Overload method that is called when the dialog widget is shown.
        
        Args:
            event (QShowEvent): the show widget event.
        """
        super(DialogLumensPURReferenceClasses, self).showEvent(event)
    
    
    def addRow(self, id=None, title=None):
        """Method for adding a reference class table row.
        
        id (str): a reference class ID.
        title (str): a reference class title.
        """
        self.tableRowCount = self.tableRowCount + 1
        
        layoutRow = QtGui.QHBoxLayout()
        
        buttonDeleteReferenceClass = QtGui.QPushButton()
        icon = QtGui.QIcon(':/ui/icons/iconActionClear.png')
        buttonDeleteReferenceClass.setIcon(icon)
        buttonDeleteReferenceClass.setObjectName('buttonDeleteReferenceClass_{0}'.format(str(self.tableRowCount)))
        layoutRow.addWidget(buttonDeleteReferenceClass)
        
        lineEditReferenceClassID = QtGui.QLineEdit()
        lineEditReferenceClassID.setObjectName('lineEditReferenceClassID_{0}'.format(str(self.tableRowCount)))
        lineEditReferenceClassID.setText(str(self.tableRowCount))
        layoutRow.addWidget(lineEditReferenceClassID)
        
        lineEditReferenceClassTitle = QtGui.QLineEdit()
        lineEditReferenceClassTitle.setText('title')
        lineEditReferenceClassTitle.setObjectName('lineEditReferenceClassTitle_{0}'.format(str(self.tableRowCount)))
        layoutRow.addWidget(lineEditReferenceClassTitle)
        
        if id:
            lineEditReferenceClassID.setText(str(id))
        if title:
            lineEditReferenceClassTitle.setText(str(title))
        
        self.layoutTableReferenceClasses.addLayout(layoutRow)
        
        buttonDeleteReferenceClass.clicked.connect(self.handlerDeleteReferenceClass)
    
    
    def clearLayout(self, layout):
        """Method for removing a layout and all its child widgets.
        
        Args:
            layout (QLayout): the layout to be removed.
        """
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)

            if isinstance(item, QtGui.QWidgetItem):
                item.widget().deleteLater() # use this to properly delete the widget
            elif isinstance(item, QtGui.QSpacerItem):
                pass
            else:
                self.clearLayout(item.layout())
            
            layout.removeItem(item)
    

    def handlerPURReferenceClassesHelp(self):
        """Slot method for opening the dialog html help document.
        """
        filePath = os.path.join(self.main.appSettings['appDir'], self.main.appSettings['folderHelp'], self.main.appSettings['helpDialogPURReferenceClassesFile'])
        
        if os.path.exists(filePath):
            dialog = DialogLumensViewer(self, 'LUMENS Help - {0}'.format('PUR Reference Classes'), 'html', filePath)
            dialog.exec_()
        else:
            QtGui.QMessageBox.critical(self, 'LUMENS Help Not Found', "Unable to open '{0}'.".format(filePath))        

    
    def handlerButtonAddRow(self):
        """Slot method for adding a reference class to the reference class table.
        """
        self.addRow()
    
    
    def handlerDeleteReferenceClass(self):
        """Slot method for deleting a reference class from the reference class table.
        """
        buttonSender = self.sender()
        objectName = buttonSender.objectName()
        tableRow = objectName.split('_')[1]
        layoutRow = self.layoutTableReferenceClasses.itemAt(int(tableRow) - 1).layout()
        self.clearLayout(layoutRow)
    
    
    def handlerButtonSave(self):
        """Slot method when accepting the dialog and saving the reference classes.
        """
        self.referenceClasses = {}
        
        for tableRow in range(1, self.tableRowCount + 1):
            lineEditReferenceClassID = self.findChild(QtGui.QLineEdit, 'lineEditReferenceClassID_' + str(tableRow))
            
            if not lineEditReferenceClassID: # Row has been deleted
                print 'DEBUG: skipping a deleted row.'
                continue
            
            lineEditReferenceClassTitle = self.findChild(QtGui.QLineEdit, 'lineEditReferenceClassTitle_' + str(tableRow))
            
            # Check for duplicate reference class IDs and empty titles
            try:
                referenceClassID = int(unicode(lineEditReferenceClassID.text()))
                referenceClassTitle = unicode(lineEditReferenceClassTitle.text())
                
                if self.referenceClasses.has_key(referenceClassID):
                    print 'DEBUG ERROR found duplicate reference class ID.'
                    QtGui.QMessageBox.critical(self, 'Duplicate Reference Class ID', 'Please make sure there are no duplicate reference class IDs.')
                    return
                
                if not referenceClassTitle:
                    print 'DEBUG ERROR reference class title cannot be empty.'
                    QtGui.QMessageBox.critical(self, 'Empty Reference Class Title', 'Please make sure there are no empty reference class titles.')
                    return
                
                self.referenceClasses[referenceClassID] = referenceClassTitle
            except ValueError as verr:
                print 'DEBUG: ERROR reference class ID must be an integer!'
                QtGui.QMessageBox.critical(self, 'Non-number Reference Class ID', 'Please make sure that reference class IDs are numbers.')
                return
        
        if self.referenceClasses:
            self.close()
            self.setResult(QtGui.QDialog.Accepted)
        else:
            print 'DEBUG: ERROR no reference classes have been set.'
            QtGui.QMessageBox.critical(self, 'No Reference Classes Found', 'Please input the reference classes.')
    
    
    def handlerButtonCancel(self):
        """Slot method when rejecting/closing the dialog.
        """
        self.close()
        self.setResult(QtGui.QDialog.Rejected)
    
