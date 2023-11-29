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