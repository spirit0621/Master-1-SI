# 🪵 Journaux d'Événements Bruts TECHCORP (`events_raw.log`)

> **Document :** `events_raw.log`  
> **Source :** [etl/data_raw/events_raw.log](file:///c:/Users/alves/Desktop/Lyc%C3%A9e,%20bts%20,%20formation,%20master/CFA-insta/Master%201%20SI/TP/TPFINALE/etl/data_raw/events_raw.log)  
> **Rôle :** Journal technique multi-composants brut ingéré et parsé par le pipeline ETL [etl/clean_and_load.py](file:///c:/Users/alves/Desktop/Lyc%C3%A9e,%20bts%20,%20formation,%20master/CFA-insta/Master%201%20SI/TP/TPFINALE/etl/clean_and_load.py).

---

## 1. Tableau Chronologique des Événements Parsés

| Horodatage (UTC) | Niveau | Machine | Composant | Message de l'Événement |
| :--- | :--- | :--- | :--- | :--- |
| `2026-09-15 09:30:00` | `INFO` | `SRV-APP-01` | `systemd` | Started TECHCORP FastAPI Service. |
| `2026-09-15 09:45:12` | `INFO` | `SRV-DB-01` | `postgresql` | database system was shut down at 2026-09-15 09:44:00 UTC |
| `2026-09-15 09:45:15` | `INFO` | `SRV-DB-01` | `postgresql` | database system is ready to accept connections |
| `2026-09-15 10:00:10` | `INFO` | `SRV-WEB-01` | `nginx` | 192.168.56.1 - "GET / HTTP/1.1" 200 615 |
| `2026-09-15 10:03:41` | `ERROR` | `SRV-APP-01` | `uvicorn` | GET /tickets/open -> 500 Internal Server Error |
| `2026-09-15 10:03:42` | `ERROR` | `SRV-DB-01` | `postgresql` | password authentication failed for user techapp from 192.168.56.10 |
| `2026-09-15 10:03:45` | `WARN` | `SRV-APP-01` | `sqlalchemy` | DB connection pool exhausted, retrying in 5s |
| `2026-09-15 10:10:00` | `ERROR` | `SRV-APP-01` | `mcp_server` | MCP get_server_from_db -> connection failed: server closed the connection unexpectedly |
| `2026-09-15 10:10:05` | `WARN` | `SRV-DB-01` | `systemd` | postgresql.service: Main process exited, code=killed, status=9/KILL |
| `2026-09-15 10:10:06` | `ERROR` | `SRV-DB-01` | `systemd` | Failed to start PostgreSQL RDBMS. |
| `2026-09-15 10:12:00` | `INFO` | `SRV-DNS-01` | `named` | resolver priming query completed |

---

## 2. Contenu Brut d'Origine (`raw text`)

```text
2026-09-15 09:30:00 [INFO] SRV-APP-01 systemd: Started TECHCORP FastAPI Service.
2026-09-15 09:45:12 [INFO] SRV-DB-01 postgresql: database system was shut down at 2026-09-15 09:44:00 UTC
2026-09-15 09:45:15 [INFO] SRV-DB-01 postgresql: database system is ready to accept connections
2026-09-15 10:00:10 [INFO] SRV-WEB-01 nginx: 192.168.56.1 - "GET / HTTP/1.1" 200 615
2026-09-15 10:03:41 [ERROR] SRV-APP-01 uvicorn: GET /tickets/open -> 500 Internal Server Error
2026-09-15 10:03:42 [ERROR] SRV-DB-01 postgresql: password authentication failed for user techapp from 192.168.56.10
2026-09-15 10:03:45 [WARN] SRV-APP-01 sqlalchemy: DB connection pool exhausted, retrying in 5s
2026-09-15 10:10:00 [ERROR] SRV-APP-01 mcp_server: MCP get_server_from_db -> connection failed: server closed the connection unexpectedly
2026-09-15 10:10:05 [WARN] SRV-DB-01 systemd: postgresql.service: Main process exited, code=killed, status=9/KILL
2026-09-15 10:10:06 [ERROR] SRV-DB-01 systemd: Failed to start PostgreSQL RDBMS.
2026-09-15 10:12:00 [INFO] SRV-DNS-01 named: resolver priming query completed
```
