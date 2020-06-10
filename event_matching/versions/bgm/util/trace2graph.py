from pm4py.objects.log.util.xes import DEFAULT_NAME_KEY
import networkx as nx
from util import constants as performance_constants


def convert_trace_to_graph(trace, starts, ends, parameters):
    """
    Encode a trace to a graph by converting every event of interest to a node

    :return graph:
        Bipartite graph
    """
    graph = nx.DiGraph(c_name=trace.attributes[DEFAULT_NAME_KEY])
    add_nodes(graph, trace, starts, ends, parameters)
    add_edges(graph, parameters)

    return graph


def add_nodes(graph, trace, starts, ends, parameters):
    """
    Add a node to the graph per event for a trace
    """
    for event in trace:
        if parameters[performance_constants.DISTANCE_ATTR] in event:
            if event[parameters[performance_constants.EVENT_CLASSIFIER]] in starts:
                graph.add_node(event[performance_constants.EVENT_INDEX], name=event[parameters[performance_constants.EVENT_CLASSIFIER]],
                               ea=event[parameters[performance_constants.DISTANCE_ATTR]], epa=event[parameters[performance_constants.EVENT_PERFORMANCE_ATTRIBUTE]],
                               partition=0)
            if event[parameters[performance_constants.EVENT_CLASSIFIER]] in ends:
                graph.add_node(event[performance_constants.EVENT_INDEX], name=event[parameters[performance_constants.EVENT_CLASSIFIER]],
                               ea=event[parameters[performance_constants.DISTANCE_ATTR]], epa=event[parameters[performance_constants.EVENT_PERFORMANCE_ATTRIBUTE]],
                               partition=1)
    return graph


def add_edges(graph, parameters):
    """
    Add edges to form a bipartite graph
    """
    nodes_start = [node for node, attr_dict in graph.nodes(data=True) if attr_dict['partition'] == 0]
    nodes_end = [node for node, attr_dict in graph.nodes(data=True) if attr_dict['partition'] == 1]

    for node_start in nodes_start:
        for node_end in nodes_end:
            if node_start < node_end:
                graph.add_edge(node_start, node_end, weight=compute_distance(graph.nodes[node_start], graph.nodes[node_end], parameters), #graph.nodes[node_end]['ea']-graph.nodes[node_start]['ea'],
                               perf=graph.nodes[node_end]['epa']-graph.nodes[node_start]['epa'])
    return graph


def compute_distance(node1, node2, parameters):
    if parameters[performance_constants.MATCHING_DISTANCE_FUNC] is None:
        if parameters[performance_constants.DISTANCE_ATTR] == performance_constants.EVENT_INDEX:
            return 1/(node2['ea'] - node1['ea'])
        elif isinstance(node1['ea'], int) or isinstance(node1['ea'], float):
            return node2['ea'] - node1['ea']
        elif isinstance(node1['ea'], str):
            return int(node1['ea'] == node2['ea'])
    else:
        return parameters[performance_constants.MATCHING_DISTANCE_FUNC](node1['ea'], node2['ea'])