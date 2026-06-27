# Backend — Technologies, Links & Standards

## Internal Resources
- **Confluence**: Backend Architecture space — ADRs, runbooks, service maps
- **Linear**: `BACKEND` project for all tickets
- **Datadog**: `nova-backend-*` dashboards for monitoring
- **GitHub**: `technova/backend-monorepo` (main repo)

## Tech Documentation

### FastAPI
- Version: 0.111+
- All routers under `app/api/`
- Dependency injection for auth via `Depends(get_current_user)`
- Pydantic v2 for request/response models

### PostgreSQL
- Version: 15
- Connection pooling via SQLAlchemy 2.0 async
- All migrations in `alembic/versions/`
- Never run raw SQL — use ORM models

### Redis
- Used for: session cache, rate limiting, distributed locks
- TTL policy: session keys expire in 8 hours
- Library: `redis-py` with async support

### Kafka
- Topics follow `nova.<service>.<event>` pattern (e.g., `nova.user.created`)
- Consumer groups named after the consuming service
- Dead letter queues enabled for all consumers

### Docker & Kubernetes
- Each service has its own `Dockerfile`
- Local dev: `docker-compose up` from repo root
- K8s manifests in `infra/k8s/`
- Staging namespace: `nova-staging`, Production: `nova-prod`

## Code Standards
- PEP8 enforced via `ruff`
- Type hints required on all functions
- Docstrings for public functions (Google style)
- No `print()` statements — use structured logging (`structlog`)

## Useful Commands
```bash
# Start local dev server
uvicorn app.main:app --reload

# Run tests
pytest tests/ -v --cov=app

# Run linter
ruff check .

# Database migrations
alembic upgrade head
alembic revision --autogenerate -m "description"
```

## Key Contacts
- **Staff Engineer**: Leads architecture reviews
- **Engineering Manager**: Escalation, career growth, 1:1s
- **DevOps team**: Infra issues, deployment help
- **#backend-dev** Slack channel: day-to-day technical discussions
