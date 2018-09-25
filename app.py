import thread

from flask import Flask, Response, request
import urllib
import urllib2
import json
import os.path
import math
from argparse import ArgumentParser
from geopy.distance import great_circle

from idle import Idle
from pointer import Pointer, TestPointer
from display import Display, TestDisplay

argp = ArgumentParser()
argp.add_argument('--test', action='store_true')
argp.add_argument('--lat_home', type=float, default=51.480332)
argp.add_argument('--long_home', type=float, default=-2.768165)
argp.add_argument('--idle', action='store_true')
argp.add_argument('--idle_delay', type=float, default=30)
args = argp.parse_args()

app = Flask(__name__)
lat_here = args.lat_home
long_here = args.long_home
home = (lat_here, long_here)

pointer = TestPointer() if args.test else Pointer()
display = TestDisplay() if args.test else Display()

do_idle = args.idle
idle_delay = args.idle_delay


def get_file(file_name):
    root = os.path.abspath(os.path.dirname(__file__))
    src = os.path.join(root, file_name)
    return open(src).read()


@app.route('/')
def page():
    content = get_file('page.html')
    return Response(content, mimetype='text/html')


def get_bearing(lat, longt):
    # convert degree angles to radians

    lat_ar = math.radians(lat_here)
    long_ar = math.radians(long_here)

    lat_br = math.radians(lat)
    long_br = math.radians(longt)

    xr = math.cos(lat_br) * math.sin(long_br - long_ar)
    yr = (math.cos(lat_ar) * math.sin(lat_br)) - (math.sin(lat_ar) * math.cos(lat_br) * math.cos(long_br - long_ar))

    br = math.atan2(xr, yr)

    bd = math.degrees(br)

    bd_int = int(bd)

    # get bearing as 0 to 360

    bd_360 = (bd_int + 360) % 360

    return bd_360


def get_steps(bearing):
    # returns number of steps to make

    frac_turn = bearing / 360.0
    steps_for_angle = 200 * frac_turn
    steps_to_make = int(steps_for_angle)
    return steps_to_make


def send_pointer(lat, longt):
    bearing = get_bearing(lat, longt)
    steps = get_steps(bearing)
    pointer.set_steps(steps)
    print('pointer updated')


def send_display(result, lat, longt):
    location = (float(lat), float(longt))
    dist = great_circle(home, location).km
    dist = round(dist, 1)
    dist = str(dist)
    print(dist)

    display.clear()
    display.font_size(3)
    display.add_text(result['BusinessName'])
    display.font_size(2)

    text = "\n".join([
        result['AddressLine1'] if result['AddressLine1'] is not None else '',
        'FHRS Hygiene Rating:',
        '%s out of 5' % result["RatingValue"],
        'Rated on ' + result['RatingDate'],
        dist + 'km away'
    ])
    display.add_text(text)
    print("display updated")


def send(result, lat, longt):
    send_pointer(lat, longt)
    send_display(result, lat, longt)


def do_query(name, address):
    url = "http://ratings.food.gov.uk/search/en-GB/%(name)s/%(address)s/json" % {
        "name": urllib.quote(name),
        "address": urllib.quote(address)
    }
    print url
    json_response = urllib2.urlopen(url).read()
    response = json.loads(json_response)
    if "EstablishmentCollection" not in response["FHRSEstablishment"]:
        return "Establishment not found - click Back in your browser to search again"
    results = response["FHRSEstablishment"]["EstablishmentCollection"]["EstablishmentDetail"]
    result = results[0] if isinstance(results, list) else results

    lat = float(result["Geocode"]["Latitude"])
    longt = float(result["Geocode"]["Longitude"])

    send(result, lat, longt)

    return "Success!"


idle = Idle(lat_here, long_here, send, idle_delay)


@app.route('/query', methods=['POST'])
def query():
    name = request.form['name']
    address = request.form['address']
    idle.delay()
    return do_query(name, address)


if __name__ == '__main__':
    if do_idle:
        thread.start_new_thread(idle.start, ())
    app.run()

