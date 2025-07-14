# Documentação do Projeto: SWAPI Search Service

**URL Base da API:** [https://u7xzgkjho0.execute-api.sa-east-1.amazonaws.com/health](https://u7xzgkjho0.execute-api.sa-east-1.amazonaws.com/health)

**Busca real na DB:** [https://u7xzgkjho0.execute-api.sa-east-1.amazonaws.com/api/v1/search?q=luke](https://u7xzgkjho0.execute-api.sa-east-1.amazonaws.com/api/v1/search?q=luke)

Este documento descreve a arquitetura, as funcionalidades e as decisões estratégicas por trás do SWAPI Search Service, um backend robusto e escalável para ingestão e consulta de dados do universo Star Wars.

## Visão Geral do Projeto

O sistema foi projetado para integrar-se com a API pública da SWAPI. Ele extrai, normaliza e armazena todos os dados de recursos (filmes, personagens, planetas, etc.) em um banco de dados PostgreSQL. Posteriormente, expõe esses dados através de uma API RESTful moderna, permitindo buscas complexas e navegação estruturada.

O projeto foi construído com foco em clareza, modularidade, escalabilidade e princípios de código limpo, culminando em uma implantação serverless na AWS.

## Funcionalidades Implementadas

O backend oferece um conjunto de funcionalidades para os consumidores da API (como um frontend React):

### Ingestão de Dados Automatizada (ETL)

Um script de linha de comando (`run_etl.py`) orquestra um processo completo de Extração, Transformação e Carga (ETL). Ele busca de forma resiliente todos os dados da SWAPI, normaliza as informações (resolvendo links de relacionamento para nomes legíveis) e os carrega em um banco de dados PostgreSQL centralizado.

### Busca Unificada com Relevância

Um único endpoint `GET /api/v1/search` permite buscas textuais (case-insensitive e parciais) em todos os tipos de recursos simultaneamente.

**Decisão Arquitetural:** A busca implementa um sistema de ranking de relevância, priorizando resultados onde o termo de busca corresponde ao nome ou título do recurso. Isso garante uma experiência de usuário mais intuitiva.

### Navegação Estruturada (Browse API)

Para complementar a busca, foram criados endpoints RESTful dedicados para cada tipo de recurso (ex: `GET /api/v1/films`, `GET /api/v1/people`). Esses endpoints permitem que o frontend navegue por categorias específicas de forma paginada.

### Filtragem Dinâmica e Detalhada

**Decisão Arquitetural:** Para oferecer uma experiência de exploração rica, os endpoints de navegação suportam filtragem dinâmica do lado do servidor. É possível combinar múltiplos filtros através de query parameters (ex: `/api/v1/films?director=lucas&producer=kurtz`). Isso permite que o frontend construa interfaces de filtro complexas sem a necessidade de buscar e filtrar grandes volumes de dados no lado do cliente.

<img width="1894" height="888" alt="image" src="https://github.com/user-attachments/assets/f464f79e-ce47-4d0f-9655-224307ceb4ad" />


### Segurança e Controle de Tráfego

**Decisão Arquitetural:** A API implementa rate limiting (limitação de taxa de requisições) na camada de borda (API Gateway). Isso protege o sistema contra abuso, controla custos e garante a estabilidade do serviço.

## Decisões de Arquitetura e Tecnologia

A arquitetura foi projetada para ser escalável e de fácil manutenção, refletindo práticas modernas de engenharia de software.

### Arquitetura Limpa (Clean Architecture)

O backend segue uma clara separação de responsabilidades em camadas:

- **API Layer (`api/`):** Define os endpoints, schemas (contratos de dados) e lida com as requisições HTTP.
- **Repository Layer (`repositories/`):** Abstrai todo o acesso a dados. Os endpoints não sabem como os dados são buscados; eles apenas pedem ao repositório, tornando o sistema testável e permitindo futuras mudanças na fonte de dados (ex: adicionar um cache).
- **Database Layer (`db/`):** Gerencia a conexão com o banco de dados e define os modelos ORM (SQLAlchemy).

### Implantação Serverless na AWS

**Decisão Arquitetural:** A aplicação é implantada em um ambiente serverless para máxima escalabilidade e otimização de custos.

- **AWS Lambda:** Executa o código da aplicação FastAPI sem a necessidade de gerenciar servidores. O pacote de implantação, contendo o código e todas as dependências, é criado de forma automatizada e consistente usando um Dockerfile multi-stage.

- **API Gateway:** Atua como a "porta de entrada" da API, gerenciando o roteamento, a segurança e o rate limiting.

- **AWS RDS (PostgreSQL):** Fornece um banco de dados relacional gerenciado, seguro e escalável.

#### Amazon S3 para Artefatos

**Decisão Arquitetural:** O AWS Lambda possui um limite de tamanho para pacotes de código enviados diretamente. Para acomodar aplicações complexas com muitas dependências, o método de implantação padrão da indústria é utilizar um bucket S3 como intermediário. Nosso pipeline de implantação automatizado faz o upload do pacote .zip da aplicação para um bucket S3 privado e, em seguida, instrui o Lambda a buscar o código a partir dessa localização. Isso aumenta o limite de tamanho e otimiza a velocidade de deploy.

#### AWS VPC e VPC Endpoints

**Decisão Arquitetural:** A segurança é um pilar central. A infraestrutura de rede foi projetada para manter o banco de dados e o Lambda em uma rede privada (VPC), isolados da internet pública. Para permitir que o Lambda acesse outros serviços da AWS (como o Secrets Manager para buscar as credenciais do banco), foram configurados VPC Endpoints. Eles criam um túnel de comunicação privado e seguro entre o Lambda e os serviços AWS, garantindo que nenhum dado sensível trafegue pela internet.
<img width="832" height="846" alt="image" src="https://github.com/user-attachments/assets/b07f3c35-21c8-40b2-b724-330f23697661" />

