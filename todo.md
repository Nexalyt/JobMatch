# Plan
## Stage 0 – Repository & Environment Bootstrap  (Architect Agent)

| Step | Action                                                       |
| ---- | ------------------------------------------------------------ |
| 0.1  | **Create mono-repo** (`resume-ranker/`) with `frontend/`, `backend/`, `infra/`, `docs/` |
| 0.2  | **Generate README** with high-level architecture, build instructions, and MoA roadmap |
| 0.3  | **Add dev-containers** (`.devcontainer.json`) pre-installing: Python 3.11, Node 18, Poetry, pnpm, LangChain, LangGraph, LiteLLM, LangSmith SDK |
| 0.4  | **Set secrets template** (`.env.sample`) for `OPENAI_API_KEY`, `LANGCHAIN_API_KEY`, `LITESHLLM_SPEND_LIMIT`, etc. |
| 0.5  | **Init Git & CI** – GitHub Actions or Replit Nix workflow running `pytest` + `npm test` on every push |

### Output

`main` branch with scaffolding; CI green.

## Stage 1 – Data Contracts & Schemas (Schema-Agent)

1. **Define JobDescription JSON**

```jsonc
{
  "id": "uuid",
  "title": "string",
  "seniority": "string",
  "categories": {
    "responsibilities": ["..."],
    "required_skills": ["..."],
    "nice_to_have_skills": ["..."]
  },
  "metadata": {
    "salary_range": "string",
    "location": "string"
  }
}
```

1. **Define Candidate JSON (post-masking)**

```jsonc
{
  "id": "uuid",
  "position_id": "uuid",
  "masked": true,
  "raw_text": "string",
  "standardized": {
    "name": "[NAME]",
    "email": "[EMAIL]",
    "phone": "[PHONE]",
    "education": [{ "degree": "...", "institution": "...", "year": 2020 }],
    "experience_years": 7,
    "skills": ["python", "sql", ...],
    "certifications": ["..."]
  },
  "scores": { "overall": 0, "skills": 0, "experience": 0 },
  "interview_feedback": []   // filled later
}
```

1. **Commit `docs/schemas/`** with JSONSchema files → enable automatic validation via `pydantic` (backend) and `zod` (frontend).

## Stage 2 – Backend Core (Backend Agent)

### Inputs

Repo + Schemas + `.env`.

### Actions

| #    | Implementation Detail                                        |
| ---- | ------------------------------------------------------------ |
| 2.1  | **FastAPI app** (`backend/app/main.py`)                      |
| 2.2  | **/api/job/parse** – LangChain chain:  → Clarifying-Q prompt → structured JSON. Persist to MongoDB (`jobs` collection). |
| 2.3  | **/api/candidates/upload** – accept multi-part files; use `pypdf`, `docx2txt`, or `textract` → raw text. |
| 2.4  | **PII Masker** – regex + spaCy NER → replace tokens with `[NAME]` etc.; flag `masked=true`. |
| 2.5  | **Resume → JSON chain** – LiteLLM wrapper (e.g., `openai/gpt-4o`) called through LangChain; map to Candidate schema. |
| 2.6  | **Standardizer** – rule-based post-processor to normalize dates, skill synonyms, etc. |
| 2.7  | **/api/candidates/rank** – take `weights`, compute weighted cosine similarity (skills) + years delta scoring. Return sorted list. |
| 2.8  | **/api/candidates/{id}/feedback** – append structured feedback to candidate doc. |
| 2.9  | **LangSmith tracing** integrated in every chain (`langchain.callbacks.LangSmithCallbackHandler`). |
| 2.10 | **Unit tests** (`tests/backend/test_api.py`) covering happy-path & error cases. |

### Outputs

Running FastAPI server with Swagger docs at `/docs`; 90 % test coverage.

## Stage 3 – LLM & Agent Pipelines (LLM-Agent)

