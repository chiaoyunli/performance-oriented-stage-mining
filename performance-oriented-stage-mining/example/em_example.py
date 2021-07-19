from pm4py.objects.log.importer.xes import factory as xes_importer
from event_matching import factory as em_factory


def show_example_result(matchings):
    """Print the matching and the performance measure of the matching of a case

    :param matchings: dict
        Event matched and corresponding measures of a case
    """
    for case_id, edges in matchings.items():
        print('Case ID', end=': ')
        print(case_id)
        for edge, measure in edges.items():
            print(edge, end=': ')
            print(measure)
        break


def run_example1(log):
    """
    Example 1: Without endpoints definition: collection of all start/end activities of all cases
    """
    # Run the algorithm
    return em_factory.apply(log)


def run_example2(log):
    """
    Example 2: Endpoints defined
    """
    # Define start and end activities
    starts = ['Permit SUBMITTED by EMPLOYEE']
    ends = ['Permit REJECTED by ADMINISTRATION', 'Permit REJECTED by BUDGET OWNER', 'Permit REJECTED by SUPERVISOR', 'Permit REJECTED by DIRECTOR', 'Permit FINAL_APPROVED by SUPERVISOR', 'Permit FINAL_APPROVED by DIRECTOR']
    # Run the algorithm
    return em_factory.apply(log, starts, ends)


def dis_func(start_value, end_value):
    if start_value == end_value:
        return 0
    else:
        return 1


def run_example3(log):
    """
    Example 3: Endpoints and matching methods defined
    """
    starts = ['Permit SUBMITTED by EMPLOYEE']
    ends = ['Permit REJECTED by ADMINISTRATION', 'Permit REJECTED by BUDGET OWNER', 'Permit REJECTED by SUPERVISOR', 'Permit REJECTED by DIRECTOR', 'Permit FINAL_APPROVED by SUPERVISOR', 'Permit FINAL_APPROVED by DIRECTOR']
    matching_param = {'distance_attribute': 'id', 'distance_func': dis_func}
    # Run the algorithm
    return em_factory.apply(log, starts, ends, matching_param)


if __name__ == "__main__":
    log = xes_importer.apply('example_log.xes')
    matching1 = run_example1(log)
    matching2 = run_example2(log)
    matching3 = run_example3(log)

    # Show example results
    show_example_result(matching1)
    print('='*25+'\n')
    show_example_result(matching2)
    print('='*25+'\n')
    show_example_result(matching3)
