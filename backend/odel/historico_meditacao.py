class HistoricoMeditacao:
    def __init__(self, id, usuario_id, meditacao_id, duracao_real_minutos, data_conclusao=None):
        self.id = id
        self.usuario_id = usuario_id
        self.meditacao_id = meditacao_id
        self.duracao_real_minutos = duracao_real_minutos
        self.data_conclusao = data_conclusao