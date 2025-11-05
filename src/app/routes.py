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
        return redirect(url_for('ficha_load'))
    if not current_user.discord_id:
        flash('Por favor, verifique seu discord primeiro.', 'alert-warning')
        return redirect(url_for('verify'))
    
    step = session.get('step_criar_ficha', 1)

    form_nome = StepNomeForm()
    form_atributos = StepAtributosForm()
    form_pericias = StepPericiasForm()

    if request.method == 'POST':
        posted_step = int(request.form.get('step', step))

        if posted_step != step:
            flash('Fluxo de criação inválido.', 'alert-danger')
            return redirect(url_for('criarficha'))

        if step == 1 and form_nome.validate_on_submit():
            session['ficha_nome'] = form_nome.nome_personagem.data
            session['step_criar_ficha'] = 2
            return redirect(url_for('criarficha'))

        if step == 2 and form_atributos.validate_on_submit():
            total = (
                form_atributos.forca.data + form_atributos.destreza.data +
                form_atributos.constituicao.data + form_atributos.carisma.data +
                form_atributos.inteligencia.data
            )
            if total > int(form_atributos.pontos_max.data):
                flash("Você gastou mais pontos do que o permitido!", "alert-danger")
                return redirect(url_for('criarficha'))

            session['ficha_forca'] = form_atributos.forca.data
            session['ficha_destreza'] = form_atributos.destreza.data
            session['ficha_constituicao'] = form_atributos.constituicao.data
            session['ficha_carisma'] = form_atributos.carisma.data
            session['ficha_inteligencia'] = form_atributos.inteligencia.data
            session['step_criar_ficha'] = 3
            return redirect(url_for('criarficha'))

        if step == 3 and form_pericias.validate_on_submit():
            atributos_map = {
                "For": "forca",
                "Des": "destreza",
                "Con": "constituicao",
                "Car": "carisma",
                "Int": "inteligencia",
            }
            form_pericias.oficio_atributo.data = atributos_map.get(form_pericias.oficio_atributo.data)

            __hp = (6 + (session.get('ficha_constituicao') * 2))

            ficha = Ficha(
                user_id=current_user.id,
                nome_personagem=session.get('ficha_nome'),
                nivel=1,
                vida_maxima=__hp,
                vida_atual=__hp,
                forca=session.get('ficha_forca'),
                destreza=session.get('ficha_destreza'),
                constituicao=session.get('ficha_constituicao'),
                carisma=session.get('ficha_carisma'),
                inteligencia=session.get('ficha_inteligencia'),
                p_acrobacia=form_pericias.acrobacia.data,
                p_adestramento=form_pericias.adestramento.data,
                p_artes=form_pericias.artes.data,
                p_atletismo=form_pericias.atletismo.data,
                p_ciencias=form_pericias.ciencias.data,
                p_crime=form_pericias.crime.data,
                p_enganacao=form_pericias.enganacao.data,
                p_fortitude=form_pericias.fortitude.data,
                p_furtividade=form_pericias.furtividade.data,
                p_iniciativa=form_pericias.iniciativa.data,
                p_intimidacao=form_pericias.intimidacao.data,
                p_intuicao=form_pericias.intuicao.data,
                p_investigacao=form_pericias.investigacao.data,
                p_luta=form_pericias.luta.data,
                p_medicina=form_pericias.medicina.data,
                p_oficio=form_pericias.oficio.data,
                oficio_nome=form_pericias.oficio_nome.data,
                oficio_atributo=form_pericias.oficio_atributo.data,
                p_percepcao=form_pericias.percepcao.data,
                p_persuasao=form_pericias.persuasao.data,
                p_pilotagem=form_pericias.pilotagem.data,
                p_pontaria=form_pericias.pontaria.data,
                p_reflexos=form_pericias.reflexos.data,
                p_religiao=form_pericias.religiao.data,
                p_sobrevivencia=form_pericias.sobrevivencia.data,
                p_tatica=form_pericias.tatica.data,
                p_tecnologia=form_pericias.tecnologia.data,
                p_historia=form_pericias.historia.data,
                p_vontade=form_pericias.vontade.data
            )
            users_database.session.add(ficha)
            users_database.session.commit()

            for key in list(session.keys()):
                if key.startswith('ficha_') or key == 'criar_ficha_etapa' or key == 'step_criar_ficha':
                    session.pop(key)

            flash('Ficha criada com sucesso!', 'alert-success')
            return redirect(url_for('ficha_load'))

    step = session.get('step_criar_ficha', 1)
    match step:
        case 1:
            return render_template('ficha/form_nome.html', form_nome=form_nome)
        case 2:
            return render_template('ficha/form_atributos.html', form_atributos=form_atributos)
        case 3:
            pericias = [
                ("Acrobacia", form_pericias.acrobacia, "Des"),
                ("Adestramento", form_pericias.adestramento, "Int"),
                ("Artes", form_pericias.artes, "Car"),
                ("Atletismo", form_pericias.atletismo, "For"),
                ("Ciências", form_pericias.ciencias, "Int"),
                ("Crime", form_pericias.crime, "Des"),
                ("Enganação", form_pericias.enganacao, "Car"),
                ("Fortitude", form_pericias.fortitude, "Con"),
                ("Furtividade", form_pericias.furtividade, "Des"),
                ("Iniciativa", form_pericias.iniciativa, "Des"),
                ("Intimidação", form_pericias.intimidacao, "Car"),
                ("Intuição", form_pericias.intuicao, "Int"),
                ("Investigação", form_pericias.investigacao, "Int"),
                ("Luta", form_pericias.luta, "For"),
                ("Medicina", form_pericias.medicina, "Int"),
                ("Ofício", form_pericias.oficio, "Int"),
                ("Percepção", form_pericias.percepcao, "Des"),
                ("Persuasão", form_pericias.persuasao, "Car"),
                ("Pilotagem", form_pericias.pilotagem, "Des"),
                ("Pontaria", form_pericias.pontaria, "Des"),
                ("Reflexos", form_pericias.reflexos, "Des"),
                ("Religião", form_pericias.religiao, "Int"),
                ("Sobrevivência", form_pericias.sobrevivencia, "Int"),
                ("Tática", form_pericias.tatica, "Des"),
                ("Tecnologia", form_pericias.tecnologia, "Int"),
                ("História", form_pericias.historia, "Int"),
                ("Vontade", form_pericias.vontade, "Car")
            ]
            return render_template('ficha/form_pericias.html', form_pericias=form_pericias, pericias=pericias)

