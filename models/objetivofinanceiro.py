from base_model import BaseModel
class ObjetivoFinanceiro(BaseModel):
    tabela = 'objetivo_financeiro'
    campos = (
        'usuario_id', 
        'descricao', 
        'valor_meta', 
        'data_inicio', 
        'data_limite'
    );