from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import  safe_str_cmp
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from blacklist import BLACKLIST



attributes = reqparse.RequestParser()

attributes.add_argument('id',type=str,required=True, help='The field login cannot be empty.')
attributes.add_argument('name',type=str,required=True, help='The field login cannot be empty.')
attributes.add_argument('email',type=str,required=True, help='The field login cannot be empty.')
attributes.add_argument('password',type=str,required=True, help='The field login cannot be empty.')


class UserRegister(Resource):
    def post(self):
        data = attributes.parse_args()
        if UserModel.find_user(data['id']):
            return {"mensage":"User already exist"}, 400 # Bad Request
        
        new_password = UserModel.encrypter(data["password"])
        user = UserModel(data["id"],data["name"],data["email"],new_password)
        try:
            user.save_user()
            return user.json(), 201 # Created
        except:
            return {'mensage':'An error occurred while saving user'}, 500 # Innternal Server Error
    
        
class UserLogin(Resource):
    
    @classmethod
    def post(cls):
        credentials = reqparse.RequestParser()
        credentials.add_argument('id',type=str,required=True, help='The field login cannot be empty.')
        credentials.add_argument('password',type=str,required=True, help='The field login cannot be empty.')

        data = credentials.parse_args()
        user = UserModel.find_user(data["id"])
        
        encrypted = UserModel.encrypter(data["password"])
       
        if user and safe_str_cmp(user.password, encrypted):
            payload = {
                "id":user.id, #campo "cpf" recebe cpf do usuario atual 
                "email":user.email #campo "email" recebe email do usuario atual 
            }
            access_token = create_access_token(identity=payload)
            return {"access_token": access_token}, 200 # OK
            
        return {"mensage":"User or Password incorrect"}, 401 #unauthorized


class UserLogout(Resource):
    
    @jwt_required()
    def post(self):
        jwt_token = get_jwt()['jti']
        try:
            BLACKLIST.add(jwt_token)
            return {"mensage":"User logged out"}, 200 #ok
        except:
            return {"mensage":"Failed to logout"}, 500 #Innternal Server Error
