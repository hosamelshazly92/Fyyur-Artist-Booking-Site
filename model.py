# Imports
#----------------------------------------------------------------------------#

import sys
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_migrate import Migrate
from flask import abort
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO_DONE: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Show(db.Model):
  __tablename__ = 'show'

  id = db.Column(db.Integer, primary_key=True) 
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id')) 
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
  start_time = db.Column(db.DateTime)

  venue = db.relationship("Venue")

  def __repr__(self):
    return f'<Show ID: {self.id}, Start Time: {self.start_time}>'

# association parent table (left)
class Artist(db.Model):
  __tablename__ = 'artist'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  image_link = db.Column(db.String(500))
  website = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  address = db.Column(db.String(120))
  genres = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  seeking_venue = db.Column(db.Boolean)
  seeking_description = db.Column(db.String(500))
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))

  venues = db.relationship("Show", backref="artist", lazy=True)
  albums = db.relationship("Album", backref="artist", lazy=True)

  def __repr__(self):
    return f'<Artist ID: {self.id}, Name: {self.name}>'

  # TODO_DONE: implement any missing fields, as a database migration using Flask-Migrate

# association child table (right)
class Venue(db.Model):
  __tablename__ = 'venue'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  address = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  website = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  genres = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  seeking_talent = db.Column(db.Boolean)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))

  def __repr__(self):
    return f'<Venue ID: {self.id}, Name: {self.name}, No. Events: {self.num_upcoming_shows}>'

  # TODO_DONE: implement any missing fields, as a database migration using Flask-Migrate

# TODO_DONE Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#

# albums
class Album(db.Model):
  __tablename__ = 'album'

  id = db.Column(db.Integer, primary_key=True)
  album = db.Column(db.String(150))
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))

  songs = db.relationship("Song", backref="album", lazy=True)

  def __repr__(self):
    return f'Album: {self.album}, Artist ID: {self.artist_id}'

# songs
class Song(db.Model):
  __tablename__ = 'song'

  id = db.Column(db.Integer, primary_key=True)
  song = db.Column(db.String(150))
  album_id = db.Column(db.Integer, db.ForeignKey('album.id'))

  def __repr__(self):
    return f'Song: {self.song}, Album ID: {self.album_id}'