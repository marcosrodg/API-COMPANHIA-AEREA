
from models.tickets import TicketModel
from models.flight import FlightModel
from flask_restful import Resource, reqparse
from flask_jwt_extended import  jwt_required, get_jwt

attributes = reqparse.RequestParser()

attributes.add_argument('id_flight',type=int,required=True, help='The field id_flight cannot be empty.')
attributes.add_argument('seat',type=str,required=True, help='The field seat cannot be empty.')
attributes.add_argument('quantity',type=int,required=True, help='The field quantity cannot be empty.')

class Ticket(Resource):
    
    @jwt_required()
    def post(self):
        """Funcao faz a reserva de voos, retornando preço,id do ticket
        e outras informacoes

        Returns:
            Informacoes do ticket, e do voo caso tenha dado certo a reserva
        """
        # instancia os dados recebido
        data = attributes.parse_args()
        
        # recebo o subject do payload passado no login
        user = get_jwt()['sub']
        cart = [] # carrinho
        error =[] # lista de assentos ocupados
        total = 0
        
        # Procura pelo voo apartir do id informado
        flight = FlightModel.find_flight(data['id_flight'])
        
        # calcula o desconto, de acordo com o numero de passageiros informado
        current_price = flight.discount(data["quantity"])
        
        # transforma os valores recebido como string em uma lista com numero
        # de cada assento
        seats =[ int(value) for value in data["seat"].split(",")]
        
        # Verifica se a quantidade de tickets informada é igual ao numero de 
        # assentos informados
        if len(seats) != data['quantity']:
            return {"mensage":" Seats and number of tickets must be the same"}, 400 # Bad Request
        
        # caso haja o voo informado
        if flight:
            for count in range(data["quantity"]): # Para cada ticket da quuantidade informada
                #Verifica a disponibilidade do assento
                if flight.occupation(seats[count]) and (seats[count] <= flight.seats):
                    # caso esteja disponivel o assento, instanciamos a classe
                    ticket = TicketModel(user["id"],data["id_flight"],seats[count],flight.date, current_price)
                    try:
                        ticket.save() # salva ticket
                        total += ticket.price # incrementa o preco a pagar
                        cart.append(ticket.json())
                    except Exception as e:
                         error.append(seats[count])
                else:
                    error.append(seats[count])
            if len(error) > 0: # Se tiver algum ticket na lista de erro , retorno os sucessos e os erros
                return {"Succesfull": [ticket for ticket in cart],
                        "Fail":f"Seats {error} ocuppied or not found, please choose another seat and try again",
                        "total": f"R${round(total,2)}"}
            
            # retorna os tickets comprados com sucesso
            return {"tickets":[ticket for ticket in cart],
                    "total": f"R${round(total,2)}"}
        
        return {"mensage":"Flight not found"}, 400 #Bad Request

