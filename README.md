# Atlas AI - Un assistant IA local

Assistant IA 100% local pour ATLAS Consulting. Aucune donnée envoyée dans le cloud.

## Lancer le projet

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
ollama serve
atlas-chat
```

## Stack
- LLM : Ollama (llama3.2:3b ou qwen3:4b)
- Mémoire : ChromaDB (vectorielle + persistante)
- Monitoring : JSONL + pandas
