"""CRUD operations."""

from model import db, User, Movie, Rating, connect_to_db


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user


def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie."""

    movie = Movie(title=title, overview=overview, release_date=release_date, poster_path=poster_path)

    return movie

def get_all_movies():
    """Return all movies"""

    return Movie.query.all()

def get_movie_by_id(movie_id):
    """Returns movie by id num"""

    return Movie.query.get(movie_id)

def get_all_users():
    """Return all users"""

    return User.query.all()

def get_user_by_id(user_id):
    """Returns user profiles"""

    return User.query.get(user_id)

def get_user_by_email(user_email):
    """Return a user by email"""
    
    return User.query.filter(User.email == user_email).first()

def create_rating(score, movie, user):
    """Create and return a new rating."""
    
    rating = Rating(score=score, movie=movie, user=user)

    return rating

if __name__ == '__main__':
    from server import app
    connect_to_db(app)