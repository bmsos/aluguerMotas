from flask import Flask, render_template, request, redirect, url_for
from flask import session as flask_session 
from models import *
# imports para segurança no upload de imagens
from werkzeug.utils import secure_filename
from uuid import uuid1

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asd98098asa099fsdkfjh8hja'

# não é possivel definir sessao e cliente como variaveis globais, pois flask_session['name'] precisa de um HTTP request ativo
# logo é necessario definir uma função para retornar essas variaveis dentro de uma route
def retornar(string):
    '''Retorna a sessão ou o cliente com o email da sessao, caso existam. Caso contrário retorna None'''
    try:
        sessao = flask_session['name']
        cliente = session.query(Cliente).filter(Cliente.email==flask_session['name']).first()
    except KeyError:
        sessao = cliente = None

    if string == 'sessao':
        return sessao
    elif string == 'cliente':
        return cliente
    else:
        raise ValueError('Wrong argument for "retornar" function. Choose only "sessao" or "cliente"')

# -------------------------- PUBLIC --------------------------------------

@app.route('/')
def index():
    return render_template('public/index.html', session=retornar('sessao'), cliente=retornar('cliente')) 

@app.route('/catalogo')
def catalogo():
    motas = session.query(Mota).all()
    categorias = session.query(Categoria).all()

    return render_template('public/catalogo.html', motas=motas, categorias=categorias, cliente=retornar('cliente'))

@app.route('/profile/<int:mota_id>')
def profile(mota_id):
    mota = session.query(Mota).filter(Mota.id == mota_id).first()
    aluguer = session.query(Aluguer).filter(Aluguer.mota_id==mota_id).first()

    if aluguer is not None:
        data_entrega = str(aluguer.entrega).split(' ')[0]
        hora_entrega = str(aluguer.entrega).split(' ')[1][:-3]

        return render_template('public/profile.html', mota=mota, data_entrega=data_entrega, hora_entrega=hora_entrega, session=retornar('sessao'), cliente=retornar('cliente'))
    else:
        return render_template('public/profile.html', mota=mota, session=retornar('sessao'), cliente=retornar('cliente'))

@app.post('/aluguer')
def aluguer():
    mota_id = request.form['mota_id']
    mota = session.query(Mota).filter(Mota.id==mota_id).first()

    if mota.is_rented == 0:
        
        levantamento = request.form['levantamento']
        entrega = request.form['entrega']

        mota.is_rented = 1
        # criacao novo registo de aluguer
        novoAluguer = Aluguer(levantamento=levantamento, entrega=entrega, cliente_id=retornar('cliente').id, mota_id=mota_id)
        session.add(novoAluguer)
        session.commit()
        data_levantamento = str(novoAluguer.levantamento).split(' ')[0]
        hora_levantamento = str(novoAluguer.levantamento).split(' ')[1][:-3]
        data_entrega = str(novoAluguer.entrega).split(' ')[0]
        hora_entrega = str(novoAluguer.entrega).split(' ')[1][:-3]
        message = f'{mota.marca} {mota.modelo} alugada entre {data_levantamento} ({hora_levantamento}h) e {data_entrega} ({hora_entrega}h).'

        return render_template('public/success.html', 
                               h1InnerHTML='Aluguer confirmado!',
                               pInnerHTML=message,
                               aInnerHTML='Voltar ao catálogo',
                               aHREF='/catalogo',
                               session=retornar('sessao'),
                               cliente=retornar('cliente')
                               )
    else:
        return render_template('public/error.html', 
                               message='Essa mota já se encontra alugada.', 
                               btnInnerHTML='Voltar ao catálogo', 
                               btnHREF='/catalogo',
                               session=retornar('sessao'),
                               cliente=retornar('cliente'))

@app.route('/registo')
def registo():
    return render_template('public/signup.html')

