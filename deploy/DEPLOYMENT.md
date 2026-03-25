# Deployment Guide

## Local container deployment

1. Copy envs:
   - `cp .env.example .env`
2. Start stack:
   - `docker compose up --build -d`
3. Health check:
   - `curl http://localhost:8000/`
4. Stop stack:
   - `docker compose down`

## Cloud production baseline

- Container registry: push `api` image.
- Orchestrator: Kubernetes/ECS with autoscaling.
- Managed services:
  - PostgreSQL (RDS/Cloud SQL)
  - Redis (Elasticache/Memorystore)
  - Object storage (S3/GCS)
  - Vector DB (managed or self-hosted Chroma)
- Ingress + TLS termination.
- Secret manager for JWT and model provider keys.
- Observability: OpenTelemetry traces + metrics dashboards.
