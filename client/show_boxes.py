from client import Client
from pdb import set_trace
import sys

if len(sys.argv) > 1:
    host = sys.argv[1]
else:
    host = "http://localhost:3000"
client = Client(host)

for sset in client.subject_sets(client.transcribe_workflow):
    for subject in client.subjects(sset):
        for child in subject['child_subjects']:
            region = child['region']
            print "%s @ %s (%s,%s)-(%s,%s)" % (
                region['label'], 
                subject['id'],
                region['x'], region['y'], 
                region['x'] + region['width'], region['x'] + region['height'], 
            )
