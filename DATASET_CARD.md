---
license: cc-by-nc-sa-4.0
task_categories:
  - text-generation
language:
  - en
tags:
  - benchmark
  - code-generation
  - prompt-consistency
  - ai-agents
  - coding-agents
  - evaluation
  - wittgenstein
  - semantic-invariance
  - caduceus
pretty_name: "WittgenSite: Prompt Consistency Benchmark"
size_categories:
  - n<1K
configs:
  - config_name: prompts
    data_files:
      - split: test
        path: PROMPTS.md
---

# WittgenSite: A Prompt Consistency Benchmark for AI Coding Agents

**Created by [Daniel Lougen](https://huggingface.co/DJLougen)**

Most benchmarks test whether an agent *can* complete a task. WittgenSite tests whether an agent produces **the same output regardless of how you ask**.

Inspired by Wittgenstein's insight that meaning is determined by use — this benchmark measures whether AI coding agents extract the same meaning from semantically equivalent prompts.

## Benchmark Design

One locked specification. 100 semantically different prompts. Same task every time. Score = consistency across runs.

The agent builds a 5-page SaaS website from `GOLDEN-SPEC.md` (vanilla HTML + Tailwind CDN). Each run uses a different prompt from `PROMPTS.md`. The outputs are compared for structural, textual, behavioral, and stylistic consistency.

## Prompt Categories

| Category | Prompts | Tests |
|----------|---------|-------|
| Direct & Minimal | 1-25 | Baseline consistency with simple instructions |
| Role / Persona Based | 26-50 | Whether persona framing ("you are a senior dev") causes drift |
| Verbose / Detailed | 51-75 | Whether extra detail causes additions or changes |
| Casual & Red Herring | 76-100 | Whether suggestive language ("make it premium") causes deviation |

## Scoring

### Per-Run: Spec Fidelity (7 dimensions)
| Dimension | Weight |
|-----------|--------|
| Structure & Files | 20% |
| Copy Fidelity | 15% |
| Theme System | 15% |
| Accessibility | 15% |
| Responsive Layout | 10% |
| Interactivity | 15% |
| Code Quality | 10% |

### Cross-Run: Consistency (5 dimensions)
| Dimension | Weight |
|-----------|--------|
| Structural Consistency | 30% |
| Copy Consistency | 25% |
| Behavioral Consistency | 20% |
| Style Consistency | 15% |
| Exact Match Rate | 10% |

### Interpretation
| Score | Meaning |
|-------|---------|
| 90-100 | Excellent — near-deterministic output |
| 75-89 | Good — minor cosmetic drift |
| 50-74 | Moderate — prompt wording affects output |
| < 50 | Poor — output depends heavily on phrasing |

## Preliminary Results

2 runs tested (Prompt #1 direct vs. Prompt #26 role-based), same model:
- Per-run spec fidelity: **100/100** and **99.5/100**
- Cross-run consistency: **31.9/100 (Poor)**

Both runs built functional websites that matched the spec individually. But the implementations were structurally different — different Tailwind classes, different JS patterns, different HTML nesting. Adding "You are a senior frontend developer" to the prompt changed the output significantly.

## Files

| File | Description |
|------|-------------|
| `GOLDEN-SPEC.md` | Locked website specification (source of truth) |
| `PROMPTS.md` | 100 semantically diverse prompts across 4 categories |
| `scoring/evaluate.py` | Per-run spec fidelity scorer |
| `scoring/consistency.py` | Cross-run consistency scorer (primary metric) |
| `task.json` | Caduceus benchmark metadata |

## Usage

```bash
# 1. Run agent with fresh context + golden spec + one prompt
# 2. Save output to runs/001/, runs/002/, etc.

# Score individual run
python scoring/evaluate.py runs/001/

# Score consistency across all runs
python scoring/consistency.py runs/
```

## Citation

```bibtex
@misc{lougen2026wittgensite,
  title={WittgenSite: A Prompt Consistency Benchmark for AI Coding Agents},
  author={Lougen, Daniel},
  year={2026},
  url={https://github.com/DJLougen/wittgensite},
  note={Inspired by Wittgenstein's philosophy of language}
}
```

## License

**CC BY-NC-SA 4.0** — Attribution required, non-commercial, share-alike.

Commercial use requires explicit written permission from [Daniel Lougen](https://x.com/DJLougen).

## Links

- **Leaderboard**: [DJLougen/Wittgensite-leaderboard](https://huggingface.co/spaces/DJLougen/Wittgensite-leaderboard)
- **GitHub**: [DJLougen/wittgensite](https://github.com/DJLougen/wittgensite)
- **Caduceus Task Page**: [djlougen.github.io/caduceus/tasks/T014](https://djlougen.github.io/caduceus/tasks/T014)
- **Author**: [@DJLougen](https://x.com/DJLougen)
