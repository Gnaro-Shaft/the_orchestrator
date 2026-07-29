/**
 * Service API pour communiquer avec l'orchestrateur
 */

const API_BASE_URL = 'http://localhost:8000/api/v1';

export const orchestratorAPI = {
  // Envoyer un message au superviseur
  sendMessage: async (message) => {
    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Erreur lors de l\'envoi du message:', error);
      throw error;
    }
  },

  // Exécuter un agent spécifique
  runAgent: async (agentType, inputs) => {
    try {
      const response = await fetch(`${API_BASE_URL}/agents/run`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          agent_type: agentType,
          inputs: inputs
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Erreur lors de l\'exécution de l\'agent:', error);
      throw error;
    }
  },

  // Obtenir le statut des agents
  getAgentStatus: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/agents/status`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Erreur lors de la récupération du statut:', error);
      throw error;
    }
  },

  // Envoyer un message entre agents
  sendAgentMessage: async (sender, recipient, content) => {
    try {
      const response = await fetch(`${API_BASE_URL}/communication/send`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          sender: sender,
          recipient: recipient,
          content: content
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Erreur lors de l\'envoi du message:', error);
      throw error;
    }
  }
};