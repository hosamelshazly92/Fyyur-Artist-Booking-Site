from model import *
from forms import *

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
  form = VenueForm()
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
    get_seeking_description = request.form.get('seeking_description')

    artist = Artist.query.get(artist_id)

    artist.name = get_name
    artist.city = get_city
    artist.state = get_state
    artist.address = get_address
    artist.phone = get_phone
    artist.image_link = get_image_link
    artist.genres = get_genres
    artist.facebook_link = get_facebook_link
    artist.seeking_description = get_seeking_description

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
