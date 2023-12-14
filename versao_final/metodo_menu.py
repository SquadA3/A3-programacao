import DAO_usuarios as usuario
import DAO_eventos as evento
import database
import os

id_usuario_autenticado = None
id_empresa_autenticada = None

def main():
    evento.limpar_tela()
    while True:
        print("============================================================")
        print("|                       EventPlanner                       |")
        print("|                  Sua agenda de ventos                    |")
        print("============================================================")
        print("\nOpções:")
        print("1. Cadastrar")
        print("2. Entrar (Login)")
        print("3. Sair")
        escolha = input("Escolha uma opção: ")
        if escolha == '1':
            evento.limpar_tela()
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
                usuario.criar_usuario_simples(nome, email, cpf, data_nascimento, login, senha)
            elif escolha_empresa_usuario == '2':
                nome_empresa = input("Nome da empresa: ")
                email_empresa = input("Email: ")
                telefone_empresa = input("Telefone: ")
                cnpj_empresa = input('CNPJ: ')
                login_empresa = input('Login: ')
                senha_empresa = input('Senha: ')
                usuario.criar_empresa(nome_empresa, email_empresa, telefone_empresa,cnpj_empresa, login_empresa, senha_empresa)
                
        elif escolha == '2':
            evento.limpar_tela()
            print('Opções: ')
            print('1. Login Usuário')
            print('2. Login Empresa')
            print('3. Cancelar')
            escolha_login = input('Escolha uma opção: ')
            if escolha_login == '1':
                login = input("Login: ")
                senha = input("Senha: ")
                usuario_autenticado = usuario.autenticar_usuario(login, senha)
                if usuario_autenticado:
                    print(f"Bem-vindo, {usuario_autenticado[1]}!\n")
                    id_usuario_autenticado = usuario_autenticado[0]
                    input('Pressione Enter para continuar...')
                    evento.limpar_tela()
                    while True:
                        print("============================================================")
                        print("|                       EventPlanner                       |")
                        print("|                  Sua agenda de ventos                    |")
                        print("============================================================")
                        print("Usuário: ", usuario_autenticado[1], "\n")
                        print("1. Listar Eventos Confirmados")
                        print("2. Confirmar Participação em um Evento")
                        print("3. Cancelar Participação em um Evento")
                        print("4. Logout")
                        opcao = input('Escolha a opção: ')
                        if opcao == '1':
                            usuario.listar_eventos_confirmados(id_usuario_autenticado)
                            input('Pressione Enter para continuar...')
                            evento.limpar_tela()
                        elif opcao == '2':
                            print("Qual categoria de evento gostaria de participar?")
                            print("1 - Música")
                            print("2 - Teatro")
                            print("3 - Cinema")
                            print("4 - Stand-Up")
                            print("5 - Todos")
                            opcoes_categoria = {
                                                '1': 'Música',
                                                '2': 'Teatro',
                                                '3': 'Cinema',
                                                '4': 'Stand-Up',
                                                '5': 'Todos'
                                                }
                            opcao_categoria = input('Escolha uma opção: ')

                            if opcao_categoria in opcoes_categoria:
                                categoria = opcoes_categoria[opcao_categoria]
                                if opcao_categoria == '5':
                                    evento.limpar_tela()
                                    evento.listar_eventos()
                                else:
                                    evento.limpar_tela()
                                    evento.listar_eventos_por_categoria(categoria)
                            else:
                                print('Opção Inválida')
                            id_evento = input("Digite o ID do evento para participar: ")
                            usuario.participar_evento(id_usuario_autenticado, id_evento)
                        elif opcao == '3':
                            database.cursor.execute('SELECT COUNT(*) FROM usuario_eventos WHERE id_usuario=?', (id_usuario_autenticado,))
                            eventos_confirmados = database.cursor.fetchone()[0]
                            if eventos_confirmados == 0:
                                print('Você não possui eventos confirmados para cancelar')
                                input('pressione Enter para continuar')
                                evento.limpar_tela()
                            else:
                                evento.limpar_tela()
                                usuario.listar_eventos_confirmados(id_usuario_autenticado)
                                id_evento = input('Informe o ID do evento que deseja cancelar: ')
                                usuario.cancelar_participacao(id_usuario_autenticado, id_evento)
                        elif opcao == '4':
                            print("Logout realizado com sucesso!")
                            input('Pressione Enter para Sair...')
                            id_usuario_autenticado = None
                            evento.limpar_tela()
                            break
                        else:
                            print("Opção inválida.")
                            input('Enter para continuar...')
                            evento.limpar_tela()
                else:
                    print("Login ou senha incorretos.(Enter para voltar...)")
                    input('')
                    os.system('cls')
                    continue
                
                
                    
            elif escolha_login == '2':
                login = input("Login: ")
                senha = input("Senha: ")
                usuario_autenticado_empresa = usuario.autenticar_empresa(login, senha)
                
                if usuario_autenticado_empresa:
                    print(f"Bem-vindo, {usuario_autenticado_empresa[1]}!")
                    id_empresa_autenticada = usuario_autenticado_empresa[0]
                    input('Pressione Enter para continuar...')
                    evento.limpar_tela()
                    while True:
                        print("============================================================")
                        print("|                       EventPlanner                       |")
                        print("|                  Sua agenda de ventos                    |")
                        print("============================================================")
                        print("Usuário: ", usuario_autenticado_empresa[1], "\n")
                        print("1. Criar Evento")
                        print("2. Listar Eventos Criados")
                        print("3. Alterar Evento")
                        print("4. Deletar Evento")
                        print("5. Logout")
                        
                        opcao_empresa = input("Escolha uma opção: ")
                        if opcao_empresa == '1':
                            evento.limpar_tela()
                            print('*** Cadastrar Evento ***\n')
                            nome_evento = input("Nome do evento: ")
                            endereco_evento = input("Endereço do evento: ")
                            print('1 - Música')
                            print('2 - Teatro')
                            print('3 - Cinema')
                            print('4 - Stund-Up')
                            opcao_evento = input("Escolha a opção do tipo de evento: ")
                            if opcao_evento == '1':
                                categoria_evento = 'Música'
                            elif opcao_evento == '2':
                                categoria_evento = 'Teatro'
                            elif opcao_evento == '3':
                                categoria_evento = 'Cinema'
                            elif opcao_evento == '4':
                                categoria_evento = 'Stund-Up'
                            else:
                                print('Opção invalida!')
                            horario_evento = input("Data e Horário do evento (AAAA-MM-DD HH:MM): ")
                            descricao_evento = input("Descrição do evento: ")
                            evento.criar_evento(nome_evento, endereco_evento, categoria_evento, horario_evento, descricao_evento, id_empresa_autenticada)
                        elif opcao_empresa == '2':
                            evento.limpar_tela()
                            evento.listar_eventos_empresa(id_empresa_autenticada)
                            input('Pressione Enter para continuar')
                            evento.limpar_tela()
                        elif opcao_empresa == '3':
                            print('*** ALTERAR EVENTO ***')
                            id_evento = input('Informe o ID do evento que deseja alterar: ')
                            novo_nome = input('Informe o novo nome: ')
                            novo_endereco = input('Informe o novo endereço: ')
                            nova_categoria = input('Informe a nova categoria: ')
                            novo_horario = input('Informe o novo horario: ')
                            nova_descricao = input('Informe o nova descrição: ')
                            evento.alterar_evento(id_evento, novo_nome, novo_endereco, nova_categoria, novo_horario, nova_descricao, id_empresa_autenticada)
                        elif opcao_empresa == '4':
                            evento.limpar_tela()
                            evento.listar_eventos_empresa(id_empresa_autenticada)
                            print('*** DELETAR EVENTO ***')
                            id_evento_deletar = input('Informe o ID do evento que deseja deletar: ')
                            evento.deletar_evento(id_evento_deletar, id_empresa_autenticada)
                        elif opcao_empresa == '5':
                            print("Logout realizado com sucesso!\n")
                            input("Pressione Enter para continuar...")
                            evento.limpar_tela()
                            break
                        else:
                            print('Opção Invalida.')
            elif escolha_login == '3':
                evento.limpar_tela()
                continue
                
            else:
                print("Login ou senha incorretos.")
                
        elif escolha == '3':
             print("Encerrando o programa.")
             break
        else:
            print("Opção inválida. Tente novamente.")
            continue