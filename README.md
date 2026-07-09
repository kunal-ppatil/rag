# Enterprise RAG Blueprint

This repository is a starter scaffold for an enterprise RAG platform with:

- FastAPI for the API surface
- Modular agent orchestration for router, RAG, and analyst workloads
- MCP integration for tool access
- PostgreSQL, Redis, and Qdrant-friendly service boundaries
- RBAC and JWT-based security hooks
- Optional OpenAI-backed answers with a local fallback corpus
- Local document ingestion from `docs/kb`

## Layout

- `src/rag_enterprise/api` for HTTP routes
- `src/rag_enterprise/agents` for orchestration and task-specific agents
- `src/rag_enterprise/services` for retrieval, ingestion, vector storage, and RBAC
- `src/rag_enterprise/mcp` for MCP server integration points
- `src/rag_enterprise/worker` for async jobs

## Start Local Infrastructure

```bash
docker compose up -d
```

## Run the API

```bash
uvicorn rag_enterprise.main:app --reload
```

## Enable a real model

Set these environment variables in `.env` to use OpenAI for generation:

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
OPENAI_API_BASE=https://api.openai.com/v1
```

## Add your own documents

Drop `.md` or `.txt` files into `docs/kb`. You can add optional metadata at the top of each file:

```text
title: Engineering Release Notes
document_id: eng-001
allowed_groups: engineering,admin

Your document text goes here.
```

The app will prefer local documents automatically and fall back to the built-in corpus if the folder is empty.

## Next Implementation Steps

1. Wire JWT validation to your identity provider.
2. Add ingestion connectors and async chunking pipelines.
3. Implement hybrid retrieval with metadata filters for RBAC.
4. Add reranking, guardrails, and citation formatting.
