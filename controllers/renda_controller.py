from controllers.base_controller import BaseController

class RendaController(BaseController):
    def criar(self, usuario_id, descricao, valor, periodicidade, ativa=True):
        if valor <= 0:
            raise ValueError("O valor da renda deve ser maior que zero.")

        query = """
            INSERT INTO renda (usuario_id, descricao, valor, periodicidade, ativa)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING *;
        """
        params = (usuario_id, descricao, valor, periodicidade, ativa)
        return self.executar(query, params, fetch_one=True)

    def listar_por_usuario(self, usuario_id, apenas_ativas=False):
        query = "SELECT * FROM renda WHERE usuario_id = %s"
        if apenas_ativas:
            query += " AND ativa = TRUE"
        query += " ORDER BY id DESC;"
        return self.executar(query, (usuario_id,), fetch=True)

    def atualizar(self, renda_id, descricao, valor, periodicidade, ativa):
        query = """
            UPDATE renda
            SET descricao = %s, valor = %s, periodicidade = %s, ativa = %s
            WHERE id = %s
            RETURNING *;
        """
        params = (descricao, valor, periodicidade, ativa, renda_id)
        return self.executar(query, params, fetch_one=True)

    def excluir(self, renda_id):
        query = "DELETE FROM renda WHERE id = %s;"
        return self.executar(query, (renda_id,))

    def total_renda_ativa(self, usuario_id):
        query = """
            SELECT COALESCE(SUM(valor), 0) AS total
            FROM renda
            WHERE usuario_id = %s AND ativa = TRUE;
        """
        res = self.executar(query, (usuario_id,), fetch_one=True)
        return res["total"] if res else 0