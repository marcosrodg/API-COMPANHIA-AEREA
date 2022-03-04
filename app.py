from flask import Flask
from flask_restful import Api, Resource
from resources.user import UserRegister
from sql_alchemy import db
import os
from dotenv import load_dotenv


os.getenv('JWT_SECRET_KEY')


app = Flask(__name__)
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_BLACKLIST_ENABLED'] = os.getenv('JWT_BLACKLIST_ENABLED')

api = Api(app)
db.init_app(app)



@app.before_first_request
def create_database():
    db.create_all()
    

api.add_resource(UserRegister,'/register')

if __name__ == '__main__':
    app.run(debug=True)