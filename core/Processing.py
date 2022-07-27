# -*- coding: utf-8 -*-

import os
import traceback

from qgis.PyQt.QtCore import QCoreApplication

from qgis.core import (QgsMessageLog,
                       QgsApplication,
                       QgsMapLayer,
                       QgsProcessingProvider,
                       QgsProcessingAlgorithm,
                       QgsProcessingException,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingOutputRasterLayer,
                       QgsProcessingOutputMapLayer,
                       QgsProcessingOutputMultipleLayers,
                       QgsProcessingFeedback,
                       QgsRuntimeProfiler)

from core.ProcessingConfig import ProcessingConfig
from core.AlgorithmExecutor import execute

from tools import dataobjects


from processing_r.processing.provider import RAlgorithmProvider


class Processing(object):
    BASIC_PROVIDERS = []

    @staticmethod
    def activateProvider(providerOrName, activate=True):
        provider_id = providerOrName.id() if isinstance(providerOrName, QgsProcessingProvider) else providerOrName
        provider = QgsApplication.processingRegistry().providerById(provider_id)
        try:
            provider.setActive(True)
            provider.refreshAlgorithms()
        except:
            # provider could not be activated
            QgsMessageLog.logMessage(Processing.tr('Error: Provider {0} could not be activated\n').format(provider_id),
                                     Processing.tr("Processing"))

    @staticmethod
    def initialize():
        if "model" in [p.id() for p in QgsApplication.processingRegistry().providers()]:
            return

        with QgsRuntimeProfiler.profile('Initialize'):
            # Add the basic providers
            for c in [
                RAlgorithmProvider
            ]:
                p = c()
                if QgsApplication.processingRegistry().addProvider(p):
                    Processing.BASIC_PROVIDERS.append(p)
            # And initialize
            ProcessingConfig.initialize()
            ProcessingConfig.readSettings()
            # RenderingStyles.loadStyles()

    @staticmethod
    def deinitialize():
        for p in Processing.BASIC_PROVIDERS:
            QgsApplication.processingRegistry().removeProvider(p)

        Processing.BASIC_PROVIDERS = []

    @staticmethod
    def runAlgorithm(algOrName, parameters, onFinish=None, feedback=None, context=None):
        if isinstance(algOrName, QgsProcessingAlgorithm):
            alg = algOrName
        else:
            alg = QgsApplication.processingRegistry().createAlgorithmById(algOrName)

        if feedback is None:
            feedback = QgsProcessingFeedback()

        if alg is None:
            msg = Processing.tr('Error: Algorithm {0} not found\n').format(algOrName)
            feedback.reportError(msg)
            raise QgsProcessingException(msg)

        if context is None:
            context = dataobjects.createContext(feedback)

        if context.feedback() is None:
            context.setFeedback(feedback)

        ok, msg = alg.checkParameterValues(parameters, context)
        if not ok:
            msg = Processing.tr('Unable to execute algorithm\n{0}').format(msg)
            feedback.reportError(msg)
            raise QgsProcessingException(msg)

        if not alg.validateInputCrs(parameters, context):
            feedback.pushInfo(
                Processing.tr('Warning: Not all input layers use the same CRS.\nThis can cause unexpected results.'))

        ret, results = execute(alg, parameters, context, feedback, catch_exceptions=False)
        if ret:
            feedback.pushInfo(
                Processing.tr('Results: {}').format(results))

            if onFinish is not None:
                onFinish(alg, context, feedback)
            else:
                # auto convert layer references in results to map layers
                for out in alg.outputDefinitions():
                    if out.name() not in results:
                        continue

                    if isinstance(out, (QgsProcessingOutputVectorLayer, QgsProcessingOutputRasterLayer, QgsProcessingOutputMapLayer)):
                        result = results[out.name()]
                        if not isinstance(result, QgsMapLayer):
                            layer = context.takeResultLayer(result)  # transfer layer ownership out of context
                            if layer:
                                results[out.name()] = layer  # replace layer string ref with actual layer (+ownership)
                    elif isinstance(out, QgsProcessingOutputMultipleLayers):
                        result = results[out.name()]
                        if result:
                            layers_result = []
                            for l in result:
                                if not isinstance(result, QgsMapLayer):
                                    layer = context.takeResultLayer(l)  # transfer layer ownership out of context
                                    if layer:
                                        layers_result.append(layer)
                                    else:
                                        layers_result.append(l)
                                else:
                                    layers_result.append(l)

                            results[
                                out.name()] = layers_result  # replace layers strings ref with actual layers (+ownership)

        else:
            msg = Processing.tr("There were errors executing the algorithm.")
            feedback.reportError(msg)
            raise QgsProcessingException(msg)

        # if isinstance(feedback, MessageBarProgress):
        #     feedback.close()
        return results

    @staticmethod
    def tr(string, context=''):
        if context == '':
            context = 'Processing'
        return QCoreApplication.translate(context, string)
