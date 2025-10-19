class Usuario:
    """Modelo de dados para representar um usuário do sistema."""
    
    def __init__(self, id=None, nome=None, email=None, password_hash=None, 
                 config=None, data_cadastro=None, cpf=None, 
                 data_nascimento=None, tipo_sanguineo=None, alergias=None,
                 foto_perfil=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.password_hash = password_hash
        self.config = config
        self.data_cadastro = data_cadastro
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.tipo_sanguineo = tipo_sanguineo
        self.alergias = alergias
        self.foto_perfil = foto_perfil
    
    def __repr__(self):
        return f"<Usuario(id={self.id}, nome='{self.nome}', email='{self.email}')>"
    
    def to_dict(self):
        """Converte o objeto Usuario para um dicionário."""
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'config': self.config,
            'data_cadastro': self.data_cadastro.isoformat() if self.data_cadastro else None,
            'cpf': self.cpf,
            'data_nascimento': self.data_nascimento.isoformat() if self.data_nascimento else None,
            'tipo_sanguineo': self.tipo_sanguineo,
            'alergias': self.alergias
        }