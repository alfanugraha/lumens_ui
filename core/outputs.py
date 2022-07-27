# -*- coding: utf-8 -*-

import sys

from qgis.core import (QgsProcessingOutputRasterLayer,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingOutputMapLayer,
                       QgsProcessingOutputHtml,
                       QgsProcessingOutputNumber,
                       QgsProcessingOutputString,
                       QgsProcessingOutputBoolean,
                       QgsProcessingOutputFolder,
                       QgsProcessingOutputMultipleLayers)


def getOutputFromString(s):
    try:
        if "|" in s and s.startswith("Output"):
            tokens = s.split("|")
            params = [t if str(t) != "None" else None for t in tokens[1:]]
            clazz = getattr(sys.modules[__name__], tokens[0])
            return clazz(*params)
        else:
            tokens = s.split("=")
            if not tokens[1].lower()[:len('output')] == 'output':
                return None

            name = tokens[0]
            description = tokens[0]

            token = tokens[1].strip()[len('output') + 1:]
            out = None

            if token.lower().strip().startswith('outputraster'):
                out = QgsProcessingOutputRasterLayer(name, description)
            elif token.lower().strip() == 'outputvector':
                out = QgsProcessingOutputVectorLayer(name, description)
            elif token.lower().strip() == 'outputlayer':
                out = QgsProcessingOutputMapLayer(name, description)
            elif token.lower().strip() == 'outputmultilayers':
                out = QgsProcessingOutputMultipleLayers(name, description)
            #            elif token.lower().strip() == 'vector point':
            #                out = OutputVector(datatype=[dataobjects.TYPE_VECTOR_POINT])
            #            elif token.lower().strip() == 'vector line':
            #                out = OutputVector(datatype=[OutputVector.TYPE_VECTOR_LINE])
            #            elif token.lower().strip() == 'vector polygon':
            #                out = OutputVector(datatype=[OutputVector.TYPE_VECTOR_POLYGON])
            #            elif token.lower().strip().startswith('table'):
            #                out = OutputTable()
            elif token.lower().strip().startswith('outputhtml'):
                out = QgsProcessingOutputHtml(name, description)
            #            elif token.lower().strip().startswith('file'):
            #                out = OutputFile()
            #                ext = token.strip()[len('file') + 1:]
            #                if ext:
            #                    out.ext = ext
            elif token.lower().strip().startswith('outputfolder'):
                out = QgsProcessingOutputFolder(name, description)
            elif token.lower().strip().startswith('outputnumber'):
                out = QgsProcessingOutputNumber(name, description)
            elif token.lower().strip().startswith('outputstring'):
                out = QgsProcessingOutputString(name, description)
            elif token.lower().strip().startswith('outputboolean'):
                out = QgsProcessingOutputBoolean(name, description)
            #            elif token.lower().strip().startswith('extent'):
            #                out = OutputExtent()

            return out
    except:
        return None
