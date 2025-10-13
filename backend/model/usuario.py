class Usuario:
    def __init__(self, id, nome, email, senha_hash, config=None, data_cadastro=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash
        self.config = config
        self.data_cadastro = data_cadastro

    def to_string(self):
        return f"ID: {self.id}, Nome: {self.nome}, Email: {self.email}"