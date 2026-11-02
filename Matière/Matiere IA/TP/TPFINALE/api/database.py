"""
Module d'accès aux données TECHCORP (PostgreSQL avec bascule locale SQLite)
Garantit le fonctionnement immédiat en local tout en ciblant PostgreSQL en production.
"""
import os
import sqlite3
from typing import List, Dict, Any, Optional
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    psycopg2 = None
    RealDictCursor = None

from dotenv import load_dotenv

load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB = os.getenv("POSTGRES_DB", "techcorp")
POSTGRES_USER = os.getenv("POSTGRES_USER", "techapp")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "techapp_password_2026")

SQLITE_PATH = os.path.join(os.path.dirname(__file__), "..", "techcorp.db")

def get_db_connection():
    """Tente une connexion à PostgreSQL 16 ; bascule sur SQLite si inaccessible ou absent."""
    if psycopg2 is not None:
        try:
            conn = psycopg2.connect(
                host=POSTGRES_HOST,
                port=POSTGRES_PORT,
                dbname=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                connect_timeout=2
            )
            return conn, "postgresql"
        except Exception:
            pass
    
    # Fallback automatique vers base locale SQLite pour exécution immédiate
    need_init = not os.path.exists(SQLITE_PATH)
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    if need_init:
        _init_sqlite_schema(conn)
    return conn, "sqlite"

def _init_sqlite_schema(conn):
    schema_file = os.path.join(os.path.dirname(__file__), "..", "sql", "schema.sql")
    if os.path.exists(schema_file):
        with open(schema_file, "r", encoding="utf-8") as f:
            sql_content = f.read()
        sqlite_sql = sql_content.replace("SERIAL PRIMARY KEY", "INTEGER PRIMARY KEY AUTOINCREMENT")
        sqlite_sql = sqlite_sql.replace("TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP", "DATETIME DEFAULT CURRENT_TIMESTAMP")
        sqlite_sql = sqlite_sql.replace("TIMESTAMP WITHOUT TIME ZONE", "DATETIME")
        cursor = conn.cursor()
        cursor.executescript(sqlite_sql)
        conn.commit()
        cursor.close()

def init_database():
    """Initialise le schéma relationnel complet."""
    conn, engine = get_db_connection()
    cursor = conn.cursor()
    
    # Lecture du schéma SQL
    schema_file = os.path.join(os.path.dirname(__file__), "..", "sql", "schema.sql")
    if os.path.exists(schema_file):
        with open(schema_file, "r", encoding="utf-8") as f:
            sql_content = f.read()
            
        if engine == "sqlite":
            # Adapter le schéma Postgres vers SQLite si nécessaire
            sqlite_sql = sql_content.replace("SERIAL PRIMARY KEY", "INTEGER PRIMARY KEY AUTOINCREMENT")
            sqlite_sql = sqlite_sql.replace("TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP", "DATETIME DEFAULT CURRENT_TIMESTAMP")
            sqlite_sql = sqlite_sql.replace("TIMESTAMP WITHOUT TIME ZONE", "DATETIME")
            cursor.executescript(sqlite_sql)
        else:
            cursor.execute(sql_content)
            
        conn.commit()
    cursor.close()
    conn.close()
    return engine

def query_db(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """Exécute une requête SQL paramétrée et retourne une liste de dictionnaires."""
    conn, engine = get_db_connection()
    cursor = conn.cursor()
    
    if engine == "postgresql":
        # Remplacer les placeholders '?' par '%s' pour psycopg2
        pg_query = query.replace("?", "%s")
        cursor.execute(pg_query, params)
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        results = [dict(zip(columns, row)) for row in cursor.fetchall()] if cursor.description else []
    else:
        cursor.execute(query, params)
        results = [dict(row) for row in cursor.fetchall()] if cursor.description else []
        
    cursor.close()
    conn.close()
    return results

def execute_db(query: str, params: tuple = ()) -> int:
    """Exécute une commande SQL (INSERT, UPDATE, DELETE) paramétrée."""
    conn, engine = get_db_connection()
    cursor = conn.cursor()
    
    if engine == "postgresql":
        pg_query = query.replace("?", "%s")
        cursor.execute(pg_query, params)
        last_id = None
        if "INSERT" in query.upper() and "RETURNING" not in query.upper():
            try:
                cursor.execute("SELECT LASTVAL();")
                last_id = cursor.fetchone()[0]
            except Exception:
                last_id = None
    else:
        cursor.execute(query, params)
        last_id = cursor.lastrowid
        
    conn.commit()
    cursor.close()
    conn.close()
    return last_id
