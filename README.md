# MeuBolso — Projeto Integrador Arthur

Interface Python/Tkinter, controllers com PostgreSQL e dados persistidos.

## Iniciar no Windows

1. Crie um ambiente virtual: `py -m venv .venv`
2. Ative: `.venv\Scripts\activate`
3. Instale: `python -m pip install -r requirements.txt`
4. Crie um banco chamado `projetoi` (ou use o banco já criado).
5. Se as tabelas ainda não existirem, execute `schema.sql` no DBeaver ou `psql -U postgres -d projetoi -f schema.sql`. **Não rode o schema original novamente num banco com tabelas já existentes**, pois usa `CREATE TABLE` sem `IF NOT EXISTS`.
6. Configure credenciais no terminal antes de executar, por exemplo em PowerShell:

```powershell
$env:DB_HOST="localhost"
$env:DB_PORT="5432"
$env:DB_NAME="projetoi"
$env:DB_USER="postgres"
$env:DB_PASSWORD="SUA_SENHA"
python main.py
```

Em primeiro acesso, o programa permite cadastrar um usuário na tabela `usuario`; com mais de um usuário, solicita seu ID. **Isso não constitui autenticação**: este projeto é uma aplicação didática local. Não utilize com informações financeiras sensíveis de usuários sem implementar autenticação e autorização no servidor/banco.

## Fluxos disponíveis

- Rendas: cadastro, consulta, alteração e exclusão de fontes de renda diárias, semanais e mensais, com indicador `ativa`.
- Categorias: CRUD, nomes únicos por usuário.
- Despesas: CRUD, categoria obrigatória do mesmo usuário, classificação fixa/variável, data e status de pagamento.
- Objetivos: CRUD de metas e prazos; progresso calculado pelos aportes efetivos.
- Regras: CRUD de porcentagens por meta, com soma máxima de 100% por usuário. Mostra sugestão de distribuição do saldo positivo; **não efetua aporte automaticamente**.
- Aportes: CRUD de valores efetivamente destinados a uma meta.
- Dashboard: saldo projetado, previsão mensal de renda, despesas registradas do mês até o dia atual, aportes do mês até hoje, valores por categoria e progresso das metas.

## Regras de cálculo

- `renda` contém **fontes recorrentes**; não existe tabela de recebimentos individuais. As projeções usam DIARIA × 30, SEMANAL × 52/12 e MENSAL × 1.
- `despesa` armazena lançamentos datados, pagos ou pendentes. O dashboard inclui ambos, porque representam despesas registradas; não é uma visão de caixa efetivo.
- `saldo projetado = rendas mensais estimadas − despesas registradas no mês até hoje − aportes realizados no mês até hoje`.
- Saldo não é saldo bancário acumulado. A tabela `renda` não armazena data de recebimento e o esquema não guarda saldos iniciais.
- O percentual sugerido em regras usa apenas `max(saldo projetado, 0)`; aportes são operações explícitas e não automáticas.

## Observações

- Alterações são transacionais; relações e valores são validados no controller e nos constraints do banco.
- Tabelas relacionadas não podem ser removidas quando possuem dependências; o erro é exibido na interface.
- Senha nunca é codificada no arquivo de conexão; variáveis de ambiente DB_* são usadas.
- Se o banco estiver indisponível, o programa apresenta um erro e fecha sem exibir números fictícios.
- A GUI deve ser validada no Windows com PostgreSQL disponível; sem um servidor PostgreSQL neste ambiente, testes de integração de banco não foram executados.
