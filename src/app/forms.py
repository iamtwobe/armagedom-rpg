from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField, IntegerField, SelectMultipleField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, NumberRange
from src.app.models import User
from flask_login import current_user


class FormSignup(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired(), Length(min=4, max=16)])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=8, max=48)])
    password_confirmation = PasswordField('Confirme sua senha', validators=[DataRequired(), Length(min=6, max=24), EqualTo('password')])
    submit_button_signup = SubmitField('Criar conta')

    def validate_password(self, password):
        password = password.data
        letters = 'abcdefghijklmnopqrstuvwxyz'
        if any(i in letters for i in password.lower()) == False:
            raise ValidationError('Sua senha precisa conter uma letra.')
        if any(char.isdigit() for char in password) == False:
            raise ValidationError('Sua senha precisa de pelo menos um número')

    def validate_username(self, username):
        if ' ' in username.data:
            raise ValidationError('Seu nome de usuário não pode conter espaços.')
        usern = User.query.filter_by(username=username.data).first()
        if usern:
            raise ValidationError('Esse nome de usuário já existe.')


class FormLogin(FlaskForm):
    account = StringField('Usuário', validators=[DataRequired(), Length(min=4, max=16)])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=8, max=48)])
    remember_data = BooleanField('Lembrar de mim')
    submit_button_login = SubmitField('Login')

class FormEditProfile(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(), Length(min= 4, max= 12)])
    password = PasswordField('Senha')
    profile_picture = FileField('Atualizar foto de perfil', validators=[FileAllowed(['jpg', 'png', 'webp', 'jpeg', 'gif'])])
    submit_button_edit_profile = SubmitField('Confirmar Edição')

    def validate_username(self, username):
        if ' ' in username.data:
            raise ValidationError('Seu nome de usuário não pode conter espaços.')
        if current_user.username != username.data:
            usern = User.query.filter_by(username=username.data).first()
            if usern:
                raise ValidationError('Esse nome de usuário já existe.')
                
    def validate_password(self, password):
        password = password.data
        if not password:
            return None
        
        if len(password) < 8:
            raise ValidationError('Sua senha precisa ter pelo menos 8 caracteres.')
        elif len(password) > 48:
            raise ValidationError('Sua senha não pode ter mais de 48 caracteres.')
        
        letters = 'abcdefghijklmnopqrstuvwxyz'
        if any(i in letters for i in password.lower()) == False:
            raise ValidationError('Sua senha precisa conter uma letra.')
        if any(char.isdigit() for char in password) == False:
            raise ValidationError('Sua senha precisa de pelo menos um número')

class FormLinkDiscord(FlaskForm):
    discord_id = StringField('ID do Discord', validators=[DataRequired(), Length(min=17, max=25)])
    submit_button_link_discord = SubmitField('Confirmar')

    def validate_discord_id(self, discord_id):
        discord_id_exists = User.query.filter_by(discord_id=discord_id.data).first()
        if discord_id_exists:
            raise ValidationError('Esse ID já está sendo usado.')

class StepNomeForm(FlaskForm):
    step = HiddenField(default='1')
    nome_personagem = StringField('Nome', validators=[DataRequired(), Length(1, 30)])
    next = SubmitField('Próximo')

class StepAtributosForm(FlaskForm):
    step = HiddenField(default='2')
    pontos_max = HiddenField(default=10)
    forca = IntegerField('Força', validators=[NumberRange(0,4)], default=1, render_kw={"id": "forca"})
    destreza = IntegerField('Destreza', validators=[NumberRange(0,4)], default=1, render_kw={"id": "destreza"})
    constituicao = IntegerField('Constituição', validators=[NumberRange(0,4)], default=1, render_kw={"id": "constituicao"})
    carisma = IntegerField('Carisma', validators=[NumberRange(0,4)], default=1, render_kw={"id": "carisma"})
    inteligencia = IntegerField('Inteligência', validators=[NumberRange(0,4)], default=1, render_kw={"id": "inteligencia"})
    next = SubmitField('Próximo')