| Step | Action                                                       |
| ---- | ------------------------------------------------------------ |
| 3.1  | **Prompt library** (`backend/app/prompts/`) – system & few-shot templates for JD parsing, resume extraction, and masking justification. |
| 3.2  | **LangGraph graph**: nodes = { JD-Parser, Resume-Extractor, PII-Masker, Scorer }; edges reflect the data flow; allow future insertion of MoA “specialist” agents. |
| 3.3  | **LiteLLM config** – `litellm.router_config.json` with model priority list and spend ceiling. |
| 3.4  | **Evals** – LangSmith LLM Evals comparing extraction accuracy over ~30 sample PDFs & DOCX; target ≥ 0.85 F1. |
| 3.5  | **README update** – document how to run LangSmith playground and see traces. |

### Output

`backend/app/llm_pipeline.py` exposing `parse_job()`, `parse_resume()` functions used by Stage 2 endpoints.

## Stage 4 – Frontend Dashboard (Frontend Agent)

### Tech

React + Vite + TypeScript + Tailwind.

### Pages & Components

| Page                | Components                                                   |
| ------------------- | ------------------------------------------------------------ |
| **/dashboard**      | KPI Cards (open positions, candidates), ActivityFeed         |
| **/positions**      | PositionTable, “Create Position” modal (upload JD)           |
| **/positions/:id**  | CandidateTable (sortable by score), “Add Candidates” drop zone, WeightSlider panel |
| **/candidates/:id** | ResumeJSONViewer (masked JSON), FeedbackTimeline, FeedbackForm |

### Implementation Checklist

1. **API hooks** via `react-query` for `/api/*` endpoints.
2. **Auth stub** (future) – implement anonymous session for MVP, but wrap routes in `PrivateRoute` for easy swap-in.
3. **State management** – `zustand` store for weight sliders; on change, invoke `/rank`.
4. **Unit / component tests** with Vitest & React-Testing-Library.

### Output

`frontend/dist` static bundle; `npm run preview` shows functional recruiter dashboard.

## Stage 5 – Infra & Deployment (DevOps Agent)

| Resource        | Tooling                                                      |
| --------------- | ------------------------------------------------------------ |
| **Database**    | Docker Compose service for MongoDB 6; init script creates indexes on `candidate.position_id` |
| **Backend**     | Dockerfile → `gunicorn backend.app.main:app -k uvicorn.workers.UvicornWorker` |
| **Frontend**    | Nginx container serving `frontend/dist`                      |
| **Local stack** | `docker-compose up` spins MongoDB, backend, frontend         |
| **Cloud**       | Terraform module that:• deploys backend on AWS Fargate or Fly.io• MongoDB Atlas free tier• front on Vercel |

### CI/CD

*GitHub Actions* workflow:
 `push → build docker images → run tests → deploy to staging → Cypress e2e → promote to prod`.

## Stage 6 – QA & UAT (QA-Agent)

1. **Cypress scripts** upload sample JD + 5 fake resumes, adjust weights, verify ranking order matches oracle.
2. **Security checks** – ensure no PII in network responses (`masked === true`).
3. **Lighthouse audit** – performance ≥ 90, a11y ≥ 90.
4. **User-acceptance checklist** in `docs/UAT.md` for recruiter persona.

## Stage 7 – Mixture-of-Agents Proof-Point (Research-Agent)

*Optional, but scaffold now to future-proof.*

| Task | Detail                                                       |
| ---- | ------------------------------------------------------------ |
| 7.1  | Add `backend/app/agents/` folder; template “SkillExtractorAgent”, “CultureFitAgent”. |
| 7.2  | Update LangGraph to run them in parallel and aggregate votes (majority / weighted). |
| 7.3  | Log agent-level scores to LangSmith; expose in `/candidates/:id` under “Agent Opinions”. |

------

### Hand-Off Summary

1. **Architect Agent → Schema Agent**: repo & env ready.
2. **Schema Agent → Backend Agent**: JSONSchema files committed.
3. **Backend Agent → LLM Agent**: API stubs call chain placeholders; supply data contracts.
4. **LLM Agent → Backend Agent**: `llm_pipeline.py` implemented; backend tests updated.
5. **Backend Agent → Frontend Agent**: swagger.json generated; frontend uses it for type-safe hooks.
6. **Frontend & Backend Agents → DevOps Agent**: Dockerfiles & environment variables defined.
7. **All Agents → QA Agent**: staging environment deployed; run test suites.
