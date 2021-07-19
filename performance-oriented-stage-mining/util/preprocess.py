from pm4py.algo.filtering.log.attributes import attributes_filter
from pm4py.util import constants
from util import constants as performance_constants


def index_events(log, parameters):
    if not parameters[performance_constants.IF_INDEXED]:
        for case in log:
            for event_index, event in enumerate(case, 1):
                event[performance_constants.EVENT_INDEX] = event_index


def filter_cases(log, starts, ends, parameters):
    for classifier_attributes in [starts, ends]:
        log = attributes_filter.apply(log, classifier_attributes,
                                      parameters={constants.PARAMETER_CONSTANT_ATTRIBUTE_KEY: parameters[performance_constants.EVENT_CLASSIFIER],
                                                  'positive': True})
    return log


def filter_events(log, starts, ends, parameters):
    log_classifier = attributes_filter.apply_events(log, starts + ends,
                                                    parameters={constants.PARAMETER_CONSTANT_ATTRIBUTE_KEY: parameters[
                                                        performance_constants.EVENT_CLASSIFIER],
                                                                'positive': True})
    return log_classifier


def filter_and_trim_cases(log, starts, ends, parameters=None):
    log_filtered = filter_cases(log, starts, ends, parameters)
    log_trimmed = filter_events(log_filtered, starts, ends, parameters)
    return log_trimmed


def get_endpoints(log, parameters, starts=None, ends=None):
    if starts is None:
        starts = list(set([case[0][parameters[performance_constants.EVENT_CLASSIFIER]] for case in log]))
    if ends is None:
        ends = list(set([case[-1][parameters[performance_constants.EVENT_CLASSIFIER]] for case in log]))
    return starts, ends