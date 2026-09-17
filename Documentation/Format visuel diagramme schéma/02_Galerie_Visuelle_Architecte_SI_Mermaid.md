# Galerie Visuelle d'Architecture SI (100% Rendu Graphique en Mermaid)

Ce document décline **l'intégralité des facettes d'un projet d'architecture SI / IA** sous forme de diagrammes **directement interprétés et affichés graphiquement** par votre lecteur Markdown sans aucun compilateur externe.

---

## 📑 Sommaire du Document
- [Vue 1. Architecture Système & Découpage en Zones (Équivalent D2 / Graphviz)](#vue-1-architecture-système--découpage-en-zones-équivalent-d2--graphviz)
- [Vue 2. Architecture Logicielle Formelle C4 Model - Container (Équivalent C4-PlantUML)](#vue-2-architecture-logicielle-formelle-c4-model-container-diagram)
- [Vue 3. Diagramme de Séquence des Échanges (Équivalent PlantUML Sequence)](#vue-3-diagramme-de-séquence-des-échanges-équivalent-plantuml-sequence)
- [Vue 4. Schéma de Données Entité-Relation (Équivalent DBML)](#vue-4-schéma-de-données-entité-relation-équivalent-dbml)
- [Vue 5. Processus Métier & Workflow de Contrôle (Équivalent BPMN)](#vue-5-processus-métier--workflow-de-contrôle-équivalent-bpmn)
- [Vue 6. Cartographie Stratégique & Risques (Mindmap de Gouvernance)](#vue-6-cartographie-stratégique--risques-mindmap-de-gouvernance)

---

## Vue 1. Architecture Système & Découpage en Zones (Équivalent D2 / Graphviz)

*Cette vue permet de visualiser les frontières de sécurité, les réseaux (DMZ) et l'urbanisation des composants.*

```mermaid
flowchart TD
    subgraph ZoneUtilisateur ["Zone Utilisateurs (Canaux Externes)"]
        User(["👤 Utilisateur Métier"])
        Web["💻 Portail Web d'Entreprise\n(React / Next.js)"]
        User -->|HTTPS / TLS 1.3| Web
    end

    subgraph ZoneDMZ ["Zone DMZ & Sécurité Frontale"]
        Gateway["🛡️ API Gateway / Reverse Proxy\n(Kong / Envoy / APISIX)\n- Validation OAuth2 & JWT\n- Rate Limiting & WAF"]
        Web -->|Appels REST API| Gateway
    end

    subgraph ZoneInterne ["Zone Interne (Réseau Privé d'Entreprise)"]
        direction TB
      
        subgraph ServicesIA ["Services Applicatifs & IA"]
            Orchestrateur["⚙️ Moteur d'Orchestration & Agents\n(FastAPI / LangGraph / LangChain)"]
            Guardrails["🛡️ Filtre Sécurité & DLP\n(NeMo Guardrails / Anonymisation)"]
            Orchestrateur --> Guardrails
        end

        subgraph Donnees ["Couche Données & Référentiels"]
            VectorDB[("📚 Base Vectorielle\n(pgvector / Qdrant)\nChunks & Index HNSW")]
            ERPDB[("🏢 ERP & BDD Métier\n(PostgreSQL / SAP)\nDonnées relationnelles")]
        end
    end

    subgraph ZoneCloudSouverain ["Zone Fournisseur de Modèles"]
        LLM["🧠 Inférence Modèle LLM\n(Mistral / Llama / Vertex AI)\nEndpoint sécurisé mTLS"]
    end

    Gateway -->|Requête authentifiée| Orchestrateur
    Orchestrateur -->|1. Recherche similarité| VectorDB
    Orchestrateur -->|2. Requête SQL métier| ERPDB
    Guardrails -->|3. Prompt enrichi & purgé| LLM
    LLM -.->|4. Flux d'inférence| Guardrails
    Guardrails -.->|5. Réponse validée| Gateway
    Gateway -.->|6. Réponse finale| Web

    style ZoneUtilisateur fill:#0f172a,stroke:#38bdf8,stroke-width:2px,color:#fff
    style ZoneDMZ fill:#1e293b,stroke:#f59e0b,stroke-width:2px,color:#fff
    style ZoneInterne fill:#090d16,stroke:#818cf8,stroke-width:2px,color:#fff
    style ZoneCloudSouverain fill:#2e1065,stroke:#ec4899,stroke-width:2px,color:#fff
```

---

## Vue 2. Architecture Logicielle Formelle C4 Model (Container Diagram)

*Le modèle standard de l'ingénierie logicielle pour documenter les conteneurs applicatifs et leurs responsabilités.*

```mermaid
C4Container
    title Diagramme C4 Container - Connexion de l'IA au Système d'Information

    Person(user, "Utilisateur Métier", "Employé de l'entreprise analysant des dossiers et posant des questions métier.")
  
    System_Boundary(si_boundary, "Périmètre du Système d'Information") {
        Container(spa, "Application Web", "TypeScript, React", "Fournit l'interface conversationnelle et les tableaux de bord analytiques.")
        Container(api_gw, "Passerelle API", "Kong / Traefik", "Gère l'authentification OpenID Connect, le routage et le filtrage des quotas.")
        Container(ai_service, "Service IA & RAG", "Python, FastAPI", "Orchestre les agents ReAct, construit le contexte et gère l'historique conversationnel.")
        ContainerDb(vectordb, "Base Vectorielle", "Qdrant / pgvector", "Stocke les index sémantiques et métadonnées des documents internes.")
        ContainerDb(erp_db, "Base Données Métier", "PostgreSQL", "Stocke les comptes clients, transactions et référentiels d'entreprise.")
    }

    System_Ext(llm_provider, "Moteur d'Inférence LLM", "Plateforme Cloud Souveraine", "Fournit l'API d'inférence de modèles de langage (Mistral Large / Llama 3).")

    Rel(user, spa, "Utilise", "HTTPS")
    Rel(spa, api_gw, "Envoie requêtes", "JSON / HTTPS")
    Rel(api_gw, ai_service, "Transmet après validation", "gRPC / HTTP2")
    Rel(ai_service, vectordb, "Recherche sémantique", "gRPC")
    Rel(ai_service, erp_db, "Requête SQL", "TCP / TLS")
    Rel(ai_service, llm_provider, "Inférence prompt", "HTTPS / mTLS")
```

---

## Vue 3. Diagramme de Séquence des Échanges (Équivalent PlantUML Sequence)

*Visualise la chronologie exacte des messages, des contrôles de sécurité et des flux asynchrones.*

```mermaid
sequenceDiagram
    autonumber
    actor U as 👤 Utilisateur
    participant W as 💻 Portail Web
    participant GW as 🛡️ API Gateway
    participant IA as ⚙️ Orchestrateur IA
    participant VDB as 📚 Base Vectorielle
    participant ERP as 🏢 ERP Métier
    participant LLM as 🧠 Service LLM

    U->>W: Saisit: "Résume les impayés du client Dupont"
    W->>GW: POST /api/v1/assistant (Bearer Token JWT)
  
    Note over GW: Validation signature JWT & Quota
    GW->>IA: Relai requête enrichie du contexte utilisateur
  
    par Recherche documentaire et données de gestion
        IA->>VDB: Recherche vectorielle ("contrat litige impayé")
        VDB-->>IA: Chunks de documents pertinents (Top-K)
    and
        IA->>ERP: SELECT montant, date FROM factures WHERE client='Dupont'
        ERP-->>IA: Données comptables (2 factures échues)
    end

    Note over IA: Construction du Prompt Système (RAG) + Données SQL
  
    IA->>LLM: Inférence(Prompt système + Contexte + Question)
    LLM-->>IA: Réponse synthétisée et sourcée
  
    Note over IA: Contrôle Guardrails (Détection PII & Hallucinations)
  
    IA-->>GW: 200 OK (JSON avec texte et sources)
    GW-->>W: Payload formaté
    W-->>U: Affichage du résumé avec liens vers les justificatifs
```

---

## Vue 4. Schéma de Données Entité-Relation (Équivalent DBML)

*Modélise la persistance des données relationnelles, vectorielles et la traçabilité des interactions IA.*

```mermaid
erDiagram
    UTILISATEUR ||--o{ SESSION_IA : initie
    UTILISATEUR ||--o{ DOCUMENT : depose
    DOCUMENT ||--|{ CHUNK_VECTORIEL : decoupe_en
    SESSION_IA ||--|{ MESSAGE_HISTORIQUE : contient
    MESSAGE_HISTORIQUE ||--o{ LOG_AUDIT_IA : genere

    UTILISATEUR {
        int id PK
        string nom
        string email
        string role_metier
        timestamp created_at
    }

    DOCUMENT {
        int id PK
        int utilisateur_id FK
        string titre
        string chemin_stockage
        string format_mime
        timestamp date_upload
    }

    CHUNK_VECTORIEL {
        uuid id PK
        int document_id FK
        text contenu_texte
        vector384 embedding_dense
        jsonb metadata
    }

    SESSION_IA {
        uuid id PK
        int utilisateur_id FK
        string titre_conversation
        timestamp date_debut
    }

    MESSAGE_HISTORIQUE {
        uuid id PK
        uuid session_id FK
        string role
        text contenu
        timestamp horodatage
    }

    LOG_AUDIT_IA {
        uuid id PK
        uuid message_id FK
        string modele_utilise
        int tokens_entree
        int tokens_sortie
        float temps_inference_ms
        float cout_estime_eur
    }
```

---

## Vue 5. Processus Métier & Workflow de Contrôle (Équivalent BPMN)

*Représente le cycle de décision avec embranchements, vérifications de conformité et garde-fous.*

```mermaid
flowchart LR
    Start([🟢 Début Requête]) --> Auth{Authentification\nValide ?}
  
    Auth -- Non --> ErrAuth[❌ Erreur 401 Unauthorized] --> EndKO([🔴 Rejet])
  
    Auth -- Oui --> Classif[Classification d'Intention & Détection PII]
    Classif --> Quota{Quotas\ndépassés ?}
  
    Quota -- Oui --> ErrRate[⚠️ Erreur 429 Too Many Requests] --> EndKO
  
    Quota -- Non --> RAG[Enrichissement RAG & Données Internes]
    RAG --> SendLLM[Appel Modèle d'Inférence LLM]
    SendLLM --> Guard{Vérification\nGuardrails}
  
    Guard -- Échec (Hallucination / Fuite) --> Fallback[Génération réponse par défaut / Escalade]
    Guard -- Succès --> Log[Journalisation Audit & FinOps]
  
    Fallback --> Log
    Log --> Reponse[Envoi de la réponse à l'utilisateur] --> EndOK([🏁 Fin Processus])

    style Start fill:#16a34a,color:#fff
    style EndOK fill:#16a34a,color:#fff
    style EndKO fill:#dc2626,color:#fff
    style Auth fill:#d97706,color:#fff
    style Quota fill:#d97706,color:#fff
    style Guard fill:#d97706,color:#fff
```

---

## Vue 6. Cartographie Stratégique & Risques (Mindmap de Gouvernance)

*Arbre décisionnel pour les comités d'architecture (Gouvernance, Sécurité, Réglementation).*

```mermaid
mindmap
  root((Urbanisation IA dans le SI))
    Gouvernance & Conformité
      EU AI Act
        Classification Risque Élevé
        Explicabilité & Auditabilité
      RGPD
        Minimisation des données
        Droit d'opposition
        Pseudonymisation DLP
    Sécurité & Résilience
      OWASP Top 10 LLM
        Prompt Injection
        Sensitive Information Disclosure
      Zero Trust
        mTLS & IAM
        Isolation des données vectorielles
    Architecture Technique
      Patterns d'Intégration
        APIs REST & gRPC
        Event Driven Kafka
        Model Context Protocol MCP
      Persistance
        Stockage hybride SQL + Vecteurs
        Cache sémantique Redis
    FinOps & Performance
      Latence d'inférence
      Budgétisation par tokens
      Modèles spécialisés vs Généralistes
```
