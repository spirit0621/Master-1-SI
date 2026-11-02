# 🔌 Historique des Mesures Réseau Brutes (`service_checks_raw.csv`)

> **Document :** `service_checks_raw.csv`  
> **Source :** [etl/data_raw/service_checks_raw.csv](file:///c:/Users/alves/Desktop/Lyc%C3%A9e,%20bts%20,%20formation,%20master/CFA-insta/Master%201%20SI/TP/TPFINALE/etl/data_raw/service_checks_raw.csv)  
> **Rôle :** Journal chronologique des sondes réseau TCP historiques utilisées pour tester l'état des services.

---

## 1. Tableau des Données Brutes

| Horodatage | Hostname brut | Port TCP | Résultat Sonde | Latence (ms) | Source de la Sonde |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `2026-09-15 09:50:00` | `SRV-APP-01` | 8000 | `SUCCESS` | 1.45 | `probe_internal` |
| `2026-09-15 10:00:00` | `srv-db-01` | 5432 | `SUCCESS` | 2.10 | `probe_internal` |
| `2026-09-15 10:05:00` | `SRV-WEB-01` | 80 | `SUCCESS` | 4.32 | `probe_external` |
| `2026-09-15 10:10:00` | `SRV-DB-01` | 5432 | `FAILED` | 0.00 | `probe_internal` |
| `2026-09-15 10:10:30` | `SRV-DB-01 ` | 5432 | `FAILED` | 0.00 | `probe_internal` |
| `2026-09-15 10:15:00` | `srv-dns-01` | 53 | `SUCCESS` | 1.12 | `probe_internal` |
| `2026-09-15 10:20:00` | `SRV-BK-01` | 9102 | `TIMEOUT` | 2000.00 | `probe_internal` |

---

## 2. Importance Opérationnelle & Corrélation

- À `10:00:00`, le port `5432` de `SRV-DB-01` répond avec succès (latence 2.10 ms).
- À `10:10:00`, la sonde échoue (`FAILED`).
- Cette mesure historique, couplée au test actif en temps réel de `check_server_availability`, permet de prouver la rupture de service survenue à 10h10 sans la confondre avec l'état statique de la CMDB (`inventory_status = UP`).
