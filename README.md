# Web Control — Sistema de Gestão Fiscal

Sistema web para organização de notas fiscais, controle de pagamentos e acompanhamento financeiro desenvolvido como Projeto Integrador (PI) da UNIVESP.

---

## Visão Geral

O **Web Control** é um MVP voltado para pequenas empresas que ainda controlam documentos fiscais de forma manual. O sistema permite:

- Cadastrar fornecedores com busca automática via CNPJ e preenchimento de endereço por CEP
- Cadastrar produtos com dados fiscais (NCM, CEST, alíquotas)
- Registrar notas fiscais de entrada com itens, cálculo automático de totais e sincronização do valor da nota
- Controlar pagamentos totais ou parciais por nota
- Visualizar indicadores financeiros no dashboard
- Receber alertas de notas prestes a vencer ou já vencidas

---

## Stack

| Camada       | Tecnologia                        |
|--------------|-----------------------------------|
| Backend      | Django 5                          |
| Banco        | SQLite (via Django ORM)           |
| Templates    | Django Templates                  |
| CSS/UI       | Bootstrap 5.3 + CSS customizado   |
| Ícones       | Bootstrap Icons 1.11              |
| Fonte        | Inter (Google Fonts)              |
| Servidor     | Gunicorn                          |
| Estáticos    | WhiteNoise                        |
| Container    | Docker + Docker Compose           |

---

## Funcionalidades

### Dashboard
- Total a pagar (notas pendentes + vencidas)
- Total vencido em aberto
- Total pago no mês corrente
- Próximos vencimentos nos próximos 7 dias
- Últimas notas cadastradas

### Fornecedores
- Cadastro completo (nome fantasia, razão social, CNPJ, telefone, e-mail, endereço)
- Validação de CNPJ com dígitos verificadores
- Busca automática de dados via API pública (publica.cnpj.ws) — sem autenticação
- Preenchimento automático de endereço via CEP (ViaCEP)
- Máscaras de campo: CNPJ, telefone, CEP
- Ativação e inativação
- Busca por nome, razão social e CNPJ

### Produtos
- Cadastro com unidade de medida, preço de custo, preço de venda e estoque
- Dados fiscais: NCM, CEST, origem da mercadoria, alíquotas (ICMS, IPI, PIS, COFINS)
- Máscaras de campo: NCM e CEST
- Alerta visual quando estoque está abaixo do mínimo
- Ativação e inativação
- Busca em tempo real (sem reload)

### Notas Fiscais
- Cabeçalho da nota (número, série, fornecedor, datas, valor, status)
- Itens com seleção de produto, preenchimento automático de descrição e preço de venda
- Cálculo automático do total de cada item e sincronização do valor total da nota
- Filtros por número, fornecedor, status e período
- Destaque visual por status: **Pendente**, **Paga**, **Vencida**, **Cancelada**
- Validação: data de vencimento não pode ser anterior à emissão
- Unicidade: número + série + fornecedor

### Pagamentos
- Registro por nota fiscal (total ou parcial)
- Formas de pagamento: Dinheiro, PIX, Boleto, Transferência, Cartão
- Validação: pagamento não pode exceder o saldo devedor
- Atualização automática do status da nota ao quitar

### Notificações
- Sino de alertas no cabeçalho
- Exibe notas vencidas e notas a vencer em até 7 dias
- Contagem de pendências em destaque

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

Edite o `.env`:

```env
SECRET_KEY=troque-para-uma-chave-secreta-forte
DEBUG=False

# Domínio de acesso (separar por vírgula se houver mais de um)
ALLOWED_HOSTS=seu-dominio.com

# Necessário para HTTPS (proxy reverso / EasyPanel)
CSRF_TRUSTED_ORIGINS=https://seu-dominio.com

DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@exemplo.com
DJANGO_SUPERUSER_PASSWORD=senha-segura-aqui
```

> **Importante:** Em produção use uma `SECRET_KEY` longa e aleatória. Nunca use `DEBUG=True` em produção.

### 3. Suba o container

