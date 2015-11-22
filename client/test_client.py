from client import Client
from pdb import set_trace
from random import randint, choice

client = Client()

for sset in client.subject_sets(client.mark_workflow):
    options = client.mark_workflow['tasks']['mark_primary']['tool_config']['options']
    colors = [x['color'] for x in options]
    subject_set = sset['id']
    for subject in client.markable(subject_set):
        for i in range(1, 15):
            color = choice(colors)
            data = client.mark(subject_set, subject['id'], color,
                               randint(0, 1500), randint(0, 1500), 
                               randint(200, 1000), randint(50, 500))

for sset in client.subject_sets(client.transcribe_workflow):
    for subject in client.transcribable(sset):
        for i in range(1, 3):
            response = client.transcribe(
                subject, 
                "Random value %s" % randint(100, 999)
            )
            print response.json()
    
