#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask_migrate import Migrate
from models import *


import json
import os
import sys
import dateutil.parser
import babel
import datetime
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import date
from dateutil import parser
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)


# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# class Venue(db.Model):
#     __tablename__ = 'venue'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     city = db.Column(db.String())
#     state = db.Column(db.String())
#     address = db.Column(db.String())
#     phone = db.Column(db.String())
#     genres = db.Column(db.String())
#     facebook_link = db.Column(db.String())
#     image_link = db.Column(db.String())
#     website_link = db.Column(db.String())
#     seeking_talent = db.Column(db.Boolean, default=False, nullable=False)
#     seeking_description = db.Column(db.String())
#     shows = db.relationship('Show', backref='Venue',
#                             lazy=True, cascade="all,delete")

#     # TODO: implement any missing fields, as a database migration using Flask-Migrate


# class Artist(db.Model):
#     __tablename__ = 'artist'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String())
#     city = db.Column(db.String())
#     state = db.Column(db.String())
#     phone = db.Column(db.String())
#     image_link = db.Column(db.String())
#     genres = db.Column(db.String())
#     facebook_link = db.Column(db.String())
#     website_link = db.Column(db.String())
#     seeking_venue = db.Column(db.Boolean, default=False, nullable=False)
#     seeking_description = db.Column(db.String())
#     shows = db.relationship('Show', backref='artist',
#                             lazy=True, cascade="all,delete")

#     # TODO: implement any missing fields, as a database migration using Flask-Migrate


# class Show(db.Model):
#     __tablename__ = 'show'

#     id = db.Column(db.Integer, primary_key=True)
#     start_time = db.Column(db.String())
#     artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
#     venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))

# class Area(db.Model):
#     __tablename__ = 'area'
#     id = db.Column(db.Integer, primary_key=True)
#     start_time = db.Column(db.String)
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    elif format == 'short':
        format = 'yyyy, mm, dd'
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

def dispatch(datas, cities):
    areas = []
    for city in cities:
        results = []
        for data in datas:
            if city == data.city:
                results.append(data)
        areas.append({
            "city": city,
            "state": results[0].state,
            "venues": results})
    return areas


