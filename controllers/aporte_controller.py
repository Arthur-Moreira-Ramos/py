from controllers.base_controller import BaseController

class AporteController(BaseController):
    def registrar(self, objetivo_id, valor, data_aporte=None):
        if valor <= 0:
            raise ValueError("O valor do aporte deve ser maior que zero.")

        if data_aporte:
            query = """
                INSERT INTO aporte_objetivo (objetivo_id, valor, data_aporte)
                VALUES (%s, %s, %s)
                RETURNING *;
            """
            params = (objetivo_id, valor, data_aporte)
        else:
            query = """
                INSERT INTO aporte_objetivo (objetivo_id, valor)
                VALUES (%s, %s)
                RETURNING *;
            """
            params = (objetivo_id, valor)

        return self.executar(query, params, fetch_one=True)

    def listar_por_objetivo(self, objetivo_id):
        query = """
            SELECT * FROM aporte_objetivo
            WHERE objetivo_id = %s
            ORDER BY data_aporte DESC;
        """
        return self.executar(query, (objetivo_id,), fetch=True)

    def excluir(self, aporte_id):
        query = "DELETE FROM aporte_objetivo WHERE id = %s;"
        return self.executar(query, (aporte_id,))