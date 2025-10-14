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
        return conexao
    except (Exception, Error) as error:
        # Este print de erro é importante e deve ficar
        print(f"Erro ao conectar ao PostgreSQL: {error}")
        return None

# Bloco de teste para este arquivo
if __name__ == '__main__':
    conn = conectar()
    if conn:
        print("Teste de conexão direta bem-sucedido!")
        conn.close()
    else:
        print("Teste de conexão direta falhou.")