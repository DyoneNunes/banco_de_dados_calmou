from conexao import conectar

def relatorio_meditacoes_por_usuario():
    """
    Relatório de Sumarização: Conta quantas meditações cada usuário completou.
    Usa GROUP BY e COUNT.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()

        sql = """
            SELECT u.nome, COUNT(h.id) as total_meditacoes
            FROM usuarios u
            JOIN historico_meditacoes h ON u.id = h.usuario_id
            GROUP BY u.nome
            ORDER BY total_meditacoes DESC;
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()
        
        print("\n--- Relatório: Total de Meditações por Usuário ---")
        if not resultados:
            print("Nenhum histórico de meditação encontrado.")
        else:
            for linha in resultados:
                print(f"Usuário: {linha[0]}, Meditações Concluídas: {linha[1]}")

    except Exception as error:
        print(f"Erro ao gerar relatório de meditações por usuário: {error}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def relatorio_historico_detalhado():
    """
    Relatório com Junção: Mostra o histórico detalhado de meditações.
    Usa JOIN para buscar o nome do usuário e o título da meditação.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()

        sql = """
            SELECT u.nome, m.titulo, h.data_conclusao
            FROM historico_meditacoes h
            JOIN usuarios u ON h.usuario_id = u.id
            JOIN meditacoes m ON h.meditacao_id = m.id
            ORDER BY h.data_conclusao DESC;
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()

        print("\n--- Relatório: Histórico Detalhado de Meditações ---")
        if not resultados:
            print("Nenhum histórico de meditação encontrado.")
        else:
            for linha in resultados:
                data_formatada = linha[2].strftime("%d/%m/%Y %H:%M:%S")
                print(f"Usuário: {linha[0]}, Meditação: '{linha[1]}', Concluído em: {data_formatada}")
                
    except Exception as error:
        print(f"Erro ao gerar relatório de histórico detalhado: {error}")
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == '__main__':
    relatorio_meditacoes_por_usuario()
    relatorio_historico_detalhado()