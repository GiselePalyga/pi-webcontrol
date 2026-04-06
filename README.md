# Web Control — Sistema de Gestão Fiscal

Sistema web para organização de notas fiscais, controle de pagamentos e acompanhamento financeiro desenvolvido como Projeto Integrador (PI) da UNIVESP.

---

## Visão Geral

O **Web Control** é um MVP voltado para pequenas empresas que ainda controlam documentos fiscais de forma manual. O sistema permite:

- Cadastrar fornecedores e produtos
- Registrar notas fiscais de entrada com seus itens
- Controlar pagamentos (totais ou parciais)
- Visualizar indicadores financeiros no dashboard
- Identificar notas pendentes, pagas e vencidas

---

## Stack

| Camada       | Tecnologia           |
|--------------|----------------------|
| Backend      | Django 5             |
| Banco        | SQLite (via Django ORM) |
| Templates    | Django Templates     |
| CSS/UI       | Bootstrap 5.3 + CSS customizado |
| Ícones       | Bootstrap Icons      |
| Servidor     | Gunicorn             |
| Estáticos    | WhiteNoise           |
| Container    | Docker + Docker Compose |

---

## Funcionalidades

### Dashboard
- Total a pagar (notas pendentes)
- Total vencido em aberto
- Total pago no mês corrente
- Próximos vencimentos em destaque
- Últimas notas cadastradas

### Fornecedores
- Cadastro completo (nome fantasia, razão social, CNPJ, endereço, contato)
- Validação de CNPJ com dígitos verificadores
- Ativação e inativação
- Busca por nome, razão social e CNPJ

### Produtos
- Cadastro com unidade de medida, preço de custo, preço de venda e estoque
- Alerta visual quando estoque está abaixo do mínimo
- Ativação e inativação

### Notas Fiscais
- Cabeçalho da nota (número, série, fornecedor, datas, valor, status)
- Itens vinculados com cálculo automático de total
- Filtros por número, fornecedor, status e período
- Destaque visual por status: **Pendente**, **Paga**, **Vencida**, **Cancelada**
- Validação: data de vencimento não pode ser anterior à emissão
- Unicidade: número + série + fornecedor

### Pagamentos
- Registro por nota fiscal (total ou parcial)
- Formas de pagamento: Dinheiro, PIX, Boleto, Transferência, Cartão
- Validação: pagamento não pode exceder o saldo devedor
- Atualização automática do status da nota ao quitar

---

## Requisitos

