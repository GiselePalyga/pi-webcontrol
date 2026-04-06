-- ============================================================
-- Web Control — Esquema do Banco de Dados
-- Banco: SQLite 3 (gerenciado pelo Django ORM)
-- ============================================================
-- Este arquivo documenta a estrutura das tabelas do sistema.
-- As tabelas são criadas automaticamente pelo Django via migrations.
-- Para recriar manualmente: python manage.py migrate
-- ============================================================


-- ── Fornecedores ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS fornecedores_fornecedor (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_fantasia   VARCHAR(200)  NOT NULL,
    razao_social    VARCHAR(200)  NOT NULL DEFAULT '',
    cnpj            VARCHAR(18)   NOT NULL UNIQUE,   -- formato: 00.000.000/0000-00
    telefone        VARCHAR(20)   NOT NULL DEFAULT '',
    email           VARCHAR(254)  NOT NULL DEFAULT '',
    -- Endereço
    cep             VARCHAR(9)    NOT NULL DEFAULT '',   -- formato: 00000-000
    logradouro      VARCHAR(200)  NOT NULL DEFAULT '',
    numero          VARCHAR(20)   NOT NULL DEFAULT '',
    bairro          VARCHAR(100)  NOT NULL DEFAULT '',
    cidade          VARCHAR(100)  NOT NULL DEFAULT '',
    uf              VARCHAR(2)    NOT NULL DEFAULT '',
    -- Controle
    ativo           BOOLEAN       NOT NULL DEFAULT 1,
    criado_em       DATETIME      NOT NULL,
    atualizado_em   DATETIME      NOT NULL
);


-- ── Produtos ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS produtos_produto (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    nome             VARCHAR(200)  NOT NULL,
    unidade_medida   VARCHAR(3)    NOT NULL DEFAULT 'UN',
    -- Preços e estoque
    preco_custo      DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    preco_venda      DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    estoque_atual    DECIMAL(10,3) NOT NULL DEFAULT 0.000,
    estoque_minimo   DECIMAL(10,3) NOT NULL DEFAULT 0.000,
    -- Dados fiscais
    ncm              VARCHAR(10)   NOT NULL DEFAULT '',  -- ex: 7307.19.00
    cest             VARCHAR(9)    NOT NULL DEFAULT '',  -- ex: 10.001.00
    origem           VARCHAR(1)    NOT NULL DEFAULT '0', -- 0 a 8 conforme tabela SEFAZ
    aliquota_icms    DECIMAL(5,2)  NOT NULL DEFAULT 0.00,
    aliquota_ipi     DECIMAL(5,2)  NOT NULL DEFAULT 0.00,
    aliquota_pis     DECIMAL(5,2)  NOT NULL DEFAULT 0.65,
    aliquota_cofins  DECIMAL(5,2)  NOT NULL DEFAULT 3.00,
    -- Controle
    ativo            BOOLEAN       NOT NULL DEFAULT 1,
    criado_em        DATETIME      NOT NULL,
    atualizado_em    DATETIME      NOT NULL
);


-- ── Notas Fiscais ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS notas_notafiscal (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    numero           VARCHAR(20)   NOT NULL,
    serie            VARCHAR(10)   NOT NULL DEFAULT '1',
    fornecedor_id    INTEGER       NOT NULL REFERENCES fornecedores_fornecedor(id),
    data_emissao     DATE          NOT NULL,
    data_vencimento  DATE          NOT NULL,
    valor_total      DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    status           VARCHAR(10)   NOT NULL DEFAULT 'pendente',
    -- status: 'pendente' | 'paga' | 'vencida' | 'cancelada'
    observacoes      TEXT          NOT NULL DEFAULT '',
    criado_em        DATETIME      NOT NULL,
    atualizado_em    DATETIME      NOT NULL,
    -- Restrição: número + série + fornecedor deve ser único
    UNIQUE (numero, serie, fornecedor_id)
);

CREATE INDEX IF NOT EXISTS idx_nota_fornecedor  ON notas_notafiscal(fornecedor_id);
CREATE INDEX IF NOT EXISTS idx_nota_status       ON notas_notafiscal(status);
CREATE INDEX IF NOT EXISTS idx_nota_vencimento   ON notas_notafiscal(data_vencimento);


-- ── Itens da Nota Fiscal ──────────────────────────────────────
CREATE TABLE IF NOT EXISTS notas_itemnotafiscal (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    nota_fiscal_id   INTEGER       NOT NULL REFERENCES notas_notafiscal(id) ON DELETE CASCADE,
    produto_id       INTEGER       REFERENCES produtos_produto(id),  -- nullable
    descricao        VARCHAR(300)  NOT NULL,
    quantidade       DECIMAL(10,3) NOT NULL,
    valor_unitario   DECIMAL(10,2) NOT NULL,
    valor_total      DECIMAL(12,2) NOT NULL   -- calculado: quantidade × valor_unitario
);

CREATE INDEX IF NOT EXISTS idx_item_nota     ON notas_itemnotafiscal(nota_fiscal_id);
CREATE INDEX IF NOT EXISTS idx_item_produto  ON notas_itemnotafiscal(produto_id);


-- ── Pagamentos ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS financeiro_pagamento (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    nota_fiscal_id   INTEGER       NOT NULL REFERENCES notas_notafiscal(id) ON DELETE CASCADE,
    data_pagamento   DATE          NOT NULL,
    valor_pago       DECIMAL(12,2) NOT NULL,
    forma_pagamento  VARCHAR(20)   NOT NULL DEFAULT 'pix',
    -- forma: 'dinheiro' | 'pix' | 'boleto' | 'transferencia' | 'cartao_debito' | 'cartao_credito' | 'cheque'
    observacoes      TEXT          NOT NULL DEFAULT '',
    criado_em        DATETIME      NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_pgto_nota  ON financeiro_pagamento(nota_fiscal_id);
CREATE INDEX IF NOT EXISTS idx_pgto_data  ON financeiro_pagamento(data_pagamento);


-- ============================================================
-- Resumo dos relacionamentos
-- ============================================================
--
--  Fornecedor (1) ──────────── (N) NotaFiscal
--  NotaFiscal (1) ──────────── (N) ItemNotaFiscal
--  NotaFiscal (1) ──────────── (N) Pagamento
--  Produto    (1) ──────────── (N) ItemNotaFiscal  [opcional]
--
-- ============================================================
-- Regras de negócio aplicadas no banco
-- ============================================================
--
--  • UNIQUE (numero, serie, fornecedor_id) em NotaFiscal
--    evita duplicidade de notas do mesmo fornecedor.
--
--  • ON DELETE CASCADE em ItemNotaFiscal e Pagamento
--    garante integridade referencial: excluir uma nota
--    remove automaticamente seus itens e pagamentos.
--
--  • ON DELETE PROTECT (via Django) em NotaFiscal → Fornecedor
--    impede excluir um fornecedor que possui notas vinculadas.
--
--  • ON DELETE PROTECT (via Django) em ItemNotaFiscal → Produto
--    impede excluir um produto que aparece em alguma nota.
--
--  • valor_total em ItemNotaFiscal é calculado automaticamente
--    pelo Django (quantidade × valor_unitario) antes de salvar.
--
--  • status em NotaFiscal é recalculado automaticamente após
--    cada pagamento registrado ou atualizado.
--
-- ============================================================
