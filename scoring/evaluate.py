#!/usr/bin/env python3
"""
Caduceus T014 – Aether Notes Golden Spec Evaluator
Scores an agent's submission against the locked specification.

Usage:
    python evaluate.py <path-to-aether-notes-directory>

Scoring dimensions (weighted):
    - Structure & Files   (20%)  — correct files, no extras, standalone
    - Copy Fidelity       (15%)  — exact headlines, labels, text
    - Theme System        (15%)  — dark/light toggle, persistence, transitions
    - Accessibility       (15%)  — semantic HTML, ARIA, focus, skip-link
    - Responsive Layout   (10%)  — mobile menu, grid breakpoints
    - Interactivity       (15%)  — carousel, accordion, pricing toggle, modals
    - Code Quality        (10%)  — no frameworks, clean markup, comments
"""

import os
import re
import sys
import json

REQUIRED_FILES = ["home.html", "features.html", "pricing.html", "blog.html", "app.html"]

REQUIRED_COPY = {
    "home.html": [
        "Your thoughts, supercharged by AI",
        "Aether Notes instantly organizes, summarizes, and connects your ideas",
        "The smartest notebook you'll ever use",
        "Get started free",
        "Watch 1:42 demo",
    ],
    "pricing.html": [
        "Free",
        "Pro",
        "Teams",
        "Save 20%",
    ],
    "blog.html": [
        "Load more",
    ],
    "app.html": [
        "New Note",
        "AI Summarize",
    ],
}

HEADER_ELEMENTS = [
    "Aether",
    "Home",
    "Features",
    "Pricing",
    "Blog",
    "App",
    "Log in",
    "Start for free",
]

FOOTER_ELEMENTS = [
    "2026 Aether Notes",
    "All rights reserved",
]

BANNED_IMPORTS = [
    r"from\s+['\"]react",
    r"import\s+.*from\s+['\"]vue",
    r"import\s+.*from\s+['\"]next",
    r"<script[^>]+src=['\"][^\"]*(?:react|vue|angular|jquery|alpine|htmx)",
]

ACCESSIBILITY_CHECKS = [
    (r"<nav[\s>]", "nav element"),
    (r"<main[\s>]", "main element"),
    (r"aria-label", "aria-label attributes"),
    (r"aria-expanded", "aria-expanded attributes"),
    (r"skip.*main|skip.*content", "skip-to-main link"),
    (r"focus:ring|focus-visible", "focus ring styles"),
]

THEME_CHECKS = [
    (r"localStorage", "localStorage persistence"),
    (r"prefers-color-scheme", "prefers-color-scheme detection"),
    (r'class\s*=\s*["\'].*dark', "dark class usage"),
    (r"dark:", "Tailwind dark: variants"),
]

INTERACTION_CHECKS = {
    "home.html": [
        (r"setInterval|auto.*slide|autoplay", "testimonial auto-slide"),
        (r"carousel|slider|testimonial", "carousel implementation"),
    ],
    "pricing.html": [
        (r"monthly|yearly|annual|toggle", "pricing toggle"),
        (r"Save\s*20%", "save badge"),
        (r"accordion|faq|collapse", "FAQ accordion"),
    ],
    "blog.html": [
        (r"search|filter", "search functionality"),
        (r"load\s*more|append|loadMore", "load more functionality"),
    ],
    "app.html": [
        (r"sidebar|collaps", "collapsible sidebar"),
        (r"modal|overlay|dialog", "note modal"),
        (r"spinner|loading|summariz", "AI summarize interaction"),
    ],
}


def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None


