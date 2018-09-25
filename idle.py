import json
import thread
import time
import datetime

import requests


class Idle:

    def get_establishments(self, lat, longt):
        headers = {'x-api-version': '2'}
        url = "http://api.ratings.food.gov.uk/Establishments?longitude=%(longt)s&latitude=%(lat)s&maxDistanceLimit=2&sortOptionKey=Distance&businessTypeId=1" % {
            'longt': str(longt),
            'lat': str(lat)
        }
        print url
        json_response = requests.get(url, headers=headers).content
        response = json.loads(json_response)
        results = response['establishments']
        print('nearby: ' + str(results.__len__()))
        return results

    def __init__(self, lat, longt, send, delay_seconds):
        self.establishments = self.get_establishments(lat, longt)
        self.establishmentsIt = self.establishments.__iter__()
        self.next_move = time.time()
        self.delay_seconds = delay_seconds
        self.delay()
        self.send = send

    def start(self):
        while True:
            if self.next_move < time.time():
                try:
                    result = next(self.establishmentsIt)
                    print result['BusinessName']
                    lat = float(result["geocode"]["latitude"])
                    longt = float(result["geocode"]["longitude"])
                    result['RatingDate'] = result['RatingDate'].split("T")[0]

                    self.send(result, lat, longt)
                except StopIteration:
                    self.establishmentsIt = self.establishments.__iter__()
                finally:
                    self.delay()
            else:
                time.sleep(self.next_move - time.time())

    def delay(self):
        self.next_move += self.delay_seconds


if __name__ == '__main__':
    idle = Idle(51.480332, -2.768165)

    t = thread.start_new_thread(idle.start, ())

    while True:
        time.sleep(1)
