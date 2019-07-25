
import googlemaps
import json
from operator import itemgetter


def get_dist_matrix(lat, longt, locs):
    gmaps = googlemaps.Client(key='AIzaSyCSMn6DIKRxyKHzfO-mhjnqU6u6ZHkUbgE')

    ids = [x[0] for x in locs]
    origins = [(x[1], x[2]) for x in locs]

    distmatrix_result = gmaps.distance_matrix(
        origins=origins, destinations=(lat, longt))

    req_details = []
    for item in distmatrix_result['rows']:
        for x in item['elements']:
            req_details.append((x['distance']['text'],
                                x['distance']['value'],
                                x['duration']['text'],
                                x['duration']['value']))

    merged = [{'id': i, 'details': a} for i, a in zip(ids, req_details)]
    shortest = min(merged, key=lambda x: x['details'][1])

    return shortest


"""locdata = [
    (1, -1.0984512, 37.0107431),
    (2, -1.0994236450388715, 37.0120918750763),
    (3, -1.098136421449109, 37.016737461090095),
    (4, -1.1003032475060555, 37.019698619842536)
]

print(get_dist_matrix(1.0985132000000002, 37.0108526, locdata))"""
