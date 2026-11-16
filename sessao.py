class Sessao:
    usuario_id = None
    usuario_nome = None

    @classmethod
    def iniciar(cls, usuario_dict):
        cls.usuario_id = usuario_dict["id"]
        cls.usuario_nome = usuario_dict["nome"]

    @classmethod
    def encerrar(cls):
        cls.usuario_id = None
        cls.usuario_nome = None