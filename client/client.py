from urllib import urlencode
import datetime
import requests
from pdb import set_trace

class Client(object):

    def __init__(self, host='http://localhost:3000'):
        self.host = host
        data = requests.get(host + '/projects').json()
        self.project = data['project']
        [self.mark_workflow] = [x for x in self.project['workflows']
                                if x['name'] == 'mark']

        [self.transcribe_workflow] = [x for x in self.project['workflows']
                                      if x['name'] == 'transcribe']

        [self.verify_workflow] = [x for x in self.project['workflows']
                                  if x['name'] == 'verify']

    def subject_sets(self, workflow):
        workflow_id = workflow['id']
        url = self.host + '/subject_sets?limit=10&workflow_id=%s&random=true' % (workflow_id)
        response = requests.get(url)
        set_trace()
        data = response.json()
        return [x for x in data['data']]

    def subjects(self, subject_set):
        url = self.host + '/subjects?subject_set_id=%s&page=1&limit=120&type=root&status=any' % subject_set
        response = requests.get(url)
        data = response.json()
        return [x for x in data['data']]

    def markable(self, subject_set):
        for subject in self.subjects(subject_set):
            yield subject

    def transcribable(self, subject_set):
        for subject in self.recursive_subjects(self.subjects(subject_set)):
            if subject['data'] and subject['data'].get('isTranscribable'):
                yield subject

    def recursive_subjects(self, initial_set):
        if not initial_set:
            return
        for s in initial_set:
            if s:
                yield s
            for ch in self.recursive_subjects(s['child_subjects']):
                if ch:
                    yield ch

    def _ca(self, d, key, value):
        d['classifications[annotation][%s]' % key] = value

    def _timestamp(self, d):
        started_at = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        d['classifications[metadata][started_at]'] = started_at
        d['classifications[metadata][finished_at]'] = started_at

    def _address(self, d, subject_set, subject):
        d['classifications[subject_id]'] = subject
        d['classifications[subject_set_id]'] = subject_set
        d['classifications[workflow_id]'] = self.workflow_id

    def mark(self, subject_set, subject, color, x, y, width, height):
        url = self.host + '/classifications'
        d = {}
        self._ca(d, 'belongsToUser', 'true')
        self._ca(d, 'userCreated', 'true')
        self._ca(d, 'isTranscribable', 'true')
        self._ca(d, 'toolName', 'rectangleTool')
        self._ca(d, 'subToolIndex', '0')
        self._ca(d, 'status', 'mark')

        self._ca(d, 'color', color)
        self._ca(d, 'x', x)
        self._ca(d, 'y', y)
        self._ca(d, 'width', width)
        self._ca(d, 'height', height)

        self._address(d, subject_set, subject)

        d['classifications[task_key]']='mark_primary'
        
        self._timestamp(d)
        response = requests.post(url, data=d)

    def transcribe(self, subject_set_id, subject_id, value):

        url = self.host + '/classifications'
        d = {}
        self._ca(d, 'value', value)       
        self._address(d, subject_set_id, subject_id)
        self._timestamp(d)

        # TODO: this is bad.
        d['classifications[task_key]'] = ':f_box_number'

        response = requests.post(url, data=d)


# Transcribe step

# classifications[annotation][value]:349
# classifications[subject_id]:5651bbe47568610b9b0a0000
# classifications[subject_set_id]:
# classifications[task_key]:f_box_number
# classifications[metadata][started_at]:2015-11-22T13:11:06.361Z
# classifications[metadata][finished_at]:2015-11-22T13:11:39.426Z
# classifications[workflow_id]:5651b7f07568610b94060000
