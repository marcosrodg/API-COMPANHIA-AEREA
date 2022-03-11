from sql_alchemy import db
from flask import jsonify



class FlightModel(db.Model):
    __tablename__ = 'flight'
    
    id = db.Column(db.Integer, primary_key=True)
    air_from_prefix = db.Column(db.String(3), db.ForeignKey('airport_from.prefix'))
    air_destination_prefix = db.Column(db.String(3), db.ForeignKey('airport_destination.prefix'))
    seats = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    tickets = db.relationship('TicketModel')
    
    
    def __init__(self,air_from_prefix, air_destination_prefix, seats, date, price):
        self.air_from_prefix = air_from_prefix
        self.air_destination_prefix = air_destination_prefix
        self.seats = seats
        self.date = date
        self.price = price
    
    @classmethod
    def find_flight(cls, id):
        flight = cls.query.filter_by(id=id).first()
        if flight:
            return flight
        return None
    
    #retorna dados do voo
    def json(self):
        return {
            "id": self.id,
            "from": self.air_from_prefix,
            "destination":self.air_destination_prefix,
            "seats":self.seats,
            "date":self.date,
            "price":self.price
        }
    
    # calcula um desconto de acordo com a quantidade de assentos informado
    def discount(self, seats):
        if seats < 3:
            return self.price
        elif seats < 6:
            return round(self.price - (self.price * 0.1 ),2)
        elif seats < 11:
            return round(self.price - (self.price * 0.2 ),2)
        else:
            return round(self.price - (self.price * 0.3 ),2)
    
    def sale(self,seats):
        return {
            "id": self.id,
            "from": self.air_from_prefix,
            "destination":self.air_destination_prefix,
            "seats":self.seats,
            "date":self.date,
            "price": self.discount(seats),
        }
    
    def my_tickets(self):
        return [ticket.json() for ticket in self.tickets]
    
    def occupation(self,pos):
        """Verifica se um determinado assentoja esta ocupado

        Args:
            pos (int): posicao do assento informado

        Returns:
            bool: False caso nao possa ver feita a reserva e True caso possa ser feita a reserva
        """
        result = [ticket.seat for ticket in self.tickets if ticket.seat == pos]
        if result:
            return False
        return  True
         
    # deleta um voo
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    # salvar o voo na tabela do banco
    def save(self):
        db.session.add(self)
        db.session.commit() 
