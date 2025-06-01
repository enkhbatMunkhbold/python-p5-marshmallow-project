from flask import request, session, jsonify
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from marshmallow import fields, validate, ValidationError
from config import app, db, api, ma

from models import User, Flight, Airline, Booking, UserSchema, FlightSchema, AirlineSchema, BookingSchema

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
        return flights_schema.dump(all_flights), 200
    
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
        return flight_schema.dump(new_flight), 201
api.add_resource(Flights, '/flights')

class Airlines(Resource):
    def get(self):
        all_airlines = Airline.query.all()
        return airlines_schema.dump(all_airlines), 200
    
    def post(self):
        data = request.get_json()
        new_airline = Airline(
            name = data['name'],
            country = data['country']
        )
        db.session.add(new_airline)
        db.session.commit()
        return airline_schema.dump(new_airline), 201

api.add_resource(Airlines, '/airlines')

class Bookings(Resource):
    def get(self):
        all_bookings = Booking.query.all()
        return bookings_schema.dump(all_bookings), 200
    
    def post(self):
        try:
            data = request.get_json()
            new_booking = Booking(**data)
            db.session.add(new_booking)
            db.session.commit()
            return booking_schema.dump(new_booking), 201
        except IntegrityError:
            db.session.rollback()
            return {'error': 'Invalid foreign key'}, 400
        
api.add_resource(Bookings, '/bookings')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

