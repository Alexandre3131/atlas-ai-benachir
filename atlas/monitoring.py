import json
import time
import uuid
from datetime import datetime, timezone
from functools import wraps
from pathlib import Path

LOG_PATH = Path("./data/traces.jsonl")


def traced(func):
    @wraps(func)
    def wrapper(model: str, messages: list, **kwargs):
        session_id = str(uuid.uuid4())[:8]
        start = time.perf_counter()

        result = func(model, messages, **kwargs)

        latency_ms = int((time.perf_counter() - start) * 1000)

        user_message = next(
            (m["content"] for m in reversed(messages) if m["role"] == "user"),
            "",
        )

        prompt_text = " ".join(m["content"] for m in messages)
        prompt_tokens = int(len(prompt_text.split()) * 1.3)
        completion_tokens = int(len(str(result).split()) * 1.3)

        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": session_id,
            "model": model,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "latency_ms": latency_ms,
            "user_message": user_message[:100],
            "assistant_message": str(result)[:200],
            "memory_hits": kwargs.get("memory_hits", 0),
            "guardrail_triggered": kwargs.get("guardrail_triggered", None),
        }

        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

        return result

    return wrapper
