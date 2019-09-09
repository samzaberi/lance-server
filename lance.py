from operator import itemgetter
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from geodist import haversine, get_dist_matrix

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


@app.route('/dispatch?destination=<lat>,<longt>', methods=['GET'])
def get_vehicle(lat, longt):
    vehicle_locs = Vehicle.query.with_entities(
        Vehicle.id, Vehicle.lat, Vehicle.longt).filter_by(isactive=True)

    distances = []
    for item in vehicle_locs:
        val = haversine(float(lat), float(longt), item[1], item[2])
        distances.append((item[0], val))

    srtd_by_dist = sorted(distances, key=itemgetter(1))
    ids_for_closest_five = [x[0] for x in srtd_by_dist[:6]]
    locs_for_req = [x for x in vehicle_locs if x[0] in ids_for_closest_five]
    dist_matrix_result = get_dist_matrix(lat, longt, locs_for_req)
    query_with_result = Vehicle.query.with_entities(
        Vehicle.drivername, Vehicle.plateno).filter_by(id=dist_matrix_result['id']).all()
    vehicle_details = {'drivername': query_with_result[0][0],
                       'plateno': query_with_result[0][1],
                       'distance': dist_matrix_result['details'][0],
                       'ETA': dist_matrix_result['details'][2]}
    print(vehicle_details)
    return jsonify(vehicle_details)


if __name__ == '__main__':
    app.run(debug=True)
