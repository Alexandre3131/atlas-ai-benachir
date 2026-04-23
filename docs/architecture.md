# Architecture

**Questions à trancher** dans votre équipe :
- Le system prompt doit-il vivre dans le Modelfile ou dans le code applicatif ? Pourquoi ?
Le system prompt vit dans `config/atlas.yaml` et est injecté par le CLI à chaque requête.
Le Modelfile définit uniquement les paramètres bas niveau (temperature, top_p, num_ctx).

- Quel impact si un utilisateur change la config YAML mais pas le Modelfile ?
Pas de conflit car le system prompt du Modelfile est écrasé par celui envoyé
dans le champ `system` des messages. Le Modelfile sert de fallback
pour les tests interactifs (`ollama run atlas`) uniquement.

- Votre CLI doit-elle pointer vers `atlas` ou vers `qwen3:8b` + system prompt côté code ?
Le modèle `atlas` (créé via Modelfile) embarque les bons paramètres.
Le system prompt reste côté code pour rester dynamique.