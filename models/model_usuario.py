from base_model import BaseModel

class Usuario(BaseModel):
    tabela = 'usuario'
    campos = (
        'nome', 
        'email', 
        'data_cadastro'
    );