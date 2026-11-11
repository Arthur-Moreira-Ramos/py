from base_model import BaseModel
class Renda(BaseModel):
    tabela = 'renda'
    campos = (
        'usuario_id', 
        'descricao', 
        'valor', 
        'periodicidade', 
        'ativa'
    );