"""
Research agent for The Orchestrator.
Uses Ollama (or any OpenAI-compatible API) to perform real research tasks.
"""

from typing import Any

from app.agents.base_agent import AgentState, BaseAgent
from app.config.settings import get_settings


class ResearchAgentState(AgentState):
    """State structure specific to the research agent"""
    query: str = ""
    research_results: list[str] = []  # noqa: RUF012
    summary: str = ""


class LLMClient:
    """Lightweight HTTP client for Ollama / OpenAI-compatible APIs."""

    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url.rstrip("/")

    def chat(self, model: str, messages: list[dict[str, str]], system: str | None = None) -> str:
        """Call the /api/chat endpoint (Ollama format)."""
        import http.client
        import json

        payload: dict[str, Any] = {"model": model, "messages": messages, "stream": False}
        if system:
            payload["messages"] = [{"role": "system", "content": system}] + payload["messages"]

        body = json.dumps(payload).encode("utf-8")
        conn = http.client.HTTPConnection(self.base_url.removeprefix("http://").removeprefix("https://"))
        conn.request("POST", "/api/chat", body=body, headers={"Content-Type": "application/json"})
        resp = conn.getresponse()
        data = json.loads(resp.read())
        conn.close()

        content = data.get("message", {}).get("content", "")
        if not content and "response" in data:
            content = data["response"]
        return content


class ResearchAgent(BaseAgent):
    """Research agent that queries an LLM and returns structured results."""

    def __init__(self, model: str = "llama3"):
        settings = get_settings()
        self.llm = LLMClient(settings.ollama_url)
        self.model = model
        super().__init__(
            name="Research Agent",
            description="An agent that researches topics and summarizes findings using an LLM",
        )

    def get_agent(self):
        """Return a compiled LangGraph workflow (when LangGraph is available)."""
        try:
            from langgraph.graph import END, StateGraph

            workflow = StateGraph(ResearchAgentState)

            workflow.add_node("research", self._research_node)
            workflow.add_node("summarize", self._summarize_node)

            workflow.set_entry_point("research")
            workflow.add_edge("research", "summarize")
            workflow.add_edge("summarize", END)

            return workflow.compile()
        except ImportError:
            return None

    # ---- LangGraph nodes ----

    def _research_node(self, state: ResearchAgentState) -> ResearchAgentState:
        system = (
            "Tu es un agent de recherche. "
            "Réponds de manière structurée en listant des points clés numérotés. "
            "Sois concis et factuel."
        )
        result_text = self.llm.chat(
            self.model,
            [{"role": "user", "content": f"Recherche : {state.query}"}],
            system=system,
        )

        results = [line.strip() for line in result_text.splitlines() if line.strip()]
        if not results:
            results = [result_text]

        return ResearchAgentState(
            messages=state.messages + [{"role": "assistant", "content": result_text}],
            query=state.query,
            research_results=results,
            summary="",
        )

    def _summarize_node(self, state: ResearchAgentState) -> ResearchAgentState:
        system = "Résume les résultats de recherche suivants de manière concise (2-3 phrases max)."
        combined = "\n".join(state.research_results)
        summary = self.llm.chat(
            self.model,
            [{"role": "user", "content": f"Résume :\n{combined}"}],
            system=system,
        )

        return ResearchAgentState(
            messages=state.messages + [{"role": "assistant", "content": summary}],
            query=state.query,
            research_results=state.research_results,
            summary=summary,
        )

    # ---- Fallback run() ----

    def run(self, inputs: dict[str, Any]) -> dict[str, Any]:
        """Direct execution without LangGraph (for simple use-cases)."""
        query = inputs.get("query", inputs.get("message", ""))
        if not query:
            return {"error": "Aucune requête fournie"}

        system = (
            "Tu es un agent de recherche. "
            "Réponds de manière structurée en listant des points clés numérotés. "
            "Sois concis et factuel."
        )
        result_text = self.llm.chat(
            self.model,
            [{"role": "user", "content": f"Recherche : {query}"}],
            system=system,
        )

        return {
            "query": query,
            "results": [line.strip() for line in result_text.splitlines() if line.strip()],
            "summary": result_text,
            "status": "completed",
        }
