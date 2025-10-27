from src.app import users_database, login_manager
from flask_login import UserMixin
import uuid


@login_manager.user_loader
def load_user(id_user):
    return User.query.get(int(id_user))


class User(users_database.Model, UserMixin):
    id = users_database.Column(users_database.Integer, primary_key=True)
    username = users_database.Column(users_database.String(16), nullable=False, unique=True)
    password = users_database.Column(users_database.String(128), nullable=False)
    profile_picture = users_database.Column(users_database.String(32), default='default_user_image.jpg', nullable=False)

    discord_id = users_database.Column(users_database.Integer, nullable=True)
    discord_username = users_database.Column(users_database.String(32), nullable=True)
    
    verification_code = users_database.Column(users_database.String(12), nullable=True)
    verification_expires = users_database.Column(users_database.DateTime, nullable=True)

    is_admin = users_database.Column(users_database.Boolean, default=False, nullable=False)

    ficha = users_database.relationship('Ficha', back_populates='user', cascade='all, delete-orphan', uselist=False)



class Ficha(users_database.Model):
    __tablename__ = 'fichas'

    id = users_database.Column(users_database.Integer, primary_key=True)
    uuid = users_database.Column(users_database.String(36), unique=True, default=lambda: str(uuid.uuid4()))
    visible = users_database.Column(users_database.Boolean, default=False, nullable=False)

    nome = users_database.Column(users_database.String(64), nullable=False)

    nivel = users_database.Column(users_database.SmallInteger, default=1, nullable=False)

    vida_maxima = users_database.Column(users_database.SmallInteger, nullable=False)
    vida_atual = users_database.Column(users_database.SmallInteger, nullable=False)
    vida_temp = users_database.Column(users_database.SmallInteger, default=0, nullable=False)

    forca = users_database.Column(users_database.SmallInteger, nullable=False)
    destreza = users_database.Column(users_database.SmallInteger, nullable=False)
    constituicao = users_database.Column(users_database.SmallInteger, nullable=False)
    inteligencia = users_database.Column(users_database.SmallInteger, nullable=False)
    carisma = users_database.Column(users_database.SmallInteger, nullable=False)

    acrobacia = users_database.Column(users_database.SmallInteger, nullable=False)
    adestramento = users_database.Column(users_database.SmallInteger, nullable=False)
    artes = users_database.Column(users_database.SmallInteger, nullable=False)
    atletismo = users_database.Column(users_database.SmallInteger, nullable=False)
    ciencias = users_database.Column(users_database.SmallInteger, nullable=False)
    crime = users_database.Column(users_database.SmallInteger, nullable=False)
    enganacao = users_database.Column(users_database.SmallInteger, nullable=False)
    fortitude = users_database.Column(users_database.SmallInteger, nullable=False)
    furtividade = users_database.Column(users_database.SmallInteger, nullable=False)
    iniciativa = users_database.Column(users_database.SmallInteger, nullable=False)
    intimidacao = users_database.Column(users_database.SmallInteger, nullable=False)
    intuicao = users_database.Column(users_database.SmallInteger, nullable=False)
    investigacao = users_database.Column(users_database.SmallInteger, nullable=False)
    luta = users_database.Column(users_database.SmallInteger, nullable=False)
    medicina = users_database.Column(users_database.SmallInteger, nullable=False)
    oficio = users_database.Column(users_database.SmallInteger, nullable=False)
    oficio_nome = users_database.Column(users_database.String(64), nullable=True)
    oficio_atributo = users_database.Column(users_database.String(16), nullable=False, default="inteligencia")
    percepcao = users_database.Column(users_database.SmallInteger, nullable=False)
    persuasao = users_database.Column(users_database.SmallInteger, nullable=False)
    pilotagem = users_database.Column(users_database.SmallInteger, nullable=False)
    pontaria = users_database.Column(users_database.SmallInteger, nullable=False)
    profissao = users_database.Column(users_database.SmallInteger, nullable=False)
    reflexos = users_database.Column(users_database.SmallInteger, nullable=False)
    religiao = users_database.Column(users_database.SmallInteger, nullable=False)
    sobrevivencia = users_database.Column(users_database.SmallInteger, nullable=False)
    tatica = users_database.Column(users_database.SmallInteger, nullable=False)
    tecnologia = users_database.Column(users_database.SmallInteger, nullable=False)
    historia = users_database.Column(users_database.SmallInteger, nullable=False)
    vontade = users_database.Column(users_database.SmallInteger, nullable=False)
    
    user_id = users_database.Column(users_database.Integer, users_database.ForeignKey('user.id'), nullable=False)
    user = users_database.relationship('User', back_populates='fichas')