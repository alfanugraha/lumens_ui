# -*- coding: utf-8 -*-


from qgis.PyQt.QtCore import QObject, pyqtSignal


class ProcessingResults(QObject):
    resultAdded = pyqtSignal()

    results = []

    def addResult(self, icon, name, timestamp, result):
        self.results.append(Result(icon, name, timestamp, result))
        self.resultAdded.emit()

    def getResults(self):
        return self.results


class Result:

    def __init__(self, icon, name, timestamp, filename):
        self.icon = icon
        self.name = name
        self.timestamp = timestamp
        self.filename = filename


resultsList = ProcessingResults()
