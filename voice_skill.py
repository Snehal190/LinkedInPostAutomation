import os

import config

_CACHE = None


def load_voice_prompt():
    """Concatenate the Meera Pillai voice skill files into one system prompt.

    Cached in-process since the files don't change during a run.
    """
    global _CACHE
    if _CACHE is not None:
        return _CACHE

    skill_md = _read(os.path.join(config.SKILL_DIR, "SKILL.md"))
    brand_facts = _read(
        os.path.join(config.SKILL_DIR, "references", "brand-facts.md")
    )
    voice_exemplars = _read(
        os.path.join(config.SKILL_DIR, "references", "voice-exemplars.md")
    )

    _CACHE = (
        skill_md
        + "\n\n---\n\n"
        + brand_facts
        + "\n\n---\n\n"
        + voice_exemplars
    )
    return _CACHE


def _read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
