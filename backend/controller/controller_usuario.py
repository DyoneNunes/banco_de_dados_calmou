import bcrypt
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash
from conexao import conectar, liberar_conexao
from model.usuario import Usuario
from model.classificacao_humor import ClassificacaoHumor
from model.meditacao import Meditacao
from model.resultado_avaliacao import ResultadoAvaliacao
from model.historico_meditacao import HistoricoMeditacao


# --- FUNÇÕES DE HASH DE SENHA ---
def generate_hash(password):
    """Gera um hash seguro para a senha usando Werkzeug (scrypt)."""
    return generate_password_hash(password)

def verify_password(plain_password, stored_hash):
    """Verifica se a senha plana corresponde ao hash armazenado (Werkzeug/scrypt)."""
    return check_password_hash(stored_hash, plain_password)


# --- FUNÇÕES DE USUÁRIO ---

def inserir_usuario(usuario):
    """Insere um novo usuário no banco de dados."""
    conn = None
    cursor = None
    try:
        conn = conectar()
        if not conn:
            raise Exception("Falha ao conectar ao banco de dados")
        
        cursor = conn.cursor()
        
        # ✅ CORREÇÃO: Usar usuario.password em vez de usuario.password_hash
        if not hasattr(usuario, 'password') or not usuario.password:
            raise ValueError("Senha é obrigatória para criar usuário")
        
        password_hash_str = generate_hash(usuario.password)
        sql = "INSERT INTO usuarios (nome, email, password_hash, config) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (usuario.nome, usuario.email, password_hash_str, usuario.config))
        conn.commit()
        print(f"✅ Usuário {usuario.nome} inserido com sucesso!")
        
    except Exception as error:
        if conn: 
            conn.rollback()
        print(f"❌ Erro ao inserir usuário: {error}")
        raise  # ✅ Re-lança a exceção para o Flask tratar
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexao(conn)

