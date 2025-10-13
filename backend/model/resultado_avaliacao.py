class ResultadoAvaliacao:
    def __init__(self, id, usuario_id, tipo, respostas, resultado_score, resultado_texto, data_avaliacao=None):
        self.id = id
        self.usuario_id = usuario_id
        self.tipo = tipo
        self.respostas = respostas
        self.resultado_score = resultado_score
        self.resultado_texto = resultado_texto
        self.data_avaliacao = data_avaliacao