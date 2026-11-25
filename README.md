# sistema-biblioteca-python
Sistema de gerenciamento de biblioteca em Python, feito para praticar Programação Orientada a Objetos, validação de dados e tratamento de exceções.

## O que o projeto faz

- Cadastra livros e usuários, impedindo IDs duplicados
- Registra empréstimos e devoluções, controlando as cópias disponíveis
- Consulta livros por título, autor e ano, com filtro de disponibilidade
- Gera um relatório com acervo, usuários e empréstimos em andamento e concluídos

## Como rodar

Requer Python 3.10 ou superior. Na pasta do projeto, execute:

`python main.py`

## Estrutura dos arquivos

- `main.py`: ponto de entrada do programa
- `menu.py`: interface de console (entradas e saídas)
- `biblioteca.py`: regras de negócio (cadastros, empréstimos, consultas)
- `models.py`: modelos Livro, Usuario e Emprestimo
- `excecoes.py`: exceções personalizadas

## Autor

Jeferson Paixão de Melo, estudante de Ciência de Dados.
