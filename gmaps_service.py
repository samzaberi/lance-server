
import googlemaps
import json


def req_dist_matrix(lat, longt, locs):
    gmaps = googlemaps.Client(key='API_KEY')

    ids = [x[0] for x in locs]
    origins = [(x[1], x[2]) for x in locs]

    distmatrix_result = gmaps.distance_matrix(
        origins=origins, destinations=(lat, longt))

    req_details = []
    for item in distmatrix_result['rows']:
        for x in item['elements']:
            req_details.append(
                {'dist_text': x['distance']['text'],
                 'distance': x['distance']['value'],
                 'duration': x['duration']['text']})
    results = []
    for i, a in zip(ids, req_details):
        results.append({'id': i, 'details': a})

    return results


locdata = [
    (1, -1.0984512, 37.0107431),
    (2, -1.0994236450388715, 37.0120918750763),
    (3, -1.098136421449109, 37.016737461090095),
    (4, -1.1003032475060555, 37.019698619842536)
]

print(req_dist_matrix(1.0985132000000002, 37.0108526, locdata))
