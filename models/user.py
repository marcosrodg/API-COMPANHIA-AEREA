from sql_alchemy import db
import hashlib


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(160), nullable=False)
    
    def __init__(self,id,name,email,password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        
    @classmethod
    def find_user(cls,id):
        user = cls.query.filter_by(id = id).first()
        if user:
            return user
        return None
    
    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email':self.email
            }
    
    def save_user(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def encrypter(cls,password):
        
        hash = hashlib.sha512(str(password).encode('utf-8')).hexdigest()
        return hash