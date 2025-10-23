from flask import Flask, jsonify, request
from controller import controller_usuario
from model.usuario import Usuario
from model.classificacao_humor import ClassificacaoHumor
from model.resultado_avaliacao import ResultadoAvaliacao  # ✅ Import adicionado

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
@app.route('/usuarios', methods=['GET', 'POST'])
def handle_usuarios():
    if request.method == 'POST':
        dados = request.get_json()
        
        # ✅ Validação de campos obrigatórios
        if not dados:
            return jsonify({"mensagem": "Payload JSON inválido"}), 400
        
        nome = dados.get('nome')
        email = dados.get('email')
        password = dados.get('password')
        
        if not nome or not email or not password:
            return jsonify({"mensagem": "Nome, email e password são obrigatórios"}), 400
        
        # ✅ CORREÇÃO: Usar 'password' em vez de 'password_hash'
        new_user = Usuario(
            id=None,
            nome=nome,
            email=email,
            password=password,  # ✅ Corrigido
            config=dados.get('config')
        )
        
        try:
            controller_usuario.inserir_usuario(new_user)
            return jsonify({"status": "sucesso", "mensagem": "Usuário criado!"}), 201
        except Exception as e:
            print(f"Erro ao criar usuário: {str(e)}")
            return jsonify({"mensagem": f"Erro ao criar usuário: {str(e)}"}), 500
    
    else:  # GET
        usuarios = controller_usuario.listar_usuarios()
        # ✅ Removido 'email' da listagem pública por segurança
        usuarios_json = [
            {
                'id': u.id,
                'nome': u.nome,
                'data_cadastro': u.data_cadastro.isoformat() if u.data_cadastro else None
            } for u in usuarios
        ] if usuarios else []
        return jsonify(usuarios_json)


