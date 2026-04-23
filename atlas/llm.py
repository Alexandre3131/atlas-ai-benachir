from typing import Generator

import httpx

OLLAMA_BASE_URL = "http://localhost:11434"


def chat(
    model: str,
    messages: list[dict],
    timeout: float = 60.0,
    stream: bool = False,
) -> str | Generator[str, None, None]:
    url = f"{OLLAMA_BASE_URL}/api/chat"
    payload = {
        "model": model,
        "messages": messages,
        "stream": stream,
        "think": False,
    }

    if stream:
        return _stream_response(url, payload, timeout)
    else:
        response = httpx.post(url, json=payload, timeout=timeout)
        response.raise_for_status()
        return response.json()["message"]["content"]


def _stream_response(
    url: str, payload: dict, timeout: float
) -> Generator[str, None, None]:
    with httpx.stream("POST", url, json=payload, timeout=timeout) as response:
        response.raise_for_status()
        for chunk in response.iter_lines():
            if chunk:
                import json

                data = json.loads(chunk)
                if token := data.get("message", {}).get("content"):
                    yield token
