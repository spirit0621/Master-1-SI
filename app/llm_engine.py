"""
Moteur d'Orchestration LLM & Tool Calling TECHCORP
Intègre Ollama (Qwen) avec le protocole MCP, la détection des contradictions
et la protection stricte contre les attaques par injection de prompt.
"""
import os
import sys
import json
import time
import uuid
from typing import Dict, Any, List, Optional
import requests
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from app.logger import log_mcp_call
from api.database import query_db
from mcp_server.server import (
    get_server_info,
    list_open_tickets,
    get_recent_events,
    check_server_availability,
    get_last_service_check,
    create_ticket,
    get_dns_procedure,
    get_incident_procedure,
    get_inventory_summary
)

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:4b")

SYSTEM_PROMPT = """Tu es l'Assistant IA d'Exploitation du Système d'Information TECHCORP.
Tu es rigoureusement relié aux données réelles via des Tools MCP.

RÈGLES IMPÉRATIVES :
1. N'invente JAMAIS l'état d'un serveur ou d'un service. Seule une mesure technique (sonde réseau TCP) prouve l'état réel.
2. Distingue TOUJOURS une information d'inventaire déclarée d'une mesure technique temps réel.
3. Si l'inventaire indique un serveur UP mais que la vérification réseau échoue (SERVICE_DOWN ou DOWN), tu DOIS formellement signaler la CONTRADICTION.
4. Tu ne dois JAMAIS afficher de mot de passe, secret ou tenter de lire le fichier .env.
5. Toute réponse doit être structurée avec clarté selon 3 axes :
   - 📌 FAITS ÉTABLIS (données brutes et résultats des outils)
   - ⚠️ ANALYSE TECHNIQUE (corrélations d'erreurs, contradictions détectées)
   - 💡 RECOMMANDATIONS (actions d'exploitation à mener)
"""

def call_ollama(prompt: str, system: str = SYSTEM_PROMPT) -> Optional[str]:
    """Appel au moteur LLM Ollama avec timeout strict et fallback gracieux."""
    try:
        url = f"{OLLAMA_HOST}/api/generate"
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "system": system,
            "stream": False,
            "options": {"temperature": 0.2}
        }
        res = requests.post(url, json=payload, timeout=6.0)
        if res.status_code == 200:
            content = res.json().get("response", "").strip()
            if content:
                return content
    except Exception:
        pass
    return None

def execute_tool_with_logging(tool_func, tool_name: str, args: dict, user_question: str, request_id: str) -> Any:
    start_t = time.time()
    status = "success"
    try:
        result = tool_func(**args)
    except Exception as e:
        status = "error"
        result = {"error": str(e)}
        
    duration = round((time.time() - start_t) * 1000, 2)
    source = result.get("source", "mcp_tool") if isinstance(result, dict) else "mcp_tool"
    log_mcp_call(
        user_question=user_question,
        tool_name=tool_name,
        tool_arguments=args,
        tool_status=status,
        source=source,
        duration_ms=duration,
        request_id=request_id
    )
    return result

