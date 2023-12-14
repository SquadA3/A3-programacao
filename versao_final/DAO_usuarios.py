import database
import os
import classe_usuario_simples as uSimples
import classe_evento as eventos
import datetime
import re

def limpar_tela():
    os.system('cls')

def criar_usuario_simples(nome, email, cpf, data_nascimento, login, senha):
    try:
        # Verificar se o CPF tem 11 dígitos e contém apenas números
        if not (re.match(r"^\d{11}$", cpf) and cpf.isnumeric()):
            raise ValueError("CPF inválido. Deve conter 11 dígitos e ser composto apenas por números.")

        # Verificar se o login já existe no banco de dados
        database.cursor.execute('SELECT COUNT(*) FROM usuario_simples WHERE login = ?', (login,))
        if database.cursor.fetchone()[0] > 0:
            raise ValueError("Login já existe. Escolha outro login.")

        # Verificar se o CPF já existe no banco de dados
        database.cursor.execute('SELECT COUNT(*) FROM usuario_simples WHERE cpf = ?', (cpf,))
        if database.cursor.fetchone()[0] > 0:
            raise ValueError("CPF já cadastrado. Faça seu login.")

        # Inserir o novo usuário no banco de dados
        database.cursor.execute('INSERT INTO usuario_simples (nome, email, cpf, data_nascimento, login, senha) VALUES (?, ?, ?, ?, ?, ?)', (nome, email, cpf, data_nascimento, login, senha))
        database.conn.commit()

        print("Usuário cadastrado com sucesso!")

    except ValueError as e:
        print(f"Erro: {e}")

    input('Pressione Enter para continuar...')
    limpar_tela()  
    
def criar_empresa(nome, email, telefone, cnpj, login, senha):
    database.cursor.execute('INSERT INTO usuario_empresa (nome, email, telefone, cnpj, login, senha) VALUES (?, ?, ?, ?, ?, ?)', (nome, email, telefone, cnpj, login, senha))
    database.conn.commit()
    print("Usuário cadastrado com sucesso!")
    input('Pressione Enter para continuar...')
    limpar_tela()
    
def autenticar_usuario(login, senha):
    database.cursor.execute('SELECT id, nome, email, cpf, data_nascimento FROM usuario_simples WHERE login=? AND senha=?', (login, senha))
    return database.cursor.fetchone()

def autenticar_empresa(login, senha):
    database.cursor.execute('SELECT * FROM usuario_empresa WHERE login=? AND senha=?', (login, senha))
    return database.cursor.fetchone()

def participar_evento(id_usuario, id_evento):
    database.cursor.execute('SELECT * FROM usuario_simples WHERE id=?', (id_usuario,))
    dados_usuario = database.cursor.fetchone()
    database.cursor.execute('SELECT * FROM eventos WHERE id=?', (id_evento,))
    dados_evento = database.cursor.fetchone()
    
    if dados_usuario and dados_evento:
        # Verificar se o usuário já está participando do evento
        participando = database.cursor.execute('SELECT * FROM usuario_eventos WHERE id_usuario=? AND id_evento=?', (id_usuario, id_evento)).fetchone()

        if participando:
            print("Você já está participando deste evento.")
        else:
            usuario = uSimples.UsuarioSimples(dados_usuario[1], dados_usuario[2], dados_usuario[3], dados_usuario[4], dados_usuario[5], dados_usuario[6])
            usuario.set_id(dados_usuario[0])
            evento = eventos.Evento(dados_evento[1], dados_evento[2], dados_evento[3], dados_evento[4], dados_evento[5])
            evento.set_id(dados_evento[0])

            # Adicionar o evento à lista de eventos que o usuário está participando
            eventos_participando = [eventos.Evento(*linha) for linha in database.cursor.execute('SELECT * FROM usuario_eventos WHERE id_usuario=?', (id_usuario,)).fetchall()]
            usuario.set_eventos_participando(eventos_participando)
            usuario.get_eventos_participando().append(evento)

            # Inserir no banco de dados que o usuário está participando do evento
            database.cursor.execute('INSERT INTO usuario_eventos (id_usuario, id_evento) VALUES (?, ?)', (id_usuario, id_evento))
            database.conn.commit()

            print("Você está participando deste evento.")

        input('Pressione Enter para continuar...')
        limpar_tela()
    else:
        print("Evento não encontrado.")
        input('Pressione Enter para continuar...')
        limpar_tela()

def cancelar_participacao(id_usuario, id_evento):
    database.cursor.execute('DELETE FROM usuario_eventos WHERE id_usuario=? AND id_evento=?', (id_usuario, id_evento))
    database.conn.commit()
    print("Participação cancelada com sucesso.")
    input('Pressione Enter para continuar...')
    limpar_tela()
    

    
def listar_eventos_confirmados(id_usuario):
    agora = datetime.datetime.now()

    # Consulta SQL para obter eventos confirmados pelo usuário
    consulta = '''
        SELECT eventos.*
        FROM eventos
        JOIN usuario_eventos ON eventos.id = usuario_eventos.id_evento
        WHERE usuario_eventos.id_usuario = ? AND eventos.horario >= ?;
    '''

    # Executar a consulta
    database.cursor.execute(consulta, (id_usuario, agora))
    eventos_confirmados = database.cursor.fetchall()

    # Exibir os eventos confirmados
    if eventos_confirmados:
        print("\nEventos confirmados nos quais você está participando:")
        for evento in eventos_confirmados:
            imprimir_evento(evento)
    else:
        print("\nVocê não confirmou presença em nenhum evento.")
       


def imprimir_evento(evento):
    print(f"ID: {evento[0]}")
    print(f"Nome: {evento[1]}")
    print(f"Endereço: {evento[2]}")
    print(f"Categoria: {evento[3]}")
    print(f"Horário: {evento[4]}")
    print(f"Descrição: {evento[5]}\n")