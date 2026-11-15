"""Conexão PostgreSQL via variáveis de ambiente (sem senhas no repositório)."""
import os
import psycopg2


def conectar():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', '5433')),
        dbname=os.getenv('DB_NAME', 'arthur'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', '1234'),
        connect_timeout=5,
    )
