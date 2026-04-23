# Atlas AI - Un assistant IA local

Assistant IA 100% local pour ATLAS Consulting. Aucune donnée envoyée dans le cloud.

## Table des matières

- [Architecture](./docs/architecture.md)
- [Installation](./docs/installation.md)
- [Configuration](./docs/configuration.md)
- [Gouvernance & RGPD](./docs/governance.md)
- [Décisions d'architecture](./adr/001-choix-ollama.md)

## Stack technique

| Composant | Techno |
|---|---|
| LLM local | Ollama + qwen3:8b |
| Mémoire longue | ChromaDB |
| Config | YAML + Pydantic |
| Guardrails | Regex |
| Monitoring | JSONL local |
| CLI | Typer |

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