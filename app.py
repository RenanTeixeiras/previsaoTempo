import requests
import json
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///previsao.db'
app.config['SECRET_KEY'] = 'chavealeatoria'

db = SQLAlchemy(app)
app.app_context().push()

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

db.create_all()
if not City.query.all():
    db.session.add(City(name='Salvador'))
    db.session.commit()

def consultarCidade(cidade):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={cidade}&units=metric&appid=271d1234d3f497eed5b1d80a07b3fcd1'
    resposta = requests.get(url).json()
    return resposta

@app.route('/')
def index_get():
    cidades = City.query.all()
    dados_previsao = []
    dict_traducao = {
        'scattered clouds':'Nuvens Esparsas',
        'clear sky':'Ceu Limpo',
        'broken clouds': 'Parcialmente Nublado'
    }
    for cidade in cidades:
        resposta = consultarCidade(cidade.name)
        temperatura = {
            'cidade': cidade.name,
            'temperatura': resposta['main']['temp'],
            'descrição' : dict_traducao[f"{resposta['weather'][0]['description']}"]
        }
        dados_previsao.append(temperatura)
        
    return render_template('previsao.html', temperatura=temperatura, dados_previsao=dados_previsao)


@app.route("/", methods=['POST'])
def index_post():
    nova_cidade = request.form.get('cidade').capitalize()
    err_msg = ''
    if nova_cidade:
        ja_existe = City.query.filter_by(name=nova_cidade).first()

        if not ja_existe:
            consulta_nova_cidade = consultarCidade(nova_cidade)
            if consulta_nova_cidade['cod'] == 200:
                db.session.add(City(name=nova_cidade))
                db.session.commit()
                
            else:
                err_msg = 'Esta cidade não existe!'
        else:
            err_msg = 'Já existe uma cidade com esse nome!'
    else:
        err_msg = 'Por favor digite uma cidade!'

    if err_msg != '':
        flash(err_msg,'error')
    else:
        flash('Cidade adicionada com sucesso!')

    return redirect(url_for('index_get'))

@app.route('/deleta_cidade/<cidade>', methods=['GET','POST'])
def deletar_cidade(cidade):
    cidade_a_deletar = City.query.filter_by(name=cidade).first()
    db.session.delete(cidade_a_deletar)
    db.session.commit()
    flash(f'Cidade {cidade} deletada com sucesso! ')
    return redirect(url_for('index_get'))


if __name__ == "__main__":
    app.run(debug = True)