@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    data = [{
        "city": "San Francisco",
        "state": "CA",
        "venues": [{
            "id": 1,
            "name": "The Musical Hop",
            "num_upcoming_shows": 0,
        }, {
            "id": 3,
            "name": "Park Square Live Music & Coffee",
            "num_upcoming_shows": 1,
        }]
    }, {
        "city": "New York",
        "state": "NY",
        "venues": [{
            "id": 2,
            "name": "The Dueling Pianos Bar",
            "num_upcoming_shows": 0,
        }]
    }]

    data = Venue.query.all()
    data1 = db.session.query(Venue.city).distinct().all()
    cities = [Cities.city for Cities in data1]
    return render_template('pages/venues.html', areas=dispatch(data, cities))


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    response = {
        "count": 1,
        "data": [{
            "id": 2,
            "name": "The Dueling Pianos Bar",
            "num_upcoming_shows": 0,
        }]
    }

    search_term = request.form.get('search_term', '')
    search = "%{}%".format(search_term)
    res = {
        "count": db.session.query(func.count(Venue.id).filter(Venue.name.ilike(search))).scalar(),
        "data": db.session.query(Venue.name.label('name'), Venue.id.label('id')).filter(Venue.name.ilike(search)).all()
    }
    return render_template('pages/search_venues.html', results=res, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:id>')
def show_venue(id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    # data1 = {
    #     "id": 1,
    #     "name": "The Musical Hop",
    #     "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    #     "address": "1015 Folsom Street",
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "phone": "123-123-1234",
    #     "website": "https://www.themusicalhop.com",
    #     "facebook_link": "https://www.facebook.com/TheMusicalHop",
    #     "seeking_talent": True,
    #     "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    #     "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    #     "past_shows": [{
    #         "artist_id": 4,
    #         "artist_name": "Guns N Petals",
    #         "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    #         "start_time": "2019-05-21T21:30:00.000Z"
    #     }],
    #     "upcoming_shows": [],
    #     "past_shows_count": 1,
    #     "upcoming_shows_count": 0,
    # }
    # data2 = {
    #     "id": 2,
    #     "name": "The Dueling Pianos Bar",
    #     "genres": ["Classical", "R&B", "Hip-Hop"],
    #     "address": "335 Delancey Street",
    #     "city": "New York",
    #     "state": "NY",
    #     "phone": "914-003-1132",
    #     "website": "https://www.theduelingpianos.com",
    #     "facebook_link": "https://www.facebook.com/theduelingpianos",
    #     "seeking_talent": False,
    #     "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    #     "past_shows": [],
    #     "upcoming_shows": [],
    #     "past_shows_count": 0,
    #     "upcoming_shows_count": 0,
    # }
    # data3 = {
    #     "id": 3,
    #     "name": "Park Square Live Music & Coffee",
    #     "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    #     "address": "34 Whiskey Moore Ave",
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "phone": "415-000-1234",
    #     "website": "https://www.parksquarelivemusicandcoffee.com",
    #     "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    #     "seeking_talent": False,
    #     "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #     "past_shows": [{
    #         "artist_id": 5,
    #         "artist_name": "Matt Quevedo",
    #         "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    #         "start_time": "2019-06-15T23:00:00.000Z"
    #     }],
    #     "upcoming_shows": [{
    #         "artist_id": 6,
    #         "artist_name": "The Wild Sax Band",
    #         "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #         "start_time": "2035-04-01T20:00:00.000Z"
    #     }, {
    #         "artist_id": 6,
    #         "artist_name": "The Wild Sax Band",
    #         "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #         "start_time": "2035-04-08T20:00:00.000Z"
    #     }, {
    #         "artist_id": 6,
    #         "artist_name": "The Wild Sax Band",
    #         "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #         "start_time": "2035-04-15T20:00:00.000Z"
    #     }],
    #     "past_shows_count": 1,
    #     "upcoming_shows_count": 1,
    # }
    # data = list(filter(lambda d: d['id'] ==
    #             venue_id, [data1, data2, data3]))[0]
    data = Venue.query.get_or_404(id)

    shows = db.session.query(Show).filter_by(venue_id=id).all()
    past_shows = []
    past_shows_data = []

    upcoming_shows = []
    upcoming_show_data = []

    for show in shows:
        if parser.parse(show.start_time) <= datetime.now():
            past_shows.append(show)
        if datetime.timestamp(parser.parse(show.start_time)) > datetime.timestamp(datetime.now()):
            upcoming_shows.append(show)

    for show in past_shows:
        # print(show.venue_id)
        artist = Artist.query.get(show.artist_id)

        d = {
            'artist_id': artist.id,
            'artist_name': artist.name,
            'artist_image_link': artist.image_link,
            "start_time": show.start_time
        }
        past_shows_data.append(d)

    for show in upcoming_shows:
        # print(show.venue_id)
        artist = Artist.query.get(show.artist_id)

        d = {
            'artist_id': artist.id,
            'artist_name': artist.name,
            'artist_image_link': artist.image_link,
            "start_time": show.start_time
        }
        upcoming_show_data.append(d)


    genre = data.genres
    a = "".join(map(str, genre))
    a = a.split(",")
    b = a[0]
    b = b[1:]
    a[0] = b
    c = a[-1]
    c = c[:-1]
    a[-1] = c
    genre = a

    resultat = {
        "id": data.id,
        "name": data.name,
        "genres": genre,
        "city": data.city,
        "state": data.state,
        "phone": data.phone,
        "seeking_talent": data.seeking_talent,
        "image_link": data.image_link,
        "past_shows": past_shows_data,
        "upcoming_shows": upcoming_show_data,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template('pages/show_venue.html', venue=resultat)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    error = False
    # body = {}
    try:
        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')
        address = request.form.get('address')
        phone = request.form.get('phone')
        image_link = request.form.get('image_link')
        genres = request.form.getlist('genres')
        facebook_link = request.form.get('facebook_link')
        website_link = request.form.get('website_link')
        seeking_talent = request.form.get('seeking_talent')
        seeking_description = request.form.get('seeking_description')

        if seeking_talent == 'y':
            seeking_talent = True
        venue = Venue(
            name=name,
            city=city,
            state=state,
            address=address,
            phone=phone,
            image_link=image_link,
            genres=genres,
            facebook_link=facebook_link,
            website_link=website_link,
            seeking_talent=seeking_talent,
            seeking_description=seeking_description
        )
        db.session.add(venue)
        db.session.commit()
        # body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        os.abort()
    else:
        #   return jsonify(body)
        # # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.route('/venues/<id>/delete')
def delete_venue(id):
    error = False
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage

    venue = Venue.query.get_or_404(id)
    try:
        db.session.delete(venue)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        os.abort()
    else:
        flash('Venue ' + venue.name + ' was successfully removed!')
        return render_template('pages/home.html')
#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    data = [{
        "id": 4,
        "name": "Guns N Petals",
    }, {
        "id": 5,
        "name": "Matt Quevedo",
    }, {
        "id": 6,
        "name": "The Wild Sax Band",
    }]
    return render_template('pages/artists.html', artists=Artist.query.all())


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    response = {
        "count": 1,
        "data": [{
            "id": 4,
            "name": "Guns N Petals",
            "num_upcoming_shows": 0,
        }]
    }

    search_term = request.form.get('search_term', '')
    search = "%{}%".format(search_term)
    res = {
        "count": db.session.query(func.count(Artist.id).filter(Artist.name.ilike(search))).scalar(),
        "data": db.session.query(Artist.name.label('name'), Artist.id.label('id')).filter(Artist.name.ilike(search)).all()
    }
    return render_template('pages/search_artists.html', results=res, search_term=search_term)


@app.route('/artists/<int:id>')
def show_artist(id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id
    data1 = {
        "id": 4,
        "name": "Guns N Petals",
        "genres": ["Rock n Roll"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "326-123-5000",
        "website": "https://www.gunsnpetalsband.com",
        "facebook_link": "https://www.facebook.com/GunsNPetals",
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        "past_shows": [{
            "venue_id": 1,
            "venue_name": "The Musical Hop",
            "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
            "start_time": "2019-05-21T21:30:00.000Z"
        }],
        "upcoming_shows": [],
        "past_shows_count": 1,
        "upcoming_shows_count": 0,
    }
    data2 = {
        "id": 5,
        "name": "Matt Quevedo",
        "genres": ["Jazz"],
        "city": "New York",
        "state": "NY",
        "phone": "300-400-5000",
        "facebook_link": "https://www.facebook.com/mattquevedo923251523",
        "seeking_venue": False,
        "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        "past_shows": [{
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
            "start_time": "2019-06-15T23:00:00.000Z"
        }],
        "upcoming_shows": [],
        "past_shows_count": 1,
        "upcoming_shows_count": 0,
    }
    data3 = {
        "id": 6,
        "name": "The Wild Sax Band",
        "genres": ["Jazz", "Classical"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "432-325-5432",
        "seeking_venue": False,
        "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "past_shows": [],
        "upcoming_shows": [{
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
            "start_time": "2035-04-01T20:00:00.000Z"
        }, {
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
            "start_time": "2035-04-08T20:00:00.000Z"
        }, {
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
            "start_time": "2035-04-15T20:00:00.000Z"
        }],
        "past_shows_count": 0,
        "upcoming_shows_count": 3,
    }
    data = Artist.query.get_or_404(id)

    shows = db.session.query(Show).filter_by(artist_id=id).all()
    past_shows = []
    past_shows_data = []

    upcoming_shows = []
    upcoming_show_data = []

    for show in shows:
        if parser.parse(show.start_time) <= datetime.now():
            past_shows.append(show)
        if datetime.timestamp(parser.parse(show.start_time)) > datetime.timestamp(datetime.now()):
            upcoming_shows.append(show)

    for show in past_shows:
        # print(show.venue_id)
        venue = Venue.query.get(show.venue_id)

        d = {
            'venue_id': venue.id,
            'venue_name': venue.name,
            'venue_image_link': venue.image_link,
            "start_time": show.start_time
        }
        past_shows_data.append(d)

    for show in upcoming_shows:
        # print(show.venue_id)
        venue = Venue.query.get(show.venue_id)

        d = {
            'venue_id': venue.id,
            'venue_name': venue.name,
            'venue_image_link': venue.image_link,
            "start_time": show.start_time
        }
        upcoming_show_data.append(d)

    genre = data.genres
    a = "".join(map(str, genre))
    a = a.split(",")
    b = a[0]
    b = b[1:]
    a[0] = b
    c = a[-1]
    c = c[:-1]
    a[-1] = c
    genre = a

    resultat = {
        "id": data.id,
        "name": data.name,
        "genres": genre,
        "city": data.city,
        "state": data.state,
        "phone": data.phone,
        "seeking_venue": data.seeking_venue,
        "image_link": data.image_link,
        "past_shows": past_shows_data,
        "upcoming_shows": upcoming_show_data,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }
    return render_template('pages/show_artist.html', artist=resultat)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:id>/edit', methods=['GET'])
def edit_artist(id):
    form = ArtistForm()
    # artist = {
    #     "id": 4,
    #     "name": "Guns N Petals",
    #     "genres": ["Rock n Roll"],
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "phone": "326-123-5000",
    #     "website": "https://www.gunsnpetalsband.com",
    #     "facebook_link": "https://www.facebook.com/GunsNPetals",
    #     "seeking_venue": True,
    #     "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    #     "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
    # }
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=Artist.query.get_or_404(id))


@app.route('/artists/<int:id>/edit', methods=['POST'])
def edit_artist_submission(id):
    error = False

    artist = Artist.query.get_or_404(id)

    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.image_link = request.form['image_link']
    artist.genres = request.form.getlist('genres')
    artist.facebook_link = request.form['facebook_link']
    artist.website_link = request.form['website_link']
    artist.seeking_venue = 0
    artist.seeking_description = request.form['seeking_description']

    try:
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        os.abort()
    else:
        # TODO: take values from the form submitted, and update existing
        # artist record with ID <artist_id> using the new attributes

        return redirect(url_for('show_artist', id=id))


@app.route('/venues/<int:id>/edit', methods=['GET'])
def edit_venue(id):
    form = VenueForm()
    # venue = {
    #     "id": 1,
    #     "name": "The Musical Hop",
    #     "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    #     "address": "1015 Folsom Street",
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "phone": "123-123-1234",
    #     "website": "https://www.themusicalhop.com",
    #     "facebook_link": "https://www.facebook.com/TheMusicalHop",
    #     "seeking_talent": True,
    #     "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    #     "image_link": "https:   //images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    # }
    venue = Venue.query.get_or_404(id)

    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:id>/edit', methods=['POST'])
def edit_venue_submission(id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    error = False

    venue = Venue.query.get_or_404(id)

    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.phone = request.form['phone']
    venue.image_link = request.form['image_link']
    venue.genres = request.form.getlist('genres')
    venue.facebook_link = request.form['facebook_link']
    venue.website_link = request.form['website_link']
    venue.seeking_talent = 0
    venue.seeking_description = request.form['seeking_description']

    try:
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        os.abort()
    else:
        # TODO: take values from the form submitted, and update existing
        # artist record with ID <artist_id> using the new attributes

        return redirect(url_for('show_venue', id=id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    form = ArtistForm(request.form)
    error = False
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    phone = request.form.get('phone')
    image_link = request.form.get('image_link')
    genres = request.form.getlist('genres')
    facebook_link = request.form.get('facebook_link')
    website_link = request.form.get('website_link')
    seeking_venue = request.form.get('seeking_venue')
    seeking_description = request.form.get('seeking_description')

    if seeking_venue == 'y':
        seeking_venue = True

    if form.validate():
        try:
            artist = Artist(
                name=name,
                city=city,
                state=state,
                phone=phone,
                image_link=image_link,
                genres=genres,
                facebook_link=facebook_link,
                website_link=website_link,
                seeking_venue=seeking_venue,
                seeking_description=seeking_description
            )
            db.session.add(artist)
            db.session.commit()
        # body['description'] = todo.description
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()
        if error:
            os.abort()
        else:
            #   return jsonify(body)
            # on successful db insert, flash success
            flash('Artist ' + request.form['name'] +
                  ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    data = [{
        "venue_id": 1,
        "venue_name": "The Musical Hop",
        "artist_id": 4,
        "artist_name": "Guns N Petals",
        "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        "start_time": "2019-05-21T21:30:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 5,
        "artist_name": "Matt Quevedo",
        "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        "start_time": "2019-06-15T23:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-01T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-08T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-15T20:00:00.000Z"
    }]
    # start_time = Show.start_time
    # artist_id = Artist.id
    # artist_name = Artist.name
    # artist_image_link = Artist.image_link
    # data = db.session.query(Show).filter(Artist.id == artist_id).all()

    data = db.session.query(Show.start_time.label('start_time'), Artist.name.label('artist_name'), Artist.id.label('artist_id'), Artist.image_link.label(
        'artist_image_link'), Venue.id.label('venue_id'), Venue.name.label('venue_name')).join(Artist, Artist.id == Show.artist_id).join(Venue, Venue.id == Show.venue_id).all()

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    error = False
    try:
        artist_id = request.form['artist_id']
        venue_id = request.form['venue_id']
        start_time = format_datetime(request.form['start_time'])

        show = Show(
            artist_id=artist_id,
            venue_id=venue_id,
            start_time=start_time
        )
        db.session.add(show)
        db.session.commit()
        # body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        os.abort()
    else:
        # on successful db insert, flash success
        flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    app.config['FLASK_DEBUG'] = True
