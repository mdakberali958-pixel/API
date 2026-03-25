# Hallucination-Aware AI — Production Design

## 1) Architecture Diagram (Text)

```text
[Next.js Frontend]
  ├─ Auth UI (JWT)
  ├─ Chat UI (Standard/Verified Toggle)
  ├─ Evidence & Risk Panel
  └─ Admin Dashboard
          |
          v
[API Gateway / FastAPI]
  ├─ /auth      -> Auth Service (JWT, RBAC)
  ├─ /chat      -> AI Orchestrator
  ├─ /kb        -> Document Ingestion Service
  ├─ /admin     -> Analytics + Monitoring APIs
  └─ /eval      -> Benchmark & reporting
          |
          v
[AI Processing Layer]
  ├─ Retrieval Service (Chroma/FAISS)
  ├─ Prompt Builder
  ├─ LLM Service (Standard vs Verified)
  ├─ Hallucination Detection Engine
  │    ├─ Grounding signal
  │    ├─ Self-consistency signal
  │    ├─ Semantic similarity signal
  │    └─ Claim-level verification signal
  └─ Confidence Scoring
          |
          v
[Data Layer]
  ├─ PostgreSQL (users, chats, logs, metrics)
  ├─ Object Storage (PDFs, docs)
  ├─ Vector DB (Chroma/FAISS)
  ├─ Redis (cache, rate limiting)
  └─ Observability (Prometheus/Grafana + OpenTelemetry)
```

## 2) Monorepo Folder Structure

```text
.
├── frontend/
│   ├── app/
│   │   ├── page.tsx            # Landing
│   │   ├── chat/page.tsx
│   │   ├── dashboard/page.tsx
│   │   ├── docs/page.tsx
│   │   └── contact/page.tsx
│   ├── components/
│   │   ├── chat/
│   │   ├── evidence/
│   │   └── ui/
│   ├── lib/api-client.ts
│   └── styles/
├── backend/
│   ├── app/
│   │   ├── api/routes/
│   │   ├── services/
│   │   ├── models/
│   │   ├── core/
│   │   └── main.py
│   └── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── deploy/DEPLOYMENT.md
```

## 3) Backend API Design

- `POST /api/v1/auth/signup` — create account
- `POST /api/v1/auth/login` — issue JWT
- `POST /api/v1/chat/query` — ask question in standard/verified mode
- `POST /api/v1/kb/upload` — upload PDF/doc
- `POST /api/v1/kb/index` — chunk + embed + store vectors
- `GET /api/v1/chat/history` — user chat history
- `GET /api/v1/admin/metrics` — system and model KPIs
- `POST /api/v1/eval/run` — run benchmark set (TruthfulQA/custom)

## 4) AI Pipeline Logic (Step-by-Step)

1. Accept user query and selected mode.
2. Validate auth, quota, and rate limit.
3. If verified mode: retrieve top-k context from vector DB.
4. Build prompt with policy constraints and mode-specific instructions.
5. Generate answer from selected LLM.
6. Run hallucination engine signals:
   - grounding (answer ↔ retrieved docs)
   - self-consistency (N generations)
   - semantic alignment
   - claim-level verification
7. Aggregate to confidence score and hallucination probability.
8. Return answer + risk explanation + evidence references.
9. Persist logs and metrics for analytics.

## 5) Database Schema (Core)

- `users(id, email, password_hash, role, created_at)`
- `conversations(id, user_id, title, created_at)`
- `messages(id, conversation_id, role, content, mode, created_at)`
- `documents(id, user_id, name, mime_type, storage_uri, created_at)`
- `chunks(id, document_id, chunk_text, embedding_id, metadata)`
- `query_logs(id, user_id, query, mode, latency_ms, created_at)`
- `hallucination_reports(id, message_id, probability, confidence, signals_json)`
- `evaluations(id, dataset_name, run_at, accuracy, hallucination_rate, notes)`

## 6) Deployment Strategy (Docker + Cloud)

- Build API image with root `Dockerfile`.
- Run full local stack with `docker-compose.yml`.
- Promote images to cloud registry and deploy with autoscaling.
- Externalize state to managed Postgres/Redis/object storage.

## 7) Scaling Strategy

- Horizontal scale API + workers with queue-based backpressure.
- Cache retrieval and frequent prompts.
- Batch embedding generation.
- Partition logs and analytics tables.
- Introduce model routing by cost/latency SLO.

## Constraint Reminder

This system estimates hallucination risk probabilistically. It does **not** guarantee truth.
