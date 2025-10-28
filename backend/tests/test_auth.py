"""Testes de autenticação"""
import pytest


class TestAuth:
    """Testes para endpoints de autenticação"""

    def test_health_check(self, client):
        """Testa health check"""
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'

    def test_register_success(self, client):
        """Testa registro de usuário com sucesso"""
        user_data = {
            'nome': 'Novo Usuario',
            'email': 'novo@test.com',
            'password': 'senha12345'
        }

        response = client.post('/register', json=user_data)
        assert response.status_code == 201

        data = response.get_json()
        assert 'access_token' in data
        assert 'refresh_token' in data
        assert data['usuario']['email'] == user_data['email']

    def test_register_validation_error(self, client):
        """Testa registro com dados inválidos"""
        # Senha muito curta
        user_data = {
            'nome': 'Test',
            'email': 'test@test.com',
            'password': '123'  # Menos de 8 caracteres
        }

        response = client.post('/register', json=user_data)
        assert response.status_code == 400

        data = response.get_json()
        assert 'erros' in data or 'mensagem' in data

    def test_register_duplicate_email(self, client):
        """Testa registro com email já existente"""
        user_data = {
            'nome': 'Usuario 1',
            'email': 'duplicate@test.com',
            'password': 'senha12345'
        }

        # Primeiro registro
        client.post('/register', json=user_data)

        # Tenta registrar novamente
        response = client.post('/register', json=user_data)
        assert response.status_code == 409  # Conflict

    def test_login_success(self, client):
        """Testa login com credenciais válidas"""
        # Primeiro registra
        user_data = {
            'nome': 'Login Test',
            'email': 'login@test.com',
            'password': 'senha12345'
        }
        client.post('/register', json=user_data)

        # Tenta fazer login
        login_data = {
            'email': user_data['email'],
            'password': user_data['password']
        }

        response = client.post('/login', json=login_data)
        assert response.status_code == 200

        data = response.get_json()
        assert 'access_token' in data
        assert 'refresh_token' in data

    def test_login_invalid_credentials(self, client):
        """Testa login com credenciais inválidas"""
        login_data = {
            'email': 'naoexiste@test.com',
            'password': 'senhaerrada'
        }

        response = client.post('/login', json=login_data)
        assert response.status_code == 401

    def test_refresh_token(self, client):
        """Testa renovação de token"""
        # Registra usuário
        user_data = {
            'nome': 'Refresh Test',
            'email': 'refresh@test.com',
            'password': 'senha12345'
        }
        response = client.post('/register', json=user_data)
        data = response.get_json()
        refresh_token = data['refresh_token']

        # Renova token
        headers = {'Authorization': f'Bearer {refresh_token}'}
        response = client.post('/refresh', headers=headers)

        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
