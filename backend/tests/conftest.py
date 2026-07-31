"""
Pytest fixtures for The Orchestrator integration tests.

Patches every agent module's LLMClient so that tests can run without
Ollama being available.
"""

from unittest.mock import patch

import pytest

_MOCKED_RESPONSE = "Mocked LLM response for testing purposes."


def _make_mock_llm():
    """Return a MagicMock with a properly configured ``chat`` method."""
    mock = __import__("unittest.mock").mock.MagicMock()
    mock.chat.return_value = _MOCKED_RESPONSE
    return mock


@pytest.fixture(autouse=True)
def _mock_llm_clients():
    """Patch LLMClient in every agent module so that all agents use the mock."""
    with patch("app.agents.research_agent.LLMClient") as mock_research:
        mock_research.return_value = _make_mock_llm()
        with patch("app.agents.code_agent.LLMClient") as mock_code:
            mock_code.return_value = _make_mock_llm()
            with patch("app.agents.supervisor.LLMClient") as mock_supervisor:
                mock_supervisor.return_value = _make_mock_llm()
