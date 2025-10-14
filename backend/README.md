# Backend API

Este é o backend da aplicação, desenvolvido em Python com Flask.

## Pré-requisitos

- Python 3.9+
- pip

## Instalação

1.  **Clone o repositório:**
    ```bash
    git clone <url-do-repositorio>
    cd backend
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    *(No Windows, use `venv\Scripts\activate`)*

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

## Executando a Aplicação

Para iniciar o servidor de desenvolvimento, execute:

```bash
python app.py
```

O servidor estará disponível em `http://0.0.0.0:5001`.

## Dependências

As dependências do projeto estão listadas no arquivo `requirements.txt`:

- blinker==1.9.0
- click==8.1.8
- Flask==3.1.2
- importlib_metadata==8.7.0
- itsdangerous==2.2.0
- Jinja2==3.1.6
- MarkupSafe==3.0.3
- psycopg2-binary==2.9.11
- Werkzeug==3.1.3
- zipp==3.23.0