@app.post('/registo')
def registo_post():
    nome = request.form['nome']
    apelido = request.form['apelido']
    email = request.form['email']
    password = request.form['password']

    profile_img = request.files['profile_img']

    # é possível que multiplos users enviem imagens com o mesmo filename
    # uuid adiciona um id unico ao filename para evitar essa possibilidade
    # secure_filename certifica-se que o filename é seguro contra ataques
    profile_img_filename = f'{str(uuid1())}_{secure_filename(profile_img.filename)}'
    profile_img_path = f'private/assets/img/user_profile/{profile_img_filename}'
    profile_img.save(f'static/{profile_img_path}')

    cliente = Cliente(nome=nome, apelido=apelido, email=email, password=password, profile_img=profile_img_path)
    session.add(cliente)
    session.commit()

    return render_template('public/success.html', 
                            h1InnerHTML='Registo confirmado!',
                            pInnerHTML=f'Damos-lhe as boas-vindas à nossa comunidade, {nome}. Já pode entrar na sua conta.',
                            aInnerHTML='Entrar',
                            aHREF='/entrar')

@app.route('/entrar')
def entrar():
    return render_template('public/signin.html')

# -------------------------- PRIVATE --------------------------------------

@app.post('/entrar')
def entrar_post():
    email = request.form['email']
    password = request.form['password']
    cliente= session.query(Cliente).filter(Cliente.email == email, Cliente.password == password).first()
    if cliente:
        flask_session['name'] = email
        return render_template('public/index.html', session=flask_session['name'], cliente=cliente)
    else:
        return render_template('public/signin.html', auth=False)

@app.route('/destroy')
def destroy():
    flask_session.pop('name', None)
    return redirect(url_for('index'))

@app.route('/adicionar-mota')
def adicionar_mota():
    categorias = session.query(Categoria).all()

    if retornar('sessao'):
        return render_template('private/adicionar_mota.html', categorias=categorias, session=retornar('sessao'), cliente=retornar('cliente'))
    else:
        return render_template('public/404.html', session=retornar('sessao'), cliente=retornar('cliente'))
    
@app.post('/adicionar-mota')
def adicionar_mota_post():
    marca=request.form['marca']
    modelo=request.form['modelo']
    cilindrada=request.form['cilindrada']
    ano=request.form['ano']
    custo=request.form['custo']
    categoria_id=request.form['categoria']

    mota = Mota(marca=marca, modelo=modelo, cilindrada=cilindrada, ano=ano, preco=custo, categoria_id=categoria_id)
    session.add(mota)
    session.commit()

    return redirect(url_for('admin_motas'))

@app.route('/admin')
def admin():
    return render_template('private/perfil.html')

@app.route('/admin/motas')
def admin_motas():
    motas = session.query(Mota).all()
    return render_template('private/motas.html', motas=motas)

@app.route('/editar-mota/<int:mota_id>')
def editar_mota(mota_id):
    motas = session.query(Mota).all()
    categorias = session.query(Categoria).all()
    mota = session.query(Mota).filter(Mota.id==mota_id).first()
    return render_template('private/motas.html', motas=motas, mota_selecionada=mota, categorias=categorias)

@app.post('/editar-mota/<int:mota_id>')
def editar_mota_post(mota_id):
    mota = session.query(Mota).filter(Mota.id==mota_id).first()
    marca = request.form['marca']
    modelo = request.form['modelo']
    cilindrada = request.form['cilindrada']
    ano = request.form['ano']
    preco = request.form['custo']
    # categoria = request.form['categoria']    ---- NÃO ESTÁ A SER ENVIADO

    print(f'Form: {request.form}')

    '''
    mota.marca = marca
    mota.modelo = modelo
    mota.cilindrada = cilindrada
    mota.ano = ano
    mota.preco = preco

    session.commit()
    '''
    return redirect(url_for('admin_motas'))

@app.route('/apagar-mota/<int:mota_id>')
def apagar_mota(mota_id):
    session.query(Mota).filter(Mota.id==mota_id).delete(synchronize_session=False)
    return redirect(url_for('admin_motas')) 

if __name__ == '__main__':
    app.run(debug=True)
