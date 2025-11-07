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
    
    verification_code = users_database.Column(users_database.String(12), nullable=True)
    verification_expires = users_database.Column(users_database.DateTime, nullable=True)

    is_admin = users_database.Column(users_database.Boolean, default=False, nullable=False)

    ficha = users_database.relationship('Ficha', back_populates='user', cascade='all, delete-orphan', uselist=False)


class Ficha(users_database.Model):
    id = users_database.Column(users_database.Integer, primary_key=True)
    uuid = users_database.Column(users_database.String(36), unique=True, default=lambda: str(uuid.uuid4().hex[:16]))
    visible = users_database.Column(users_database.Boolean, default=False, nullable=False)

    nome_personagem = users_database.Column(users_database.String(32), nullable=False)

    historia_personagem = users_database.Column(users_database.Text, nullable=True)
    aparencia_personagem = users_database.Column(users_database.Text, nullable=True)
    bio_personagem = users_database.Column(users_database.Text, nullable=True)
    favoritos_personagem = users_database.Column(users_database.Text, nullable=True)
    defeitos_personagem = users_database.Column(users_database.Text, nullable=True)

    nivel = users_database.Column(users_database.SmallInteger, default=1, nullable=False)
    level_up = users_database.Column(users_database.Boolean, default=False, nullable=False)
    dice = users_database.Column(users_database.SmallInteger, default='black', nullable=False)

    vida_maxima = users_database.Column(users_database.SmallInteger, nullable=False)
    vida_atual = users_database.Column(users_database.SmallInteger, nullable=False)
    vida_temp = users_database.Column(users_database.SmallInteger, default=0, nullable=False)

    forca = users_database.Column(users_database.SmallInteger, nullable=False)
    destreza = users_database.Column(users_database.SmallInteger, nullable=False)
    constituicao = users_database.Column(users_database.SmallInteger, nullable=False)
    inteligencia = users_database.Column(users_database.SmallInteger, nullable=False)
    carisma = users_database.Column(users_database.SmallInteger, nullable=False)

    p_acrobacia = users_database.Column(users_database.SmallInteger, nullable=False)
    p_adestramento = users_database.Column(users_database.SmallInteger, nullable=False)
    p_artes = users_database.Column(users_database.SmallInteger, nullable=False)
    p_atletismo = users_database.Column(users_database.SmallInteger, nullable=False)
    p_ciencias = users_database.Column(users_database.SmallInteger, nullable=False)
    p_crime = users_database.Column(users_database.SmallInteger, nullable=False)
    p_enganacao = users_database.Column(users_database.SmallInteger, nullable=False)
    p_fortitude = users_database.Column(users_database.SmallInteger, nullable=False)
    p_furtividade = users_database.Column(users_database.SmallInteger, nullable=False)
    p_iniciativa = users_database.Column(users_database.SmallInteger, nullable=False)
    p_intimidacao = users_database.Column(users_database.SmallInteger, nullable=False)
    p_intuicao = users_database.Column(users_database.SmallInteger, nullable=False)
    p_investigacao = users_database.Column(users_database.SmallInteger, nullable=False)
    p_luta = users_database.Column(users_database.SmallInteger, nullable=False)
    p_medicina = users_database.Column(users_database.SmallInteger, nullable=False)
    p_oficio = users_database.Column(users_database.SmallInteger, nullable=False)
    oficio_nome = users_database.Column(users_database.String(20), nullable=False)
    oficio_atributo = users_database.Column(users_database.String(16), nullable=False, default="inteligencia")
    p_percepcao = users_database.Column(users_database.SmallInteger, nullable=False)
    p_persuasao = users_database.Column(users_database.SmallInteger, nullable=False)
    p_pilotagem = users_database.Column(users_database.SmallInteger, nullable=False)
    p_pontaria = users_database.Column(users_database.SmallInteger, nullable=False)
    p_reflexos = users_database.Column(users_database.SmallInteger, nullable=False)
    p_religiao = users_database.Column(users_database.SmallInteger, nullable=False)
    p_sobrevivencia = users_database.Column(users_database.SmallInteger, nullable=False)
    p_tatica = users_database.Column(users_database.SmallInteger, nullable=False)
    p_tecnologia = users_database.Column(users_database.SmallInteger, nullable=False)
    p_historia = users_database.Column(users_database.SmallInteger, nullable=False)
    p_vontade = users_database.Column(users_database.SmallInteger, nullable=False)
    
    user_id = users_database.Column(users_database.Integer, users_database.ForeignKey('user.id'), nullable=False)
    user = users_database.relationship('User', back_populates='ficha')

    inventory = users_database.relationship('Inventory', back_populates='ficha', cascade='all, delete-orphan')


class Inventory(users_database.Model):
    item_id = users_database.Column(users_database.Integer, primary_key=True)

    item_name = users_database.Column(users_database.String(64), nullable=False)
    is_weapon = users_database.Column(users_database.Boolean, nullable=False, default=False)
    item_damage = users_database.Column(users_database.String(16), nullable=False)
    is_equipped = users_database.Column(users_database.Boolean, nullable=False, default=False) # maybe if weapon gives bonus
    item_description = users_database.Column(users_database.String(256), nullable=False)



    ficha_id = users_database.Column(users_database.Integer, users_database.ForeignKey('ficha.id'), nullable=False)
    ficha = users_database.relationship('Ficha', back_populates='inventory')