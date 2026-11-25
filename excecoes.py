"""Exceções personalizadas do sistema de biblioteca."""


class BibliotecaError(Exception):
    """Classe base para todos os erros do sistema."""


class DadoInvalidoError(BibliotecaError):
    """Lançada quando um dado informado é inválido (vazio, negativo etc.)."""


class CadastroDuplicadoError(BibliotecaError):
    """Lançada ao tentar cadastrar um ID que já existe."""


class LivroNaoEncontradoError(BibliotecaError):
    """Lançada quando o livro não existe no acervo."""


class UsuarioNaoEncontradoError(BibliotecaError):
    """Lançada quando o usuário não está cadastrado."""


class LivroIndisponivelError(BibliotecaError):
    """Lançada quando não há cópias disponíveis para empréstimo."""


class EmprestimoNaoEncontradoError(BibliotecaError):
    """Lançada quando o empréstimo informado não existe."""


class EmprestimoJaConcluidoError(BibliotecaError):
    """Lançada ao tentar devolver um empréstimo já concluído."""


class EmprestimoDuplicadoError(BibliotecaError):
    """Lançada quando o usuário já tem um empréstimo ativo do mesmo livro."""
