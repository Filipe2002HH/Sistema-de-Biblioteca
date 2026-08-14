# 📚 Sistema de Biblioteca — Aplicação Web

Versão web do sistema de biblioteca, construída com **Flask** (Python) e conectada diretamente ao banco **Oracle**, usando as procedures e a view em PL/SQL já criadas no projeto.

## 🛠️ Tecnologias

- **Flask** — framework web em Python
- **oracledb** — driver de conexão com Oracle
- **Oracle Database** — armazenamento e regras de negócio (procedures, view, trigger)
- HTML + CSS puro nas telas (sem frameworks JS)

## 📄 Páginas

- **Painel** (`/`) — resumo com total de livros, usuários, empréstimos ativos e atrasados
- **Livros** (`/livros`) — cadastro e listagem do acervo
- **Usuários** (`/usuarios`) — cadastro e listagem de leitores
- **Empréstimos** (`/emprestimos`) — registrar novo empréstimo, ver histórico e registrar devoluções

## 🔒 Login

O sistema exige login (usuário/senha) para acessar qualquer página. A senha é armazenada com hash (via `werkzeug.security`), nunca em texto puro.

## 🚀 Como executar

1. Certifique-se de já ter criado as tabelas e objetos PL/SQL no Oracle (scripts `01_criar_tabelas.sql` e `02_plsql_objetos.sql` do projeto principal), além da tabela de admins (`03_criar_admin.sql`).

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure a conexão no início do `app.py`:
   ```python
   DB_USER = "filipe"
   DB_PASSWORD = "sua_senha_aqui"
   DB_DSN = "localhost:1521/XEPDB1"
   ```

4. Crie seu usuário administrador (só precisa fazer isso uma vez):
   ```bash
   python criar_admin.py
   ```
   Vai pedir um nome de usuário e uma senha — use isso para fazer login no site.

5. Execute a aplicação:
   ```bash
   python app.py
   ```

6. Acesse no navegador: **http://localhost:5000** — você será redirecionado para a tela de login.

## 📌 Próximos passos (ideias de melhoria)

- Autenticação de login
- Cálculo automático de multa por atraso
- Busca/filtro na listagem de livros
- Paginação nas tabelas