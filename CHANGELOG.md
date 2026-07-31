# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Real LLM integration in ResearchAgent (Ollama)
- Real LLM integration in CodeAgent (Ollama)
- SupervisorAgent with LLM-based routing
- Frontend connected to backend API
- Proper CSS styling (separate App.css)
- Models module (Conversation, AgentLog, SystemConfig)
- Docker Compose with backend, frontend, Ollama, Qdrant

### Fixed
- Frontend no longer uses mock chat — calls real API
- CSS inline `<style jsx>` replaced with proper stylesheet
- `requirements.txt` no longer mixes Python and frontend deps
- CORS configuration fixed (removed `allow_credentials=True` with `*`)
- SupervisorAgent registered in AgentManager

## [0.1.0] — 2026-07-29

### Added
- Initial project scaffold
- FastAPI backend with `/` and `/health` endpoints
- React frontend with chat UI (mock)
- Base agent infrastructure
- Documentation (vision, architecture, supervisor design)
- Basic test suite (health, root)
