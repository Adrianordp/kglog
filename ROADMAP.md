# KgLog Roadmap

## release/logweight-v0.1.0 — Monorepo Foundation

### feat/repo-init
- [x] Create top-level folder structure: `backend/`, `frontend/`
- [x] Add `.gitignore`
- [x] Add `.env.example` with all required variable keys (no values)
- [x] Add `README.md` skeleton with project description and local setup instructions

### feat/django-bootstrap
- [x] Create and activate Python virtual environment with uv with Python 3.13
- [ ] Install Django 6 and create `backend/` Django project
- [ ] Set up basic project structure with `config/` for settings and `apps/` for Django apps
- [ ] Run `django-admin startproject config backend/`
- [ ] Create `backend/apps/` package directory
- [ ] Split settings into `config/settings/base.py`, `dev.py`, `prod.py`
- [ ] Install and configure `django-environ`; load all secrets and DB URL from `.env`
- [ ] Add `requirements/base.txt`, `dev.txt`, `prod.txt`
- [ ] Confirm `python manage.py check` passes

### feat/docker-local
- [ ] Write `backend/Dockerfile` (dev stage with hot-reload)
- [ ] Write `frontend/Dockerfile` (dev stage with Vite HMR)
- [ ] Write `docker-compose.yml` with services: `db` (postgres:16), `redis`, `backend`, `frontend`
- [ ] Mount volumes for code hot-reload in both services
- [ ] Confirm `docker-compose up` boots all services cleanly

---

## release/logweight-v0.2.0 — Authentication

### feat/custom-user-model
- [ ] Create Django app `apps/users`
- [ ] Define `User` model extending `AbstractUser` (email as primary login field)
- [ ] Set `AUTH_USER_MODEL = "users.User"` in base settings
- [ ] Create and run initial migration
- [ ] Register `User` in Django admin

### feat/social-auth-backend
- [ ] Install `django-allauth`, `dj-rest-auth`, `djangorestframework-simplejwt`
- [ ] Configure `django-allauth` with Google OAuth2 provider
- [ ] Wire up `/api/v1/auth/` endpoints via `dj-rest-auth`
- [ ] Configure `simplejwt` to return access + refresh token pair on login
- [ ] Add Google client ID and secret to `.env.example`
- [ ] Manually test Google login flow returns valid JWT pair

---

## release/logweight-v0.3.0 — Organizations & Multi-Tenancy

### feat/organizations-model
- [ ] Create Django app `apps/organizations`
- [ ] Define `Organization` model: `name`, `slug`, `owner (FK User)`, timestamps
- [ ] Define `Membership` model: `user`, `org`, `role` (owner / member)
- [ ] Create and run migrations
- [ ] Register both models in Django admin

### feat/organizations-api
- [ ] Create `OrgScopedViewSet` mixin that filters all querysets by the request user's active org
- [ ] Implement `OrganizationViewSet` and `MembershipViewSet` with DRF
- [ ] Register routes under `/api/v1/orgs/`
- [ ] Install `drf-spectacular`; annotate endpoints and verify OpenAPI schema generates at `/api/docs/`
- [ ] Write unit tests for org scoping mixin

---

## release/logweight-v0.4.0 — Weight Tracking API

### feat/weight-model
- [ ] Create Django app `apps/tracking`
- [ ] Define `WeightEntry` model: `org (FK)`, `user (FK)`, `date`, `value_kg`, `notes`
- [ ] Create and run migration

### feat/weight-api
- [ ] Implement `WeightEntryViewSet` (list, create, retrieve, update, destroy)
- [ ] Apply `OrgScopedViewSet` mixin
- [ ] Add date-range filtering via `django-filter`
- [ ] Add cursor pagination
- [ ] Annotate with `drf-spectacular` schemas
- [ ] Write unit tests covering CRUD and org isolation

---

## release/logweight-v0.5.0 — React Foundation & Auth UI

### feat/vite-bootstrap
- [ ] Scaffold frontend with `npm create vite@latest frontend -- --template react-ts`
- [ ] Install and configure Tailwind CSS
- [ ] Install and configure `shadcn/ui`
- [ ] Install React Router v6, Zustand, Axios, TanStack Query (`@tanstack/react-query`)
- [ ] Configure Vite dev proxy: `/api/` → Django backend
- [ ] Create page scaffolding: `LoginPage`, `DashboardPage`, `NotFoundPage`
- [ ] Set up React Router with routes for the above pages

