import sqlite3
import datetime

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('eventos.db')
cursor = conn.cursor()

# Criar tabelas se não existirem
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT,
        idade INTEGER,
        cpf TEXT,
        cnpj TEXT,
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

conn.commit()

class Usuario:
    def __init__(self, nome, email, idade, cpf, cnpj ):
        self._nome = nome
        self._email = email
        self._idade = idade
        self.cpf = cpf
        self.cnpj = cnpj
        self._eventos_participando = []

    def get_nome(self):
        return self._nome

    def set_nome(self, nome):
        self._nome = nome

    def get_email(self):
        return self._email

    def set_email(self, email):
        self._email = email

    def get_idade(self):
        return self._idade

    def set_idade(self, idade):
        self._idade = idade

    def get_eventos_participando(self):
        return self._eventos_participando

    def set_eventos_participando(self, eventos_participando):
        self._eventos_participando = eventos_participando
        
class UsuarioSimples(Usuario):
    def __init__(self, nome, email, idade, cpf):
        super().__init__(nome, email, idade, cpf, None)
        
class EmpresaEventos(Usuario):
    def __init__(self, nome, email, idade, cpf, cnpj):
        super().__init__(nome, email, idade, None, cnpj)

class Evento:
    def __init__(self, nome, endereco, categoria, horario, descricao):
        self._nome = nome
        self._endereco = endereco
        self._categoria = categoria
        self._horario = horario
        self._descricao = descricao

    def get_nome(self):
        return self._nome

    def set_nome(self, nome):
        self._nome = nome

    def get_endereco(self):
        return self._endereco

    def set_endereco(self, endereco):
        self._endereco = endereco

    def get_categoria(self):
        return self._categoria

    def set_categoria(self, categoria):
        self._categoria = categoria

    def get_horario(self):
        return self._horario

    def set_horario(self, horario):
        self._horario = horario

    def get_descricao(self):
        return self._descricao

    def set_descricao(self, descricao):
        self._descricao = descricao

def criar_usuario(nome, email, idade):
    cursor.execute('INSERT INTO usuarios (nome, email, idade) VALUES (?, ?, ?)', (nome, email, idade))
    conn.commit()
    print("Usuário cadastrado com sucesso!")

def criar_evento(nome, endereco, categoria, horario, descricao):
    cursor.execute('INSERT INTO eventos (nome, endereco, categoria, horario, descricao) VALUES (?, ?, ?, ?, ?)', (nome, endereco, categoria, horario, descricao))
    conn.commit()
    print("Evento cadastrado com sucesso!")

def listar_eventos():
    agora = datetime.datetime.now()
    cursor.execute('SELECT * FROM eventos ORDER BY horario')
    eventos = cursor.fetchall()
    
    print("\nEventos disponíveis:")
    for evento in eventos:
        horario_evento = datetime.datetime.strptime(evento[4], "%Y-%m-%d %H:%M")
        if horario_evento >= agora:
            imprimir_evento(evento)
    
    print("\nEventos que já ocorreram:")
    for evento in eventos:
        horario_evento = datetime.datetime.strptime(evento[4], "%Y-%m-%d %H:%M")
        if horario_evento < agora:
            imprimir_evento(evento)

def participar_evento(id_usuario, id_evento):
    cursor.execute('SELECT * FROM usuarios WHERE id=?', (id_usuario,))
    dados_usuario = cursor.fetchone()
    cursor.execute('SELECT * FROM eventos WHERE id=?', (id_evento,))
    dados_evento = cursor.fetchone()
    
    if dados_usuario and dados_evento:
        usuario = Usuario(dados_usuario[1], dados_usuario[2], dados_usuario[3])
        evento = Evento(dados_evento[1], dados_evento[2], dados_evento[3], dados_evento[4], dados_evento[5])

        eventos_participando = [Evento(*linha) for linha in cursor.execute('SELECT * FROM usuario_eventos WHERE id_usuario=?', (id_usuario,)).fetchall()]

        usuario.set_eventos_participando(eventos_participando)
        usuario.get_eventos_participando().append(evento)
        cursor.execute('INSERT INTO usuario_eventos (id_usuario, id_evento) VALUES (?, ?)', (id_usuario, id_evento))
        conn.commit()
        print("Você está participando deste evento.")
    else:
        print("Usuário ou evento não encontrado.")

def imprimir_evento(evento):
    print(f"Nome: {evento[1]}")
    print(f"Endereço: {evento[2]}")
    print(f"Categoria: {evento[3]}")
    print(f"Horário: {evento[4]}")
    print(f"Descrição: {evento[5]}\n")

def main():
    while True:
        print("\nOpções:")
        print("1. Cadastrar usuário")
        print("2. Cadastrar evento")
        print("3. Listar eventos")
        print("4. Participar de um evento")
        print("5. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            nome = input("Nome: ")
            email = input("E-mail: ")
            idade = input("Idade: ")
            criar_usuario(nome, email, idade)
        elif escolha == '2':
            nome = input("Nome do evento: ")
            endereco = input("Endereço: ")
            categoria = input("Categoria: ")
            horario = input("Horário (AAAA-MM-DD HH:MM): ")
            descricao = input("Descrição: ")
            criar_evento(nome, endereco, categoria, horario, descricao)
        elif escolha == '3':
            listar_eventos()
        elif escolha == '4':
            id_usuario = input("Digite o ID de usuário: ")
            id_evento = input("Digite o ID do evento que deseja participar: ")
            participar_evento(id_usuario, id_evento)
        elif escolha == '5':
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
