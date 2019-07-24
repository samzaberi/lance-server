from operator import itemgetter

from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from geodist import haversine
from gmaps_service import req_dist_matrix

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicles.sqlite3'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drivername = db.Column(db.String())
    plateno = db.Column(db.String())
    lat = db.Column(db.Float)
    longt = db.Column(db.Float())
    isactive = db.Column(db.Boolean())


@app.route('/dispatch/destination=<lat>,<longt>', methods=['GET'])
def get_vehicle(lat, longt):
    vehicle_locs = Vehicle.query.with_entities(
        Vehicle.id, Vehicle.lat, Vehicle.longt).filter_by(isactive=True)
    distances = []
    for item in vehicle_locs:
        val = haversine(float(lat), float(longt), item[1], item[2])
        distances.append({'id': item[0], 'distance': val})

    srtd_by_dist = sorted(distances, key=itemgetter('distance'))
    closest_five_dist = srtd_by_dist[:6]
    print(closest_five_dist)
    ids_for_closest_five = [x['id'] for x in closest_five_dist]
    locs_for_req = [x for x in vehicle_locs if x[0] in ids_for_closest_five]
    result = req_dist_matrix(lat, longt, locs_for_req)
    print(result)
    """id_shortest_dist = srtd_by_dist[0]['id']
    veh = Vehicle.query.with_entities(
        Vehicle.drivername, Vehicle.plateno).filter_by(id=id_shortest_dist).all()
    vehdict = {'drivername': veh[0][0], 'plateno': veh[0][1]}"""

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
