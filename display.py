import requests
import json


class Display:
    host = 'http://192.168.3.102/display'

    def __init__(self):
        pass

    def clear(self):
        requests.get(self.host + '/clear')

    def font_size(self, size):
        requests.get(self.host + '/fontsize?font-size=' + str(size))

    def add_text(self, text):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        body = {'display-text': text}
        requests.post(self.host + '/textdisplay', data=json.dumps(body), headers=headers)


class TestDisplay:

    def __init__(self):
        pass

    def clear(self):
        print('clear')

    def font_size(self, size):
        print('font: ' + str(size))

    def add_text(self, text):
        print('text: ' + text)
