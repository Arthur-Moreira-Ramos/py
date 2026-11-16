from conexao import conectar  # Ajuste conforme o nome da função em conexao.py

class BaseController:
    def executar_comando(self, query, params=None, fetch=False, fetch_one=False):
        conn = conectar()
        if not conn:
            raise ConnectionError("Não foi possível conectar ao banco PostgreSQL.")
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())
                
                if fetch_one:
                    resultado = cursor.fetchone()
                    conn.commit()
                    return resultado
                
                if fetch:
                    resultado = cursor.fetchall()
                    conn.commit()
                    return resultado
                
                conn.commit()
                return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()