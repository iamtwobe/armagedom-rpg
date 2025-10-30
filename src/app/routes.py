from flask import render_template, request, flash, redirect, url_for, jsonify, session
from src.app import app, users_database, bcrypt
from src.app.models import User, Ficha
from src.app.forms import FormLogin, FormSignup, FormEditProfile, FormLinkDiscord, StepNomeForm, StepAtributosForm, StepPericiasForm
from flask_login import login_user, logout_user, login_required, current_user
from src.utils.send_dm_discord import send_dm_to_user
from datetime import datetime, timedelta
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
        login_user(user)
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
        if form.password.data:
            current_user.password = bcrypt.generate_password_hash(form.password.data)      
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


@app.route('/verify', methods=['GET', 'POST'])
@login_required
def verify():
    if current_user.discord_id:
        flash('Você já tem um discord configurado.', 'alert-warning')
        return redirect(url_for('home'))
    
    form_verify_discord = FormLinkDiscord()
    if form_verify_discord.validate_on_submit():
        code = send_dm_to_user(form_verify_discord.discord_id.data, 'Seu código de acesso é:')
        if code.startswith('error'):
            code = code[5:]
            if code == 'offline':
                return jsonify({"error": "O Bot está offline no momento, tente novamente mais tarde."}), 400
            return jsonify({"error": code})
        current_user.verification_code = code
        current_user.verification_expires = datetime.now() + timedelta(minutes=10)
        users_database.session.commit()
        return jsonify({"success": True, "message": "Seu código de acesso foi enviado"}), 200

    else:
        if form_verify_discord.errors:
            for field, errors in form_verify_discord.errors.items():
                for error in errors:
                    if error == 'The CSRF token is missing.':
                        continue
                    return jsonify({"error": error}), 400

    if request.is_json:
        data = request.get_json()
        discord_id = data.get("discord_id")
        code = data.get("verification_code")
        if code == current_user.verification_code and datetime.now() < current_user.verification_expires:
            current_user.discord_id = discord_id
            users_database.session.commit()
            flash('Discord configurado com sucesso!', 'alert-success')
            return jsonify({"redirect": url_for('home')}), 200
        else:
            return jsonify({"error": "Código inválido ou expirado"}), 400

    return render_template('discord_verify.html', form_verify_discord=form_verify_discord)

