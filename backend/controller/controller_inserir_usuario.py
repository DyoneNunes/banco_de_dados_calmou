import bcrypt
from conexao import conectar
from model.usuario import Usuario

# --- FUNÇÕES DE HASH DE SENHA ---
def gerar_hash(senha):
    """Gera um hash seguro para a senha."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(senha.encode('utf-8'), salt)

def verificar_senha(senha_plana, hash_armazenado):
    """Verifica se a senha plana corresponde ao hash armazenado."""
    # O hash do banco vem como string, precisamos converter para bytes
    return bcrypt.checkpw(senha_plana.encode('utf-8'), hash_armazenado.encode('utf-8'))


# --- FUNÇÃO CREATE (MODIFICADA) ---
def inserir_usuario(usuario):
    try:
        conn = conectar()
        cursor = conn.cursor()
        senha_hash = gerar_hash(usuario.senha_hash)
        sql = "INSERT INTO usuarios (nome, email, senha_hash, config) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (usuario.nome, usuario.email, senha_hash, usuario.config))
        conn.commit()
    except Exception as error:
        if conn:
            conn.rollback()
        print(f"Erro ao inserir usuário: {error}")
    finally:
        if conn:
            cursor.close()
            conn.close()

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
            usuario = Usuario(id=linha[0], nome=linha[1], email=linha[2], senha_hash=str(linha[3]), config=linha[4], data_cadastro=linha[5])
            usuarios_lista.append(usuario)
        return usuarios_lista
    except Exception as error:
        print(f"Erro ao listar usuários: {error}")
        return None
    finally:
        if conn:
            cursor.close()
            conn.close()

def buscar_usuario_por_email(email):
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "SELECT * FROM usuarios WHERE email = %s"
        cursor.execute(sql, (email,))
        linha = cursor.fetchone()
        if linha:
            return Usuario(id=linha[0], nome=linha[1], email=linha[2], senha_hash=str(linha[3]), config=linha[4], data_cadastro=linha[5])
        return None
    except Exception as error:
        print(f"Erro ao buscar usuário por email: {error}")
        return None
    finally:
        if conn:
            cursor.close()
            conn.close()

def buscar_usuario_por_id(id):
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "SELECT * FROM usuarios WHERE id = %s"
        cursor.execute(sql, (id,))
        linha = cursor.fetchone()
        if linha:
            return Usuario(id=linha[0], nome=linha[1], email=linha[2], senha_hash=str(linha[3]), config=linha[4], data_cadastro=linha[5])
        return None
    except Exception as error:
        print(f"Erro ao buscar usuário: {error}")
        return None
    finally:
        if conn:
            cursor.close()
            conn.close()

# --- FUNÇÃO UPDATE ---
def atualizar_usuario(usuario):
    try:
        conn = conectar()
        cursor = conn.cursor()
        # Lógica para decidir se a senha deve ser atualizada
        if usuario.senha_hash and usuario.senha_hash != 'senha_nao_alterada':
            senha_hash = gerar_hash(usuario.senha_hash)
            sql = "UPDATE usuarios SET nome = %s, email = %s, senha_hash = %s, config = %s WHERE id = %s"
            params = (usuario.nome, usuario.email, senha_hash, usuario.config, usuario.id)
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