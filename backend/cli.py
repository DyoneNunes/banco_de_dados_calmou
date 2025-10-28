
import os
from controller import controller_usuario
from model.usuario import Usuario
from model.meditacao import Meditacao

def limpar_tela():
    """Limpa o terminal para melhorar a legibilidade."""
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_menu_principal():
    """Mostra o menu principal da aplicação CLI."""
    limpar_tela()
    print("--- Calmou APP | Back-office ---")
    print("1. Gerenciar Meditações")
    print("2. Gerenciar Usuários")
    print("3. Gerenciar Avaliações (em breve)")
    print("4. Gerar Relatórios (em breve)")
    print("5. Sair")
    return input("Escolha uma opção: ")

def exibir_menu_meditacoes():
    """Mostra o menu de gerenciamento de meditações."""
    limpar_tela()
    print("--- Gerenciar Meditações ---")
    print("1. Adicionar Nova Meditação")
    print("2. Listar Meditações")
    print("3. Voltar ao Menu Principal")
    return input("Escolha uma opção: ")

def exibir_menu_usuarios():
    """Mostra o menu de gerenciamento de usuários."""
    limpar_tela()
    print("--- Gerenciar Usuários ---")
    print("1. Adicionar Novo Usuário")
    print("2. Listar Usuários")
    print("3. Voltar ao Menu Principal")
    return input("Escolha uma opção: ")

def adicionar_nova_meditacao():
    """Coleta dados do usuário e adiciona uma nova meditação."""
    limpar_tela()
    print("--- Adicionar Nova Meditação ---")
    try:
        titulo = input("Título: ")
        descricao = input("Descrição: ")
        duracao_minutos = int(input("Duração (em minutos): "))
        url_audio = input("URL do Áudio: ")
        tipo = input("Tipo (ex: 'Guiada', 'Mindfulness'): ")
        categoria = input("Categoria (ex: 'Ansiedade', 'Sono'): ")
        imagem_capa = input("URL da Imagem de Capa: ")

        nova_meditacao = Meditacao(
            id=None,
            titulo=titulo,
            descricao=descricao,
            duracao_minutos=duracao_minutos,
            url_audio=url_audio,
            tipo=tipo,
            categoria=categoria,
            imagem_capa=imagem_capa
        )

        controller_usuario.inserir_meditacao(nova_meditacao)
    
    except ValueError:
        print("\n❌ Erro: A duração deve ser um número inteiro.")
    except Exception as e:
        print(f"\n❌ Ocorreu um erro inesperado: {e}")
    
    input("\nPressione Enter para continuar...")

def listar_meditacoes_cli():
    """Busca e exibe todas as meditações cadastradas."""
    limpar_tela()
    print("--- Lista de Meditações ---")
    meditacoes = controller_usuario.listar_meditacoes()
    if not meditacoes:
        print("Nenhuma meditação encontrada.")
    else:
        for m in meditacoes:
            print(f"ID: {m.id} | Título: {m.titulo} | Categoria: {m.categoria} | Duração: {m.duracao_minutos} min")
    
    input("\nPressione Enter para continuar...")

def adicionar_novo_usuario():
    """Coleta dados e adiciona um novo usuário."""
    limpar_tela()
    print("--- Adicionar Novo Usuário ---")
    try:
        nome = input("Nome: ")
        email = input("Email: ")
        password = input("Senha: ")

        if not all([nome, email, password]):
            print("\n❌ Erro: Nome, email e senha são obrigatórios.")
        else:
            novo_usuario = Usuario(
                nome=nome,
                email=email,
                password=password,
                config='{}' # JSON vazio como padrão
            )
            controller_usuario.inserir_usuario(novo_usuario)

    except Exception as e:
        print(f"\n❌ Ocorreu um erro inesperado: {e}")

    input("\nPressione Enter para continuar...")

def listar_usuarios_cli():
    """Busca e exibe todos os usuários."""
    limpar_tela()
    print("--- Lista de Usuários ---")
    usuarios = controller_usuario.listar_usuarios()
    if not usuarios:
        print("Nenhum usuário encontrado.")
    else:
        for u in usuarios:
            print(f"ID: {u.id} | Nome: {u.nome} | Email: {u.email}")
    
    input("\nPressione Enter para continuar...")


def loop_meditacoes():
    while True:
        escolha = exibir_menu_meditacoes()
        if escolha == '1':
            adicionar_nova_meditacao()
        elif escolha == '2':
            listar_meditacoes_cli()
        elif escolha == '3':
            break
        else:
            print("Opção inválida. Tente novamente.")
            input("\nPressione Enter para continuar...")

def loop_usuarios():
    while True:
        escolha = exibir_menu_usuarios()
        if escolha == '1':
            adicionar_novo_usuario()
        elif escolha == '2':
            listar_usuarios_cli()
        elif escolha == '3':
            break
        else:
            print("Opção inválida. Tente novamente.")
            input("\nPressione Enter para continuar...")


def main():
    """Função principal que executa o loop da aplicação."""
    while True:
        escolha = exibir_menu_principal()
        if escolha == '1':
            loop_meditacoes()
        elif escolha == '2':
            loop_usuarios()
        elif escolha == '3':
            print("Funcionalidade de avaliações em desenvolvimento.")
            input("\nPressione Enter para continuar...")
        elif escolha == '4':
            print("Funcionalidade de relatórios em desenvolvimento.")
            input("\nPressione Enter para continuar...")
        elif escolha == '5':
            print("Saindo do programa. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")
            input("\nPressione Enter para continuar...")

if __name__ == '__main__':
    main()
