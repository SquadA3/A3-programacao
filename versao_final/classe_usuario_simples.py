from classe_usuarios import Usuarios

class UsuarioSimples(Usuarios):
    def __init__(self, nome, cpf, data_nascimento, email, login, senha):
        super().__init__(nome, email, login, senha)
        self._id = None
        self._cpf = cpf
        self._data_nascimento = data_nascimento
        self._eventos_participando = []  # Corrigido o nome do atributo

    def get_id(self):
        return self._id

    def set_id(self, identificador):
        self._id = identificador

    def get_cpf(self):
        return self._cpf

    def set_cpf(self, cpf):
        self._cpf = cpf

    def get_data_nascimento(self):
        return self._data_nascimento

    def set_data_nascimento(self, data_nascimento):
        self._data_nascimento = data_nascimento

    def get_eventos_participando(self):
        return self._eventos_participando

    def set_eventos_participando(self, eventos_participando):
        self._eventos_participando = eventos_participando
