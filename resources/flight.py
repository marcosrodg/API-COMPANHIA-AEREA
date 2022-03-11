from models.flight import FlightModel
from models.airport import AirportFromModel, AirportDestinationModel
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
        
        #Verifica no banco de dados se existe aeroportos informados na origem e destino
        from_verify = AirportFromModel.find_airport(data['air_from_prefix'])
        destination_verify = AirportDestinationModel.find_airport(data['air_destination_prefix'])
        
        # se existir 
        if from_verify and destination_verify and ( from_verify.zone == destination_verify.zone):
            # passa para a tabela os valores dos campos
            flight = FlightModel(data['air_from_prefix'],data['air_destination_prefix'],
                                data['seats'], data['date'], data['price'])
            try:
                flight.save() # salva os dados e comita
                return flight.json(), 201 # Created
            except Exception as e:
                return {"mensage":"Fail to create flight"}, 501 #Internal server error
        return {"mensage":"Origin or Destination not found or not in the flight zone "}, 400 # Bad request
    
    
    
    # retorna todos os voos apartir de uma data informada como parametro
    def get(self):
        #.../flight?date=dd-mm-yyyy
        
        path_params = reqparse.RequestParser()
        path_params.add_argument('date',type=str,required=True, help='The field date cannot be empty.')
        date = path_params.parse_args()
         #retorna todos os voos na data informada
        return {"flights":[ flight.json() for flight in FlightModel.query.filter_by(date=date['date']).all() ] }
    

class FlightSale(Resource):
    #.../flight/sale?tickets=<int>&from=<prefix>&destination=<prefix>
    
    def get(self):
        
        # Recebe os parametros pela url
        path_params = reqparse.RequestParser()
        path_params.add_argument('tickets',type=int,required=True, help='The field tickets cannot be empty.')
        path_params.add_argument('destination',type=str,required=True, help='The field destination cannot be empty.')
        path_params.add_argument('from',type=str,required=True, help='The field from cannot be empty.')
        data= path_params.parse_args()

        # lista os voos , sem desconto
        return {"flights":[flight.sale(data["tickets"]) for flight in \
            FlightModel.query.filter_by(air_from_prefix=data['from']).filter_by(air_destination_prefix=data['destination']).limit(5)]}
        

            

        