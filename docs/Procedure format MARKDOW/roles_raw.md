# 👥 Matrice des Rôles et Droits Utilisateurs (`roles_raw.csv`)

> **Document :** `roles_raw.csv`  
> **Source :** [etl/data_raw/roles_raw.csv](file:///c:/Users/alves/Desktop/Lyc%C3%A9e,%20bts%20,%20formation,%20master/CFA-insta/Master%201%20SI/TP/TPFINALE/etl/data_raw/roles_raw.csv)  
> **Rôle :** Définition du contrôle d'accès basé sur les rôles (RBAC) pour l'exécution des Tools MCP et la confirmation humaine des actions sensibles.

---

## 1. Tableau des Rôles et Permissions (RBAC)

| Rôle (`role_name`) | Description Opérationnelle | Outils MCP Autorisés (`allowed_tools`) | Habilitation Action Sensible (`can_confirm_action`) |
| :--- | :--- | :--- | :---: |
| `support_n1` | Équipe Support Niveau 1 | `get_server_info`, `list_open_tickets`, `get_recent_events` | ❌ Non |
| `ops_system` | Équipe Exploitation Système | `get_server_info`, `list_open_tickets`, `get_recent_events`, `check_server_availability`, `get_last_service_check` | ❌ Non |
| `lead_ops` | Responsable Exploitation / Astreinte | `get_server_info`, `list_open_tickets`, `get_recent_events`, `check_server_availability`, `get_last_service_check`, `create_ticket` | ✅ Oui |
| `admin_si` | Administrateur Global | `*` (Tous les outils d'observation et de remédiation) | ✅ Oui |

---

## 2. Contenu Brut d'Origine (`raw text`)

```csv
role_name,description,allowed_tools,can_confirm_action
support_n1,Équipe Support Niveau 1,"get_server_info,list_open_tickets,get_recent_events",false
ops_system,Équipe Exploitation Système,"get_server_info,list_open_tickets,get_recent_events,check_server_availability,get_last_service_check",false
lead_ops,Responsable Exploitation / Astreinte,"get_server_info,list_open_tickets,get_recent_events,check_server_availability,get_last_service_check,create_ticket",true
admin_si,Administrateur Global,"*",true
```
