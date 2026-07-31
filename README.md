# The Orchestrator

Modular AI Orchestrator built with LangGraph, FastAPI and React.
Local-first, plugin-based and production-ready.

## Quick Start

### Prerequisites

- Python 3.13+
- Node.js 20+
- [Ollama](https://ollama.ai) (optional, for real LLM calls)
- [Docker](https://docker.com) (optional, for full stack)

### Backend

```bash
cd backend
uv sync
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm start
```

### Full Stack (Docker)

```bash
docker compose up --build
```

- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

## Architecture

```
Frontend (React) → API (FastAPI) → LangGraph Supervisor → Agents → Ollama
```

See `docs/agentIA.md` for the full vision and `docs/architecture/Architecture v1` for the design.

## Available Agents

| Agent      | Purpose                          |
|------------|----------------------------------|
| research   | Research & analysis via LLM      |
| code       | Code generation, debugging       |
| supervisor | Routes tasks to specialist agents |

## Roadmap

See `docs/agentIA.md` — sections Évolutions prévues and Sprint 1.

## License

MIT — see `LICENCE`.
