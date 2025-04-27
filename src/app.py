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
from models import db, User, Planet, People, favorite_type
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

@app.route('/user', methods=['GET'])
def get_user():
    new_user = User.query.all()
    if not new_user:
        return jsonify({"msg": "User not found"}), 400
    return 
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

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

@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all() #gets all persons from model
    people_info  = list(map(lambda person: person.serialize(), people))

    return jsonify(people_info), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id) #gets a single planet from model
    if person is None:
        return jsonify({"Error msg": "person not found"}), 404
    person_info  = person.serialize() #no need to map list cuz we are returning just one planet
    return jsonify(person_info), 200
    


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
