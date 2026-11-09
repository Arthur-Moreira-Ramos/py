    
-- ============================================
-- PROJETO INTEGRADOR - MEUBOLSO
-- GERENCIAMENTO FINANCEIRO PESSOAL
-- SGBD: PostgreSQL
-- ============================================


-- 1. TABELA USUARIO
CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    data_cadastro DATE NOT NULL DEFAULT CURRENT_DATE
);


-- 2. TABELA RENDA
CREATE TABLE renda (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    descricao VARCHAR(150) NOT NULL,
    valor NUMERIC(12,2) NOT NULL,
    periodicidade VARCHAR(20) NOT NULL,
    ativa BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT fk_renda_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuario(id),

    CONSTRAINT chk_renda_valor
        CHECK (valor > 0),

    CONSTRAINT chk_periodicidade
        CHECK (periodicidade IN (
            'DIARIA',
            'SEMANAL',
            'MENSAL'
        ))
);


-- 3. TABELA CATEGORIA_DESPESA
CREATE TABLE categoria_despesa (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(200),

    CONSTRAINT fk_categoria_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuario(id),

    CONSTRAINT uq_categoria_usuario
        UNIQUE (usuario_id, nome),

    CONSTRAINT uq_categoria_id_usuario
        UNIQUE (id, usuario_id)
);


-- 4. TABELA DESPESA
CREATE TABLE despesa (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    categoria_id INTEGER NOT NULL,
    descricao VARCHAR(150) NOT NULL,
    valor NUMERIC(12,2) NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    data_despesa DATE NOT NULL,
    pago BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT fk_despesa_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuario(id),

    CONSTRAINT fk_despesa_categoria
        FOREIGN KEY (categoria_id, usuario_id)
        REFERENCES categoria_despesa(id, usuario_id),

    CONSTRAINT chk_despesa_valor
        CHECK (valor > 0),

    CONSTRAINT chk_despesa_tipo
        CHECK (tipo IN (
            'FIXA',
            'VARIAVEL'
        ))
);


-- 5. TABELA OBJETIVO_FINANCEIRO
CREATE TABLE objetivo_financeiro (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    descricao VARCHAR(150) NOT NULL,
    valor_meta NUMERIC(12,2) NOT NULL,
    data_inicio DATE NOT NULL DEFAULT CURRENT_DATE,
    data_limite DATE NOT NULL,

    CONSTRAINT fk_objetivo_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuario(id),

    CONSTRAINT chk_objetivo_valor
        CHECK (valor_meta > 0),

    CONSTRAINT chk_objetivo_datas
        CHECK (data_limite >= data_inicio)
);


-- 6. TABELA REGRA_DISTRIBUICAO
CREATE TABLE regra_distribuicao (
    id SERIAL PRIMARY KEY,
    objetivo_id INTEGER NOT NULL UNIQUE,
    porcentagem NUMERIC(5,2) NOT NULL,

    CONSTRAINT fk_regra_objetivo
        FOREIGN KEY (objetivo_id)
        REFERENCES objetivo_financeiro(id),

    CONSTRAINT chk_porcentagem
        CHECK (
            porcentagem > 0
            AND porcentagem <= 100
        )
);


-- 7. TABELA APORTE_OBJETIVO
CREATE TABLE aporte_objetivo (
    id SERIAL PRIMARY KEY,
    objetivo_id INTEGER NOT NULL,
    valor NUMERIC(12,2) NOT NULL,
    data_aporte DATE NOT NULL DEFAULT CURRENT_DATE,

    CONSTRAINT fk_aporte_objetivo
        FOREIGN KEY (objetivo_id)
        REFERENCES objetivo_financeiro(id),

    CONSTRAINT chk_aporte_valor
        CHECK (valor > 0)
);
 