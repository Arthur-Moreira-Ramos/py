from base_model import BaseModel
class CategoriaDespesa(BaseModel):
    tabela = 'categoria_despesa'
    campos = (
        'usuario_id', 
        'nome', 
        'descricao'
    );