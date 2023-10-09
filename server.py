"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db
import crud
from model import db
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "supa dupa secret"
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def homepage():
    return render_template('homepage.html')

@app.route("/movies")
def all_movies():
    movies = crud.get_movies()
    return render_template('all_movies.html', movies=movies)

@app.route("/movies/<movie_id>")
def show_movie(movie_id):
    movie = crud.get_movie_by_id(movie_id)
    return render_template("movie_details.html", movie=movie)


@app.route("/users", methods=["GET"])
def all_users():
    users = crud.get_users()
    return render_template('all_users.html', users=users)

@app.route("/users", methods=["POST"])
def register_account():
    new_email = request.form["email"]
    new_password = request.form["password"]
    
    if crud.get_user_by_email(new_email):
        flash("User already exists")
    else:
        new_user = crud.create_user(new_email, new_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Account Created")
    return redirect("/")

@app.route("/users/<user_id>")
def show_user(user_id):
    user = crud.get_user_by_id(user_id)
    return render_template('user_details.html', user=user)
    
@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]
    
    
    if crud.get_user_by_login(email, password):
        session["user_email"] = email
        flash(f"Successfully logged in as {email}")
    else:
        flash("Login Failed")
    return redirect("/")
    
@app.route("/rating/<movie_id>", methods=["POST"]) 
def rate_movie(movie_id):
    user = crud.get_user_by_email(session["user_email"])
    movie = crud.get_movie_by_id(movie_id) 
    
    score = int(request.form["score"])
    
    new_rating = crud.create_rating(user, movie, score)
    db.session.add(new_rating)
    db.session.commit()
    
    return redirect(f"/movies/{movie_id}")

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)