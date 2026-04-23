# Installation

## Prérequis

- Python 3.10+
- [Ollama](https://ollama.com) installé et démarré
- 16 Go de RAM minimum

## Étapes

### 1. Cloner le projet

```bash
git clone <repo-url>
cd atlas-ai
```

### 2. Environnement virtuel

```bash
python -m venv .venv
source .venv/bin/activate # Linux/Mac
.venv\Scripts\activate # Windows
```

### 3. Dépendances

```bash
pip install -e ".[dev]"
```

### 4. Modèle Ollama

```bash
ollama pull qwen3:8b
# Optionnel : créer le modèle Atlas personnalisé
ollama create atlas -f Modelfile
```

### 5. Lancer l'assistant

```bash
atlas-chat
# OU
python -m atlas.cli
```

## Vérification

```bash
pytest -v
```