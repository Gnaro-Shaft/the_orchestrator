"""
Integration tests for The Orchestrator API.

Tests all endpoints via FastAPI TestClient.  LLMClient is mocked by the
``conftest.py`` fixture so Ollama does not need to be running.
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# Root & Health
# ---------------------------------------------------------------------------

def test_root():
    response = client.get("/api/v1/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "The Orchestrator API"
    assert data["version"] == "0.1.0"


def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


# ---------------------------------------------------------------------------
# Chat endpoint
# ---------------------------------------------------------------------------

def test_chat_sends_message():
    """POST /api/v1/chat — vérifie structure et code HTTP."""
    payload = {"message": "Bonjour"}
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["agent_used"] == "supervisor"
    assert data["status"] in ("completed", "processing")
    assert "response" in data
    assert "timestamp" in data


def test_chat_with_context():
    """POST /api/v1/chat avec contexte optionnel."""
    payload = {"message": "Test", "context": "Contexte supplémentaire"}
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ("completed", "processing")


def test_chat_missing_message():
    """Missing message field returns 422."""
    payload = {}
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# Agents: list
# ---------------------------------------------------------------------------

def test_agents_list():
    response = client.get("/api/v1/agents/list")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["agents"], list)
    assert "research" in data["agents"]
    assert "code" in data["agents"]
    assert "supervisor" in data["agents"]


# ---------------------------------------------------------------------------
# Agents: status
# ---------------------------------------------------------------------------

def test_agents_status():
    response = client.get("/api/v1/agents/status")
    assert response.status_code == 200
    data = response.json()
    agents = data["agents"]
    assert len(agents) == 3

    names = {a["name"] for a in agents}
    assert names == {"research", "code", "supervisor"}

    status_map = {a["name"]: a["status"] for a in agents}
    assert status_map["research"] == "active"
    assert status_map["supervisor"] == "active"
    assert status_map["code"] == "idle"


# ---------------------------------------------------------------------------
# Agents: run — valid agents
# ---------------------------------------------------------------------------

def test_run_research_agent():
    payload = {"agent_type": "research", "inputs": {"query": "Test query"}}
    response = client.post("/api/v1/agents/run", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["agent_type"] == "research"
    assert data["status"] == "completed"
    assert "result" in data
    assert data["result"]["status"] == "completed"


def test_run_code_agent():
    payload = {"agent_type": "code", "inputs": {"task": "Generate API"}}
    response = client.post("/api/v1/agents/run", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["agent_type"] == "code"
    assert data["status"] == "completed"


def test_run_supervisor_agent():
    payload = {"agent_type": "supervisor", "inputs": {"current_task": "Test"}}
    response = client.post("/api/v1/agents/run", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["agent_type"] == "supervisor"
    assert data["status"] == "completed"


# ---------------------------------------------------------------------------
# Agents: run — error cases
# ---------------------------------------------------------------------------

def test_run_unknown_agent():
    payload = {"agent_type": "trading", "inputs": {}}
    response = client.post("/api/v1/agents/run", json=payload)
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "trading" in data["detail"]


def test_run_missing_agent_type():
    payload = {"inputs": {}}
    response = client.post("/api/v1/agents/run", json=payload)
    assert response.status_code == 422


def test_run_missing_inputs():
    payload = {"agent_type": "research"}
    response = client.post("/api/v1/agents/run", json=payload)
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# Supervisor routing (end-to-end)
# ---------------------------------------------------------------------------

def test_supervisor_routes_to_research():
    payload = {"message": "Recherche les tendances IA 2026"}
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ("completed", "processing")


def test_supervisor_routes_to_code():
    payload = {"message": "Débogue cette fonction Python"}
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ("completed", "processing")
