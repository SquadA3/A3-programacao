import sqlite3


# Conectar ao banco de dados SQLite
conn = sqlite3.connect('eventos.db')
cursor = conn.cursor()

# Criar tabelas se não existirem
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT,
        cpf INTEGER,
        data_nascimento DATE,
        login TEXT,
        senha TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS empresa_eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT,
        telefone INTEGER,
        cnpj INTEGER,
        login TEXT,
        senha TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        endereco TEXT,
        categoria TEXT,
        horario DATETIME,
        descricao TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuario_eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER,
        id_evento INTEGER,
        FOREIGN KEY (id_usuario) REFERENCES usuarios (id),
        FOREIGN KEY (id_evento) REFERENCES eventos (id)
    )
''')