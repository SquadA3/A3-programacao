class Usuarios:
    def __init__(self, nome, email, login, senha):
        self._id = None
        self._nome = nome
        self._email = email
        self._login = login
        self._senha = senha

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
        

    def get_login(self):
        return self._login

    def set_login(self, login):
        self._login = login

    def get_senha(self):
        return self._senha

    def set_senha(self, senha):
        self._senha = senha

    