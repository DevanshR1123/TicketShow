import os
import io
import qrcode
import base64
from datetime import datetime, timedelta

from flask import Flask, redirect, render_template, request
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_restful import Api

from api import ShowAPI, VenueAPI
from models import User, db, Show, Venue, Booking, ScheduledAt, ShowTags

cwd = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
api = Api(app, prefix='/api')
login_manager = LoginManager(app)

app.secret_key = '9mwY7f-lEiSyHTXRX3nXMgyT98t5HRDnKxJaxTORbOo'
app.config['SECRET_KEY'] = '9mwY7f-lEiSyHTXRX3nXMgyT98t5HRDnKxJaxTORbOo'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(cwd, 'database.sqlite3')
db.init_app(app)
app.app_context().push()

db.create_all()

login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(username):
    return User.query.filter(User.username == username).first()


@app.template_filter('formatdate')
def date_format(d: datetime):
    return d.date().strftime('%d %b, %Y')


@app.template_filter('formattime')
def time_format(d: datetime):
    return d.time().strftime('%I:%M %p')


@app.template_filter('formatdatetime')
def datetime_format(d: datetime):
    return d.strftime('%d %b, %Y %I:%M %p')


@app.get('/')
def index():
    shows = db.session.query(Show)\
        .join(ScheduledAt)\
        .join(ShowTags, isouter=True)\
        .order_by(ScheduledAt.show_date_time)\
        .all()
    venues = Venue.query.all()

    return render_template('index.html', shows=shows, venues=venues)


@app.get('/shows')
def shows():
    upcoming_shows = db.session.query(Show)\
        .join(ShowTags, isouter=True)\
        .join(ScheduledAt, isouter=True)\
        .join(Venue, isouter=True)\
        .filter(ScheduledAt.upcoming)\
        .order_by(ScheduledAt.show_date_time)
    all_shows = db.session.query(Show)\
        .join(ShowTags, isouter=True)\
        .join(ScheduledAt, isouter=True)\
        .join(Venue, isouter=True)

    role = current_user.role if current_user.is_authenticated else None
    shows = upcoming_shows if role == 'user' else all_shows

    args = request.args

    if len(args) > 0:

        venue = args.get('venue')
        if venue != '':
            shows = shows.filter(Venue.name == venue)

        tag = args.get('tag')
        if tag != '':
            shows = shows.filter(ShowTags.tag == tag)

        rating = args.get('rating')
        shows = shows.filter(Venue.rating >= rating)

        date_from = args.get('date_from')
        if date_from:
            shows = shows\
                .filter(ScheduledAt.show_date_time >= datetime.fromisoformat(date_from))

        date_to = args.get('date_to')
        if date_to:
            shows = shows\
                .filter(ScheduledAt.show_date_time <= datetime.fromisoformat(date_to))

    shows = shows.all()
    venues = sorted(set([v.name for v in Venue.query.all()]))
    tags = sorted(set([t.tag for t in ShowTags.query.all()]))

    return render_template('shows.html', shows=shows, venues=venues, tags=tags)


@app.get('/venues')
def venues():
    venues = db.session.query(Venue)

    args = request.args

    if len(args) > 0:

        location = args.get('location')
        if location != '':
            venues = venues.filter(Venue.location == location)

        rating = args.get('rating')
        venues = venues.filter(Venue.rating >= rating)

    venues = venues.all()
    locations = sorted(set([v.location for v in Venue.query.all()]))
    return render_template('venues.html', venues=venues, locations=locations)


@app.get('/show/<int:id>')
def show(id):
    show = db.session.query(Show).get(id)
    upcoming = any([x.upcoming for x in show.scheduled_at])
    return render_template('show.html', show=show, upcoming=upcoming)


@app.get('/venue/<int:id>')
def venue(id):
    venue = db.session.query(Venue).get(id)
    upcoming = any([x.upcoming for x in venue.scheduled_shows])
    return render_template('venue.html', venue=venue, upcoming=upcoming)


