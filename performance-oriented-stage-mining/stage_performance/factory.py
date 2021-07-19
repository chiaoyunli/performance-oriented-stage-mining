from pm4py.objects.log.util.xes import DEFAULT_TIMESTAMP_KEY
from pm4py.objects.log.util.xes import DEFAULT_NAME_KEY
from stage_performance import versions
from util import constants as performance_constants
from util import preprocess as preprocessor


STAGE_VERSION_CLASSIC = 'classic'
VERSIONS = {STAGE_VERSION_CLASSIC: versions.classic.apply}


def apply(log, stages=None, parameters=None, variant=STAGE_VERSION_CLASSIC):

    if parameters is None:
        parameters = {}

    parameters[performance_constants.EVENT_CLASSIFIER] = parameters[performance_constants.EVENT_CLASSIFIER] \
        if performance_constants.EVENT_CLASSIFIER in parameters else DEFAULT_NAME_KEY
    parameters[performance_constants.EVENT_PERFORMANCE_ATTRIBUTE] = parameters[performance_constants.EVENT_PERFORMANCE_ATTRIBUTE] \
        if performance_constants.EVENT_PERFORMANCE_ATTRIBUTE in parameters else DEFAULT_TIMESTAMP_KEY
    parameters[performance_constants.EVENT_INDEX] = parameters[performance_constants.EVENT_INDEX] \
        if performance_constants.EVENT_INDEX in parameters else performance_constants.EVENT_INDEX

    stages_definition = define_stages(log, stages, parameters)

    stage_performance = VERSIONS[variant](log, stages_definition, parameters=parameters)
    performance_per_stage_variant = get_stage_variant(stage_performance)

    return performance_per_stage_variant


def define_stages(log, stages, parameters):

    if stages is None:
        starts, ends = preprocessor.get_endpoints(log, parameters)
        stages = {'process': {'starts': starts, 'ends': ends, 'matching_param': dict()}}
    else:
        for stage_key, stage_definition in stages.items():
            stage_definition['matching_param'] = stage_definition['matching_param'] \
                if 'matching_param' in stage_definition else dict()
    return stages


def get_stage_variant(performance_per_case):
    stage_variant_cases = dict()
    stage_variant_ref = dict()
    for case, stages in performance_per_case.items():
        stage_keys = {key for key in stages.keys() if '/' not in key}
        if stage_keys not in stage_variant_ref.values():
            stage_variant_ref[len(stage_variant_ref) + 1] = stage_keys
            stage_variant_cases[len(stage_variant_ref)] = []
        for variant_key, variant in stage_variant_ref.items():
            if stage_keys == variant:
                stage_variant_cases[variant_key].append(case)
    return get_cases_by_stage_variant(performance_per_case, stage_variant_ref, stage_variant_cases)


def get_cases_by_stage_variant(performance_per_case, stage_variant_ref, stage_variant_cases):
    variant_performance = []
    for stage_ref, cases in stage_variant_cases.items():
        variant_performance.append({'stage_variant': stage_variant_ref[stage_ref],
                                    'cases_performance': {key: value for key, value in performance_per_case.items() if key in cases}})
    return variant_performance

