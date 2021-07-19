from event_matching.versions.bgm import util


def apply(log, starts, ends, parameters):
    """
    Match two events with 1-1 relation using LP

    :param log:
        Event log
    :param starts:
        Sets of selected attributes as the sources of measurement
    :param ends:
        Sets of selected activities as the sinks of measurement
    :param parameters:
        universal parameters for event matching
    :return matching:
        [{case: {edge: measurement}}]
    """

    measurements = dict()
    for trace in log:
        graph = util.trace2graph.convert_trace_to_graph(trace, starts, ends, parameters)
        if len(graph.edges) >= 1:
            edges = util.lp_matching.get_matching_edges(graph, parameters)
            measurements[graph.graph['c_name']] = {edge: graph[edge[0]][edge[1]]['perf'] for edge in edges}
    return measurements

