import urllib
from time import sleep
import requests


class Pointer:
    max_steps = 200
    current_steps = 0
    host = 'http://192.168.3.101/stepper'

    def __init__(self):
        pass

    def set_steps(self, steps):
        requests.get(self.host + '/start')
        requests.get(self.host + '/steps?' + urllib.urlencode({'steps': (self.max_steps - self.current_steps)}))
        sleep(2)
        requests.get(self.host + '/steps?' + urllib.urlencode({'steps': steps}))
        requests.get(self.host + '/stop')

        self.current_steps = steps


class TestPointer:

    def __init__(self):
        pass

    def set_steps(self, steps):
        print("steps: " + str(steps))
