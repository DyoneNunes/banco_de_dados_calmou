from flask import Flask, jsonify, request
from controller import controller_usuario

# 1. A criação do app DEVE VIR PRIMEIRO
app = Flask(__name__)


# 2. AGORA, todos os endpoints (rotas) podem ser definidos
# --- Endpoint de Login ---
@app.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    email = dados.get('email')
    senha = dados.get('senha')

    if not email or not senha:
        return jsonify({"mensagem": "Email e senha são obrigatórios"}), 400

    usuario_encontrado = controller_usuario.buscar_usuario_por_email(email)

    if not usuario_encontrado:
        return jsonify({"mensagem": "Usuário não encontrado"}), 404

    if controller_usuario.verificar_senha(senha, usuario_encontrado.senha_hash):
        return jsonify({
            "mensagem": "Login bem-sucedido!",
            "usuario": {
                "id": usuario_encontrado.id,
                "nome": usuario_encontrado.nome,
                "email": usuario_encontrado.email
            }
        })
    else:
        return jsonify({"mensagem": "Senha incorreta"}), 401

# --- Endpoints de Usuários ---
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

@app.route('/usuarios/<int:id>', methods=['GET'])
def get_usuario_by_id(id):
    usuario = controller_usuario.buscar_usuario_por_id(id)
    if usuario:
        return jsonify({
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email,
            'data_cadastro': usuario.data_cadastro
        })
    return jsonify({"mensagem": "Usuário não encontrado"}), 404

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

@app.route('/usuarios/<int:id>', methods=['PUT'])
def put_usuario(id):
    dados = request.get_json()
    usuario_atualizado = controller_usuario.Usuario(
        id=id,
        nome=dados['nome'],
        email=dados['email'],
        senha_hash=dados.get('senha_hash'), # .get() para ser opcional
        config=dados.get('config')
    )
    controller_usuario.atualizar_usuario(usuario_atualizado)
    return jsonify({"status": "sucesso", "mensagem": "Usuário atualizado!"})

@app.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    controller_usuario.remover_usuario(id)
    return jsonify({"status": "sucesso", "mensagem": "Usuário removido!"})


# 3. O bloco para rodar a aplicação vem por último
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)