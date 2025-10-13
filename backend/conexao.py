import psycopg2
from psycopg2 import Error

def conectar():
    """
    Função para conectar ao banco de dados PostgreSQL.
    """
    try:
        conexao = psycopg2.connect(
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432",
            database="calmou"
        )
        print("Conexão ao PostgreSQL bem-sucedida!")
        return conexao
    except (Exception, Error) as error:
        print(f"Erro ao conectar ao PostgreSQL: {error}")
        return None

if __name__ == '__main__':
    conn = conectar()
    if conn:
        conn.close()
        print("Conexão ao PostgreSQL foi fechada.")