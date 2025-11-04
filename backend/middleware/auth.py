"""Middleware de autenticação JWT"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError


def jwt_required_custom(optional=False):
    """
    Decorator personalizado para proteger rotas com JWT.

    Args:
        optional (bool): Se True, permite acesso sem token (útil para rotas opcionais)

    Usage:
        @app.route('/protected')
        @jwt_required_custom()
        def protected_route():
            user_id = get_current_user_id()
            return {'user_id': user_id}
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request(optional=optional)
                return fn(*args, **kwargs)
            except NoAuthorizationError:
                return jsonify({
                    'mensagem': 'Token de autenticação não fornecido',
                    'error': 'missing_authorization_header'
                }), 401
            except InvalidHeaderError:
                return jsonify({
                    'mensagem': 'Token de autenticação inválido',
                    'error': 'invalid_header'
                }), 401
            except Exception as e:
                return jsonify({
                    'mensagem': 'Erro ao validar token',
                    'error': str(e)
                }), 401

        return wrapper
    return decorator


def get_current_user_id():
    """
    Retorna o ID do usuário autenticado a partir do token JWT.

    Returns:
        int: ID do usuário

    Raises:
        Exception: Se não houver token válido
    """
    try:
        identity = get_jwt_identity()
        return int(identity)
    except Exception:
        return None


def admin_required():
    """
    Decorator para rotas que exigem permissões de admin.
    Nota: Requer implementação de campo 'role' no modelo de usuário.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            # TODO: Implementar verificação de role quando adicionar campo no banco
            # user_id = get_current_user_id()
            # user = controller_usuario.buscar_usuario_por_id(user_id)
            # if not user or user.role != 'admin':
            #     return jsonify({'mensagem': 'Acesso negado'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
