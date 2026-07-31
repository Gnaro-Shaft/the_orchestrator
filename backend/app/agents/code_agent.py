"""
Code/Development expert agent for The Orchestrator.
Uses Ollama (or any OpenAI-compatible API) for code generation, debugging, and explanation.
"""

from typing import Any

from app.agents.base_agent import AgentState, BaseAgent
from app.config.settings import get_settings


class CodeAgentState(AgentState):
    """State structure specific to the code development agent"""
    task: str = ""
    programming_language: str = "Python"
    code_snippet: str = ""
    explanation: str = ""
    issues_found: list[str] = []  # noqa: RUF012
    improvements: list[str] = []  # noqa: RUF012


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


class CodeAgent(BaseAgent):
    """Specialized agent for code-related tasks and development assistance."""

    def __init__(self, model: str = "llama3"):
        settings = get_settings()
        self.llm = LLMClient(settings.ollama_url)
        self.model = model
        super().__init__(
            name="Code Development Expert",
            description="An expert agent specialized in coding, debugging, and software development tasks",
        )

    def get_agent(self):
        try:
            from langgraph.graph import END, StateGraph

            workflow = StateGraph(CodeAgentState)
            workflow.add_node("analyze", self._analyze_node)
            workflow.add_node("respond", self._respond_node)

            workflow.set_entry_point("analyze")
            workflow.add_edge("analyze", "respond")
            workflow.add_edge("respond", END)

            return workflow.compile()
        except ImportError:
            return None

    def _analyze_node(self, state: CodeAgentState) -> CodeAgentState:
        task = state.task.lower()
        if "debug" in task:
            prompt = (
                f"Débogue le code suivant en {state.programming_language} :\n"
                f"{state.code_snippet}\n\n"
                "Liste les problèmes trouvés et propose des corrections."
            )
        elif "generate" in task or "create" in task:
            prompt = (
                f"Génère du code en {state.programming_language} pour la tâche suivante :\n"
                f"{state.task}"
            )
        elif "explain" in task:
            prompt = (
                f"Explique ce code en {state.programming_language} :\n"
                f"{state.code_snippet}\n\n"
                "Donne une explication claire des concepts clés, des meilleures pratiques et des pièges courants."
            )
        else:
            prompt = (
                f"Assistance développement en {state.programming_language} :\n"
                f"{state.task}"
            )

        system = (
            "Tu es un expert en développement logiciel. "
            "Fournis du code propre, commenté et fonctionnel. "
            "Si on te demande de déboguer, analyse le code ligne par ligne."
        )
        response = self.llm.chat(self.model, [{"role": "user", "content": prompt}], system=system)

        return CodeAgentState(
            messages=state.messages + [{"role": "assistant", "content": response}],
            task=state.task,
            programming_language=state.programming_language,
            code_snippet=state.code_snippet,
            explanation=response,
            issues_found=[],
            improvements=[],
        )

    def _respond_node(self, state: CodeAgentState) -> CodeAgentState:
        return CodeAgentState(
            messages=state.messages + [{"role": "assistant", "content": f"---\n{state.explanation}"}],
            task=state.task,
            programming_language=state.programming_language,
            code_snippet=state.code_snippet,
            explanation=state.explanation,
            issues_found=state.issues_found,
            improvements=state.improvements,
        )

    def run(self, inputs: dict[str, Any]) -> dict[str, Any]:
        """Direct execution without LangGraph."""
        task = inputs.get("task", inputs.get("message", "Développement"))
        language = inputs.get("programming_language", "Python")
        code = inputs.get("code_snippet", "")

        system = (
            "Tu es un expert en développement logiciel. "
            "Fournis du code propre, commenté et fonctionnel."
        )
        prompt = f"Tâche : {task}\nLangage : {language}"
        if code:
            prompt += f"\nCode :\n{code}"

        response = self.llm.chat(self.model, [{"role": "user", "content": prompt}], system=system)

        return {
            "task": task,
            "programming_language": language,
            "output": response,
            "status": "completed",
        }
