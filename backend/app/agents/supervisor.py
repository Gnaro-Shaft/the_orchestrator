"""
Supervisor agent for The Orchestrator.
Routes user tasks to the appropriate specialist agent.
"""

from typing import Any

from app.agents.base_agent import AgentState, BaseAgent
from app.config.settings import get_settings


class SupervisorState(AgentState):
    """State structure for the supervisor agent"""
    current_task: str = ""
    task_description: str = ""
    agent_responses: list[dict[str, Any]] = []  # noqa: RUF012
    final_output: str = ""
    task_status: str = ""
    routed_agent: str = ""


class LLMClient:
    """Lightweight HTTP client for Ollama / OpenAI-compatible APIs."""

    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url.rstrip("/")

    def chat(self, model: str, messages: list[dict[str, str]], system: str | None = None) -> str:
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


class SupervisorAgent(BaseAgent):
    """Main supervisor that routes tasks to specialist agents via LLM."""

    def __init__(self, model: str = "llama3"):
        settings = get_settings()
        self.llm = LLMClient(settings.ollama_url)
        self.model = model
        super().__init__(
            name="Supervisor Agent",
            description="Routes tasks to specialist agents (research, code) based on content analysis",
        )

    def get_agent(self):
        try:
            from langgraph.graph import END, StateGraph

            workflow = StateGraph(SupervisorState)
            workflow.add_node("route", self._route_node)
            workflow.add_node("execute", self._execute_node)
            workflow.add_node("finalize", self._finalize_node)

            workflow.set_entry_point("route")
            workflow.add_edge("route", "execute")
            workflow.add_edge("execute", "finalize")
            workflow.add_edge("finalize", END)

            return workflow.compile()
        except ImportError:
            return None

    # ---- LangGraph nodes ----

    def _route_node(self, state: SupervisorState) -> SupervisorState:
        system = (
            "Tu es un superviseur technique. Analyse la tâche de l'utilisateur et détermine "
            "si elle relève de 'research' (recherche, analyse, explication de concepts) "
            "ou de 'code' (génération de code, débogage, développement). "
            "Réponds UNIQUEMENT par le mot 'research' ou 'code'. Pas d'autre texte."
        )
        response = self.llm.chat(
            self.model,
            [{"role": "user", "content": state.current_task or state.task_description}],
            system=system,
        ).strip().lower()

        routed_agent = "research" if "research" in response else "code"

        return SupervisorState(
            messages=state.messages,
            current_task=state.current_task,
            task_description=state.task_description,
            agent_responses=[],
            final_output="",
            task_status="routed",
            routed_agent=routed_agent,
        )

    def _execute_node(self, state: SupervisorState) -> SupervisorState:
        from app.agents.manager import AgentManager

        manager = AgentManager()
        agent_type = state.routed_agent

        try:
            result = manager.run_agent(agent_type, {
                "message": state.task_description or state.current_task,
                "query": state.task_description or state.current_task,
                "task": state.task_description or state.current_task,
            })
            return SupervisorState(
                messages=state.messages,
                current_task=state.current_task,
                task_description=state.task_description,
                agent_responses=[{"agent": agent_type, "result": result}],
                final_output="",
                task_status="executed",
                routed_agent=agent_type,
            )
        except Exception:  # noqa: BLE001
            return SupervisorState(
                messages=state.messages,
                current_task=state.current_task,
                task_description=state.task_description,
                agent_responses=[{"agent": agent_type, "error": "不可用"}],
                final_output="",
                task_status="error",
                routed_agent=agent_type,
            )

    def _finalize_node(self, state: SupervisorState) -> SupervisorState:
        responses = state.agent_responses

        # If there was an error, report it
        for r in responses:
            if "error" in r:
                return SupervisorState(
                    messages=state.messages,
                    current_task=state.current_task,
                    task_description=state.task_description,
                    agent_responses=responses,
                    final_output=f"Erreur lors de l'exécution par l'agent '{state.routed_agent}'",
                    task_status="error",
                    routed_agent=state.routed_agent,
                )

        # Collect all outputs into a summary
        outputs = []
        for r in responses:
            if "result" in r:
                result = r["result"]
                if isinstance(result, dict):
                    outputs.append(result.get("summary", result.get("output", str(result))))
                else:
                    outputs.append(str(result))

        if not outputs:
            return SupervisorState(
                messages=state.messages,
                current_task=state.current_task,
                task_description=state.task_description,
                agent_responses=responses,
                final_output="Aucune réponse disponible.",
                task_status="completed",
                routed_agent=state.routed_agent,
            )

        system = "Résume les réponses des agents en une réponse cohérente et complète pour l'utilisateur."
        combined = "\n\n".join(outputs)
        final = self.llm.chat(
            self.model,
            [{"role": "user", "content": f"Contexte : {state.task_description or state.current_task}\nRéponses agents :\n{combined}"}],
            system=system,
        )

        return SupervisorState(
            messages=state.messages + [{"role": "assistant", "content": final}],
            current_task=state.current_task,
            task_description=state.task_description,
            agent_responses=responses,
            final_output=final,
            task_status="completed",
            routed_agent=state.routed_agent,
        )

    # ---- Fallback run() ----

    def run(self, inputs: dict[str, Any]) -> dict[str, Any]:
        """Direct execution without LangGraph."""
        task = inputs.get("current_task", inputs.get("task_description", inputs.get("message", "")))
        if not task:
            return {"final_output": "Aucune tâche fournie.", "status": "error"}

        # Simple keyword-based routing fallback
        code_keywords = ["code", "coder", "débug", "debug", "générer", "créer", "programme", "fonction", "api", "frontend", "backend"]
        research_keywords = ["recherche", "explique", "qu'est-ce", "c'est quoi", "tendance", "analyse", "info"]

        task_lower = task.lower()
        if any(kw in task_lower for kw in code_keywords):
            agent_type = "code"
        elif any(kw in task_lower for kw in research_keywords):
            agent_type = "research"
        else:
            agent_type = "research"  # default

        from app.agents.manager import AgentManager
        manager = AgentManager()

        try:
            result = manager.run_agent(agent_type, {
                "message": task,
                "query": task,
                "task": task,
            })
            return {
                "final_output": result.get("summary", result.get("output", str(result))),
                "task": task,
                "routed_agent": agent_type,
                "status": "completed",
            }
        except Exception:  # noqa: BLE001
            return {
                "final_output": "Erreur lors de l'exécution de l'agent.",
                "task": task,
                "routed_agent": agent_type,
                "status": "error",
            }
