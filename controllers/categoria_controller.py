from controllers.base_controller import BaseController

class CategoriaController(BaseController):
    def criar(self, usuario_id, nome, descricao=None):
        query = """
            INSERT INTO categoria_despesa (usuario_id, nome, descricao)
            VALUES (%s, %s, %s)
            RETURNING *;
        """
        return self.executar(query, (usuario_id, nome, descricao), fetch_one=True)

    def listar_por_usuario(self, usuario_id):
        query = """
            SELECT * FROM categoria_despesa
            WHERE usuario_id = %s
            ORDER BY nome;
        """
        return self.executar(query, (usuario_id,), fetch=True)

    def atualizar(self, categoria_id, nome, descricao):
        query = """
            UPDATE categoria_despesa
            SET nome = %s, descricao = %s
            WHERE id = %s
            RETURNING *;
        """
        return self.executar(query, (nome, descricao, categoria_id), fetch_one=True)

    def excluir(self, categoria_id):
        query = "DELETE FROM categoria_despesa WHERE id = %s;"
        return self.executar(query, (categoria_id,))