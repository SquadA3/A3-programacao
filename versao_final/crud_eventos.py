import database
import datetime
import os

def limpar_tela():
    os.system('cls')

def criar_evento(nome, endereco, categoria, horario, descricao, id_empresa):
    database.cursor.execute('''
        INSERT INTO eventos (nome, endereco, categoria, horario, descricao, id_empresa)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nome, endereco, categoria, horario, descricao, id_empresa))
    database.conn.commit()
    print("Evento cadastrado com sucesso!\n")
    input('Pressione Enter para continuar...')
    limpar_tela()

def listar_eventos():
    agora = datetime.datetime.now()
    database.cursor.execute('SELECT * FROM eventos ORDER BY horario')
    eventos = database.cursor.fetchall()

    if not eventos:
        print("Não há eventos disponíveis.")
        return

    print("\nEventos disponíveis:")
    for evento in eventos:
        if evento[4]:  # Verifique se a data e hora do evento não são None
            horario_evento = datetime.datetime.strptime(evento[5], "%Y-%m-%d %H:%M")
            if horario_evento >= agora:
                imprimir_evento(evento)

    print("\nEventos que já ocorreram:")
    for evento in eventos:
        if evento[4]:
            horario_evento = datetime.datetime.strptime(evento[5], "%Y-%m-%d %H:%M")
            if horario_evento < agora:
                imprimir_evento(evento)
                
def listar_eventos_por_categoria(categoria):
    agora = datetime.datetime.now()
    database.cursor.execute('SELECT * FROM eventos WHERE categoria = ? ORDER BY horario', (categoria,))
    eventos = database.cursor.fetchall()

    if not eventos:
        print(f"Não há eventos disponíveis na categoria {categoria}.\n")
        return

    print(f"\nEventos disponíveis na categoria {categoria}:")
    for evento in eventos:
        if evento[4]:  # Verifique se a data e hora do evento não são None
            horario_evento = datetime.datetime.strptime(evento[5], "%Y-%m-%d %H:%M")
            if horario_evento >= agora:
                imprimir_evento(evento)

    print(f"\nEventos na categoria {categoria} que já ocorreram:")
    for evento in eventos:
        if evento[4]:
            horario_evento = datetime.datetime.strptime(evento[5], "%Y-%m-%d %H:%M")
            if horario_evento < agora:
                imprimir_evento(evento)
                
import datetime

def listar_eventos_empresa(id_empresa):
    agora = datetime.datetime.now()

    # Consulta SQL para obter todos os eventos criados pela empresa
    consulta = '''
        SELECT *
        FROM eventos
        WHERE id_empresa = ?;
    '''

    # Executar a consulta
    database.cursor.execute(consulta, (id_empresa,))
    eventos_criados_pela_empresa = database.cursor.fetchall()

    
    eventos_nao_ocorridos = []
    eventos_ocorridos = []

    for evento in eventos_criados_pela_empresa:
        horario_evento = datetime.datetime.strptime(evento[5], '%Y-%m-%d %H:%M')

        if horario_evento >= agora:
            eventos_nao_ocorridos.append(evento)
        else:
            eventos_ocorridos.append(evento)

    # Exibir os eventos não ocorridos
    if eventos_nao_ocorridos:
        print("\nEventos não ocorridos criados pela empresa:")
        for evento in eventos_nao_ocorridos:
            imprimir_evento_empresa(evento)
    else:
        print("\nA empresa não tem eventos não ocorridos.")

    # Exibir os eventos ocorridos
    if eventos_ocorridos:
        print("\nEventos ocorridos criados pela empresa:")
        for evento in eventos_ocorridos:
            imprimir_evento_empresa(evento)
    else:
        print("\nA empresa não tem eventos ocorridos.")

def alterar_evento(id_evento, nome, endereco, categoria, horario, descricao, id_empresa_autenticada):
    # Verificar se o evento existe
    dados_evento = database.cursor.execute('SELECT * FROM eventos WHERE id=?', (id_evento,)).fetchone()

    if dados_evento:
        # Verificar se a empresa autenticada é a mesma que criou o evento
        id_empresa_evento = dados_evento[1]

        if id_empresa_autenticada == id_empresa_evento:
            # Atualizar as informações do evento
            database.cursor.execute('''
                UPDATE eventos
                SET nome=?, endereco=?, categoria=?, horario=?, descricao=?
                WHERE id=?;
            ''', (nome, endereco, categoria, horario, descricao, id_evento))

            database.conn.commit()
            print("Evento alterado com sucesso!")
        else:
            print("Você não tem permissão para alterar este evento, pois não o criou.")
    else:
        print("Evento não encontrado.")

    input('Pressione Enter para continuar...')
    limpar_tela()
    
def deletar_evento(id_evento, id_empresa_autenticada):
    # Verificar se o evento existe
    dados_evento = database.cursor.execute('SELECT * FROM eventos WHERE id=?', (id_evento,)).fetchone()

    if dados_evento:
        # Verificar se a empresa autenticada é a mesma que criou o evento
        id_empresa_evento = dados_evento[1]

        if id_empresa_autenticada == id_empresa_evento:
            # Deletar o evento do banco de dados
            database.cursor.execute('DELETE FROM eventos WHERE id=?;', (id_evento,))
            database.conn.commit()
            print("Evento deletado com sucesso!\n")
            input('Pressione Enter para continuar...')
            limpar_tela()
            
        else:
            print("Você não tem permissão para deletar este evento, pois não o criou.\n")
            input('Pressione Enter para continuar...')
            limpar_tela()
    else:
        print("Evento não encontrado.\n")
        input('Pressione Enter para continuar...')
        limpar_tela()
    
def imprimir_evento(evento):
    print(f"ID: {evento[0]}")
    print(f"Nome: {evento[1]}")
    print(f"Endereço: {evento[2]}")
    print(f"Categoria: {evento[3]}")
    print(f"Horário: {evento[4]}")
    print(f"Descrição: {evento[5]}\n")

def imprimir_evento_empresa(evento):
    print(f"ID: {evento[0]}")
    print(f"ID Empresa: {evento[1]}")
    print(f"Nome: {evento[2]}")
    print(f"Endereço: {evento[3]}")
    print(f"Categoria: {evento[4]}")
    print(f"Horário: {evento[5]}")
    print(f"Descrição: {evento[6]}\n")