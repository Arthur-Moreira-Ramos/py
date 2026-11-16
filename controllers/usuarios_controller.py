from controllers.base_controller import BaseController

class UsuarioController(BaseController):
    def criar(self, nome, email):
        query = """
            INSERT INTO usuario (nome, email)
            VALUES (%s, %s)
            RETURNING id, nome, email, data_cadastro;
        """
        return self.executar(query, (nome, email), fetch_one=True)

    def buscar_por_id(self, usuario_id):
        query = "SELECT * FROM usuario WHERE id = %s;"
        return self.executar(query, (usuario_id,), fetch_one=True)

    def buscar_por_email(self, email):
        query = "SELECT * FROM usuario WHERE email = %s;"
        return self.executar(query, (email,), fetch_one=True)

    def listar_todos(self):
        query = "SELECT * FROM usuario ORDER BY nome;"
        return self.executar(query, fetch=True)

    def atualizar(self, usuario_id, nome, email):
        query = """
            UPDATE usuario
            SET nome = %s, email = %s
            WHERE id = %s
            RETURNING *;
        """
        return self.executar(query, (nome, email, usuario_id), fetch_one=True)

    def excluir(self, usuario_id):
        query = "DELETE FROM usuario WHERE id = %s;"
        return self.executar(query, (usuario_id,))