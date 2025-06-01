from flask import request, session, jsonify
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from marshmallow import fields, validate, ValidationError

# Import app and extensions first
from config import app, db, api, ma

# Then import models and schemas
from models import User, Flight, Airline, Booking, UserSchema, FlightSchema, AirlineSchema, BookingSchema

# Initialize schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)
flight_schema = FlightSchema()
flights_schema = FlightSchema(many=True)
airline_schema = AirlineSchema()
airlines_schema = AirlineSchema(many=True)
booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)

@app.route('/')
def index():
    return '<h1>Project Server</h1>'

class Flights(Resource):
    def get(self):
        all_flights = Flight.query.all()
        return jsonify(flights_schema.dump(all_flights))
    
    def post(self):
        data = request.get_json()
        new_flight = Flight(
            origin = data['origin'],
            destination = data['destination'],
            departure_time = data['departure_time'],
            arrival_time = data['arrival_time']
        )
        db.session.add(new_flight)
        db.session.commit()
        return jsonify(flight_schema.dump(new_flight), 201)

if __name__ == '__main__':
    app.run(port=5555, debug=True)

