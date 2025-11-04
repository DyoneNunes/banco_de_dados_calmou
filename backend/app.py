"""
API Calmou - Backend Flask
Aplicação de saúde mental e bem-estar
"""
import logging
import os
from datetime import timedelta
from logging.handlers import RotatingFileHandler

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from marshmallow import ValidationError

# Imports locais
from config import get_config
from controller import controller_usuario
from model.usuario import Usuario
from model.classificacao_humor import ClassificacaoHumor
from model.resultado_avaliacao import ResultadoAvaliacao
from model.historico_meditacao import HistoricoMeditacao
from schemas import (
    LoginSchema, UsuarioCreateSchema, UsuarioUpdateSchema,
    ClassificacaoHumorSchema, ResultadoAvaliacaoSchema, HistoricoMeditacaoSchema
)

# ==================== CONFIGURAÇÃO DO APP ====================

# Carrega configurações
config = get_config()

app = Flask(__name__)
app.config.from_object(config)

# ==================== LOGGING ESTRUTURADO ====================

# Cria diretório de logs se não existir
os.makedirs('logs', exist_ok=True)

# Configuração do logger
formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)

# Handler para arquivo (com rotação)
file_handler = RotatingFileHandler(
    config.LOG_FILE,
    maxBytes=config.LOG_MAX_BYTES,
    backupCount=config.LOG_BACKUP_COUNT
)
file_handler.setFormatter(formatter)
file_handler.setLevel(getattr(logging, config.LOG_LEVEL))

# Handler para console
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.INFO)

# Configura o logger do app
app.logger.addHandler(file_handler)
app.logger.addHandler(console_handler)
app.logger.setLevel(getattr(logging, config.LOG_LEVEL))

# ==================== EXTENSÕES ====================

