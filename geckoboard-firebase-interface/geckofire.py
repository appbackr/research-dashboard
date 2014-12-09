import requests, json
import boto.sqs
import time
from firebasin import Firebase

AWS_REGION = 'us-east-1'
AWS_ACCESS_KEY_ID = 'AKIAIFTIY5ZI7LLA77UQ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_SQS_JOB_QUEUE = 'DeepAPKInspection'

FIREBASE_URL = 'https://appbackr-dashboard.firebaseio.com/techeval'
GECKO_KEY = '6162a0490fb4a013ff38cd8c859f3803'

class Gecko(object):
    def __init__(self, api_key):
        self.api_key = api_key

    def push(self, widget_key, data):
        ret = requests.post("https://push.geckoboard.com/v1/send/%s" % widget_key, json.dumps({'api_key' : self.api_key, 'data' : data}), verify=False)
        if not (ret.status_code == 200 and ret.json().get('success') == True):
            #raise ValueError(ret.content)
            print ret.content

    def number(self, widget_key, number1, number2=None):
        data = {'item' : []}
        if number1: data['item'].append({'value' : number1, 'text' : ''})
        if number2: data['item'].append({'value' : number2, 'text' : ''})
        return self.push(widget_key, data)

    def rag(self, widget_key, *items):
        data = {'item' : []}
        for item in items:
            data['item'].append({'value' : item[0], 'text' : item[1]})
        return self.push(widget_key, data)

    def line(self, widget_key, values, **kwargs):
        data = {'item' : [], 'settings' :kwargs}
        for item in values:
            data['item'].append(item)
        return self.push(widget_key, data)

    def text(self, widget_key, *texts):
        data = { "item" : [] }
        for text in texts:
            if isinstance(text, dict):
                data['item'].append(dict(text))
            else:
                data['item'].append({"text" : text, "type" : 0})
        return self.push(widget_key, data)

    def heartbeat(self, widget_key, utc=True, format="%H:%M / %d %b"):
        import datetime
        dt = (datetime.datetime.utcnow if utc else datetime.datetime.now)().strftime(format)
        return self.text(widget_key, dt)

    def beater(self, *args, **kwargs):
        return lambda: self.heartbeat(*args, **kwargs)


'''
ws4py raises an Exception whenever WebSocketClient fails, probably due to firebase
Catch the exception and restart the reporting to avoid having to manually restart
the script
'''
while True:
    try:
        print "(" + time.asctime( time.localtime(time.time()) ) + ") Clean Start..."

        dashboard = Gecko(GECKO_KEY)
        firebase = Firebase(FIREBASE_URL)

        last_completedAPKs = 0
        last_APKsInQueue = 0

        def onAPKCompletion(snapshot):
            global last_completedAPKs
            global last_APKsInQueue

            conn = boto.sqs.connect_to_region(
                    AWS_REGION,
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
            q = conn.get_queue(AWS_SQS_JOB_QUEUE)

            if last_completedAPKs != snapshot.numChildren():
                last_completedAPKs = snapshot.numChildren()
                dashboard.push('117656-be1bb359-bd24-495d-a8ca-d238e9ffd7f0', {'item': [
                    {
                        'value': snapshot.numChildren(),
                        'text': 'APKs Analysed'
                    }]})

            if last_APKsInQueue != q.count():
                last_APKsInQueue = q.count()
                dashboard.push('8113-a8063c60-6195-0132-c490-22000b51936c', {'item': [
                    {
                        'value': q.count(),
                        'text': 'APKs Awaiting Analysis'
                    }]})

        firebase.child("completions").on('value', onAPKCompletion)

        def onInstanceStatusChange(snapshot):
            data = list()
            raw = snapshot.exportVal()

            while raw:
                k, v = raw.popitem()
                data.append({'title': {'text': k}, 'description': v['status'] + '. Last Update: ' + v['last_update']})

            dashboard.push('117656-6cd6ee10-7538-40fe-b5fc-88d1c45a89e8', data)

        firebase.child("instances").on('value', onInstanceStatusChange)

        def onFailure(snapshot):
            dashboard.push('117656-a8b93f28-d15c-4446-ac38-b89c74b0c27a', {'item': [
            {'text': 'FlowDroid Java Exception', 'value': snapshot.child('FlowDroidJavaException').numChildren()},
            {'text': 'FlowDroid Timeout', 'value': snapshot.child('FlowDroidTimeout').numChildren()},
            {'text': 'Reverse Engineering Exception', 'value': snapshot.child('ReverseEngineeringException').numChildren()}]})

        firebase.child("failures").on('value', onFailure)

        '''completedAPKs = list()

        def onAPKCompletionChildAdded(childSnapshot):
            completedAPKs.insert(0, {'title': childSnapshot.name(), 'text': childSnapshot.val()['instance']})
            dashboard.push('117656-0ffd0ee2-4754-41f4-8faf-295c6edae030', completedAPKs)

        try:
            firebase.child("completions").on('child_added', onAPKCompletionChildAdded)
        except:
            None'''

        firebase.waitForInterrupt()
    except:
        pass
    else:
        break