def score_structure(directory):
    """Check required files exist, no frameworks used."""
    score = 0
    max_score = 100
    details = []

    # File existence (50 pts)
    found = 0
    for fname in REQUIRED_FILES:
        path = os.path.join(directory, fname)
        if os.path.isfile(path):
            found += 1
        else:
            details.append(f"MISSING: {fname}")
    file_score = (found / len(REQUIRED_FILES)) * 50
    score += file_score

    # Standalone check — each file has <html>, <head>, <body> (20 pts)
    standalone = 0
    for fname in REQUIRED_FILES:
        content = read_file(os.path.join(directory, fname))
        if content and "<html" in content and "<head" in content and "<body" in content:
            standalone += 1
        elif content:
            details.append(f"NOT STANDALONE: {fname}")
    score += (standalone / max(len(REQUIRED_FILES), 1)) * 20

    # Tailwind CDN present (15 pts)
    tailwind_count = 0
    for fname in REQUIRED_FILES:
        content = read_file(os.path.join(directory, fname))
        if content and "cdn.tailwindcss.com" in content:
            tailwind_count += 1
    score += (tailwind_count / max(len(REQUIRED_FILES), 1)) * 15

    # No banned frameworks (15 pts)
    violations = 0
    for fname in REQUIRED_FILES:
        content = read_file(os.path.join(directory, fname))
        if content:
            for pattern in BANNED_IMPORTS:
                if re.search(pattern, content, re.IGNORECASE):
                    violations += 1
                    details.append(f"BANNED IMPORT in {fname}: {pattern}")
    score += 15 if violations == 0 else max(0, 15 - violations * 5)

    return min(score, max_score), details


def score_copy(directory):
    """Check exact copy text matches."""
    score = 0
    total_checks = 0
    matches = 0
    details = []

    for fname, phrases in REQUIRED_COPY.items():
        content = read_file(os.path.join(directory, fname))
        for phrase in phrases:
            total_checks += 1
            if content and phrase.lower() in content.lower():
                matches += 1
            else:
                details.append(f"COPY MISSING in {fname}: '{phrase}'")

    # Header/footer on all pages
    for fname in REQUIRED_FILES:
        content = read_file(os.path.join(directory, fname))
        for element in HEADER_ELEMENTS:
            total_checks += 1
            if content and element in content:
                matches += 1
            else:
                details.append(f"HEADER MISSING in {fname}: '{element}'")

        for element in FOOTER_ELEMENTS:
            total_checks += 1
            if content and element in content:
                matches += 1
            else:
                details.append(f"FOOTER MISSING in {fname}: '{element}'")

    score = (matches / max(total_checks, 1)) * 100
    return min(score, 100), details


def score_theme(directory):
    """Check theme system implementation."""
    score = 0
    details = []
    total = len(THEME_CHECKS) * len(REQUIRED_FILES)
    found = 0

    for fname in REQUIRED_FILES:
        content = read_file(os.path.join(directory, fname))
        if not content:
            continue
        for pattern, label in THEME_CHECKS:
            if re.search(pattern, content, re.IGNORECASE):
                found += 1
            else:
                details.append(f"THEME MISSING in {fname}: {label}")

    score = (found / max(total, 1)) * 100
    return min(score, 100), details


def score_accessibility(directory):
    """Check accessibility features."""
    total = len(ACCESSIBILITY_CHECKS) * len(REQUIRED_FILES)
    found = 0
    details = []

    for fname in REQUIRED_FILES:
        content = read_file(os.path.join(directory, fname))
        if not content:
            continue
        for pattern, label in ACCESSIBILITY_CHECKS:
            if re.search(pattern, content, re.IGNORECASE):
                found += 1
            else:
                details.append(f"A11Y MISSING in {fname}: {label}")

    score = (found / max(total, 1)) * 100
    return min(score, 100), details


def score_responsive(directory):
    """Check responsive design indicators."""
    total = 0
    found = 0
    details = []

    for fname in REQUIRED_FILES:
        content = read_file(os.path.join(directory, fname))
        if not content:
            continue

        # Viewport meta
        total += 1
        if 'viewport' in content:
            found += 1
        else:
            details.append(f"NO VIEWPORT in {fname}")

        # Responsive classes
        total += 1
        if re.search(r"\b(sm:|md:|lg:|xl:)", content):
            found += 1
        else:
            details.append(f"NO RESPONSIVE CLASSES in {fname}")

        # Mobile menu (hamburger)
        total += 1
        if re.search(r"hamburger|mobile.*menu|menu.*mobile|md:hidden|lg:hidden", content, re.IGNORECASE):
            found += 1

    score = (found / max(total, 1)) * 100
    return min(score, 100), details


