/**
 * Service API pour communiquer avec l'orchestrateur
 */

const API_BASE_URL = 'http://localhost:8000/api/v1';

export const orchestratorAPI = {
  /** Envoyer un message au superviseur */
  sendMessage: async (message, context) => {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, context }),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return response.json();
  },

  /** Exécuter un agent spécifique */
  runAgent: async (agentType, inputs) => {
    const response = await fetch(`${API_BASE_URL}/agents/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ agent_type: agentType, inputs }),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return response.json();
  },

  /** Obtenir le statut des agents */
  getAgentStatus: async () => {
    const response = await fetch(`${API_BASE_URL}/agents/status`);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return response.json();
  },

  /** Lister les agents disponibles */
  listAgents: async () => {
    const response = await fetch(`${API_BASE_URL}/agents/list`);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return response.json();
  },
};
