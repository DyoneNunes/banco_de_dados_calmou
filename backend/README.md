# 🧘 API Calmou - Backend

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

API REST segura e escalável para aplicativo de saúde mental e bem-estar, com autenticação JWT, validação de dados, rate limiting e logging estruturado.

---

## 📋 Índice

- [Características](#características)
- [Tecnologias](#tecnologias)
- [Instalação](#instalação)
  - [Desenvolvimento Local](#desenvolvimento-local)
  - [Docker](#docker)
- [Configuração](#configuração)
- [Uso](#uso)
- [API Endpoints](#api-endpoints)
- [Autenticação](#autenticação)
- [Testes](#testes)
- [Deploy](#deploy)
- [Segurança](#segurança)
- [Contribuindo](#contribuindo)

---

## ✨ Características

- ✅ **Autenticação JWT** com access e refresh tokens
- ✅ **Validação de schemas** com Marshmallow
- ✅ **Rate limiting** para proteção contra abuse
- ✅ **Logging estruturado** com rotação de arquivos
- ✅ **Connection pooling** do PostgreSQL
- ✅ **CORS configurável** para segurança
- ✅ **Docker** e docker-compose prontos para produção
- ✅ **Testes automatizados** com pytest
- ✅ **Documentação completa** da API

---

## 🛠️ Tecnologias

### Core
- **Python 3.11+**
- **Flask 3.1.2** - Framework web
- **PostgreSQL 16** - Banco de dados
- **psycopg2** - Driver PostgreSQL com connection pooling

### Segurança
- **Flask-JWT-Extended** - Autenticação JWT
- **bcrypt** - Hash de senhas
- **Flask-CORS** - Controle de acesso cross-origin
- **Flask-Limiter** - Rate limiting

### Validação & Qualidade
- **Marshmallow** - Validação de schemas
- **pytest** - Framework de testes
- **email-validator** - Validação de emails

### Deploy
- **Gunicorn** - WSGI server para produção
- **Docker** - Containerização
- **Docker Compose** - Orquestração de containers

---

## 📦 Instalação

### Desenvolvimento Local

#### 1. Clone o repositório
```bash
git clone https://github.com/DyoneNunes/banco_de_dados_calmou.git
cd banco_de_dados_calmou/backend
```

#### 2. Crie um ambiente virtual
```bash
python -m venv .venv

# Linux/Mac
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

#### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

#### 4. Configure as variáveis de ambiente
```bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais
```

Exemplo de `.env`:
```env
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=sua_senha_segura
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=meu_banco

# Flask
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=sua-secret-key-muito-segura
JWT_SECRET_KEY=sua-jwt-secret-key-muito-segura

# CORS
CORS_ORIGINS=http://localhost:8081,http://127.0.0.1:8081

# Rate Limiting
RATELIMIT_ENABLED=True
RATELIMIT_DEFAULT=100 per minute

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

#### 5. Configure o banco de dados
```bash
# Crie o banco de dados
createdb meu_banco

# Execute o script SQL
psql -U postgres -d meu_banco -f calmousql.sql

# Execute a migração de correção (se necessário)
psql -U postgres -d meu_banco -f migration_fix_usuarios.sql
```

#### 6. Inicie o servidor
```bash
python app.py
```

Servidor rodando em: `http://localhost:5001`

---

### Docker

#### 1. Configure o ambiente
```bash
cp .env.example .env
# Edite .env com suas configurações
```

#### 2. Inicie os containers
```bash
# Apenas banco de dados
docker-compose up -d postgres

# Backend + Banco de dados
docker-compose up -d

# Com pgAdmin para gerenciar o banco
docker-compose --profile tools up -d
```

#### 3. Verifique os logs
```bash
docker-compose logs -f backend
```

#### 4. Acesse os serviços
- **API**: `http://localhost:5001`
- **Health Check**: `http://localhost:5001/health`
- **pgAdmin** (se usando profile tools): `http://localhost:5050`

---

## ⚙️ Configuração

### Variáveis de Ambiente

| Variável | Padrão | Descrição |
|----------|---------|-----------|
| `POSTGRES_USER` | postgres | Usuário do PostgreSQL |
| `POSTGRES_PASSWORD` | - | Senha do PostgreSQL (obrigatório) |
| `POSTGRES_HOST` | localhost | Host do PostgreSQL |
| `POSTGRES_PORT` | 5432 | Porta do PostgreSQL |
| `POSTGRES_DB` | meu_banco | Nome do banco de dados |
| `FLASK_ENV` | development | Ambiente (development/production) |
| `FLASK_DEBUG` | False | Modo debug |
| `SECRET_KEY` | - | Chave secreta do Flask |
| `JWT_SECRET_KEY` | - | Chave secreta do JWT |
| `CORS_ORIGINS` | http://localhost:* | Origens permitidas (separadas por vírgula) |
| `RATELIMIT_ENABLED` | True | Habilitar rate limiting |
| `RATELIMIT_DEFAULT` | 100 per minute | Limite padrão de requisições |
| `LOG_LEVEL` | INFO | Nível de logging (DEBUG/INFO/WARNING/ERROR) |
| `LOG_FILE` | logs/app.log | Arquivo de log |

---

## 🚀 Uso

### Registro de Usuário

```bash
curl -X POST http://localhost:5001/register \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "email": "joao@email.com",
    "password": "senha123456"
  }'
```

**Resposta:**
```json
{
  "mensagem": "Usuário criado com sucesso!",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "usuario": {
    "id": 1,
    "nome": "João Silva",
    "email": "joao@email.com"
  }
}
```

### Login

```bash
curl -X POST http://localhost:5001/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao@email.com",
    "password": "senha123456"
  }'
```

### Acessar Endpoint Protegido

```bash
curl -X GET http://localhost:5001/usuarios/1 \
  -H "Authorization: Bearer seu_access_token_aqui"
```

---

## 🔌 API Endpoints

### Autenticação (Público)

| Método | Endpoint | Descrição | Rate Limit |
|--------|----------|-----------|------------|
| `POST` | `/register` | Cria nova conta | 3/min |
| `POST` | `/login` | Autentica usuário | 5/min |
| `POST` | `/refresh` | Renova access token | - |

### Usuários (Protegido)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/usuarios` | Lista usuários |
| `GET` | `/usuarios/<id>` | Busca usuário por ID |
| `PUT` | `/usuarios/<id>` | Atualiza usuário |
| `DELETE` | `/usuarios/<id>` | Remove usuário |
| `PUT` | `/perfil` | Atualiza perfil |

### Humor (Protegido)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/humor` | Registra humor |
| `GET` | `/humor/relatorio-semanal` | Relatório dos últimos 7 dias |

### Meditações (Público)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/meditacoes` | Lista meditações |
| `GET` | `/meditacoes/<id>` | Busca meditação por ID |

### Avaliações (Protegido)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/avaliacoes` | Salva avaliação |
| `GET` | `/avaliacoes/historico` | Histórico de avaliações |

### Utilidades

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/` | Informações da API |
| `GET` | `/health` | Health check |
| `GET` | `/stats` | Estatísticas do sistema |

---

## 🔐 Autenticação

A API usa **JWT (JSON Web Tokens)** para autenticação.

### Fluxo de Autenticação

1. **Registro/Login**: Receba `access_token` e `refresh_token`
2. **Requisições**: Envie `access_token` no header `Authorization: Bearer <token>`
3. **Renovação**: Use `refresh_token` em `/refresh` quando `access_token` expirar

### Tempos de Expiração

- **Access Token**: 1 hora
- **Refresh Token**: 30 dias

### Exemplo de Uso

```python
import requests

# Login
response = requests.post('http://localhost:5001/login', json={
    'email': 'user@email.com',
    'password': 'senha123'
})

tokens = response.json()
access_token = tokens['access_token']

# Requisição autenticada
headers = {'Authorization': f'Bearer {access_token}'}
response = requests.get('http://localhost:5001/usuarios/1', headers=headers)

user_data = response.json()
```

---

## 🧪 Testes

### Executar Testes

```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=. --cov-report=html

# Apenas testes de autenticação
pytest tests/test_auth.py

# Com output detalhado
pytest -v
```

### Estrutura de Testes

```
tests/
├── __init__.py
├── conftest.py           # Configuração e fixtures
├── test_auth.py          # Testes de autenticação
└── test_usuarios.py      # Testes de usuários
```

---

## 🚢 Deploy

### Produção com Docker

```bash
# 1. Configure variáveis de ambiente de produção
cp .env.example .env.production
# Edite .env.production com configurações seguras

# 2. Build da imagem
docker-compose -f docker-compose.yml build

# 3. Inicie em produção
docker-compose -f docker-compose.yml up -d

# 4. Verifique logs
docker-compose logs -f backend
```

### Checklist de Deploy

- [ ] Configurar `SECRET_KEY` e `JWT_SECRET_KEY` únicos
- [ ] Definir `FLASK_ENV=production` e `FLASK_DEBUG=False`
- [ ] Configurar `CORS_ORIGINS` com domínios específicos
- [ ] Usar senhas fortes para PostgreSQL
- [ ] Configurar backup automático do banco
- [ ] Configurar monitoramento e alertas
- [ ] Habilitar HTTPS (nginx/traefik na frente)
- [ ] Revisar limites de rate limiting
- [ ] Configurar rotação de logs

---

## 🔒 Segurança

### Medidas Implementadas

✅ **Autenticação JWT** com tokens de curta duração
✅ **Hash de senhas** com bcrypt (12 rounds)
✅ **Validação de inputs** com Marshmallow
✅ **Rate limiting** contra força bruta
✅ **CORS configurável** para controle de origens
✅ **Prepared statements** contra SQL injection
✅ **Connection pooling** para performance
✅ **Logging estruturado** para auditoria
✅ **Headers de segurança** configurados
✅ **Senhas** com mínimo de 8 caracteres

### Boas Práticas

- Nunca commitar o arquivo `.env`
- Usar HTTPS em produção
- Manter dependências atualizadas
- Monitorar logs regularmente
- Fazer backups frequentes do banco
- Revisar acessos regularmente

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

### Padrões de Código

- Siga PEP 8 para Python
- Adicione testes para novas funcionalidades
- Atualize a documentação conforme necessário
- Use mensagens de commit descritivas

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👨‍💻 Desenvolvedores

- **Derek Cobain** - [derek.cobaindev@gmail.com](mailto:derek.cobaindev@gmail.com)
- **Dyone Andrade** - [andradedyone5@gmail.com](mailto:andradedyone5@gmail.com)

---

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/DyoneNunes/banco_de_dados_calmou/issues)
- **Documentação**: Este README
- **Email**: andradedyone5@gmail.com

---

## 🗺️ Roadmap

- [ ] Implementar WebSockets para notificações em tempo real
- [ ] Adicionar suporte a múltiplos idiomas
- [ ] Implementar sistema de roles e permissões
- [ ] Adicionar upload de imagens para perfil
- [ ] Integrar com serviços de email (SendGrid/SES)
- [ ] Adicionar documentação Swagger/OpenAPI
- [ ] Implementar cache com Redis
- [ ] Adicionar CI/CD com GitHub Actions

---

**⭐ Se este projeto foi útil, considere dar uma estrela no GitHub!**
