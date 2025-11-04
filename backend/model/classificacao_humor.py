class ClassificacaoHumor:
    def __init__(self, id, usuario_id, nivel_humor, sentimento_principal, notas, data_classificacao=None):
        self.id = id
        self.usuario_id = usuario_id
        self.nivel_humor = nivel_humor
        self.sentimento_principal = sentimento_principal
        self.notas = notas
        self.data_classificacao = data_classificacao
