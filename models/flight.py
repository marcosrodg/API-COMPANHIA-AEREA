from sql_alchemy import db


class FlightModel(db.Model):
    __tablename__ = 'flight'
    
    id = db.Column(db.Integer, primary_key=True)
    air_from_prefix = db.Column(db.String(3), db.ForeignKey('airport_from.prefix'))
    air_destination_prefix = db.Column(db.String(3), db.ForeignKey('airport_destination.prefix'))
    seats = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    
    
    def __init__(self,air_from_prefix, air_destination_prefix, seats, date, price):
        self.air_from_prefix = air_from_prefix
        self.air_destination_prefix = air_destination_prefix
        self.seats = seats
        self.date = date
        self.price = price
    
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
    
    def sale(self,percentage):
        return {
            "id": self.id,
            "from": self.air_from_prefix,
            "destination":self.air_destination_prefix,
            "seats":self.seats,
            "date":self.date,
            "price":round(self.price - (self.price * (percentage / 100) ),2),
            "discount": f"{percentage}%"
        }
        
    # deleta um voo
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    # salvar o voo na tabela do banco
    def save(self):
        db.session.add(self)
        db.session.commit() 
