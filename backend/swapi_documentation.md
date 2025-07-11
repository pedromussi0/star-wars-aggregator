# API de Busca e Navegação do SWAPI

Serviço de backend para agregação de dados de Star Wars. O sistema executa um processo de ETL a partir da API pública swapi.info, armazena os dados em PostgreSQL e os expõe através de uma aplicação FastAPI com dois padrões de acesso.

## Tabela de Conteúdos

- [Funcionalidades](#funcionalidades)
- [Visão Geral da Arquitetura](#visão-geral-da-arquitetura)
- [Pipeline de ETL](#pipeline-de-etl)
- [Schema do Banco de Dados](#schema-do-banco-de-dados)
- [Design da API](#design-da-api)
- [Configuração](#configuração)
- [Endpoints da API](#endpoints-da-api)
- [Desenvolvimento](#desenvolvimento)
- [Estrutura do Projeto](#estrutura-do-projeto)

## Funcionalidades

- **Pipeline de ETL**: Script de linha de comando que busca dados do SWAPI, valida usando Pydantic e resolve URLs de relacionamento.
- **Padrões de API Duplos**: 
  - Navegação RESTful: Endpoints por tipo de recurso
  - Busca Unificada: Endpoint único para busca de texto em todos os recursos
- **API Rica em Hipermídia**: Todas as respostas incluem URLs autorreferenciais
- **Arquitetura Escalável**: FastAPI, PostgreSQL e SQLAlchemy com abstração de motor de busca
- **Configuração baseada em ambiente**: Logs estruturados em JSON, migrações Alembic e containerização Docker

## Visão Geral da Arquitetura

```
[SWAPI] --(ETL)--> [PostgreSQL] <--(API)-- [FastAPI]
```

## Pipeline de ETL

O processo de ETL (`scripts/run_etl.py`) executa três etapas:

1. **Extração**: SwapiClient busca todos os recursos de swapi.info
2. **Transformação**: DataNormalizer converte URLs de relacionamento em objetos ricos
   - Antes: `{"films": ["https://.../films/1"]}`
   - Depois: `{"films": [{"url": "https://.../films/1", "title": "A New Hope"}]}`
3. **Carga**: DataLoader realiza inserção em massa no PostgreSQL

## Schema do Banco de Dados

Tabela única `swapi_resource`:

- `id`, `swapi_id`, `type`, `name`: Metadados para indexação
- `data` (JSONB): Objeto JSON completo do recurso
- `searchable_text` (TEXT): Campo desnormalizado para busca

**Índices**:
- Índice GIN em `searchable_text` para busca de texto completo
- Índice único em `(type, swapi_id)` para busca de itens específicos

## Design da API

Dois padrões de acesso:

- **Navegação**: Endpoints RESTful por tipo (`/api/v1/films`, `/api/v1/people/{id}`)
- **Busca**: Endpoint único (`/api/v1/search?q=...`) para busca global

## Configuração

### Pré-requisitos

- Docker & Docker Compose
- Poetry

### Configuração Local

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd pedromussi0-star-wars-aggregator/backend
```

2. **Configure variáveis de ambiente**
```bash
cp .env.example .env
```

3. **Instale dependências**
```bash
poetry install
```

4. **Inicie o banco de dados**
```bash
docker-compose up -d db
```

5. **Aplique migrações**
```bash
poetry run alembic upgrade head
```

6. **Execute o pipeline de ETL**
```bash
poetry run python scripts/run_etl.py
```

7. **Inicie o servidor**
```bash
poetry run uvicorn swapi_search.main:app --reload
```

**URLs disponíveis**:
- API: http://localhost:8000
- Documentação: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## Endpoints da API

Todos os endpoints estão sob o prefixo `/api/v1`.

### Endpoints de Navegação

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/films` | Lista paginada de filmes |
| GET | `/films/{film_id}` | Filme específico |
| GET | `/people` | Lista paginada de pessoas |
| GET | `/people/{person_id}` | Pessoa específica |
| GET | `/planets` | Lista paginada de planetas |
| GET | `/planets/{planet_id}` | Planeta específico |
| GET | `/species` | Lista paginada de espécies |
| GET | `/species/{species_id}` | Espécie específica |
| GET | `/starships` | Lista paginada de naves |
| GET | `/starships/{starship_id}` | Nave específica |
| GET | `/vehicles` | Lista paginada de veículos |
| GET | `/vehicles/{vehicle_id}` | Veículo específico |

**Exemplo**:
```bash
curl http://localhost:8000/api/v1/people/1
```

### Endpoint de Busca

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/search` | Busca global por palavras-chave |

**Parâmetros**:
- `q` (obrigatório): Termo de busca
- `type` (opcional): Filtrar por tipo específico
- `limit` (opcional, padrão: 10): Resultados por página
- `offset` (opcional, padrão: 0): Deslocamento para paginação

**Exemplo**:
```bash
curl "http://localhost:8000/api/v1/search?q=droid&limit=5"
```

## Desenvolvimento

### Testes

```bash
poetry run pytest
```

### Migrações do Banco de Dados

**Gerar nova migração**:
```bash
poetry run alembic revision --autogenerate -m "Descrição da mudança"
```

**Aplicar migrações**:
```bash
poetry run alembic upgrade head
```

**Reverter migração**:
```bash
poetry run alembic downgrade -1
```

### Execução Local vs Docker

- **Local**: Usa configurações do `.env` e conecta ao PostgreSQL em localhost
- **Docker**: O `docker-compose.yml` substitui `POSTGRES_HOST=db` para conexão interna

## Estrutura do Projeto

```
backend/
├── alembic/                # Scripts de migração do banco de dados
├── scripts/                # Scripts autônomos, principalmente ETL
│   └── etl/
├── src/
│   └── swapi_search/       # Código-fonte principal
│       ├── api/            # Camada da API: endpoints, schemas, dependências
│       ├── core/           # Componentes centrais: config, logging
│       ├── db/             # Camada do banco: models, gerenciamento de sessão
│       └── search/         # Abstração do motor de busca
├── tests/                  # Testes automatizados
├── .env.example            # Exemplo de configuração
├── alembic.ini             # Configuração do Alembic
├── docker-compose.yml      # Configuração do Docker Compose
├── Dockerfile              # Instruções Docker para o container da API
└── pyproject.toml          # Dependências e configuração do projeto
```