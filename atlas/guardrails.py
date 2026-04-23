import re
from dataclasses import dataclass

from atlas.config import config

_PII_PATTERNS = [
    (r"FR\d{2}(?:[ ]?\d{4}){5}(?:[ ]?\d{2})", "[IBAN_MASQUÉ]"),
    (r"\b(?:\d{4}[ -]){3}\d{4}\b|\b\d{13,16}\b", "[CB_MASQUÉE]"),
    (r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}", "[EMAIL_MASQUÉ]"),
    (r"\b(?:0|\+33)[1-9](?:[ .-]?\d{2}){4}\b", "[TEL_MASQUÉ]"),
]

_BLOCKED_TOPICS = [
    r"\b(hack|exploit|injection sql|ddos|ransomware|malware)\b",
    r"\b(données personnelles concurrents|espionnage|surveillance illégale)\b",
]

_INJECTION_PATTERNS = [
    r"ignore (all )?(previous |prior )?(instructions?|prompt)",
    r"forget (everything|what you were told)",
    r"you are now",
    r"new persona",
    r"disregard (your )?(instructions?|rules?|guidelines?)",
    r"jailbreak",
    r"act as (if you (are|were)|a|an)",
]


@dataclass
class GuardResult:
    allowed: bool
    text: str
    reason: str = ""
    triggered_rule: str = ""


def mask_pii(text: str) -> str:
    if not config.guardrails.enable_pii_masking:
        return text
    for pattern, replacement in _PII_PATTERNS:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


def check_input(text: str) -> GuardResult:
    cfg = config.guardrails

    if cfg.enable_length_check and len(text) > cfg.max_input_chars:
        return GuardResult(
            allowed=False,
            text=text,
            reason=f"Requête trop longue ({cfg.max_input_chars} caractères max)",
            triggered_rule="length",
        )

    if cfg.enable_injection_check:
        for pattern in _INJECTION_PATTERNS:
            if re.search(pattern, text, flags=re.IGNORECASE):
                return GuardResult(
                    allowed=False,
                    text=text,
                    reason="Tentative de prompt injection détectée",
                    triggered_rule="injection",
                )

    if cfg.enable_blocked_topics:
        for pattern in _BLOCKED_TOPICS:
            if re.search(pattern, text, flags=re.IGNORECASE):
                return GuardResult(
                    allowed=False,
                    text=text,
                    reason="Sujet non autorisé",
                    triggered_rule="blocked_topic",
                )

    clean_text = mask_pii(text)
    triggered = "pii_masking" if clean_text != text else ""
    return GuardResult(allowed=True, text=clean_text, triggered_rule=triggered)
