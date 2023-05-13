from flask import url_for, request, redirect, flash
from app.posts import post_bp, delete_bp
from app.extensions import db
from app.models.post import City
import sys
sys.path.insert(0,'C:\\Users\\aluno\\Documents\\wwp\\app\\consultar_cidades')
from consultar_cidades import consultar_cidade

@post_bp.route("/", methods=['POST'])
def index_post():
    nova_cidade = request.form.get('cidade').capitalize()
    err_msg = ''
    if nova_cidade:
        ja_existe = City.query.filter_by(name=nova_cidade).first()

        if not ja_existe:
            consulta_nova_cidade = consultar_cidade.consultarCidade(nova_cidade)
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

    return redirect(url_for('main.index_get'))


@delete_bp.route('/deleta_cidade/<cidade>', methods=['GET','POST'])
def deletar_cidade(cidade):
    cidade_a_deletar = City.query.filter_by(name=cidade).first()
    db.session.delete(cidade_a_deletar)
    db.session.commit()
    flash(f'Cidade {cidade} deletada com sucesso! ')
    return redirect(url_for('main.index_get'))