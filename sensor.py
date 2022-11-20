import datetime
import json
import random
import time
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'
from google.cloud import tasks_v2

client = tasks_v2.CloudTasksClient()

project = 'fluted-gantry-367015'
queue = 'lab2'
location = 'europe-west1'
task_name = 'my-unique-task'

parent = client.queue_path(project, location, queue)


class Data:
    def __init__(self):
        self._data_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self._data_humidity = random.randint(0, 100)
        self._data_temperature = random.randint(0, 20)
        self._data_pressure = random.randint(800, 1200)

    def __str__(self):
        return json.dumps({key[6:]: data if not isinstance(data, str) else '\'' + data + '\''
                           for key, data in self.__dict__.items() if key.startswith('_data')})


def get_task(url):
    return {
        'http_request': {
            'http_method': tasks_v2.HttpMethod.POST,
            'url': url,
            'headers': {'Content-type': 'application/json'},
            'body': str(Data()).encode()
        }
    }


while True:
    response = client.create_task(request={"parent": parent, "task": get_task('https://europe-west1-fluted-gantry-367015.cloudfunctions.net/add_data')})
    time.sleep(1)
