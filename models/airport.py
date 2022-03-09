from sql_alchemy import db

class Tools():
    # procura por um aeroporto apartir do prefixo informado
    @classmethod
    def find_airport(cls,prefix):
        # procura por um aeroporto apartir do prefixo informado
        airport = cls.query.filter_by(prefix=prefix).first() 
        if airport:
            return airport
        return None
    # retorna os dados do aeroporto
    def json(self):
        return {
            "prefix": self.prefix,
            "name": self.name,
            "city": self.city,
            "state": self.state
            }
    
    # retorna os voos que estao agendados daquele aeroporto
    def flights_json(self):
        return {
            "flights":[flight.json() for flight in self.flights]
        }
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def save(self):
        db.session.add(self)
        db.session.commit() 
        
# criacao da tabela onde vao conter todos os aeroportos de destino e origem
class AirportsAll(db.Model,Tools):
    __tablename__ = 'airports_all'
    
    prefix = db.Column(db.String(3), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    
    def __init__(self,prefix, name,city,state):
        self.prefix = prefix
        self.name = name
        self.city = city
        self.state = state

#criacao da classe/tabela aeroportos from
class AirportFromModel(db.Model,Tools):
    __tablename__ = 'airport_from'
    
    prefix = db.Column(db.String(3), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zone = db.Column(db.Integer, nullable=False)
    flights = db.relationship('FlightModel')

    
    def __init__(self, prefix, name, city, state, zone=0):
        self.prefix = prefix
        self.name = name
        self.city = city
        self.state = state
        self.zone = zone
        
# criacao da classe/ tabela Aeroportos destination
class AirportDestinationModel(db.Model,Tools):
    __tablename__ = 'airport_destination'
    
    prefix = db.Column(db.String(3), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zone = db.Column(db.Integer, nullable=False)
    flights = db.relationship('FlightModel')

    
    def __init__(self, prefix, name, city, state, zone=0):
        self.prefix = prefix
        self.name = name
        self.city = city
        self.state = state
        self.zone = zone

