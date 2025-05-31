from datetime import datetime, timezone
from sqlalchemy.ext.hybrid import hybrid_property
from config import db, bcrypt, ma


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)

    flights = db.relationship('Flight', secondary='bookings', viewonly=True)
    airlines = db.relationship('Airline', secondary='bookings', viewonly=True)

    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self.password_hash, password.encode('utf-8'))

class Flight(db.Model):
    __tablename__ = 'flights'

    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)

    bookings = db.relationship('Booking', backref='flight', lazy=True)

class Airline(db.Model):
    __tablename__ = 'airlines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)

    bookings = db.relationship('Booking', backref='airline', lazy=True)

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    total_price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'), nullable=False)
    airline_id = db.Column(db.Integer, db.ForeignKey('airlines.id'), nullable=False)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ('password',)

class AirlineSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Airline
        load_instance = True

class FlightSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Flight
        load_instance = True


class BookingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Booking
        load_instance = True
        include_fk = True

    user = ma.Nested(UserSchema)
    flight = ma.Nested(FlightSchema)
    airline = ma.Nested(AirlineSchema)

