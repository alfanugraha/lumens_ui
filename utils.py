#!/usr/bin/env python
#-*- coding:utf-8 -*-

import logging
from PyQt5 import QtGui, QtWidgets


def is_number(s):
    try:
        n=str(float(s))
        if n == 'nan' or n == 'inf' or n == '-inf':
            return False
    except ValueError:
        try:
            complex(s)
        except ValueError:
            return False
    return True


class QPlainTextEditLogger(logging.Handler):
    """A custom text widget that receives the logging output.
    """
    
    def __init__(self, parent):
        super(QPlainTextEditLogger, self).__init__()
        
        self.widget = QtWidgets.QPlainTextEdit(parent)
        self.widget.setReadOnly(True)
    
    
    def emit(self, record):
        msg = self.format(record)
        try:
            self.widget.appendPlainText(msg)
        except:
            pass
    
    
    def write(self, m):
        pass


#############################################################################


class DetailedMessageBox(QtWidgets.QMessageBox):
    """A custom detail info message box where the show detail button is already clicked.
    """
    
    def __init__(self, *args, **kwargs):            
        super(DetailedMessageBox, self).__init__(*args, **kwargs)
    
    
    def showEvent(self, event):
        """Overload method that is called when the widget is shown.
        
        Args:
            event (QShowEvent): the show widget event.
        """
        super(DetailedMessageBox, self).showEvent(event)
        
        # Show details immediately on messagebox open
        for button in self.buttons():
            if button.text() == 'Show Details...':
                button.click()
    
    
    def resizeEvent(self, event):
        """Overload method that is called when the widget is resized.
        
        Args:
            event (QResizeEvent): the resize widget event.
        """
        result = super(DetailedMessageBox, self).resizeEvent(event)

        details_box = self.findChild(QtGui.QTextEdit)
        
        if details_box is not None:
            details_box.setFixedSize(details_box.sizeHint())

        return result
    
