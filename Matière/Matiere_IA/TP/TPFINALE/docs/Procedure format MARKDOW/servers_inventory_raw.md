# 🖥️ Inventaire Brut des Serveurs (`servers_inventory_raw.csv`)

> **Document :** `servers_inventory_raw.csv`  
> **Source :** [etl/data_raw/servers_inventory_raw.csv](file:///c:/Users/alves/Desktop/Lyc%C3%A9e,%20bts%20,%20formation,%20master/CFA-insta/Master%201%20SI/TP/TPFINALE/etl/data_raw/servers_inventory_raw.csv)  
> **Rôle :** Inventaire brut des serveurs TECHCORP avec anomalies pour ingestion et nettoyage par [etl/clean_and_load.py](file:///c:/Users/alves/Desktop/Lyc%C3%A9e,%20bts%20,%20formation,%20master/CFA-insta/Master%201%20SI/TP/TPFINALE/etl/clean_and_load.py).

---

## 1. Tableau des Données Brutes

| Hostname brut | IP Address | Rôle | OS | Service | Port | Statut brut | Env | Équipe |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `SRV-APP-01` | `192.168.56.10` | API | Ubuntu Server 24.04 | FastAPI | 8000 | UP | PROD | Application Team |
| `srv-db-01` | `192.168.56.20` | database | ubuntu 24.04 | postgresql | 5432 | active | production | DBA |
| `SRV-DB-01 ` | `192.168.56.20` | DB | Ubuntu | PostgreSQL | 5432 | UP | PROD | Database Team |
| `SRV-LEGACY-01` | `192.168.56.999` | Legacy | CentOS 7 | HTTP | 80 | UNKNOWN | PROD | Legacy Team |
| `SRV-API-02` | *(vide)* | API | Ubuntu | FastAPI | 8000 | UP | DEV | Development |
| `SRV-WEB-01` | `192.168.56.30` | Web | Debian 12 | Nginx | 80 | UP | PROD | Web Team |
| `srv-web-01` | `192.168.56.30` | web | debian 12 | nginx | 80 | up | prod | Web Team |
| `SRV-DNS-01 ` | `192.168.56.53` | DNS | Alpine Linux | named | 53 | UP | PROD | Network Team |
| `SRV-BK-01` | `192.168.56.40` | Backup | Ubuntu 22.04 | Bacula | 9102 | maintenance | STAGING | Infra Team |

---

## 2. Anomalies et Traitements dans l'ETL

1. **Doublons logiques :** `srv-db-01` et `SRV-DB-01 ` (avec espace) ➔ normalisation casse et suppression des espaces, fusion en un enregistrement unique PROD `SRV-DB-01`.
2. **Doublons logiques :** `srv-web-01` et `SRV-WEB-01` ➔ fusion en un enregistrement unique `SRV-WEB-01`.
3. **IP Invalide :** `SRV-LEGACY-01` avec `192.168.56.999` ➔ rejet automatique via validation regex IPv4 stricte (`0-255`), tracé dans `ingestion_audit`.
4. **Champ manquant :** `SRV-API-02` sans adresse IP ➔ rejet automatique, tracé dans `ingestion_audit`.
5. **Statuts hétérogènes :** `active`, `up`, `UP` ➔ normalisation en `UP` ; `maintenance` ➔ normalisation en `MAINTENANCE`.
