# py
É um arquivo de orientação pro projeto orientador do senac

meu projeto é uma controle financeiro.Cujo a ideia segue as ideias a seguir:  

Objetivo:
Fazer uma carteira digital ou apenas um programa. Que pegue ou você forneça, o quanto você ganha em certo espaço de tempo da sua preferência (Diariamente, Semanalmente, Mensalmente) e despesas mensais pra poder dividir e organizar seu dinheiro de acordo com as seus objetivos e perído pra alcança-los  (investimento, viagem, presentear alguém e etc)
Banco de dados: 
porcentagem fixa da divisão de acordo com a quantidade de dinheiro que sobra e tipos diferentes de despesas. Pode envolver uma função pra calcular 
Quanto que ele ganha 
Sua despesa mensal 
divisão das despesas 
Público-alvo:
pessoas que começaram a ter um contato mais recente com dinheiro (jovens )
pessoas com a rotina corrida por causa de conciliação do trabalho com outros ambientes


![Minha Imagem](diagramabd.png)

| Entidade A | Cardinalidade | Entidade B | Explicação |
|---|:---:|---|---|
| Usuário | 1:N | Renda | Um usuário pode ter várias fontes de renda. |
| Usuário | 1:N | Categoria de despesa | Um usuário pode criar várias categorias. |
| Categoria de despesa | 1:N | Despesa | Uma categoria pode classificar várias despesas. |
| Usuário | 1:N | Despesa | Um usuário pode registrar várias despesas. |
| Usuário | 1:N | Objetivo financeiro | Um usuário pode criar vários objetivos. |
| Objetivo financeiro | 1:0..1 | Regra de distribuição | Um objetivo pode ter uma regra percentual ou nenhuma. |
| Objetivo financeiro | 1:N | Aporte | Um objetivo pode receber vários aportes. |