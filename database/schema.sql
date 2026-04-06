-- Modelo inicial de banco de dados para o projeto Web Control.
-- O Django criara tabelas internas de autenticacao. Aqui ficam as tabelas do dominio.

CREATE TABLE fornecedores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_fantasia VARCHAR(120) NOT NULL,
    razao_social VARCHAR(160),
    cnpj VARCHAR(18) NOT NULL UNIQUE,
    telefone VARCHAR(20),
    email VARCHAR(120),
    cidade VARCHAR(100),
    uf CHAR(2),
    ativo BOOLEAN NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(120) NOT NULL,
    unidade_medida VARCHAR(10) NOT NULL,
    preco_custo DECIMAL(10, 2) NOT NULL DEFAULT 0,
    preco_venda DECIMAL(10, 2) NOT NULL DEFAULT 0,
    estoque_atual DECIMAL(10, 2) NOT NULL DEFAULT 0,
    estoque_minimo DECIMAL(10, 2) NOT NULL DEFAULT 0,
    ativo BOOLEAN NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE notas_fiscais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero VARCHAR(30) NOT NULL,
    serie VARCHAR(10),
    fornecedor_id INTEGER NOT NULL,
    data_emissao DATE NOT NULL,
    data_vencimento DATE NOT NULL,
    valor_total DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('pendente', 'paga', 'vencida', 'cancelada')),
    observacoes TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_notas_fornecedor
        FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id),
    CONSTRAINT uq_nota
        UNIQUE (numero, serie, fornecedor_id)
);

CREATE TABLE itens_nota_fiscal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nota_fiscal_id INTEGER NOT NULL,
    produto_id INTEGER,
    descricao VARCHAR(160) NOT NULL,
    quantidade DECIMAL(10, 2) NOT NULL,
    valor_unitario DECIMAL(10, 2) NOT NULL,
    valor_total DECIMAL(10, 2) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_item_nota
        FOREIGN KEY (nota_fiscal_id) REFERENCES notas_fiscais(id),
    CONSTRAINT fk_item_produto
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
);

CREATE TABLE pagamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nota_fiscal_id INTEGER NOT NULL,
    data_pagamento DATE NOT NULL,
    valor_pago DECIMAL(10, 2) NOT NULL,
    forma_pagamento VARCHAR(30) NOT NULL,
    observacoes TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_pagamento_nota
        FOREIGN KEY (nota_fiscal_id) REFERENCES notas_fiscais(id)
);

CREATE TABLE movimentacoes_estoque (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER NOT NULL,
    item_nota_id INTEGER,
    tipo VARCHAR(10) NOT NULL CHECK (tipo IN ('entrada', 'saida', 'ajuste')),
    quantidade DECIMAL(10, 2) NOT NULL,
    data_movimentacao DATE NOT NULL,
    observacoes TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_movimentacao_produto
        FOREIGN KEY (produto_id) REFERENCES produtos(id),
    CONSTRAINT fk_movimentacao_item
        FOREIGN KEY (item_nota_id) REFERENCES itens_nota_fiscal(id)
);

CREATE INDEX idx_notas_status ON notas_fiscais(status);
CREATE INDEX idx_notas_vencimento ON notas_fiscais(data_vencimento);
CREATE INDEX idx_pagamentos_nota ON pagamentos(nota_fiscal_id);
CREATE INDEX idx_itens_nota ON itens_nota_fiscal(nota_fiscal_id);

