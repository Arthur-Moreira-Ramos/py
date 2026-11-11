from base_model import BaseModel

class RegraDistribuicao(BaseModel):
    tabela = 'regra_distribuicao'
    campos = (
        'objetivo_id', 
        'porcentagem'
    );