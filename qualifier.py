from __future__ import annotations

import os
import re
from dataclasses import dataclass

import config
from gemini_client import generate

_CACHE = None

_INSTRUCTION_SUFFIX = """

---

You are evaluating exactly ONE thought (not a batch), sent in raw form on
Telegram. Apply the hard stops and the 8 metrics to it and return only the
single "Output format" block from the skill above for this one thought — no
intro, no ranked list at the end (that section is for batches only).
"""


@dataclass
class QualifierResult:
    raw_text: str
    verdict: str | None  # "QUALIFIES", "DISCARD", or None if unparseable
    score: int | None
    angle: str | None
    to_strengthen: str | None


def evaluate_thought(thought: str) -> QualifierResult:
    system_prompt = _load_prompt() + _INSTRUCTION_SUFFIX
    raw = generate(system_prompt, f"Thought:\n\n{thought}", temperature=0.2)
    return _parse(raw)


def _load_prompt():
    global _CACHE
    if _CACHE is None:
        path = os.path.join(config.QUALIFIER_SKILL_DIR, "SKILL.md")
        with open(path, "r", encoding="utf-8") as f:
            _CACHE = f.read()
    return _CACHE


def _parse(raw: str) -> QualifierResult:
    verdict_match = re.search(r"Verdict:\s*(QUALIFIES|DISCARD)", raw, re.IGNORECASE)
    score_match = re.search(r"Score:\s*(\d+)\s*/\s*8", raw)
    angle_match = re.search(r"Angle to write:\s*(.+)", raw)
    strengthen_match = re.search(r"To strengthen:\s*(.+)", raw)

    return QualifierResult(
        raw_text=raw,
        verdict=verdict_match.group(1).upper() if verdict_match else None,
        score=int(score_match.group(1)) if score_match else None,
        angle=angle_match.group(1).strip() if angle_match else None,
        to_strengthen=strengthen_match.group(1).strip() if strengthen_match else None,
    )
