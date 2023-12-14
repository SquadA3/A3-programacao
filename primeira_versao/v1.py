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
        cpf,
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

conn.commit()

class Usuario:
    def __init__(self, nome, email, cpf, data_nascimento, login, senha):
        self._id = None
        self._nome = nome
        self._email = email
        self._cpf = cpf
        self._data_nascimento = data_nascimento
        self._login = login
        self._senha = senha
        self._eventos_participando = []

    def get_id(self):
        return self._id

    def set_id(self, identificador):
        self._id = identificador

    def get_nome(self):
        return self._nome

    def set_nome(self, nome):
        self._nome = nome

    def get_email(self):
        return self._email

    def set_email(self, email):
        self._email = email
        
    def get_cpf(self):
        return self._cpf
    
    def set_cpf(self, cpf):
        self._cpf = cpf

    def get_data_nascimento(self):
        return self._data_nascimento

    def set_data_nascimento(self, data_nascimento):
        self._data_nascimento = data_nascimento

    def get_login(self):
        return self._login

    def set_login(self, login):
        self._login = login

    def get_senha(self):
        return self._senha

    def set_senha(self, senha):
        self._senha = senha

    def get_eventos_participando(self):
        return self._eventos_participando

    def set_eventos_participando(self, eventos_participando):
        self._eventos_participando = eventos_participando
        
class Empresa(Usuario):
    def __init__(self, nome, email, login, senha, cnpj):
        super().__init__(nome, email, None, login, senha, cnpj)
        self._cnpj = cnpj

    def get_cnpj(self):
        return self._cnpj

    def set_cnpj(self, cnpj):
        self._cnpj = cnpj

    def menu_empresa(self):
        pass

class Evento:
    def __init__(self, nome, endereco, categoria, horario, descricao):
        self._id = None
        self._nome = nome
        self._endereco = endereco
        self._categoria = categoria
        self._horario = horario
        self._descricao = descricao

    def get_id(self):
        return self._id

    def set_id(self, identificador):
        self._id = identificador

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
        

def criar_usuario(nome, email, cpf, data_nascimento, login, senha):
    cursor.execute('INSERT INTO usuarios (nome, email, cpf, data_nascimento, login, senha) VALUES (?, ?, ?, ?, ?, ?)', (nome, email, cpf, data_nascimento, login, senha))
    conn.commit()
    print("Usuário cadastrado com sucesso!")
    
def criar_empresa(nome, email, telefone, cnpj, login, senha):
    cursor.execute('INSERT INTO empresa_eventos (nome, email, telefone, cnpj, login, senha) VALUES (?, ?, ?, ?, ?, ?)', (nome, email, telefone, cnpj, login, senha))
    conn.commit()
    print("Usuário cadastrado com sucesso!")

def criar_evento(nome, endereco, categoria, data, horario, descricao):
    cursor.execute('INSERT INTO eventos (nome, endereco, categoria, horario, descricao) VALUES (?, ?, ?, ?, ?)', (nome, endereco, categoria, horario, descricao))
    conn.commit()
    print("Evento cadastrado com sucesso!")

def listar_eventos():
    agora = datetime.datetime.now()
    cursor.execute('SELECT * FROM eventos ORDER BY horario')
    eventos = cursor.fetchall()

    if not eventos:
        print("Não há eventos disponíveis.")
        return

    print("\nEventos disponíveis:")
    for evento in eventos:
        if evento[4]:  # Verifique se a data e hora do evento não são None
            horario_evento = datetime.datetime.strptime(evento[4], "%Y-%m-%d %H:%M")
            if horario_evento >= agora:
                imprimir_evento(evento)

    print("\nEventos que já ocorreram:")
    for evento in eventos:
        if evento[4]:
            horario_evento = datetime.datetime.strptime(evento[4], "%Y-%m-%d %H:%M")
            if horario_evento < agora:
                imprimir_evento(evento)

def participar_evento(id_usuario, id_evento):
    cursor.execute('SELECT * FROM usuarios WHERE id=?', (id_usuario,))
    dados_usuario = cursor.fetchone()
    cursor.execute('SELECT * FROM eventos WHERE id=?', (id_evento,))
    dados_evento = cursor.fetchone()
    
    if dados_usuario and dados_evento:
        usuario = Usuario(dados_usuario[1], dados_usuario[2], dados_usuario[3], dados_usuario[4], dados_usuario[5])
        usuario.set_id(dados_usuario[0])
        evento = Evento(dados_evento[1], dados_evento[2], dados_evento[3], dados_evento[4], dados_evento[5])
        evento.set_id(dados_evento[0])

        eventos_participando = [Evento(*linha) for linha in cursor.execute('SELECT * FROM usuario_eventos WHERE id_usuario=?', (id_usuario,)).fetchall()]

        usuario.set_eventos_participando(eventos_participando)
        usuario.get_eventos_participando().append(evento)
        cursor.execute('INSERT INTO usuario_eventos (id_usuario, id_evento) VALUES (?, ?)', (id_usuario, id_evento))
        conn.commit()
        print("Você está participando deste evento.")
    else:
        print("Usuário ou evento não encontrado.")