@app.route('/criarficha', methods=['GET', 'POST'])
@login_required
def criarficha():
    if current_user.id in Ficha.query.all():
        return redirect(url_for('ficha'))
    if not current_user.discord_id:
        flash('Por favor, verifique seu discord primeiro.', 'alert-warning')
        return redirect(url_for('verify'))
    
    step = session.get('step_criar_ficha', 1)

    form1 = StepNomeForm()
    form2 = StepAtributosForm()
    form3 = StepPericiasForm()

    if request.method == 'POST':
        print(request.form)
        posted_step = int(request.form.get('step', step))

        if posted_step != step:
            print('Step:', step, posted_step)
            flash('Fluxo de criação inválido.', 'alert-danger')
            return redirect(url_for('criarficha'))

        if step == 1 and form1.validate_on_submit():
            session['ficha_nome'] = form1.nome_personagem.data
            session['step_criar_ficha'] = 2
            return redirect(url_for('criarficha'))

        if step == 2 and form2.validate_on_submit():
            total = (
                form2.forca.data + form2.destreza.data +
                form2.constituicao.data + form2.carisma.data +
                form2.inteligencia.data
            )
            if total > 12:
                flash("Você gastou mais pontos do que o permitido!", "alert-danger")
                return redirect(url_for('criarficha'))

            session['ficha_forca'] = form2.forca.data
            session['ficha_destreza'] = form2.destreza.data
            session['ficha_constituicao'] = form2.constituicao.data
            session['ficha_carisma'] = form2.carisma.data
            session['ficha_inteligencia'] = form2.inteligencia.data
            session['step_criar_ficha'] = 3
            return redirect(url_for('criarficha'))

        if step == 3 and form3.validate_on_submit():
            for key in list(session.keys()):
                print(key)
                if key.startswith('ficha_') or key == 'step_criar_ficha':
                    session.pop(key)
            return redirect(url_for('criarficha'))
            ficha = Ficha(
                nome_personagem=session.get('ficha_nome'),
                forca=session.get('ficha_forca'),
                destreza=session.get('ficha_destreza'),
                constituicao=session.get('ficha_constituicao'),
                carisma=session.get('ficha_carisma'),
                inteligencia=session.get('ficha_inteligencia'),
                acrobacia=form3.acrobacia.data,
                adestramento=form3.adestramento.data,
                artes=form3.artes.data,
                atletismo=form3.atletismo.data,
                ciencias=form3.ciencias.data,
                crime=form3.crime.data,
                enganacao=form3.enganacao.data,
                fortitude=form3.fortitude.data,
                furtividade=form3.furtividade.data,
                iniciativa=form3.iniciativa.data,
                intimidacao=form3.intimidacao.data,
                intuicao=form3.intuicao.data,
                investigacao=form3.investigacao.data,
                luta=form3.luta.data,
                medicina=form3.medicina.data,
                oficio=form3.oficio.data,
                oficio_nome=form3.oficio_nome.data,
                oficio_atributo=form3.oficio_atributo.data,
                percepcao=form3.percepcao.data,
                persuasao=form3.persuasao.data,
                pilotagem=form3.pilotagem.data,
                pontaria=form3.pontaria.data,
                profissao=form3.profissao.data,
                reflexos=form3.reflexos.data,
                religiao=form3.religiao.data,
                sobrevivencia=form3.sobrevivencia.data,
                tatica=form3.tatica.data,
                tecnologia=form3.tecnologia.data,
                historia=form3.historia.data,
                vontade=form3.vontade.data,
                user_id=current_user.id
            )
            users_database.session.add(ficha)
            users_database.session.commit()

            for key in list(session.keys()):
                if key.startswith('ficha_') or key == 'criar_ficha_etapa':
                    session.pop(key)

            flash('Ficha criada com sucesso!', 'alert-success')
            return redirect(url_for('ficha'))

    step = session.get('step_criar_ficha', 1)
    match step:
        case 1:
            return render_template('ficha/form_nome.html', form1=form1)
        case 2:
            return render_template('ficha/form_atributos.html', form2=form2)
        case 3:
            return render_template('ficha/form_pericias.html', form3=form3)

@app.route('/ficha', methods=['GET'])
@login_required
def ficha_load():
    if current_user.ficha is None:
        return redirect(url_for('criarficha'))
    
    return redirect(url_for('ficha', id_ficha=current_user.ficha.uuid))

@app.route('/ficha/<string:id_ficha>', methods=['GET', 'POST'])
@login_required
def ficha_view(id_ficha):
    ficha = Ficha.query.filter_by(id_ficha=id_ficha).first_or_404()
    if not ficha.visible and ficha.user_id != current_user.id and not current_user.is_admin:
        flash('Você não tem permissão para acessar essa ficha.', 'alert-danger')
        return redirect(url_for('home'))
    
    editable = ficha.user_id == current_user.id or current_user.is_admin

    if request.method == 'POST' and editable:
        ficha.nome_personagem = request.form.get('nome_personagem')
        users_database.session.commit()
        flash('Ficha atualizada com sucesso.', 'alert-success')
        return redirect(url_for('ficha_view', id_ficha=id_ficha))

    return render_template('ficha.html', ficha=ficha, editable=editable)

@app.route('/admin/ficha/<int:id>')
@login_required
def admin_ficha(id):
    if not current_user.is_admin:
        return redirect(url_for('home'))
    ficha = Ficha.query.get_or_404(id)
    return render_template('admin_ficha.html', ficha=ficha)

@app.route('/server_status')
def server_status():
    return jsonify({"status": "online"}), 200