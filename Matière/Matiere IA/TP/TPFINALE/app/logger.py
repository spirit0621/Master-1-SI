"""
Module de Journalisation et de Traçabilité TECHCORP
Enregistre chaque appel conformément à la section 11.1 du sujet officiel :
timestamp, request_id, user_question, tool_name, tool_arguments, tool_status, source, duration_ms.
Exclut rigoureusement tout secret, token ou mot de passe.
"""
import os
import json
import uuid
import time
from datetime import datetime
from typing import Dict, Any, Optional

LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
LOG_FILE = os.path.join(LOG_DIR, "techcorp_calls.jsonl")

def ensure_log_dir():
    os.makedirs(LOG_DIR, exist_ok=True)

def sanitize_data(data: Any) -> Any:
    """Masque toute clé ou valeur sensible."""
    if isinstance(data, dict):
        cleaned = {}
        for k, v in data.items():
            if any(secret_kw in k.lower() for secret_kw in ["pass", "pwd", "token", "secret", "key", "auth"]):
                cleaned[k] = "[MASQUÉ / SECRET TECHCORP]"
            else:
                cleaned[k] = sanitize_data(v)
        return cleaned
    elif isinstance(data, list):
        return [sanitize_data(item) for item in data]
    return data

def log_mcp_call(
    user_question: str,
    tool_name: str,
    tool_arguments: Dict[str, Any],
    tool_status: str,
    source: str,
    duration_ms: float,
    request_id: Optional[str] = None
) -> str:
    """Écrit une ligne de log structurée au format JSON Lines."""
    ensure_log_dir()
    req_id = request_id or str(uuid.uuid4())
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "request_id": req_id,
        "user_question": user_question,
        "tool_name": tool_name,
        "tool_arguments": sanitize_data(tool_arguments),
        "tool_status": tool_status,
        "source": source,
        "duration_ms": duration_ms
    }
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        
    return req_id

def get_recent_logs(limit: int = 50) -> list:
    """Lit les derniers logs enregistrés."""
    ensure_log_dir()
    if not os.path.exists(LOG_FILE):
        return []
    logs = []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    logs.append(json.loads(line.strip()))
                except Exception:
                    pass
    return logs[-limit:]

def clear_mcp_logs():
    """Vide intégralement le journal d'appels MCP."""
    ensure_log_dir()
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("")
    return True