- [Docker](https://docs.docker.com/get-docker/) 20.10+
- [Docker Compose](https://docs.docker.com/compose/) v2+

---

## Subindo com Docker

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd pi-univesp
```

### 2. Configure o arquivo `.env`

```bash
cp .env.example .env
```

Edite o `.env` conforme necessário:

```env
SECRET_KEY=troque-para-uma-chave-secreta-forte
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@webcontrol.local
DJANGO_SUPERUSER_PASSWORD=webcontrol@2025
```

> **Importante:** Em produção, use uma `SECRET_KEY` longa e aleatória. Nunca use `DEBUG=True` em produção.

### 3. Suba o container

```bash
docker compose up -d
```

O comando irá:
1. Construir a imagem Docker
2. Aplicar as migrações do banco de dados automaticamente
3. Criar o superusuário definido no `.env`
4. Iniciar o servidor Gunicorn na porta `8000`

### 4. Acesse o sistema

| URL | Descrição |
|-----|-----------|
| `http://localhost:8000` | Sistema (redireciona para login) |
| `http://localhost:8000/admin/` | Painel administrativo Django |

**Credenciais padrão** (definidas no `.env`):
- Usuário: `admin`
- Senha: `webcontrol@2025`

---

## Comandos úteis

```bash
# Ver logs em tempo real
docker compose logs -f

# Parar o container
docker compose down

# Rebuild completo (após mudanças no código)
docker compose up -d --build

# Acessar o shell do container
docker compose exec web bash

# Criar superusuário manualmente
docker compose exec web python manage.py createsuperuser

# Executar migrações manualmente
docker compose exec web python manage.py migrate

# Shell do Django
docker compose exec web python manage.py shell
```

---

## Estrutura do Projeto

```
pi-univesp/
├── apps/
│   ├── core/           # Dashboard
│   ├── accounts/       # Autenticação (login/logout)
│   ├── fornecedores/   # CRUD de fornecedores
│   ├── produtos/       # CRUD de produtos
│   ├── notas/          # Notas fiscais e itens
│   └── financeiro/     # Pagamentos
├── config/
│   ├── settings.py     # Configurações do Django
│   ├── urls.py         # URLs raiz
│   └── wsgi.py         # Entry point WSGI
├── database/           # Arquivo SQLite (persistido via volume Docker)
├── docs/               # Documentação do projeto
├── scripts/
│   ├── entrypoint.sh   # Script de inicialização do container
│   └── bootstrap_django.sh
├── static/
│   ├── css/main.css    # CSS customizado
│   └── js/main.js      # JavaScript
├── templates/
│   ├── base.html       # Template base com sidebar
│   ├── registration/   # Login
│   ├── dashboard/      # Painel
│   ├── fornecedores/   # Templates de fornecedores
│   ├── produtos/       # Templates de produtos
│   └── notas/          # Templates de notas fiscais
├── .env.example        # Exemplo de configuração
├── .dockerignore
├── docker-compose.yml
├── Dockerfile
├── manage.py
└── requirements.txt
```

---

## Arquitetura do Código

O projeto segue a separação de responsabilidades do Django:

| Arquivo | Responsabilidade |
|---------|-----------------|
| `models.py` | Definição de entidades e regras de dados |
| `forms.py` | Validação de entrada e campos de formulário |
| `views.py` | Fluxo de requisição/resposta |
| `urls.py` | Roteamento por módulo |
| `templates/` | Interface visual |
| `admin.py` | Registro no painel admin |

---

## Regras de Negócio Implementadas

- Nota fiscal não pode ser salva sem fornecedor
- Data de vencimento não pode ser anterior à data de emissão
- Pagamento não pode exceder o saldo devedor da nota
- Ao quitar o saldo, o status muda automaticamente para **Paga**
- Notas com vencimento passado e saldo em aberto são marcadas como **Vencidas** no dashboard
- CNPJ é validado com algoritmo de dígitos verificadores
- Unicidade de nota por número + série + fornecedor

---

## Variáveis de Ambiente

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `SECRET_KEY` | (obrigatório) | Chave secreta do Django |
| `DEBUG` | `False` | Modo debug |
| `ALLOWED_HOSTS` | `*` | Hosts permitidos (separados por vírgula) |
| `DJANGO_SUPERUSER_USERNAME` | `admin` | Usuário admin criado na inicialização |
| `DJANGO_SUPERUSER_EMAIL` | `admin@webcontrol.local` | E-mail do admin |
| `DJANGO_SUPERUSER_PASSWORD` | `webcontrol@2025` | Senha do admin |

---

## Dados Persistidos

O banco de dados SQLite é armazenado em `/app/database/db.sqlite3` dentro do container e montado via volume Docker nomeado `db_data`. Os dados não são perdidos ao recriar o container.

Para fazer backup do banco:

```bash
docker compose cp web:/app/database/db.sqlite3 ./backup.sqlite3
```

Para restaurar:

```bash
docker compose cp ./backup.sqlite3 web:/app/database/db.sqlite3
```

---

## Desenvolvimento Local (sem Docker)

```bash
# Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure o .env
cp .env.example .env
# Edite o .env e defina DEBUG=True

# Aplique as migrações
python manage.py migrate

# Crie um superusuário
python manage.py createsuperuser

# Inicie o servidor de desenvolvimento
python manage.py runserver
```

---

## Licença

Projeto desenvolvido para fins acadêmicos — UNIVESP Projeto Integrador.
