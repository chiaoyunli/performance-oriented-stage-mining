# Stage-Based Process Performance Mining

Extract stage instances and visualize the stage performance evolution.

## Usage
```python
from pm4py.objects.log.importer.xes import factory as xes_importer
from event_matching import factory as em_factory


log = xes_importer.apply('example_log.xes')

starts = ['Permit SUBMITTED by EMPLOYEE'] # Start activities
ends = ['Permit FINAL_APPROVED by SUPERVISOR', 'Permit FINAL_APPROVED by DIRECTOR'] # End activities
matching = em_factory.apply(log, starts, ends) # Return index of pairs of events per case
```

More examples of event matching are shown in example/em_example.py