class StepPericiasForm(FlaskForm):
    step = HiddenField(default='3')
    acrobacia = IntegerField('Acrobacia', validators=[NumberRange(0, 2)], default=0)
    adestramento = IntegerField('Adestramento', validators=[NumberRange(0, 2)], default=0)
    artes = IntegerField('Artes', validators=[NumberRange(0, 2)], default=0)
    atletismo = IntegerField('Atletismo', validators=[NumberRange(0, 2)], default=0)
    ciencias = IntegerField('Ciências', validators=[NumberRange(0, 2)], default=0)
    crime = IntegerField('Crime', validators=[NumberRange(0, 2)], default=0)
    enganacao = IntegerField('Enganação', validators=[NumberRange(0, 2)], default=0)
    fortitude = IntegerField('Fortitude', validators=[NumberRange(0, 2)], default=0)
    furtividade = IntegerField('Furtividade', validators=[NumberRange(0, 2)], default=0)
    iniciativa = IntegerField('Iniciativa', validators=[NumberRange(0, 2)], default=0)
    intimidacao = IntegerField('Intimidação', validators=[NumberRange(0, 2)], default=0)
    intuicao = IntegerField('Intuição', validators=[NumberRange(0, 2)], default=0)
    investigacao = IntegerField('Investigação', validators=[NumberRange(0, 2)], default=0)
    luta = IntegerField('Luta', validators=[NumberRange(0, 2)], default=0)
    medicina = IntegerField('Medicina', validators=[NumberRange(0, 2)], default=0)
    oficio = IntegerField('Oficio', validators=[NumberRange(0, 2)], default=0)
    oficio_nome = StringField('oficio_nome', validators=[Length(0, 20)], default='Ofício')
    oficio_atributo = StringField('oficio_atributo', default='inteligencia')
    percepcao = IntegerField('Percepção', validators=[NumberRange(0, 2)], default=0)
    persuasao = IntegerField('Persuasão', validators=[NumberRange(0, 2)], default=0)
    pilotagem = IntegerField('Pilotagem', validators=[NumberRange(0, 2)], default=0)
    pontaria = IntegerField('Pontaria', validators=[NumberRange(0, 2)], default=0)
    reflexos = IntegerField('Reflexos', validators=[NumberRange(0, 2)], default=0)
    religiao = IntegerField('Religião', validators=[NumberRange(0, 2)], default=0)
    sobrevivencia = IntegerField('Sobrevivência', validators=[NumberRange(0, 2)], default=0)
    tatica = IntegerField('Tática', validators=[NumberRange(0, 2)], default=0)
    tecnologia = IntegerField('Tecnologia', validators=[NumberRange(0, 2)], default=0)
    historia = IntegerField('História', validators=[NumberRange(0, 2)], default=0)
    vontade = IntegerField('Vontade', validators=[NumberRange(0, 2)], default=0)
    finish = SubmitField('Finalizar')


class LevelUp_PericiasForm(FlaskForm):
    acrobacia = IntegerField('Acrobacia', validators=[NumberRange(0, 2)], default=0)
    adestramento = IntegerField('Adestramento', validators=[NumberRange(0, 2)], default=0)
    artes = IntegerField('Artes', validators=[NumberRange(0, 2)], default=0)
    atletismo = IntegerField('Atletismo', validators=[NumberRange(0, 2)], default=0)
    ciencias = IntegerField('Ciências', validators=[NumberRange(0, 2)], default=0)
    crime = IntegerField('Crime', validators=[NumberRange(0, 2)], default=0)
    enganacao = IntegerField('Enganação', validators=[NumberRange(0, 2)], default=0)
    fortitude = IntegerField('Fortitude', validators=[NumberRange(0, 2)], default=0)
    furtividade = IntegerField('Furtividade', validators=[NumberRange(0, 2)], default=0)
    iniciativa = IntegerField('Iniciativa', validators=[NumberRange(0, 2)], default=0)
    intimidacao = IntegerField('Intimidação', validators=[NumberRange(0, 2)], default=0)
    intuicao = IntegerField('Intuição', validators=[NumberRange(0, 2)], default=0)
    investigacao = IntegerField('Investigação', validators=[NumberRange(0, 2)], default=0)
    luta = IntegerField('Luta', validators=[NumberRange(0, 2)], default=0)
    medicina = IntegerField('Medicina', validators=[NumberRange(0, 2)], default=0)
    oficio = IntegerField('Oficio', validators=[NumberRange(0, 2)], default=0)
    percepcao = IntegerField('Percepção', validators=[NumberRange(0, 2)], default=0)
    persuasao = IntegerField('Persuasão', validators=[NumberRange(0, 2)], default=0)
    pilotagem = IntegerField('Pilotagem', validators=[NumberRange(0, 2)], default=0)
    pontaria = IntegerField('Pontaria', validators=[NumberRange(0, 2)], default=0)
    reflexos = IntegerField('Reflexos', validators=[NumberRange(0, 2)], default=0)
    religiao = IntegerField('Religião', validators=[NumberRange(0, 2)], default=0)
    sobrevivencia = IntegerField('Sobrevivência', validators=[NumberRange(0, 2)], default=0)
    tatica = IntegerField('Tática', validators=[NumberRange(0, 2)], default=0)
    tecnologia = IntegerField('Tecnologia', validators=[NumberRange(0, 2)], default=0)
    historia = IntegerField('História', validators=[NumberRange(0, 2)], default=0)
    vontade = IntegerField('Vontade', validators=[NumberRange(0, 2)], default=0)
    finish = SubmitField('Finalizar')


class LevelUp_AtributosForm(FlaskForm):
    pontos_max = HiddenField(default=1)
    forca = IntegerField('Força', validators=[NumberRange(0)], render_kw={"id": "forca"})
    destreza = IntegerField('Destreza', validators=[NumberRange(0)], render_kw={"id": "destreza"})
    constituicao = IntegerField('Constituição', validators=[NumberRange(0)], render_kw={"id": "constituicao"})
    carisma = IntegerField('Carisma', validators=[NumberRange(0)], render_kw={"id": "carisma"})
    inteligencia = IntegerField('Inteligência', validators=[NumberRange(0)], render_kw={"id": "inteligencia"})
    finish = SubmitField('Finalizar')


class IniciativaForm(FlaskForm):
    fichas = SelectMultipleField('Fichas', coerce=int, validators=[DataRequired()])
    criar_iniciativa = SubmitField('Criar iniciativa')