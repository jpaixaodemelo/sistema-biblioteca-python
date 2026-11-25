"""Regras de negócio da biblioteca (sem prints: só retorna dados ou lança exceções)."""
from typing import List, Optional

from excecoes import (
    CadastroDuplicadoError,
    EmprestimoDuplicadoError,
    EmprestimoJaConcluidoError,
    EmprestimoNaoEncontradoError,
    LivroIndisponivelError,
    LivroNaoEncontradoError,
    UsuarioNaoEncontradoError,
)
from models import Emprestimo, Livro, Situacao, Usuario


class Biblioteca:
    """Gerencia livros, usuários e empréstimos."""

    def __init__(self):
        self.livros: List[Livro] = []
        self.usuarios: List[Usuario] = []
        self.emprestimos: List[Emprestimo] = []
        self._proximo_id_emprestimo = 1

    # ---------- Buscas internas ----------
    def _buscar_livro(self, id_livro: str) -> Livro:
        for livro in self.livros:
            if livro.id_livro == id_livro:
                return livro
        raise LivroNaoEncontradoError(f"Livro com ID '{id_livro}' não encontrado.")

    def _buscar_usuario(self, id_usuario: str) -> Usuario:
        for usuario in self.usuarios:
            if usuario.id_usuario == id_usuario:
                return usuario
        raise UsuarioNaoEncontradoError(f"Usuário com ID '{id_usuario}' não encontrado.")

    def _buscar_emprestimo(self, id_emprestimo: int) -> Emprestimo:
        for emp in self.emprestimos:
            if emp.id_emprestimo == id_emprestimo:
                return emp
        raise EmprestimoNaoEncontradoError(f"Empréstimo {id_emprestimo} não encontrado.")

    # ---------- Cadastros ----------
    def cadastrar_livro(self, livro: Livro) -> None:
        """Adiciona um livro ao acervo, impedindo IDs duplicados."""
        if any(l.id_livro == livro.id_livro for l in self.livros):
            raise CadastroDuplicadoError(
                f"Já existe um livro cadastrado com o ID {livro.id_livro}."
            )
        self.livros.append(livro)

    def cadastrar_usuario(self, usuario: Usuario) -> None:
        """Adiciona um usuário, impedindo IDs duplicados."""
        if any(u.id_usuario == usuario.id_usuario for u in self.usuarios):
            raise CadastroDuplicadoError(
                f"Já existe um usuário cadastrado com o ID {usuario.id_usuario}."
            )
        self.usuarios.append(usuario)

    # ---------- Empréstimo e devolução ----------
    def registrar_emprestimo(self, id_livro: str, id_usuario: str) -> Emprestimo:
        """Registra um empréstimo e reduz o número de cópias disponíveis."""
        livro = self._buscar_livro(id_livro)
        usuario = self._buscar_usuario(id_usuario)

        if livro.copias_disponiveis <= 0:
            raise LivroIndisponivelError(
                f"Não há cópias disponíveis do livro '{livro.titulo}'."
            )
        if any(e.livro is livro and e.usuario is usuario
               and e.situacao == Situacao.EM_ANDAMENTO for e in self.emprestimos):
            raise EmprestimoDuplicadoError(
                f"{usuario.nome} já está com uma cópia de '{livro.titulo}'."
            )

        livro.copias_disponiveis -= 1
        emprestimo = Emprestimo(self._proximo_id_emprestimo, livro, usuario)
        self._proximo_id_emprestimo += 1
        self.emprestimos.append(emprestimo)
        return emprestimo

    def devolver_livro(self, id_emprestimo: int) -> Emprestimo:
        """Registra a devolução e aumenta o número de cópias disponíveis."""
        emprestimo = self._buscar_emprestimo(id_emprestimo)
        if emprestimo.situacao == Situacao.CONCLUIDO:
            raise EmprestimoJaConcluidoError(
                f"O empréstimo {id_emprestimo} já foi concluído."
            )
        emprestimo.livro.copias_disponiveis += 1
        emprestimo.concluir()
        return emprestimo

    # ---------- Consultas ----------
    def consultar_livros(self, titulo: Optional[str] = None,
                         autor: Optional[str] = None,
                         ano_publicacao: Optional[int] = None,
                         apenas_disponiveis: bool = False) -> List[Livro]:
        """Retorna os livros que atendem a todos os filtros informados."""
        resultado = []
        for livro in self.livros:
            if titulo and titulo.casefold() not in livro.titulo.casefold():
                continue
            if autor and autor.casefold() not in livro.autor.casefold():
                continue
            if ano_publicacao is not None and livro.ano_publicacao != ano_publicacao:
                continue
            if apenas_disponiveis and livro.copias_disponiveis <= 0:
                continue
            resultado.append(livro)
        return resultado

    def emprestimos_por_situacao(self, situacao: Situacao) -> List[Emprestimo]:
        """Retorna os empréstimos com a situação informada."""
        return [e for e in self.emprestimos if e.situacao == situacao]

    def emprestimos_do_usuario(self, id_usuario: str) -> List[Emprestimo]:
        """Retorna todos os empréstimos de um usuário."""
        self._buscar_usuario(id_usuario)  # lança erro se não existir
        return [e for e in self.emprestimos if e.usuario.id_usuario == id_usuario]
