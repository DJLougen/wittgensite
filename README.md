# T014 - Aether Notes: Golden Spec SaaS Website

**Caduceus Benchmark Task** | Domain: Web & API | Difficulty: Hard

## Task

Build a fully functional, self-contained 5-page SaaS marketing website from a locked golden specification. The agent must produce exactly the specified site using only vanilla HTML/CSS/JS + Tailwind CDN. Zero creative deviations allowed.

## What the Agent Must Do

1. Read `GOLDEN-SPEC.md` — the single source of truth
2. Create exactly 5 HTML files: `home.html`, `features.html`, `pricing.html`, `blog.html`, `app.html`
3. Implement all required features: dark/light mode, responsive design, WCAG 2.2 AA accessibility, reactive pricing toggle, testimonial carousel, blog search, and a mock dashboard app
4. Match all copy text, colors, animations, and behavior exactly as specified

## Evaluation

Run the scoring script against the agent's output directory:

```bash
python scoring/evaluate.py <path-to-output-directory>
```

### Scoring Dimensions (weighted)

| Dimension | Weight | What's Checked |
|-----------|--------|----------------|
| Structure & Files | 20% | Correct files, standalone, Tailwind CDN, no frameworks |
| Copy Fidelity | 15% | Exact headlines, button labels, header/footer text |
| Theme System | 15% | Dark/light toggle, localStorage, prefers-color-scheme |
| Accessibility | 15% | Semantic HTML, ARIA, focus rings, skip-to-main |
| Responsive Layout | 10% | Viewport meta, responsive classes, mobile menu |
| Interactivity | 15% | Carousel, accordion, pricing toggle, modals, search |
| Code Quality | 10% | Comments, reasonable structure, clean markup |

**Pass threshold: 70/100**

## Par Steps

25 steps expected for a competent agent.

## License

Apache 2.0
