#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, logging, datetime
from qgis.core import *
from PyQt4 import QtCore, QtGui

from dialog_lumens_base import DialogLumensBase

"""LUMENS "SCIENDO" module dialog Create DINAMICA Raster Cube using egoml,
   an xml type format, which is used as a single project in DINAMICA EGO software
    BEGIN_TAG
      script
          ~ property
          
          ~ functor = SaveMap
          ~ functor = LoadMap_1
          ~ functor = LoadMap_2
          .
          .
          ~ functor = LoadMap_n
          
          ~ containerfunctor= CreateCubeMap
      script
    END_TAG
"""
class DialogLumensSciendoDinamica(QtGui.QDialog, DialogLumensBase):
    # bikin displaynya dulu
    # gimana cara retrieve path setelah milih factor untuk jadi salah satu input di egoml
    def __init__(self, parent):
        super(DialogLumensSciendoDinamica, self).__init__(parent)
        
    
  
    # 0. how to parse an xml and pass its property value and display it to user interface
    
    # 1. how to modify
    
    # 2. how to add new functors


"""
IF XML_IS_EXIST
    MODIFY_XML
THEN
    CREATE_NEW_XML
"""
