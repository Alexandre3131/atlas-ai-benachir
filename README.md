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

**Définir votre stratégie de mémorisation**. Questions à trancher en équipe :
- Qu'est-ce qu'on stocke ? Chaque message ? Chaque paire Q/R ? Des résumés ?
Les paires question réponses paraît mieux, plus structuré et compréhensible qu'un message tout seul
Des résumés, ça demanderait probablement du traitement en plus?

- Quand on cherche en mémoire ? À chaque tour ? Seulement sur certains mots-clés ?
A chaque tour je pense en fonction du message de l'utilisateur

- Combien de souvenirs on injecte dans le prompt ? (Attention à la taille du contexte !)
Les plus importants et plus recents , donc peut etre le premier toujours et 2/3 autres donc 3/4 dans le prompt

- Comment on gère les doublons / informations contradictoires ?
On genere un hash en fonction du contenu, donc si le contenu est le meme ça ecrase simplement
si c'est contradictoire, on prend en compte le plus récent

