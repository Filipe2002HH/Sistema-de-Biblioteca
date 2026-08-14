# Sistema de Biblioteca

Projeto que fiz pra entender na prática como Python, Flask e Oracle (SQL/PL-SQL) trabalham juntos numa aplicação real — desde o banco de dados até a tela que o usuário vê.

A ideia era simples: um sistema de biblioteca onde dá pra cadastrar livros, usuários, registrar empréstimos e devoluções, com as regras de negócio (tipo controlar quantidade de exemplares disponíveis) ficando no banco, em PL/SQL.

## Tecnologias

- Flask (Python) pro back-end
- Oracle Database, com procedures, view e trigger em PL/SQL
- oracledb pra conectar o Python no Oracle
- HTML/CSS direto, sem framework de front-end

## Páginas

- **Painel** — resumo geral (livros, usuários, empréstimos ativos e atrasados)
- **Livros** — cadastro e listagem do acervo
- **Usuários** — cadastro e listagem de leitores
- **Empréstimos** — novo empréstimo, histórico e devolução

## Login

Acesso protegido por login (usuário/senha), com senha em hash — nada de senha salva em texto puro no banco.

## Como rodar

1. Criar as tabelas e objetos PL/SQL no Oracle (`01_criar_tabelas.sql`, `02_plsql_objetos.sql` e `03_criar_admin.sql`).

2. Instalar as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Ajustar a conexão no `app.py`:
   ```python
   DB_USER = "filipe"
   DB_PASSWORD = "sua_senha_aqui"
   DB_DSN = "localhost:1521/XEPDB1"
   ```

4. Criar o usuário admin (só uma vez):
   ```bash
   python criar_admin.py
   ```

5. Rodar:
   ```bash
   python app.py
   ```

6. Acessar `http://localhost:5000`

## O que ainda quero melhorar

- Multa automática por atraso
- Busca/filtro na listagem de livros
- Paginação nas tabelas