@app.get('/show/edit/<int:id>')
@login_required
def edit_show_form(id):
    if (current_user.role != 'admin'):
        return redirect('/')
    show = db.session.query(Show).get(id)
    venues = Venue.query\
        .order_by(Venue.name)\
        .distinct()
    return render_template('edit_show.html', mode='edit', show=show, venues=venues)


@app.post('/show/edit/<int:id>')
@login_required
def edit_show(id):
    if (current_user.role != 'admin'):
        return redirect('/')
    show = db.session.query(Show).get(id)
    args = request.json

    ds = args.get('show')

    show.name = ds['name']
    show.description = ds['description']
    show.category = ds['category']
    show.rating = ds['rating']
    show.ticket_price = ds['ticket_price']

    etag = [x.tag for x in show.tags]
    for tag in ds['tags']:
        if tag not in etag:
            db.session.add(ShowTags(show_id=id, tag=tag))

    for x in args.get('schedule_remove'):
        s = db.session.query(ScheduledAt).get(int(x))
        db.session.delete(s)

    for x in args.get('schedule_add'):
        show_date_time = datetime\
            .strptime(x['show_date_time'], '%Y-%m-%dT%H:%M:%S.%fZ') \
            + timedelta(hours=5, minutes=30)
        db.session.add(ScheduledAt(show_id=id,
                                   venue_id=x['venue_id'],
                                   show_date_time=show_date_time))

    db.session.commit()

    return {'id': show.id}


@app.get('/show/add')
@login_required
def add_show_form():
    if (current_user.role != 'admin'):
        return redirect('/')
    venues = Venue.query\
        .order_by(Venue.name)\
        .distinct()
    return render_template('edit_show.html', mode='add', show={}, venues=venues)


@app.post('/show/add')
@login_required
def add_show():
    if (current_user.role != 'admin'):
        return redirect('/')
    show = Show()
    args = request.json

    ds = args.get('show')

    show.name = ds['name']
    show.description = ds['description']
    show.category = ds['category']
    show.rating = ds['rating']
    show.ticket_price = ds['ticket_price']

    db.session.add(show)
    db.session.commit()

    for tag in ds['tags']:
        db.session.add(ShowTags(show_id=show.id, tag=tag))

    for x in args.get('schedule_add'):
        show_date_time = datetime\
            .strptime(x['show_date_time'], '%Y-%m-%dT%H:%M:%S.%fZ') \
            + timedelta(hours=5, minutes=30)
        db.session.add(ScheduledAt(show_id=show.id,
                                   venue_id=x['venue_id'],
                                   show_date_time=show_date_time))

    db.session.commit()

    return {'id': show.id}


@app.get('/venue/edit/<int:id>')
@login_required
def edit_venue_form(id):
    if (current_user.role != 'admin'):
        return redirect('/')
    venue = db.session.query(Venue).get(id)
    return render_template('edit_venue.html', venue=venue, mode='edit')


@app.post('/venue/edit/<int:id>')
@login_required
def edit_venue(id):
    if (current_user.role != 'admin'):
        return redirect('/')
    venue = db.session.query(Venue).get(id)
    args = request.form

    venue.name = args['name']
    venue.description = args['description']
    venue.location = args['location']
    venue.rating = args['rating']
    venue.capacity = args['capacity']

    db.session.commit()

    return redirect(f'/venue/{id}')


@app.get('/venue/add')
@login_required
def add_venue_form():
    if (current_user.role != 'admin'):
        return redirect('/')
    return render_template('edit_venue.html', venue={}, mode='add')


@app.post('/venue/add')
@login_required
def add_venue():
    if (current_user.role != 'admin'):
        return redirect('/')
    venue = Venue()
    args = request.form

    venue.name = args['name']
    venue.description = args['description']
    venue.location = args['location']
    venue.rating = args['rating']
    venue.capacity = args['capacity']

    db.session.add(venue)
    db.session.commit()

    return redirect(f'/venue/{venue.id}')