def listar_usuarios():
    """Lista todos os usuários cadastrados."""
    conn = None
    cursor = None
    usuarios_lista = []
    try:
        conn = conectar()
        if not conn:
            raise Exception("Falha ao conectar ao banco de dados")
        
        cursor = conn.cursor()
        sql = "SELECT * FROM usuarios"
        cursor.execute(sql)
        resultados = cursor.fetchall()
        
        for linha in resultados:
            usuario = Usuario(
                id=linha[0], 
                nome=linha[1], 
                email=linha[2], 
                password_hash=linha[3], 
                config=linha[4], 
                data_cadastro=linha[5]
            )
            usuarios_lista.append(usuario)
        return usuarios_lista
        
    except Exception as error:
        print(f"❌ Erro ao listar usuários: {error}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexao(conn)

def buscar_usuario_por_email(email):
    """Busca um usuário pelo email."""
    conn = None
    cursor = None
    try:
        conn = conectar()
        if not conn:
            raise Exception("Falha ao conectar ao banco de dados")
        
        cursor = conn.cursor()
        sql = "SELECT * FROM usuarios WHERE email = %s"
        cursor.execute(sql, (email,))
        linha = cursor.fetchone()
        
        if linha:
            return Usuario(
                id=linha[0], 
                nome=linha[1], 
                email=linha[2], 
                password_hash=linha[3], 
                config=linha[4], 
                data_cadastro=linha[5],
                cpf=linha[6] if len(linha) > 6 else None,
                data_nascimento=linha[7] if len(linha) > 7 else None,
                tipo_sanguineo=linha[8] if len(linha) > 8 else None,
                alergias=linha[9] if len(linha) > 9 else None,
                foto_perfil=linha[10] if len(linha) > 10 else None
            )
        return None
        
    except Exception as error:
        print(f"❌ Erro ao buscar usuário por email: {error}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexao(conn)

def buscar_usuario_por_id(id):
    """Busca um usuário pelo ID."""
    conn = None
    cursor = None
    try:
        conn = conectar()
        if not conn:
            raise Exception("Falha ao conectar ao banco de dados")
        
        cursor = conn.cursor()
        sql = "SELECT * FROM usuarios WHERE id = %s"
        cursor.execute(sql, (id,))
        linha = cursor.fetchone()
        
        if linha:
            return Usuario(
                id=linha[0], 
                nome=linha[1], 
                email=linha[2], 
                password_hash=linha[3], 
                config=linha[4], 
                data_cadastro=linha[5],
                cpf=linha[6] if len(linha) > 6 else None,
                data_nascimento=linha[7] if len(linha) > 7 else None,
                tipo_sanguineo=linha[8] if len(linha) > 8 else None,
                alergias=linha[9] if len(linha) > 9 else None,
                foto_perfil=linha[10] if len(linha) > 10 else None  # ✅ CORREÇÃO: Adicionado foto_perfil
            )
        return None
        
    except Exception as error:
        print(f"❌ Erro ao buscar usuário por id: {error}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexao(conn)

def atualizar_usuario(usuario):
    """Atualiza os dados de um usuário."""
    conn = None
    cursor = None
    try:
        conn = conectar()
        if not conn:
            raise Exception("Falha ao conectar ao banco de dados")
        
        cursor = conn.cursor()
        
        # ✅ CORREÇÃO: Verificar usuario.password em vez de password_hash
        if hasattr(usuario, 'password') and usuario.password:
            password_hash = generate_hash(usuario.password)
            sql = "UPDATE usuarios SET nome = %s, email = %s, password_hash = %s, config = %s WHERE id = %s"
            params = (usuario.nome, usuario.email, password_hash, usuario.config, usuario.id)
        else:
            sql = "UPDATE usuarios SET nome = %s, email = %s, config = %s WHERE id = %s"
            params = (usuario.nome, usuario.email, usuario.config, usuario.id)
        
        cursor.execute(sql, params)
        conn.commit()
        print(f"✅ Usuário ID {usuario.id} atualizado com sucesso!")
        
    except Exception as error:
        if conn: 
            conn.rollback()
        print(f"❌ Erro ao atualizar usuário: {error}")
        raise  # ✅ Re-lança a exceção
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexao(conn)

def atualizar_perfil(usuario):
    """Atualiza apenas os dados do perfil do usuário (não credenciais)."""
    conn = None
    cursor = None
    try:
        conn = conectar()
        if not conn:
            raise Exception("Falha ao conectar ao banco de dados")
        
        cursor = conn.cursor()
        
        # ✅ CORREÇÃO: Adicionado foto_perfil no UPDATE
        sql = """
            UPDATE usuarios 
            SET nome = %s, cpf = %s, data_nascimento = %s, 
                tipo_sanguineo = %s, alergias = %s, foto_perfil = %s
            WHERE id = %s
        """
        
        cursor.execute(sql, (
            usuario.nome,
            usuario.cpf,
            usuario.data_nascimento,
            usuario.tipo_sanguineo,
            usuario.alergias,
            usuario.foto_perfil,  # ✅ CORREÇÃO: Adicionado
            usuario.id
        ))
        
        conn.commit()
        print(f"✅ Perfil atualizado com sucesso para usuário ID: {usuario.id}")
        return True
        
    except Exception as error:
        if conn: 
            conn.rollback()
        print(f"❌ Erro ao atualizar perfil: {error}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexao(conn)

def remover_usuario(id):
    """Remove um usuário do banco de dados."""
    conn = None
    cursor = None
    try:
        conn = conectar()
        if not conn:
            raise Exception("Falha ao conectar ao banco de dados")
        
        cursor = conn.cursor()
        sql = "DELETE FROM usuarios WHERE id = %s"
        cursor.execute(sql, (id,))
        conn.commit()
        print(f"✅ Usuário ID {id} removido com sucesso!")
        
    except Exception as error:
        if conn: 
            conn.rollback()
        print(f"❌ Erro ao remover usuário: {error}")
        raise  # ✅ Re-lança a exceção
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexao(conn)


# --- FUNÇÕES DE HUMOR ---

def inserir_classificacao_humor(classificacao):
    """Insere um novo registro de humor no banco de dados."""
    conn = None
    cursor = None
    try:
        conn = conectar()
        if not conn:
            raise Exception("Falha ao conectar ao banco de dados")
        
        cursor = conn.cursor()
        sql = "INSERT INTO classificacoes_humor (usuario_id, nivel_humor, sentimento_principal, notas) VALUES (%s, %s, %s, %s)"
        
        cursor.execute(sql, (
            classificacao.usuario_id, 
            classificacao.nivel_humor, 
            classificacao.sentimento_principal, 
            classificacao.notas
        ))
        conn.commit()
        print(f"✅ Classificação de humor inserida para usuário ID {classificacao.usuario_id}")
        
    except Exception as error:
        if conn: 
            conn.rollback()
        print(f"❌ Erro ao inserir classificação de humor: {error}")
        raise  # ✅ Re-lança a exceção
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexao(conn)

def relatorio_humor_semanal(usuario_id):
    """Busca as classificações de humor dos últimos 7 dias para um usuário."""
    conn = None
    cursor = None
    registros = []
    try:
        conn = conectar()
        if not conn:
            raise Exception("Falha ao conectar ao banco de dados")
        
        cursor = conn.cursor()
        sql = """
            SELECT data_classificacao, nivel_humor 
            FROM classificacoes_humor
            WHERE usuario_id = %s AND data_classificacao >= current_date - interval '7 days'
            ORDER BY data_classificacao ASC;
        """
        cursor.execute(sql, (usuario_id,))
        resultados = cursor.fetchall()
        
        for linha in resultados:
            registros.append({
                'data': linha[0].strftime('%d/%m'),
                'nivel': linha[1]
            })
        return registros
        
    except Exception as error:
        print(f"❌ Erro ao gerar relatório de humor semanal: {error}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexao(conn)


# --- FUNÇÕES DE MEDITAÇÃO ---

def listar_meditacoes():
    """Busca todas as meditações do catálogo."""
    conn = None
    cursor = None
    meditacoes_lista = []
    try:
        conn = conectar()
        if not conn:
            raise Exception("Falha ao conectar ao banco de dados")
        
        cursor = conn.cursor()
        sql = "SELECT * FROM meditacoes"
        cursor.execute(sql)
        resultados = cursor.fetchall()
        
        for linha in resultados:
            meditacao = Meditacao(
                id=linha[0], 
                titulo=linha[1], 
                descricao=linha[2], 
                duracao_minutos=linha[3], 
                url_audio=linha[4], 
                tipo=linha[5], 
                categoria=linha[6], 
                imagem_capa=linha[7]
            )
            meditacoes_lista.append(meditacao)
        return meditacoes_lista
        
    except Exception as error:
        print(f"❌ Erro ao listar meditações: {error}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexao(conn)

def buscar_meditacao_por_id(id):
    """Busca os detalhes de uma única meditação pelo seu ID."""
    conn = None
    cursor = None
    try:
        conn = conectar()
        if not conn:
            raise Exception("Falha ao conectar ao banco de dados")
        
        cursor = conn.cursor()
        sql = "SELECT * FROM meditacoes WHERE id = %s"
        cursor.execute(sql, (id,))
        linha = cursor.fetchone()
        
        if linha:
            return Meditacao(
                id=linha[0], 
                titulo=linha[1], 
                descricao=linha[2], 
                duracao_minutos=linha[3], 
                url_audio=linha[4], 
                tipo=linha[5], 
                categoria=linha[6], 
                imagem_capa=linha[7]
            )
        return None
        
    except Exception as error:
        print(f"❌ Erro ao buscar meditação: {error}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexao(conn)

def inserir_meditacao(meditacao):
    """Insere uma nova meditação no catálogo."""
    conn = None
    cursor = None
    try:
        conn = conectar()
        if not conn:
            raise Exception("Falha ao conectar ao banco de dados")
        
        cursor = conn.cursor()
        sql = """
            INSERT INTO meditacoes 
            (titulo, descricao, duracao_minutos, url_audio, tipo, categoria, imagem_capa) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(sql, (
            meditacao.titulo,
            meditacao.descricao,
            meditacao.duracao_minutos,
            meditacao.url_audio,
            meditacao.tipo,
            meditacao.categoria,
            meditacao.imagem_capa
        ))
        
        conn.commit()
        print(f"✅ Meditação '{meditacao.titulo}' inserida com sucesso!")
        return True

    except Exception as error:
        if conn:
            conn.rollback()
        print(f"❌ Erro ao inserir meditação: {error}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexao(conn)


# --- FUNÇÕES DE HISTÓRICO DE MEDITAÇÕES ---

def registrar_meditacao_concluida(historico):
    """Registra uma meditação concluída pelo usuário."""
    conn = None
    cursor = None
    try:
        conn = conectar()
        if not conn:
            raise Exception("Falha ao conectar ao banco de dados")

        cursor = conn.cursor()
        sql = """
            INSERT INTO historico_meditacoes
            (usuario_id, meditacao_id, duracao_real_minutos)
            VALUES (%s, %s, %s)
            RETURNING id, data_conclusao
        """

        cursor.execute(sql, (
            historico.usuario_id,
            historico.meditacao_id,
            historico.duracao_real_minutos
        ))

        resultado = cursor.fetchone()
        conn.commit()

        print(f"✅ Meditação registrada no histórico para usuário {historico.usuario_id}")

        # Retorna o ID e data de conclusão gerados
        return {
            'id': resultado[0],
            'data_conclusao': resultado[1].isoformat() if resultado[1] else None
        }

    except Exception as error:
        if conn:
            conn.rollback()
        print(f"❌ Erro ao registrar histórico de meditação: {error}")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexao(conn)


def listar_historico_meditacoes(usuario_id, limit=None):
    """Lista o histórico de meditações de um usuário."""
    conn = None
    cursor = None
    historico_lista = []
    try:
        conn = conectar()
        if not conn:
            raise Exception("Falha ao conectar ao banco de dados")

        cursor = conn.cursor()

        if limit:
            sql = """
                SELECT hm.id, hm.usuario_id, hm.meditacao_id, hm.data_conclusao,
                       hm.duracao_real_minutos, m.titulo, m.descricao, m.duracao_minutos,
                       m.categoria, m.tipo, m.imagem_capa
                FROM historico_meditacoes hm
                JOIN meditacoes m ON hm.meditacao_id = m.id
                WHERE hm.usuario_id = %s
                ORDER BY hm.data_conclusao DESC
                LIMIT %s
            """
            cursor.execute(sql, (usuario_id, limit))
        else:
            sql = """
                SELECT hm.id, hm.usuario_id, hm.meditacao_id, hm.data_conclusao,
                       hm.duracao_real_minutos, m.titulo, m.descricao, m.duracao_minutos,
                       m.categoria, m.tipo, m.imagem_capa
                FROM historico_meditacoes hm
                JOIN meditacoes m ON hm.meditacao_id = m.id
                WHERE hm.usuario_id = %s
                ORDER BY hm.data_conclusao DESC
            """
            cursor.execute(sql, (usuario_id,))

        resultados = cursor.fetchall()

        for linha in resultados:
            historico_lista.append({
                'id': linha[0],
                'usuario_id': linha[1],
                'meditacao_id': linha[2],
                'data_conclusao': linha[3].isoformat() if linha[3] else None,
                'duracao_real_minutos': linha[4],
                'meditacao': {
                    'titulo': linha[5],
                    'descricao': linha[6],
                    'duracao_minutos': linha[7],
                    'categoria': linha[8],
                    'tipo': linha[9],
                    'imagem_capa': linha[10]
                }
            })

        return historico_lista

    except Exception as error:
        print(f"❌ Erro ao listar histórico de meditações: {error}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexao(conn)


def obter_estatisticas_meditacoes(usuario_id):
    """Obtém estatísticas das meditações do usuário."""
    conn = None
    cursor = None
    try:
        conn = conectar()
        if not conn:
            raise Exception("Falha ao conectar ao banco de dados")

        cursor = conn.cursor()

        # Total de meditações concluídas
        cursor.execute("""
            SELECT COUNT(*) FROM historico_meditacoes WHERE usuario_id = %s
        """, (usuario_id,))
        total_meditacoes = cursor.fetchone()[0]

        # Total de minutos meditados
        cursor.execute("""
            SELECT COALESCE(SUM(duracao_real_minutos), 0)
            FROM historico_meditacoes
            WHERE usuario_id = %s
        """, (usuario_id,))
        total_minutos = cursor.fetchone()[0]

        # Categoria mais praticada
        cursor.execute("""
            SELECT m.categoria, COUNT(*) as total
            FROM historico_meditacoes hm
            JOIN meditacoes m ON hm.meditacao_id = m.id
            WHERE hm.usuario_id = %s
            GROUP BY m.categoria
            ORDER BY total DESC
            LIMIT 1
        """, (usuario_id,))
        categoria_result = cursor.fetchone()
        categoria_favorita = categoria_result[0] if categoria_result else None

        # Sequência atual (dias consecutivos)
        cursor.execute("""
            SELECT COUNT(DISTINCT DATE(data_conclusao))
            FROM historico_meditacoes
            WHERE usuario_id = %s
            AND data_conclusao >= CURRENT_DATE - INTERVAL '7 days'
        """, (usuario_id,))
        dias_consecutivos = cursor.fetchone()[0]

        # Última meditação
        cursor.execute("""
            SELECT MAX(data_conclusao)
            FROM historico_meditacoes
            WHERE usuario_id = %s
        """, (usuario_id,))
        ultima_meditacao = cursor.fetchone()[0]

        return {
            'total_meditacoes': total_meditacoes,
            'total_minutos': int(total_minutos),
            'categoria_favorita': categoria_favorita,
            'dias_consecutivos_ultima_semana': dias_consecutivos,
            'ultima_meditacao': ultima_meditacao.isoformat() if ultima_meditacao else None
        }

    except Exception as error:
        print(f"❌ Erro ao obter estatísticas de meditações: {error}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexao(conn)


def remover_historico_meditacao(historico_id, usuario_id):
    """Remove um registro específico do histórico (apenas do próprio usuário)."""
    conn = None
    cursor = None
    try:
        conn = conectar()
        if not conn:
            raise Exception("Falha ao conectar ao banco de dados")

        cursor = conn.cursor()

        # Verifica se o histórico pertence ao usuário antes de deletar
        sql = """
            DELETE FROM historico_meditacoes
            WHERE id = %s AND usuario_id = %s
            RETURNING id
        """
        cursor.execute(sql, (historico_id, usuario_id))
        resultado = cursor.fetchone()

        if not resultado:
            raise Exception("Histórico não encontrado ou não pertence ao usuário")

        conn.commit()
        print(f"✅ Histórico ID {historico_id} removido com sucesso")
        return True

    except Exception as error:
        if conn:
            conn.rollback()
        print(f"❌ Erro ao remover histórico de meditação: {error}")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexao(conn)


# --- FUNÇÕES DE AVALIAÇÃO ---

def inserir_resultado_avaliacao(resultado):
    """Insere o resultado de uma avaliação no banco de dados."""
    conn = None
    cursor = None
    try:
        conn = conectar()
        if not conn:
            raise Exception("Falha ao conectar ao banco de dados")
        
        cursor = conn.cursor()
        
        # O campo 'respostas' é JSONB, então podemos passar o dicionário diretamente
        sql = """
            INSERT INTO resultados_avaliacoes 
            (usuario_id, tipo, respostas, resultado_score, resultado_texto) 
            VALUES (%s, %s, %s, %s, %s)
        """
        
        cursor.execute(sql, (
            resultado.usuario_id,
            resultado.tipo,
            psycopg2.extras.Json(resultado.respostas),  # Converte dict para JSONB
            resultado.resultado_score,
            resultado.resultado_texto
        ))
        conn.commit()
        print(f"✅ Avaliação salva com sucesso para usuário {resultado.usuario_id}")
        
    except Exception as error:
        if conn: 
            conn.rollback()
        print(f"❌ Erro ao inserir resultado da avaliação: {error}")
        raise  # ✅ Re-lança a exceção
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexao(conn)

def buscar_avaliacoes_usuario(usuario_id, tipo=None):
    """Busca todas as avaliações de um usuário, opcionalmente filtradas por tipo."""
    conn = None
    cursor = None
    avaliacoes = []
    try:
        conn = conectar()
        if not conn:
            raise Exception("Falha ao conectar ao banco de dados")
        
        cursor = conn.cursor()
        
        if tipo:
            sql = """
                SELECT id, usuario_id, tipo, respostas, resultado_score, resultado_texto, data_avaliacao
                FROM resultados_avaliacoes
                WHERE usuario_id = %s AND tipo = %s
                ORDER BY data_avaliacao DESC
            """
            cursor.execute(sql, (usuario_id, tipo))
        else:
            sql = """
                SELECT id, usuario_id, tipo, respostas, resultado_score, resultado_texto, data_avaliacao
                FROM resultados_avaliacoes
                WHERE usuario_id = %s
                ORDER BY data_avaliacao DESC
            """
            cursor.execute(sql, (usuario_id,))
        
        resultados = cursor.fetchall()
        for linha in resultados:
            avaliacoes.append({
                'id': linha[0],
                'usuario_id': linha[1],
                'tipo': linha[2],
                'respostas': linha[3],
                'resultado_score': linha[4],
                'resultado_texto': linha[5],
                'data_avaliacao': linha[6].isoformat() if linha[6] else None
            })
        return avaliacoes
        
    except Exception as error:
        print(f"❌ Erro ao buscar avaliações do usuário: {error}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexao(conn)

def buscar_ultima_avaliacao_usuario(usuario_id, tipo):
    """Busca a última avaliação de um tipo específico para um usuário."""
    conn = None
    cursor = None
    try:
        conn = conectar()
        if not conn:
            raise Exception("Falha ao conectar ao banco de dados")
        
        cursor = conn.cursor()
        sql = """
            SELECT id, usuario_id, tipo, respostas, resultado_score, resultado_texto, data_avaliacao
            FROM resultados_avaliacoes
            WHERE usuario_id = %s AND tipo = %s
            ORDER BY data_avaliacao DESC
            LIMIT 1
        """
        cursor.execute(sql, (usuario_id, tipo))
        linha = cursor.fetchone()
        
        if linha:
            return {
                'id': linha[0],
                'usuario_id': linha[1],
                'tipo': linha[2],
                'respostas': linha[3],
                'resultado_score': linha[4],
                'resultado_texto': linha[5],
                'data_avaliacao': linha[6].isoformat() if linha[6] else None
            }
        return None
        
    except Exception as error:
        print(f"❌ Erro ao buscar última avaliação: {error}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexao(conn)


# --- FUNÇÕES DE ESTATÍSTICAS ---

def get_database_stats():
    """Busca a contagem de registros das principais tabelas."""
    conn = None
    cursor = None
    stats = {}
    try:
        conn = conectar()
        if not conn:
            raise Exception("Falha ao conectar ao banco de dados")
        
        cursor = conn.cursor()

        # ✅ MELHORIA: Lista de tabelas validadas
        TABELAS_VALIDAS = ['usuarios', 'meditacoes', 'classificacoes_humor', 'resultados_avaliacoes']
        
        for tabela in TABELAS_VALIDAS:
            try:
                # Ainda usando f-string mas com validação explícita
                cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
                stats[tabela] = cursor.fetchone()[0]
            except Exception as table_error:
                print(f"⚠️  Aviso: Tabela {tabela} não encontrada - {table_error}")
                stats[tabela] = 0

        return stats
        
    except Exception as error:
        print(f"❌ Erro ao buscar estatísticas: {error}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexao(conn)

def listar_avaliacoes_por_usuario(usuario_id):
    """Busca todos os resultados de avaliações de um usuário, ordenados por data."""
    conn = None
    cursor = None
    resultados = []
    try:
        conn = conectar()
        if not conn:
            raise Exception("Falha ao conectar ao banco de dados")

        cursor = conn.cursor()
        sql = """
            SELECT tipo, resultado_score, resultado_texto, data_avaliacao
            FROM resultados_avaliacoes
            WHERE usuario_id = %s
            ORDER BY data_avaliacao DESC
        """
        cursor.execute(sql, (usuario_id,))

        for linha in cursor.fetchall():
            resultados.append({
                'tipo': linha[0],
                'score': linha[1],
                'resultado': linha[2],
                'data': linha[3].strftime('%d/%m/%Y')  # Formata a data
            })
        return resultados

    except Exception as error:
        print(f"❌ Erro ao listar avaliações do usuário: {error}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexao(conn)


def excluir_conta_completa(usuario_id):
    """
    Exclui completamente a conta de um usuário e todos os seus dados relacionados.
    Esta operação é irreversível e deleta:
    - Classificações de humor
    - Histórico de meditações
    - Resultados de avaliações
    - Registro do usuário
    """
    conn = None
    cursor = None
    try:
        conn = conectar()
        if not conn:
            raise Exception("Falha ao conectar ao banco de dados")

        cursor = conn.cursor()

        # Inicia transação explícita
        print(f"🗑️  Iniciando exclusão completa da conta do usuário {usuario_id}")

        # 1. Deleta classificações de humor
        cursor.execute("DELETE FROM classificacoes_humor WHERE usuario_id = %s", (usuario_id,))
        humor_count = cursor.rowcount
        print(f"  ✓ {humor_count} registro(s) de humor deletado(s)")

        # 2. Deleta histórico de meditações
        cursor.execute("DELETE FROM historico_meditacoes WHERE usuario_id = %s", (usuario_id,))
        meditacao_count = cursor.rowcount
        print(f"  ✓ {meditacao_count} registro(s) de meditação deletado(s)")

        # 3. Deleta resultados de avaliações
        cursor.execute("DELETE FROM resultados_avaliacoes WHERE usuario_id = %s", (usuario_id,))
        avaliacao_count = cursor.rowcount
        print(f"  ✓ {avaliacao_count} resultado(s) de avaliação deletado(s)")

        # 4. Deleta o usuário
        cursor.execute("DELETE FROM usuarios WHERE id = %s RETURNING email", (usuario_id,))
        usuario_deleted = cursor.fetchone()

        if not usuario_deleted:
            raise Exception(f"Usuário {usuario_id} não encontrado")

        email_deletado = usuario_deleted[0]

        # Commit da transação
        conn.commit()

        print(f"✅ Conta do usuário {email_deletado} (ID: {usuario_id}) excluída completamente!")
        print(f"📊 Total de dados removidos: {humor_count + meditacao_count + avaliacao_count + 1} registros")

        return {
            'success': True,
            'email': email_deletado,
            'registros_removidos': {
                'humor': humor_count,
                'meditacoes': meditacao_count,
                'avaliacoes': avaliacao_count,
                'usuario': 1
            }
        }

    except Exception as error:
        if conn:
            conn.rollback()
        print(f"❌ Erro ao excluir conta completa: {error}")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexao(conn)