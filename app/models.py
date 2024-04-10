from app import db
from flask_login import UserMixin
from itsdangerous import URLSafeSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from app import config


class Articulo(db.Model):
    __tablename__ = 'articulo'

    id = db.Column(db.Integer, primary_key=True, name='id')
    name = db.Column(db.String(70), unique=True, nullable=False, name='name')
    price = db.Column(db.Float, nullable=False, unique=False, name='price')
    description = db.Column(db.String(250), name='description')
    image_name = db.Column(db.String(250), unique=True, name='image_name')
    #relaciona el articulo a el id de una de las Categorias 
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), name='categoria_id',nullable=False)


class Categorias(db.Model):
    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(70), unique=True, nullable=False, name='name')
    image_category = db.Column(db.String(250), unique=True, name='image_category')
    articulos = db.relationship('Articulo', backref='categoria')

class Usuario(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)

    def get_token(self):
        serial = Serializer(config.SECRET_KEY)
        return serial.dumps({'user_id': self.id})
    
    @staticmethod
    def verify_token(token):
        serial = Serializer(config.SECRET_KEY)
        
        try:
            user_id = serial.loads(token)['user_id']
        except:
            return None
        return Usuario.query.get(user_id)
    def set_password(self, password):
            self.password =generate_password_hash(password)

    def check_passwored(self, password):
        return check_password_hash(self.password, password)