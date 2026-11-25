"""Modelos de dados: Livro, Usuario e Emprestimo."""
from datetime import datetime
from enum import Enum
from typing import Optional

from excecoes import DadoInvalidoError


class Situacao(Enum):
    """Situação possível de um empréstimo."""
    EM_ANDAMENTO = "Em andamento"
    CONCLUIDO = "Concluído"


def _validar_texto(valor: str, campo: str) -> str:
    """Remove espaços das pontas e impede texto vazio."""
    valor = str(valor).strip()
    if not valor:
        raise DadoInvalidoError(f"O campo '{campo}' não pode ser vazio.")
    return valor


class Livro:
    """Representa um livro do acervo."""

    def __init__(self, id_livro: str, titulo: str, autor: str,
                 ano_publicacao: int, total_copias: int):
        ano_atual = datetime.now().year
        if not 0 < ano_publicacao <= ano_atual:
            raise DadoInvalidoError(
                f"Ano de publicação deve estar entre 1 e {ano_atual}."
            )
        if total_copias < 1:
            raise DadoInvalidoError("Informe pelo menos uma cópia.")

        self.id_livro = _validar_texto(id_livro, "ID do livro")
        self.titulo = _validar_texto(titulo, "Título")
        self.autor = _validar_texto(autor, "Autor")
        self.ano_publicacao = ano_publicacao
        self.total_copias = total_copias
        # Ao cadastrar, todas as cópias estão disponíveis.
        self.copias_disponiveis = total_copias

    def __str__(self) -> str:
        return (f"{self.titulo} ({self.ano_publicacao}) por {self.autor} "
                f"[{self.copias_disponiveis}/{self.total_copias} disponíveis]")


class Usuario:
    """Representa um usuário da biblioteca."""

    def __init__(self, id_usuario: str, nome: str, contato: str):
        self.id_usuario = _validar_texto(id_usuario, "ID do usuário")
        self.nome = _validar_texto(nome, "Nome")
        self.contato = _validar_texto(contato, "Contato")

    def __str__(self) -> str:
        return f"{self.nome} (ID: {self.id_usuario}, contato: {self.contato})"


class Emprestimo:
    """Representa o empréstimo de um livro a um usuário."""

    def __init__(self, id_emprestimo: int, livro: Livro, usuario: Usuario):
        self.id_emprestimo = id_emprestimo
        self.livro = livro
        self.usuario = usuario
        self.data_emprestimo = datetime.now()
        self.data_devolucao: Optional[datetime] = None
        self.situacao = Situacao.EM_ANDAMENTO

    def concluir(self) -> None:
        """Marca o empréstimo como concluído e registra a data."""
        self.situacao = Situacao.CONCLUIDO
        self.data_devolucao = datetime.now()
