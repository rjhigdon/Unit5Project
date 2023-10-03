"""Models for movie ratings app."""
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

"""User Table"""
class User(db.Model):
    
    __tablename__ = "users"
    
    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String ,unique= True, nullable = False)
    password = db.Column(db.String, nullable = False)
    
    # ratings = a list of Rating objects
    
    def __repr__(self): 
        return f"<User user_id={self.user_id} email={self.email}>" 
    
    def __init__(self, email, password):
        self.email = email 
        self.password = password 
        
class Movie(db.Model):
    __tablename__ = "movies"
        
    movie_id = db.Column(db.Integer, primary_key = True, autoincrement =True)
    title = db.Column(db.String, nullable = False)
    overview = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    poster = db.Column(db.String)
    
    # ratings = a list of Rating objects
    
    def __repr__(self):
        return f"<Movie Title: {self.title}, Release Date: {self.release_date}"
    
    def __init__ (self, title, overview, release_date, poster):
        self.title = title
        self.overview = overview
        self.release_date = release_date
        self.poster = poster
    
class Rating(db.Model):
    
    __tablename__ = "ratings"
    
    rating_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    score = db.Column(db.Integer)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies"))
    user_id = db.Column(db.Integer, db.ForeignKey("users"))
    
    movies = db.relationship("Movie", backref = "ratings", lazy = True)
    users = db.relationship("User", backref= "ratings", lazy = True)
    
    def __repr__(self):
        return f"<Rating rating_id={self.rating_id} score={self.score}>"
    
    def __init__ (self, score, movie_id, user_id):
        self.score = score
        self.movie_id = movie_id
        self.user_id = user_id


def connect_to_db(flask_app, db_uri=os.environ["POSTGRES_URI"], echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

if __name__ == "__main__":
    from server import app
    print("Connected to the db!")
    connect_to_db(app)

