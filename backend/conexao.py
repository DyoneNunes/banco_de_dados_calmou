import psycopg2
from psycopg2 import Error
import os
from dotenv import load_dotenv

# ✅ Carrega variáveis de ambiente do arquivo .env
load_dotenv()

def conectar():
    """
    Função para conectar ao banco de dados PostgreSQL.
    Usa variáveis de ambiente para credenciais de segurança.
    """
    try:
        conexao = psycopg2.connect(
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD"),  # ✅ OBRIGATÓRIO via .env
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", "5432"),
            database=os.getenv("POSTGRES_DB", "calmou")
        )
        return conexao
    except (Exception, Error) as error:
        # Este print de erro é importante e deve ficar
        print(f"❌ Erro ao conectar ao PostgreSQL: {error}")
        return None

# ✅ OPCIONAL: Implementação com pool de conexões (mais eficiente)
# Descomente para usar em produção
"""
from psycopg2 import pool

# Pool de conexões global
connection_pool = None

def inicializar_pool():
    '''Inicializa o pool de conexões.'''
    global connection_pool
    try:
        connection_pool = pool.SimpleConnectionPool(
            1,  # Mínimo de conexões
            20,  # Máximo de conexões
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", "5432"),
            database=os.getenv("POSTGRES_DB", "calmou")
        )
        if connection_pool:
            print("✅ Pool de conexões criado com sucesso!")
    except (Exception, Error) as error:
        print(f"❌ Erro ao criar pool de conexões: {error}")

def conectar_com_pool():
    '''Obtém uma conexão do pool.'''
    global connection_pool
    try:
        if connection_pool is None:
            inicializar_pool()
        
        if connection_pool:
            return connection_pool.getconn()
        return None
    except (Exception, Error) as error:
        print(f"❌ Erro ao obter conexão do pool: {error}")
        return None

def liberar_conexao(conn):
    '''Retorna a conexão ao pool.'''
    global connection_pool
    try:
        if connection_pool and conn:
            connection_pool.putconn(conn)
    except (Exception, Error) as error:
        print(f"❌ Erro ao liberar conexão: {error}")

def fechar_pool():
    '''Fecha todas as conexões do pool.'''
    global connection_pool
    try:
        if connection_pool:
            connection_pool.closeall()
            print("✅ Pool de conexões fechado!")
    except (Exception, Error) as error:
        print(f"❌ Erro ao fechar pool: {error}")
"""

# Bloco de teste para este arquivo
if __name__ == '__main__':
    print("🔍 Testando conexão com o banco de dados...")
    print(f"📍 Conectando em: {os.getenv('POSTGRES_HOST', 'localhost')}:{os.getenv('POSTGRES_PORT', '5432')}")
    print(f"🗄️  Banco de dados: {os.getenv('POSTGRES_DB', 'calmou')}")
    print(f"👤 Usuário: {os.getenv('POSTGRES_USER', 'postgres')}")
    
    conn = conectar()
    if conn:
        print("✅ Teste de conexão direta bem-sucedido!")
        
        # Teste adicional: verifica versão do PostgreSQL
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()
            print(f"🐘 PostgreSQL version: {db_version[0]}")
            cursor.close()
        except Exception as e:
            print(f"⚠️  Não foi possível obter versão do PostgreSQL: {e}")
        
        conn.close()
    else:
        print("❌ Teste de conexão direta falhou.")
        print("\n💡 Dicas:")
        print("   1. Verifique se o PostgreSQL está rodando")
        print("   2. Verifique as credenciais no arquivo .env")
        print("   3. Verifique se o banco 'calmou' existe")