from flask import render_template, request, flash, redirect, url_for
from src.app import app, users_database, bcrypt
from src.app.models import User, Ficha
from src.app.forms import FormLogin, FormSignup, FormEditProfile, FormCriarFicha, FormLinkDiscord
from flask_login import login_user, logout_user, login_required, current_user
from src.utils.send_dm_discord import send_dm_to_user
from datetime import datetime, timedelta, UTC
from PIL import Image
import os


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit() and 'submit_button_login' in request.form:
        user = User.query.filter_by(username=form_login.account.data).first()
        par_next = request.args.get('next')
        if user and bcrypt.check_password_hash(user.password, form_login.password.data):
            login_user(user, remember=form_login.remember_data.data)
            flash(f'Bem-vindo(a) {form_login.account.data}', 'alert-success')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Falha no login. Usuário ou senha incorretos.', 'alert-danger')
    
    return render_template('login.html', form_login=form_login)

@app.route('/logout')
def logout():
    logout_user()
    flash(f'Desconectado.', 'alert-danger')
    return redirect(url_for('home'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form_signup = FormSignup()
    if form_signup.validate_on_submit() and 'submit_button_signup' in request.form:
        crypt_password = bcrypt.generate_password_hash(form_signup.password.data)
        user = User(username=form_signup.username.data, password=crypt_password)
        users_database.session.add(user)
        users_database.session.commit()
        flash(f'Conta criada com sucesso. Bem-vindo(a) {form_signup.username.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('signup.html', form_signup=form_signup)

@app.route('/players', methods=['GET'])
@login_required
def players():
    pass
    users_list = User.query.all()
    return render_template('players.html', users_list=users_list)

def save_image(old_image, image):
    if old_image != 'default_user_image.jpg':
        old_path = os.path.join(app.root_path, 'static/profile_pictures', old_image)
        if os.path.exists(old_path):
            os.remove(old_path)
    name, extension = os.path.splitext(image.filename)
    extension = extension.lower()
    file_name = current_user.username + extension
    path = os.path.join(app.root_path, 'static/profile_pictures', file_name)
    if extension == '.gif':
        image.save(path)
    else:
        size = (400, 400)
        reduced_image = Image.open(image)
        reduced_image.thumbnail(size)
        reduced_image = reduced_image.convert('RGB')
        reduced_image.save(path)
    return file_name

def rename_profile_image(old_profile_pic, new_username):
    if old_profile_pic == 'default_user_image.jpg':
        return old_profile_pic
    old_path = os.path.join(app.root_path, 'static/profile_pictures', old_profile_pic)
    name, extension = os.path.splitext(old_profile_pic)
    extension = extension.lower()
    new_filename = new_username + extension
    new_path = os.path.join(app.root_path, 'static/profile_pictures', new_filename)
    
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
    
    return new_filename

@app.route('/profile', methods=['GET'])
@login_required
def profile():
    profile_picture = url_for('static', filename=f'profile_pictures/{current_user.profile_picture}')
    return render_template('profile.html', profile_picture=profile_picture)

@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = FormEditProfile()
    if form.validate_on_submit():
        if current_user.username != form.username.data:
            current_user.profile_picture = rename_profile_image(current_user.profile_picture, form.username.data)
            current_user.username = form.username.data
        if form.profile_picture.data:
            image_name = save_image(current_user.profile_picture, form.profile_picture.data)
            current_user.profile_picture = image_name
        users_database.session.commit()
        flash('Perfil atualizado com sucesso.', 'alert-success')
            
        return redirect(url_for('profile'))
    
    elif request.method == "GET":
        form.username.data = current_user.username
    profile_picture = url_for('static', filename=f'profile_pictures/{current_user.profile_picture}')
    return render_template('profile_edit.html', profile_picture=profile_picture, form=form)

@app.route('/ficha', methods=['GET', 'POST'])
def ficha():
    if current_user.id not in Ficha.query.all():
        return redirect(url_for('criarficha'))

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if current_user.discord_id:
        flash('Você já tem um discord configurado.', 'alert-warning')
        return redirect(url_for('home'))
    
    form_verify_discord = FormLinkDiscord()
    if form_verify_discord.validate_on_submit():
        code = send_dm_to_user(form_verify_discord.discord_id.data, 'Seu código de acesso é:')
        current_user.verification_code = code
        current_user.verification_expires = datetime.now(UTC) + timedelta(minutes=10)
        users_database.session.commit()

    if datetime.now(UTC) > current_user.verification_expires:
        print('sifodias')

    return render_template('discord_verify.html', form_verify_discord=form_verify_discord)

@app.route('/criarficha', methods=['GET', 'POST'])
@login_required
def criarficha():
    if current_user.id in Ficha.query.all():
        return redirect(url_for('ficha'))
    if not current_user.discord_id:
        flash('Por favor, verifique seu discord primeiro.', 'alert-warning')
        return redirect(url_for('verify'))
    form = FormCriarFicha()
    if form.validate_on_submit():
        ficha = Ficha(
            nome_personagem=form.nome.data, 
            idade_personagem=form.idade.data
        )
        users_database.session.add(ficha)
        users_database.commit()
        flash('Ficha criada com sucesso', 'alert-success')
        return redirect(url_for('ficha/'))
    return render_template('ficha.html')