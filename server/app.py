#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_mail import Mail, Message

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'

migrate = Migrate(app, db)
db.init_app(app)
mail = Mail(app)

api = Api(app)

class Index(Resource):
    def get(self):
        response_dict = {
            "message": "Welcome to the Superheroes API",
        }
        response = make_response(response_dict, 200)
        return response

api.add_resource(Index, '/')

class Heroes(Resource):
    def get(self):
        heroes = Hero.query.all()
        response_dict_list = [hero.to_dict(only=('id', 'name', 'super_name')) for hero in heroes]
        response = make_response(response_dict_list, 200)
        return response

api.add_resource(Heroes, '/heroes')

class HeroByID(Resource):
    def get(self, id):
        hero = Hero.query.filter_by(id=id).first()
        
        if not hero:
            response_dict = {"error": "Hero not found"}
            response = make_response(response_dict, 404)
            return response
        
        response_dict = hero.to_dict()
        response = make_response(response_dict, 200)
        return response

api.add_resource(HeroByID, '/heroes/<int:id>')

class Powers(Resource):
    def get(self):
        powers = Power.query.all()
        response_dict_list = [power.to_dict(only=('id', 'name', 'description')) for power in powers]
        response = make_response(response_dict_list, 200)
        return response

api.add_resource(Powers, '/powers')

class PowerByID(Resource):
    def get(self, id):
        power = Power.query.filter_by(id=id).first()
        
        if not power:
            response_dict = {"error": "Power not found"}
            response = make_response(response_dict, 404)
            return response
        
        response_dict = power.to_dict(only=('id', 'name', 'description'))
        response = make_response(response_dict, 200)
        return response

    def patch(self, id):
        power = Power.query.filter_by(id=id).first()
        
        if not power:
            response_dict = {"error": "Power not found"}
            response = make_response(response_dict, 404)
            return response
        
        data = request.get_json()
        
        if 'description' in data:
            if not data['description'] or len(data['description']) < 20:
                response_dict = {"errors": ["validation errors"]}
                response = make_response(response_dict, 400)
                return response
            
            power.description = data['description']
        
        db.session.add(power)
        db.session.commit()
        
        response_dict = power.to_dict(only=('id', 'name', 'description'))
        response = make_response(response_dict, 200)
        return response

api.add_resource(PowerByID, '/powers/<int:id>')

class HeroPowers(Resource):
    def post(self):
        data = request.get_json()
        
        strength = data.get('strength')
        power_id = data.get('power_id')
        hero_id = data.get('hero_id')
        
        if strength not in ['Strong', 'Weak', 'Average']:
            response_dict = {"errors": ["validation errors"]}
            response = make_response(response_dict, 400)
            return response
        
        hero = Hero.query.filter_by(id=hero_id).first()
        power = Power.query.filter_by(id=power_id).first()
        
        if not hero or not power:
            response_dict = {"errors": ["validation errors"]}
            response = make_response(response_dict, 400)
            return response
        
        new_hero_power = HeroPower(
            strength=strength,
            power_id=power_id,
            hero_id=hero_id
        )
        
        db.session.add(new_hero_power)
        db.session.commit()
        
        response_dict = new_hero_power.to_dict()
        response = make_response(response_dict, 201)
        return response

api.add_resource(HeroPowers, '/hero_powers')

if __name__ == '__main__':
    app.run(port=5555, debug=True)