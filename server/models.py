from datetime import datetime, timezone
from config import db, bcrypt, ma
from marshmallow import post_load


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)

    # flights = db.relationship('Flight', secondary='bookings', viewonly=True)
    # airlines = db.relationship('Airline', secondary='bookings', viewonly=True)
    bookings = db.relationship('Booking', backref='user', lazy=True)

    def set_password(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))  

    def __repr__(self):
        return f"<User {self.name}>"  
    

class Flight(db.Model):
    __tablename__ = 'flights'

    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)

    bookings = db.relationship('Booking', backref='flight', lazy=True)

    def __repr__(self):
        return f"<Flight from {self.origin} to {self.destination}>"

class Airline(db.Model):
    __tablename__ = 'airlines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)

    bookings = db.relationship('Booking', backref='airline', lazy=True)

    def __repr__(self):
        return f"<Airline {self.name} of {self.country}>"

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    total_price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'), nullable=False)
    airline_id = db.Column(db.Integer, db.ForeignKey('airlines.id'), nullable=False)

    def __repr__(self):
        return f"<Booking from {self.booking_date} to {self.total_price}>"

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ('_password_hash', 'bookings')
        include_fk = True

    password = ma.String(load_only=True)

    @post_load
    def make_user(self, data, **kwargs):
        if 'password' in data:
            user = User(
                username=data['username'],
                email=data['email']
            )
            user.set_password(data['password'])
            return user
        return User(**data)

class AirlineSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Airline
        load_instance = True
        include_fk = True
        exclude = ('bookings',)

class FlightSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Flight
        load_instance = True
        include_fk = True
        exclude = ('bookings',)

class BookingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Booking
        load_instance = True
        include_fk = True

    user = ma.Nested(UserSchema)
    flight = ma.Nested(FlightSchema)
    airline = ma.Nested(AirlineSchema)

