# ✈️ FlyWatch — Flight Price Monitoring API

A backend service for tracking flight prices and managing user subscriptions. Built with Django, Django REST Framework, Celery, and Redis — with real-time price monitoring, smart notifications, and exponential backoff for external API resilience.

---

## 📋 Table of Contents

- [About](#about)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Environment Variables](#environment-variables)
- [Testing](#testing)
- [Swagger](#swagger)
- [Tips](#tips)

---

## About

FlyWatch solves a common traveler problem: constantly checking flight prices manually. Users subscribe to a route, and the system notifies them automatically — but only when the price actually drops.

### Key Features

- **Flight Search** — real-time flight data via SerpApi (Google Flights integration)
- **Smart Caching** — search results cached in Redis for 5 minutes to reduce external API calls
- **Resilient External Calls** — Exponential Backoff handles third-party API downtime gracefully
- **Price Monitoring** — Celery Beat checks all active subscriptions every 6 hours in the background
- **Drop-Only Notifications** — users are notified only when the price falls below the last recorded notified price
- **Data Isolation** — strict per-user scoping for subscriptions and notifications; no data leakage between accounts

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Django + DRF | Backend framework and REST API |
| PostgreSQL | Primary database |
| Redis | Caching and Celery broker |
| Celery + Celery Beat | Background tasks and periodic scheduling |
| SerpApi | Google Flights data source |
| Docker & Docker Compose | Containerization |
| pytest | Testing |

---

## Quick Start

### Requirements

- Docker and Docker Compose
- SerpApi key
- Filled `.env` file (see below)

### 1. Clone the Repository

```bash
git clone <repo_url>
cd flywatch
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
# Fill in your values
```

### 3. Build and Run

```bash
docker-compose up --build
```

### Running Services

| Service | Port |
|---|---|
| API | 8000 |
| PostgreSQL | 5432 |
| Redis | 6379 |
| Celery Worker | — |
| Celery Beat | — |

> ⚠️ For local development (without Docker), ensure Redis and PostgreSQL are running and accessible before starting the server.

### Local Development (without Docker)

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## Environment Variables

```env
SECRET_API_KEY=your_serpapi_key
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_db_name
DJANGO_SECRET_KEY=your_django_secret_key
```

> ⚠️ Never commit real credentials. Use `.env.example` as the version-controlled template.

---

## Testing

23 unit and integration tests covering the core monitoring and notification logic.

Run inside Docker:

```bash
docker-compose exec web python manage.py test
```

### Test Coverage

- Serializer validation
- Service-layer mocking
- Celery task logic
- Security and permission checks

---

## Swagger

Interactive API documentation is available at:

```
http://localhost:8000/api/docs/
```

---

## Tips

- Use the Django Admin Panel (`/admin/`) to manually manage subscriptions during development or testing.
- Docker ensures a consistent environment across Redis, Celery, and PostgreSQL — no manual service management needed.
- Celery Beat runs automatically inside the Docker setup — no extra configuration required.

---

## Summary

This project demonstrates:

- Django + DRF backend with real-world third-party API integration
- Intelligent notification system (price-drop-only alerts)
- Background scheduling with Celery Beat
- Redis caching to minimize external API usage
- Exponential Backoff for production-grade resilience
- Strict per-user data isolation and permission scoping
- Full containerization with Docker Compose

> 👉 **Main focus:** automated flight price monitoring with smart notifications and resilient external API handling.

---

## License

MIT License