# CORS com origens restritas
CORS(app, resources={
    r"/*": {
        "origins": config.CORS_ORIGINS,
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# JWT
jwt = JWTManager(app)

# Rate Limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[config.RATELIMIT_DEFAULT],
    storage_uri=config.RATELIMIT_STORAGE_URL,
    enabled=config.RATELIMIT_ENABLED
)

# ==================== ERROR HANDLERS ====================

@app.errorhandler(ValidationError)
def handle_validation_error(error):
    """Handler para erros de validação do Marshmallow"""
    app.logger.warning(f"Erro de validação: {error.messages}")
    return jsonify({
        'mensagem': 'Erro de validação',
        'erros': error.messages
    }), 400


@app.errorhandler(404)
def not_found(error):
    """Handler para erro 404"""
    return jsonify({'mensagem': 'Recurso não encontrado'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handler para erro 500"""
    app.logger.error(f"Erro interno: {error}")
    return jsonify({'mensagem': 'Erro interno do servidor'}), 500


@app.errorhandler(429)
def ratelimit_handler(error):
    """Handler para erro de rate limit"""
    app.logger.warning(f"Rate limit atingido: {get_remote_address()}")
    return jsonify({
        'mensagem': 'Muitas requisições. Tente novamente mais tarde.'
    }), 429


# ==================== JWT CALLBACKS ====================

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """Callback quando token expirou"""
    return jsonify({
        'mensagem': 'Token expirado',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    """Callback quando token é inválido"""
    return jsonify({
        'mensagem': 'Token inválido',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    """Callback quando token não foi enviado"""
    return jsonify({
        'mensagem': 'Token de autenticação não fornecido',
        'error': 'authorization_required'
    }), 401


# ==================== ROTAS PÚBLICAS ====================

@app.route('/', methods=['GET'])
def index():
    """Rota raiz - Informações da API"""
    return jsonify({
        'app': config.APP_NAME,
        'version': config.APP_VERSION,
        'status': 'online',
        'endpoints': {
            'auth': '/login, /register, /refresh',
            'users': '/usuarios, /perfil',
            'mood': '/humor',
            'meditations': '/meditacoes',
            'meditation_history': '/meditacoes/historico, /meditacoes/estatisticas',
            'assessments': '/avaliacoes',
            'stats': '/stats'
        }
    })


@app.route('/health', methods=['GET'])
def health_check():
    """Health check para monitoramento"""
    return jsonify({'status': 'healthy'}), 200


# ==================== AUTENTICAÇÃO ====================

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # Proteção contra força bruta
def login():
    """
    Endpoint de login com JWT
    ---
    Valida credenciais e retorna access_token e refresh_token
    """
    try:
        # Validação com Marshmallow
        schema = LoginSchema()
        dados = schema.load(request.get_json())

        email = dados['email']
        password = dados['password']

        # Busca usuário
        user_found = controller_usuario.buscar_usuario_por_email(email)

        if not user_found:
            app.logger.warning(f"Tentativa de login com email inexistente: {email}")
            return jsonify({"mensagem": "Credenciais inválidas"}), 401

        # Verifica senha
        if not controller_usuario.verify_password(password, user_found.password_hash):
            app.logger.warning(f"Tentativa de login com senha incorreta: {email}")
            return jsonify({"mensagem": "Credenciais inválidas"}), 401

        # Cria tokens JWT
        access_token = create_access_token(identity=str(user_found.id))
        refresh_token = create_refresh_token(identity=str(user_found.id))

        app.logger.info(f"Login bem-sucedido: {email}")

        return jsonify({
            "mensagem": "Login bem-sucedido!",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "usuario": {
                "id": user_found.id,
                "nome": user_found.nome,
                "email": user_found.email
            }
        }), 200

    except ValidationError as err:
        return jsonify({
            'mensagem': 'Erro de validação',
            'erros': err.messages
        }), 400
    except Exception as e:
        app.logger.error(f"Erro no login: {str(e)}")
        return jsonify({"mensagem": "Erro ao realizar login"}), 500


@app.route('/register', methods=['POST'])
@limiter.limit("3 per minute")  # Limite mais restrito para registro
def register():
    """
    Endpoint de registro de novo usuário
    ---
    Cria conta e retorna tokens JWT
    """
    try:
        # Validação
        schema = UsuarioCreateSchema()
        dados = schema.load(request.get_json())

        # Verifica se email já existe
        existing_user = controller_usuario.buscar_usuario_por_email(dados['email'])
        if existing_user:
            return jsonify({"mensagem": "Email já cadastrado"}), 409

        # Cria usuário
        new_user = Usuario(
            id=None,
            nome=dados['nome'],
            email=dados['email'],
            password=dados['password'],
            config=dados.get('config')
        )

        controller_usuario.inserir_usuario(new_user)

        # Busca usuário criado para pegar o ID
        created_user = controller_usuario.buscar_usuario_por_email(dados['email'])

        # Cria tokens
        access_token = create_access_token(identity=str(created_user.id))
        refresh_token = create_refresh_token(identity=str(created_user.id))

        app.logger.info(f"Novo usuário registrado: {dados['email']}")

        return jsonify({
            "mensagem": "Usuário criado com sucesso!",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "usuario": {
                "id": created_user.id,
                "nome": created_user.nome,
                "email": created_user.email
            }
        }), 201

    except ValidationError as err:
        return jsonify({
            'mensagem': 'Erro de validação',
            'erros': err.messages
        }), 400
    except Exception as e:
        app.logger.error(f"Erro ao criar usuário: {str(e)}")
        return jsonify({"mensagem": f"Erro ao criar usuário: {str(e)}"}), 500


@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Endpoint para renovar access token usando refresh token
    """
    try:
        current_user_id = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user_id)

        return jsonify({
            'access_token': new_access_token
        }), 200

    except Exception as e:
        app.logger.error(f"Erro ao renovar token: {str(e)}")
        return jsonify({'mensagem': 'Erro ao renovar token'}), 500


# ==================== USUÁRIOS (PROTEGIDO) ====================

@app.route('/usuarios', methods=['GET'])
@jwt_required()
def listar_usuarios():
    """
    Lista todos os usuários (protegido)
    Apenas usuários autenticados
    """
    try:
        current_user_id = get_jwt_identity()
        app.logger.info(f"Usuário {current_user_id} listando usuários")

        usuarios = controller_usuario.listar_usuarios()
        usuarios_json = [
            {
                'id': u.id,
                'nome': u.nome,
                'data_cadastro': u.data_cadastro.isoformat() if u.data_cadastro else None
            } for u in usuarios
        ] if usuarios else []

        return jsonify(usuarios_json), 200

    except Exception as e:
        app.logger.error(f"Erro ao listar usuários: {str(e)}")
        return jsonify({"mensagem": "Erro ao listar usuários"}), 500


@app.route('/usuarios/<int:id>', methods=['GET'])
@jwt_required()
def buscar_usuario(id):
    """
    Busca usuário por ID (protegido)
    Usuário só pode ver seus próprios dados
    """
    try:
        current_user_id = int(get_jwt_identity())

        # Verifica se está tentando acessar outro usuário
        if current_user_id != id:
            app.logger.warning(f"Usuário {current_user_id} tentou acessar dados do usuário {id}")
            return jsonify({"mensagem": "Acesso negado"}), 403

        usuario = controller_usuario.buscar_usuario_por_id(id)

        if not usuario:
            return jsonify({"mensagem": "Usuário não encontrado"}), 404

        return jsonify({
            'id': usuario.id,
            'nome': usuario.nome or '',
            'email': usuario.email or '',
            'cpf': usuario.cpf or '',
            'data_nascimento': usuario.data_nascimento.isoformat() if usuario.data_nascimento else None,
            'tipo_sanguineo': usuario.tipo_sanguineo or '',
            'alergias': usuario.alergias or '',
            'data_cadastro': usuario.data_cadastro.isoformat() if usuario.data_cadastro else None,
            'foto_perfil': usuario.foto_perfil or None
        }), 200

    except Exception as e:
        app.logger.error(f"Erro ao buscar usuário: {str(e)}")
        return jsonify({"mensagem": "Erro ao buscar usuário"}), 500


@app.route('/usuarios/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_usuario(id):
    """
    Atualiza usuário (protegido)
    Usuário só pode atualizar seus próprios dados
    """
    try:
        current_user_id = int(get_jwt_identity())

        if current_user_id != id:
            return jsonify({"mensagem": "Acesso negado"}), 403

        schema = UsuarioUpdateSchema()
        dados = schema.load(request.get_json())

        updated_user = Usuario(
            id=id,
            nome=dados.get('nome'),
            email=dados.get('email'),
            password=dados.get('password'),
            config=dados.get('config')
        )

        controller_usuario.atualizar_usuario(updated_user)
        app.logger.info(f"Usuário {id} atualizado")

        return jsonify({"mensagem": "Usuário atualizado com sucesso!"}), 200

    except ValidationError as err:
        return jsonify({'mensagem': 'Erro de validação', 'erros': err.messages}), 400
    except Exception as e:
        app.logger.error(f"Erro ao atualizar usuário: {str(e)}")
        return jsonify({"mensagem": "Erro ao atualizar usuário"}), 500


@app.route('/usuarios/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_usuario(id):
    """
    Remove usuário (protegido)
    Usuário só pode deletar sua própria conta
    """
    try:
        current_user_id = int(get_jwt_identity())

        if current_user_id != id:
            return jsonify({"mensagem": "Acesso negado"}), 403

        controller_usuario.remover_usuario(id)
        app.logger.info(f"Usuário {id} removido")

        return jsonify({"mensagem": "Usuário removido com sucesso!"}), 200

    except Exception as e:
        app.logger.error(f"Erro ao remover usuário: {str(e)}")
        return jsonify({"mensagem": "Erro ao remover usuário"}), 500


@app.route('/usuarios/<int:id>/excluir-conta', methods=['DELETE'])
@jwt_required()
@limiter.limit("3 per minute")  # Proteção contra abuso
def excluir_conta_completa(id):
    """
    Exclui completamente a conta do usuário e todos os seus dados (protegido)

    Esta é uma operação IRREVERSÍVEL que deleta:
    - Todas as classificações de humor
    - Todo o histórico de meditações
    - Todos os resultados de avaliações
    - O registro do usuário

    Requer:
    - Autenticação JWT válida
    - Senha do usuário para confirmação
    - Usuário só pode excluir sua própria conta
    """
    try:
        current_user_id = int(get_jwt_identity())

        # Verifica se está tentando excluir outra conta
        if current_user_id != id:
            app.logger.warning(f"Usuário {current_user_id} tentou excluir conta do usuário {id}")
            return jsonify({"mensagem": "Acesso negado. Você só pode excluir sua própria conta"}), 403

        # Pega a senha do body para validação adicional
        dados = request.get_json()
        if not dados or 'password' not in dados:
            return jsonify({"mensagem": "Senha é obrigatória para confirmar a exclusão da conta"}), 400

        password = dados['password']

        # Busca o usuário para validar a senha
        usuario = controller_usuario.buscar_usuario_por_id(id)
        if not usuario:
            return jsonify({"mensagem": "Usuário não encontrado"}), 404

        # Verifica a senha
        if not controller_usuario.verify_password(password, usuario.password_hash):
            app.logger.warning(f"Tentativa de exclusão de conta com senha incorreta: usuário {id}")
            return jsonify({"mensagem": "Senha incorreta. Exclusão cancelada"}), 401

        # Executa a exclusão completa
        resultado = controller_usuario.excluir_conta_completa(id)

        app.logger.info(f"🗑️  Conta do usuário {id} ({resultado['email']}) excluída completamente")
        app.logger.info(f"📊 Registros removidos: {resultado['registros_removidos']}")

        return jsonify({
            "mensagem": "Conta excluída com sucesso. Todos os seus dados foram removidos permanentemente.",
            "email": resultado['email'],
            "dados_removidos": resultado['registros_removidos']
        }), 200

    except Exception as e:
        app.logger.error(f"Erro ao excluir conta completa: {str(e)}")
        return jsonify({"mensagem": f"Erro ao excluir conta: {str(e)}"}), 500


# ==================== PERFIL ====================

@app.route('/perfil', methods=['PUT'])
@jwt_required()
def atualizar_perfil():
    """
    Atualiza perfil do usuário autenticado
    """
    try:
        current_user_id = int(get_jwt_identity())
        dados = request.get_json()

        if not dados:
            return jsonify({"mensagem": "Payload JSON inválido"}), 400

        usuario_para_atualizar = Usuario(
            id=current_user_id,
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
            app.logger.info(f"Perfil do usuário {current_user_id} atualizado")
            return jsonify({"mensagem": "Perfil atualizado com sucesso!"}), 200
        else:
            return jsonify({"mensagem": "Erro ao atualizar perfil"}), 500

    except Exception as e:
        app.logger.error(f"Erro ao atualizar perfil: {str(e)}")
        return jsonify({"mensagem": f"Erro ao atualizar perfil: {str(e)}"}), 500


# ==================== HUMOR ====================

@app.route('/humor', methods=['POST'])
@jwt_required()
def registrar_humor():
    """
    Registra classificação de humor do usuário autenticado
    """
    try:
        current_user_id = int(get_jwt_identity())

        schema = ClassificacaoHumorSchema()
        dados = schema.load(request.get_json())

        # Verifica se está registrando para si mesmo
        if dados['usuario_id'] != current_user_id:
            return jsonify({"mensagem": "Você só pode registrar seu próprio humor"}), 403

        nova_classificacao = ClassificacaoHumor(
            id=None,
            usuario_id=current_user_id,
            nivel_humor=dados['nivel_humor'],
            sentimento_principal=dados.get('sentimento_principal'),
            notas=dados.get('notas'),
            data_classificacao=None
        )

        controller_usuario.inserir_classificacao_humor(nova_classificacao)
        app.logger.info(f"Humor registrado para usuário {current_user_id}")

        return jsonify({"mensagem": "Registro de humor salvo com sucesso!"}), 201

    except ValidationError as err:
        return jsonify({'mensagem': 'Erro de validação', 'erros': err.messages}), 400
    except Exception as e:
        app.logger.error(f"Erro ao salvar humor: {str(e)}")
        return jsonify({"mensagem": "Erro ao salvar humor"}), 500


@app.route('/humor/relatorio-semanal', methods=['GET'])
@jwt_required()
def relatorio_humor_semanal():
    """
    Retorna relatório semanal de humor do usuário autenticado
    """
    try:
        current_user_id = int(get_jwt_identity())

        dados_relatorio = controller_usuario.relatorio_humor_semanal(current_user_id)

        if dados_relatorio is not None:
            return jsonify(dados_relatorio), 200
        else:
            return jsonify({"mensagem": "Erro ao gerar relatório"}), 500

    except Exception as e:
        app.logger.error(f"Erro ao gerar relatório de humor: {str(e)}")
        return jsonify({"mensagem": "Erro ao gerar relatório"}), 500


# ==================== MEDITAÇÕES ====================

@app.route('/meditacoes', methods=['GET'])
def listar_meditacoes():
    """
    Lista todas as meditações (público)
    """
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

        return jsonify(meditacoes_json), 200

    except Exception as e:
        app.logger.error(f"Erro ao listar meditações: {str(e)}")
        return jsonify({"mensagem": "Erro ao listar meditações"}), 500


@app.route('/meditacoes/<int:id>', methods=['GET'])
def buscar_meditacao(id):
    """
    Busca detalhes de uma meditação específica (público)
    """
    try:
        meditacao = controller_usuario.buscar_meditacao_por_id(id)

        if not meditacao:
            return jsonify({"mensagem": "Meditação não encontrada"}), 404

        return jsonify({
            'id': meditacao.id,
            'titulo': meditacao.titulo,
            'descricao': meditacao.descricao,
            'duracao_minutos': meditacao.duracao_minutos,
            'url_audio': meditacao.url_audio,
            'tipo': meditacao.tipo,
            'categoria': meditacao.categoria,
            'imagem_capa': meditacao.imagem_capa
        }), 200

    except Exception as e:
        app.logger.error(f"Erro ao buscar meditação: {str(e)}")
        return jsonify({"mensagem": "Erro ao buscar meditação"}), 500


# ==================== HISTÓRICO DE MEDITAÇÕES ====================

@app.route('/meditacoes/historico', methods=['POST'])
@jwt_required()
def registrar_meditacao():
    """
    Registra uma meditação concluída pelo usuário autenticado
    """
    try:
        current_user_id = int(get_jwt_identity())

        schema = HistoricoMeditacaoSchema()
        dados = schema.load(request.get_json())

        # Verifica se está registrando para si mesmo
        if dados['usuario_id'] != current_user_id:
            return jsonify({"mensagem": "Você só pode registrar suas próprias meditações"}), 403

        # Verifica se a meditação existe
        meditacao = controller_usuario.buscar_meditacao_por_id(dados['meditacao_id'])
        if not meditacao:
            return jsonify({"mensagem": "Meditação não encontrada"}), 404

        novo_historico = HistoricoMeditacao(
            usuario_id=current_user_id,
            meditacao_id=dados['meditacao_id'],
            duracao_real_minutos=dados['duracao_real_minutos']
        )

        resultado = controller_usuario.registrar_meditacao_concluida(novo_historico)
        app.logger.info(f"Meditação registrada no histórico para usuário {current_user_id}")

        return jsonify({
            "mensagem": "Meditação registrada com sucesso!",
            "historico": resultado
        }), 201

    except ValidationError as err:
        return jsonify({'mensagem': 'Erro de validação', 'erros': err.messages}), 400
    except Exception as e:
        app.logger.error(f"Erro ao registrar meditação: {str(e)}")
        return jsonify({"mensagem": "Erro ao registrar meditação"}), 500


@app.route('/meditacoes/historico', methods=['GET'])
@jwt_required()
def listar_historico():
    """
    Lista o histórico de meditações do usuário autenticado
    Query params:
    - limit: Número máximo de registros (opcional)
    """
    try:
        current_user_id = int(get_jwt_identity())
        limit = request.args.get('limit', type=int)

        historico = controller_usuario.listar_historico_meditacoes(current_user_id, limit)

        if historico is not None:
            return jsonify(historico), 200
        else:
            return jsonify({"mensagem": "Erro ao buscar histórico"}), 500

    except Exception as e:
        app.logger.error(f"Erro ao listar histórico: {str(e)}")
        return jsonify({"mensagem": "Erro ao listar histórico"}), 500


@app.route('/meditacoes/estatisticas', methods=['GET'])
@jwt_required()
def estatisticas_meditacoes():
    """
    Retorna estatísticas de meditações do usuário autenticado
    """
    try:
        current_user_id = int(get_jwt_identity())

        estatisticas = controller_usuario.obter_estatisticas_meditacoes(current_user_id)

        if estatisticas is not None:
            return jsonify(estatisticas), 200
        else:
            return jsonify({"mensagem": "Erro ao buscar estatísticas"}), 500

    except Exception as e:
        app.logger.error(f"Erro ao buscar estatísticas: {str(e)}")
        return jsonify({"mensagem": "Erro ao buscar estatísticas"}), 500


@app.route('/meditacoes/historico/<int:historico_id>', methods=['DELETE'])
@jwt_required()
def remover_historico(historico_id):
    """
    Remove um registro específico do histórico
    Usuário só pode remover seus próprios registros
    """
    try:
        current_user_id = int(get_jwt_identity())

        controller_usuario.remover_historico_meditacao(historico_id, current_user_id)
        app.logger.info(f"Histórico {historico_id} removido pelo usuário {current_user_id}")

        return jsonify({"mensagem": "Registro removido com sucesso!"}), 200

    except Exception as e:
        app.logger.error(f"Erro ao remover histórico: {str(e)}")
        return jsonify({"mensagem": str(e)}), 500


# ==================== AVALIAÇÕES ====================

@app.route('/avaliacoes', methods=['POST'])
@jwt_required()
def salvar_avaliacao():
    """
    Salva resultado de avaliação do usuário autenticado
    """
    try:
        current_user_id = int(get_jwt_identity())

        schema = ResultadoAvaliacaoSchema()
        dados = schema.load(request.get_json())

        # Verifica se está salvando para si mesmo
        if dados['usuario_id'] != current_user_id:
            return jsonify({"mensagem": "Você só pode salvar suas próprias avaliações"}), 403

        novo_resultado = ResultadoAvaliacao(
            id=None,
            usuario_id=current_user_id,
            tipo=dados['tipo'],
            respostas=dados['respostas'],
            resultado_score=dados['resultado_score'],
            resultado_texto=dados.get('resultado_texto')
        )

        controller_usuario.inserir_resultado_avaliacao(novo_resultado)
        app.logger.info(f"Avaliação salva para usuário {current_user_id}")

        return jsonify({"mensagem": "Avaliação salva com sucesso!"}), 201

    except ValidationError as err:
        return jsonify({'mensagem': 'Erro de validação', 'erros': err.messages}), 400
    except Exception as e:
        app.logger.error(f"Erro ao salvar avaliação: {str(e)}")
        return jsonify({"mensagem": "Erro ao salvar avaliação"}), 500


@app.route('/avaliacoes/historico', methods=['GET'])
@jwt_required()
def historico_avaliacoes():
    """
    Retorna histórico de avaliações do usuário autenticado
    """
    try:
        current_user_id = int(get_jwt_identity())

        historico = controller_usuario.listar_avaliacoes_por_usuario(current_user_id)

        if historico is not None:
            return jsonify(historico), 200
        else:
            return jsonify({"mensagem": "Erro ao buscar histórico"}), 500

    except Exception as e:
        app.logger.error(f"Erro ao buscar histórico de avaliações: {str(e)}")
        return jsonify({"mensagem": "Erro ao buscar histórico"}), 500


# ==================== ESTATÍSTICAS ====================

@app.route('/stats', methods=['GET'])
def obter_estatisticas():
    """
    Retorna estatísticas gerais do sistema (público)
    """
    try:
        stats = controller_usuario.get_database_stats()

        if stats is not None:
            return jsonify(stats), 200
        else:
            return jsonify({"mensagem": "Erro ao buscar estatísticas"}), 500

    except Exception as e:
        app.logger.error(f"Erro ao buscar estatísticas: {str(e)}")
        return jsonify({"mensagem": "Erro ao buscar estatísticas"}), 500


# ==================== ARQUIVOS ESTÁTICOS ====================

@app.route('/static/images/<path:filename>')
def serve_static_image(filename):
    """
    Serve arquivos de imagem estáticos
    """
    try:
        static_dir = os.path.join(os.path.dirname(__file__), 'static', 'images')
        return send_from_directory(static_dir, filename)
    except Exception as e:
        app.logger.error(f"Erro ao servir imagem {filename}: {str(e)}")
        return jsonify({"mensagem": "Imagem não encontrada"}), 404


# ==================== INICIALIZAÇÃO ====================

if __name__ == '__main__':
    app.logger.info(f"🚀 Iniciando {config.APP_NAME} v{config.APP_VERSION}")
    app.logger.info(f"🌍 Ambiente: {config.ENV}")
    app.logger.info(f"🔒 Debug: {config.DEBUG}")
    app.logger.info(f"📊 Logging: {config.LOG_LEVEL}")

    app.run(
        host='0.0.0.0',
        port=5001,
        debug=config.DEBUG,
        use_reloader=config.DEBUG  # Hot reload ativado em desenvolvimento
    )