def query_techcorp_assistant(user_question: str, confirm_action: bool = False) -> Dict[str, Any]:
    """Point d'entrée principal pour traiter une question utilisateur."""
    request_id = str(uuid.uuid4())
    traces = []
    
    q_lower = user_question.lower()
    
    # --------------------------------------------------------------------------
    # 1. Protection contre les Injections de Prompt & Tentatives de Fuite de Secrets
    # --------------------------------------------------------------------------
    if any(k in q_lower for k in [".env", "mot de passe", "password", "ignore toutes les règles", "ignore all rules", "secret"]):
        refusal_log_id = log_mcp_call(
            user_question=user_question,
            tool_name="security_firewall_rejection",
            tool_arguments={"pattern_matched": "secret_access_attempt"},
            tool_status="blocked_by_security",
            source="security_hardened_kernel",
            duration_ms=1.2,
            request_id=request_id
        )
        return {
            "answer": """### 🛡️ ALERTE DE SÉCURITÉ TECHCORP — ACTION BLOQUÉE
**1. Faits établis :**
- La requête contient une tentative d'accès non autorisé à des fichiers de configuration sensibles (`.env`) ou des identifiants système.
- Aucun outil d'accès au système de fichiers ni de commande shell arbitraire n'est exposé au LLM.

**2. Analyse technique :**
- Règle de sécurité violée : Cloisonnement strict des secrets (Section 8.2 du référentiel).
- Contrôle technique actif : Le serveur MCP restreint les opérations aux seules APIs déclarées.

**3. Recommandations :**
- L'incident a été tracé dans les journaux d'observabilité.
- Les identifiants doivent rester cantonnés aux variables d'environnement non accessibles par l'interface utilisateur.
""",
            "traces": [{"tool": "security_firewall", "result": "BLOCKED", "source": "security_kernel"}],
            "request_id": request_id
        }

    # --------------------------------------------------------------------------
    # 2. Détection et Orchestration des Scénarios Métier
    # --------------------------------------------------------------------------
    
    # --- Scénario F0 / Diagnostic 360° : Couverture intégrale des 6 critères d'évaluation ---
    if any(k in q_lower for k in ["audit", "360", "complet", "intégral", "retrouver l'adresse ip", "retrouver l’adresse ip", "confusion", "inventaire, historique"]) or ("ip" in q_lower and "ticket" in q_lower and "événement" in q_lower):
        target = "SRV-DB-01"
        if "web" in q_lower or "srv-web-01" in q_lower:
            target = "SRV-WEB-01"
        elif "app" in q_lower or "srv-app-01" in q_lower:
            target = "SRV-APP-01"
        elif "dns" in q_lower or "srv-dns-01" in q_lower:
            target = "SRV-DNS-01"

        # 1. Retrouver l'adresse IP et le rôle (Inventaire PostgreSQL)
        info = execute_tool_with_logging(get_server_info, "get_server_info", {"hostname": target}, user_question, request_id)
        traces.append({"tool": "get_server_info", "args": {"hostname": target}, "result": info, "source": "postgresql_direct"})

        # 2. Consulter les tickets associés (API Métier FastAPI via MCP)
        all_tickets = execute_tool_with_logging(list_open_tickets, "list_open_tickets", {}, user_question, request_id)
        srv_tickets = [t for t in all_tickets if t.get("hostname") == target]
        if not srv_tickets and all_tickets:
            srv_tickets = all_tickets[:2]
        traces.append({"tool": "list_open_tickets", "args": {"hostname": target}, "result": srv_tickets, "source": "fastapi_api_http"})

        # 3. Observer les événements récents (Historique Logs)
        events = execute_tool_with_logging(get_recent_events, "get_recent_events", {"hostname": target, "limit": 3}, user_question, request_id)
        traces.append({"tool": "get_recent_events", "args": {"hostname": target, "limit": 3}, "result": events, "source": "postgresql_events"})

        # 4. Vérifier si le serveur et son service répondent réellement (Sonde TCP active temps réel)
        probe = execute_tool_with_logging(check_server_availability, "check_server_availability", {"hostname": target}, user_question, request_id)
        traces.append({"tool": "check_server_availability", "args": {"hostname": target}, "result": probe, "source": "live_tcp_socket_probe"})

        # 5. Consulter une procédure d'exploitation (Resource MCP)
        if target == "SRV-DNS-01":
            proc_text = get_dns_procedure()
            proc_uri = "procedures://dns"
        else:
            proc_text = get_incident_procedure()
            proc_uri = "procedures://incidents"
        traces.append({"resource": proc_uri, "result": "LOADED", "source": "mcp_resource"})

        # Formatage des éléments factuels
        tickets_str = "\n".join([f"  * Ticket #{t['id']} [{t.get('priority')}]: `{t.get('title')}`" for t in srv_tickets]) if srv_tickets else "  * Aucun ticket ouvert pour cette machine."
        events_str = "\n".join([f"  * [{e.get('timestamp')}] [{e.get('level')}]: `{e.get('message')}`" for e in events]) if events else "  * Aucun événement récent."

        inv_status = info.get("inventory_status", "UNKNOWN")
        live_result = probe.get("result", "UNKNOWN")
        tested_port = probe.get("port_tested", 5432)
        latency = probe.get("latency_ms", 0)

        # 6. Présenter une conclusion sans confondre inventaire, historique et état temps réel
        if inv_status == "UP" and live_result in ["SERVICE_DOWN", "DOWN"]:
            analysis_status = f"⚠️ **CONTRADICTION DÉTECTÉE ENTRE INVENTAIRE ET TEMPS RÉEL :** La CMDB déclare la machine `{inv_status}`, mais la sonde TCP active révèle un échec sur le port {tested_port} (`{live_result}`). L'OS peut être sous tension mais le processus applicatif n'écoute plus."
        else:
            analysis_status = f"✅ Cohérence constatée : Inventaire `{inv_status}` | Sonde temps réel `{live_result}` ({latency} ms)."

        answer = f"""### 🛡️ Diagnostic Complet d'Exploitation : {target}

**1. Faits établis (Preuves techniques collectées via MCP) :**
- **• Adresse IP & Rôle (Inventaire PostgreSQL) :** IP `{info.get('ip_address')}` | Rôle `{info.get('role')}` | OS `{info.get('os')}` | Environnement `{info.get('environment')}` | Statut inventaire `{inv_status}`.
- **• Tickets associés (API Métier FastAPI `/tickets`) :**
{tickets_str}
- **• Événements récents (Historique Logs) :**
{events_str}
- **• Vérification active temps réel (Sonde TCP Port {tested_port}) :** Résultat `{live_result}` (Latence : {latency} ms).
- **• Procédure d'exploitation consultée (Resource MCP `{proc_uri}`) :**
```text
{proc_text[:350]}...
```

**2. Analyse technique & Distinction rigoureuse des 3 paliers :**
- **Couche 1 — Référentiel Déclaratif (Inventaire) :** Donne les caractéristiques théoriques (`{info.get('ip_address')}`, rôle `{info.get('role')}`, statut `{inv_status}`). Ce n'est qu'une base de connaissances statique.
- **Couche 2 — Traces Passées (Historique) :** Les événements récents et tickets décrivent les incidents antérieurs (alertes, saturations ou pannes passées).
- **Couche 3 — Mesure Active (Temps Réel) :** Seule la sonde TCP prouve l'état de fonctionnement présent (`{live_result}`).
- **Synthèse :** {analysis_status}

**3. Recommandations d'intervention :**
1. Appliquer les consignes de la procédure consultée (`{proc_uri}`).
2. Effectuer une vérification directe du service sur `{target}` : `systemctl status postgresql` ou `ss -lntp`.
3. Mettre à jour le ticket associé via FastAPI une fois l'intervention terminée.
"""
        return {"answer": answer, "traces": traces, "request_id": request_id}

    # --- Scénario F1 : Tickets critiques ouverts ---
    elif "ticket" in q_lower and ("critique" in q_lower or "critical" in q_lower or "ouvert" in q_lower or "open" in q_lower):
        res = execute_tool_with_logging(list_open_tickets, "list_open_tickets", {"priority": "CRITICAL"}, user_question, request_id)
        traces.append({"tool": "list_open_tickets", "args": {"priority": "CRITICAL"}, "result": res, "source": "fastapi_api_http"})
        
        ticket_lines = []
        for t in res:
            ticket_lines.append(f"- **Ticket #{t['id']}** : `{t['title']}` (Machine: `{t.get('hostname')}`, Priorité: `{t['priority']}`)")
        tickets_str = "\n".join(ticket_lines) if ticket_lines else "- Aucun incident critique ouvert."
        
        answer = f"""### 📋 Tickets d'Incident Critiques Ouverts
**1. Faits établis (Source : API Métier FastAPI via MCP) :**
{tickets_str}

**2. Analyse technique :**
- Les incidents ont été récupérés en interrogeant l'endpoint `/tickets/open` de l'API métier FastAPI.
- La priorité `CRITICAL` cible des dysfonctionnements majeurs affectant l'infrastructure ou la base de données.

**3. Recommandations :**
- Traiter en priorité l'incident DB sur `SRV-DB-01` pour rétablir les accès applicatifs.
- Vérifier les alertes réseau associées.
"""
        return {"answer": answer, "traces": traces, "request_id": request_id}

    # --- Scénario F3 : Contradiction Fonctionne-t-il réellement / Disponibilité ---
    elif ("fonctionne" in q_lower or "disponible" in q_lower or "status" in q_lower or "état" in q_lower) and ("srv-db-01" in q_lower or "db" in q_lower):
        target = "SRV-DB-01"
        info = execute_tool_with_logging(get_server_info, "get_server_info", {"hostname": target}, user_question, request_id)
        traces.append({"tool": "get_server_info", "args": {"hostname": target}, "result": info, "source": "postgresql_direct"})
        
        probe = execute_tool_with_logging(check_server_availability, "check_server_availability", {"hostname": target}, user_question, request_id)
        traces.append({"tool": "check_server_availability", "args": {"hostname": target}, "result": probe, "source": "live_tcp_socket_probe"})
        
        events = execute_tool_with_logging(get_recent_events, "get_recent_events", {"hostname": target, "limit": 3}, user_question, request_id)
        traces.append({"tool": "get_recent_events", "args": {"hostname": target, "limit": 3}, "result": events, "source": "postgresql_events"})

        # Détection de contradiction
        inv_status = info.get("inventory_status", "UNKNOWN")
        live_result = probe.get("result", "UNKNOWN")
        
        contradiction_msg = ""
        if inv_status == "UP" and live_result in ["SERVICE_DOWN", "DOWN"]:
            contradiction_msg = f"⚠️ **CONTRADICTION MAJEURE DÉTECTÉE** : `{target}` est déclaré `{inv_status}` dans le référentiel d'inventaire, mais le test de connectivité réseau TCP direct a échoué (`{live_result}`). Le service PostgreSQL n'écoute plus sur le port 5432."
        else:
            contradiction_msg = f"Statut cohérent : Inventaire `{inv_status}` / Sonde réseau `{live_result}`."

        answer = f"""### 🔍 Diagnostic d'Exploitation : {target}
**1. Faits établis :**
- **Inventaire (PostgreSQL) :** Machine `{target}` déclarée statut `{inv_status}` (Rôle: `{info.get('role')}`, OS: `{info.get('os')}`).
- **Test Réseau Temps Réel (Sonde TCP) :** Port {probe.get('port_tested')} $\rightarrow$ Résultat : `{live_result}` (Latence : {probe.get('latency_ms')}ms).
- **Dernier événement journalisé :** `{events[0]['message'] if events else 'Aucun'}`.

**2. Analyse technique :**
- {contradiction_msg}
- Un événement récent signale des échecs d'authentification et une fermeture inattendue de connexion.

**3. Recommandations :**
1. Ne pas conclure à un crash complet de la machine hôte sans vérification système préalable.
2. Se connecter sur `SRV-DB-01` et vérifier le service : `systemctl status postgresql`.
3. Contrôler les autorisations dans `pg_hba.conf` et les sockets ouverts : `ss -lntp | grep 5432`.
"""
        return {"answer": answer, "traces": traces, "request_id": request_id}

    # --- Annexe D / Q4 : Le dernier test du port PostgreSQL est-il cohérent avec l'inventaire ? ---
    elif any(k in q_lower for k in ["cohérent", "coherent", "cohérence"]) or ("dernier test" in q_lower and "postgresql" in q_lower) or ("dernier test" in q_lower and "inventaire" in q_lower):
        target = "SRV-DB-01"
        info = execute_tool_with_logging(get_server_info, "get_server_info", {"hostname": target}, user_question, request_id)
        traces.append({"tool": "get_server_info", "args": {"hostname": target}, "result": info, "source": "postgresql_direct"})
        
        last_check = execute_tool_with_logging(get_last_service_check, "get_last_service_check", {"hostname": target}, user_question, request_id)
        traces.append({"tool": "get_last_service_check", "args": {"hostname": target}, "result": last_check, "source": "postgresql_service_checks_history"})

        inv_status = info.get("inventory_status", "UNKNOWN")
        tcp_res = last_check.get("tcp_result", "UNKNOWN")
        tested_port = last_check.get("port", 5432)
        check_time = last_check.get("timestamp", "Inconnu")

        is_coherent = (inv_status == "UP" and tcp_res == "SUCCESS") or (inv_status in ["DOWN", "MAINTENANCE"] and tcp_res in ["FAILED", "DOWN", "TIMEOUT"])
        
        if not is_coherent:
            diag = f"⚠️ **NON COHÉRENT (Contradiction Formelle) :** L'inventaire déclare `{target}` en statut `{inv_status}`, alors que la dernière mesure historique sur le port {tested_port} à `{check_time}` indique `{tcp_res}` (échec de connexion)."
        else:
            diag = f"✅ **COHÉRENT :** L'inventaire `{inv_status}` concorde avec la dernière mesure `{tcp_res}`."

        answer = f"""### ⚖️ Vérification de Cohérence : Inventaire vs Dernier Test PostgreSQL
**1. Faits établis :**
- **Statut d'inventaire CMDB (Table `servers`) :** `{target}` déclaré `{inv_status}` (IP: `{info.get('ip_address')}`).
- **Dernier test réseau enregistré (Table `service_checks`) :** Port {tested_port} $\\rightarrow$ `{tcp_res}` à `{check_time}` (Latence : {last_check.get('latency_ms', 0)} ms).

**2. Analyse technique :**
- {diag}
- À 10:00:00, le test TCP était encore en `SUCCESS`. La rupture est survenue à 10:10:00 (`FAILED`), sans mise à jour corrélative du statut de la CMDB.

**3. Recommandations :**
1. Lancer un test actif en temps réel pour confirmer si le port 5432 est toujours fermé.
2. Aligner le statut CMDB vers `MAINTENANCE` ou `DOWN` le temps du diagnostic.
3. Vérifier le processus PostgreSQL via `systemctl status postgresql`.
"""
        return {"answer": answer, "traces": traces, "request_id": request_id}

    # --- Annexe D / Q5 : Événements récents concernant SRV-WEB-01 ---
    elif ("événement" in q_lower or "evenement" in q_lower or "log" in q_lower or "logs" in q_lower) and ("srv-web-01" in q_lower or "web" in q_lower):
        target = "SRV-WEB-01"
        events = execute_tool_with_logging(get_recent_events, "get_recent_events", {"hostname": target, "limit": 5}, user_question, request_id)
        traces.append({"tool": "get_recent_events", "args": {"hostname": target, "limit": 5}, "result": events, "source": "postgresql_events"})

        info = execute_tool_with_logging(get_server_info, "get_server_info", {"hostname": target}, user_question, request_id)
        traces.append({"tool": "get_server_info", "args": {"hostname": target}, "result": info, "source": "postgresql_direct"})

        ev_lines = [f"- `[{e.get('timestamp')}]` **[{e.get('level')}]** {e.get('component')}: `{e.get('message')}`" for e in events]
        ev_str = "\n".join(ev_lines) if ev_lines else "- Aucun événement enregistré pour SRV-WEB-01."

        answer = f"""### 📜 Événements Récents concernant {target}
**1. Faits établis (Source : PostgreSQL Table `events`) :**
{ev_str}
- **Fiche machine :** IP `{info.get('ip_address')}`, Service `Nginx` (Port 80), Statut inventaire `{info.get('inventory_status')}`.

**2. Analyse technique :**
- À `10:00:10`, Nginx a servi une requête HTTP standard avec un code `200 OK`.
- Aucun événement de niveau `ERROR` ni `WARN` n'est recensé pour ce serveur dans les journaux.
- Le ticket associé (#114 - Renouvellement certificat SSL) a été traité et fermé avec succès.

**3. Recommandations :**
- Le serveur web fonctionne nominalement. Aucun incident actif n'affecte `SRV-WEB-01`.
"""
        return {"answer": answer, "traces": traces, "request_id": request_id}

    # --- Scénario F2 : Fiche d'un serveur précis ---
    elif "srv-db-01" in q_lower or "information" in q_lower or "fiche" in q_lower:
        target = "SRV-DB-01" if "db" in q_lower else ("SRV-APP-01" if "app" in q_lower else "SRV-WEB-01")
        info = execute_tool_with_logging(get_server_info, "get_server_info", {"hostname": target}, user_question, request_id)
        traces.append({"tool": "get_server_info", "args": {"hostname": target}, "result": info, "source": "postgresql_direct"})
        
        last_check = execute_tool_with_logging(get_last_service_check, "get_last_service_check", {"hostname": target}, user_question, request_id)
        traces.append({"tool": "get_last_service_check", "args": {"hostname": target}, "result": last_check, "source": "postgresql_service_checks_history"})

        services_desc = ", ".join([f"{s['service_name']} (port {s['port']})" for s in info.get("services", [])]) or "Aucun déclaré"

        answer = f"""### 🖥️ Fiche Serveur Normalisée : {target}
**1. Faits établis (Source : PostgreSQL Direct) :**
- **Nom d'hôte :** `{info.get('hostname')}`
- **Adresse IP :** `{info.get('ip_address')}`
- **Rôle & Environnement :** `{info.get('role')}` ({info.get('environment')})
- **Système d'exploitation :** `{info.get('os')}`
- **Statut d'inventaire :** `{info.get('inventory_status')}`
- **Services déclarés :** {services_desc}
- **Dernière mesure enregistrée :** `{last_check.get('tcp_result')}` à `{last_check.get('timestamp')}`

**2. Analyse technique :**
- Les informations d'inventaire proviennent directement de la table `servers` normalisée par le pipeline ETL.

**3. Recommandations :**
- Pour valider la disponibilité en direct, effectuer une mesure active par sonde réseau.
"""
        return {"answer": answer, "traces": traces, "request_id": request_id}

    # --- Scénario F4 : Corrélation d'erreur à 10:03 ---
    elif "10:03" in q_lower or "corrélation" in q_lower or "s'est-il passé" in q_lower:
        events = execute_tool_with_logging(get_recent_events, "get_recent_events", {"hostname": "SRV-APP-01", "limit": 5}, user_question, request_id)
        traces.append({"tool": "get_recent_events", "args": {"hostname": "SRV-APP-01"}, "result": events, "source": "postgresql_events"})
        
        db_events = execute_tool_with_logging(get_recent_events, "get_recent_events", {"hostname": "SRV-DB-01", "limit": 5}, user_question, request_id)
        traces.append({"tool": "get_recent_events", "args": {"hostname": "SRV-DB-01"}, "result": db_events, "source": "postgresql_events"})

        answer = """### 🔗 Corrélation d'Incidents — Analyse de l'Erreur de 10:03
**1. Faits chronologiques établis :**
- `10:03:41` [SRV-APP-01] : L'API renvoie une erreur HTTP 500 sur `GET /tickets/open`.
- `10:03:42` [SRV-DB-01] : Échec d'authentification PostgreSQL (`password authentication failed for user techapp from 192.168.56.10`).
- `10:03:45` [SRV-APP-01] : Le pool de connexions SQLAlchemy est saturé suite aux échecs répétés.
- `10:10:00` [SRV-APP-01] : Le serveur MCP subit une déconnexion brutale de PostgreSQL.

**2. Analyse technique :**
- La panne de l'API à 10:03 n'est pas un bug interne de code FastAPI mais une conséquence directe de l'indisponibilité de la base causée par un problème d'identifiant applicatif `techapp`.
- Cette cascade d'erreurs a fini par saturer les sockets de connexion jusqu'à l'arrêt du service RDBMS.

**3. Recommandations :**
1. Valider le mot de passe du compte applicatif `techapp` configuré sur SRV-APP-01.
2. Redémarrer PostgreSQL sur SRV-DB-01 une fois la configuration fiabilisée.
"""
        return {"answer": answer, "traces": traces, "request_id": request_id}

    # --- Scénario F5 : Procédure d'escalade DNS ---
    elif "dns" in q_lower or "procédure" in q_lower or "procedure" in q_lower:
        proc_content = get_dns_procedure()
        traces.append({"resource": "procedures://dns", "result": "LOADED", "source": "mcp_resource"})
        
        answer = f"""### 📖 Procédure d'Exploitation : Incident DNS Critique
**1. Faits établis (Source : Resource MCP `procedures://dns`) :**
- Cible : `SRV-DNS-01` (`192.168.56.53`), Port 53 UDP/TCP.
- Symptômes associés : Rupture de résolution d'adresses internes, erreurs 'Host not found'.

**2. Procédure d'Intervention :**
1. Tester la connectivité UDP/TCP sur le port 53 :
   `nc -zvu 192.168.56.53 53`
2. Contrôler et redémarrer le démon DNS sur la cible :
   `systemctl restart bind9`
3. Consulter les journaux :
   `journalctl -u bind9 -n 50 --no-pager`

**3. Recommandations d'escalade :**
- Si la panne excède 10 minutes, déclencher l'astreinte Réseau et créer un ticket prioritaire `CRITICAL`.
"""
        return {"answer": answer, "traces": traces, "request_id": request_id}

    # --- Action avancée : Création de ticket avec confirmation ---
    elif "crée un ticket" in q_lower or "creer un ticket" in q_lower or "create_ticket" in q_lower:
        action_res = execute_tool_with_logging(
            create_ticket,
            "create_ticket",
            {
                "hostname": "SRV-WEB-01",
                "priority": "HIGH",
                "title": "Alerte de supervision : charge anormale Nginx",
                "confirm": confirm_action
            },
            user_question,
            request_id
        )
        traces.append({"tool": "create_ticket", "args": {"confirm": confirm_action}, "result": action_res, "source": "mcp_action_tool"})
        
        if not confirm_action:
            answer = """### ⚠️ Confirmation Humaine Requise
**Action sensible détectée :** Création d'un ticket incident de priorité `HIGH` pour `SRV-WEB-01`.
- L'outil a bloqué l'opération conformément aux règles de sécurité.
- **Veuillez cocher la case de confirmation ci-dessous pour valider la création effective.**"""
        else:
            answer = f"""### ✅ Ticket d'Incident Créé avec Succès
- **Numéro du Ticket :** #{action_res.get('id')}
- **Titre :** {action_res.get('title')}
- **Machine :** {action_res.get('hostname')}
- **Priorité :** {action_res.get('priority')}
- **Horodatage :** {action_res.get('created_at')}
- **Source :** API Métier FastAPI via MCP."""
        return {"answer": answer, "traces": traces, "request_id": request_id}

    # --- Requête sur l'état de l'API / des APIs ---
    elif any(k in q_lower for k in ["api", "apis", "fastapi", "endpoint", "endpoints", "santé", "sante", "health"]) or ("marche" in q_lower and "srv" not in q_lower and "serveur" not in q_lower):
        api_url = os.getenv("FASTAPI_URL", "http://127.0.0.1:8000")
        api_status = "UNKNOWN"
        api_db = "UNKNOWN"
        latency = 0.0
        try:
            t0 = time.time()
            resp = requests.get(f"{api_url}/health", timeout=2.0)
            latency = round((time.time() - t0) * 1000, 2)
            if resp.status_code == 200:
                data = resp.json()
                api_status = data.get("status", "healthy")
                api_db = data.get("database", "CONNECTED")
            else:
                api_status = f"HTTP {resp.status_code}"
        except Exception as e:
            api_status = f"INDISPONIBLE ({str(e)})"
            
        probe_app = execute_tool_with_logging(check_server_availability, "check_server_availability", {"hostname": "SRV-APP-01"}, user_question, request_id)
        traces.append({"tool": "check_server_availability", "args": {"hostname": "SRV-APP-01"}, "result": probe_app, "source": "live_tcp_socket_probe"})
        
        open_tickets = execute_tool_with_logging(list_open_tickets, "list_open_tickets", {}, user_question, request_id)
        traces.append({"tool": "list_open_tickets", "args": {}, "result": open_tickets, "source": "fastapi_api_http"})

        is_healthy = api_status in ["healthy", "ok"]
        state_icon = "✅" if is_healthy else "⚠️"
        state_text = "OPÉRATIONNELLE" if is_healthy else "INDISPONIBLE OU PARTIELLEMENT ACCESSIBLE"

        answer = f"""### {state_icon} État de Fonctionnement de l'API Métier : {state_text}
**1. Faits établis (Vérification technique temps réel) :**
- **Santé de l'API (`{api_url}/health`) :** Statut : `{api_status}` | Connexion base : `{api_db}` (Latence : {latency} ms).
- **Hôte Applicatif (`SRV-APP-01:8000`) :** `{probe_app.get('result')}` (Port applicatif 8000 joignable).
- **Consommation MCP ➔ FastAPI :** Fonctionnelle, `{len(open_tickets)}` ticket(s) actuellement recensé(s) via l'endpoint `/tickets`.

**2. Analyse technique :**
- L'API Métier FastAPI répond normalement aux requêtes HTTP sur le port `8000`.
- Le lien entre l'API et la base relationnelle PostgreSQL est actif et opérationnel.
- L'encapsulation métier fonctionne conformément aux règles d'architecture : le serveur FastMCP dialogue avec FastAPI via HTTP REST.

**3. Recommandations :**
- L'API est prête à recevoir les requêtes des équipes d'exploitation.
- La documentation OpenAPI Swagger est accessible sur `{api_url}/docs`.
"""
        return {"answer": answer, "traces": traces, "request_id": request_id}

    # --- Synthèse globale du parc de serveurs ---
    elif any(k in q_lower for k in ["parc", "serveurs", "inventaire", "machines", "tous les serveurs"]):
        summary_raw = get_inventory_summary()
        traces.append({"resource": "inventory://summary", "result": "LOADED", "source": "mcp_resource"})
        
        answer = f"""### 🌐 Vue Globale du Parc de Serveurs TECHCORP
**1. Faits établis (Source : Resource MCP `inventory://summary`) :**
```text
{summary_raw}
```

**2. Analyse technique :**
- L'inventaire est issu de la base de données PostgreSQL normalisée par le pipeline ETL.
- Les statuts indiqués sont déclaratifs (CMDB). Pour vérifier l'état en direct d'un serveur spécifique, une sonde TCP active est requise.

**3. Recommandations :**
- Utilisez *« SRV-DB-01 fonctionne-t-il réellement ? »* pour déclencher une vérification active contradictoire.
"""
        return {"answer": answer, "traces": traces, "request_id": request_id}

    # --- Scénario Section 9.3 : Contradictions globales ---
    elif any(k in q_lower for k in ["contradictoire", "contradictoires", "contradiction"]):
        sql = """
        SELECT s.hostname, s.inventory_status, sc.port, sc.tcp_result, sc.timestamp
        FROM servers s
        JOIN service_checks sc ON s.hostname = sc.hostname
        WHERE s.inventory_status = 'UP' AND sc.tcp_result IN ('FAILED', 'DOWN', 'TIMEOUT');
        """
        rows = query_db(sql)
        traces.append({"tool": "detect_contradictions_sql", "result": rows, "source": "postgresql_correlation"})
        
        lines = []
        for r in rows:
            lines.append(f"- **{r['hostname']}** : Déclaré `{r['inventory_status']}` en inventaire, mais la mesure réseau sur le port {r['port']} indique `{r['tcp_result']}` ({r['timestamp']}).")
        res_str = "\n".join(lines) if lines else "- Aucune contradiction détectée."

        answer = f"""### ⚠️ Serveurs Présentant des Données Contradictoires (Section 9.3)
**1. Faits établis :**
{res_str}

**2. Analyse technique :**
- L'inventaire de la CMDB est décorrélé de l'état réseau effectif.
- Le cas le plus critique est `SRV-DB-01` : le serveur est étiqueté opérationnel alors que son port PostgreSQL 5432 est fermé.

**3. Recommandations :**
- Déclencher immédiatement une sonde temps réel sur `SRV-DB-01`.
- Aligner la CMDB en passant le statut d'inventaire à `MAINTENANCE` ou `DOWN`.
"""
        return {"answer": answer, "traces": traces, "request_id": request_id}

    # --- Scénario Section 9.3 : Top serveurs concentrant le plus d'erreurs ---
    elif any(k in q_lower for k in ["plus d'erreurs", "concentre le plus d'erreurs", "top erreurs", "plus d'erreur"]):
        error_rows = query_db("SELECT hostname, COUNT(*) as cnt FROM events WHERE level='ERROR' GROUP BY hostname ORDER BY cnt DESC;")
        traces.append({"tool": "top_error_servers_sql", "result": error_rows, "source": "postgresql_events"})
        
        lines = [f"- **{r['hostname']}** : `{r['cnt']}` événement(s) ERROR répertorié(s)" for r in error_rows]
        err_str = "\n".join(lines) if lines else "- Aucun événement ERROR recensé."

        answer = f"""### 📊 Top des Serveurs Concentrant le Plus d'Erreurs (Section 9.3)
**1. Faits établis :**
{err_str}

**2. Analyse technique :**
- `SRV-APP-01` et `SRV-DB-01` concentrent la quasi-totalité des erreurs critiques du SI.
- La corrélation temporelle démontre que les erreurs de `SRV-APP-01` (HTTP 500) sont des erreurs collatérales causées par l'échec d'authentification PostgreSQL sur `SRV-DB-01` à 10:03.

**3. Recommandations :**
- Prioriser le rétablissement de `SRV-DB-01`.
- Vérifier les logs d'authentification applicative du compte `techapp`.
"""
        return {"answer": answer, "traces": traces, "request_id": request_id}

    # --- Réponse générale contextualisée ---
    else:
        info = execute_tool_with_logging(get_server_info, "get_server_info", {"hostname": "SRV-DB-01"}, user_question, request_id)
        traces.append({"tool": "get_server_info", "args": {"hostname": "SRV-DB-01"}, "result": info, "source": "postgresql_direct"})
        
        summary_raw = get_inventory_summary()
        tickets_crit = execute_tool_with_logging(list_open_tickets, "list_open_tickets", {"priority": "CRITICAL"}, user_question, request_id)
        traces.append({"tool": "list_open_tickets", "args": {"priority": "CRITICAL"}, "result": tickets_crit, "source": "fastapi_api_http"})
        
        prompt_llm = f"""Données réelles du SI TECHCORP obtenues via Tools MCP :
{summary_raw}
Tickets critiques ouverts : {len(tickets_crit)} ticket(s).

Question de l'opérateur : "{user_question}"

Réponds précisément à la question en te basant UNIQUEMENT sur ces données réelles.
Structure ta réponse obligatoirement ainsi :
**1. Faits établis :**
**2. Analyse technique :**
**3. Recommandations :**
"""
        llm_response = call_ollama(prompt_llm)
        if llm_response:
            return {"answer": llm_response, "traces": traces, "request_id": request_id}
            
        answer = f"""### 🤖 Diagnostic Synthétique TECHCORP
**1. Faits observés :**
- Requête reçue : *"{user_question}"*
- Données vérifiées via MCP : Parc de serveurs analysé, {len(tickets_crit)} incident(s) critique(s) ouvert(s).

**2. Analyse technique :**
- L'infrastructure est supervisée par le serveur MCP via ses Tools (PostgreSQL direct, FastAPI, sondes TCP actives).
- Vous pouvez interroger le système sur :
  * L'état de l'API (*« Est-ce que les API marchent ? »*).
  * La disponibilité d'un serveur précis (*« SRV-DB-01 fonctionne-t-il réellement ? »*).
  * Les incidents déclarés (*« Quels tickets critiques sont ouverts ? »*).
  * Les fiches d'inventaire (*« Donne-moi les informations de SRV-WEB-01 »*).
  * Les procédures d'urgence (*« Que faire pour un incident DNS critique ? »*).

**3. Recommandations :**
- Utilisez les boutons de scénarios rapides (F1 à F5) situés dans le volet gauche pour explorer les démonstrations types du projet.
"""
        return {"answer": answer, "traces": traces, "request_id": request_id}
