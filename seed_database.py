import os  
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb ratings")
os.system("createdb ratings")

model.connect_to_db(server.app)

with app.app_context():
    model.db.create_all()
    
with open('data/movies.json') as f:
    movie_data = json.loads(f.read())
    
    