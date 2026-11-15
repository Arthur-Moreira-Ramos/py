"""Controllers/repositório com escopo por usuário e transações PostgreSQL.

Valores monetários são Decimal; todas as consultas recebem parâmetros.
Renda recorrente é previsão mensal, e não recebimento comprovado.
"""
from contextlib import contextmanager
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from psycopg2 import sql, IntegrityError
from psycopg2.extras import RealDictCursor
from conexao import conectar

TABLES = {
    'renda': ('descricao', 'valor', 'periodicidade', 'ativa'),
    'categoria_despesa': ('nome', 'descricao'),
    'despesa': ('categoria_id', 'descricao', 'valor', 'tipo', 'data_despesa', 'pago'),
    'objetivo_financeiro': ('descricao', 'valor_meta', 'data_inicio', 'data_limite'),
    'aporte_objetivo': ('objetivo_id', 'valor', 'data_aporte'),
    'regra_distribuicao': ('objetivo_id', 'porcentagem'),
}
MONTH_FACTORS = {'DIARIA': Decimal('30'), 'SEMANAL': Decimal('52') / 12, 'MENSAL': Decimal('1')}


def moeda_decimal(value):
    text = str(value).strip().replace('R$', '').replace(' ', '')
    if ',' in text:
        text = text.replace('.', '').replace(',', '.')
    try:
        result = Decimal(text)
    except (InvalidOperation, ValueError):
        raise ValueError('Informe um valor numérico válido.') from None
    if not result.is_finite():
        raise ValueError('O valor deve ser finito.')
    return result.quantize(Decimal('0.01'))


def data_valida(value):
    if isinstance(value, date):
        return value
    value = str(value).strip()
    try:
        return datetime.strptime(value, '%d/%m/%Y').date() if '/' in value else date.fromisoformat(value)
    except ValueError:
        raise ValueError('Data inválida. Utilize DD/MM/AAAA.') from None


@contextmanager
def sessao():
    conn = conectar()
    try:
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                yield cur
    finally:
        conn.close()


