from flask import Flask, jsonify, request
from controller import controller_usuario
from model.usuario import Usuario  # Importando o modelo para clareza

# Criação do app
app = Flask(__name__)


# --- Endpoint de Login ---
@app.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    if not dados:
        return jsonify({"mensagem": "Payload JSON inválido"}), 400

    email = dados.get('email')
    password = dados.get('password')

    if not email or not password:
        return jsonify({"mensagem": "Email e password são obrigatórios no payload"}), 400

    # Busca o usuário pelo email
    user_found = controller_usuario.buscar_usuario_por_email(email)

    if not user_found:
        return jsonify({"mensagem": "Usuário não encontrado"}), 404

    # ATUALIZADO: Chamando a nova função 'verify_password' e usando o atributo 'password_hash'
    if controller_usuario.verify_password(password, user_found.password_hash):
        return jsonify({
            "mensagem": "Login bem-sucedido!",
            "usuario": {
                "id": user_found.id,
                "nome": user_found.nome,
                "email": user_found.email
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
    # ATUALIZADO: Usando 'password_hash' ao criar o objeto Usuario
    new_user = Usuario(
        id=None,
        nome=dados['nome'],
        email=dados['email'],
        password_hash=dados['password'], # O frontend envia 'password'
        config=dados.get('config')
    )
    controller_usuario.inserir_usuario(new_user)
    return jsonify({"status": "sucesso", "mensagem": "Usuário criado!"}), 201

@app.route('/usuarios/<int:id>', methods=['PUT'])
def put_usuario(id):
    dados = request.get_json()
    # ATUALIZADO: Usando 'password_hash' ao criar o objeto Usuario
    updated_user = Usuario(
        id=id,
        nome=dados['nome'],
        email=dados['email'],
        password_hash=dados.get('password'), # .get() para ser opcional
        config=dados.get('config')
    )
    controller_usuario.atualizar_usuario(updated_user)
    return jsonify({"status": "sucesso", "mensagem": "Usuário atualizado!"})

@app.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    controller_usuario.remover_usuario(id)
    return jsonify({"status": "sucesso", "mensagem": "Usuário removido!"})


# Bloco para rodar a aplicação
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
