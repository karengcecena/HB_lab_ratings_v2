"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# Replace this with routes and view functions!
@app.route("/")
def homepage():
    """View homepage."""

    return render_template("homepage.html")

@app.route("/movies")
def view_movies():
    """View all movies"""
    
    movies = crud.get_all_movies()

    return render_template("all_movies.html", movies=movies)

@app.route("/movies/<movie_id>")
def display_movie(movie_id):
    """Display's info for each movie"""

    movie = crud.get_movie_by_id(movie_id)

    return render_template("movie_details.html", movie=movie)

@app.route("/users")
def display_users():
    """View all users"""

    users = crud.get_all_users()

    return render_template("all_users.html", users=users)

@app.route("/users", methods=["POST"])
def register_user():
    """Creates a new user"""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if user:
        ###  get_flashed_messages() ?!?!?!?!?! 
        flash("Email is already taken. Please try again.")

    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account was created successfully. You can now log in.")

    return redirect("/")

@app.route("/login", methods=["POST"])
def login_user():
    """Lets user login"""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email) 

    if not user:
        flash("This user doesn't exist") 

    elif not password:
        flash("You forgot a password silly") 

    else:
        if user.password == password:
            # log the user in by adding their primary key to the Flask session.
            session["email"] = email
            flash("Logged in!")

        else:
            flash("Your password and email didn't match. Try again") 

    return redirect("/")

@app.route("/users/<user_id>")
def display_user_profile(user_id):
    """View user profile page"""

    user = crud.get_user_by_id(user_id)

    return render_template("user_profile.html", user=user)

@app.route("/movies/<movie_id>/ratings", methods=["POST"])
def rate_movie(movie_id):
    """Allows user to rate a movie"""

    score = request.form.get("rating")
    movie = crud.get_movie_by_id(movie_id)

    if "email" in session:
        user_email = session["email"]
        user = crud.get_user_by_email(user_email)

        rating = crud.create_rating(score, movie, user)
        db.session.add(rating)
        db.session.commit()
        
        flash(f"You rated {movie.title} a {score} out of 5.")

    else:
        flash("Sorry, you cannot add a rating because you are not a user.")

    return redirect(f"/movies/{movie_id}")


############################ trying to figure out how to not let multiple ratings be valid #########################
# score = request.form.get("rating")
#     movie = crud.get_movie_by_id(movie_id)

#     if "email" in session:
#         user_email = session["email"]
#         user = crud.get_user_by_email(user_email)
#         all_ratings = movie.ratings

#         # check if the user has rated this movie before
#         if all_ratings.query.filter(movie.ratings.user_id == user.user_id).all():
#             flash(f"You already rated {movie.title} a {all_ratings.user_id.score} out of 5.")

#         else:
#             rating = crud.create_rating(score, movie, user)
#             db.session.add(rating)
#             db.session.commit()
            
#         flash(f"You rated {movie.title} a {score} out of 5.")

#     else:
#         flash("Sorry, you cannot add a rating because you are not a user.")

#     return redirect(f"/movies/{movie_id}")
    


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
