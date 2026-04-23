# Atlas AI - Un assistant IA local

Assistant IA 100% local pour ATLAS Consulting. Aucune donnée envoyée dans le cloud.

## Lancer le projet

Sur Linux :
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
ollama serve
atlas-chat
```

## Stack
- LLM : Ollama (qwen3:8b)
- Mémoire : ChromaDB
- Monitoring : JSONL + pandas
