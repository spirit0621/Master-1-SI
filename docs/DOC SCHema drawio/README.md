# 📊 CLASSEUR DES SCHÉMAS D'ARCHITECTURE & FLUX (DRAW.IO)

Ce dossier contient les diagrammes d'architecture officiels exigés par la **Section 13 (Livrable 4)** et la **Section 16 (Critères A9, A11, A14)**.

---

## 📑 Inventaire des Fichiers Draw.io

| Fichier | Nom du Schéma | Description & Rôle pour l'Évaluation |
| :--- | :--- | :--- |
| **`TECHCORP_TOUS_LES_SCHEMAS.drawio`** | **Classeur Global Multi-Onglets** | Contient l'ensemble des 5 diagrammes ci-dessous dans un fichier unique à onglets pour une présentation fluide. |
| **`schema_architecture_reseau.drawio`** | **1. Architecture & Flux Réseau** | Découpage en 4 zones étanches (Client, App, Data, Cibles réseau). Détail des IP (`192.168.56.x`), ports (`8000`, `8501`, `11434`, `5432`) et protocoles. |
| **`schema_cycle_fonctionnel_ia.drawio`** | **2. Cycle Fonctionnel de l'IA** | Parcours complet en 8 étapes : Saisie utilisateur ➔ LLM Qwen ➔ FastMCP ➔ Sources SI ➔ Analyse critique & arbitrage ➔ Restitution structurée (Faits, Vérif, Recommandations). |
| **`schema_dual_tool_calling.drawio`** | **3. Architecture Dual Tool Calling** | Comparatif architectural des canaux d'accès : Accès direct DB vs Consommation API REST FastAPI vs Sonde Réseau Socket TCP vs Validation humaine. |
| **`schema_modele_donnees_erd.drawio`** | **4. Modèle Relationnel ERD (3FN)** | Diagramme Entité-Association complet des tables PostgreSQL/SQLite (`servers`, `services`, `tickets`, `service_checks`, `events`, `procedures`, `roles`, `ingestion_audit`). |
| **`schema_sequence_scenario_f3.drawio`** | **5. Diagramme de Séquence Scénario F3** | Déroulé chronologique du cas contradictoire (Panne active de SRV-DB-01) illustrant la confrontation entre l'inventaire théorique et la mesure active. |

---

## 🛠️ Comment Ouvrir & Exporter ces Schémas

1. **Dans VS Code :**
   - Installez l'extension **Draw.io Integration** (`hediet.vscode-drawio`).
   - Cliquez simplement sur n'importe quel fichier `.drawio` pour l'éditer visuellement.
2. **Dans un Navigateur Web :**
   - Rendez-vous sur [https://app.diagrams.net/](https://app.diagrams.net/).
   - Menu `Fichier` ➔ `Ouvrir à partir de` ➔ `Appareil` et sélectionnez le fichier `.drawio`.
   - Exportez en PNG ou PDF pour insertion directe dans votre rapport final.