@app.get('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.get('/profile/admin')
@login_required
def admin():
    if (current_user.role == 'admin'):
        return render_template('admin.html', shows=Show.query.all(), venues=Venue.query.all())
    else:
        return redirect('/profile')


@app.get('/tickets')
@login_required
def tickets():
    tickets = db.session\
        .query(Booking)\
        .filter(Booking.user_id == current_user.id)\
        .all()

    buffers = [io.BytesIO() for _ in tickets]
    qrs = [qrcode.make(f'{x.ticket.show.name} at {x.ticket.venue.name} on {x.ticket.show_date_time}')
           for x in tickets]

    for qr, buffer in zip(qrs, buffers):
        qr.save(buffer, "JPEG")

    encoded_qrs = [base64
                   .b64encode(x.getvalue())
                   .decode('utf-8')
                   for x in buffers]

    return render_template('tickets.html', tickets=list(zip(tickets, encoded_qrs)))


@app.get('/book/<int:id>')
@login_required
def booking_form(id):
    return render_template('book_ticket.html', scheduled_show=db.session.query(ScheduledAt).get(id))


@app.post('/book/<int:id>')
@login_required
def book_ticket(id):
    n_tickets = request.form.get('no_of_tickets')
    ticket = Booking(user_id=current_user.id,
                     svd_id=id, no_of_tickets=n_tickets)
    db.session.add(ticket)
    db.session.commit()
    return redirect('/tickets')


@app.post('/schedule')
def schedule_template():
    args = request.json
    venue = db.session.query(Venue).get(args.get('venue_id'))
    show_date_time = datetime\
        .strptime(args.get('show_date_time'), '%Y-%m-%dT%H:%M:%S.%fZ') \
        + timedelta(hours=5, minutes=30)

    shows = db.session.query(ScheduledAt)\
        .filter(ScheduledAt.venue_id == int(args.get('venue_id')))
    show_id = args.get('show_id')
    if show_id != '':
        shows = shows.filter(ScheduledAt.show_id == int(show_id))
    shows = shows.all()

    if any([x.show_date_time == show_date_time for x in shows]):
        return '', 400
    return render_template('scheduled_show.html', venue=venue, show_date_time=show_date_time)


@app.get('/signup')
def signup_form():
    return render_template('signup.html')


@app.post('/signup')
def signup():

    args = request.form

    if (db.session.query(User).filter(User.username == args.get('username')).first()):
        return render_template('signup.html', error='The entered username is taken.')

    if (db.session.query(User).filter(User.email == args.get('email')).first()):
        return render_template('signup.html', error='The entered email is associated with another account.')

    if (args.get('password') != args.get('password-confirm')):
        return render_template('signup.html', error='Please enter matching passwords!')

    user = User(
        first_name=args.get('first_name'),
        last_name=args.get('last_name'),
        username=args.get('username'),
        email=args.get('email'),
        password=args.get('password'),
        role='user',
        authenticated=False
    )

    db.session.add(user)
    db.session.commit()

    return render_template('login.html')


@app.get('/login')
def login_form():
    return render_template('login.html')


@app.post('/login')
def login():
    if not request.form:
        return {'message': 'send credentials to authenticate'}, 406

    info = request.form
    username = info.get('username', 'guest')
    password = info.get('password', '')

    user = User.query\
        .filter(User.username == username)\
        .filter(User.password == password)\
        .first()
    if user:
        user.authenticated = True
        login_user(user)
        return redirect('/')
    else:
        return render_template('login.html', error=True), 401


@app.route("/logout")
@login_required
def logout():
    logout_user()
    current_user.authenticated = False
    return redirect('/')


api.add_resource(ShowAPI, '/shows', '/shows/<int:id>', endpoint='api-shows')
api.add_resource(VenueAPI, '/venues', '/venues/<int:id>',
                 endpoint='api-venues')


if __name__ == "__main__":
    app.run(debug=True)
