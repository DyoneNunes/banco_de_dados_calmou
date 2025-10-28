"""
Model para Histórico de Meditações
Representa o registro de meditações concluídas por usuários
"""


class HistoricoMeditacao:
    """Modelo de dados para histórico de meditações realizadas"""

    def __init__(self, id=None, usuario_id=None, meditacao_id=None,
                 data_conclusao=None, duracao_real_minutos=None):
        self.id = id
        self.usuario_id = usuario_id
        self.meditacao_id = meditacao_id
        self.data_conclusao = data_conclusao
        self.duracao_real_minutos = duracao_real_minutos

    def __repr__(self):
        return f"<HistoricoMeditacao(id={self.id}, usuario_id={self.usuario_id}, meditacao_id={self.meditacao_id})>"

    def to_dict(self):
        """Converte o objeto para um dicionário"""
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'meditacao_id': self.meditacao_id,
            'data_conclusao': self.data_conclusao.isoformat() if self.data_conclusao else None,
            'duracao_real_minutos': self.duracao_real_minutos
        }
