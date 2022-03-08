from flask import Flask
from flask_restful import Api
from sql_alchemy import db
from blacklist import BLACKLIST
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os
from dotenv import load_dotenv
from resources.user import (UserRegister, UserLogin, UserLogout,)
from resources.airport import Airport, AirportFrom, AirportDestination, Destination


app = Flask(__name__)

# configuracoes de ambiente
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_BLACKLIST_ENABLED'] = os.getenv('JWT_BLACKLIST_ENABLED')
app.config['JWT_ALGORITHM'] = 'HS512' # escolha um algoritimo de sua preferencia HS256 é o padrão, neste caso escolhi o HS512 = SHA512
app.config["JWT_DECODE_ALGORITHMS"] = 'HS512'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

api = Api(app)
db.init_app(app)
jwt = JWTManager(app)


# cria o banco antes da primeira requisicao
@app.before_first_request
def create_database():
    db.create_all()

# verifica se o token do usuario atual esta na BLACKLIST
@jwt.token_in_blocklist_loader
def verify_blocklist(self, token):
    return token['jti'] in BLACKLIST

# Revoga o token, e nao permite aquele usuario com o token atual
@jwt.revoked_token_loader
def access_token_invalid(jwt_header, jwt_payload):
    return {"mensage":"You have been logged out"}, 401 #unauthorized
    
# Adicionando rotas
api.add_resource(UserRegister,'/register')
api.add_resource(UserLogin,'/login')
api.add_resource(UserLogout,'/logout')
api.add_resource(AirportFrom,'/airport/from/<prefix_airport>')
api.add_resource(AirportDestination,'/airport/destination/<prefix_airport>')
api.add_resource(Airport,'/airports')
api.add_resource(Destination,'/airports/<prefix_from>')


if __name__ == '__main__':
    app.run(debug=True)