from classe_usuarios import Usuarios

class Empresa(Usuarios):
    def __init__(self, nome, cnpj, email, telefone, login, senha):
        super().__init__(nome, email, login, senha)
        self._id = None
        self._cnpj = cnpj
        self._telefone = telefone
        
    def get_id(self):
        return self._id

    def set_id(self, identificador):
        self._id = identificador

    def get_cnpj(self):
        return self._cnpj

    def set_cnpj(self, cnpj):
        self._cnpj = cnpj
        
    def get_telefone(self):
        return self._cnpj

    def set_telefone(self, cnpj):
        self._cnpj = cnpj

  