# Banco de Dados — Web Control

## Tecnologia

O sistema utiliza **SQLite 3** como banco de dados relacional, gerenciado pelo **Django ORM** via migrations. A escolha do SQLite é justificada pelo perfil do projeto:

- Instalação zero — não requer servidor de banco de dados separado
- Adequado para o volume de dados de uma pequena empresa
- Persistência garantida via volume Docker nomeado (`db_data`)
- Fácil portabilidade (banco é um único arquivo `db.sqlite3`)

Em caso de necessidade de escala, a troca para PostgreSQL ou MySQL exige apenas alterar a variável `DATABASES` em `settings.py` sem modificar o código da aplicação — o ORM abstrai o banco.

---

## Diagrama Entidade-Relacionamento

```
┌─────────────────────────┐
│       Fornecedor        │
├─────────────────────────┤
│ PK id                   │
│    nome_fantasia         │
│    razao_social          │
│    cnpj (único)          │
│    telefone              │
│    email                 │
│    cep                   │
│    logradouro            │
│    numero                │
│    bairro                │
│    cidade                │
│    uf                    │
│    ativo                 │
│    criado_em             │
│    atualizado_em         │
└────────────┬────────────┘
             │ 1
             │ PROTECT
             │ N
┌────────────▼────────────┐         ┌─────────────────────────┐
│       NotaFiscal        │         │        Produto          │
├─────────────────────────┤         ├─────────────────────────┤
│ PK id                   │         │ PK id                   │
│ FK fornecedor_id        │         │    nome                 │
│    numero               │         │    unidade_medida       │
│    serie                │         │    preco_custo          │
│    data_emissao         │         │    preco_venda          │
│    data_vencimento      │         │    estoque_atual        │
│    valor_total          │         │    estoque_minimo       │
│    status               │         │    ncm                  │
│    observacoes          │         │    cest                 │
│ UNIQUE(numero,serie,    │         │    origem               │
│        fornecedor_id)   │         │    aliquota_icms        │
│    criado_em            │         │    aliquota_ipi         │
│    atualizado_em        │         │    aliquota_pis         │
└──────┬──────────────────┘         │    aliquota_cofins      │
       │ 1              │ 1         │    ativo                │
       │                │           │    criado_em            │
  CASCADE           CASCADE         │    atualizado_em        │
       │                │           └──────────┬──────────────┘
       │ N              │ N                     │ 1
┌──────▼──────┐   ┌─────▼────────┐        PROTECT
│  Pagamento  │   │ItemNotaFiscal│             │ N
├─────────────┤   ├──────────────┤    ┌────────▼──────────────┐
│ PK id       │   │ PK id        │    │   (ItemNotaFiscal)     │
│ FK nota_id  │   │ FK nota_id   │◄───┘ FK produto_id (null)  │
│ data_pag.   │   │ FK produto_id│    └───────────────────────┘
│ valor_pago  │   │ descricao    │
│ forma_pag.  │   │ quantidade   │
│ observacoes │   │ valor_unit.  │
│ criado_em   │   │ valor_total  │
└─────────────┘   └──────────────┘
```

---

## Tabelas

### `fornecedores_fornecedor`
Armazena os fornecedores cadastrados. O campo `cnpj` possui restrição `UNIQUE`. Fornecedores inativos (`ativo = False`) não aparecem nos formulários de notas.

### `produtos_produto`
Catálogo de produtos com dados comerciais (preço de custo, preço de venda, estoque) e dados fiscais obrigatórios para emissão de notas (NCM, CEST, origem, alíquotas tributárias).

### `notas_notafiscal`
Cabeçalho da nota fiscal. A combinação `(numero, serie, fornecedor_id)` é única no banco. O campo `status` pode ser: `pendente`, `paga`, `vencida` ou `cancelada` — atualizado automaticamente pelo sistema.

### `notas_itemnotafiscal`
Itens vinculados a uma nota. O `valor_total` de cada item é calculado automaticamente (`quantidade × valor_unitario`) antes da persistência. A relação com `Produto` é opcional (nullable).

### `financeiro_pagamento`
Registros de pagamento por nota fiscal. Permite pagamentos parciais. O sistema valida que a soma dos pagamentos não excede o `valor_total` da nota.

---

## Índices

| Índice | Tabela | Coluna(s) | Motivo |
|--------|--------|-----------|--------|
| `idx_nota_fornecedor` | `notas_notafiscal` | `fornecedor_id` | Filtro/join frequente |
| `idx_nota_status` | `notas_notafiscal` | `status` | Filtro por status no dashboard |
| `idx_nota_vencimento` | `notas_notafiscal` | `data_vencimento` | Cálculo de vencimentos e alertas |
| `idx_item_nota` | `notas_itemnotafiscal` | `nota_fiscal_id` | Join ao carregar itens da nota |
| `idx_item_produto` | `notas_itemnotafiscal` | `produto_id` | Consulta de itens por produto |
| `idx_pgto_nota` | `financeiro_pagamento` | `nota_fiscal_id` | Cálculo do saldo devedor |
| `idx_pgto_data` | `financeiro_pagamento` | `data_pagamento` | Relatório de pagamentos por período |

---

## Integridade Referencial

| Relação | Comportamento ao excluir |
|---------|--------------------------|
| Fornecedor → NotaFiscal | **PROTECT** — bloqueia exclusão se houver notas vinculadas |
| NotaFiscal → ItemNotaFiscal | **CASCADE** — exclui os itens junto com a nota |
| NotaFiscal → Pagamento | **CASCADE** — exclui os pagamentos junto com a nota |
| Produto → ItemNotaFiscal | **PROTECT** — bloqueia exclusão se o produto constar em notas |

---

## Regras de Negócio no Banco

1. **Unicidade de nota**: `UNIQUE(numero, serie, fornecedor_id)` — evita duplicidade
2. **Valor calculado**: `ItemNotaFiscal.valor_total = quantidade × valor_unitario` (calculado no Django antes de salvar)
3. **Saldo devedor**: calculado em tempo real como `NotaFiscal.valor_total − SUM(pagamentos.valor_pago)`
4. **Atualização de status**: executada automaticamente após cada pagamento salvo
5. **Limite de pagamento**: validado no Django — `valor_pago ≤ saldo_devedor`

---

## Migrations

O Django gerencia as migrations em `apps/<modulo>/migrations/`. Para verificar o estado atual:

```bash
python manage.py showmigrations
```

Para aplicar:

```bash
python manage.py migrate
```

Para gerar novas migrations após alterar um model:

```bash
python manage.py makemigrations
```

---

## Backup e Restore

```bash
# Backup
docker compose cp web:/app/database/db.sqlite3 ./backup.sqlite3

# Restore
docker compose cp ./backup.sqlite3 web:/app/database/db.sqlite3
docker compose restart web
```

O arquivo `db.sqlite3` **não é versionado** (está no `.gitignore`). Somente o esquema (`schema.sql`) e esta documentação são commitados.
