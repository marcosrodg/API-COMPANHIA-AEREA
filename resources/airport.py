from models.airport import AirportOriginModel, AirportDestinyModel
from flask_restful import Resource, reqparse
from flask_jwt_extended import  jwt_required


attributes = reqparse.RequestParser()

attributes.add_argument('name',type=str,required=True, help='The field name cannot be empty.')
attributes.add_argument('city',type=str,required=True, help='The field city cannot be empty.')
attributes.add_argument('state',type=str,required=True, help='The field state cannot be empty.')


class Airport(Resource):
    
    def get(self):
        pass


class AirportOrigin(Resource):
    
    @jwt_required()
    def post(self,prefix_airport):
        data = attributes.parse_args()
        origin = AirportOriginModel.find_airport(prefix_airport)
        if not origin:
            airport = AirportOriginModel(prefix_airport.lower(),data["name"].lower(),data["city"].lower(), data["state"].lower())
            try:
                airport.save()
                return {"mensage": airport.json()}
            except Exception as e:
                return {"mensage":"Fail to save Airport"}, 500 # Innternal Server Error
        return {"mensage":f"Airport prefix {prefix_airport} already exists"}, 400 # Bad Request
    
    @jwt_required()
    def delete(self,prefix_airport):
        
        origin = AirportOriginModel.find_airport(prefix_airport)
        if origin:
            try:
                origin.delete()
                return {"mensage":"Airport origin deleted successfully"}, 200 #ok
            except Exception as e:
                return {"mensage":"Fail to delete airport"}, 500 #Internal server error  
        return {"mensage":"Airport not found"}, 400 # Bad Request

class AirportDestiny(Resource):
    
    @jwt_required()
    def post(self,prefix_airport):
        data = attributes.parse_args()
        destiny = AirportDestinyModel.find_airport(prefix_airport)
        if not destiny:
            airport = AirportDestinyModel(prefix_airport.lower(),data["name"].lower(),data["city"].lower(), data["state"].lower())
            try:
                airport.save()
                return {"mensage": airport.json()}
            except Exception as e:
                return {"mensage":"Fail to save Airport"}, 500 # Innternal Server Error
        return {"mensage":f"Airport prefix {prefix_airport} already exists"}, 400 # Bad Request
    
    @jwt_required()
    def delete(self,prefix_airport):
        
        origin = AirportDestinyModel.find_airport(prefix_airport)
        if origin:
            try:
                origin.delete()
                return {"mensage":"Airport origin deleted successfully"}, 200 #ok
            except Exception as e:
                return {"mensage":"Fail to delete airport"}, 500 #Internal server error  
        return {"mensage":"Airport not found"}, 400 # Bad Request
    