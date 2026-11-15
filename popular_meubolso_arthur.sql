-- ================================================================
-- MEUBOLSO | DADOS DE DEMONSTRACAO | PostgreSQL
-- Compativel com schema.sql do projeto do Arthur (7 tabelas).
-- Execute DEPOIS de criar as tabelas no banco "projetoi".
-- Nao apaga, nao altera registros existentes e nao duplica os exemplos
-- nas execucoes seguintes (mesmo usuario + descricao/data/valor).
-- Datas relativas ao mes atual: dashboard funciona em qualquer mes.
-- ================================================================
BEGIN;

DO $seed$
DECLARE
    v_ana INTEGER;
    v_bruno INTEGER;
    v_usuario INTEGER;
    v_cat_moradia INTEGER;
    v_cat_alimentacao INTEGER;
    v_cat_transporte INTEGER;
    v_cat_lazer INTEGER;
    v_cat_saude INTEGER;
    v_cat_educacao INTEGER;
    v_meta_emergencia INTEGER;
    v_meta_viagem INTEGER;
    v_meta_notebook INTEGER;
    v_meta_bruno INTEGER;
    v_inicio_mes DATE := date_trunc('month', CURRENT_DATE)::date;
    v_mes DATE;
    v_data DATE;
    v_i INTEGER;
