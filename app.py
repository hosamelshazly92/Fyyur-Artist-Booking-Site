#----------------------------------------------------------------------------#
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
from flask_wtf import FlaskForm
from forms import *
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

# association table
# show = db.Table('show',
#   db.Column('id', db.Integer, primary_key=True), 
#   db.Column('artist_id', db.Integer, db.ForeignKey('artist.id')), 
#   db.Column('venue_id', db.Integer, db.ForeignKey('venue.id')),
#   db.Column('start_time', db.DateTime)
# )

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
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))

  venues = db.relationship("Show", backref="artist")

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
  seeking_talent = db.Column(db.String(120))
  seeking_description = db.Column(db.String(500))
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  num_upcoming_shows = db.Column(db.Integer, default=0)

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
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO_DONE: replace with real venues data.
  area = db.session.query(Venue.city, Venue.state).distinct()
  venue = db.session.query(Venue)

  return render_template('pages/venues.html', venues=venue, areas=area)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO_DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
  term = request.form.get('search_term', '')
  data = Venue.query.filter(Venue.name.ilike('%' + term + '%')).all()
  count = Venue.query.filter(Venue.name.ilike('%' + term + '%')).count()

  return render_template('pages/search_venues.html', results=data, count=count, search_term=term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # TODO_DONE: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  show = Show.query.join(Venue).filter(Venue.id==venue_id).all()

  upcoming = 0
  past = 0
  for i in show:
    if (i.start_time > datetime.now()):
      upcoming += 1
    else:
      past += 1
  # print(f'==========> Upcoming: {upcoming}, Past: {past}')

  return render_template('pages/show_venue.html', venues=venue, shows=show, upcoming_shows_count=upcoming, past_shows_count=past, now=datetime.now())

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():    
  error = False
  try:
    get_name = request.form.get('name')
    get_city = request.form.get('city')
    get_state = request.form.get('state')
    get_address = request.form.get('address')
    get_phone = request.form.get('phone')
    get_image_link = request.form.get('image_link')
    get_genres = request.form.getlist('genres')
    get_facebook_link = request.form.get('facebook_link')

    venue_new = Venue(name=get_name, city=get_city, state=get_state, address=get_address, phone=get_phone, image_link=get_image_link, genres=get_genres, facebook_link=get_facebook_link)

    db.session.add(venue_new)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    # if form.validate_on_submit():
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/home.html')

  # TODO_DONE: insert form data as a new Venue record in the db, instead
  # TODO_DONE: modify data to be the data object returned from db insertion

  # TODO_DONE: on unsuccessful db insert, flash an error instead.

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO_DONE: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = False
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    return jsonify({'success': True})

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO_DONE: replace with real data returned from querying the database
  artist = Artist.query.order_by(Artist.id).all()

  return render_template('pages/artists.html', artists=artist)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO_DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
  term = request.form.get('search_term', '')
  data = Artist.query.filter(Artist.name.ilike('%' + term + '%')).all()
  count = Artist.query.filter(Artist.name.ilike('%' + term + '%')).count()

  return render_template('pages/search_artists.html', results=data, count=count, search_term=term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO_DONE: replace with real venue data from the venues table, using venue_id

  artist = Artist.query.get(artist_id)
  show = Show.query.select_from(Artist).filter(Show.artist_id==artist_id).all()

  upcoming = 0
  past = 0
  for i in show:
    if (i.start_time > datetime.now()):
      upcoming += 1
    else:
      past += 1
  # print(f'==========> Upcoming: {upcoming}, Past: {past}')

  return render_template('pages/show_artist.html', artists=artist, shows=show, upcoming_shows_count=upcoming, past_shows_count=past, now=datetime.now())

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)

  # TODO_DONE: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  error = False
  try:
    get_name = request.form.get('name')
    get_city = request.form.get('city')
    get_state = request.form.get('state')
    get_address = request.form.get('address')
    get_phone = request.form.get('phone')
    get_image_link = request.form.get('image_link')
    get_genres = request.form.getlist('genres')
    get_facebook_link = request.form.get('facebook_link')

    artist = Artist.query.get(artist_id)

    artist.name = get_name
    artist.city = get_city
    artist.state = get_state
    artist.address = get_address
    artist.phone = get_phone
    artist.image_link = get_image_link
    artist.genres = get_genres
    artist.facebook_link = get_facebook_link

    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    return redirect(url_for('show_artist', artist_id=artist_id))
  # TODO_DONE: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  
  # TODO_DONE: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  error = False
  try:
    get_name = request.form.get('name')
    get_city = request.form.get('city')
    get_state = request.form.get('state')
    get_address = request.form.get('address')
    get_phone = request.form.get('phone')
    get_image_link = request.form.get('image_link')
    get_genres = request.form.getlist('genres')
    get_facebook_link = request.form.get('facebook_link')

    venue = Venue.query.get(venue_id)

    venue.name = get_name
    venue.city = get_city
    venue.state = get_state
    venue.address = get_address
    venue.phone = get_phone
    venue.image_link = get_image_link
    venue.genres = get_genres
    venue.facebook_link = get_facebook_link

    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    return redirect(url_for('show_venue', venue_id=venue_id))
  # TODO_DONE: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()

  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  error = False
  try:
    get_name = request.form.get('name')
    get_city = request.form.get('city')
    get_state = request.form.get('state')
    get_address = request.form.get('address')
    get_phone = request.form.get('phone')
    get_image_link = request.form.get('image_link')
    get_genres = request.form.getlist('genres')
    get_facebook_link = request.form.get('facebook_link')

    artist_new = Artist(name=get_name, city=get_city, state=get_state, address=get_address, phone=get_phone, image_link=get_image_link, genres=get_genres, facebook_link=get_facebook_link)

    db.session.add(artist_new)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    # if form.validate_on_submit():
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/home.html')
  # TODO_DONE: insert form data as a new Venue record in the db, instead
  # TODO_DONE: modify data to be the data object returned from db insertion

  # TODO_DONE: on unsuccessful db insert, flash an error instead.

#  Delete
#  ----------------------------------------------------------------

@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
  error = False
  try:
    Artist.query.filter_by(id=artist_id).delete()
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    return jsonify({'success': True})

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # TODO_DONE: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  show = Show.query.all()

  return render_template('pages/shows.html', shows=show)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # TODO_DONE: insert form data as a new Show record in the db, instead

  error = False
  try:
    artist_id = request.form.get('artist_id')
    artist = Artist.query.get(artist_id)

    start_time = request.form.get('start_time')
    show = Show(start_time=start_time)

    venue_id = request.form.get('venue_id')
    show.venue = Venue.query.get(venue_id)

    artist.venues.append(show)

    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    # if form.validate_on_submit():
    flash('Show was successfully listed!')
    return render_template('pages/home.html')  
    # TODO_DONE: on unsuccessful db insert, flash an error instead.
  

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
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
    app.run(debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
