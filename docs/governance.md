# Gouvernance & RGPD

## Données collectées

Chaque interaction produit une trace dans `data/traces.jsonl` :

| Champ | Contenu | Sensibilité |
|---|---|---|
| `user_message` | 100 premiers caractères | Potentiellement personnel |
| `assistant_message` | 200 premiers caractères | Faible |
| `prompt_tokens` | Comptage estimé | Aucune |
| `latency_ms` | Durée en ms | Aucune |
| `guardrail_triggered` | Règle déclenchée | Faible |

## Politique de rétention

- Les traces sont conservées **localement** dans `data/traces.jsonl`
- **Aucune donnée n'est envoyée à un service externe** (pas d'OpenAI, pas de cloud)
- Purge manuelle : `rm data/traces.jsonl`
- Purge de la mémoire vectorielle : `rm -rf data/memory`

## Masquage PII automatique

Avant tout envoi au modèle, les données suivantes sont **automatiquement masquées** :

- Numéros de carte bancaire → `[CB_MASQUÉE]`
- Adresses email → `[EMAIL_MASQUÉ]`
- IBAN français → `[IBAN_MASQUÉ]`
- Numéros de téléphone français → `[TEL_MASQUÉ]`

## Conformité RGPD

- Traitement 100% local : pas de transfert hors UE
- Pas de données biométriques collectées
- Droit à l'effacement : `rm -rf data/` suffit