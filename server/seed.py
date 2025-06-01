#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc
from datetime import datetime, timedelta, timezone

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, User, Flight, Airline, Booking

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")
        
        # Create all tables
        print("Creating database tables...")
        # db.create_all()
        
        # Clear existing data
        print("Clearing existing data...")
        Booking.query.delete()
        Flight.query.delete()
        Airline.query.delete()
        User.query.delete()
        
        print("Creating airlines...")
        airlines = []
        airline_names = [
            "SkyWings Airlines",
            "Global Airways",
            "Pacific Express",
            "Atlantic Air",
            "Mountain View Airlines"
        ]
        
        for name in airline_names:
            airline = Airline(
                name=name,
                country=fake.country()
            )
            airlines.append(airline)
            db.session.add(airline)
        
        db.session.commit()
        
        print("Creating flights...")
        flights = []
        cities = [
            "New York", "Los Angeles", "London", "Tokyo", "Paris",
            "Sydney", "Dubai", "Singapore", "Hong Kong", "Berlin"
        ]
        
        for _ in range(20):  # Create 20 flights
            origin = rc(cities)
            destination = rc([city for city in cities if city != origin])
            
            # Generate random departure time within next 7 days
            departure_time = datetime.now(timezone.utc) + timedelta(
                days=randint(0, 7),
                hours=randint(0, 23),
                minutes=randint(0, 59)
            )
            
            # Flight duration between 1 and 12 hours
            duration = timedelta(hours=randint(1, 12))
            arrival_time = departure_time + duration
            
            flight = Flight(
                origin=origin,
                destination=destination,
                departure_time=departure_time,
                arrival_time=arrival_time
            )
            flights.append(flight)
            db.session.add(flight)
        
        db.session.commit()
        
        print("Creating users...")
        users = []
        for _ in range(3):  # Create 3 users
            user = User(
                username=fake.user_name(),
                email=fake.email(),
            )
            user.set_password("password123")  # Set a default password
            users.append(user)
            db.session.add(user)
        
        db.session.commit()
        
        print("Creating bookings...")
        for _ in range(30):  # Create 30 bookings
            user = rc(users)
            flight = rc(flights)
            airline = rc(airlines)
            
            # Generate random booking date in the past
            booking_date = datetime.now(timezone.utc) - timedelta(
                days=randint(1, 30),
                hours=randint(0, 23),
                minutes=randint(0, 59)
            )
            
            # Generate random price between 100 and 2000
            total_price = round(randint(100, 2000) + randint(0, 99) / 100, 2)
            
            booking = Booking(
                booking_date=booking_date,
                total_price=total_price,
                user_id=user.id,
                flight_id=flight.id,
                airline_id=airline.id
            )
            db.session.add(booking)
        
        db.session.commit()
        print("Seed completed!")
