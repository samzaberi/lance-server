
from locutils import haversine
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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


@app.route('/dispatch/vehicle/destination=<lat>,<longt>', methods=['GET'])
def get_vehicle(lat, longt):
    locations = Vehicle.query.with_entities(
        Vehicle.id, Vehicle.lat, Vehicle.longt).all()
    results = []
    for item in locations:
        val = haversine(float(lat), float(longt), item[1], item[2])
        results.append(val)
    return jsonify(results)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
