#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, csv, tempfile
from PyQt4 import QtGui

from dialog_lumens_viewer import DialogLumensViewer

from menu_factory import MenuFactory

class DialogLumensBase:
    """Base class for LUMENS dialogs.
    """
    
    def __init__(self, parent):
        self.main = parent
    
    
    def populateAddedDataComboBox(self, addedData, comboBox):
        """Method for populating a combobox with data previously added to the project.
        """
        if len(addedData):
            comboBox.clear()
            
            # Sort by key name
            for key in sorted(addedData):
                comboBox.addItem(key, addedData[key])
            
            comboBox.setEnabled(True)


    def handlerPopulateNameFromLookupData(self, lookupData, comboBox):
        """Populate name or description from a spesific lookup table
        """
        if len(lookupData):
            comboBox.clear()
            for value in lookupData.values():
                comboBox.addItem(value[list(value)[0]]) # value.values()[0] <-- only support in python 2
            comboBox.setEnabled(True)
            
    
    def handlerDialogHelp(self, dialogName):
        """Slot method for opening the dialog html help document.
        
        Args:
            dialogName (str): the name of the dialog.
        """
        helpDialogFile = None
        
        if dialogName == 'PUR':
            helpDialogFile = 'helpDialogPURFile'
        elif dialogName == 'QUES':
            helpDialogFile = 'helpDialogQUESFile'
        elif dialogName == 'TA':
            helpDialogFile = 'helpDialogTAFile'
        elif dialogName == 'SCIENDO':
            helpDialogFile = 'helpDialogSCIENDOFile'
        elif dialogName == 'Layer Properties':
            helpDialogFile = 'helpDialogLayerPropertiesFile'
        elif dialogName == 'Create':
            helpDialogFile = 'helpDialogCreateFile'
        elif dialogName == 'PUR Reference Classes':
            helpDialogFile = 'helpDialogLayerPropertiesFile'
        else:
            helpDialogFile = 'helpLUMENSFile'
        
        filePath = os.path.join(self.main.appSettings['appDir'], self.main.appSettings['folderHelp'], self.main.appSettings[helpDialogFile])
        
        if os.path.exists(filePath):
            dialog = DialogLumensViewer(self, MenuFactory.getLabel(MenuFactory.APP_LUMENS_HELP) + ' - {0}'.format(dialogName), 'html', filePath)
            dialog.exec_()
        else:
            QtGui.QMessageBox.critical(self, MenuFactory.getLabel(MenuFactory.MSG_APP_HELP_NOT_FOUND), MenuFactory.getDescription(MenuFactory.MSG_APP_HELP_NOT_FOUND) + " '{0}'.".format(filePath))
    
    
    def validForm(self, formName=False):
        """Method for validating the form values.
        
        Args:
            formName (str): the name of the form to validate. If false then use the class name.
        """
        settingsIndex = type(self).__name__
        
        if formName:
            settingsIndex = formName
            logging.getLogger(type(self).__name__).info('form validate: %s', formName)
            logging.getLogger(type(self).__name__).info('form values: %s', self.main.appSettings[formName])
        else:
            logging.getLogger(type(self).__name__).info('form validate: %s', type(self).__name__)
            logging.getLogger(type(self).__name__).info('form values: %s', self.main.appSettings[type(self).__name__])
        
        valid = True
        
        for key, val in self.main.appSettings[settingsIndex].iteritems():
            if val == 0: # for values set specific to 0
                continue
            elif not val:
                valid = False
        
        if not valid:
            QtGui.QMessageBox.critical(self, MenuFactory.getLabel(MenuFactory.MSG_ERROR),  MenuFactory.getDescription(MenuFactory.MSG_ERROR))
        
        return valid
    
    
    def outputsMessageBox(self, algName, outputs, successMessage, errorMessage):
        """Display a messagebox based on the processing result.
        
        Args:
            algName (str): the name of the executed algorithm.
            outputs (dict): the output of the executed algorithm.
            successMessage (str): the success message to be display in a message box.
            errorMessage (str): the error message to be display in a message box.
        """
        success = False
        outputMessage = 'Algorithm "{0}"'.format(algName)
        
        # R script key
        statusOutputKey = 'statusoutput'
        
        # Modeler script key
        if algName.lower().startswith('modeler:'):
            statusOutputKey = 'statusoutput_ALG1'
            if statusOutputKey not in outputs:
                statusOutputKey = 'statusoutput_ALG0'
        
        if outputs and statusOutputKey in outputs:
            if os.path.exists(outputs[statusOutputKey]):
                with open(outputs[statusOutputKey], 'rb') as f:
                    hasHeader = csv.Sniffer().has_header(f.read(1024))
                    f.seek(0)
                    reader = csv.reader(f)
                    if hasHeader: # Skip the header
                        next(reader)
                    for row in reader: # Just read the first row
                        verb = 'failed'
                        statusCode = row[0]
                        successMessage = errorMessage = statusMessage = row[1] # a bit weird, still need to be simplified
                        if int(statusCode) == 1:
                            success = True
                            verb = 'succeeded'
                        outputMessage = '{0} {1} with status message: {2}'.format(outputMessage, verb, statusMessage)
                        break
            else:
                outputMessage = '{0} failed.'.format(outputMessage)
        
        if success:
            logging.getLogger(type(self).__name__).info(outputMessage)
            QtGui.QMessageBox.information(self, MenuFactory.getLabel(MenuFactory.MSG_APP_RESULT_SUCCESS), successMessage)
            return True
        
        logging.getLogger(type(self).__name__).error(outputMessage)
        QtGui.QMessageBox.critical(self, MenuFactory.getLabel(MenuFactory.MSG_APP_RESULT_ERROR), errorMessage)
        return False
    

    def writeListCsv(self, listOfData, forwardDirSeparator=False):
        """Method for writing the dissolved table to a temp csv file. Inspired from DialogLumensViewer.
        
        Args:
            listOfData (list): a list which is contained the list of checked QUES-C database 
            forwardDirSeparator (bool): return the temp csv file path with forward slash dir separator.
        """        
        handle, csvFilePath = tempfile.mkstemp(suffix='.csv')
        
        with os.fdopen(handle, 'w') as f:
            writer = csv.writer(f)
            
            for tableRow in listOfData:
                writer.writerow([tableRow])
            
        if forwardDirSeparator:
            return csvFilePath.replace(os.path.sep, '/')
            
        return csvFilePath
        
    
    @staticmethod
    def writeTableCsv(tableWidget, forwardDirSeparator=False):
        """Method for writing the table data to a temp csv file.
        
        Args:
            forwardDirSeparator (bool): return the temp csv file path with forward slash dir separator.
        """
        dataTable = []
        
        # Loop rows
        for tableRow in range(tableWidget.rowCount()):
            dataRow = []
            
            # Loop row columns
            for tableColumn in range(tableWidget.columnCount()):
                item = tableWidget.item(tableRow, tableColumn)
                widget = tableWidget.cellWidget(tableRow, tableColumn)
                
                # Check if cell is a combobox widget
                if widget and isinstance(widget, QtGui.QComboBox):
                    dataRow.append(widget.currentText())
                else:
                    itemText = item.text()
                    
                    if itemText:
                        dataRow.append(itemText)
                    else:
                        return '' # Cell is empty!
                
            dataTable.append(dataRow)
        
        if dataTable:
            handle, tableCsvFilePath = tempfile.mkstemp(suffix='.csv')
        
            with os.fdopen(handle, 'w') as f:
                writer = csv.writer(f)
                for dataRow in dataTable:
                    writer.writerow(dataRow)
            
            if forwardDirSeparator:
                return tableCsvFilePath.replace(os.path.sep, '/')
            
            return tableCsvFilePath
        
        # Table unused, or something wrong with the table
        return ''



