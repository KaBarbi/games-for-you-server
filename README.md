
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

Built with ❤️ by [Kaue Barbi](https://kabarbi.vercel.app)



