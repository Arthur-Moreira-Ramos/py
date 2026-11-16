from controllers.base_controller import BaseController

class DistribuicaoController(BaseController):
    def definir_regra(self, usuario_id, objetivo_id, porcentagem):
        if not (0 < porcentagem <= 100):
            raise ValueError("A porcentagem deve estar entre 0.01 e 100.")

        # Verifica quanto o usuário já tem comprometido em outros objetivos
        total_atual = self.total_porcentagem_usuario(usuario_id, ignorar_objetivo_id=objetivo_id)
        if total_atual + porcentagem > 100:
            disponivel = 100 - total_atual
            raise ValueError(f"Limite excedido. Você possui apenas {disponivel:.2f}% disponível para distribuir.")

        # Verifica se já existe regra para este objetivo (Atualiza ou Insere)
        existente = self.buscar_por_objetivo(objetivo_id)
        if existente:
            query = """
                UPDATE regra_distribuicao
                SET porcentagem = %s
                WHERE objetivo_id = %s
                RETURNING *;
            """
            return self.executar(query, (porcentagem, objetivo_id), fetch_one=True)
        else:
            query = """
                INSERT INTO regra_distribuicao (objetivo_id, porcentagem)
                VALUES (%s, %s)
                RETURNING *;
            """
            return self.executar(query, (objetivo_id, porcentagem), fetch_one=True)

    def buscar_por_objetivo(self, objetivo_id):
        query = "SELECT * FROM regra_distribuicao WHERE objetivo_id = %s;"
        return self.executar(query, (objetivo_id,), fetch_one=True)

    def listar_por_usuario(self, usuario_id):
        query = """
            SELECT r.id, r.objetivo_id, o.descricao AS objetivo_descricao, r.porcentagem
            FROM regra_distribuicao r
            INNER JOIN objetivo_financeiro o ON r.objetivo_id = o.id
            WHERE o.usuario_id = %s
            ORDER BY r.porcentagem DESC;
        """
        return self.executar(query, (usuario_id,), fetch=True)

    def total_porcentagem_usuario(self, usuario_id, ignorar_objetivo_id=None):
        query = """
            SELECT COALESCE(SUM(r.porcentagem), 0) AS total
            FROM regra_distribuicao r
            INNER JOIN objetivo_financeiro o ON r.objetivo_id = o.id
            WHERE o.usuario_id = %s
        """
        params = [usuario_id]
        if ignorar_objetivo_id:
            query += " AND r.objetivo_id != %s"
            params.append(ignorar_objetivo_id)

        res = self.executar(query + ";", tuple(params), fetch_one=True)
        return float(res["total"]) if res else 0.0

    def calcular_rateio(self, usuario_id, valor_livre):
        """Calcula quanto em R$ cada objetivo receberia dado um valor livre (ex: Renda - Despesas)."""
        regras = self.listar_por_usuario(usuario_id)
        rateio = []
        for regra in regras:
            valor_destinado = round((float(regra["porcentagem"]) / 100.0) * float(valor_livre), 2)
            rateio.append({
                "objetivo_id": regra["objetivo_id"],
                "objetivo": regra["objetivo_descricao"],
                "porcentagem": regra["porcentagem"],
                "valor_destinado": valor_destinado
            })
        return rateio

    def excluir(self, regra_id):
        query = "DELETE FROM regra_distribuicao WHERE id = %s;"
        return self.executar(query, (regra_id,))