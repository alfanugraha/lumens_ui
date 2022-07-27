# -*- coding: utf-8 -*-

import os
import time
import sys
import uuid
import math

from qgis.PyQt.QtCore import QDir
from qgis.core import (QgsApplication,
                       QgsProcessingUtils)

numExported = 1


def userFolder():
    userDir = os.path.join(QgsApplication.qgisSettingsDirPath(), 'processing')
    if not QDir(userDir).exists():
        QDir().mkpath(userDir)

    return str(QDir.toNativeSeparators(userDir))


def defaultOutputFolder():
    folder = os.path.join(userFolder(), 'outputs')
    if not QDir(folder).exists():
        QDir().mkpath(folder)

    return str(QDir.toNativeSeparators(folder))


def isWindows():
    return os.name == 'nt'


def isMac():
    return sys.platform == 'darwin'


def getTempFilename(ext=None):
    tmpPath = QgsProcessingUtils.tempFolder()
    t = time.time()
    m = math.floor(t)
    uid = '{:8x}{:05x}'.format(m, int((t - m) * 1000000))
    if ext is None:
        filename = os.path.join(tmpPath, '{}{}'.format(uid, getNumExportedLayers()))
    else:
        filename = os.path.join(tmpPath, '{}{}.{}'.format(uid, getNumExportedLayers(), ext))
    return filename


def getTempDirInTempFolder():
    """Returns a temporary directory, putting it into a temp folder.
    """

    path = QgsProcessingUtils.tempFolder()
    path = os.path.join(path, uuid.uuid4().hex)
    mkdir(path)
    return path


def removeInvalidChars(string):
    validChars = \
        'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789:.'
    string = ''.join(c for c in string if c in validChars)
    return string


def getNumExportedLayers():
    global numExported
    numExported += 1
    return numExported


def mkdir(newdir):
    newdir = newdir.strip('\n\r ')
    if os.path.isdir(newdir):
        pass
    else:
        (head, tail) = os.path.split(newdir)
        if head and not os.path.isdir(head):
            mkdir(head)
        if tail:
            os.mkdir(newdir)


def tempHelpFolder():
    tmp = os.path.join(str(QDir.tempPath()), 'processing_help')
    if not QDir(tmp).exists():
        QDir().mkpath(tmp)

    return str(os.path.abspath(tmp))