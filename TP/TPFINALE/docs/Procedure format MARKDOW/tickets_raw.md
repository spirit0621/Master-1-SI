# 🎫 Tickets d'Incidents Bruts (`tickets_raw.json`)

> **Document :** `tickets_raw.json`  
> **Source :** [etl/data_raw/tickets_raw.json](file:///c:/Users/alves/Desktop/Lyc%C3%A9e,%20bts%20,%20formation,%20master/CFA-insta/Master%201%20SI/TP/TPFINALE/etl/data_raw/tickets_raw.json)  
> **Rôle :** Fichier JSON brut d'incidents contenant des anomalies de dates, de priorités et d'intégrité référentielle pour l'ETL.

---

## 1. Tableau des Données Brutes

| ID | Titre de l'Incident | Hostname brut | Priorité brute | Statut brut | Horodatage brut | Description |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| `111` | DNS intermittence | `srv-dns-01 ` | `CRITIQUE` | `open` | `2026-09-15T11:18:00` | Latence anormale et pertes de paquets. |
| `112` | Incident incomplet | *(vide)* | *(vide)* | `OPEN` | `15/09/2026 12:00:00` | Signalement sans machine renseignée. |
| `113` | Erreur récurrente de connexion DB | `SRV-DB-01` | `CRITICAL` | `open` | `2026-09-15T10:05:00` | Échec de connexion PostgreSQL depuis SRV-APP-01. |
| `114` | Certificat SSL bientôt expiré | `SRV-WEB-01` | `LOW` | `closed` | `2026-09-10T08:30:00` | Renouvellement effectué sur Nginx. |
| `115` | Dégradation performances API | `SRV-APP-01` | `high` | `open` | `2026-09-15T10:15:00` | Temps de réponse anormalement élevés sur /tickets/open. |
| `116` | Incident sur hôte fantôme | `SRV-UNKNOWN-99` | `MEDIUM` | `open` | `2026-09-14T14:20:00` | Machine inconnue dans l'inventaire CMDB. |

---

## 2. Anomalies et Traitements dans l'ETL

1. **Format de date hétérogène :** Ticket 112 au format français `15/09/2026 12:00:00` vs format ISO 8601 `2026-09-15T...`. Normalisation via parsing `datetime.strptime`.
2. **Priorités disparates :** `CRITIQUE` et `high` ➔ standardisation en `CRITICAL` et `HIGH`.
3. **Champs obligatoires manquants :** Ticket 112 sans `hostname` ni `priority` ➔ **rejeté** et consigné dans `ingestion_audit`.
4. **Hostname avec espace :** `srv-dns-01 ` ➔ `strip() + upper()` ➔ `SRV-DNS-01`.
5. **Intégrité référentielle :** Ticket 116 sur `SRV-UNKNOWN-99` (non présent dans la table `servers`) ➔ inséré avec avertissement d'audit.
