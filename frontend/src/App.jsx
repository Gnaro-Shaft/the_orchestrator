import React, { useState, useEffect } from 'react';

// Composant principal de l'application
function App() {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [agentStatus, setAgentStatus] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // Récupérer le statut des agents au démarrage
  useEffect(() => {
    fetchAgentStatus();
    // Mettre à jour toutes les 30 secondes
    const interval = setInterval(fetchAgentStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchAgentStatus = async () => {
    try {
      // Remplacement par une simulation pour le moment
      setAgentStatus([
        { name: "Research Agent", status: "active", last_active: "Il y a 2 min" },
        { name: "Code Agent", status: "idle", last_active: "Il y a 10 min" },
        { name: "Supervisor", status: "active", last_active: "Il y a 1 min" }
      ]);
    } catch (error) {
      console.error('Erreur lors de la récupération du statut:', error);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    // Ajouter le message utilisateur
    const userMessage = {
      id: Date.now(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date().toISOString()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      // Simulation de réponse (dans un vrai système, cela appellerait l'API)
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const systemMessage = {
        id: Date.now() + 1,
        text: `Réponse du système : Je vous ai bien reçu sur "${inputMessage}". Le superviseur analyse votre requête.`,
        sender: 'system',
        timestamp: new Date().toISOString()
      };
      
      setMessages(prev => [...prev, systemMessage]);
    } catch (error) {
      console.error('Erreur lors de l\'envoi:', error);
      
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Erreur : Impossible de communiquer avec le système',
        sender: 'system',
        timestamp: new Date().toISOString()
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Composant MessageBubble
  const MessageBubble = ({ message }) => {
    const isUser = message.sender === 'user';
    
    return (
      <div className={`message-bubble ${isUser ? 'user-message' : 'system-message'}`}>
        <div className="message-content">
          {message.text}
        </div>
        <div className="message-timestamp">
          {new Date(message.timestamp).toLocaleTimeString()}
        </div>
      </div>
    );
  };

  // Composant AgentStatus
  const AgentStatus = () => (
    <div className="agent-status-section">
      <h2>Statut des Agents</h2>
      <div className="status-grid">
        {agentStatus.length > 0 ? (
          agentStatus.map((agent) => (
            <div key={agent.name} className="agent-card">
              <h3>{agent.name}</h3>
              <p className={`status ${agent.status}`}>
                {agent.status === 'active' ? '✓ Actif' : 
                 agent.status === 'idle' ? '○ Inactif' : 
                 agent.status === 'error' ? '✗ Erreur' : '• Inconnu'}
              </p>
              <p className="last-active">
                Dernier actif: {agent.last_active || 'Jamais'}
              </p>
            </div>
          ))
        ) : (
          <p>Aucun agent enregistré</p>
        )}
      </div>
    </div>
  );

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>🤖 The Orchestrator</h1>
        <p>Interface de communication avec les agents IA</p>
      </header>

      <main className="app-main">
        <div className="chat-section">
          <div className="chat-messages">
            {messages.map((message) => (
              <MessageBubble key={message.id} message={message} />
            ))}
            {isLoading && (
              <div className="message-bubble system-message">
                <div className="message-content">En cours de traitement...</div>
              </div>
            )}
          </div>

          <form onSubmit={handleSendMessage} className="chat-input">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Tapez votre message..."
              className="message-input"
            />
            <button 
              type="submit" 
              disabled={!inputMessage.trim() || isLoading}
              className="send-button"
            >
              Envoyer
            </button>
          </form>
        </div>

        <AgentStatus />
      </main>

      <style jsx>{`
        .app-container {
          max-width: 1200px;
          margin: 0 auto;
          padding: 20px;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }

        .app-header {
          text-align: center;
          margin-bottom: 30px;
          padding: 20px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border-radius: 10px;
        }

        .app-main {
          display: grid;
          grid-template-columns: 2fr 1fr;
          gap: 20px;
        }

        .chat-section {
          background: #f5f5f5;
          border-radius: 10px;
          padding: 20px;
        }

        .chat-messages {
          height: 400px;
          overflow-y: auto;
          margin-bottom: 20px;
          padding: 10px;
        }

        .message-bubble {
          margin-bottom: 15px;
          padding: 12px 16px;
          border-radius: 18px;
          max-width: 80%;
        }

        .user-message {
          background: #4a90e2;
          color: white;
          margin-left: auto;
          text-align: right;
        }

        .system-message {
          background: #e0e0e0;
          color: #333;
        }

        .message-timestamp {
          font-size: 0.7em;
          opacity: 0.7;
          margin-top: 5px;
        }

        .chat-input {
          display: flex;
          gap: 10px;
        }

        .message-input {
          flex: 1;
          padding: 12px;
          border: 1px solid #ddd;
          border-radius: 20px;
          outline: none;
        }

        .send-button {
          padding: 12px 24px;
          background: #4a90e2;
          color: white;
          border: none;
          border-radius: 20px;
          cursor: pointer;
        }

        .send-button:disabled {
          background: #ccc;
          cursor: not-allowed;
        }

        .agent-status-section {
          background: #f8f9fa;
          border-radius: 10px;
          padding: 20px;
        }

        .agent-status-section h2 {
          margin-top: 0;
          color: #333;
        }

        .status-grid {
          display: grid;
          gap: 15px;
        }

        .agent-card {
          background: white;
          padding: 15px;
          border-radius: 8px;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .agent-card h3 {
          margin: 0 0 10px 0;
          color: #333;
        }

        .status {
          font-weight: bold;
        }

        .status.active {
          color: #28a745;
        }

        .status.idle {
          color: #6c757d;
        }

        .status.error {
          color: #dc3545;
        }

        @media (max-width: 768px) {
          .app-main {
            grid-template-columns: 1fr;
          }
          
          .chat-messages {
            height: 300px;
          }
        }
      `}</style>
    </div>
  );
}

export default App;