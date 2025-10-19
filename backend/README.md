# Backend API Calmou

Este é o backend da aplicação Calmou, desenvolvido em Python com o framework Flask. A API é responsável por gerenciar usuários, registros de humor, meditações e outras funcionalidades da aplicação.

## Pré-requisitos

- Python 3.9+
- pip
- PostgreSQL

## Instalação

1.  **Clone o repositório:**
    ```bash
    git clone <url-do-repositorio>
    cd backend
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Para macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # Para Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuração do Banco de Dados

A aplicação utiliza um banco de dados PostgreSQL. Antes de iniciar o servidor, você precisa ter o PostgreSQL instalado e um banco de dados criado.

1.  **Instale o PostgreSQL** (caso ainda não tenha).
2.  **Crie um banco de dados** chamado `calmou`. Você pode usar o seguinte comando SQL:
    ```sql
    CREATE DATABASE calmou;
    ```
3.  As credenciais de conexão estão definidas no arquivo `conexao.py` e são:
    - **Usuário:** `postgres`
    - **Senha:** `postgres`
    - **Host:** `localhost`
    - **Porta:** `5432`

    Certifique-se de que seu servidor PostgreSQL esteja configurado com essas credenciais ou altere o arquivo `conexao.py` conforme necessário.

## Executando a Aplicação

Com o ambiente virtual ativado e o banco de dados configurado, inicie o servidor de desenvolvimento com o comando:

```bash
python app.py
```

O servidor estará disponível em `http://127.0.0.1:5001`.

## Estrutura do Projeto

-   `app.py`: Arquivo principal que inicializa o Flask e define os endpoints da API.
-   `conexao.py`: Módulo responsável pela conexão com o banco de dados PostgreSQL.
-   `requirements.txt`: Lista de dependências do projeto.
-   `controller/`: Contém a lógica de negócio e as funções que interagem com o banco de dados.
-   `model/`: Contém as classes que representam as entidades do banco de dados (ex: `Usuario`, `Meditacao`).
-   `.env`: Arquivo de exemplo para variáveis de ambiente (atualmente não utilizado pela conexão de banco de dados).