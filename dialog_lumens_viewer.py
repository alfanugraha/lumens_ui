#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, tempfile, csv
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebKitWidgets import QWebView

from menu_factory import MenuFactory

class DialogLumensViewer(QDialog):
    """LUMENS dialog class for displaying csv, html, and text content.
    """
    
    def __init__(self, parent, contentTitle, contentType, contentSource, editableTable=False, contentMessage=''):
        """Constructor method for initializing a LUMENS viewer dialog window instance.
        
        Args:
            parent: the dialog's parent instance.
            contentTitle (str): the title of the dialog window.
            contentType (str): the type of the content.
            contentSource (str): a file path to the content file.
            editableTable (bool): if true allow the table content of the csv to be editable.
            contentMessage (str): message to be shown on top of the content.
        """
        super(DialogLumensViewer, self).__init__(parent)
        self.main = parent
        self.dialogTitle = 'LUMENS ' + MenuFactory.getLabel(MenuFactory.APP_LUMENS_VIEWER) + ' - ' + contentTitle
        
        self.contentType = contentType
        self.contentSource = contentSource
        self.editableTable = editableTable
        self.contentMessage = contentMessage
        
        self.setupUi(self)
        
        self.loadContent()
    
    
    def setupUi(self, parent):
        """Method for building the dialog UI.
        
        Args:
            parent: the dialog's parent instance.
        """
        self.dialogLayout = QVBoxLayout()
        
        self.setLayout(self.dialogLayout)
        
        self.setWindowTitle(self.dialogTitle)
        self.setMinimumSize(600, 600)
        self.resize(parent.sizeHint())
    
    
    def getTableData(self):
        """Method for returning the table data as list of lists.
        """
        tableData = []
        
        # Loop rows
        for tableRow in range(self.tableModel.rowCount()):
            dataRow = []
            
            # Loop row columns
            for tableColumn in range(self.tableModel.columnCount()):
                item = self.tableModel.item(tableRow, tableColumn)
                dataRow.append(item.text())
            
            tableData.append(dataRow)
        
        return tableData
    
    
    def getTableCsv(self, tableData, forwardDirSeparator=False):
        """Method for writing the table data to a temp csv file.
        
        Args:
            tableData (list of lists): list of table rows.
            forwardDirSeparator (bool): return the temp csv file path with forward slash dir separator.
        """
        handle, csvFilePath = tempfile.mkstemp(suffix='.csv')
        
        with os.fdopen(handle, 'w') as f:
            writer = csv.writer(f)
            for dataRow in tableData:
                writer.writerow(dataRow)
        
        if forwardDirSeparator:
            return csvFilePath.replace(os.path.sep, '/')
        
        return csvFilePath
    
    
    def closeEvent(self, event):
        """Overload method that is called when the dialog widget is closed.
        
        Args:
            event (QCloseEvent): the close widget event.
        """
        super(DialogLumensViewer, self).closeEvent(event)
        
        # Set result code
        self.done(1)
        
        event.accept()
    
    
    def loadContent(self):
        """Method for loading the source content in the appropriate widget.
        
        The supported contents are csv, html, and text files. Content from csv files
        can be showned in an editable table widget.
        """
        if len(self.contentMessage):
            self.labelContentMessage = QLabel()
            self.labelContentMessage.setText(self.contentMessage)
            self.dialogLayout.addWidget(self.labelContentMessage)
        
        if self.contentType == 'csv':
            self.tableModel = QStandardItemModel()
        
            self.tableContent = QTableView()
            self.tableContent.setModel(self.tableModel)
            
            # Disable table editing
            if not self.editableTable:
                self.tableContent.setSelectionMode(QAbstractItemView.NoSelection)
                self.tableContent.setEditTriggers(QAbstractItemView.NoEditTriggers)
            
            self.tableContent.verticalHeader().setVisible(False)
            self.tableContent.horizontalHeader().setResizeMode(QHeaderView.Interactive)
            
            self.dialogLayout.addWidget(self.tableContent)
            
            with open(self.contentSource, 'rb') as csvFile:
                for row in csv.reader(csvFile):
                    items = [QStandardItem(field) for field in row]
                    self.tableContent.model().appendRow(items)
            
            self.tableContent.horizontalHeader().resizeSections()
        elif self.contentType == 'html':
            self.webContent = QWebView()
            self.dialogLayout.addWidget(self.webContent)
            
            self.webContent.load(QUrl.fromLocalFile(self.contentSource))
            self.setMinimumSize(800, 600)
        elif self.contentType == 'text':
            self.textContent = QPlainTextEdit()
            self.textContent.setReadOnly(True)
            
            self.dialogLayout.addWidget(self.textContent)
            
            with open(self.contentSource) as file:
                text = file.read()
                self.textContent.setPlainText(text)
    