def score_interactivity(directory):
    """Check page-specific interactive elements."""
    total = 0
    found = 0
    details = []

    for fname, checks in INTERACTION_CHECKS.items():
        content = read_file(os.path.join(directory, fname))
        for pattern, label in checks:
            total += 1
            if content and re.search(pattern, content, re.IGNORECASE):
                found += 1
            else:
                details.append(f"INTERACTION MISSING in {fname}: {label}")

    score = (found / max(total, 1)) * 100
    return min(score, 100), details


def score_code_quality(directory):
    """Check code quality indicators."""
    score = 70  # baseline
    details = []

    total_lines = 0
    comment_lines = 0

    for fname in REQUIRED_FILES:
        content = read_file(os.path.join(directory, fname))
        if not content:
            continue
        lines = content.split("\n")
        total_lines += len(lines)
        comment_lines += sum(1 for l in lines if "<!--" in l or "//" in l.strip()[:2] or "/*" in l)

    # Comments present (15 pts)
    if comment_lines > 5:
        score += 15
        details.append(f"Good: {comment_lines} comment lines found")
    elif comment_lines > 0:
        score += 8

    # Reasonable file sizes (15 pts)
    if total_lines > 100:
        score += 15
    elif total_lines > 50:
        score += 8

    return min(score, 100), details


def evaluate(directory):
    """Run full evaluation and return results."""
    weights = {
        "structure": 0.20,
        "copy": 0.15,
        "theme": 0.15,
        "accessibility": 0.15,
        "responsive": 0.10,
        "interactivity": 0.15,
        "code_quality": 0.10,
    }

    results = {}

    struct_score, struct_details = score_structure(directory)
    results["structure"] = {"score": round(struct_score, 1), "details": struct_details}

    copy_score, copy_details = score_copy(directory)
    results["copy"] = {"score": round(copy_score, 1), "details": copy_details}

    theme_score, theme_details = score_theme(directory)
    results["theme"] = {"score": round(theme_score, 1), "details": theme_details}

    a11y_score, a11y_details = score_accessibility(directory)
    results["accessibility"] = {"score": round(a11y_score, 1), "details": a11y_details}

    resp_score, resp_details = score_responsive(directory)
    results["responsive"] = {"score": round(resp_score, 1), "details": resp_details}

    inter_score, inter_details = score_interactivity(directory)
    results["interactivity"] = {"score": round(inter_score, 1), "details": inter_details}

    quality_score, quality_details = score_code_quality(directory)
    results["code_quality"] = {"score": round(quality_score, 1), "details": quality_details}

    overall = sum(
        results[dim]["score"] * weights[dim]
        for dim in weights
    )

    output = {
        "overall_score": round(overall, 1),
        "pass": overall >= 70,
        "dimensions": results,
    }

    return output


def main():
    if len(sys.argv) < 2:
        print("Usage: python evaluate.py <path-to-aether-notes-directory>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a directory")
        sys.exit(1)

    result = evaluate(directory)

    print("\n" + "=" * 60)
    print("  CADUCEUS T014 - Aether Notes Golden Spec Evaluation")
    print("=" * 60)

    for dim, data in result["dimensions"].items():
        status = "PASS" if data["score"] >= 70 else "FAIL"
        print(f"\n  {dim.upper():20s}  {data['score']:5.1f}/100  [{status}]")
        for detail in data["details"][:5]:  # show first 5 issues per dimension
            print(f"    - {detail}")
        remaining = len(data["details"]) - 5
        if remaining > 0:
            print(f"    ... and {remaining} more issues")

    print("\n" + "-" * 60)
    verdict = "PASS" if result["pass"] else "FAIL"
    print(f"  OVERALL: {result['overall_score']}/100  [{verdict}]")
    print(f"  Threshold: 70/100")
    print("=" * 60 + "\n")

    # Also write JSON output
    with open(os.path.join(directory, "evaluation_result.json"), "w") as f:
        json.dump(result, f, indent=2)
    print(f"  Full results written to {os.path.join(directory, 'evaluation_result.json')}\n")


if __name__ == "__main__":
    main()
