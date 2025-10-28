"""Configuração dos testes pytest"""
import pytest
import os
import sys

# Adiciona o diretório pai ao path para imports funcionarem
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as flask_app


@pytest.fixture
def app():
    """Cria instância da aplicação para testes"""
    flask_app.config.update({
        'TESTING': True,
        'JWT_SECRET_KEY': 'test-secret-key',
        'RATELIMIT_ENABLED': False,  # Desabilita rate limiting nos testes
    })

    yield flask_app


@pytest.fixture
def client(app):
    """Cria cliente de teste"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Cria CLI runner"""
    return app.test_cli_runner()


@pytest.fixture
def auth_headers(client):
    """
    Cria usuário de teste e retorna headers de autenticação
    """
    # Dados do usuário de teste
    test_user = {
        'nome': 'Teste User',
        'email': 'test@test.com',
        'password': 'senha12345'
    }

    # Registra usuário
    response = client.post('/register', json=test_user)
    data = response.get_json()

    # Retorna headers com token
    return {
        'Authorization': f"Bearer {data['access_token']}"
    }
