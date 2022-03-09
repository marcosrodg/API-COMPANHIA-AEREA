from models.flight import FlightModel
from flask_restful import Resource, reqparse
from flask_jwt_extended import  jwt_required

attributes = reqparse.RequestParser()

attributes.add_argument('air_from_prefix',type=str,required=True, help='The field air_from_prefix cannot be empty.')
attributes.add_argument('air_destination_prefix',type=str,required=True, help='The field air_destination_prefix cannot be empty.')
attributes.add_argument('seats',type=str,required=True, help='The field seats cannot be empty.')
attributes.add_argument('date',type=str,required=True, help='The field date cannot be empty.')
attributes.add_argument('price',type=str,required=True, help='The field price cannot be empty.')

class Flight(Resource):
    #.../flight
    
    @jwt_required()
    def post(self):
        data = attributes.parse_args()
        # Verifica se a origem e o destino do voo sao os mesmos
        if data['air_from_prefix'] == data['air_destination_prefix']:
            # caso sejam os mesmos, vai retornar mensagem de erro
            return {"mensage":"impossible flight with same origin and destination"}, 400 # Bad Request
        
        # passa para a tabela os valores dos campos
        flight = FlightModel(data['air_from_prefix'],data['air_destination_prefix'],
                             data['seats'], data['date'], data['price'])
        try:
            flight.save() # salva os dados e comita
            return flight.json(), 201 # Created
        except Exception as e:
            return {"mensage":"Fail to create flight"}, 501 #Internal server error
    
    # retorna todos os voos
    def get (self):
        return {"flights":[ flight.json() for flight in FlightModel.query.all()]}