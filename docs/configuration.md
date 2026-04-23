# Configuration

Toute la configuration vit dans `config/atlas.yaml`.
Aucune modification de code n'est nécessaire.

## Options disponibles

### Modèle

| Clé | Défaut | Description |
|---|---|---|
| `model.name` | `qwen3:8b` | Nom du modèle Ollama |
| `model.temperature` | `0.3` | Créativité |
| `model.top_p` | `0.9` | Diversité des tokens candidats |
| `model.num_ctx` | `4096` | Taille de la fenêtre de contexte |

### Persona

| Clé | Description |
|---|---|
| `persona.name` | Nom affiché de l'assistant |
| `persona.system_prompt` | Instructions de comportement |

### Mémoire

| Clé | Défaut | Description |
|---|---|---|
| `memory.top_k` | `5` | Nb de souvenirs injectés par requête |
| `memory.min_similarity` | `0.7` | Seuil de pertinence |

### Guardrails

| Clé | Défaut | Description |
|---|---|---|
| `guardrails.enabled` | `true` | Active/désactive tous les guardrails |
| `guardrails.max_input_chars` | `4000` | Longueur max d'une requête |
| `guardrails.blocked_topics` | `[]` | Liste de sujets interdits |

## Validation

Au démarrage, Pydantic valide le fichier et affiche une erreur explicite
si une valeur est invalide (ex: `temperature` hors de `[0, 2]`).