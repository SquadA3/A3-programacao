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