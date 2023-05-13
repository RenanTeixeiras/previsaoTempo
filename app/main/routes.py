from flask import render_template
from app.main import get_bp
from app.extensions import db
from app.models.post import City

import sys
sys.path.insert(0,'C:\\Users\\aluno\\Documents\\wwp\\app\\consultar_cidades')
from consultar_cidades import consultar_cidade

@get_bp.route('/')
def index_get():
    cidades = City.query.all()
    dados_previsao = []
    dict_traducao = {
        'scattered clouds':'Nuvens Esparsas',
        'clear sky':'Ceu Limpo',
        'broken clouds': 'Parcialmente Nublado',
        'overcast clouds': 'Nuvens Carregadas'
    }
    for cidade in cidades:
        resposta = consultar_cidade.consultarCidade(cidade.name)
        temperatura = {
            'cidade': cidade.name,
            'temperatura': resposta['main']['temp'],
            'descrição' : dict_traducao[f"{resposta['weather'][0]['description']}"]
        }
        dados_previsao.append(temperatura)
        
    return render_template('previsao.html', dados_previsao=dados_previsao)