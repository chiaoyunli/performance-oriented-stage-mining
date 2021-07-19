from pm4py.objects.log.util.xes import DEFAULT_NAME_KEY
from util import constants as performance_constants
from event_matching import factory as event_matching_factory


def apply(log, stages_definition, parameters):
    stage_cycle_pa_with_edge = get_stage_cycle_pa_with_edge(log, stages_definition, parameters)
    endpoints_pa = get_endpoints_pa(log, stages_definition, parameters)
    stage_performance = combine_flow_and_cycle_time(stage_cycle_pa_with_edge, endpoints_pa)
    set_flow_pa(stage_performance)
    set_betweenstage_pa(stage_performance)
    return stage_performance


def get_stage_cycle_pa_with_edge(log, stages_definition, parameters):
    stage_cycle_pa_with_edge = dict()
    for stage_key, stage_def in stages_definition.items():
        stage_def['matching_param'].update(parameters)
        matching_result = event_matching_factory.apply(log, stage_def['starts'], stage_def['ends'], stage_def['matching_param'])
        for case, cm_with_edge in matching_result.items():
            stage_cycle_pa_with_edge[case] = dict() if case not in stage_cycle_pa_with_edge.keys() \
                else stage_cycle_pa_with_edge[case]
            stage_cycle_pa_with_edge[case][stage_key] = dict() if stage_key not in stage_cycle_pa_with_edge[case].keys()\
                else stage_cycle_pa_with_edge[case][stage_key]
            stage_cycle_pa_with_edge[case][stage_key]['cm_with_edge'] = cm_with_edge
    return stage_cycle_pa_with_edge


def get_endpoints_pa(log, stages_definition, parameters):
    performance_attr = parameters[performance_constants.EVENT_PERFORMANCE_ATTRIBUTE]
    event_classifier = parameters[performance_constants.EVENT_CLASSIFIER]
    endpoint_pa = dict()
    for stage_key, stage_def in stages_definition.items():
        for case in log:
            startevent_pa = sorted([event[performance_attr] for event in case if
                            event[event_classifier] in stage_def['starts']])
            endevent_pa = sorted([event[performance_attr] for event in case if
                           event[event_classifier] in stage_def['ends']])
            if len(startevent_pa) > 0 and len(endevent_pa) > 0: #and startevent_pa[0] < endevent_pa[0]:
                if case.attributes[DEFAULT_NAME_KEY] not in endpoint_pa:
                    endpoint_pa[case.attributes[DEFAULT_NAME_KEY]] = dict()
                endpoint_pa[case.attributes[DEFAULT_NAME_KEY]][stage_key] = {'firststartevent_pa': startevent_pa[0],
                                                                             'laststartevent_pa': startevent_pa[-1],
                                                                             'firstendevent_pa': endevent_pa[0],
                                                                             'lastendevent_pa': endevent_pa[-1]}
    return endpoint_pa


def combine_flow_and_cycle_time(stage_cycle_pa_with_edge, endpoints_pa):
    for case, stages_perfs in stage_cycle_pa_with_edge.items():
        for stage_key, stage_perf in stages_perfs.items():
            stages_perfs[stage_key].update(endpoints_pa[case][stage_key])
    return stage_cycle_pa_with_edge


def set_flow_pa(stage_performance):
    for case, stages_endpoints_pa in stage_performance.items():
        for stage_key, endpoints in stages_endpoints_pa.items():
            endpoints['ft'] = endpoints['lastendevent_pa'] - endpoints['firststartevent_pa']


def set_betweenstage_pa(stage_performance):
    for case, stage_endpoints in stage_performance.items():
        stages = list(stage_endpoints.keys())
        if len(stages) >= 2:
            for i in range(len(stages) - 1):
                twostages = [stages[i], stages[i + 1]]
                betweenstage_key = '/'.join(twostages)
                stage_performance[case][betweenstage_key] = {'ff': stage_endpoints[twostages[1]]['firststartevent_pa'] -
                                                                   stage_endpoints[twostages[0]]['firststartevent_pa'],
                                                             'fl': stage_endpoints[twostages[1]]['lastendevent_pa'] -
                                                                   stage_endpoints[twostages[0]]['firststartevent_pa'],
                                                             'lf': stage_endpoints[twostages[1]]['firststartevent_pa'] -
                                                                   stage_endpoints[twostages[0]]['lastendevent_pa'],
                                                             'll': stage_endpoints[twostages[1]]['lastendevent_pa'] -
                                                                   stage_endpoints[twostages[0]]['lastendevent_pa']}


