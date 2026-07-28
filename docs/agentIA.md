# agentIA.md

# The Orchestrator

## Mission

Créer une plateforme d'orchestration d'agents IA moderne, modulaire et
open source, capable de servir de fondation à plusieurs applications :

-   Mnemo
-   Assistant IA personnel
-   Assistant de développement
-   Bot de trading
-   Automatisations
-   Futurs SaaS

Le projet doit rester simple à utiliser tout en étant suffisamment
robuste pour une utilisation en production.

------------------------------------------------------------------------

# Vision

L'objectif n'est pas de créer un simple chatbot, mais un framework
d'orchestration d'agents.

À terme, un nouvel agent devra pouvoir être ajouté sans modifier le cœur
de l'application.

------------------------------------------------------------------------

# Principes d'architecture

-   Clean Architecture
-   SOLID
-   Modularité
-   Séparation des responsabilités
-   Configuration par environnement
-   Tests avant intégration
-   Documentation continue
-   Faible couplage
-   Forte cohésion

------------------------------------------------------------------------

# Stack technique

## Frontend

-   React 19
-   TypeScript
-   Vite
-   Tailwind CSS 4
-   shadcn/ui
-   React Router
-   TanStack Query
-   Zustand
-   React Hook Form
-   Zod
-   Vitest
-   Playwright

## Backend

-   Python 3.13
-   FastAPI
-   LangGraph
-   Pydantic
-   SQLAlchemy
-   Alembic
-   Pytest
-   Ruff
-   Black
-   MyPy

## IA

-   Ollama
-   Architecture compatible OpenAI
-   Compatible Anthropic
-   Compatible vLLM

## Bases de données

### SQLite

-   Conversations
-   Historique
-   Paramètres
-   Configuration
-   Logs

### Qdrant

-   Embeddings
-   RAG
-   Mémoire vectorielle
-   Documentation
-   Vault Obsidian

------------------------------------------------------------------------

# Architecture logique

Frontend React → API FastAPI → LangGraph Supervisor → Agents → Outils →
Stockage (SQLite / Qdrant)

------------------------------------------------------------------------

# Registres

Le cœur du projet sera composé de plusieurs registres :

-   Agent Registry
-   Tool Registry
-   Model Registry
-   Memory Registry

Ces registres permettront d'ajouter des fonctionnalités sans modifier le
noyau.

------------------------------------------------------------------------

# Évolutions prévues

v0.1 : Chat

v0.2 : Router + RAG

v0.3 : Mémoire

v0.4 : Outils

v0.5 : Multi-agents

v0.6 : Plugins

v0.7 : Dashboard

v0.8 : API publique

v0.9 : Extensions

v1.0 : Plateforme complète

------------------------------------------------------------------------

# Interface Web

## MVP

-   Liste des conversations
-   Chat
-   Streaming
-   Paramètres
-   Mode sombre

## Futur

-   Dashboard
-   Inspecteur d'agents
-   Visualisation LangGraph
-   Historique des outils
-   Sources RAG
-   Mémoire
-   Statistiques
-   Monitoring

------------------------------------------------------------------------

# Structure du dépôt

backend/ frontend/ docs/ docker/ tests/ .github/

------------------------------------------------------------------------

# Sprint 1 (v0.1)

## Backend

-   Initialisation
-   FastAPI
-   LangGraph
-   Chat Agent
-   Endpoint /chat
-   Streaming
-   Ollama
-   Docker

## Frontend

-   React
-   Chat
-   Streaming
-   Gestion des conversations

## Qualité

-   Ruff
-   Black
-   MyPy
-   ESLint
-   Prettier
-   Pytest
-   Vitest

Livrable : Un orchestrateur complet capable de dialoguer avec Ollama via
LangGraph depuis une interface React.

------------------------------------------------------------------------

# Règles de développement

Chaque fonctionnalité suit le cycle :

1.  Analyse
2.  Conception
3.  Tests
4.  Développement
5.  Documentation
6.  Validation
7.  Version

Aucune fonctionnalité n'est intégrée sans tests ni documentation.

------------------------------------------------------------------------

# Objectif long terme

Construire un projet de référence, réutilisable dans tous les futurs
projets IA et suffisamment qualitatif pour être présenté comme une
réalisation majeure sur GitHub.
