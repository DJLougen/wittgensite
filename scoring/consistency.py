#!/usr/bin/env python3
"""
WittgenSite Consistency Benchmark Scorer

Measures how consistent an agent's outputs are across multiple runs
of the same task with semantically different prompts.

Usage:
    python consistency.py <runs-directory>

Where <runs-directory> contains numbered subdirectories:
    runs/
    ├── 001/   (home.html, features.html, pricing.html, blog.html, app.html)
    ├── 002/
    ├── 003/
    └── ...

Scoring dimensions:
    - Structural Consistency (30%) — same HTML elements, same nesting
    - Copy Consistency      (25%) — identical text content across runs
    - Behavioral Consistency(20%) — same JS logic, event handlers, animations
    - Style Consistency     (15%) — same Tailwind classes, CSS properties
    - Spec Fidelity         (10%) — does each run match the golden spec
"""

import os
import re
import sys
import json
import hashlib
from collections import Counter, defaultdict
from difflib import SequenceMatcher

FILES = ["home.html", "features.html", "pricing.html", "blog.html", "app.html"]


def read_file(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception:
        return None


def normalize_whitespace(text):
    """Collapse whitespace for fairer comparison."""
    return re.sub(r"\s+", " ", text).strip()


def extract_text_content(html):
    """Extract visible text from HTML, stripping tags and scripts."""
    # Remove script and style blocks
    cleaned = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
    cleaned = re.sub(r"<style[^>]*>.*?</style>", "", cleaned, flags=re.DOTALL | re.IGNORECASE)
    # Remove tags
    cleaned = re.sub(r"<[^>]+>", " ", cleaned)
    # Decode entities
    cleaned = cleaned.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    cleaned = cleaned.replace("&quot;", '"').replace("&#39;", "'").replace("&apos;", "'")
    return normalize_whitespace(cleaned)


def extract_tags(html):
    """Extract ordered list of HTML tags."""
    return re.findall(r"<(\w+)[\s>]", html)


def extract_classes(html):
    """Extract all Tailwind/CSS classes used."""
    classes = re.findall(r'class\s*=\s*["\']([^"\']*)["\']', html)
    all_classes = []
    for cls_str in classes:
        all_classes.extend(cls_str.split())
    return sorted(all_classes)


def extract_js(html):
    """Extract JavaScript content."""
    scripts = re.findall(r"<script[^>]*>(.*?)</script>", html, re.DOTALL | re.IGNORECASE)
    return normalize_whitespace(" ".join(scripts))


def file_hash(content):
    """SHA256 of normalized content."""
    return hashlib.sha256(normalize_whitespace(content).encode()).hexdigest()


def similarity(a, b):
    """String similarity ratio 0-1."""
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


def pairwise_consistency(items):
    """Average pairwise similarity across a list of strings."""
    if len(items) < 2:
        return 1.0
    total = 0
    count = 0
    for i in range(len(items)):
        for j in range(i + 1, min(i + 10, len(items))):  # cap comparisons for speed
            total += similarity(items[i], items[j])
            count += 1
    return total / count if count > 0 else 1.0


def hash_consistency(hashes):
    """What fraction of runs produced the most common hash."""
    if not hashes:
        return 0.0
    counts = Counter(hashes)
    most_common = counts.most_common(1)[0][1]
    return most_common / len(hashes)


def load_runs(runs_dir):
    """Load all run directories."""
    runs = {}
    for entry in sorted(os.listdir(runs_dir)):
        run_path = os.path.join(runs_dir, entry)
        if os.path.isdir(run_path):
            run_data = {}
            for fname in FILES:
                content = read_file(os.path.join(run_path, fname))
                if content:
                    run_data[fname] = content
            if run_data:
                runs[entry] = run_data
    return runs


def score_structural(runs):
    """How consistent is the HTML structure across runs."""
    per_file = {}
    for fname in FILES:
        tag_lists = []
        for run_data in runs.values():
            if fname in run_data:
                tags = extract_tags(run_data[fname])
                tag_lists.append(" ".join(tags))
        per_file[fname] = pairwise_consistency(tag_lists) if tag_lists else 0.0

    avg = sum(per_file.values()) / max(len(per_file), 1)
    return round(avg * 100, 1), per_file


def score_copy(runs):
    """How consistent is the visible text content."""
    per_file = {}
    for fname in FILES:
        texts = []
        for run_data in runs.values():
            if fname in run_data:
                texts.append(extract_text_content(run_data[fname]))
        per_file[fname] = pairwise_consistency(texts) if texts else 0.0

    avg = sum(per_file.values()) / max(len(per_file), 1)
    return round(avg * 100, 1), per_file


def score_behavioral(runs):
    """How consistent is the JavaScript logic."""
    per_file = {}
    for fname in FILES:
        scripts = []
        for run_data in runs.values():
            if fname in run_data:
                scripts.append(extract_js(run_data[fname]))
        per_file[fname] = pairwise_consistency(scripts) if scripts else 0.0

    avg = sum(per_file.values()) / max(len(per_file), 1)
    return round(avg * 100, 1), per_file


def score_style(runs):
    """How consistent are the CSS classes used."""
    per_file = {}
    for fname in FILES:
        class_lists = []
        for run_data in runs.values():
            if fname in run_data:
                class_lists.append(" ".join(extract_classes(run_data[fname])))
        per_file[fname] = pairwise_consistency(class_lists) if class_lists else 0.0

    avg = sum(per_file.values()) / max(len(per_file), 1)
    return round(avg * 100, 1), per_file


def score_exact_match(runs):
    """What percentage of runs are byte-identical (after whitespace normalization)."""
    per_file = {}
    for fname in FILES:
        hashes = []
        for run_data in runs.values():
            if fname in run_data:
                hashes.append(file_hash(run_data[fname]))
        per_file[fname] = hash_consistency(hashes) if hashes else 0.0

    avg = sum(per_file.values()) / max(len(per_file), 1)
    return round(avg * 100, 1), per_file


def evaluate(runs_dir):
    runs = load_runs(runs_dir)
    n_runs = len(runs)

    if n_runs < 2:
        print(f"Error: Need at least 2 runs to measure consistency. Found {n_runs}.")
        sys.exit(1)

    weights = {
        "structural": 0.30,
        "copy": 0.25,
        "behavioral": 0.20,
        "style": 0.15,
        "exact_match": 0.10,
    }

    results = {}

    struct_score, struct_detail = score_structural(runs)
    results["structural"] = {"score": struct_score, "per_file": {k: round(v * 100, 1) for k, v in struct_detail.items()}}

    copy_score, copy_detail = score_copy(runs)
    results["copy"] = {"score": copy_score, "per_file": {k: round(v * 100, 1) for k, v in copy_detail.items()}}

    behav_score, behav_detail = score_behavioral(runs)
    results["behavioral"] = {"score": behav_score, "per_file": {k: round(v * 100, 1) for k, v in behav_detail.items()}}

    style_score, style_detail = score_style(runs)
    results["style"] = {"score": style_score, "per_file": {k: round(v * 100, 1) for k, v in style_detail.items()}}

    exact_score, exact_detail = score_exact_match(runs)
    results["exact_match"] = {"score": exact_score, "per_file": {k: round(v * 100, 1) for k, v in exact_detail.items()}}

    overall = sum(results[dim]["score"] * weights[dim] for dim in weights)

    output = {
        "overall_consistency": round(overall, 1),
        "total_runs": n_runs,
        "dimensions": results,
        "interpretation": {
            "90-100": "Excellent — near-deterministic output across prompt variations",
            "75-89": "Good — minor cosmetic drift but structurally consistent",
            "50-74": "Moderate — noticeable variation, prompt wording affects output",
            "below_50": "Poor — significant inconsistency, output depends heavily on prompt phrasing",
        },
    }

    return output


def main():
    if len(sys.argv) < 2:
        print("Usage: python consistency.py <runs-directory>")
        print()
        print("Directory structure:")
        print("  runs/")
        print("  ├── 001/  (home.html, features.html, ...)")
        print("  ├── 002/")
        print("  └── ...")
        sys.exit(1)

    runs_dir = sys.argv[1]
    if not os.path.isdir(runs_dir):
        print(f"Error: '{runs_dir}' is not a directory")
        sys.exit(1)

    result = evaluate(runs_dir)

    print()
    print("=" * 64)
    print("  WITTGENSITE CONSISTENCY BENCHMARK")
    print(f"  {result['total_runs']} runs analyzed")
    print("=" * 64)

    for dim, data in result["dimensions"].items():
        print(f"\n  {dim.upper():20s}  {data['score']:5.1f}/100")
        for fname, fscore in data["per_file"].items():
            bar = "#" * int(fscore / 5) + "." * (20 - int(fscore / 5))
            print(f"    {fname:20s}  [{bar}] {fscore:5.1f}%")

    print()
    print("-" * 64)
    print(f"  OVERALL CONSISTENCY: {result['overall_consistency']}/100")
    print()
    for bracket, desc in result["interpretation"].items():
        marker = " <<" if bracket != "below_50" and result["overall_consistency"] >= float(bracket.split("-")[0]) else ""
        if bracket == "below_50" and result["overall_consistency"] < 50:
            marker = " <<"
        print(f"    {bracket:>8s}: {desc}{marker}")
    print("=" * 64)

    out_path = os.path.join(runs_dir, "consistency_report.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\n  Full report: {out_path}\n")


if __name__ == "__main__":
    main()
