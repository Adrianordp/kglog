# KgLog

A SaaS fitness tracking application that allows users to log and visualize their weight, body measurements, and bioimpedance data over time.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.13 / Django 6 |
| REST API | Django REST Framework (DRF) |
| API Schema | drf-spectacular (OpenAPI 3) |
| Authentication | django-allauth + dj-rest-auth + SimpleJWT |
| Social Login | Google OAuth2 |
| Frontend | React 19 + TypeScript + Vite |
| UI | Tailwind CSS + shadcn/ui |
| Server State | TanStack Query (React Query) |
| Client State | Zustand |
| HTTP Client | Axios |
| Charts | Recharts |
| Database | PostgreSQL 18 |
| Multi-tenancy | Shared schema (org-scoped rows) |
| Deployment | AWS (ECS Fargate + RDS + S3 + CloudFront) |
| CI/CD | GitHub Actions |

---

## Repository Structure

```
kglog/
├── backend/
│   ├── config/
│   │   └── settings/
│   └── apps/
│       ├── users/            # Custom User model, Google OAuth
│       ├── organizations/    # Tenant model, Membership, org scoping
│       └── tracking/         # WeightEntry, BodyMeasurement, BioimpedanceEntry
│   ├── frontend/
│   └── src/
│       ├── api/              # Axios client + per-resource query hooks
│       ├── components/       # Shared UI components
│       ├── pages/            # Route-level page components
│       ├── store/            # Zustand slices (auth, org)
│       └── charts/           # Recharts wrappers
├── docker-compose.yml
├── .env.example
├── ROADMAP.md
└── README.md
```

---

## Core Features

### Weight Tracking
Log body weight entries with date and optional notes. Visualize progress as a trend line chart with configurable date ranges (30 / 90 / 180 days / all time).

### Body Measurements
Record and track circumference measurements: waist, hip, chest, arm, thigh. Multi-line chart to compare dimension evolution over time.

### Bioimpedance
Log bioimpedance scale readings: body fat %, muscle mass, bone mass, body water %, and visceral fat index. Stacked bar chart for body composition breakdown.

---

## Architecture Decisions

**Shared-schema multi-tenancy** — every tenant-scoped model has a `ForeignKey` to `Organization`. A shared `OrgScopedViewSet` mixin automatically filters all querysets to the authenticated user's active org. Simpler to operate at early stage; can migrate to schema-per-tenant if isolation requirements grow.

**JWT over sessions** — required for a stateless API consumed by a separate-origin SPA. Access token stored in memory (Zustand); refresh token in an `httpOnly` cookie. A silent refresh Axios interceptor retries any 401 automatically.

**TanStack Query over Redux** — handles all server state (caching, pagination, background refetch, mutations) without boilerplate. Zustand is used only for the thin auth/org slice.

**Custom User model from day one** — `AUTH_USER_MODEL` is set before the first migration. Email is the primary login identifier.

**Split Django settings** — `base.py` / `dev.py` / `prod.py` loaded via `DJANGO_SETTINGS_MODULE`. All secrets and connection strings come from environment variables via `django-environ`.

---

## Local Development

### Prerequisites
- Docker and Docker Compose
- A Google OAuth2 client ID and secret

### Setup

```bash
git clone https://github.com/your-org/kglog.git
cd kglog
cp .env.example .env          # fill in required values
docker-compose up --build
```

| Service | URL |
|---|---|
| React frontend (Vite HMR) | http://localhost:5173 |
| Django API | http://localhost:8000 |
| API docs (Swagger UI) | http://localhost:8000/api/docs/ |
| Django admin | http://localhost:8000/admin/ |

### Running tests

```bash
# Backend
docker-compose exec backend pytest --cov

# Frontend
docker-compose exec frontend npm run test
```

---

## Deployment (AWS)

| Component | AWS Service |
|---|---|
| Frontend (static build) | S3 + CloudFront |
| Backend (Django + Gunicorn) | ECS Fargate |
| Database | RDS PostgreSQL |
| Secrets | AWS Secrets Manager |
| Container registry | ECR |

CI/CD is handled by GitHub Actions:
- Every PR → run `pytest` + `vitest`
- Merge to `main` → build Docker image → push to ECR → deploy new ECS task revision + Vite build → S3 sync → CloudFront invalidation

---

## Roadmap

See [ROADMAP.md](ROADMAP.md) for the full list of planned releases and feature branches.
