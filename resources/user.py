from flask_restful import Resource, reqparse
from models.user import UserModel


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
        user = UserModel(data['id'],data['name'],data['email'], data['password'])
        try:
            user.save_user()
            return user.json(), 201 # Created
        except:
            return {'mensage':'An error occurred while saving user'}, 500 # Innternal Server Error
    
        
        