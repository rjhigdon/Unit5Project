from model import db, User, Movie, Rating, connect_to_db

def create_user(email, password):
    user = User(
        email = email, 
        password = password
        )    
    return user

def create_movie(title, overview, release_date, poster):
    movie = Movie(
        title = title, 
        overview = overview, 
        release_date = release_date, 
        poster = poster
        )
    return movie

def create_rating(user, movie, score):
    """Create and return a new rating."""

    rating = Rating(score=score, movie=movie, user=user)

    return rating

if __name__ == '__main__':
    from server import app
    connect_to_db(app)