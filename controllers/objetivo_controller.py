from controllers.base_controller import BaseController

class ObjetivoController(BaseController):
    def criar(self, usuario_id, descricao, valor_meta, data_inicio, data_limite=None):
        if valor_meta <= 0:
            raise ValueError("O valor da meta deve ser maior que zero.")

        query = """
            INSERT INTO objetivo_financeiro (usuario_id, descricao, valor_meta, data_inicio, data_limite)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING *;
        """
        params = (usuario_id, descricao, valor_meta, data_inicio, data_limite)
        return self.executar(query, params, fetch_one=True)

    def listar_com_progresso(self, usuario_id):
        query = """
            SELECT 
                o.*,
                COALESCE(SUM(a.valor), 0) AS valor_acumulado,
                ROUND((COALESCE(SUM(a.valor), 0) / NULLIF(o.valor_meta, 0)) * 100, 2) AS percentual_concluido
            FROM objetivo_financeiro o
            LEFT JOIN aporte_objetivo a ON o.id = a.objetivo_id
            WHERE o.usuario_id = %s
            GROUP BY o.id
            ORDER BY o.data_limite ASC NULLS LAST;
        """
        return self.executar(query, (usuario_id,), fetch=True)

    def atualizar(self, objetivo_id, descricao, valor_meta, data_inicio, data_limite):
        query = """
            UPDATE objetivo_financeiro
            SET descricao = %s, valor_meta = %s, data_inicio = %s, data_limite = %s
            WHERE id = %s
            RETURNING *;
        """
        params = (descricao, valor_meta, data_inicio, data_limite, objetivo_id)
        return self.executar(query, params, fetch_one=True)

    def excluir(self, objetivo_id):
        query = "DELETE FROM objetivo_financeiro WHERE id = %s;"
        return self.executar(query, (objetivo_id,))