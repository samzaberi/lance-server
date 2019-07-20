import locutils

from flask import Flask, jsonify

app = Flask(__name__)

locations = [
    {
        'id': 1,
        'lat': -1.2865850785072128,
        'long': 36.88099622726441
    },
    {
        'id': 2,
        'lat': -1.2885479597710903,
        'long': 36.88336193561555
    },
    {
        'id': 3,
        'lat': -1.2885211444634657,
        'long': 36.87934935092927
    }
]


@app.route('/vehicles/origin=<src_lat>,<src_long>', methods=['GET'])
def get_vehicle(src_lat, src_long):
    results = locutils.haversine_on_dict(
        float(src_lat), float(src_long), locations)
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
