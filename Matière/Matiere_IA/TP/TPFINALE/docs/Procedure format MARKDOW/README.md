# 📚 Référentiel Markdown des Données Brutes & Procédures TECHCORP

> **Dossier :** `docs/format texte, MARKDOW/`  
> **Objectif :** Présenter sous forme structurée, lisible et documentée l'intégralité des jeux de données brutes, journaux d'événements et procédures d'exploitation du système d'information TECHCORP.  
> **Traçabilité :** Ces fichiers constituent la transcription fidèle en Markdown des fichiers bruts situés dans `etl/data_raw/` et `procedures/`.

---

## 📑 Index des Fichiers Disponibles

| Fichier Markdown | Fichier Source Brut | Rôle dans le Projet TECHCORP | Table / Ressource Associée |
| :--- | :--- | :--- | :--- |
| [servers_inventory_raw.md](file:///c:/Users/alves/Desktop/Lyc%C3%A9e,%20bts%20,%20formation,%20master/CFA-insta/Master%201%20SI/TP/TPFINALE/docs/format%20texte,%20MARKDOW/servers_inventory_raw.md) | `etl/data_raw/servers_inventory_raw.csv` | Inventaire brut des serveurs (doublons, IP invalide `999`, champs vides) | `servers`, `ingestion_audit` |
| [tickets_raw.md](file:///c:/Users/alves/Desktop/Lyc%C3%A9e,%20bts%20,%20formation,%20master/CFA-insta/Master%201%20SI/TP/TPFINALE/docs/format%20texte,%20MARKDOW/tickets_raw.md) | `etl/data_raw/tickets_raw.json` | Tickets d'incidents bruts (anomalies de date, casse, ticket #112 incomplet) | `tickets`, `ingestion_audit` |
| [events_raw.md](file:///c:/Users/alves/Desktop/Lyc%C3%A9e,%20bts%20,%20formation,%20master/CFA-insta/Master%201%20SI/TP/TPFINALE/docs/format%20texte,%20MARKDOW/events_raw.md) | `etl/data_raw/events_raw.log` | Journal chronologique multi-systèmes (panne en chaîne à 10:03) | `events` |
| [service_checks_raw.md](file:///c:/Users/alves/Desktop/Lyc%C3%A9e,%20bts%20,%20formation,%20master/CFA-insta/Master%201%20SI/TP/TPFINALE/docs/format%20texte,%20MARKDOW/service_checks_raw.md) | `etl/data_raw/service_checks_raw.csv` | Historique des sondes réseau TCP (passage à FAILED à 10:10) | `service_checks` |
| [roles_raw.md](file:///c:/Users/alves/Desktop/Lyc%C3%A9e,%20bts%20,%20formation,%20master/CFA-insta/Master%201%20SI/TP/TPFINALE/docs/format%20texte,%20MARKDOW/roles_raw.md) | `etl/data_raw/roles_raw.csv` | Matrice RBAC des rôles et autorisations pour les Tools MCP | `roles` |
| [procedure_dns.md](file:///c:/Users/alves/Desktop/Lyc%C3%A9e,%20bts%20,%20formation,%20master/CFA-insta/Master%201%20SI/TP/TPFINALE/docs/format%20texte,%20MARKDOW/procedure_dns.md) | `procedures/procedure_dns.txt` | Procédure opérationnelle d'incident DNS critique (`PROC-NET-DNS-001`) | Resource `procedure://dns` |
| [procedure_incidents.md](file:///c:/Users/alves/Desktop/Lyc%C3%A9e,%20bts%20,%20formation,%20master/CFA-insta/Master%201%20SI/TP/TPFINALE/docs/format%20texte,%20MARKDOW/procedure_incidents.md) | `procedures/procedure_incidents.txt` | Procédure générale de gestion des priorités et arbitrage d'état | Resource `procedure://incidents` |
| [procedures_exploitation.md](file:///c:/Users/alves/Desktop/Lyc%C3%A9e,%20bts%20,%20formation,%20master/CFA-insta/Master%201%20SI/TP/TPFINALE/docs/format%20texte,%20MARKDOW/procedures_exploitation.md) | `etl/data_raw/procedures_exploitation.txt` | Fiche de synthèse brute des consignes d'exploitation DNS et BDD | Ingestion documentaire |

---

## 🔍 Pourquoi ce format Markdown ?

1. **Lisibilité Immédiate :** Permet à l'évaluateur ou au jury de consulter directement les jeux d'essai sans devoir ouvrir des fichiers bruts hétérogènes (CSV, JSON, LOG).
2. **Explication des Pièges & Anomalies :** Chaque document liste en Section 2 les anomalies introduites volontairement par le sujet d'examen et les règles de nettoyage appliquées par l'ETL (`etl/clean_and_load.py`).
3. **Traçabilité des Tests :** Sert de base de référence pour vérifier la bonne insertion dans PostgreSQL et le comportement attendu des 6 Tools MCP.