@app.route('/ficha', methods=['GET'])
@login_required
def ficha_load():
    if current_user.ficha is None:
        return redirect(url_for('criarficha'))
    
    return redirect(url_for('ficha_view', id_ficha=current_user.ficha.uuid))

@app.route('/ficha/<string:id_ficha>', methods=['GET', 'POST'])
@login_required
def ficha_view(id_ficha):
    ficha = Ficha.query.filter_by(uuid=id_ficha).first_or_404()
    if not ficha.visible and ficha.user_id != current_user.id and not current_user.is_admin:
        flash('Você não tem permissão para acessar essa ficha.', 'alert-danger')
        return redirect(url_for('home'))
    
    editable = ficha.user_id == current_user.id or current_user.is_admin

    _pericias = [
        ("Acrobacia", ficha.p_acrobacia, "Des"),
        ("Adestramento", ficha.p_adestramento, "Int"),
        ("Artes", ficha.p_artes, "Car"),
        ("Atletismo", ficha.p_atletismo, "For"),
        ("Ciências", ficha.p_ciencias, "Int"),
        ("Crime", ficha.p_crime, "Des"),
        ("Enganação", ficha.p_enganacao, "Car"),
        ("Fortitude", ficha.p_fortitude, "Con"),
        ("Furtividade", ficha.p_furtividade, "Des"),
        ("Iniciativa", ficha.p_iniciativa, "Des"),
        ("Intimidação", ficha.p_intimidacao, "Car"),
        ("Intuição", ficha.p_intuicao, "Int"),
        ("Investigação", ficha.p_investigacao, "Int"),
        ("Luta", ficha.p_luta, "For"),
        ("Medicina", ficha.p_medicina, "Int"),
        (ficha.oficio_nome, ficha.p_oficio, ficha.oficio_atributo[:3].capitalize()),
        ("Percepção", ficha.p_percepcao, "Des"),
        ("Persuasão", ficha.p_persuasao, "Car"),
        ("Pilotagem", ficha.p_pilotagem, "Des"),
        ("Pontaria", ficha.p_pontaria, "Des"),
        ("Reflexos", ficha.p_reflexos, "Des"),
        ("Religião", ficha.p_religiao, "Int"),
        ("Sobrevivência", ficha.p_sobrevivencia, "Int"),
        ("Tática", ficha.p_tatica, "Des"),
        ("Tecnologia", ficha.p_tecnologia, "Int"),
        ("História", ficha.p_historia, "Int"),
        ("Vontade", ficha.p_vontade, "Car")
    ]

    if request.method == 'POST' and editable:
        if "historia_personagem" in request.form:
            ficha.historia_personagem = request.form.get('historia_personagem')
            ficha.aparencia_personagem = request.form.get('aparencia_personagem')
            ficha.bio_personagem = request.form.get('bio_personagem')
            ficha.favoritos_personagem = request.form.get('favoritos_personagem')
            ficha.defeitos_personagem = request.form.get('defeitos_personagem')
            users_database.session.commit()

        flash('Ficha atualizada com sucesso.', 'alert-success')
        return redirect(url_for('ficha_view', id_ficha=id_ficha))

    return render_template('ficha/ficha.html', ficha=ficha, pericias=_pericias, editable=editable)

@app.route('/api/update_hp/<id_ficha>', methods=["POST"])
def update_hp(id_ficha):
    ficha = Ficha.query.filter_by(id=id_ficha).first()
    if not ficha:
        return jsonify({"error": "Ficha não encontrada"}), 404

    data = request.get_json()
    if not data or "vida_atual" not in data:
        return jsonify({"error": "Dados inválidos"}), 400

    try:
        nova_vida = int(data["vida_atual"])
    except ValueError:
        return jsonify({"error": "Valor inválido"}), 400

    ficha.vida_atual = nova_vida
    users_database.session.commit()

    return jsonify({"success": True, "vida_atual": ficha.vida_atual})

@app.route('/api/update_config/<id_ficha>', methods=["POST"])
def update_config(id_ficha):
    ficha = Ficha.query.filter_by(uuid=id_ficha).first()
    if not ficha:
        flash('Ficha não encontrada.', 'alert-danger')
        return redirect(url_for('ficha_view', id_ficha=id_ficha))

    visible_value = request.form.get("visible")
    dice = request.form.get("dice")


    ficha.visible = True if visible_value == "publica" else False
    ficha.dice = dice or ficha.dice
    users_database.session.commit()

    flash('Ficha atualizada com sucesso.', 'alert-success')
    return redirect(url_for('ficha_view', id_ficha=id_ficha))

@app.route('/admin/ficha/<int:id>')
@login_required
def admin_ficha(id):
    if not current_user.is_admin:
        return redirect(url_for('home'))
    ficha = Ficha.query.get_or_404(id)
    return render_template('admin/admin_ficha.html', ficha=ficha)

@app.route('/server_status')
def server_status():
    return jsonify({"status": "online"}), 200