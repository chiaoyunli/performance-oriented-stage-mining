from pm4py import util as pmutil
from pm4py.objects.log.util import xes as xes_util
from pm4py.objects.log.util.xes import DEFAULT_NAME_KEY
from pm4py.objects.log.util.xes import DEFAULT_TIMESTAMP_KEY
from util import constants as performance_constants
from util import preprocess as preprocessor
from event_matching.versions.bgm import bgm
import os


MATCHING_VERSION_BGM = 'bgm'

VERSIONS = {MATCHING_VERSION_BGM: bgm.apply}

DEFAULT_PARAMETERS = {pmutil.constants.PARAMETER_CONSTANT_ACTIVITY_KEY: xes_util.DEFAULT_NAME_KEY,
                      pmutil.constants.PARAMETER_CONSTANT_TIMESTAMP_KEY: xes_util.DEFAULT_TIMESTAMP_KEY}


def apply(log, starts=None, ends=None, parameters=None, variant=MATCHING_VERSION_BGM):

    if parameters is None:
        parameters = {}

    parameters[performance_constants.EVENT_PERFORMANCE_ATTRIBUTE] = parameters[performance_constants.EVENT_PERFORMANCE_ATTRIBUTE] \
        if performance_constants.EVENT_PERFORMANCE_ATTRIBUTE in parameters else DEFAULT_TIMESTAMP_KEY
    parameters[performance_constants.EVENT_CLASSIFIER] = parameters[performance_constants.EVENT_CLASSIFIER] \
        if performance_constants.EVENT_CLASSIFIER in parameters else DEFAULT_NAME_KEY
    parameters[performance_constants.IF_INDEXED] = parameters[performance_constants.IF_INDEXED] \
        if performance_constants.IF_INDEXED in parameters else False
    if variant == MATCHING_VERSION_BGM:  # attribute to compute distance, distance function, matching constraints on node
        parameters[performance_constants.DISTANCE_ATTR] = parameters[performance_constants.DISTANCE_ATTR] \
            if performance_constants.DISTANCE_ATTR in parameters else performance_constants.EVENT_INDEX
        parameters[performance_constants.MATCHING_DISTANCE_FUNC] = parameters[performance_constants.MATCHING_DISTANCE_FUNC] \
            if performance_constants.MATCHING_DISTANCE_FUNC in parameters else None
        parameters[performance_constants.MATCHING_NODE_CONSTRAINT] = parameters[performance_constants.MATCHING_NODE_CONSTRAINT] \
            if performance_constants.MATCHING_NODE_CONSTRAINT in parameters else '1:1'

    starts, ends = preprocessor.get_endpoints(log, parameters, starts, ends)

    preprocessor.index_events(log, parameters)
    log_filtered = preprocessor.filter_and_trim_cases(log, starts, ends, parameters=parameters)
    edge_measure_per_case = VERSIONS[variant](log_filtered, starts, ends, parameters=parameters)
    remove_files()
    return edge_measure_per_case


def remove_files():
    for file_name in os.listdir('.'):
        if '.mps' in file_name:
            os.remove(file_name)

