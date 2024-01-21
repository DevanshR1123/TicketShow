from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import func
import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def __repr__(self) -> str:
        return f'<User {self.id} {self.first_name} {self.role}>'

    def get_id(self):
        return self.username

    def is_authenticated(self):
        return self.authenticated


class Venue(db.Model):
    __tablename__ = 'venue'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String)
    description = db.Column(db.String)
    rating = db.Column(db.Numeric(1))
    capacity = db.Column(db.Integer)

    scheduled_shows = db.relationship('ScheduledAt', viewonly=True,
                                      order_by="ScheduledAt.show_date_time")

    def __repr__(self) -> str:
        return f'<Venue {self.id} {self.name}>'


class Show(db.Model):
    __tablename__ = 'show'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String)
    description = db.Column(db.String)
    rating = db.Column(db.Numeric(1))
    ticket_price = db.Column(db.Numeric(2))

    tags = db.relationship('ShowTags', viewonly=True)
    scheduled_at = db.relationship('ScheduledAt', viewonly=True,
                                   order_by="ScheduledAt.show_date_time")

    def __repr__(self) -> str:
        return f'<Show {self.id} {self.name}>'


class ShowTags(db.Model):
    __tablename__ = 'show_tags'
    show_id = db.Column(db.Integer,
                        db.ForeignKey('show.id', ondelete="CASCADE"),
                        nullable=False, primary_key=True)
    tag = db.Column(db.String, primary_key=True)

    def __repr__(self) -> str:
        return self.tag


class ScheduledAt(db.Model):
    __tablename__ = 'scheduled_at'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    venue_id = db.Column(db.Integer,
                         db.ForeignKey('venue.id', ondelete="CASCADE"),
                         nullable=False)
    show_id = db.Column(db.Integer,
                        db.ForeignKey('show.id', ondelete="CASCADE"),
                        nullable=False)
    show_date_time = db.Column(db.DateTime, nullable=False)

    show = db.relationship('Show', viewonly=True)
    venue = db.relationship('Venue', viewonly=True)
    bookings = db.relationship('Booking', viewonly=True)

    upcoming = db\
        .column_property(show_date_time > datetime.datetime.now())

    @property
    def total_tickets(self):
        return db.session.query(func.sum(Booking.no_of_tickets))\
                         .filter(Booking.svd_id == self.id)\
                         .scalar() or 0

    @property
    def full(self):
        return self.venue.capacity <= self.total_tickets


class Booking(db.Model):
    __tablename__ = 'booking'
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id', ondelete="CASCADE"),
                        primary_key=True)
    svd_id = db.Column(db.Integer,
                       db.ForeignKey('scheduled_at.id', ondelete="CASCADE"),
                       primary_key=True)
    no_of_tickets = db.Column(db.Integer, default=1)

    ticket = db.relationship('ScheduledAt', viewonly=True,
                             order_by="ScheduledAt.show_date_time")
