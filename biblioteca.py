"""
Sistema de Biblioteca - Interface em Python
Conecta ao Oracle e utiliza as procedures/views criadas em PL/SQL.

Instalação necessária:
    pip install oracledb
"""

import oracledb

# ---------------------------------------------------------
# Configuração da conexão - ajuste com seus dados
# ---------------------------------------------------------
DB_USER = "system"
DB_PASSWORD = "123"
DB_DSN = "localhost:1521/XEPDB1"  # host:porta/service_name


def conectar():
    return oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)


def cadastrar_usuario(nome: str, email: str):
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO usuarios (nome, email) VALUES (:1, :2)",
            [nome, email]
        )
        conn.commit()
        print(f"Usuário '{nome}' cadastrado com sucesso.")


def cadastrar_livro(titulo: str, autor: str, isbn: str, quantidade: int = 1):
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO livros (titulo, autor, isbn, quantidade_total, quantidade_disponivel)
               VALUES (:1, :2, :3, :4, :4)""",
            [titulo, autor, isbn, quantidade]
        )
        conn.commit()
        print(f"Livro '{titulo}' cadastrado com sucesso.")


def emprestar_livro(id_usuario: int, id_livro: int, dias_prazo: int = 7):
    with conectar() as conn:
        cur = conn.cursor()
        try:
            cur.callproc("registrar_emprestimo", [id_usuario, id_livro, dias_prazo])
            print("Empréstimo registrado com sucesso.")
        except oracledb.DatabaseError as e:
            print(f"Erro ao registrar empréstimo: {e}")


def devolver_livro(id_emprestimo: int):
    with conectar() as conn:
        cur = conn.cursor()
        try:
            cur.callproc("registrar_devolucao", [id_emprestimo])
            print("Devolução registrada com sucesso.")
        except oracledb.DatabaseError as e:
            print(f"Erro ao registrar devolução: {e}")


def listar_atrasados():
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM emprestimos_atrasados")
        colunas = [c[0] for c in cur.description]
        print(" | ".join(colunas))
        for linha in cur:
            print(linha)


def listar_livros_disponiveis():
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT titulo, autor, quantidade_disponivel FROM livros WHERE quantidade_disponivel > 0"
        )
        for titulo, autor, qtd in cur:
            print(f"{titulo} - {autor} ({qtd} disponíveis)")


# ---------------------------------------------------------
# Menu simples via terminal
# ---------------------------------------------------------
def menu():
    opcoes = {
        "1": ("Cadastrar usuário", lambda: cadastrar_usuario(
            input("Nome: "), input("Email: "))),
        "2": ("Cadastrar livro", lambda: cadastrar_livro(
            input("Título: "), input("Autor: "), input("ISBN: "), int(input("Quantidade: ")))),
        "3": ("Emprestar livro", lambda: emprestar_livro(
            int(input("ID usuário: ")), int(input("ID livro: ")))),
        "4": ("Devolver livro", lambda: devolver_livro(
            int(input("ID empréstimo: ")))),
        "5": ("Listar livros disponíveis", listar_livros_disponiveis),
        "6": ("Listar empréstimos atrasados", listar_atrasados),
        "0": ("Sair", None),
    }

    while True:
        print("\n=== SISTEMA DE BIBLIOTECA ===")
        for chave, (descricao, _) in opcoes.items():
            print(f"{chave}. {descricao}")

        escolha = input("Escolha uma opção: ").strip()
        if escolha == "0":
            print("Saindo...")
            break
        elif escolha in opcoes:
            opcoes[escolha][1]()
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()