import React, { useState, useEffect } from 'react';
import './App.css';
import { orchestratorAPI } from './services/api';

const API_AVAILABLE = true;
const DEFAULT_AGENTS = [
  { name: 'Research Agent', status: 'offline' },
  { name: 'Code Agent', status: 'offline' },
  { name: 'Supervisor', status: 'offline' },
];

function App() {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [agentStatus, setAgentStatus] = useState(DEFAULT_AGENTS);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [apiReachable, setApiReachable] = useState(false);

  // Check API health on mount
  useEffect(() => {
    checkApiHealth();
    const interval = setInterval(checkApiHealth, 30000);
    return () => clearInterval(interval);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const checkApiHealth = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/v1/health');
      if (res.ok) {
        setApiReachable(true);
        try {
          const data = await orchestratorAPI.getAgentStatus();
          if (data.agents) {
            setAgentStatus(data.agents.map(a => ({
              name: a.name,
              status: a.status,
              last_active: a.last_active
                ? new Date(a.last_active).toLocaleString('fr-FR')
                : 'Jamais',
            })));
          }
        } catch {
          // Agent status endpoint may not exist yet; stay offline
        }
      } else {
        setApiReachable(false);
      }
    } catch {
      setApiReachable(false);
    }
  };

  const showError = (msg) => {
    setError(msg);
    setTimeout(() => setError(null), 5000);
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    const userMessage = {
      id: Date.now(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);
    setError(null);

    try {
      const data = await orchestratorAPI.sendMessage(inputMessage);
      const systemMessage = {
        id: Date.now() + 1,
        text: data.response || 'Aucune réponse reçue.',
        sender: 'system',
        timestamp: new Date().toISOString(),
        agentUsed: data.agent_used,
      };
      setMessages(prev => [...prev, systemMessage]);
    } catch (err) {
      console.error('Erreur API:', err);
      const errorMessage = {
        id: Date.now() + 1,
        text: `Erreur de connexion au backend (${err.message}). Vérifiez que l'API FastAPI est démarrée sur le port 8000.`,
        sender: 'system',
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, errorMessage]);
      showError(`Impossible de joindre le backend : ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  /* ---- Render helpers ---- */

  const MessageBubble = ({ message }) => {
    const isUser = message.sender === 'user';
    return (
      <div className={`message-bubble ${isUser ? 'user-message' : 'system-message'}`}>
        <div className="message-content">{message.text}</div>
        <div className="message-timestamp">
          {new Date(message.timestamp).toLocaleTimeString('fr-FR')}
          {message.agentUsed && ` · ${message.agentUsed}`}
        </div>
      </div>
    );
  };

  const AgentStatusCard = () => (
    <div className="agent-status-section">
      <h2>Statut des Agents</h2>
      <p style={{ fontSize: '0.8rem', color: '#888', marginBottom: 12 }}>
        {apiReachable ? '✅ Backend connecté' : '❌ Backend injoignable'}
      </p>
      <div className="status-grid">
        {agentStatus.map(agent => (
          <div key={agent.name} className="agent-card">
            <h3>{agent.name}</h3>
            <p className={`status ${agent.status}`}>
              {agent.status === 'active' ? '● Actif' :
               agent.status === 'idle' ? '○ Inactif' :
               agent.status === 'error' ? '✗ Erreur' : '○ Hors ligne'}
            </p>
            <p className="last-active">
              Dernier actif : {agent.last_active || 'Jamais'}
            </p>
          </div>
        ))}
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
            {messages.length === 0 && (
              <div className="empty-state">
                Envoyez un message pour commencer une conversation avec les agents.
              </div>
            )}
            {messages.map(msg => (
              <MessageBubble key={msg.id} message={msg} />
            ))}
            {isLoading && (
              <div className="message-bubble system-message">
                <div className="message-content">⏳ Traitement en cours…</div>
              </div>
            )}
          </div>

          <form onSubmit={handleSendMessage} className="chat-input">
            <input
              type="text"
              value={inputMessage}
              onChange={e => setInputMessage(e.target.value)}
              placeholder="Tapez votre message…"
              className="message-input"
              disabled={isLoading}
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

        <AgentStatusCard />
      </main>

      {error && <div className="error-toast">{error}</div>}
    </div>
  );
}

export default App;
