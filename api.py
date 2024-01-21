from flask_restful import Resource, marshal_with, fields, reqparse, request
from flask import redirect, render_template
from datetime import datetime

from models import db, User, Show, Venue, ScheduledAt, ShowTags

show_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'category': fields.String,
    'rating': fields.Integer,
    'ticket_price': fields.Float,
    'tags': fields.List(fields.String)
}

show_parser = reqparse.RequestParser()
show_parser.add_argument('name', location='form')
show_parser.add_argument('description', location='form')
show_parser.add_argument('category', location='form')
show_parser.add_argument('rating', type=int, location='form')
show_parser.add_argument('ticket_price', type=float, location='form')
show_parser.add_argument('tags', location='form')

venue_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'location': fields.String,
    'rating': fields.Integer,
    'capacity': fields.Integer
}

venue_parser = reqparse.RequestParser()
venue_parser.add_argument('name')
venue_parser.add_argument('description')
venue_parser.add_argument('location')
venue_parser.add_argument('rating', type=int)
venue_parser.add_argument('capacity', type=int)


class ShowAPI(Resource):

    @marshal_with(show_fields)
    def get(self, id=None):
        if id:
            shows = Show.query.get_or_404(id, description='Show id not found')
        else:
            shows = Show.query.all()
        return shows

    @marshal_with(show_fields)
    def post(self):

        args = show_parser.parse_args()
        show = Show(
            name=args['name'],
            description=args['description'],
            category=args['category'],
            ticket_price=args['ticket_price'],
            rating=args['rating'],
        )
        db.session.add(show)
        db.session.commit()

        tags = args['tags'].split(',')

        for tag in tags:
            db.session.add(ShowTags(show_id=show.id, tag=tag))

        db.session.commit()

        return show

    @marshal_with(show_fields)
    def put(self, id):

        args = show_parser.parse_args()
        show = db.session.query(Show)\
            .get_or_404(id, description='Show id not found')
        show.name = args['name']
        show.description = args['description']
        show.category = args['category']
        show.ticket_price = args['ticket_price']
        show.rating = args['rating']
        db.session.add(show)
        db.session.commit()

        tags = args['tags'].split(',')

        etag = [x.tag for x in show.tags]
        for tag in tags:
            if tag not in etag:
                db.session.add(ShowTags(show_id=id, tag=tag))

        db.session.commit()

        return show

    def delete(self, id):
        show = Show.query.get_or_404(id, description='Show id not found')
        db.session.delete(show)
        db.session.commit()
        return ''


class VenueAPI(Resource):

    @marshal_with(venue_fields)
    def get(self, id=None):
        if id:
            venues = Venue.query\
                .get_or_404(id, description='Venue id not found')
        else:
            venues = Venue.query.all()
        return venues

    def post(self):

        args = venue_parser.parse_args()
        venue = Venue(
            name=args['name'],
            description=args['description'],
            location=args['location'],
            rating=args['rating'],
            capacity=args['capacity']
        )

        db.session.add(venue)
        db.session.commit()

        return venue

    def put(self, id):

        args = venue_parser.parse_args()
        venue = db.session.query(Venue)\
            .get_or_404(id, description='Venue id not found')
        venue.name = args['name'],
        venue.description = args['description'],
        venue.location = args['location'],
        venue.rating = args['rating'],
        venue.capacity = args['capacity']

        db.session.add(venue)
        db.session.commit()

        return venue

    def delete(self, id):
        venue = Venue.query.get_or_404(id, description='Venue id not found')
        db.session.delete(venue)
        db.session.commit()
        return ''
