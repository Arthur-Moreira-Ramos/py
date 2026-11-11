from base_model import BaseModel
class AporteObjetivo(BaseModel):
    tabela = 'aporte_objetivo'
    campos = (
        'objetivo_id', 
        'valor', 
        'data_aporte'
    );