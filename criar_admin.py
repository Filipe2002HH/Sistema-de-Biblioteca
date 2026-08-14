"""
Script auxiliar - cria o usuário administrador do sistema.
Execute UMA VEZ, depois de rodar o 03_criar_admin.sql.

Instalação necessária:
    pip install oracledb werkzeug

Execução:
    python criar_admin.py
"""

import getpass
import oracledb
from werkzeug.security import generate_password_hash

DB_USER = "system"
DB_PASSWORD = "123"
DB_DSN = "localhost:1521/XEPDB1"


def main():
    usuario = input("Nome de usuário do admin (ex: filipe): ").strip()
    senha = getpass.getpass("Senha do admin: ")
    senha_confirma = getpass.getpass("Confirme a senha: ")

    if senha != senha_confirma:
        print("As senhas não conferem. Tente novamente.")
        return

    senha_hash = generate_password_hash(senha)

    with oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO admins (usuario, senha_hash) VALUES (:1, :2)",
            [usuario, senha_hash],
        )
        conn.commit()

    print(f"Admin '{usuario}' criado com sucesso!")


if __name__ == "__main__":
    main()
