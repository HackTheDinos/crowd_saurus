from client import Client
from pdb import set_trace
import random

client = Client()

for sset in client.subject_sets(client.mark_workflow):
    subject_set = sset['id']
    set_trace()
    for subject in client.markable(subject_set):
        set_trace()
        pass

for sset in client.subject_sets(client.transcribe_workflow):
    for subject in client.transcribable(subject_set):
        for i in range(1, 15):
            client.transcribe(
                subject['subject_set_id'], subject['id'], random.randint(100, 999)
            )
    