def cancelar_participacao(id_usuario, id_evento):
    cursor.execute('DELETE FROM usuario_eventos WHERE id_usuario=? AND id_evento=?', (id_usuario, id_evento))
    conn.commit()
    print("Participação cancelada com sucesso.")

def autenticar_usuario(login, senha):
    cursor.execute('SELECT id, nome, email, cpf, data_nascimento FROM usuarios WHERE login=? AND senha=?', (login, senha))
    return cursor.fetchone()

def autenticar_empresa(login, senha):
    cursor.execute('SELECT * FROM empresa_eventos WHERE login=? AND senha=?', (login, senha))
    return cursor.fetchone()

def imprimir_evento(evento):
    print(f"ID: {evento[0]}")
    print(f"Nome: {evento[1]}")
    print(f"Endereço: {evento[2]}")
    print(f"Categoria: {evento[3]}")
    print(f"Horário: {evento[4]}")
    print(f"Descrição: {evento[5]}\n")

#def menu_usuario():
    
    
#def menu_empresa(opcao):
    

def main():
    while True:
        print("\nOpções:")
        print("1. Cadastrar")
        print("2. Entrar (Login)")
        print("3. Sair")
        escolha = input("Escolha uma opção: ")
        if escolha == '1':
            print('Escolha o tipo de cadastro:')
            print('1. Cadastro de Usuário')
            print('2. Cadastro de empresa')
            
            escolha_empresa_usuario = input("Escolha uma opção:")
            if escolha_empresa_usuario == '1':
                nome = input("Nome: ")
                email = input("E-mail: ")
                cpf = input("CPF: ")
                data_nascimento = input("data_nascimento (AAAA-MM-DD): ")
                login = input("Login: ")
                senha = input("Senha: ")
                criar_usuario(nome, email, cpf, data_nascimento, login, senha)
            elif escolha_empresa_usuario == '2':
                nome_empresa = input("Nome da empresa: ")
                email_empresa = input("Email: ")
                telefone_empresa = input("Telefone: ")
                cnpj_empresa = input('CNPJ: ')
                login_empresa = input('Login: ')
                senha_empresa = input('Senha: ')
                criar_empresa(nome_empresa, email_empresa, telefone_empresa,cnpj_empresa, login_empresa, senha_empresa)
                
        elif escolha == '2':
            print('Opções: ')
            print('1. Login Usuário')
            print('2. Login Empresa')
            escolha_login = input('Escolha uma opção: ')
            if escolha_login == '1':
                login = input("Login: ")
                senha = input("Senha: ")
                usuario_autenticado = autenticar_usuario(login, senha)
                
                if usuario_autenticado:
                    print(f"Bem-vindo, {usuario_autenticado[1]}!")
                    id_usuario_autenticado = usuario_autenticado[0]
                    
                    while True:
                        print("1. Listar Eventos")
                        print("2. Confirmar Participação em um Evento")
                        print("3. Cancelar Participação em um Evento")
                        print("4. Alterar Cadastro")
                        print("5. Logout")
                        opcao = input('Escolha a opção: ')
                        if opcao == '1':
                            listar_eventos()
                        elif opcao == '2':
                            listar_eventos()
                            id_evento = input("Digite o ID do evento para participar: ")
                            participar_evento(id_usuario_autenticado, id_evento)
                        elif opcao == '3':
                            id_evento = input("Digite o ID do evento para cancelar participação: ")
                            cancelar_participacao(id_usuario_autenticado, id_evento)
                        elif opcao == '4':
                            # Implementar a lógica para alterar cadastro usando id_usuario_autenticado
                            pass
                        elif opcao == '5':
                            print("Logout realizado com sucesso!")
                            id_usuario_autenticado = None
                            break
                        else:
                            print("Opção inválida.")
            elif escolha_login == '2':
                login = input("Login: ")
                senha = input("Senha: ")
                usuario_autenticado_empresa = autenticar_empresa(login, senha)
                
                if usuario_autenticado_empresa:
                    print(f"Bem-vindo, {usuario_autenticado_empresa[1]}!")

                    while True:
                        print("1. Criar Evento")
                        print("2. Listar Eventos Criados")
                        print("3. Listar Clientes Confirmados")
                        print("4. Alterar Cadastro")
                        print("5. Logout")
                        opcao_empresa = input("Escolha uma opção: ")
                        if opcao_empresa == '1':
                            nome_evento = input("Nome do evento: ")
                            endereco_evento = input("Endereço do evento: ")
                            categoria_evento = input("Categoria do evento: ")
                            horario_evento = input("Data e Horário do evento (AAAA-MM-DD HH:MM): ")
                            descricao_evento = input("Descrição do evento: ")
                            criar_evento(nome_evento, endereco_evento, categoria_evento, horario_evento, descricao_evento)
                        elif opcao_empresa == '2':
                            listar_eventos()
                        elif opcao_empresa == '3':
                            pass
                        elif opcao_empresa == '4':
                            pass
                        elif opcao_empresa == '5':
                            print("Logout realizado com sucesso!")
                            break
                        else:
                            print('Opção Invalida.')   
            else:
                print("Login ou senha incorretos.")
        elif escolha == '3':
             print("Encerrando o programa.")
             break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
