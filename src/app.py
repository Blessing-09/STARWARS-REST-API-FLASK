"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, People, Favorite,favorite_type
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET']) #Get a list of all the blog post users.
def get_user():
    users = User.query.all()
    if not users:
        return jsonify({"Error msg": "Users not found"}), 404
    
    users_info  = list(map(lambda user: user.serialize(), users))
    return jsonify(users_info), 200

@app.route('/users/favorites', methods=['GET']) #Get all the favorites that belong to the current user.
def get_users_favorites():
    user = User.query.first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    favorites = Favorite.query.filter_by(user_id = user.id).all() #user_id in fav model(FK)
    all_favorites = [favorite.serialize() for favorite in favorites]
    return jsonify(all_favorites), 200


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all() #gets all planets from model
    planets_info  = list(map(lambda planet: planet.serialize(), planets))

    return jsonify(planets_info), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id) #gets a single planet from model
    if planet is None:
        return jsonify({"Error msg": "planet not found"}), 404
    planet_info  = planet.serialize() #no need to map list cuz we are returning just one planet
    return jsonify(planet_info), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST']) #Add new favorite planet to the current user with the planet id = planet_id.
def add_planet(planet_id):
    user = User.query.first()
    if user is None:
        return jsonify({"Error": "User not found"}), 400
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"Error": "Planet not found"}), 404
    new_favorite_planet = Favorite(user_id = user.id, planet_id = planet_id, type = favorite_type.PLANET)
     #save to database
    db.session.add(new_favorite_planet)
    db.session.commit()
    return jsonify(new_favorite_planet.serialize()), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE']) #Delete a favorite planet with the id = planet_id.
def delete_planet(planet_id):
    user = User.query.first()
    if user is None:
        return jsonify({"Error": "User not found"}), 400
    favorite = Planet.query.filter_by(user_id = user.id, planet_id = planet_id, type = favorite_type.PLANET).first()
    if favorite is None:
        return jsonify({"Error": "Planet not found"}), 404
     #save to database
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"Msg": "Favorite deleted successfully"}), 200

@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all() #gets all persons from model
    people_info  = list(map(lambda person: person.serialize(), people))

    return jsonify(people_info), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id) #gets a single person from model
    if person is None:
        return jsonify({"Error msg": "person not found"}), 404
    person_info  = person.serialize() #no need to map list cuz we are returning just one planet
    return jsonify(person_info), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST']) #Add new favorite people to the current user with the people id = people_id.
def add_person(people_id):
    user = User.query.first()
    if user is None:
        return jsonify({"Error": "User not found"}), 404
    person = People.query.get(people_id)
    if person is None:
        return jsonify({"Error": "Person not found"}), 404
    new_favorite_people = Favorite(
        user_id = user.id, 
        people_id = people_id, 
        type = favorite_type.PEOPLE, 
        name=person.name)

     #save to database
    db.session.add(new_favorite_people)
    db.session.commit()
    return jsonify(new_favorite_people.serialize()), 201

@app.route('/favorite/people/<int:people_id>', methods=['DELETE']) #Delete a favorite people with the id = people_id.
def delete_people(people_id):
    user = User.query.first()
    if user is None:
        return jsonify({"Error": "User not found"}), 400
    favorite = People.query.filter_by(user_id= user.id, people_id = people_id, type=favorite_type.PEOPLE).first()
    if favorite is None:
        return jsonify({"Error": "Person not found"}), 404
     #save to database
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"Msg": "Favorite deleted successfully"}), 200


@app.route('/favorites', methods=['GET'])
def get_favorites():
    favorites = Favorite.query.all() #gets all favorites from model
    favorites_info  = list(map(lambda favorite: favorite.serialize(), favorites))

    return jsonify(favorites_info), 200
'''
@app.route('/favorites', methods=['POST'])
def create_favorites():
    data = request.get_json()
    user_id = data("user_id")
    favorite_type = data("type")

    # 3. Validate the fields (good practice!)
    if not user_id or not favorite_type:
        return jsonify({"error": "user_id and type are required"}), 400
    
    new_favorite = Favorite(user_id=user_id, type=favorite_type)

    #save to database
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 201
    '''

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
