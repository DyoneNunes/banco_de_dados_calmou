from flask import Flask, jsonify, request
from controller import controller_usuario

@app.route('/usuarios/<int:id>', methods=['PUT'])
def put_usuario(id):
    dados = request.get_json()
    usuario_atualizado = controller_usuario.Usuario(
        id=id,
        nome=dados['nome'],
        email=dados['email'],
        senha_hash=dados['senha_hash'],
        config=dados.get('config')
    )
    controller_usuario.atualizar_usuario(usuario_atualizado)
    return jsonify({"status": "sucesso", "mensagem": "Usuário atualizado!"})

app = Flask(__name__)


# 2. AGORA, todos os endpoints (rotas) podem ser definidos
# --- Endpoint para Listar Todos os Usuários ---
@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = controller_usuario.listar_usuarios()
    usuarios_json = []
    if usuarios:
        for usuario in usuarios:
            usuarios_json.append({
                'id': usuario.id,
                'nome': usuario.nome,
                'email': usuario.email,
                'data_cadastro': usuario.data_cadastro
            })
    return jsonify(usuarios_json)

@app.route('/usuarios', methods=['POST'])
def post_usuario():
    dados = request.get_json()
    novo_usuario = controller_usuario.Usuario(
        id=None,
        nome=dados['nome'],
        email=dados['email'],
        senha_hash=dados['senha_hash'],
        config=dados.get('config')
    )
    controller_usuario.inserir_usuario(novo_usuario)
    return jsonify({"status": "sucesso", "mensagem": "Usuário criado!"}), 201

@app.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    controller_usuario.remover_usuario(id)
    return jsonify({"status": "sucesso", "mensagem": "Usuário removido!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

@app.route('/usuarios/<int:id>', methods=['GET'])
def get_usuario_by_id(id):
    usuario = controller_usuario.buscar_usuario_por_id(id)
    if usuario:
        usuario_json = {
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email,
            'data_cadastro': usuario.data_cadastro
        }
        return jsonify(usuario_json)
    return jsonify({"mensagem": "Usuário não encontrado"}), 404