from classe_usuario import Usuario

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