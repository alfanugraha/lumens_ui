# -*- coding: utf-8 -*-


from qgis.core import (QgsApplication,
                       QgsProcessingParameterEnum)
from core.Processing import Processing


def algorithmHelp(id):
    """
    Prints algorithm parameters with their types. Also
    provides information about parameters and outputs,
    and their acceptable values.

    :param id: An algorithm's ID
    :type id: str
    """
    alg = QgsApplication.processingRegistry().algorithmById(id)
    if alg is not None:
        print('{} ({})\n'.format(alg.displayName(), alg.id()))
        if alg.shortDescription():
            print(alg.shortDescription() + '\n')
        if alg.shortHelpString():
            print(alg.shortHelpString() + '\n')
        print('\n----------------')
        print('Input parameters')
        print('----------------')
        for p in alg.parameterDefinitions():
            print('\n{}: {}'.format(p.name(), p.description()))
            if p.help():
                print('\n\t{}'.format(p.help()))

            print('\n\tParameter type:\t{}'.format(p.__class__.__name__))

            if isinstance(p, QgsProcessingParameterEnum):
                opts = []
                for i, o in enumerate(p.options()):
                    opts.append('\t\t- {}: {}'.format(i, o))
                print('\n\tAvailable values:\n{}'.format('\n'.join(opts)))

            parameter_type = QgsApplication.processingRegistry().parameterType(p.type())
            accepted_types = parameter_type.acceptedPythonTypes() if parameter_type is not None else []
            if accepted_types:
                opts = []
                for t in accepted_types:
                    opts.append('\t\t- {}'.format(t))
                print('\n\tAccepted data types:')
                print('\n'.join(opts))

        print('\n----------------')
        print('Outputs')
        print('----------------')

        for o in alg.outputDefinitions():
            print('\n{}:  <{}>'.format(o.name(), o.__class__.__name__))
            if o.description():
                print('\t' + o.description())

    else:
        print('Algorithm "{}" not found.'.format(id))


def run(algOrName, parameters, onFinish=None, feedback=None, context=None, is_child_algorithm=False):
    """
    Executes given algorithm and returns its outputs as dictionary object.

    :param algOrName: Either an instance of an algorithm, or an algorithm's ID
    :param parameters: Algorithm parameters dictionary
    :param onFinish: optional function to run after the algorithm has completed
    :param feedback: Processing feedback object
    :param context: Processing context object
    :param is_child_algorithm: Set to True if this algorithm is being run as part of a larger algorithm,
    i.e. it is a sub-part of an algorithm which calls other Processing algorithms.

    :returns algorithm results as a dictionary, or None if execution failed
    :rtype: Union[dict, None]
    """
    if onFinish or not is_child_algorithm:
        return Processing.runAlgorithm(algOrName, parameters, onFinish, feedback, context)
    else:
        # for child algorithms, we disable to default post-processing step where layer ownership
        # is transferred from the context to the caller. In this case, we NEED the ownership to remain
        # with the context, so that further steps in the algorithm have guaranteed access to the layer.
        def post_process(_alg, _context, _feedback):
            return

        return Processing.runAlgorithm(algOrName, parameters, onFinish=post_process, feedback=feedback, context=context)

