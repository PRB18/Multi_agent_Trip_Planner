# Project Context — Multi-Agent Trip Planner

> This file exists so any new conversation can immediately pick up where we left off.
> Last updated: 2026-10-13

---

## What This Project Is

A trip planning system built in **plain Python + Google Gemini API** (no frameworks).
The goal is NOT just to plan trips — it's to **learn how multi-agent AI systems work from scratch**,
by building one manually before ever touching LangGraph or CrewAI.

The user is learning while building. They write the code. The assistant explains, guides, and reviews — does NOT write code unless explicitly asked.

---

## Teaching Approach (IMPORTANT)
- Take it slow. One concept at a time.
- User codes, assistant explains the "why" behind each piece.
- Ask the user questions to check understanding before moving forward.
- Use analogies (e.g. "one generalist vs 4 specialists").
- Stage-gating: don't move to the next stage until the current one runs and the user understands it.

---

## Tech Stack
- Language: Python 3.13
- LLM SDK: `google-genai` (`from google import genai`)
- Env management: `python-dotenv`
- API Key: `GEMINI_API_KEY` stored in `.env`
- Model used: `gemini-2.5-flash` with `temperature=0.2`
- No frameworks (LangGraph, CrewAI etc.) yet — intentionally

---

## Files in the Project

| File | Purpose |
|---|---|
| `llm_client.py` | Thin wrapper around Gemini API. Exports `ask_gemini(system_prompt, user_prompt)`. Shared by all agents. |
| `single_agent.py` | Stage 1 baseline. One function `build_prompt()`, one LLM call, full itinerary output. |
| `itinerary.md` | Saved output of `single_agent.py`. Serves as the benchmark to compare multi-agent output against. |
| `naive_multi_agent.py` | Stage 2: Research Agent (`research_agent`) finding structured options and unit prices. |
| `budget_agent.py` | Stage 2: Budget Agent (`budget_agent`) auditing costs and calculating bottom-up math. |
| `main_start.py` | Stage 2: Entry point chaining the agents sequentially. |
| `.env` | Contains `GEMINI_API_KEY=...` (never committed) |
| `.env.example` | Template showing which env vars are needed |
| `.gitignore` | Excludes `.env`, `__pycache__`, etc. |
| `README.md` | Project overview and setup instructions |
| `CONTEXT.md` | This file — cross-conversation continuity |

---

## The 4-Agent Design (the target architecture)

| Agent | Job |
|---|---|
| **Research Agent** | Finds trains, hotels, activities, food options based on destination + preferences. Returns raw options with unit prices — does NOT plan or budget. (Built!) |
| **Budget Agent** | Takes Research's picks. Checks each one against the per-person budget. Flags what's too expensive. Does bottom-up math. (Built!) |
| **Logistics Agent** | Takes Budget-approved picks. Sequences them into a realistic day-by-day plan. Enforces geographic clustering, travel time realism. (Next!) |
| **Coordinator** | The orchestrator. Calls agents in order. When Budget rejects a Research pick, sends it back to Research to revise. Capped at 3 retries. |

---

## The 6-Stage Build Plan

| Stage | Status | Description |
|---|---|---|
| **1** | ✅ DONE | Single agent in `single_agent.py`. One prompt, one LLM call, full itinerary. Baseline saved to `itinerary.md`. |
| **2** | 🟡 IN PROGRESS | Split into 4 Python functions. Naive context passing. Research & Budget agents built and verified in `main_start.py`. Next: Logistics & Coordinator agents. |
| **3** | ⬜ | Log and inspect what each agent actually receives. Identify irrelevant info (Budget doesn't need travel times, Research doesn't need cost totals). |
| **4** | ⬜ | Design a shared context object (Python dict or small class). Each agent reads/writes only the fields it needs. This is the core learning stage. Integrate live search/tools. |
| **5** | ⬜ | Coordinator conflict loop: Budget rejects Research pick → Coordinator asks Research to revise → retry capped at 3 iterations. |
| **6** | ⬜ (Optional) | Re-implement in LangGraph or CrewAI. Compare what the framework does vs what you built manually. |

---

## Key Lessons Learned So Far (Stage 1)

### Why a single prompt fails at scale:
- **Day count drift**: LLM counted overnight transit as extra days (Day 0 → Day 5 instead of Day 1 → Day 4).
- **Preference overrides**: Asked for Sleeper (SL) train, got AC 3-Tier because LLM has a comfort bias.
- **Fake math**: Budget table summed to exactly ₹15,000 because model worked backward from the cap, not bottom-up from real costs.
- **No geographic realism**: Scheduled Old Goa → Palolem (2hr each way) with a 4:30 PM start and 8 PM return — impossible in traffic.
- **Hallucinated prices**: All fares and Airbnb rates were plausible-sounding guesses, not real benchmarks.

### Fixes applied to `single_agent.py`:
- `temperature=0.2` on the LLM call to reduce hallucinations.
- Explicit rules in system prompt: strict day count, SL class only, bottom-up math, geographic clustering, seasonal awareness.
- Python-side budget multiplication (not delegated to LLM).
- Structured output format demanded: Itinerary + Budget Table + Verification Audit.
- Windows UTF-8 encoding fix for ₹ symbol (`sys.stdout.reconfigure(encoding='utf-8')`).
- Output saved to `itinerary.md` automatically.

---

## Stage 2 — What to Build Next (`naive_multi_agent.py`)

### Concept
4 functions called in sequence. Each function:
1. Gets a `system_prompt` defining its role.
2. Gets a `user_prompt` with the trip parameters + everything previous agents returned (raw text pasted in).
3. Calls `ask_gemini()` and returns a string.

### The deliberate pain to feel:
- Token count balloons with each agent (each one gets all previous text).
- Budget Agent receives travel-time descriptions it doesn't need.
- Logistics Agent receives cost arithmetic it doesn't need.
- By Stage 3, you'll print all of this and see the waste clearly.

### Open Question (answer before coding Stage 2):
> Should the Research Agent's output be raw prose, or a structured list?
> Why does that choice matter when Budget Agent has to read it?
> (User's answer to this will shape context object design in Stage 4.)

---

## How to Run

```powershell
# From project directory
python single_agent.py         # Stage 1 baseline
python naive_multi_agent.py    # Stage 2 (once built)
```

---

## GitHub
Repo: https://github.com/PRB18/Multi_agent_Trip_RAG
Branch: main
All files committed (except .env).
