
# Games For You – Backend (Django + Neon PostgreSQL)

(The project is still in development.)

This repository contains the backend API for Games For You, an e-commerce platform for digital games.

The backend is built with Django, Django REST Framework, Neon PostgreSQL, CORS, and connects to a React + Vite + TypeScript frontend.

Front-end repository - (https://github.com/KaBarbi/games-for-you-frontend)

---

## Tech Stack

- Python 3
- Django
- Django REST Framework
- PostgreSQL (Neon DB)
- django-filter
- drf-spectacular (OpenAPI / Swagger)
- django-cors-headers
- Render (deployment-ready)

---

## Architecture

The backend follows a **layered RESTful architecture** using Django and DRF.

### Architectural Principles

- Separation of concerns (models, serializers, views, filters)
- Stateless authentication (JWT)
- Modular app structure
- Environment-based configuration
- Production-grade relational database (PostgreSQL)

The system is structured to support horizontal scalability and future feature expansion.

---

## Core Features

- JWT authentication (access & refresh tokens)
- Secure user registration and login
- Paginated game catalog
- Dynamic filtering (price range and platform)
- RESTful endpoint design
- Structured validation using DRF serializers
- Automatic OpenAPI schema generation

---

## Architectural Decisions

- DRF ViewSets for standardized CRUD operations
- Declarative filtering with django-filter
- Global pagination configuration
- Explicit permission classes per endpoint
- Automatic schema generation with drf-spectacular
- Environment variable isolation (.env)
- PostgreSQL instead of SQLite for production readiness

---

## Security Considerations

- SECRET_KEY excluded from version control
- Database credentials managed via environment variables
- CORS properly configured
- Explicit authentication and authorization enforcement
- No sensitive user data exposed in responses

---
- Resiliência:
O projeto já implementa validações robustas nos serializers com raise_exception=True que captura erros e retorna respostas HTTP estruturadas, evitando crashes. O rate limiting global protege contra abuso com 100 requisições/hora para anônimos e 1000 para usuários autenticados. O PostgreSQL garante transações ACID em operações críticas. No futuro, seria interessante adicionar um handler customizado para padronizar todas as respostas de erro em um formato único. Implementar validações específicas nos serializers do carrinho para verificar estoque antes de adicionar itens. Adicionar logging detalhado para rastrear exceções em produção.

- Performance:
O projeto já utiliza paginação global evitando retornar dados excessivos, filtros declarativos com django-filter otimizando queries no banco, e estrutura modular que evita redundâncias. No futuro, seria interessante adicionar índices de banco de dados nos campos platform, price e created_at para acelerar buscas filtradas. Implementar select_related() e prefetch_related() nos ViewSets eliminando problema N+1 queries. Substituir o cache local por Redis, permitindo múltiplas instâncias compartilharem cache. 

- Segurança: 
O projeto já mantém CORS restrito apenas aos domínios necessários (localhost:5173 em dev e Render em produção), credentials de banco em variáveis de ambiente, JWT com 60 minutos de access token, e validadores de senha padrão do Django implementando múltiplas verificações. No futuro, seria interessante reduzir o access token para 15 minutos aumentando segurança contra tokens comprometidos. Adicionar validação rigorosa e sanitização de inputs do cliente nos serializers. Garantir que produção rode exclusivamente sob HTTPS.

- Simultaneidade:
O projeto está fundamentado como stateless em WSGI permitindo distribuição horizontal entre múltiplas instâncias, PostgreSQL gerencia acesso concorrente naturalmente através de transações, e rate limiting protege contra sobrecarga de um cliente singular. No futuro, seria interessante configurar Gunicorn com múltiplos workers distribuindo carga entre processos. Considerar workers gevent para melhor eficiência em termos de memória. Implementar connection pooling no PostgreSQL com pgBouncer. Configurar Nginx como load balancer distribuindo requisições entre instâncias.

---

Built with ❤️ by [Kaue Barbi](https://kabarbi.vercel.app)



