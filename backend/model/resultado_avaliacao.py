class ResultadoAvaliacao:
    """
    Modelo para representar o resultado de uma avaliação de saúde mental.
    
    Atributos:
        id (int): ID único do resultado (gerado pelo banco)
        usuario_id (int): ID do usuário que fez a avaliação
        tipo (str): Tipo de avaliação (ex: 'ansiedade', 'depressao', 'estresse')
        respostas (dict): Dicionário com as respostas do questionário (armazenado como JSONB)
        resultado_score (int): Pontuação total da avaliação
        resultado_texto (str): Classificação textual do resultado (ex: 'Leve', 'Moderado', 'Grave')
        data_avaliacao (datetime): Data e hora da avaliação (gerado automaticamente pelo banco)
    """
    
    def __init__(self, id, usuario_id, tipo, respostas, resultado_score, resultado_texto, data_avaliacao=None):
        self.id = id
        self.usuario_id = usuario_id
        self.tipo = tipo
        self.respostas = respostas  # Dict que será convertido para JSONB
        self.resultado_score = resultado_score
        self.resultado_texto = resultado_texto
        self.data_avaliacao = data_avaliacao
    
    def to_dict(self):
        """Converte o objeto para um dicionário."""
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'tipo': self.tipo,
            'respostas': self.respostas,
            'resultado_score': self.resultado_score,
            'resultado_texto': self.resultado_texto,
            'data_avaliacao': self.data_avaliacao.isoformat() if self.data_avaliacao else None
        }
    
    def __repr__(self):
        """Representação em string do objeto."""
        return f"ResultadoAvaliacao(id={self.id}, usuario_id={self.usuario_id}, tipo='{self.tipo}', score={self.resultado_score}, resultado='{self.resultado_texto}')"