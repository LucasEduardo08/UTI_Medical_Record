from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from blockchain import BlockchainService
from auth import gerar_token, token_requerido
import os

app = Flask(
    __name__,
    static_folder="../frontend/public",
    static_url_path=""
)

CORS(app)

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

blockchain = BlockchainService()

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'blockchain_connected': blockchain.is_connected()
    })

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    endereco = data.get('endereco')
    private_key = data.get('privateKey')
    
    if not endereco or not private_key:
        return jsonify({'error': 'Credenciais incompletas'}), 400
    
    # Verificar usuário no blockchain
    usuario = blockchain.obter_usuario(endereco)
    
    if not usuario or not usuario['ativo']:
        return jsonify({'error': 'Usuário não autorizado'}), 401
    
    # Gerar token JWT
    token = gerar_token(endereco, usuario['nome'], usuario['cargo'])
    
    return jsonify({
        'token': token,
        'usuario': {
            'endereco': usuario['enderecoCarteira'],
            'nome': usuario['nome'],
            'cargo': usuario['cargo']
        }
    })

@app.route('/api/usuarios', methods=['POST'])
@token_requerido
def criar_usuario():
    data = request.json
    
    # Apenas admin pode criar usuários
    if request.user['cargo'] != 'Admin':
        return jsonify({'error': 'Permissão negada'}), 403
    
    resultado = blockchain.criar_usuario(
        request.user['endereco'],
        os.getenv('PRIVATE_KEY'),  # Usar chave do admin
        data['endereco'],
        data['nome'],
        data['cargo']
    )
    
    return jsonify(resultado)

@app.route('/api/obterusuarios', methods=['GET'])
def listar_usuarios():
    try:
        usuarios = blockchain.obter_todos_usuarios()
        return jsonify(usuarios)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/pacientes', methods=['POST'])
@token_requerido
def criar_paciente():
    data = request.json
    
    resultado = blockchain.criar_paciente(
        request.user['endereco'],
        data['privateKey'],  # Usuário fornece sua chave
        data['nome'],
        data['cpf'],
        data['diagnostico']
    )
    
    return jsonify(resultado)

@app.route('/api/obterpacientes', methods=['GET'])
def listar_pacientes():
    try:
        # Chama a função que já retorna todos os pacientes ativos
        pacientes = blockchain.obter_todos_pacientes()  
        return jsonify(pacientes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/registros', methods=['POST'])
@token_requerido
def adicionar_registro():
    data = request.json
    
    resultado = blockchain.adicionar_registro(
        request.user['endereco'],
        data['privateKey'],
        data['pacienteId'],
        data['tipoRegistro'],
        data['descricao'],
        data['sinaisVitais'],
        data['medicamentos']
    )
    
    return jsonify(resultado)

@app.route('/api/pacientes/<int:paciente_id>/registros', methods=['GET'])
@token_requerido
def obter_registros(paciente_id):
    registros = blockchain.obter_registros_paciente(paciente_id)
    return jsonify(registros)

if __name__ == '__main__':
    app.run(debug=True, port=5000)