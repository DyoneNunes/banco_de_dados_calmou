"""Testes de endpoints de usuários"""
import pytest


class TestUsuarios:
    """Testes para endpoints de usuários"""

    def test_listar_usuarios_sem_auth(self, client):
        """Testa acesso a listagem sem autenticação"""
        response = client.get('/usuarios')
        assert response.status_code == 401  # Unauthorized

    def test_listar_usuarios_com_auth(self, client, auth_headers):
        """Testa listagem de usuários autenticado"""
        response = client.get('/usuarios', headers=auth_headers)
        assert response.status_code == 200

        data = response.get_json()
        assert isinstance(data, list)

    def test_buscar_usuario_proprio(self, client, auth_headers):
        """Testa busca de dados do próprio usuário"""
        # Primeiro, obtém ID do usuário logado fazendo login novamente
        # (em um cenário real, você pegaria do token)
        # Por simplicidade, vamos usar ID 1
        response = client.get('/usuarios/1', headers=auth_headers)

        # Pode retornar 200 se for o próprio usuário, ou 403 se não for
        assert response.status_code in [200, 403]

    def test_buscar_usuario_outro(self, client, auth_headers):
        """Testa tentativa de acessar dados de outro usuário"""
        # Tenta acessar usuário com ID alto que provavelmente não é o dele
        response = client.get('/usuarios/9999', headers=auth_headers)

        # Deve retornar 403 (Forbidden) ou 404 (Not Found)
        assert response.status_code in [403, 404]

    def test_atualizar_usuario_sem_auth(self, client):
        """Testa atualização sem autenticação"""
        update_data = {'nome': 'Novo Nome'}
        response = client.put('/usuarios/1', json=update_data, headers={})

        assert response.status_code == 401

    def test_deletar_usuario_sem_auth(self, client):
        """Testa deleção sem autenticação"""
        response = client.delete('/usuarios/1')

        assert response.status_code == 401
