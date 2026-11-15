import unittest
from datetime import date
from decimal import Decimal
# Testes unitários executáveis mesmo sem driver/servidor PostgreSQL.
# A conexão real deverá ser verificada em uma máquina com o requirements instalado.
import sys
import types
try:
    import psycopg2
except ImportError:
    adapter = types.ModuleType('psycopg2')
    adapter.sql = types.SimpleNamespace()
    adapter.IntegrityError = type('IntegrityError', (Exception,), {})
    sys.modules['psycopg2'] = adapter
    extras = types.ModuleType('psycopg2.extras')
    extras.RealDictCursor = object
    sys.modules['psycopg2.extras'] = extras
from controllers.financeiro import moeda_decimal, data_valida, FinanceiroController


class TestValidacao(unittest.TestCase):
    def test_moeda_brasileira(self):
        self.assertEqual(moeda_decimal('R$ 1.234,56'), Decimal('1234.56'))

    def test_valor_decimal(self):
        self.assertEqual(moeda_decimal('200.30'), Decimal('200.30'))

    def test_nan_rejeitado(self):
        with self.assertRaises(ValueError):
            moeda_decimal('NaN')

    def test_data(self):
        self.assertEqual(data_valida('15/11/2026'), date(2026,11,15))

    def test_periodicidade_invalida(self):
        instance=FinanceiroController.__new__(FinanceiroController)
        with self.assertRaises(ValueError):
            instance._validar('renda', {'periodicidade':'VARIAVEL'})

    def test_tabela_invalida(self):
        instance=FinanceiroController.__new__(FinanceiroController)
        with self.assertRaises(ValueError):
            instance._validar('usuario', {'nome':'Teste'})

if __name__=='__main__':
    unittest.main()