```bash
docker compose up -d --build
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

---

## Deploy com EasyPanel

O `docker-compose.yml` está configurado para funcionar com proxy reverso (EasyPanel, Traefik, Nginx):

- Usa `expose: 8000` em vez de `ports` — o EasyPanel gerencia o roteamento
- `USE_X_FORWARDED_HOST = True` e `SECURE_PROXY_SSL_HEADER` configurados para HTTPS correto

Variáveis de ambiente obrigatórias no EasyPanel:

```
SECRET_KEY=chave-secreta-forte
DEBUG=False
ALLOWED_HOSTS=seu-dominio.easypanel.host
CSRF_TRUSTED_ORIGINS=https://seu-dominio.easypanel.host
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@exemplo.com
DJANGO_SUPERUSER_PASSWORD=senha-segura
```

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

# Backup do banco de dados
docker compose cp web:/app/database/db.sqlite3 ./backup.sqlite3

# Restaurar backup
docker compose cp ./backup.sqlite3 web:/app/database/db.sqlite3
```

---

## Estrutura do Projeto

```
pi-univesp/
├── apps/
│   ├── core/           # Dashboard e context processor de notificações
│   ├── accounts/       # Autenticação (login/logout)
│   ├── fornecedores/   # CRUD de fornecedores
│   ├── produtos/       # CRUD de produtos + endpoint JSON para auto-fill
│   ├── notas/          # Notas fiscais e itens
│   └── financeiro/     # Pagamentos
├── config/
│   ├── settings.py     # Configurações do Django
│   ├── urls.py         # URLs raiz
│   └── wsgi.py         # Entry point WSGI
├── database/           # SQLite persistido via volume Docker
├── scripts/
│   └── entrypoint.sh   # Migrações + criação de superusuário + Gunicorn
├── static/
│   ├── css/main.css    # CSS customizado (minimalista, sem dependências)
│   └── js/main.js      # JS: sidebar, máscaras, live search, notificações
├── templates/
│   ├── base.html       # Template base com sidebar e barra de notificações
│   ├── registration/   # Login
│   ├── dashboard/      # Painel principal
│   ├── fornecedores/   # Lista e formulário
│   ├── produtos/       # Lista e formulário
│   └── notas/          # Lista, formulário e detalhe
├── .env.example
├── .dockerignore
├── docker-compose.yml
├── Dockerfile
├── manage.py
└── requirements.txt
```

---

## Variáveis de Ambiente

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `SECRET_KEY` | — | Chave secreta do Django (obrigatório) |
| `DEBUG` | `False` | Modo debug (nunca `True` em produção) |
| `ALLOWED_HOSTS` | `*,localhost,127.0.0.1` | Hosts permitidos (separados por vírgula) |
| `CSRF_TRUSTED_ORIGINS` | — | Origens HTTPS confiáveis para CSRF |
| `DJANGO_SUPERUSER_USERNAME` | `admin` | Usuário admin criado na inicialização |
| `DJANGO_SUPERUSER_EMAIL` | `admin@webcontrol.local` | E-mail do admin |
| `DJANGO_SUPERUSER_PASSWORD` | `webcontrol@2025` | Senha do admin |

---

## APIs Externas Utilizadas

| API | Uso | Autenticação |
|-----|-----|--------------|
| [publica.cnpj.ws](https://publica.cnpj.ws) | Consulta dados de empresa pelo CNPJ | Nenhuma |
| [ViaCEP](https://viacep.com.br) | Preenchimento de endereço pelo CEP | Nenhuma |

---

## Regras de Negócio

- Nota fiscal não pode ser salva sem fornecedor ativo
- Data de vencimento não pode ser anterior à data de emissão
- Pagamento não pode exceder o saldo devedor da nota
- Ao quitar o saldo, o status muda automaticamente para **Paga**
- Notas vencidas e a vencer são exibidas nas notificações do sistema
- CNPJ é validado com algoritmo de dígitos verificadores
- Unicidade de nota por número + série + fornecedor

---

## Desenvolvimento Local (sem Docker)

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

pip install -r requirements.txt

cp .env.example .env
# Edite o .env: DEBUG=True, ALLOWED_HOSTS=localhost

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## Licença

Projeto desenvolvido para fins acadêmicos — UNIVESP Projeto Integrador.
