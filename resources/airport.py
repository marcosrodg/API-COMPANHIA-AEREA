from models.airport import AirportFromModel, AirportDestinationModel, AirportsAll
from flask_restful import Resource, reqparse
from flask_jwt_extended import  jwt_required


attributes = reqparse.RequestParser()

attributes.add_argument('name',type=str,required=True, help='The field name cannot be empty.')
attributes.add_argument('city',type=str,required=True, help='The field city cannot be empty.')
attributes.add_argument('state',type=str,required=True, help='The field state cannot be empty.')
attributes.add_argument('zone',type=str,required=True, help='The field zone cannot be empty.')


class Airport(Resource):
    # .../aeroports
    
    def get(self):
        # retorna todos os aeroportos que a companhia aerea atende,
        # seja ele uma origem ou destino
        
        # busca o prefixo de todos aeropostos na tabela
        airports = [air.prefix for air in AirportsAll.query.all()]
        
        for air in airports:
            # procura nas tabelas de origem e destino se o aeroporto em questao
            # ainda é uma rota 
            resp_from = AirportFromModel.find_airport(air)
            resp_dest = AirportDestinationModel.find_airport(air)
            if not (resp_from or resp_dest):
                # caso o aeroporto n seja mais uma rota de origem ou destinos
                # ele é deletado
                resp_all = AirportsAll.find_airport(air)
                resp_all.delete()
        
        # retorno os bancos restante na tabela     
        return {"airports":[air.json() for air in AirportsAll.query.all()]}, 200 #OK


class AirportFrom(Resource):
    # .../aeroport/from/<prefix_airport>
    
    @jwt_required()
    def post(self,prefix_airport): # Insere um novo aeroporto, recebe um parametro da URL pra isso
        # Instancia os argumentos passados pelo body
        data = attributes.parse_args()
        # Verifica se o aeroporto ja esta cadastrado na base de dados
        air_from = AirportFromModel.find_airport(prefix_airport)
        if not air_from:
            # sera instanciado um novo aeroporto, com os dados informados
            airport = AirportFromModel(prefix_airport.lower(),data["name"].lower(),data["city"].lower(), data["state"].lower(), data['zone'])
            generals = AirportsAll.find_airport(prefix_airport)# verifico se a tabela aeroporto gerais, ja tem o aeroporto
            if not generals: # Se encontrar na tabela geral, insiro nela esse novo registro
                air = AirportsAll(prefix_airport.lower(),data["name"].lower(),data["city"].lower(), data["state"].lower())
                air.save()
            try:
                airport.save()# tento inserir o registro na tabela aeroporto_from
                return {"mensage": airport.json()}, 201 #Created
            except Exception as e:
                return {"mensage":"Fail to save Airport"}, 500 # Innternal Server Error
        return {"mensage":f"Airport prefix {prefix_airport} already exists"}, 400 # Bad Request
    
    @jwt_required()
    def delete(self,prefix_airport):
        # busca pelo aeroporto de prefixo informado
        air_from = AirportFromModel.find_airport(prefix_airport)
        if air_from:
            try:
                air_from.delete() # chamado o metodo de delecao da classe
                return {"mensage":"Airport deleted successfully"}, 200 #ok
            except Exception as e:
                return {"mensage":"Fail to delete airport"}, 500 #Internal server error  
        return {"mensage":"Airport not found"}, 400 # Bad Request

class AirportDestination(Resource):
     # .../airport/destination/<prefix_airport>

    @jwt_required()
    def post(self,prefix_airport): # Insere um novo aeroporto, recebe um parametro da URL pra isso
        # Instancia os argumentos passados pelo body
        data = attributes.parse_args()
        # Verifica se o aeroporto ja esta cadastrado na base de dados
        destination = AirportDestinationModel.find_airport(prefix_airport)
        # caso nao estiver cadastrado nenhum aeroporto com o prefixo informado
        if not destination:
            # sera instanciado um novo aeroporto, com os dados informados
            airport = AirportDestinationModel(prefix_airport.lower(),data["name"].lower(),data["city"].lower(), data["state"].lower(),data['zone'])
            generals = AirportsAll.find_airport(prefix_airport) # verifico se a tabela aeroporto gerais, ja tem o aeroporto
            if not generals: # Se encontrar na tabela geral, insiro nela esse novo registro
                air = AirportsAll(prefix_airport.lower(),data["name"].lower(),data["city"].lower(), data["state"].lower())
                air.save()
            try:# tento inserir o registro na tabela aeroporto_destination
                airport.save()
                return {"mensage": airport.json()}, 201 # Created
            except Exception as e:
                return {"mensage":"Fail to save Airport"}, 500 # Innternal Server Error
        return {"mensage":f"Airport prefix {prefix_airport} already exists"}, 400 # Bad Request
    
    @jwt_required()
    def delete(self,prefix_airport):
        """ Delecao de aeroportos

        Args:
            prefix_airport (str): passado na url, como sendo o identificado do 
            aeroporto a ser excluido

        Returns:
            Resposta da tentativa de delecao
        """
        # busca pelo aeroporto de prefixo informado
        air_dest= AirportDestinationModel.find_airport(prefix_airport) 
        # Caso exista
        if  air_dest:
            try:
                # Tenta fazer sua delecao, chamando um metodo da classe
                air_dest.delete()
                return {"mensage":"Airport destination deleted successfully"}, 200 #ok
            except Exception as e:
                print(e)
                return {"mensage":"Fail to delete airport"}, 500 #Internal server error  
        return {"mensage":"Airport not found"}, 400 # Bad Request

class Destination(Resource):
    # .../aeroports/<prefix_from>
    
    def get (self, prefix_from):
        """Busca por aeropostos de destino apartir de um aeroporto informado

        Args:
            prefix_from (str): prefixo do aeroporto de origem 

        Returns:
            list: Retorna uma lista com todos os aeroportos no qual o aeroporto informado
            pode fazer voo
        """
        air_from = AirportFromModel.find_airport(prefix_from) # Procura na tabela de origem pelo aeroporto informado
        # se o aeroporto for encontrado
        if air_from: 
            # se o valor da zona for 0, ele viaja para todos os aeroportos
            if air_from.zone == 0:
                # listo todos aeroportos da tabela de destinos, excluindo o aeroporto de origem caso ele tbm for um destino
                return {"destinations":[ air.json() for air in AirportDestinationModel.query.all() \
                    if air.prefix != air_from.prefix ] }, 200 #OK
            # Mas se a zona nao for zero, busco todos de zonas iguais ao informado
            alls = AirportDestinationModel.query.filter_by(zone=air_from.zone).all()
            # retorno todos os aeroportos de mesma zona, excluindo o aeroporto de origem caso ele tbm for um destino
            return {"destinations":[air.json() for air in alls if air.prefix != air_from.prefix]}, 200 #Ok
        # O aeroporto informado nao é nenhum de origem
        return {"mensage":"Airport not found"}, 400 #Bad request