# T014 - WittgenSite: Prompt Consistency Benchmark

**Caduceus Benchmark Task** | Domain: Web & API | Difficulty: Hard

## What This Tests

Most benchmarks test whether an agent can complete a task. WittgenSite tests whether an agent produces **the same output regardless of how you ask**.

The agent builds a 5-page SaaS website from a locked golden specification. The same spec. 100 times. With 100 semantically different prompts. The score measures how consistent the outputs are across runs.

## How It Works

1. **Golden Spec** (`GOLDEN-SPEC.md`) — A locked, detailed specification for a 5-page vanilla HTML/Tailwind SaaS website called "Aether Notes"
2. **100 Prompts** (`PROMPTS.md`) — Semantically diverse ways to ask for the same thing: direct, role-based, verbose, casual, red-herring style
3. **Per-run evaluation** (`scoring/evaluate.py`) — Does each individual run match the spec?
4. **Consistency scoring** (`scoring/consistency.py`) — How similar are the outputs across all runs?

## Running the Benchmark

### Step 1: Run the agent N times with different prompts

For each run, give the agent fresh context + the golden spec + one prompt from PROMPTS.md. Save the output to a numbered directory:

```
runs/
├── 001/   (home.html, features.html, pricing.html, blog.html, app.html)
├── 002/
├── 003/
└── ...
```

### Step 2: Score individual runs against the spec

```bash
python scoring/evaluate.py runs/001/
python scoring/evaluate.py runs/002/
# ...
```

### Step 3: Score consistency across all runs

```bash
python scoring/consistency.py runs/
```

## Consistency Scoring Dimensions

| Dimension | Weight | What's Measured |
|-----------|--------|-----------------|
| Structural Consistency | 30% | Same HTML elements and nesting across runs |
| Copy Consistency | 25% | Identical visible text content |
| Behavioral Consistency | 20% | Same JavaScript logic and event handlers |
| Style Consistency | 15% | Same Tailwind classes and CSS |
| Exact Match Rate | 10% | Percentage of byte-identical outputs |

### Interpretation

| Score | Meaning |
|-------|---------|
| 90-100 | Excellent — near-deterministic output across prompt variations |
| 75-89 | Good — minor cosmetic drift but structurally consistent |
| 50-74 | Moderate — noticeable variation, prompt wording affects output |
| < 50 | Poor — significant inconsistency, prompt-dependent output |

## Prompt Categories

The 100 prompts are divided into 4 categories to test different failure modes:

- **1-25: Direct & Minimal** — Simple instructions, tests baseline consistency
- **26-50: Role / Persona Based** — "You are a senior developer..." etc., tests whether persona framing causes drift
- **51-75: Verbose / Detailed** — Long instructions restating the spec, tests whether extra detail causes additions
- **76-100: Casual & Red Herring** — "Make it feel premium", "focus on dark mode" — tests whether suggestive language causes deviation

## Files

| File | Purpose |
|------|---------|
| `GOLDEN-SPEC.md` | Locked specification — the source of truth |
| `PROMPTS.md` | 100 semantically diverse prompts |
| `scoring/evaluate.py` | Per-run spec fidelity scorer (7 dimensions) |
| `scoring/consistency.py` | Cross-run consistency scorer (5 dimensions) |
| `task.json` | Caduceus task metadata |

## License

Apache 2.0
