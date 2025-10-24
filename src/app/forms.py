from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
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
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=8, max=48)])
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
        letters = 'abcdefghijklmnopqrstuvwxyz'
        if any(i in letters for i in password.lower()) == False:
            raise ValidationError('Sua senha precisa conter uma letra.')
        if any(char.isdigit() for char in password) == False:
            raise ValidationError('Sua senha precisa de pelo menos um número')

class FormLinkDiscord(FlaskForm):
    discord_id = StringField('ID do Discord', validators=[DataRequired(), Length(min=17, max=25)])
    submit_button_link_discord = SubmitField('Confirmar')

class FormCriarFicha(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(1, 30)])
    submit_button_ficha = SubmitField('Criar')