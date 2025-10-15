class Usuario:
    def __init__(self, id, nome, email, password_hash, config=None, data_cadastro=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.password_hash = password_hash
        self.config = config
        self.data_cadastro = data_cadastro

    # O método to_string é uma exigência do edital
    def to_string(self):
        return f"ID: {self.id}, Nome: {self.nome}, Email: {self.email}"
