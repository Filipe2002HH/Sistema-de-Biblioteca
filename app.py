"""
Sistema de Biblioteca - Aplicação Web (Flask + Oracle)

Instalação necessária:
    pip install flask oracledb

Execução:
    python app.py
Depois acesse: http://localhost:5000
"""

from flask import Flask, render_template, request, redirect, url_for, flash
import oracledb

app = Flask(__name__)
app.secret_key = "biblioteca-filipe-2026-xyz123"

# ---------------------------------------------------------
# Configuração da conexão - ajuste com seus dados
# ---------------------------------------------------------
DB_USER = "system"
DB_PASSWORD = "123"
DB_DSN = "localhost:1521/XEPDB1"


def conectar():
    return oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)


# ---------------------------------------------------------
# Página inicial - painel com resumo
# ---------------------------------------------------------
@app.route("/")
def index():
    with conectar() as conn:
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM livros")
        total_livros = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM usuarios")
        total_usuarios = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM emprestimos WHERE data_devolucao IS NULL")
        emprestimos_ativos = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM emprestimos_atrasados")
        atrasados = cur.fetchone()[0]

    return render_template(
        "index.html",
        total_livros=total_livros,
        total_usuarios=total_usuarios,
        emprestimos_ativos=emprestimos_ativos,
        atrasados=atrasados,
    )


# ---------------------------------------------------------
# Livros
# ---------------------------------------------------------
@app.route("/livros")
def livros():
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT id_livro, titulo, autor, isbn, quantidade_total, quantidade_disponivel
               FROM livros ORDER BY titulo"""
        )
        lista = cur.fetchall()
    return render_template("livros.html", livros=lista)


@app.route("/livros/novo", methods=["POST"])
def novo_livro():
    titulo = request.form["titulo"]
    autor = request.form["autor"]
    isbn = request.form["isbn"]
    quantidade = int(request.form["quantidade"])

    with conectar() as conn:
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO livros (titulo, autor, isbn, quantidade_total, quantidade_disponivel)
               VALUES (:1, :2, :3, :4, :5)""",
            [titulo, autor, isbn, quantidade, quantidade],
        )
        conn.commit()

    flash(f"Livro '{titulo}' cadastrado com sucesso.")
    return redirect(url_for("livros"))


# ---------------------------------------------------------
# Usuários
# ---------------------------------------------------------
@app.route("/usuarios")
def usuarios():
    with conectar() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id_usuario, nome, email, data_cadastro FROM usuarios ORDER BY nome")
        lista = cur.fetchall()
    return render_template("usuarios.html", usuarios=lista)


@app.route("/usuarios/novo", methods=["POST"])
def novo_usuario():
    nome = request.form["nome"]
    email = request.form["email"]

    with conectar() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO usuarios (nome, email) VALUES (:1, :2)", [nome, email]
        )
        conn.commit()

    flash(f"Usuário '{nome}' cadastrado com sucesso.")
    return redirect(url_for("usuarios"))


# ---------------------------------------------------------
# Empréstimos
# ---------------------------------------------------------
@app.route("/emprestimos")
def emprestimos():
    with conectar() as conn:
        cur = conn.cursor()

        cur.execute(
            """SELECT e.id_emprestimo, u.nome, l.titulo, e.data_emprestimo,
                      e.data_prevista, e.data_devolucao
               FROM emprestimos e
               JOIN usuarios u ON u.id_usuario = e.id_usuario
               JOIN livros l ON l.id_livro = e.id_livro
               ORDER BY e.data_emprestimo DESC"""
        )
        lista = cur.fetchall()

        cur.execute("SELECT id_usuario, nome FROM usuarios ORDER BY nome")
        usuarios_lista = cur.fetchall()

        cur.execute(
            "SELECT id_livro, titulo FROM livros WHERE quantidade_disponivel > 0 ORDER BY titulo"
        )
        livros_disponiveis = cur.fetchall()

    return render_template(
        "emprestimos.html",
        emprestimos=lista,
        usuarios=usuarios_lista,
        livros=livros_disponiveis,
    )


@app.route("/emprestimos/novo", methods=["POST"])
def novo_emprestimo():
    id_usuario = int(request.form["id_usuario"])
    id_livro = int(request.form["id_livro"])
    dias_prazo = int(request.form.get("dias_prazo", 7))

    with conectar() as conn:
        cur = conn.cursor()
        try:
            cur.callproc("mb_registrar_emprestimo", [id_usuario, id_livro, dias_prazo])
            flash("Empréstimo registrado com sucesso.")
        except oracledb.DatabaseError as e:
            flash(f"Erro ao registrar empréstimo: {e}")

    return redirect(url_for("emprestimos"))


@app.route("/emprestimos/<int:id_emprestimo>/devolver", methods=["POST"])
def devolver_emprestimo(id_emprestimo):
    with conectar() as conn:
        cur = conn.cursor()
        try:
            cur.callproc("registrar_devolucao", [id_emprestimo])
            flash("Devolução registrada com sucesso.")
        except oracledb.DatabaseError as e:
            flash(f"Erro ao registrar devolução: {e}")

    return redirect(url_for("emprestimos"))


if __name__ == "__main__":
    app.run(debug=True)
