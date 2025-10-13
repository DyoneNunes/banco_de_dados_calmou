from conexao import conectar
from model.usuario import Usuario

def inserir_usuario(usuario):
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "INSERT INTO usuarios (nome, email, senha_hash, config) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (usuario.nome, usuario.email, usuario.senha_hash, usuario.config))
        conn.commit()
        print("Usuário inserido com sucesso!")
    except Exception as error:
        conn.rollback()
        print(f"Erro ao inserir usuário: {error}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def buscar_usuario_por_id(id):
    """Busca um único usuário pelo seu ID."""
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "SELECT * FROM usuarios WHERE id = %s"
        cursor.execute(sql, (id,))
        linha = cursor.fetchone() # fetchone() pega apenas um resultado
        if linha:
            return Usuario(id=linha[0], nome=linha[1], email=linha[2], senha_hash=linha[3], config=linha[4], data_cadastro=linha[5])
        return None
    except Exception as error:
        print(f"Erro ao buscar usuário: {error}")
        return None
    finally:
        if conn:
            cursor.close()
            conn.close()

def listar_usuarios():
    usuarios_lista = []
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "SELECT * FROM usuarios"
        cursor.execute(sql)
        resultados = cursor.fetchall()
        for linha in resultados:
            usuario = Usuario(id=linha[0], nome=linha[1], email=linha[2], senha_hash=linha[3], config=linha[4], data_cadastro=linha[5])
            usuarios_lista.append(usuario)
        return usuarios_lista
    except Exception as error:
        print(f"Erro ao listar usuários: {error}")
        return None
    finally:
        if conn:
            cursor.close()
            conn.close()

def atualizar_usuario(usuario):
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "UPDATE usuarios SET nome = %s, email = %s, senha_hash = %s, config = %s WHERE id = %s"
        cursor.execute(sql, (usuario.nome, usuario.email, usuario.senha_hash, usuario.config, usuario.id))
        conn.commit()
        print(f"Usuário com ID {usuario.id} atualizado com sucesso!")
    except Exception as error:
        conn.rollback()
        print(f"Erro ao atualizar usuário: {error}")
    finally:
        if conn:
            cursor.close()
            conn.close()


def remover_usuario(id):
    """
    Função para remover um usuário do banco de dados pelo seu ID.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()

        sql = "DELETE FROM usuarios WHERE id = %s"

        cursor.execute(sql, (id,))

        conn.commit()
        print(f"Usuário com ID {id} removido com sucesso!")

    except Exception as error:
        conn.rollback()
        print(f"Erro ao remover usuário: {error}")
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == '__main__':
    
    print("--- Listando usuários ANTES da remoção ---")
    usuarios = listar_usuarios()
    if usuarios:
        for usuario in usuarios:
            print(usuario.to_string())
    
    id_para_remover = 1
    print(f"\n--- Removendo o usuário com ID {id_para_remover} ---")
    remover_usuario(id_para_remover)

    print("\n--- Listando usuários DEPOIS da remoção ---")
    usuarios_depois = listar_usuarios()
    if usuarios_depois:
        if any(u.id == id_para_remover for u in usuarios_depois):
             print(f"ERRO: Usuário com ID {id_para_remover} não foi removido.")
        else:
             print(f"Confirmado: Usuário com ID {id_para_remover} não está mais na lista.")
        for usuario in usuarios_depois:
            print(usuario.to_string())