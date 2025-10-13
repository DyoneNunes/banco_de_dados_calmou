class Notificacao:
    def __init__(self, id, usuario_id, titulo, mensagem, lida=False, data_envio=None):
        self.id = id
        self.usuario_id = usuario_id
        self.titulo = titulo
        self.mensagem = mensagem
        self.lida = lida
        self.data_envio = data_envio