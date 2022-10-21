"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

# dropping the db
os.system("dropdb ratings")

# creating the db
os.system('createdb ratings')

# connecting to the server
model.connect_to_db(server.app)

# creating all tables
model.db.create_all()

# open json file as f
with open('data/movies.json') as f:
    # loading file as a list of dictionaries
    movie_data = json.loads(f.read())


# Create movies, store them in list so we can use them
# to create fake ratings later
movies_in_db = []
for movie in movie_data:
    # TODO: get the title, overview, and poster_path from the movie
    title = movie["title"] 
    overview = movie["overview"]
    poster_path = movie["poster_path"]

    # dictionary. Then, get the release_date and convert it to a
    release_date = movie["release_date"]
    # format to datetime
    format = "%Y-%m-%d"
    # datetime object with datetime.strptime
    release_date = datetime.strptime(release_date, format)

    # TODO: create a movie here and append it to movies_in_db
    # if no crude file, could have done the code below?
    # new_movie = model.Movie(title=title, overview=overview, poster_path=poster_path, release_date=release_date)
    db_movie = crud.create_movie(title, overview, release_date, poster_path)
    movies_in_db.append(db_movie)

# add the movies into the db
model.db.session.add_all(movies_in_db)
model.db.session.commit()

# random movie rating: 
for n in range(10):
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'

    # TODO: create a user here
    user = crud.create_user(email, password)
    model.db.session.add(user)

    # TODO: create 10 ratings for the user
    for m in range(10):
        movie = choice(movies_in_db)
        score = randint(1,5)
        
        rating = crud.create_rating(score, movie, user)
        model.db.session.add(rating)

model.db.session.commit()