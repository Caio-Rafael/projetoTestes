from flask import Flask, request, jsonify, render_template, redirect, url_for
from database import get_db, init_db, add_initial_data, close_connection

app = Flask(__name__)
app.config['DATABASE'] = 'carros.db'

@app.teardown_appcontext
def close_db_connection(exception):
    close_connection(exception)

@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM carros')
    carros = cursor.fetchall()
    return render_template('index.html', carros=carros)

@app.route('/adicionar', methods=['POST'])
def adicionar_carro():
    marca = request.form['marca']
    modelo = request.form['modelo']
    ano = request.form['ano']
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO carros (marca, modelo, ano) VALUES (?, ?, ?)', (marca, modelo, ano))
    db.commit()
    return redirect(url_for('index'))

@app.route('/listar', methods=['GET'])
def listar_carros():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM carros')
    carros = cursor.fetchall()
    return jsonify(carros)

@app.route('/atualizar/<int:id>', methods=['PUT'])
def atualizar_carro(id):
    data = request.get_json()
    marca = data['marca']
    modelo = data['modelo']
    ano = data['ano']
    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE carros SET marca=?, modelo=?, ano=? WHERE id=?', (marca, modelo, ano, id))
    db.commit()
    return jsonify({'message': 'Carro atualizado com sucesso!'})

@app.route('/excluir/<int:id>', methods=['DELETE'])
def excluir_carro(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM carros WHERE id=?', (id,))
    db.commit()
    return jsonify({'message': 'Carro excluído com sucesso!'})

@app.route('/reiniciar', methods=['POST'])
def reiniciar_banco():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DROP TABLE IF EXISTS carros')
    db.commit()
    init_db(app)
    add_initial_data(app)
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        init_db(app)
        add_initial_data(app)
    app.run()
