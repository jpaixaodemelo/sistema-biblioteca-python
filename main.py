"""Ponto de entrada do sistema de gerenciamento de biblioteca."""
from biblioteca import Biblioteca
from menu import executar


def main() -> None:
    executar(Biblioteca())


if __name__ == "__main__":
    main()
