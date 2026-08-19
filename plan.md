# City Companion — Project Development Plan

*Go + TypeScript + PostgreSQL/PostGIS + Redis + AI*

Project goal: Build a local activity-discovery platform where users can post plans (movies, bowling, gaming, sports, food, etc.), discover nearby activities on a map, and request to join. AI will later improve semantic discovery, recommendations, moderation, and natural-language interaction.

## Architecture Principle

- Start as a modular monolith. Do not begin with microservices.
- Go owns the core application/backend APIs.
- TypeScript + Next.js owns the web frontend.
- PostgreSQL is the primary database; PostGIS handles geographic queries.
- Redis is introduced only when caching, rate limiting, sessions, queues, or realtime workflows require it.
- AI is introduced after the core product works. Use a separate Python/FastAPI AI service because the Python ML/GenAI ecosystem is stronger.

## Phase 1 — Basic Frontend / Product Prototype

Objective: Build the user-facing experience with mock/local data first. The goal is to validate the UX before spending time on backend complexity.

- Set up Next.js + TypeScript + Tailwind CSS + component library.
- Create application layout: navbar, map area, event cards, filters, event detail page.
- Implement event creation form.
- Implement event browsing and category filtering.
- Add map integration using Leaflet + OpenStreetMap.
- Display event markers and event details from mock JSON.
- Create responsive mobile-friendly UI.
- Create loading, empty, and error states.
- Define TypeScript types for User, Event, Location, JoinRequest, and Category.

**Deliverable:** A clickable frontend where a user can browse nearby plans, open an event, create a plan, and see plans on a map using mock data.

**Do NOT build yet:**
- Authentication
- Chat
- AI
- Redis
- Microservices
- Complex state management

## Phase 2 — Backend + Real Data

Objective: Replace mock data with a production-style Go backend and persistent PostgreSQL data.

### Backend Stack

- Go
- Gin
- PostgreSQL
- PostGIS
- GORM initially; move toward sqlc for stronger SQL/type-safety once the schema stabilizes
- Redis
- Docker + Docker Compose

### Implementation Order

1. **Project setup:** Go modules, configuration, environment variables, Docker Compose, database connection, migrations.
2. **Event API:** Create, read, update, delete events; validation; pagination.
3. **Geographic queries:** Store latitude/longitude using PostGIS and query events within a radius.
4. **Users:** User model and authentication using short-lived access tokens and refresh tokens.
5. **Join requests:** Request to join, accept/reject, event capacity, membership state.
6. **Event discovery:** Category filters, time filters, radius filters, pagination.
7. **Redis:** Add only where useful: caching, rate limiting, sessions, or background jobs.
8. **Realtime:** WebSockets for join-request and notification updates.
9. **Testing:** Unit tests for services, integration tests for APIs/database, request validation.
10. **Observability:** Structured logs and basic metrics; later Prometheus + Grafana.

### Core Data Model

- users
- events
- join_requests
- event_members
- categories
- notifications

**Deliverable:** A working full-stack application where real users can create events, discover nearby events on a map, and request to join.

## Phase 3 — AI / ML Integration

Objective: Add AI only where it improves discovery, matching, trust, or user experience. AI is not a decorative chatbot.

### AI Stack

- Python
- FastAPI
- pgvector inside PostgreSQL
- Sentence Transformers and/or hosted embedding APIs
- LLM API such as Gemini or OpenAI
- Ollama for local-model experimentation
- Pydantic for structured AI inputs/outputs

### AI Feature Roadmap

1. **Semantic Event Search:** Embed event descriptions and user queries; use pgvector similarity search so queries such as "something fun indoors tonight" can find relevant events even without exact keywords.
2. **AI Event Categorization:** Infer categories from free-form event descriptions instead of forcing users to select everything manually.
3. **Event Description Assistant:** Turn a short input such as "bowling tonight, need 3 people" into a clear structured event description.
4. **Recommendation Engine:** Combine semantic similarity, distance, time, category, past interactions, and popularity to rank relevant events.
5. **AI Match Score:** Estimate compatibility between a user and an event using interests, activity history, and semantic similarity.
6. **Moderation:** Detect spam, scams, abusive content, suspicious event descriptions, and potentially unsafe content.
7. **Natural-Language Discovery:** Convert requests such as "indoor activities within 5 km after 7 PM" into structured filters and retrieve matching events.

### AI Service Architecture

```
Frontend → Go API → PostgreSQL/PostGIS/Redis
                ↓
          Python AI Service
                ↓
        LLM / Embedding Model
```

Important: keep business-critical logic in Go. The AI service should expose focused capabilities such as `/embed`, `/recommend`, `/moderate`, and `/parse-query` rather than becoming the entire backend.

## Recommended Repository Structure After Phase 3

```
city-companion/
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── types/
│
├── backend/
│   ├── cmd/api/
│   ├── internal/
│   │   ├── handlers/
│   │   ├── services/
│   │   ├── repositories/
│   │   ├── models/
│   │   ├── database/
│   │   └── middleware/
│   └── migrations/
│
├── ai-service/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   ├── models/
│   │   └── retrieval/
│   └── requirements.txt
│
├── docker-compose.yml
└── README.md
```

## Milestones / Definition of Done

- **M1 — Frontend prototype:** Mock events + map + event creation UI
- **M2 — Core backend:** Go API + PostgreSQL + CRUD
- **M3 — Geo discovery:** PostGIS radius queries + map backed by real data
- **M4 — Social workflow:** Authentication + join requests + event membership
- **M5 — Production foundations:** Validation + tests + Docker + Redis where justified
- **M6 — Semantic discovery:** Embeddings + pgvector + natural-language event search
- **M7 — Recommendations:** Hybrid recommendation/ranking system
- **M8 — Trust + AI UX:** Moderation + description assistant + natural-language filters

## What to Learn Along the Way

- **TypeScript:** types, generics, async code, API clients, React/Next.js patterns.
- **Go:** interfaces, goroutines, context, error handling, HTTP APIs, dependency injection.
- **PostgreSQL:** joins, indexes, transactions, constraints, query planning.
- **PostGIS:** coordinates, spatial indexes, radius and bounding-box queries.
- **Redis:** caching, TTLs, rate limiting, and when caching is actually useful.
- **Backend architecture:** handlers → services → repositories.
- **Security:** password hashing, token rotation, authorization, input validation, rate limiting.
- **AI:** embeddings, vector search, RAG, structured outputs, evaluation, recommendation systems.
- **ML:** feature engineering, ranking, classification, offline evaluation.
- **DevOps:** Docker, environment management, CI/CD, logging, metrics, deployment.

## Critical Rules for the Project

- Do not add a technology merely because it looks impressive on a resume.
- Do not introduce microservices until there is a real reason to split a component.
- Do not add an LLM chatbot as the primary AI feature.
- Do not introduce a dedicated vector database before pgvector becomes insufficient.
- Do not build recommendations before collecting enough interaction data; start with content-based/hybrid ranking.
- Every AI feature needs an evaluation method. "It seems good" is not enough.
- Ship each phase before starting the next one.

## Suggested First Build Sequence

1. Phase 1: Finish the frontend screens with mock data.
2. Phase 2: Build the Go event API.
3. Phase 2: Connect PostgreSQL.
4. Phase 2: Add PostGIS and real map-based discovery.
5. Phase 2: Add authentication and join requests.
6. Phase 2: Add tests and Docker.
7. Phase 3: Add embeddings + pgvector semantic search.
8. Phase 3: Add recommendations.
9. Phase 3: Add moderation and natural-language discovery.
