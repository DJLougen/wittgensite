# Aether Notes -- Golden Spec v1.0 (Locked for Benchmark)

**Purpose**
This is the single source of truth for building a consistent, modern 5-page SaaS website. The model/agent must produce **exactly** the same website (visually, functionally, and in code structure) no matter how the request is rephrased. Zero creative changes to copy, colors, layout, or behavior.

**Project Goal for the Agent**
Build a fully functional, self-contained 5-page website that demonstrates 2026 modern web standards: dark/light mode with smooth transitions, excellent accessibility (WCAG 2.2 AA), responsive mobile-first design, purposeful micro-interactions, and reactive elements -- all using only the allowed tech stack.

## 1. Technical Constraints (Strict -- Do Not Deviate)

- **Exactly 5 HTML files**:
  - `home.html`
  - `features.html`
  - `pricing.html`
  - `blog.html`
  - `app.html`
- **Tech stack (mandatory)**:
  - Vanilla HTML5 + CSS + JavaScript only
  - Tailwind CSS **via CDN only**: `<script src="https://cdn.tailwindcss.com"></script>`
  - No React, Vue, Next.js, frameworks, build tools, or external JS libraries (except the Tailwind script)
  - All JavaScript must be vanilla and inline or in `<script>` tags at the bottom of each file
- Project structure (create exactly this):
  ```
  aether-notes/
  ├── home.html
  ├── features.html
  ├── pricing.html
  ├── blog.html
  ├── app.html
  ├── README.md          (include setup instructions)
  └── GOLDEN-SPEC.md     (this file -- do not modify)
  ```
- No folders for assets unless absolutely necessary (use inline SVGs or Tailwind gradients for visuals).
- All pages must be fully standalone and open correctly by double-clicking the HTML file.

## 2. Global Requirements (Apply to ALL Pages)

**Theme System**
- Full dark + light mode support.
- Toggle in header (sun/moon icon).
- Persist choice with `localStorage`.
- Respect `prefers-color-scheme` on first visit.
- Smooth 200ms color transitions (use Tailwind `dark:` variants + `class="dark"` on `<html>`).
- Support `prefers-reduced-motion` (disable or shorten animations).

**Color Palette**
- Light mode: bg-white, surface slate-50/100, text slate-900/600, border slate-200, accent #6366F1 (indigo-500)
- Dark mode: bg-slate-950, surface slate-800/900, text slate-50/300, border slate-700, accent #6366F1
- Use Tailwind classes or CSS custom properties for easy switching.

**Typography**
- Font stack: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif
- Fluid headings with `clamp()` (e.g. `text-4xl md:text-6xl`)
- Body: leading-relaxed, good contrast (>=4.5:1 in both modes)

**Shared Header (identical pixel-for-pixel and behavior on every page)**
- Sticky top-0, backdrop-blur-md, border-b
- Left: Logo "Aether" (text-2xl font-semibold tracking-tighter) + small inline SVG note icon with spark
- Center (md+): Navigation links in exact order: Home, Features, Pricing, Blog, App
  - Active page gets accent color + underline
- Right: Theme toggle (24x24 icon), "Log in" text link, "Start for free" primary button (accent bg, hover scale-105, 200ms transition)
- Mobile: Hamburger -> full-screen slide menu (300ms transform + opacity, backdrop blur, centered vertical links)

**Shared Footer (identical on every page)**
- Background slate-100 (light) / slate-900 (dark)
- 4-column grid on large screens: Product, Company, Resources, Legal
- Bottom bar: "(c) 2026 Aether Notes. All rights reserved." + placeholder social icons (inline SVGs)

**Accessibility (Mandatory -- Test with keyboard + screen reader simulation)**
- Semantic HTML (`<nav>`, `<main>`, `<section>`, headings hierarchy)
- ARIA labels, `aria-expanded`, roles for all interactive elements
- Visible focus rings (indigo accent)
- Skip-to-main link
- All placeholder visuals must have descriptive `alt` or `aria-label`

## 3. Page-Specific Requirements

**Home (home.html) -- Easiest**
- Hero: full viewport height, centered content, big headline "Your thoughts, supercharged by AI.", subheadline "Aether Notes instantly organizes, summarizes, and connects your ideas. The smartest notebook you'll ever use."
- Two CTAs: "Get started free" (primary) + "Watch 1:42 demo" (outline)
- Right side: Large illustrative placeholder (gradient + floating note cards with indigo glow using divs + shadows)
- Sections: Features (6-card grid with hover lift), How it Works (3-step), Testimonials (carousel with auto-slide every 5s, pause on hover, dots + arrows, 400ms smooth transition), Final CTA

**Features (features.html) -- Medium**
- Hero variant
- Detailed feature sections (use accordions or tabs)
- Mock screenshots as bordered divs with sample UI inside
- Comparison table

**Pricing (pricing.html) -- Medium-Hard (Reactive Test)**
- Toggle: Monthly / Yearly (segmented control or switch)
- On toggle: instantly update all prices + show "Save 20%" badge with subtle scale animation
- 3 tiers in responsive grid: Free, Pro (most popular badge with accent border), Teams
- Feature checklists with check icons
- FAQ accordion below (smooth max-height transition + chevron rotation, one open at a time)

**Blog (blog.html) -- Harder**
- Search bar (fake filtering or "no results" toast)
- Grid of blog post cards (placeholder images, titles, excerpts, read time, tags)
- Sidebar with categories and popular posts
- "Load more" button that appends cards with fade-in

**App (app.html) -- Hardest (Full Reactive Mock)**
- Mock dashboard interface:
  - Collapsible left sidebar (navigation items)
  - Top bar with "New Note" button
  - Split view: note list (clickable) + editor pane with sample content
  - "AI Summarize" button -> 300ms loading spinner then fade-in summary
  - Clicking notes opens modal (scale + fade animation)
- Theme toggle must also affect the mock app UI colors

## 4. Locked Interactions & Animations

- Theme toggle: 200ms transition
- Mobile menu: 300ms slide-in + backdrop
- FAQ accordion: smooth height + chevron rotate (200ms)
- Testimonials carousel: auto 5s, pause hover, smooth slide, dots/arrows
- Pricing toggle: instant price change + 150ms scale on price text
- Buttons/cards: hover scale-105 + 200ms transition
- Toasts/modals: slide/fade with backdrop blur
- All dynamic elements must be fully usable with keyboard and mouse

## 5. Acceptance Criteria (Agent Must Verify Before Finishing)

- All 5 pages open and look/function identically in both light and dark mode
- All links between pages work
- All interactive elements (toggle, accordion, carousel, modal, search, etc.) behave exactly as described
- No console errors
- Responsive on mobile, tablet, desktop
- Code is clean, well-commented where complex JS is used
- Matches this spec with zero deviations in copy text or core design
