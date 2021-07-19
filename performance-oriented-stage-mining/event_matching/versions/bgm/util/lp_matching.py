import pulp
from util import constants as performance_constants

def get_matching_edges(graph, parameters):
    """
    Apply minimal weight maximal matching with LP

    :param graph:
        Encoded graph of a trace
    :return edges:
        selected edge of a graph
    """

    "Declare a LP solver"
    if parameters[performance_constants.MATCHING_DISTANCE_FUNC] is None and parameters[performance_constants.DISTANCE_ATTR] == performance_constants.EVENT_INDEX:
        model = pulp.LpProblem('Event matching', pulp.LpMaximize)
    else:
        model = pulp.LpProblem('Event matching', pulp.LpMinimize)

    "Declare variables"
    variables = pulp.LpVariable.dicts('edge', [str(edge) for edge in graph.edges], cat='Binary')

    "Define objective"
    model += pulp.lpSum([variables[str(edge)]*graph[edge[0]][edge[1]]['weight'] for edge in graph.edges])

    "Set constraint for the number of edges selected"
    model += pulp.lpSum(list(variables.values())) == min(len([node for node, attr_dict in graph.nodes(data=True) if attr_dict['partition'] == 0]),
                                                         len([node for node, attr_dict in graph.nodes(data=True) if attr_dict['partition'] == 1]))
    "Set constraint on nodes"
    set_constraints_on_nodes(model, variables, graph.nodes, graph.edges)
    model.solve()
    return get_edges(variables)


def set_constraints_on_nodes(model, variables, nodes, edges):
    for node in nodes:
        edges_of_node = [edge for edge in edges if node in edge]
        model += pulp.lpSum([variables[str(edge)] for edge in edges_of_node]) <= 1


def get_edges(variables):
    edges = []
    for edge in variables.keys():
        if variables[edge].varValue == 1:
            start = int(edge.split(',')[0].split('(')[1])
            end = int(edge.split(',')[1].split(')')[0])
            edges.append((start, end))
    return edges