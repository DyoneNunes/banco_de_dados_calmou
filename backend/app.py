from flask import Flask, jsonify, request
from controller import controller_usuario
from model.usuario import Usuario
from model.classificacao_humor import ClassificacaoHumor
from model.meditacao import Meditacao
from model.resultado_avaliacao import ResultadoAvaliacao

# Criação do app
app = Flask(__name__)


# --- Inicio dos EndPoints ---

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

    user_found = controller_usuario.buscar_usuario_por_email(email)

    if not user_found:
        return jsonify({"mensagem": "Usuário não encontrado"}), 404

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
    usuarios_json = [
        {
            'id': u.id,
            'nome': u.nome,
            'email': u.email,
            'data_cadastro': u.data_cadastro
        } for u in usuarios
    ] if usuarios else []
    return jsonify(usuarios_json)


@app.route('/usuarios/<int:id>', methods=['GET'])
def get_usuario_by_id(id):
    try:
        usuario = controller_usuario.buscar_usuario_por_id(id)
        if usuario:
            data_nasc_str = usuario.data_nascimento.isoformat() if usuario.data_nascimento else None
            data_cadastro_str = usuario.data_cadastro.isoformat() if usuario.data_cadastro else None
            return jsonify({
                'id': usuario.id,
                'nome': usuario.nome or '',
                'email': usuario.email or '',
                'cpf': usuario.cpf or '',
                'data_nascimento': data_nasc_str,
                'tipo_sanguineo': usuario.tipo_sanguineo or '',
                'alergias': usuario.alergias or '',
                'data_cadastro': data_cadastro_str,
                'foto_perfil': usuario.foto_perfil or None
            })
        return jsonify({"mensagem": "Usuário não encontrado"}), 404
    except Exception as e:
        print(f"Erro ao buscar usuário: {str(e)}")
        return jsonify({"mensagem": f"Erro ao buscar usuário: {str(e)}"}), 500


@app.route('/usuarios', methods=['POST'])
def post_usuario():
    dados = request.get_json()
    new_user = Usuario(
        id=None,
        nome=dados['nome'],
        email=dados['email'],
        password_hash=dados['password'],
        config=dados.get('config')
    )
    controller_usuario.inserir_usuario(new_user)
    return jsonify({"status": "sucesso", "mensagem": "Usuário criado!"}), 201


@app.route('/usuarios/<int:id>', methods=['PUT'])
def put_usuario(id):
    dados = request.get_json()
    updated_user = Usuario(
        id=id,
        nome=dados['nome'],
        email=dados['email'],
        password_hash=dados.get('password', 'password_not_changed'),
        config=dados.get('config')
    )
    controller_usuario.atualizar_usuario(updated_user)
    return jsonify({"status": "sucesso", "mensagem": "Usuário atualizado!"})


@app.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    controller_usuario.remover_usuario(id)
    return jsonify({"status": "sucesso", "mensagem": "Usuário removido!"})


# --- Endpoint para Atualizar o Perfil ---
@app.route('/perfil', methods=['PUT'])
def put_perfil():
    try:
        dados = request.get_json()
        
        if not dados:
            return jsonify({"mensagem": "Payload JSON inválido"}), 400
        
        if not dados.get('id'):
            return jsonify({"mensagem": "ID do usuário é obrigatório"}), 400
        
        usuario_para_atualizar = Usuario(
            id=dados.get('id'),
            nome=dados.get('nome'),
            cpf=dados.get('cpf'),
            data_nascimento=dados.get('data_nascimento'),
            tipo_sanguineo=dados.get('tipo_sanguineo'),
            alergias=dados.get('alergias'),
            foto_perfil=dados.get('foto_perfil'),
            email=None,
            password_hash=None
        )
        
        resultado = controller_usuario.atualizar_perfil(usuario_para_atualizar)
        
        if resultado:
            return jsonify({"status": "sucesso", "mensagem": "Perfil atualizado!"})
        else:
            return jsonify({"mensagem": "Erro ao atualizar perfil"}), 500
    
    except Exception as e:
        print(f"Erro ao atualizar perfil: {str(e)}")
        return jsonify({"mensagem": f"Erro ao atualizar perfil: {str(e)}"}), 500


