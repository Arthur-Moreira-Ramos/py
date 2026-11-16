from controllers.base_controller import BaseController
# from models.modelo_despesa import Despesa

class DespesaController(BaseController):
    def adicionar_despesa(self, usuario_id, categoria_id, descricao, valor, data_despesa):
        if valor <= 0:
            raise ValueError("O valor da despesa deve ser maior que zero.")
            
        query = """
            INSERT INTO despesas (usuario_id, categoria_id, descricao, valor, data_despesa)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
        """
        resultado = self.executar_comando(
            query, 
            (usuario_id, categoria_id, descricao, valor, data_despesa), 
            fetch_one=True
        )
        return resultado[0] if resultado else None

    def listar_por_usuario(self, usuario_id):
        query = """
            SELECT d.id, d.descricao, d.valor, d.data_despesa, c.nome AS categoria
            FROM despesas d
            LEFT JOIN categorias_despesa c ON d.categoria_id = c.id
            WHERE d.usuario_id = %s
            ORDER BY d.data_despesa DESC;
        """
        return self.executar_comando(query, (usuario_id,), fetch=True)

    def excluir_despesa(self, despesa_id):
        query = "DELETE FROM despesas WHERE id = %s;"
        return self.executar_comando(query, (despesa_id,))