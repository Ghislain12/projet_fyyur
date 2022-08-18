#ici c'est models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String())
    state = db.Column(db.String())
    address = db.Column(db.String())
    phone = db.Column(db.String())
    genres = db.Column(db.String())
    facebook_link = db.Column(db.String())
    image_link = db.Column(db.String())
    website_link = db.Column(db.String())
    seeking_talent = db.Column(db.Boolean, default=False, nullable=False)
    seeking_description = db.Column(db.String())
    shows = db.relationship('Show', backref='Venue',
                            lazy=True, cascade="all,delete")

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    city = db.Column(db.String())
    state = db.Column(db.String())
    phone = db.Column(db.String())
    image_link = db.Column(db.String())
    genres = db.Column(db.String())
    facebook_link = db.Column(db.String())
    website_link = db.Column(db.String())
    seeking_venue = db.Column(db.Boolean, default=False, nullable=False)
    seeking_description = db.Column(db.String())
    shows = db.relationship('Show', backref='artist',
                            lazy=True, cascade="all,delete")

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Show(db.Model):
    __tablename__ = 'show'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.String())
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
