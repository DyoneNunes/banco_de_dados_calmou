Arguments
content:
# API Calmou - Backend

API RESTful desenvolvida em Flask para a aplicação "Calmou", uma plataforma de saúde mental e bem-estar.

## Sobre o Projeto

A API gerencia usuários, autenticação, registros de humor, meditações, avaliações de saúde mental e mais. Ela é projetada para ser consumida por um aplicativo frontend, fornecendo todos os dados necessários para a operação da plataforma.

## Pré-requisitos

Antes de começar, certifique-se de ter os seguintes softwares instalados em sua máquina:

- **Python 3.8+**
- **PostgreSQL 12+**
- **pip** (gerenciador de pacotes do Python)

## Configuração do Ambiente

Siga os passos abaixo para configurar o ambiente de desenvolvimento local.

### 1. Clone o Repositório
Com o projeto ja clonado!
### 2. Crie e Ative um Ambiente Virtual


```bash
# Criar o ambiente virtual
python3 -m venv .venv

# Ativar no macOS/Linux
source .venv/bin/activate

# Ativar no Windows
.venv\Scripts\activate
```

### 3. Instale as Dependências

Com o ambiente virtual ativado, instale as bibliotecas Python necessárias:

```bash
pip install -r requirements.txt
```

### 4. Configure o Banco de Dados PostgreSQL

A aplicação requer um banco de dados PostgreSQL.

1.  **Crie o banco de dados**:
    Você pode usar um cliente PostgreSQL como `psql` ou uma ferramenta gráfica como DBeaver/pgAdmin para criar um novo banco de dados. O nome padrão esperado é `meu_banco`.

    ```sql
    CREATE DATABASE meu_banco;
    ```

2.  **Crie as tabelas**:
    Execute o script `calmousql.sql` para criar todas as tabelas e tipos necessários no banco de dados recém-criado.

    ```bash
    psql -U seu_usuario -d meu_banco -f calmousql.sql
    ```
    Substitua `seu_usuario` pelo seu nome de usuário do PostgreSQL.

### 5. Configure as Variáveis de Ambiente

As credenciais do banco de dados e outras configurações são gerenciadas através de um arquivo `.env`.

1.  **Copie o arquivo de exemplo**:

    ```bash
    cp .env.example .env
    ```

2.  **Edite o arquivo `.env`**:
    Abra o arquivo `.env` e preencha com as suas credenciais do PostgreSQL.

    ```ini
    # Credenciais do PostgreSQL
    POSTGRES_USER=seu_usuario_postgres
    POSTGRES_PASSWORD=sua_senha_aqui
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432
    POSTGRES_DB=meu_banco

    # Configurações do Flask
    FLASK_DEBUG=True
    FLASK_ENV=development
    ```

## Execução da Aplicação

Com o ambiente configurado, você pode iniciar o servidor de desenvolvimento do Flask:

```bash
python app.py
```

O servidor estará rodando em `http://127.0.0.1:5001`. Você verá logs no console indicando que a aplicação foi iniciada com sucesso.

## Execução dos Testes

O projeto utiliza `pytest` para testes automatizados. Para rodar a suíte de testes, execute:

```bash
pytest
```

Isso descobrirá e executará todos os testes localizados no diretório `tests/`.

## Estrutura do Projeto

```
.
├── controller/   # Lógica de negócio e acesso ao banco
├── model/        # Classes que representam as entidades do banco
├── schemas/      # Schemas de validação (Marshmallow)
├── tests/        # Testes automatizados
├── .env.example  # Exemplo de arquivo de configuração
├── app.py        # Ponto de entrada da aplicação Flask (rotas)
├── conexao.py    # Gerenciamento da conexão com o banco
├── config.py     # Configurações da aplicação
├── requirements.txt # Dependências do projeto
└── calmousql.sql # Script de criação do banco de dados
```
file_path:
/Users/dyoneandrade/Dev/banco_de_dados_calmou/backend/README.md