BEGIN
    -- 1. USUARIOS (email e unico no esquema)
    INSERT INTO usuario (nome, email)
    VALUES ('Ana Souza', 'ana.souza.demo@exemplo.com')
    ON CONFLICT (email) DO NOTHING;
    INSERT INTO usuario (nome, email)
    VALUES ('Bruno Lima', 'bruno.lima.demo@exemplo.com')
    ON CONFLICT (email) DO NOTHING;

    SELECT id INTO STRICT v_ana FROM usuario WHERE email = 'ana.souza.demo@exemplo.com';
    SELECT id INTO STRICT v_bruno FROM usuario WHERE email = 'bruno.lima.demo@exemplo.com';

    -- 2. CATEGORIAS (unicas por usuario + nome)
    FOREACH v_usuario IN ARRAY ARRAY[v_ana, v_bruno] LOOP
        INSERT INTO categoria_despesa (usuario_id, nome, descricao) VALUES
            (v_usuario, 'Moradia', 'Aluguel, energia e manutencao da casa'),
            (v_usuario, 'Alimentação', 'Mercado e refeicoes'),
            (v_usuario, 'Transporte', 'Onibus, combustivel e aplicativos'),
            (v_usuario, 'Lazer', 'Passeios e entretenimento'),
            (v_usuario, 'Saúde', 'Farmacia e consultas'),
            (v_usuario, 'Educação', 'Cursos, livros e materiais')
        ON CONFLICT (usuario_id, nome) DO NOTHING;
    END LOOP;

    SELECT id INTO STRICT v_cat_moradia FROM categoria_despesa WHERE usuario_id=v_ana AND nome='Moradia';
    SELECT id INTO STRICT v_cat_alimentacao FROM categoria_despesa WHERE usuario_id=v_ana AND nome='Alimentação';
    SELECT id INTO STRICT v_cat_transporte FROM categoria_despesa WHERE usuario_id=v_ana AND nome='Transporte';
    SELECT id INTO STRICT v_cat_lazer FROM categoria_despesa WHERE usuario_id=v_ana AND nome='Lazer';
    SELECT id INTO STRICT v_cat_saude FROM categoria_despesa WHERE usuario_id=v_ana AND nome='Saúde';
    SELECT id INTO STRICT v_cat_educacao FROM categoria_despesa WHERE usuario_id=v_ana AND nome='Educação';

    -- 3. FONTES DE RENDA (cadastradas como renda recorrente,
    --    NAO como recebimentos de uma data especifica)
    INSERT INTO renda (usuario_id, descricao, valor, periodicidade, ativa)
    SELECT v_ana, s.descricao, s.valor, s.periodicidade, s.ativa
    FROM (VALUES
        ('Salário mensal', 4200.00::numeric, 'MENSAL', TRUE),
        ('Freelance semanal', 250.00::numeric, 'SEMANAL', TRUE),
        ('Serviço eventual diário', 90.00::numeric, 'DIARIA', FALSE)
    ) AS s(descricao, valor, periodicidade, ativa)
    WHERE NOT EXISTS (
        SELECT 1 FROM renda r
        WHERE r.usuario_id=v_ana AND r.descricao=s.descricao AND r.periodicidade=s.periodicidade
    );

    INSERT INTO renda (usuario_id, descricao, valor, periodicidade, ativa)
    SELECT v_bruno, s.descricao, s.valor, s.periodicidade, TRUE
    FROM (VALUES
        ('Salário mensal', 3500.00::numeric, 'MENSAL'),
        ('Aulas particulares', 150.00::numeric, 'SEMANAL')
    ) AS s(descricao, valor, periodicidade)
    WHERE NOT EXISTS (
        SELECT 1 FROM renda r
        WHERE r.usuario_id=v_bruno AND r.descricao=s.descricao AND r.periodicidade=s.periodicidade
    );

    -- 4. DESPESAS DOS ULTIMOS 6 MESES PARA ANA
    -- Datas sempre no passado ou hoje. Os primeiros 5 meses usam
    -- dias fixos, e o mes corrente usa LEAST(dia, CURRENT_DATE).
    FOR v_i IN 0..5 LOOP
        v_mes := (v_inicio_mes - make_interval(months => v_i))::date;

        v_data := LEAST(v_mes + 2, CURRENT_DATE);
        INSERT INTO despesa (usuario_id,categoria_id,descricao,valor,tipo,data_despesa,pago)
        SELECT v_ana,v_cat_moradia,'Aluguel',1200.00,'FIXA',v_data,TRUE
        WHERE NOT EXISTS (SELECT 1 FROM despesa WHERE usuario_id=v_ana AND descricao='Aluguel' AND data_despesa=v_data);

        v_data := LEAST(v_mes + 4, CURRENT_DATE);
        INSERT INTO despesa (usuario_id,categoria_id,descricao,valor,tipo,data_despesa,pago)
        SELECT v_ana,v_cat_alimentacao,'Supermercado',350.00 + v_i*8,'VARIAVEL',v_data,TRUE
        WHERE NOT EXISTS (SELECT 1 FROM despesa WHERE usuario_id=v_ana AND descricao='Supermercado' AND data_despesa=v_data);

        v_data := LEAST(v_mes + 6, CURRENT_DATE);
        INSERT INTO despesa (usuario_id,categoria_id,descricao,valor,tipo,data_despesa,pago)
        SELECT v_ana,v_cat_transporte,'Transporte',150.00 + v_i*5,'VARIAVEL',v_data,TRUE
        WHERE NOT EXISTS (SELECT 1 FROM despesa WHERE usuario_id=v_ana AND descricao='Transporte' AND data_despesa=v_data);

        v_data := LEAST(v_mes + 8, CURRENT_DATE);
        INSERT INTO despesa (usuario_id,categoria_id,descricao,valor,tipo,data_despesa,pago)
        SELECT v_ana,v_cat_lazer,'Lazer do mês',125.00 + v_i*10,'VARIAVEL',v_data,TRUE
        WHERE NOT EXISTS (SELECT 1 FROM despesa WHERE usuario_id=v_ana AND descricao='Lazer do mês' AND data_despesa=v_data);
    END LOOP;

    -- Despesas adicionais apenas no mes atual (no maximo a data de hoje).
    v_data := LEAST(v_inicio_mes + 9, CURRENT_DATE);
    INSERT INTO despesa (usuario_id,categoria_id,descricao,valor,tipo,data_despesa,pago)
    SELECT v_ana,v_cat_saude,'Farmácia',68.90,'VARIAVEL',v_data,TRUE
    WHERE NOT EXISTS (SELECT 1 FROM despesa WHERE usuario_id=v_ana AND descricao='Farmácia' AND data_despesa=v_data);

    v_data := LEAST(v_inicio_mes + 10, CURRENT_DATE);
    INSERT INTO despesa (usuario_id,categoria_id,descricao,valor,tipo,data_despesa,pago)
    SELECT v_ana,v_cat_educacao,'Curso de Python',110.00,'FIXA',v_data,FALSE
    WHERE NOT EXISTS (SELECT 1 FROM despesa WHERE usuario_id=v_ana AND descricao='Curso de Python' AND data_despesa=v_data);

    -- Despesas para Bruno: o controller filtra por usuario.
    SELECT id INTO STRICT v_cat_moradia FROM categoria_despesa WHERE usuario_id=v_bruno AND nome='Moradia';
    SELECT id INTO STRICT v_cat_alimentacao FROM categoria_despesa WHERE usuario_id=v_bruno AND nome='Alimentação';
    SELECT id INTO STRICT v_cat_transporte FROM categoria_despesa WHERE usuario_id=v_bruno AND nome='Transporte';

    v_data := LEAST(v_inicio_mes + 2, CURRENT_DATE);
    INSERT INTO despesa (usuario_id,categoria_id,descricao,valor,tipo,data_despesa,pago)
    SELECT v_bruno,v_cat_moradia,'Aluguel',950.00,'FIXA',v_data,TRUE
    WHERE NOT EXISTS (SELECT 1 FROM despesa WHERE usuario_id=v_bruno AND descricao='Aluguel' AND data_despesa=v_data);

    v_data := LEAST(v_inicio_mes + 5, CURRENT_DATE);
    INSERT INTO despesa (usuario_id,categoria_id,descricao,valor,tipo,data_despesa,pago)
    SELECT v_bruno,v_cat_alimentacao,'Compras do mês',410.00,'VARIAVEL',v_data,TRUE
    WHERE NOT EXISTS (SELECT 1 FROM despesa WHERE usuario_id=v_bruno AND descricao='Compras do mês' AND data_despesa=v_data);

    v_data := LEAST(v_inicio_mes + 7, CURRENT_DATE);
    INSERT INTO despesa (usuario_id,categoria_id,descricao,valor,tipo,data_despesa,pago)
    SELECT v_bruno,v_cat_transporte,'Combustível',190.00,'VARIAVEL',v_data,FALSE
    WHERE NOT EXISTS (SELECT 1 FROM despesa WHERE usuario_id=v_bruno AND descricao='Combustível' AND data_despesa=v_data);

    -- 5. OBJETIVOS
    INSERT INTO objetivo_financeiro (usuario_id,descricao,valor_meta,data_inicio,data_limite)
    SELECT v_ana,s.descricao,s.valor_meta,v_inicio_mes,s.data_limite
    FROM (VALUES
        ('Reserva de emergência', 10000.00::numeric, (v_inicio_mes + INTERVAL '18 months')::date),
        ('Viagem de férias',       4500.00::numeric, (v_inicio_mes + INTERVAL '12 months')::date),
        ('Notebook novo',         6000.00::numeric, (v_inicio_mes + INTERVAL '14 months')::date)
    ) AS s(descricao,valor_meta,data_limite)
    WHERE NOT EXISTS (SELECT 1 FROM objetivo_financeiro o WHERE o.usuario_id=v_ana AND o.descricao=s.descricao);

    INSERT INTO objetivo_financeiro (usuario_id,descricao,valor_meta,data_inicio,data_limite)
    SELECT v_bruno,'Comprar bicicleta',2500.00,v_inicio_mes,(v_inicio_mes + INTERVAL '10 months')::date
    WHERE NOT EXISTS (SELECT 1 FROM objetivo_financeiro WHERE usuario_id=v_bruno AND descricao='Comprar bicicleta');

    SELECT id INTO STRICT v_meta_emergencia FROM objetivo_financeiro WHERE usuario_id=v_ana AND descricao='Reserva de emergência';
    SELECT id INTO STRICT v_meta_viagem FROM objetivo_financeiro WHERE usuario_id=v_ana AND descricao='Viagem de férias';
    SELECT id INTO STRICT v_meta_notebook FROM objetivo_financeiro WHERE usuario_id=v_ana AND descricao='Notebook novo';
    SELECT id INTO STRICT v_meta_bruno FROM objetivo_financeiro WHERE usuario_id=v_bruno AND descricao='Comprar bicicleta';

    -- 6. REGRAS DE DISTRIBUICAO: 50% + 30% + 20% = 100% (Ana)
    INSERT INTO regra_distribuicao (objetivo_id, porcentagem)
    VALUES (v_meta_emergencia,50.00),(v_meta_viagem,30.00),(v_meta_notebook,20.00)
    ON CONFLICT (objetivo_id) DO NOTHING;
    INSERT INTO regra_distribuicao (objetivo_id, porcentagem)
    VALUES (v_meta_bruno,40.00)
    ON CONFLICT (objetivo_id) DO NOTHING;

    -- 7. APORTES: alguns passados e outros no mes corrente.
    -- Nao inserir aportes futuros (resumo() conta ate CURRENT_DATE).
    FOR v_i IN 0..3 LOOP
        v_mes := (v_inicio_mes - make_interval(months => v_i))::date;
        v_data := LEAST(v_mes + 10, CURRENT_DATE);
        INSERT INTO aporte_objetivo (objetivo_id,valor,data_aporte)
        SELECT v_meta_emergencia,250.00,v_data
        WHERE NOT EXISTS (SELECT 1 FROM aporte_objetivo WHERE objetivo_id=v_meta_emergencia AND valor=250.00 AND data_aporte=v_data);
        INSERT INTO aporte_objetivo (objetivo_id,valor,data_aporte)
        SELECT v_meta_viagem,125.00,v_data
        WHERE NOT EXISTS (SELECT 1 FROM aporte_objetivo WHERE objetivo_id=v_meta_viagem AND valor=125.00 AND data_aporte=v_data);
    END LOOP;

    v_data := LEAST(v_inicio_mes + 11, CURRENT_DATE);
    INSERT INTO aporte_objetivo (objetivo_id,valor,data_aporte)
    SELECT v_meta_notebook,200.00,v_data
    WHERE NOT EXISTS (SELECT 1 FROM aporte_objetivo WHERE objetivo_id=v_meta_notebook AND valor=200.00 AND data_aporte=v_data);

    v_data := LEAST(v_inicio_mes + 8, CURRENT_DATE);
    INSERT INTO aporte_objetivo (objetivo_id,valor,data_aporte)
    SELECT v_meta_bruno,120.00,v_data
    WHERE NOT EXISTS (SELECT 1 FROM aporte_objetivo WHERE objetivo_id=v_meta_bruno AND valor=120.00 AND data_aporte=v_data);

END $seed$;

COMMIT;

-- 8. CONFERENCIA: totais por usuario / tabela
SELECT u.nome, u.email,
 (SELECT COUNT(*) FROM renda r WHERE r.usuario_id=u.id) AS rendas,
 (SELECT COUNT(*) FROM categoria_despesa c WHERE c.usuario_id=u.id) AS categorias,
 (SELECT COUNT(*) FROM despesa d WHERE d.usuario_id=u.id) AS despesas,
 (SELECT COUNT(*) FROM objetivo_financeiro o WHERE o.usuario_id=u.id) AS objetivos,
 (SELECT COUNT(*) FROM regra_distribuicao r JOIN objetivo_financeiro o ON o.id=r.objetivo_id WHERE o.usuario_id=u.id) AS regras,
 (SELECT COUNT(*) FROM aporte_objetivo a JOIN objetivo_financeiro o ON o.id=a.objetivo_id WHERE o.usuario_id=u.id) AS aportes
FROM usuario u
WHERE u.email IN ('ana.souza.demo@exemplo.com', 'bruno.lima.demo@exemplo.com')
ORDER BY u.nome;