@app.route('/usuarios/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_usuario_by_id(id):
    if request.method == 'PUT':
        dados = request.get_json()
        
        if not dados:
            return jsonify({"mensagem": "Payload JSON inválido"}), 400
        
        # ✅ Validação de campos obrigatórios
        nome = dados.get('nome')
        email = dados.get('email')
        
        if not nome or not email:
            return jsonify({"mensagem": "Nome e email são obrigatórios"}), 400
        
        # ✅ CORREÇÃO: Usar 'password' em vez de 'password_hash'
        updated_user = Usuario(
            id=id,
            nome=nome,
            email=email,
            password=dados.get('password'),  # ✅ Corrigido - None se não fornecido
            config=dados.get('config')
        )
        
        try:
            controller_usuario.atualizar_usuario(updated_user)
            return jsonify({"status": "sucesso", "mensagem": "Usuário atualizado!"})
        except Exception as e:
            print(f"Erro ao atualizar usuário: {str(e)}")
            return jsonify({"mensagem": f"Erro ao atualizar usuário: {str(e)}"}), 500

    elif request.method == 'DELETE':
        try:
            controller_usuario.remover_usuario(id)
            return jsonify({"status": "sucesso", "mensagem": "Usuário removido!"})
        except Exception as e:
            print(f"Erro ao remover usuário: {str(e)}")
            return jsonify({"mensagem": f"Erro ao remover usuário: {str(e)}"}), 500

    else:  # GET
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
            foto_perfil=dados.get('foto_perfil'),  # ✅ Já estava correto
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

    # ✅ CORREÇÃO: Validação melhorada para evitar rejeitar 0
    usuario_id = dados.get('usuario_id')
    nivel_humor = dados.get('nivel_humor')
    
    if usuario_id is None or nivel_humor is None:
        return jsonify({"mensagem": "usuario_id e nivel_humor são obrigatórios"}), 400

    nova_classificacao = ClassificacaoHumor(
        id=None,
        usuario_id=usuario_id,
        nivel_humor=nivel_humor,
        sentimento_principal=dados.get('sentimento_principal'),
        notas=dados.get('notas'),
        data_classificacao=None  # ✅ Explícito (será gerado pelo banco)
    )
    
    try:
        controller_usuario.inserir_classificacao_humor(nova_classificacao)
        return jsonify({"status": "sucesso", "mensagem": "Registro de humor salvo!"}), 201
    except Exception as e:
        print(f"Erro ao salvar humor: {str(e)}")
        return jsonify({"mensagem": f"Erro ao salvar humor: {str(e)}"}), 500


@app.route('/humor/relatorio-semanal/<int:usuario_id>', methods=['GET'])
def get_relatorio_humor(usuario_id):
    try:
        dados_relatorio = controller_usuario.relatorio_humor_semanal(usuario_id)
        if dados_relatorio is not None:
            return jsonify(dados_relatorio)
        else:
            return jsonify({"mensagem": "Erro ao gerar relatório"}), 500
    except Exception as e:
        print(f"Erro ao gerar relatório: {str(e)}")
        return jsonify({"mensagem": f"Erro ao gerar relatório: {str(e)}"}), 500


# --- Endpoints de Meditações ---
@app.route('/meditacoes', methods=['GET'])
def get_meditacoes():
    try:
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
    except Exception as e:
        print(f"Erro ao listar meditações: {str(e)}")
        return jsonify({"mensagem": f"Erro ao listar meditações: {str(e)}"}), 500


@app.route('/meditacoes/<int:id>', methods=['GET'])
def get_meditacao_by_id(id):
    try:
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
    except Exception as e:
        print(f"Erro ao buscar meditação: {str(e)}")
        return jsonify({"mensagem": f"Erro ao buscar meditação: {str(e)}"}), 500


# --- Endpoints de Avaliações ---
@app.route('/avaliacoes', methods=['POST'])
def post_avaliacao():
    dados = request.get_json()
    if not dados:
        return jsonify({"mensagem": "Payload JSON inválido"}), 400

    # ✅ Validação melhorada
    usuario_id = dados.get('usuario_id')
    tipo = dados.get('tipo')
    respostas = dados.get('respostas')
    resultado_score = dados.get('resultado_score')
    
    if not all([
        usuario_id is not None,
        tipo,
        respostas is not None,
        resultado_score is not None
    ]):
        return jsonify({"mensagem": "Campos obrigatórios ausentes (usuario_id, tipo, respostas, resultado_score)"}), 400

    novo_resultado = ResultadoAvaliacao(
        id=None,
        usuario_id=usuario_id,
        tipo=tipo,
        respostas=respostas,
        resultado_score=resultado_score,
        resultado_texto=dados.get('resultado_texto')
    )
    
    try:
        controller_usuario.inserir_resultado_avaliacao(novo_resultado)
        return jsonify({"status": "sucesso", "mensagem": "Avaliação salva com sucesso!"}), 201
    except Exception as e:
        print(f"Erro ao salvar avaliação: {str(e)}")
        return jsonify({"mensagem": f"Erro ao salvar avaliação: {str(e)}"}), 500


@app.route('/avaliacoes/historico/<int:usuario_id>', methods=['GET'])
def get_historico_avaliacoes(usuario_id):
    try:
        historico = controller_usuario.listar_avaliacoes_por_usuario(usuario_id)
        if historico is not None:
            return jsonify(historico)
        else:
            return jsonify({"mensagem": "Erro ao buscar histórico"}), 500
    except Exception as e:
        print(f"Erro ao buscar histórico: {str(e)}")
        return jsonify({"mensagem": f"Erro ao buscar histórico: {str(e)}"}), 500


# --- Endpoint de Estatísticas ---
@app.route('/stats', methods=['GET'])
def get_stats():
    try:
        stats = controller_usuario.get_database_stats()
        if stats is not None:
            return jsonify(stats)
        else:
            return jsonify({"mensagem": "Erro ao buscar estatísticas"}), 500
    except Exception as e:
        print(f"Erro ao buscar estatísticas: {str(e)}")
        return jsonify({"mensagem": f"Erro ao buscar estatísticas: {str(e)}"}), 500


# --- Bloco para rodar a aplicação ---
if __name__ == '__main__':
    # ✅ CORREÇÃO: debug=False em produção
    # Para desenvolvimento local, pode deixar True
    import os
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(host='0.0.0.0', port=5001, debug=debug_mode)