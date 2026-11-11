
from conexao import conectar
from faker import Faker

fake = Faker("pt_BR")

try:
    conexao = conectar()
    cursor = conexao.cursor()

    print("Conexão bem-sucedida!")

    for i in range(10):
        nome = fake.name()
        email=fake.email()

        sql = """
            INSERT INTO usuario
            (nome, email)
            VALUES (%s, %s)
        """

        cursor.execute(
            sql,
            ( nome,email )
        )

    conexao.commit()
    print("10 usuários cadastrados com sucesso!")

except Exception as erro:
    if 'conexao' in locals() and not conexao.closed:
        conexao.rollback()
    print("Erro:", erro)

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conexao' in locals() and not conexao.closed:
        conexao.close()


