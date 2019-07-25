import math
import googlemaps
import json
from operator import itemgetter


def haversine(lat1, lon1, lat2, lon2):

    # distance between latitudes
    # and longitudes
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0

    # convert to radians
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0

    # apply formulae
    a = (pow(math.sin(dLat / 2), 2) +
         pow(math.sin(dLon / 2), 2) *
         math.cos(lat1) * math.cos(lat2))
    # radius of the earth in kilometres
    rad = 6371
    c = 2 * math.asin(math.sqrt(a))
    # result in kilometres
    return rad * c


def get_dist_matrix(lat, longt, locs):
    gmaps = googlemaps.Client(key='API_KEY')

    ids = [x[0] for x in locs]
    origins = [(x[1], x[2]) for x in locs]

    distmatrix_result = gmaps.distance_matrix(
        origins=origins, destinations=(lat, longt))

    desired_fields = []
    for item in distmatrix_result['rows']:
        for x in item['elements']:
            desired_fields.append((x['distance']['text'],
                                   x['distance']['value'],
                                   x['duration']['text'],
                                   x['duration']['value']))

    merged = [{'id': i, 'details': a} for i, a in zip(ids, desired_fields)]
    shortest = min(merged, key=lambda x: x['details'][1])

    return shortest
