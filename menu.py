"""Interface de console: só lê entradas e mostra resultados."""
from biblioteca import Biblioteca
from excecoes import BibliotecaError
from models import Livro, Situacao, Usuario

FORMATO_DATA = "%d/%m/%Y %H:%M"


# ---------- Funções auxiliares de entrada ----------
def ler_texto(mensagem: str) -> str:
    return input(mensagem).strip()


def ler_inteiro(mensagem: str, opcional: bool = False):
    """Repete a pergunta até receber um inteiro válido (ou vazio, se opcional)."""
    while True:
        texto = input(mensagem).strip()
        if opcional and not texto:
            return None
        try:
            return int(texto)
        except ValueError:
            print("Digite um número inteiro válido.")


# ---------- Ações do menu ----------
def cadastrar_livro(bib: Biblioteca) -> None:
    id_livro = ler_texto("ID do Livro: ")
    titulo = ler_texto("Título: ")
    autor = ler_texto("Autor: ")
    ano = ler_inteiro("Ano de Publicação: ")
    copias = ler_inteiro("Total de Cópias: ")
    bib.cadastrar_livro(Livro(id_livro, titulo, autor, ano, copias))
    print("Livro cadastrado com sucesso.")


def cadastrar_usuario(bib: Biblioteca) -> None:
    id_usuario = ler_texto("ID do Usuário: ")
    nome = ler_texto("Nome: ")
    contato = ler_texto("Contato: ")
    bib.cadastrar_usuario(Usuario(id_usuario, nome, contato))
    print("Usuário cadastrado com sucesso.")


def registrar_emprestimo(bib: Biblioteca) -> None:
    id_livro = ler_texto("ID do Livro: ")
    id_usuario = ler_texto("ID do Usuário: ")
    emp = bib.registrar_emprestimo(id_livro, id_usuario)
    print(f"Empréstimo {emp.id_emprestimo} registrado: "
          f"{emp.livro.titulo} para {emp.usuario.nome}.")


def devolver_livro(bib: Biblioteca) -> None:
    id_emprestimo = ler_inteiro("ID do Empréstimo: ")
    emp = bib.devolver_livro(id_emprestimo)
    print(f"Devolução registrada: {emp.livro.titulo} de {emp.usuario.nome}.")


def consultar_livros(bib: Biblioteca) -> None:
    titulo = ler_texto("Título (vazio para não filtrar): ") or None
    autor = ler_texto("Autor (vazio para não filtrar): ") or None
    ano = ler_inteiro("Ano (vazio para não filtrar): ", opcional=True)
    livros = bib.consultar_livros(titulo, autor, ano)
    if not livros:
        print("Nenhum livro encontrado.")
    for livro in livros:
        print(f"- {livro}")


def exibir_relatorio(bib: Biblioteca) -> None:
    print("\n=== Relatório da Biblioteca ===")

    print("\n-- Todos os livros do acervo --")
    for livro in bib.livros:
        print(f"- {livro}")
    if not bib.livros:
        print("(nenhum)")

    print("\n-- Livros disponíveis --")
    disponiveis = bib.consultar_livros(apenas_disponiveis=True)
    for livro in disponiveis:
        print(f"- {livro.titulo} ({livro.copias_disponiveis} disponíveis)")
    if not disponiveis:
        print("(nenhum)")

    print("\n-- Usuários cadastrados --")
    for usuario in bib.usuarios:
        print(f"- {usuario}")
    if not bib.usuarios:
        print("(nenhum)")

    print("\n-- Livros emprestados (em andamento) --")
    ativos = bib.emprestimos_por_situacao(Situacao.EM_ANDAMENTO)
    for e in ativos:
        print(f"- #{e.id_emprestimo} {e.livro.titulo} -> {e.usuario.nome} "
              f"(desde {e.data_emprestimo.strftime(FORMATO_DATA)})")
    if not ativos:
        print("(nenhum)")

    print("\n-- Empréstimos concluídos --")
    concluidos = bib.emprestimos_por_situacao(Situacao.CONCLUIDO)
    for e in concluidos:
        print(f"- #{e.id_emprestimo} {e.livro.titulo} <- {e.usuario.nome} "
              f"({e.data_emprestimo.strftime(FORMATO_DATA)} a "
              f"{e.data_devolucao.strftime(FORMATO_DATA)})")
    if not concluidos:
        print("(nenhum)")


# ---------- Loop principal ----------
OPCOES = {
    "1": cadastrar_livro,
    "2": cadastrar_usuario,
    "3": registrar_emprestimo,
    "4": devolver_livro,
    "5": consultar_livros,
    "6": exibir_relatorio,
}


def exibir_menu() -> None:
    print("\n=== Menu ===")
    print("1 - Cadastrar Livro")
    print("2 - Cadastrar Usuário")
    print("3 - Registrar Empréstimo")
    print("4 - Devolução de Livros")
    print("5 - Consultar Livros")
    print("6 - Relatório")
    print("7 - Sair")


def executar(bib: Biblioteca) -> None:
    """Executa o menu até o usuário escolher sair."""
    while True:
        exibir_menu()
        try:
            opcao = input("Escolha uma opção: ").strip()
            if opcao == "7":
                print("Saindo...")
                break
            acao = OPCOES.get(opcao)
            if acao is None:
                print("Opção inválida. Tente novamente.")
                continue
            acao(bib)
        except BibliotecaError as erro:      # erros de regra de negócio
            print(f"Erro: {erro}")
        except (KeyboardInterrupt, EOFError):  # Ctrl+C / Ctrl+D
            print("\nEncerrando o sistema...")
            break