### feat/auth-flow
- [ ] Create Axios instance with JWT bearer interceptor
- [ ] Add silent token refresh interceptor (retry on 401 with refresh token)
- [ ] Create Zustand `authSlice`: stores access token (memory) + current user/org
- [ ] Install `@react-oauth/google`; add Google login button to `LoginPage`
- [ ] On OAuth success, POST `id_token` to `/api/v1/auth/google/` and store JWT in Zustand
- [ ] Implement `<ProtectedRoute>` wrapper that redirects unauthenticated users to `/login`
- [ ] Test full login → dashboard redirect flow

---

## release/logweight-v0.6.0 — Weight Log UI

### feat/weight-list
- [ ] Create TanStack Query hook `useWeightEntries` (GET `/api/v1/weights/`)
- [ ] Build `WeightTable` component: columns for date, value (kg), notes
- [ ] Add pagination controls tied to the query hook

### feat/weight-form
- [ ] Build `WeightFormModal` using `shadcn/ui` Dialog + Form components
- [ ] Create `useCreateWeightEntry` and `useUpdateWeightEntry` mutation hooks
- [ ] Implement delete with confirmation dialog (`useDeleteWeightEntry`)
- [ ] Invalidate `useWeightEntries` cache on mutation success

### feat/weight-chart
- [ ] Install `recharts`
- [ ] Build `WeightLineChart` component: date on X axis, kg on Y axis
- [ ] Add configurable date range selector (last 30 / 90 / 180 days / all time)
- [ ] Make chart responsive with `<ResponsiveContainer>`

---

## release/logweight-v0.7.0 — Body Measurements

### feat/measurements-model
- [ ] Define `BodyMeasurement` model: `org`, `user`, `date`, `waist_cm`, `hip_cm`, `chest_cm`, `arm_cm`, `thigh_cm`, `notes`
- [ ] Create and run migration

### feat/measurements-api
- [ ] Implement `BodyMeasurementViewSet` (CRUD) with org scoping
- [ ] Add date-range filtering and pagination
- [ ] Annotate OpenAPI schema
- [ ] Write unit tests

### feat/measurements-ui
- [ ] Create `useBodyMeasurements` query hook and mutations
- [ ] Build `MeasurementsTable` and `MeasurementFormModal` components
- [ ] Build `MeasurementsChart` (multi-line Recharts for each dimension)
- [ ] Add Measurements section to Dashboard

---

## release/logweight-v0.8.0 — Bioimpedance Tracking

### feat/bioimpedance-model
- [ ] Define `BioimpedanceEntry` model: `org`, `user`, `date`, `body_fat_pct`, `muscle_mass_kg`, `bone_mass_kg`, `body_water_pct`, `visceral_fat`, `notes`
- [ ] Create and run migration

### feat/bioimpedance-api
- [ ] Implement `BioimpedanceViewSet` (CRUD) with org scoping
- [ ] Add date-range filtering and pagination
- [ ] Annotate OpenAPI schema
- [ ] Write unit tests

### feat/bioimpedance-ui
- [ ] Create `useBioimpedance` query hook and mutations
- [ ] Build `BioimpedanceTable` and `BioimpedanceFormModal` components
- [ ] Build `BodyCompositionChart` (stacked bar: fat %, muscle, water %)
- [ ] Add Bioimpedance section to Dashboard

---

## release/logweight-v1.0.0 — Production Deployment

### feat/aws-infra
- [ ] Write production `backend/Dockerfile` (Gunicorn + `collectstatic` stage)
- [ ] Create S3 bucket and CloudFront distribution for the Vite build
- [ ] Define ECS Fargate task definition (backend container + Nginx sidecar)
- [ ] Provision RDS PostgreSQL instance
- [ ] Store all secrets in AWS Secrets Manager; inject as env vars in ECS task
- [ ] Configure `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, `SECURE_*` Django settings for prod

### feat/cicd
- [ ] Add GitHub Actions workflow: run `pytest` + `vitest` on every PR
- [ ] Add GitHub Actions workflow: build Docker image and push to ECR on merge to `main`
- [ ] Add GitHub Actions step: deploy new ECS task revision after image push
- [ ] Add GitHub Actions step: `vite build` → sync to S3 → CloudFront invalidation

### feat/prod-hardening
- [ ] Run and resolve `python manage.py check --deploy`
- [ ] Add rate limiting on all `/api/v1/auth/` endpoints (e.g. `django-ratelimit`)
- [ ] Integrate Sentry SDK in Django (error + performance)
- [ ] Integrate Sentry SDK in React frontend
- [ ] Verify HTTPS redirect and HSTS header in production
