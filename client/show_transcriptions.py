from client import Client
from pdb import set_trace
import sys

if len(sys.argv) > 1:
    host = sys.argv[1]
else:
    host = "http://localhost:3000"
client = Client(host)

for sset in client.subject_sets(client.transcribe_workflow):
    for child in client.recursive_subjects(client.subjects(sset)):
        if child['data'] and 'values' in child['data']:
            region = child['region']
            value = ", ".join(
                [x['value'] for x in child['data']['values'] if 'value' in x]
            )
            print "%s %s @ (%s,%s)-(%s,%s): %s" % (
                region['label'], 
                child['parent_subject_id'],
                region['x'], region['y'], 
                region['x'] + region['width'], region['x'] + region['height'], 
                value
            )
