import bcrypt
from conexao import conectar
from model.usuario import Usuario

# --- FUNÇÕES DE HASH DE SENHA (RENOMEADAS) ---
def generate_hash(password):
    """Gera um hash seguro para a senha e retorna como string."""
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_bytes.decode('utf-8')

def verify_password(plain_password, stored_hash):
    """Verifica se a senha plana corresponde ao hash armazenado."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), stored_hash.encode('utf-8'))

# --- FUNÇÃO CREATE ---
def inserir_usuario(usuario):
    try:
        conn = conectar()
        cursor = conn.cursor()
        password_hash_str = generate_hash(usuario.password_hash)
        sql = "INSERT INTO usuarios (nome, email, password_hash, config) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (usuario.nome, usuario.email, password_hash_str, usuario.config))
        conn.commit()
    except Exception as error:
        if conn: conn.rollback()
        print(f"Erro ao inserir usuário: {error}")
    finally:
        if conn: cursor.close(); conn.close()

# --- FUNÇÕES READ ---
def listar_usuarios():
    usuarios_lista = []
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "SELECT * FROM usuarios"
        cursor.execute(sql)
        resultados = cursor.fetchall()
        for linha in resultados:
            usuario = Usuario(id=linha[0], nome=linha[1], email=linha[2], password_hash=linha[3], config=linha[4], data_cadastro=linha[5])
            usuarios_lista.append(usuario)
        return usuarios_lista
    except Exception as error:
        print(f"Erro ao listar usuários: {error}")
        return None
    finally:
        if conn: cursor.close(); conn.close()

def buscar_usuario_por_email(email):
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "SELECT * FROM usuarios WHERE email = %s"
        cursor.execute(sql, (email,))
        linha = cursor.fetchone()
        if linha:
            return Usuario(id=linha[0], nome=linha[1], email=linha[2], password_hash=linha[3], config=linha[4], data_cadastro=linha[5])
        return None
    except Exception as error:
        print(f"Erro ao buscar usuário por email: {error}")
        return None
    finally:
        if conn: cursor.close(); conn.close()

def buscar_usuario_por_id(id):
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "SELECT * FROM usuarios WHERE id = %s"
        cursor.execute(sql, (id,))
        linha = cursor.fetchone()
        if linha:
            return Usuario(id=linha[0], nome=linha[1], email=linha[2], password_hash=linha[3], config=linha[4], data_cadastro=linha[5])
        return None
    except Exception as error:
        print(f"Erro ao buscar usuário por id: {error}")
        return None
    finally:
        if conn: cursor.close(); conn.close()

# --- FUNÇÃO UPDATE ---
def atualizar_usuario(usuario):
    try:
        conn = conectar()
        cursor = conn.cursor()
        if usuario.password_hash and usuario.password_hash != 'password_not_changed':
            password_hash = generate_hash(usuario.password_hash)
            sql = "UPDATE usuarios SET nome = %s, email = %s, password_hash = %s, config = %s WHERE id = %s"
            params = (usuario.nome, usuario.email, password_hash, usuario.config, usuario.id)
        else:
            sql = "UPDATE usuarios SET nome = %s, email = %s, config = %s WHERE id = %s"
            params = (usuario.nome, usuario.email, usuario.config, usuario.id)
        
        cursor.execute(sql, params)
        conn.commit()
    except Exception as error:
        if conn:
            conn.rollback()
        print(f"Erro ao atualizar usuário: {error}")
    finally:
        if conn:
            cursor.close()
            conn.close()

# --- FUNÇÃO DELETE ---
def remover_usuario(id):
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "DELETE FROM usuarios WHERE id = %s"
        cursor.execute(sql, (id,))
        conn.commit()
    except Exception as error:
        if conn:
            conn.rollback()
        print(f"Erro ao remover usuário: {error}")
    finally:
        if conn:
            cursor.close()
            conn.close()