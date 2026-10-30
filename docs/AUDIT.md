# Profile audit and verification

Reviewed 29 October 2026 against live GitHub source, not previous profile summaries.

## Starting point

The default branch already contained a partial redesign, merged in PR #1. It included a hero, terminal, short project table, external language widget, and daily city workflow. The city SVG was a setup placeholder. The generator lacked a saved data snapshot, strict data checks, empty day platforms, window details, retry/failure documentation, and tests. No project artwork or snake workflow existed.

This change preserves the identity, business email, verified contact URLs, experience statements, and useful workflow structure while completing the visual system and data pipeline. It does not modify featured application repositories.

## Featured source evidence

| Project | Inspected implementation | What the profile can accurately say |
| --- | --- | --- |
| [Vihaara](https://github.com/AishwaryaChandel27/Vihaara--AI-powered-mental-wellness-and-healthcare-app) | README, source tree, `client/src/lib/local-ai.ts`, worker and validation paths | React/TypeScript local-first wellbeing prototype; WebLLM in a worker, model lifecycle and fallback. Not clinical or production-readiness evidence. |
| [AURA](https://github.com/AishwaryaChandel27/AURA) | README, source tree, `agents/agent_controller.py` | Flask research prototype coordinating retrieval, summaries and hypothesis modules. TensorFlow files exist, but the profile does not claim validated ML performance. Some comments identify incomplete persistence. |
| [RAG-powered Assistant](https://github.com/AishwaryaChandel27/RAG-powered-assistant) | README, source tree, `rag_pipeline.py`, `vector_store.py` | Active pipeline uses `SimpleSearchEngine` and formatted retrieved text. FAISS/OpenAI vector code exists separately; it is not the active default. No claim that the current answer path uses an LLM. |
| [TasteTravel](https://github.com/AishwaryaChandel27/TasteTravel---Personalized-Cultural-Travel-Planner) | README, source tree, `server/services/ai-service.ts` | React/TypeScript/Express prototype with provider fallback logic. API integrations are implemented; availability and recommendation quality are not verified. |
| [Engineering Portfolio](https://github.com/AishwaryaChandel27/aishwarya-engineering-portfolio) | README and full source tree | Active static JavaScript/HTML/CSS portfolio; labeled fictional demos, original mascots, motion controls, deployment validator. Do not relabel it as a React project. |

Repository inventory informed selection; five focused projects communicate implementation more clearly than a long unranked list. Other public projects remain accessible through the repository index. Private repository names and source are excluded from published data.

## Claims and links

- Existing public profile and user brief support Bitwise ETL/data quality, AdventX Python backend, Capital Rush 15+ React/TypeScript pages, and third prize at a 2024 national-level hackathon. These are user-provided professional statements, not independently verified employment records. No new employment dates, tenure, performance metrics, or production claims were added.
- Snowflake is labeled coursework. Project technologies, experience, and learning are separated in the toolkit.
- `https://portfolio-one-alpha-13.vercel.app/` returned HTTP 200 and rendered the user's older public portfolio in the browser. It is distinct from the newer engineering-portfolio repository; the README says so.
- That older portfolio contains an outdated `yourusername/vihaara` link and older stack claims. These were not copied into this profile. Fixing that separate deployment is outside this profile change.
- AURA's own README contains a template clone URL. This profile links to the actual repository and controller instead.
- LinkedIn and email match the user-supplied brief and the rendered portfolio contact section; inbox delivery and LinkedIn authentication were not tested.
- Project repository and implementation links were confirmed through GitHub reads. No unverified project live-demo links are included.
- All README images are local. External badge/stat image services were removed, so a service outage cannot break the core profile. Native GitHub activity/achievements are linked instead of scraped or invented trophies.

## Verification record

- Actual public calendar fetched successfully: 369 continuous dates in the initial snapshot, 28 visible contributions. The committed data is inspectable and may be refreshed by Actions.
- Public repository snapshot fetched successfully: 22 owned public non-fork repositories in the initial snapshot. This is not the count of all accessible repositories.
- Eight unit tests pass: exact date/count rendering, zero platforms, invalid data rejection, GraphQL failures, public markup guardrails, streak boundaries, unchanged output, and preservation after network failure.
- Python compile checks, SVG XML/safety checks, image paths, accessible image labels, local Markdown links, and all three workflow YAML files are checked locally.
- Static assets and saved-data renders are deterministic; repeat generation must leave no Git diff.
- Read-only CI repeats generator tests and reproducibility checks on PRs. Publication jobs only stage named output paths.

Runtime checks and final browser findings are recorded in the pull request. Local tests alone do not prove that a repository policy permits workflow writes or that GitHub's scheduler will run on time. Full application tests and model inference for featured projects are outside this profile audit.
