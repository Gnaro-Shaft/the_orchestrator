"""
Example workflow demonstrating agent collaboration in The Orchestrator.
This shows how the supervisor orchestrates multiple agents working together.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.agents.manager import AgentManager
from app.agents.communication import (
    send_agent_message, 
    receive_agent_messages,
    store_agent_memory,
    retrieve_agent_memory
)


def example_workflow():
    """Demonstrate a collaborative workflow between agents"""
    
    print("=== Exemple de Workflow Collaboratif ===")
    print("Superviseur → Recherche → Développement")
    print()
    
    # Création du gestionnaire d'agents
    manager = AgentManager()
    print(f"✓ Agents disponibles : {manager.list_agents()}")
    print()
    
    # 1. Le superviseur reçoit une tâche complexe
    task = "Créer un système de recommandation basé sur les tendances IA pour 2026"
    print(f"1. Superviseur recoit la tâche : {task}")
    
    # 2. Le superviseur analyse et distribue aux agents
    print("2. Superviseur analyse la tâche...")
    print("   - Besoin de recherche sur les tendances IA")
    print("   - Besoin de développement d'une solution technique")
    print()
    
    # 3. Envoie une demande de recherche au agent de recherche
    send_agent_message(
        sender='supervisor', 
        recipient='research', 
        content='Rechercher les principales tendances en intelligence artificielle pour 2026',
        message_type='request'
    )
    
    # 4. Reçoit le message et exécute l'agent de recherche
    research_msgs = receive_agent_messages('research')
    if research_msgs:
        print(f"3. Agent de recherche reçoit la commande : {research_msgs[0].content}")
        
        # Exécution de l'agent de recherche via le gestionnaire
        research_result = manager.run_agent('research', {
            'messages': [{'role': 'user', 'content': 'Recherche sur IA 2026'}],
            'query': 'Tendances IA 2026'
        })
        print(f"   Résultat de la recherche : {research_result}")
        
        # Stocke les résultats dans la mémoire partagée
        store_agent_memory('research', 'trends_2026', [
            'IA générale et grandes modèles',
            'IA pour le développement logiciel',
            'IA et sécurité cybernétique'
        ])
        print("   Résultat stocké en mémoire partagée")
    
    print()
    
    # 5. Envoie une demande au développeur
    trends = retrieve_agent_memory('research', 'trends_2026')
    if trends:
        send_agent_message(
            sender='supervisor',
            recipient='code', 
            content=f'Créer une solution technique pour : {", ".join(trends[:2])}',
            message_type='request'
        )
        print("4. Superviseur demande au développeur de créer une solution")
        
        # Exécution du code agent (simulation) 
        code_result = manager.run_agent('code', {
            'task': 'créer solution technique',
            'programming_language': 'Python'
        })
        print(f"   Résultat du développement : {code_result['type']}")
    
    print()
    
    # 6. Le superviseur rassemble tous les résultats
    print("5. Superviseur compile les résultats et produit une réponse finale")
    
    research_trends = retrieve_agent_memory('research', 'trends_2026')
    if research_trends:
        final_output = f"""
Résultat du workflow collaboratif :
=================================

Tâche : {task}

Résultats de la recherche :
- {research_trends[0]}
- {research_trends[1]}
- {research_trends[2]}

Solution technique proposée :
- Architecture basée sur des modèles d'IA
- Intégration API REST
- Système de recommandation adaptatif

Évaluation : Le projet est structuré pour être évolutif et utilisable en production.
        """
        print(final_output)
    
    print("✓ Workflow collaboratif terminé avec succès !")
    return "Workflow complet"


def demo_full_system():
    """Demonstrate full system functionality"""
    print("\n=== Démonstration Système Complet ===")
    
    # Test de communication complète
    try:
        from app.agents.communication import (
            send_agent_message, 
            receive_agent_messages,
            store_agent_memory,
            retrieve_agent_memory,
            broadcast_system_message
        )
        
        print("1. Test des communications :")
        msg1 = send_agent_message('research', 'code', 'Besoin d\'aide pour le débogage')
        msg2 = send_agent_message('supervisor', 'research', 'Recherche sur les tendances IA')
        print(f"   Messages envoyés : {msg1.sender} -> {msg1.recipient}, {msg2.sender} -> {msg2.recipient}")
        
        # Réception des messages
        code_msgs = receive_agent_messages('code')
        research_msgs = receive_agent_messages('research')
        print(f"   Messages reçus pour 'code' : {len(code_msgs)}")
        print(f"   Messages reçus pour 'research' : {len(research_msgs)}")
        
        # Test de mémoire
        print("2. Test de mémoire partagée :")
        store_agent_memory('supervisor', 'system_status', 'Operational')
        status = retrieve_agent_memory('supervisor', 'system_status')
        print(f"   Statut système : {status}")
        
        # Test de broadcast
        print("3. Test de broadcast :")
        broadcasts = broadcast_system_message('supervisor', 'Maintenance prévue demain')
        print(f"   Broadcast envoyé à {len(broadcasts)} agents")
        
        print("\n✓ Système complet fonctionnel !")
        return True
        
    except Exception as e:
        print(f"✗ Erreur dans la démonstration complète : {e}")
        return False


if __name__ == "__main__":
    example_workflow()
    demo_full_system()
    print("\n=== Fin de la démonstration ===")