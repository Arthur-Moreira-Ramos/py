class Despesa(BaseModel):
    tabela = 'despesa'
    campos = (
        'usuario_id', 
        'categoria_id', 
        'descricao', 
        'valor', 
        'tipo', 
        'data_despesa', 
        'pago'
    );