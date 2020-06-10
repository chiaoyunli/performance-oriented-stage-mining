from pm4py.objects.log.importer.xes import factory as xes_importer
from stage_performance import factory as stage_factory


def show_example_result(stage_performance):
    """Print the performance metrics of a case

    :param stage_performance: list
        List of case performance per stage_variant
    """
    for cases_perf_per_stage_variant in stage_performance:
        print('Stage Variant', end=': ')
        print(cases_perf_per_stage_variant['stage_variant'])
        for case, case_performance in cases_perf_per_stage_variant['cases_performance'].items():
            print('Case ID', end=': ')
            print(case)
            for stage_key, stage_metrics in case_performance.items():
                print('Stage', end=': ')
                print(stage_key)
                for metrics_key, metrics in stage_metrics.items():
                    print(metrics_key, end=': ')
                    print(metrics)
            break
        break


log = xes_importer.apply('example_log.xes')


def run_example1(log):
    """
    Example 1: Without stage definition: collection of all start/end activities of all cases
    """
    # Run the algorithm
    return stage_factory.apply(log)


def run_example2(log):
    """
    Example 2: Stages defined
    """
    # Define stages
    stages_def = {'A': {'starts': ['Permit SUBMITTED by EMPLOYEE'],
                        'ends': ['Permit REJECTED by ADMINISTRATION', 'Permit REJECTED by BUDGET OWNER', 'Permit REJECTED by SUPERVISOR', 'Permit REJECTED by DIRECTOR', 'Permit FINAL_APPROVED by SUPERVISOR', 'Permit FINAL_APPROVED by DIRECTOR']},
                  'R': {'starts': ['Request For Payment SUBMITTED by EMPLOYEE'],
                        'ends': ['Request For Payment REJECTED by ADMINISTRATION', 'Request For Payment REJECTED by BUDGET OWNER', 'Permit REJECTED by SUPERVISOR', 'Payment Handled']},
                  'D': {'starts': ['Declaration SUBMITTED by EMPLOYEE'],
                        'ends': ['Declaration REJECTED by ADMINISTRATION', 'Declaration REJECTED by BUDGET OWNER', 'Declaration REJECTED by SUPERVISOR', 'Declaration REJECTED by DIRECTOR', 'Payment Handled']}}
    # Run the algorithm
    return stage_factory.apply(log, stages_def)


def run_example3(log):
    """
    Example 3: Stages and matching parameters defined
    """
    # Define stages
    stages_def = {'A': {'starts': ['Permit SUBMITTED by EMPLOYEE'],
                    'ends': ['Permit REJECTED by ADMINISTRATION', 'Permit REJECTED by BUDGET OWNER', 'Permit REJECTED by SUPERVISOR', 'Permit REJECTED by DIRECTOR', 'Permit FINAL_APPROVED by SUPERVISOR', 'Permit FINAL_APPROVED by DIRECTOR']},
             'R': {'starts': ['Request For Payment SUBMITTED by EMPLOYEE'],
                   'ends': ['Request For Payment REJECTED by ADMINISTRATION', 'Request For Payment REJECTED by BUDGET OWNER', 'Permit REJECTED by SUPERVISOR', 'Payment Handled'],
                   'matching_param': {'distance_attribute': 'Rfp_id'}},
             'D': {'starts': ['Declaration SUBMITTED by EMPLOYEE'],
                   'ends': ['Declaration REJECTED by ADMINISTRATION', 'Declaration REJECTED by BUDGET OWNER', 'Declaration REJECTED by SUPERVISOR', 'Declaration REJECTED by DIRECTOR', 'Payment Handled'],
                   'matching_param': {'distance_attribute': 'dec_id'}}}
    # Run the algorithm
    return stage_factory.apply(log, stages_def)


if __name__ == "__main__":
    log = xes_importer.apply('example_log.xes')
    stage_performance1 = run_example1(log)
    stage_performance2 = run_example2(log)
    stage_performance3 = run_example3(log)

    # Show example results
    show_example_result(stage_performance1)
    print('='*25+'\n')
    show_example_result(stage_performance2)
    print('='*25+'\n')
    show_example_result(stage_performance3)