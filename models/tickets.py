from sql_alchemy import db


class TicketModel(db.Model):
    __tablename__ = 'ticket'
    
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    id_flight = db.Column(db.Integer, db.ForeignKey('flight.id'), nullable=False)
    seat = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    
    
    def __init__(self,id_user,id_flight,seat,date,price):
        self.id_user = id_user
        self.id_flight = id_flight
        self.seat = seat
        self.date = date
        self.price = price
    
    @classmethod  
    def find_ticket_by_flight(cls,id_flight):
        """ Busca por todos os ticket apartir do id de um voo

        Args:
            id_flight (int): id do voo presente no ticket

        Returns:
            list: lista de tickets encontrados para um voo
        """
        ticket = cls.query.filter_by(id_flight=id_flight).all()
        if ticket:
            return ticket
        return None
    
    #retorna dados do voo
    def json(self):
        return {
            "id": self.id,
            "id_usuer": self.id_user,
            "id_flight":self.id_flight,
            "seat":self.seat,
            "date":self.date,
            "price":self.price
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        