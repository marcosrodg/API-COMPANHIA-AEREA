from sql_alchemy import db

class Tools():
    
    @classmethod
    def find_airport(cls,prefix):
        airport = cls.query.filter_by(prefix=prefix).first()
        if airport:
            return airport
        return None
    
    def json(self):
        return {
            "prefix": self.prefix,
            "name": self.name,
            "city": self.city,
            "state": self.state
            }
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def save(self):
        db.session.add(self)
        db.session.commit() 
        
        
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


class AirportOriginModel(db.Model,Tools):
    __tablename__ = 'airport_origin'
    
    prefix = db.Column(db.String(3), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    
    def __init__(self, prefix,name,city,state ):
        self.prefix = prefix
        self.name = name
        self.city = city
        self.state = state
        

class AirportDestinyModel(db.Model,Tools):
    __tablename__ = 'airport_destiny'
    
    prefix = db.Column(db.String(3), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    
    def __init__(self,prefix, name,city,state):
        self.prefix = prefix
        self.name = name
        self.city = city
        self.state = state
        