class FinanceiroController:
    def __init__(self, usuario_id):
        self.usuario_id = int(usuario_id)
        with sessao() as cur:
            cur.execute('SELECT id FROM usuario WHERE id=%s', (self.usuario_id,))
            if not cur.fetchone():
                raise ValueError('Usuário inexistente.')

    @staticmethod
    def usuarios():
        with sessao() as cur:
            cur.execute('SELECT id, nome, email FROM usuario ORDER BY nome, id')
            return cur.fetchall()

    @staticmethod
    def criar_usuario(nome, email):
        nome, email = nome.strip(), email.strip().lower()
        if not nome or '@' not in email or len(nome) > 100 or len(email) > 150:
            raise ValueError('Preencha nome e um e-mail válido.')
        with sessao() as cur:
            cur.execute('INSERT INTO usuario (nome,email) VALUES (%s,%s) RETURNING id', (nome, email))
            return cur.fetchone()['id']

    def listar(self, tabela):
        if tabela not in TABLES:
            raise ValueError('Recurso inválido.')
        with sessao() as cur:
            if tabela in ('aporte_objetivo', 'regra_distribuicao'):
                cur.execute(sql.SQL('SELECT t.* FROM {} t JOIN objetivo_financeiro o ON o.id=t.objetivo_id WHERE o.usuario_id=%s ORDER BY t.id DESC').format(sql.Identifier(tabela)), (self.usuario_id,))
            else:
                cur.execute(sql.SQL('SELECT * FROM {} WHERE usuario_id=%s ORDER BY id DESC').format(sql.Identifier(tabela)), (self.usuario_id,))
            return cur.fetchall()

    def _validar(self, tabela, dados):
        if tabela not in TABLES or not dados or set(dados) - set(TABLES[tabela]):
            raise ValueError('Campos inválidos para este formulário.')
        cleaned = dict(dados)
        for key in ('valor', 'valor_meta', 'porcentagem'):
            if key in cleaned:
                cleaned[key] = moeda_decimal(cleaned[key])
                if cleaned[key] <= 0:
                    raise ValueError('O valor deve ser maior que zero.')
        if 'porcentagem' in cleaned and cleaned['porcentagem'] > 100:
            raise ValueError('A porcentagem máxima é 100%.')
        for key in ('data_despesa', 'data_inicio', 'data_limite', 'data_aporte'):
            if key in cleaned:
                cleaned[key] = data_valida(cleaned[key])
        if 'periodicidade' in cleaned and cleaned['periodicidade'] not in MONTH_FACTORS:
            raise ValueError('Periodicidade inválida.')
        if 'tipo' in cleaned and cleaned['tipo'] not in ('FIXA', 'VARIAVEL'):
            raise ValueError('Tipo de despesa inválido.')
        for key in ('descricao', 'nome'):
            if key in cleaned:
                cleaned[key] = str(cleaned[key]).strip()
                if not cleaned[key]:
                    raise ValueError('Descrição/nome não pode ser vazio.')
        for key in ('pago', 'ativa'):
            if key in cleaned:
                cleaned[key] = cleaned[key] in (True, 1, 'Sim', 'Ativa', 'True')
        for key in ('objetivo_id', 'categoria_id'):
            if key in cleaned:
                cleaned[key] = int(cleaned[key])
        return cleaned

    def _ownership(self, cur, tabela, item_id):
        if tabela in ('aporte_objetivo', 'regra_distribuicao'):
            cur.execute(sql.SQL('SELECT t.id FROM {} t JOIN objetivo_financeiro o ON o.id=t.objetivo_id WHERE t.id=%s AND o.usuario_id=%s FOR UPDATE OF t').format(sql.Identifier(tabela)), (item_id, self.usuario_id))
        else:
            cur.execute(sql.SQL('SELECT id FROM {} WHERE id=%s AND usuario_id=%s FOR UPDATE').format(sql.Identifier(tabela)), (item_id, self.usuario_id))
        if not cur.fetchone():
            raise ValueError('Registro não encontrado para este usuário.')

    def _validar_relacoes(self, cur, tabela, dados, item_id=None):
        if 'categoria_id' in dados:
            cur.execute('SELECT id FROM categoria_despesa WHERE id=%s AND usuario_id=%s', (dados['categoria_id'], self.usuario_id))
            if not cur.fetchone():
                raise ValueError('Categoria não pertence ao usuário.')
        if 'objetivo_id' in dados:
            cur.execute('SELECT id FROM objetivo_financeiro WHERE id=%s AND usuario_id=%s', (dados['objetivo_id'], self.usuario_id))
            if not cur.fetchone():
                raise ValueError('Objetivo não pertence ao usuário.')
        if tabela == 'regra_distribuicao':
            cur.execute('SELECT COALESCE(SUM(r.porcentagem), 0) AS total FROM regra_distribuicao r JOIN objetivo_financeiro o ON o.id=r.objetivo_id WHERE o.usuario_id=%s AND (%s IS NULL OR r.id<>%s)', (self.usuario_id, item_id, item_id))
            if cur.fetchone()['total'] + dados['porcentagem'] > 100:
                raise ValueError('A soma das regras não pode superar 100%.')
        if tabela == 'objetivo_financeiro' and 'data_inicio' in dados and 'data_limite' in dados and dados['data_limite'] < dados['data_inicio']:
            raise ValueError('Prazo anterior ao início do objetivo.')

    def salvar(self, tabela, dados, item_id=None):
        dados = self._validar(tabela, dados)
        with sessao() as cur:
            if item_id is not None:
                self._ownership(cur, tabela, int(item_id))
            self._validar_relacoes(cur, tabela, dados, item_id)
            if tabela not in ('aporte_objetivo', 'regra_distribuicao') and item_id is None:
                dados['usuario_id'] = self.usuario_id
            keys = list(dados)
            if item_id is None:
                query = sql.SQL('INSERT INTO {} ({}) VALUES ({}) RETURNING id').format(sql.Identifier(tabela), sql.SQL(',').join(map(sql.Identifier, keys)), sql.SQL(',').join(sql.Placeholder() for _ in keys))
                cur.execute(query, [dados[k] for k in keys])
            else:
                query = sql.SQL('UPDATE {} SET {} WHERE id=%s RETURNING id').format(sql.Identifier(tabela), sql.SQL(',').join(sql.SQL('{}=%s').format(sql.Identifier(k)) for k in keys))
                cur.execute(query, [dados[k] for k in keys] + [int(item_id)])
            return cur.fetchone()['id']

    def excluir(self, tabela, item_id):
        if tabela not in TABLES:
            raise ValueError('Recurso inválido.')
        with sessao() as cur:
            self._ownership(cur, tabela, int(item_id))
            cur.execute(sql.SQL('DELETE FROM {} WHERE id=%s').format(sql.Identifier(tabela)), (int(item_id),))

    def resumo(self):
        today = date.today()
        start = today.replace(day=1)
        with sessao() as cur:
            cur.execute('SELECT descricao, valor, periodicidade FROM renda WHERE usuario_id=%s AND ativa', (self.usuario_id,))
            incomes = cur.fetchall()
            receita = sum((r['valor'] * MONTH_FACTORS[r['periodicidade']] for r in incomes), Decimal('0'))
            cur.execute('SELECT COALESCE(SUM(valor),0) total, COUNT(*) quantidade FROM despesa WHERE usuario_id=%s AND data_despesa >= %s AND data_despesa <= %s', (self.usuario_id, start, today))
            despesas = cur.fetchone()
            cur.execute('SELECT COALESCE(SUM(a.valor),0) total FROM aporte_objetivo a JOIN objetivo_financeiro o ON o.id=a.objetivo_id WHERE o.usuario_id=%s AND a.data_aporte >= %s AND a.data_aporte <= %s', (self.usuario_id, start, today))
            aportes = cur.fetchone()['total']
            cur.execute('SELECT c.nome, COALESCE(SUM(d.valor),0) total FROM categoria_despesa c LEFT JOIN despesa d ON d.categoria_id=c.id AND d.data_despesa BETWEEN %s AND %s WHERE c.usuario_id=%s GROUP BY c.id,c.nome ORDER BY total DESC', (start,today,self.usuario_id))
            categorias = cur.fetchall()
            cur.execute('SELECT descricao,valor,data_despesa FROM despesa WHERE usuario_id=%s ORDER BY data_despesa DESC,id DESC LIMIT 6', (self.usuario_id,))
            ultimas = cur.fetchall()
        return {'receita': receita.quantize(Decimal('0.01')), 'despesas': despesas['total'], 'quantidade_despesas': despesas['quantidade'], 'aportes': aportes, 'saldo': receita - despesas['total'] - aportes, 'categorias': categorias, 'ultimas': ultimas, 'fontes': len(incomes)}

    def metas(self):
        with sessao() as cur:
            cur.execute('''SELECT o.*, COALESCE(SUM(a.valor), 0) AS acumulado FROM objetivo_financeiro o LEFT JOIN aporte_objetivo a ON a.objetivo_id=o.id WHERE o.usuario_id=%s GROUP BY o.id ORDER BY o.id DESC''', (self.usuario_id,))
            return cur.fetchall()

    def sugestoes(self):
        saldo = max(Decimal('0'), self.resumo()['saldo'])
        with sessao() as cur:
            cur.execute('''SELECT r.id, r.objetivo_id, o.descricao, r.porcentagem FROM regra_distribuicao r JOIN objetivo_financeiro o ON o.id=r.objetivo_id WHERE o.usuario_id=%s ORDER BY o.descricao''', (self.usuario_id,))
            return [dict(r, sugerido=(saldo*r['porcentagem']/100).quantize(Decimal('0.01'))) for r in cur.fetchall()]