# --- Endpoints de Humor ---
@app.route('/humor', methods=['POST'])
def post_humor():
    dados = request.get_json()
    if not dados:
        return jsonify({"mensagem": "Payload JSON inválido"}), 400

    nova_classificacao = ClassificacaoHumor(
        id=None,
        usuario_id=dados.get('usuario_id'),
        nivel_humor=dados.get('nivel_humor'),
        sentimento_principal=dados.get('sentimento_principal'),
        notas=dados.get('notas')
    )

    if not nova_classificacao.usuario_id or not nova_classificacao.nivel_humor:
        return jsonify({"mensagem": "usuario_id e nivel_humor são obrigatórios"}), 400
    
    controller_usuario.inserir_classificacao_humor(nova_classificacao)
    
    return jsonify({"status": "sucesso", "mensagem": "Registro de humor salvo!"}), 201


@app.route('/humor/relatorio-semanal/<int:usuario_id>', methods=['GET'])
def get_relatorio_humor(usuario_id):
    dados_relatorio = controller_usuario.relatorio_humor_semanal(usuario_id)
    if dados_relatorio is not None:
        return jsonify(dados_relatorio)
    else:
        return jsonify({"mensagem": "Erro ao gerar relatório"}), 500


# --- Endpoints de Meditações ---
@app.route('/meditacoes', methods=['GET'])
def get_meditacoes():
    meditacoes = controller_usuario.listar_meditacoes()
    meditacoes_json = [
        {
            'id': m.id,
            'titulo': m.titulo,
            'categoria': m.categoria,
            'imagem_capa': m.imagem_capa
        } for m in meditacoes
    ] if meditacoes else []
    return jsonify(meditacoes_json)


@app.route('/meditacoes/<int:id>', methods=['GET'])
def get_meditacao_by_id(id):
    meditacao = controller_usuario.buscar_meditacao_por_id(id)
    if meditacao:
        return jsonify({
            'id': meditacao.id,
            'titulo': meditacao.titulo,
            'descricao': meditacao.descricao,
            'duracao_minutos': meditacao.duracao_minutos,
            'url_audio': meditacao.url_audio,
            'tipo': meditacao.tipo,
            'categoria': meditacao.categoria,
            'imagem_capa': meditacao.imagem_capa
        })
    return jsonify({"mensagem": "Meditação não encontrada"}), 404


# --- Endpoints de Avaliações ---
@app.route('/avaliacoes', methods=['POST'])
def post_avaliacao():
    dados = request.get_json()
    if not dados:
        return jsonify({"mensagem": "Payload JSON inválido"}), 400

    novo_resultado = ResultadoAvaliacao(
        id=None,
        usuario_id=dados.get('usuario_id'),
        tipo=dados.get('tipo'),
        respostas=dados.get('respostas'),
        resultado_score=dados.get('resultado_score'),
        resultado_texto=dados.get('resultado_texto')
    )

    if not all([
        novo_resultado.usuario_id,
        novo_resultado.tipo,
        novo_resultado.respostas is not None,
        novo_resultado.resultado_score is not None
    ]):
        return jsonify({"mensagem": "Campos obrigatórios ausentes"}), 400
    
    controller_usuario.inserir_resultado_avaliacao(novo_resultado)
    
    return jsonify({"status": "sucesso", "mensagem": "Avaliação salva com sucesso!"}), 201


@app.route('/avaliacoes/historico/<int:usuario_id>', methods=['GET'])
def get_historico_avaliacoes(usuario_id):
    historico = controller_usuario.listar_avaliacoes_por_usuario(usuario_id)
    if historico is not None:
        return jsonify(historico)
    else:
        return jsonify({"mensagem": "Erro ao buscar histórico"}), 500


# --- Endpoint de Estatísticas ---
@app.route('/stats', methods=['GET'])
def get_stats():
    stats = controller_usuario.get_database_stats()
    if stats is not None:
        return jsonify(stats)
    else:
        return jsonify({"mensagem": "Erro ao buscar estatísticas"}), 500


# --- Bloco para rodar a aplicação ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)