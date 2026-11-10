# Cours Complet : Architecture des Systèmes d'Information (Master SI)

> **Niveau :** Master 1 / Master 2 — Systèmes d'Information & Génie Logiciel
> **Établissement :** CFA INSTA / Master SI
> **Auteur & Pédagogie :** Référentiel Académique & Pratiques Professionnelles d'Entreprise
> **Statut :** Support de cours de référence (Théorie, Méthodologies, Paradigmes, Modélisation, Cas Pratiques & Examens)

---

## 📑 Sommaire Général du Cours

1. [Module 1 : Fondements et Enjeux de l&#39;Architecture des SI](#module-1--fondements-et-enjeux-de-larchitecture-des-si)
   - 1.1 Qu'est-ce qu'un Système d'Information (SI) ?
   - 1.2 Définition de l'Architecture SI et Architecture d'Entreprise (EA)
   - 1.3 Les différents métiers de l'Architecte
   - 1.4 Les objectifs stratégiques : Alignement Métier-IT, TCO, Dette Technique, Agilité
2. [Module 2 : Méthodologies &amp; Cadres de Référence (Frameworks)](#module-2--méthodologies--cadres-de-référence-frameworks)
   - 2.1 La démarche d'Urbanisation du SI (Modèle Français)
   - 2.2 TOGAF (The Open Group Architecture Framework) et la méthode ADM
   - 2.3 Le Cadre de Zachman
   - 2.4 La norme ISO/IEC/IEEE 42010
3. [Module 3 : Modélisation et Cartographie du SI](#module-3--modélisation-et-cartographie-du-si)
   - 3.1 Cartographie des Processus Métier (BPMN 2.0)
   - 3.2 Modélisation d'Architecture d'Entreprise avec ArchiMate 3.x
   - 3.3 Les 4 vues canoniques de l'urbanisme (Métier, Fonctionnelle, Applicative, Technique)
   - 3.4 Matrices de flux et référentiels d'architecture (EAM)
4. [Module 4 : Paradigmes &amp; Styles d&#39;Architecture Logicielle et Applicative](#module-4--paradigmes--styles-darchitecture-logicielle-et-applicative)
   - 4.1 Monolithe vs Architecture Distribuée
   - 4.2 Architecture Orientée Services (SOA) et Enterprise Service Bus (ESB)
   - 4.3 Architecture Microservices (Principes, Patterns, Anti-patterns)
   - 4.4 Architecture Orientée Événements (EDA) : Pub/Sub, Event Sourcing, CQRS
   - 4.5 Domain-Driven Design (DDD) appliqué à l'Architecture SI
   - 4.6 Architectures Propres : Hexagonale (Ports & Adapters) et Clean Architecture
5. [Module 5 : Architecture des Données (Data Architecture)](#module-5--architecture-des-données-data-architecture)
   - 5.1 Gestion des Données de Référence (MDM - Master Data Management)
   - 5.2 Du Relationnel (ACID) au NoSQL / NewSQL (BASE & Théorème CAP)
   - 5.3 Décisionnel : Data Warehouse, Data Marts, Data Lake, Data Lakehouse
   - 5.4 Le paradigme Data Mesh (Décentralisation & Data as a Product)
   - 5.5 Gouvernance de données, Lignage (Data Lineage) et RGPD
6. [Module 6 : Architecture d&#39;Intégration &amp; Échanges Inter-Applicatifs](#module-6--architecture-dintégration--échanges-inter-applicatifs)
   - 6.1 Styles d'APIs : REST, GraphQL, gRPC, WebSockets, Webhooks
   - 6.2 API Management (APIM), API Gateway et Service Mesh
   - 6.3 Patterns d'Intégration d'Entreprise (EIP - Gregor Hohpe)
   - 6.4 Stratégies d'échanges : Batch (ETL/ELT) vs Streaming temps réel (Kafka)
7. [Module 7 : Architecture d&#39;Infrastructure, Cloud &amp; Sécurité](#module-7--architecture-dinfrastructure-cloud--sécurité)
   - 7.1 Modèles Cloud : IaaS, PaaS, SaaS, Serverless (FaaS) — Stratégies Hybride & Multi-cloud
   - 7.2 Conteneurisation et Orchestration (Docker, Kubernetes)
   - 7.3 Infrastructure as Code (IaC) et paradigme GitOps / Cloud Native
   - 7.4 Sécurité de l'Architecture : Zero Trust (NIST SP 800-207), Défense en profondeur, IAM, Cryptographie
8. [Module 8 : Gouvernance, Trajectoire SI et Schéma Directeur (SDSI)](#module-8--gouvernance-trajectoire-si-et-schéma-directeur-sdsi)
   - 8.1 Élaboration du Schéma Directeur des SI (SDSI)
   - 8.2 Analyse des écarts (Gap Analysis : As-Is ➔ To-Be ➔ Trajectoire)
   - 8.3 Gestion du Portefeuille Applicatif (Modèle TIME du Gartner)
   - 8.4 Comités d'Architecture (Architecture Review Board - ARB) et KPIs
9. [Module 9 : Étude de Cas Fil Conducteur &amp; Exercices d&#39;Examen](#module-9--étude-de-cas-fil-conducteur--exercices-dexamen)
   - Cas pratique : Refonte du SI d'une banque de détail / e-commerce
   - Questions types d'examen Master & Corrigés détaillés

---

# Module 1 : Fondements et Enjeux de l'Architecture des SI

## 1.1 Qu'est-ce qu'un Système d'Information (SI) ?

Un **Système d'Information (SI)** est un ensemble organisé de ressources permettant d'acquérir, traiter, stocker, communiquer et diffuser des informations au sein d'une organisation pour soutenir ses processus opérationnels et ses prises de décision.

```mermaid
graph LR
    Collecte["📥 Acquisition / Collecte"] --> Traitement["⚙️ Traitement / Règles de calcul"]
    Traitement --> Stockage["💾 Mémorisation / Stockage"]
    Stockage --> Restitution["📊 Communication / Diffusion"]
    Restitution --> Decision["🎯 Décision & Action Métier"]
    Decision -. "Boucle de rétroaction" .-> Collecte

    style Collecte fill:#e0f2fe,stroke:#0284c7,stroke-width:2px,color:#000
    style Traitement fill:#fef3c7,stroke:#f59e0b,stroke-width:2px,color:#000
    style Stockage fill:#dcfce7,stroke:#16a34a,stroke-width:2px,color:#000
    style Restitution fill:#f3e8ff,stroke:#9333ea,stroke-width:2px,color:#000
    style Decision fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#000
```

### Distinction fondamentale : SI vs Système Informatique

* **Système Informatique :** Composé exclusivement d'éléments matériels (serveurs, réseaux, routeurs) et logiciels (SGBD, OS, applications, scripts). C'est le support technique opérationnel.
* **Système d'Information (SI) :** Englobe le système informatique, mais intègre impérativement **la dimension humaine** (utilisateurs, gestionnaires, clients), **les processus métier** (procédures d'achat, de facturation, logistique) et **la gouvernance organisationnelle**.

---

## 1.2 Définition de l'Architecture SI et Architecture d'Entreprise (EA)

L'**Architecture d'Entreprise** (*Enterprise Architecture* ou EA) est la discipline formelle qui organise, structure et documente la cohérence globale d'une entreprise : depuis sa stratégie jusqu'à son exécution technologique.

> **Définition ISO/IEC/IEEE 42010 :**
> *"L'architecture est l'organisation fondamentale d'un système incarnée par ses composants, leurs relations entre eux et avec l'environnement, ainsi que les principes guidant sa conception et son évolution."*

L'architecture SI répond à un dilemme permanent : **concilier la pérennité du long terme (stabilité, sécurité) avec l'agilité du court terme (besoins business immédiats)**.

---

## 1.3 Les différents métiers de l'Architecte

Dans les grandes organisations, le rôle d'architecte se décline en 4 spécialités complémentaires :

| Rôle                                                        | Périmètre d'intervention                                                                   | Horizon temporel | Interlocuteurs principaux                     |
| :----------------------------------------------------------- | :------------------------------------------------------------------------------------------- | :--------------- | :-------------------------------------------- |
| **Enterprise Architect (EA)** / **Urbaniste SI** | Vision globale transversale du SI de l'entreprise                                            | 3 à 5 ans       | Direction Générale, DSI, Directeurs Métier |
| **Solution Architect**                                 | Conception d'une solution applicative complète bout en bout répondant à un besoin métier | 1 à 2 ans       | Product Owners, Chefs de projet, Leads Tech   |
| **Software Architect**                                 | Conception interne du code, design patterns, modularité, performance logicielle             | Projet en cours  | Développeurs, Tech Leads, QA                 |
| **Infrastructure / Cloud Architect**                   | Réseaux, plateformes Cloud, virtualisation, dimensionnement matériel, sécurité réseau   | 1 à 3 ans       | Équipes Ops, DevOps, RSSI, SysAdmins         |

---

## 1.4 Les Objectifs Stratégiques de l'Architecture

### 1.4.1 L'Alignement Métier-IT (Business-IT Alignment)

Formalisé par **Henderson & Venkatraman (1993)** dans le *Strategic Alignment Model (SAM)*, l'architecture doit synchroniser quatre domaines :

```mermaid
flowchart TD
    subgraph Metier["🏢 DOMAINE STRATÉGIE & MÉTIER"]
        SM["🎯 Stratégie Métier<br><i>(Vision, Marchés, Partenariats)</i>"]
        PO["👥 Organisation & Processus<br><i>(RH, Ventes, Logistique)</i>"]
        SM <-->|"Cohérence Stratégique"| PO
    end

    subgraph IT["💻 DOMAINE TECHNOLOGIE & IT"]
        SI["🚀 Stratégie IT<br><i>(Cloud, IA, APIs, Sécurité)</i>"]
        IA["⚙️ Infrastructure & Applications<br><i>(ERP, Microservices, Kubernetes)</i>"]
        SI <-->|"Cohérence Technologique"| IA
    end

    SM <===>|"Alignement Stratégique"| SI
    PO <===>|"Intégration Opérationnelle"| IA

    style Metier fill:#fef3c7,stroke:#f59e0b,stroke-width:2px,color:#000
    style IT fill:#e0f2fe,stroke:#0284c7,stroke-width:2px,color:#000
    style SM fill:#ffffff,stroke:#d97706,stroke-width:1.5px,color:#000
    style PO fill:#ffffff,stroke:#d97706,stroke-width:1.5px,color:#000
    style SI fill:#ffffff,stroke:#0369a1,stroke-width:1.5px,color:#000
    style IA fill:#ffffff,stroke:#0369a1,stroke-width:1.5px,color:#000
```

### 1.4.2 TCO (Total Cost of Ownership) & ROI

* **CAPEX (Capital Expenditures) :** Dépenses d'investissement initiales (achat de serveurs, licences perpétuelles).
* **OPEX (Operational Expenditures) :** Dépenses récurrentes de fonctionnement (abonnements SaaS, consommation Cloud au CPU/heure, infogérance).
* L'architecture doit réduire le coût global de possession en évitant les redondances applicatives (ex: avoir 3 CRM différents dans des filiales distinctes).

### 1.4.3 La Dette Technique et l'Obsolescence

La dette technique désigne le surcoût futur engendré par le choix d'une solution de contournement rapide ("quick and dirty") au détriment d'une architecture saine et modulaire.

* Intérêts de la dette : chaque évolution prend 2 à 5 fois plus de temps.
* Risque de faillite technique : impossibilité de faire évoluer le système sans tout casser.

---

# Module 2 : Méthodologies & Cadres de Référence (Frameworks)

## 2.1 La démarche d'Urbanisation du SI (L'Approche Française)

Inspirée par la planification urbaine des villes (Christoph, Sassoon, Longépé), l'urbanisation part du constat qu'**on ne rase pas une métropole pour construire un nouveau quartier ; on la fait évoluer par blocs cohérents**.

### 2.1.1 La Métaphore de la Ville

| Concept Urbain                               | Équivalent dans le Système d'Information | Rôle dans l'Architecture SI                            |
| :------------------------------------------- | :----------------------------------------- | :------------------------------------------------------ |
| **Territoire / Métropole**            | **Ensemble du SI d'Entreprise**      | Périmètre complet de gouvernance                      |
| **Zone d'activité**                   | **Zone Fonctionnelle**               | Découpage macro (ex: Zone Vente, Zone Finance)         |
| **Quartier**                           | **Quartier Fonctionnel**             | Regroupement de fonctions cohérentes (ex: Facturation) |
| **Îlot**                              | **Bloc Fonctionnel Élémentaire**   | Responsable d'une tâche précise (ex: Calcul TVA)      |
| **Réseaux (Eau, Gaz, Électricité)** | **Bus d'Échange / Middleware**      | Réseau d'échanges d'APIs, Kafka, ESB                  |
| **Plan Local d'Urbanisme (PLU)**       | **Règles d'Urbanisme & POS**        | Standards d'intégration et politiques d'urbanisation   |

### 2.1.2 Les Principes d'Urbanisme

1. **Forte cohésion interne :** Un bloc accomplit une et une seule mission fonctionnelle bien identifiée.
2. **Faible couplage externe :** Deux blocs ne communiquent jamais par accès direct à leurs bases de données respectives, mais uniquement via des interfaces formalisées (APIs, contrats de messages).
3. **Non-redondance :** Chaque donnée possède un bloc unique qui en est le maître légitime (*Système d'enregistrement* ou *System of Record*).
4. **Indépendance des couches :** Modifier la couche technique (migrer de MySQL à PostgreSQL) ne doit impacter ni la couche applicative ni la couche métier.

---

## 2.2 TOGAF (The Open Group Architecture Framework)

TOGAF est le standard international le plus utilisé dans les grandes entreprises pour conduire des projets d'architecture globale.

### 2.2.1 Les 4 Piliers BDAT de TOGAF

1. **Business Architecture (Architecture Métier) :** Définit la stratégie d'entreprise, les capacités métier, les processus, la structure organisationnelle.
2. **Data Architecture (Architecture des Données) :** Structure des actifs de données logiques et physiques, gouvernance de la donnée.
3. **Application Architecture (Architecture Applicative) :** Plan de chaque application à déployer, interactions entre systèmes sans s'attacher au code interne.
4. **Technology Architecture (Architecture Technique) :** Capacités matérielles, logicielles d'infrastructure, réseaux, Cloud, OS, middleware.

### 2.2.2 La Roue ADM (Architecture Development Method)

L'ADM est le cœur opérationnel itératif de TOGAF :

```mermaid
flowchart TD
    Prelim["Phase Préliminaire : Principes & Outils"] --> A["Phase A : Vision de l'Architecture"]
    A --> B["Phase B : Architecture Métier"]
    B --> C["Phase C : Architecture des SI (Données & Applications)"]
    C --> D["Phase D : Architecture Technologique"]
    D --> E["Phase E : Opportunités & Solutions"]
    E --> F["Phase F : Planification de la Migration"]
    F --> G["Phase G : Gouvernance du Déploiement"]
    G --> H["Phase H : Gestion du Changement d'Architecture"]
    H --> A
  
    subgraph Centre["Gestion Continue"]
        RM["Gestion des Exigences (Requirements Management)"]
    end
  
    A <--> RM
    B <--> RM
    C <--> RM
    D <--> RM
    E <--> RM
    F <--> RM
    G <--> RM
    H <--> RM
```

---

## 2.3 Le Cadre de Zachman (Zachman Framework)

Proposé par John Zachman chez IBM en 1987, c'est une **matrice taxonomique bidimensionnelle (6 x 6)** permettant de classifier l'ensemble des artefacts d'un SI sans imposer de méthode séquentielle :

* **Les 6 Colonnes (Les Questions Fondamentales) :**

  1. **Quoi (What) :** Les données (Modèles conceptuels, logiques, physiques de données).
  2. **Comment (How) :** Les fonctions et processus (Diagrammes de flux, cas d'utilisation, spécifications).
  3. **Où (Where) :** La distribution géographique et réseau (Sites, topologies, adresses IP).
  4. **Qui (Who) :** Les personnes et organisations (Acteurs, rôles, RACI, sécurité d'accès).
  5. **Quand (When) :** Le temps (Fréquences d'exécution, ordonnancement, états système).
  6. **Pourquoi (Why) :** Les motivations et objectifs stratégiques (Règles métier, KPI, ROI).
* **Les 6 Lignes (Les Perspectives des Acteurs) :**

  1. *Actionnaire / Planificateur :* Contexte global & Vision.
  2. *Propriétaire Métier :* Modèle conceptuel du métier.
  3. *Architecte / Concepteur :* Modèle logique du système.
  4. *Ingénieur / Bâtisseur :* Modèle physique et technologique.
  5. *Sous-traitant / Intégrateur :* Composants détaillés et code.
  6. *Utilisateur final :* Système fonctionnel en exploitation.

---

## 2.4 La Norme ISO/IEC/IEEE 42010

Standard mondial régissant la description des architectures :

* **Stakeholder (Partie prenante) :** Personne ou groupe ayant un intérêt dans le système (ex: RSSI, DAF, Développeur).
* **Concern (Préoccupation) :** Sujet d'attention critique pour une partie prenante (sécurité, latence, coût, conformité).
* **Viewpoint (Point de vue) :** Convention de formalisation fixant la notation, les règles et types de modèles appropriés pour traiter un ensemble de préoccupations (ex: Vue Sécurité, Vue Déploiement).
* **View (Vue) :** Représentation du système selon un point de vue précis pour une partie prenante donnée.

---

# Module 3 : Modélisation et Cartographie du SI

## 3.1 Cartographie des Processus Métier avec BPMN 2.0

BPMN (*Business Process Model and Notation*) normalisé par l'OMG est le standard de référence pour modéliser les processus opérationnels.

### Les Composants Clés de BPMN :

1. **Flow Objects :**
   * *Événements (Cercles) :* Début (vert fin), Intermédiaire (double cercle), Fin (cercle gras).
   * *Activités (Rectangles aux coins arrondis) :* Tâches utilisateur, tâches automatiques (Service Task), sous-processus.
   * *Passerelles (Losanges) :* Exclusive (XOR - choix unique), Parallèle (AND - branches simultanées), Inclusive (OR - une ou plusieurs branches).
2. **Swimlanes (Lignes d'eau) :**
   * *Pool :* Représente une organisation ou entité juridique participante (ex: "Client", "Banque").
   * *Lane :* Sous-division au sein d'une pool (ex: "Service Commercial", "Service Comptabilité").
3. **Connecting Objects :** Flux de séquence (flèche pleine intra-pool), Flux de message (flèche pointillée inter-pools).

```mermaid
sequenceDiagram
    autonumber
    actor Client as 👤 Acheteur (Client)
    participant Front as 🌐 Portail Web E-Commerce
    participant OrderSvc as 📦 Service Commande
    participant StockSvc as 🏬 Service Logistique
    participant PaySvc as 💳 Passerelle Paiement

    Client->>Front: Valider le panier
    Front->>OrderSvc: POST /orders (Créer commande)
    OrderSvc->>StockSvc: Vérifier et réserver stock
    alt Stock insuffisant
        StockSvc-->>OrderSvc: Erreur (Rupture stock)
        OrderSvc-->>Front: Refus commande (Produit indisponible)
    else Stock OK
        StockSvc-->>OrderSvc: Stock réservé
        OrderSvc->>PaySvc: Débiter la carte
        PaySvc-->>OrderSvc: Paiement confirmé (Transaction ID)
        OrderSvc-->>Front: Commande confirmée #12345
        Front-->>Client: Affichage ticket & confirmation
    end
```

---

## 3.2 Modélisation d'Architecture d'Entreprise avec ArchiMate 3.x

Géré par The Open Group, ArchiMate offre un métamodèle unifié connectant la stratégie aux serveurs physiques avec des codes couleurs stricts :

```mermaid
flowchart TD
    subgraph Strat["🟡 COUCHE STRATÉGIE (Strategy Layer)"]
        Course["🎯 Course of Action (Plan)"] --> Cap["⚡ Capability (Capacité Métier)"]
    end

    subgraph Business["🟡 COUCHE MÉTIER (Business Layer)"]
        Actor["👤 Business Actor (Rôle / Acteur)"] --> BProc["🔄 Business Process (Processus)"]
        BProc --> BServ["🏷️ Business Service (Service Métier)"]
    end

    subgraph App["🔵 COUCHE APPLICATIVE (Application Layer)"]
        AComp["🧩 Application Component (Logiciel)"] --> AInt["🔌 Application Interface (API)"]
        AInt --> AServ["🚀 Application Service (Fonction logicielle)"]
    end

    subgraph Tech["🟢 COUCHE TECHNIQUE (Technology Layer)"]
        Node["🖥️ Node (Serveur / VM / Pod)"] --> SysSoft["⚙️ System Software (OS / SGBD)"]
        SysSoft --> TServ["📡 Technology Service (Réseau / Stockage)"]
    end

    subgraph Phys["⚪ COUCHE PHYSIQUE (Physical Layer)"]
        DataCenter["🏢 Facility (Datacenter)"] --> Equip["🔌 Equipment & Distribution Network"]
    end

    Strat ==>|"Oriente"| Business
    Business ==>|"S'appuie sur"| App
    App ==>|"S'exécute sur"| Tech
    Tech ==>|"Est hébergé par"| Phys

    style Strat fill:#fef9c3,stroke:#ca8a04,stroke-width:2px,color:#000
    style Business fill:#fef08a,stroke:#eab308,stroke-width:2px,color:#000
    style App fill:#bae6fd,stroke:#0284c7,stroke-width:2px,color:#000
    style Tech fill:#bbf7d0,stroke:#16a34a,stroke-width:2px,color:#000
    style Phys fill:#f1f5f9,stroke:#64748b,stroke-width:2px,color:#000
```

---

## 3.3 Les 4 Vues Canoniques de l'Urbanisme

```mermaid
flowchart TD
    subgraph V1["1. VUE MÉTIER : Pourquoi & Pour Qui ?"]
        M1["Processus Métier & Activités"]
        M2["Acteurs, Clients, Rôles & Données Métier"]
        M3["Règles de Gestion & Contrats d'Assurance/Vente"]
    end

    subgraph V2["2. VUE FONCTIONNELLE : Que doit faire le système ?"]
        F1["Zones Fonctionnelles (Ventes, Facturation, RH)"]
        F2["Quartiers & Îlots Fonctionnels"]
        F3["Blocs Fonctionnels Indépendants (Agnostiques de la Tech)"]
    end

    subgraph V3["3. VUE APPLICATIVE : Comment le logiciel réalise-t-il la fonction ?"]
        A1["Microservices, ERP, CRM, Portails Web & Mobiles"]
        A2["APIs REST, gRPC, Événements Kafka, ESB"]
        A3["Bases de Données Applicatives (SQL, NoSQL, Cache)"]
    end

    subgraph V4["4. VUE TECHNIQUE : Sur quelles machines & réseaux tout tourne-t-il ?"]
        T1["Clusters Kubernetes, Pods, Conteneurs Docker"]
        T2["Serveurs Physiques, Machines Virtuelles, Cloud Public/Privé"]
        T3["Routeurs, Load Balancers, VPNs, Pare-feu & WAF"]
    end

    V1 ==>|"Détermine les besoins de"| V2
    V2 ==>|"Est instrumenté et automatisé par"| V3
    V3 ==>|"S'exécute physiquement sur"| V4

    style V1 fill:#fef3c7,stroke:#f59e0b,stroke-width:2px,color:#000
    style V2 fill:#dcfce7,stroke:#16a34a,stroke-width:2px,color:#000
    style V3 fill:#e0f2fe,stroke:#0284c7,stroke-width:2px,color:#000
    style V4 fill:#f3e8ff,stroke:#9333ea,stroke-width:2px,color:#000
```

---

# Module 4 : Paradigmes & Styles d'Architecture Logicielle et Applicative

## 4.1 Monolithe vs Architecture Distribuée

```mermaid
graph TD
    subgraph Monolithe["Monolithe Traditionnel"]
        UI["Interface Web"]
        BL["Logique Métier Unique<br>(Facturation, Stock, Clients)"]
        DB[(Base de données unique)]
        UI --- BL
        BL --- DB
    end

    subgraph Microservices["Architecture Microservices"]
        GW["API Gateway"]
        MS1["Service Client"] --> DB1[(DB Client)]
        MS2["Service Commande"] --> DB2[(DB Commande)]
        MS3["Service Facture"] --> DB3[(DB Facture)]
        GW --> MS1
        GW --> MS2
        GW --> MS3
    end

    style Monolithe fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#000
    style Microservices fill:#e0f2fe,stroke:#0284c7,stroke-width:2px,color:#000
```

### Matrice Comparative :

| Caractéristique                      | Architecture Monolithique                                     | Architecture Microservices                                |
| :------------------------------------ | :------------------------------------------------------------ | :-------------------------------------------------------- |
| **Complexité de déploiement** | Simple (un seul binaire/jar/war à déployer)                 | Complexe (nécessite Kubernetes, CI/CD avancée)          |
| **Scalabilité**                | Globale (on duplique tout le monolithe)                       | Granulaire (on scale uniquement le service surchargé)    |
| **Couplage**                    | Fort (risque de code spaghettis et dépendances cachées)     | Faible (communication via des contrats d'API stricts)     |
| **Isolation des pannes**        | Faible (un memory leak dans un module plante tout le serveur) | Forte (un crash du service d'avis n'empêche pas l'achat) |
| **Cohérence des données**     | Transactionnelle immédiate (ACID facile)                     | Éventuelle (Transactions distribuées Saga nécessaires) |

---

## 4.2 Architecture Orientée Services (SOA) & ESB

### Les principes de la SOA :

1. **Contrat standardisé :** Définition formelle (WSDL/XSD en SOAP, OpenAPI en REST).
2. **Couplage lâche :** Les consommateurs ne connaissent pas l'implémentation interne du fournisseur.
3. **Abstraction :** Masque la complexité des systèmes sous-jacents.
4. **Réutilisabilité :** Un service client sert à la fois au web, au mobile et aux agences physiques.
5. **Composabilité :** Les services atomiques s'assemblent pour créer des services composites.

---

## 4.3 Architecture Orientée Événements (EDA) : CQRS & Event Sourcing

Dans une EDA, les composants ne s'appellent pas directement de manière synchrone : ils réagissent à des **événements** (changements d'état significatifs du système).

### Le Pattern CQRS (Command Query Responsibility Segregation) :

Séparation stricte de la **Commande** (écriture, forte cohérence) et de la **Requête** (lecture, optimisée pour l'affichage) :

```mermaid
flowchart LR
    User(["👤 Utilisateur / Client"])

    subgraph WriteSide["ÉCRITURE (Command)"]
        Cmd["Commande<br><i>CreateOrder</i>"] --> Val["Validation Métier & Logique pure"]
        Val --> WriteDB[("💾 Base d'Écriture<br>PostgreSQL (ACID)")]
    end

    subgraph Sync["BUS D'ÉVÉNEMENTS"]
        Broker[["⚡ Apache Kafka<br><i>Event: OrderCreated</i>"]]
    end

    subgraph ReadSide["LECTURE (Query)"]
        ReadDB[("🔍 Base de Lecture<br>Elasticsearch / Redis")] --> Query["Requête<br><i>GetOrderDetails</i>"]
    end

    User -->|"1. Écriture / Modification"| Cmd
    WriteDB -->|"2. Publication d'événement"| Broker
    Broker -->|"3. Projection asynchrone"| ReadDB
    User <-->|"4. Consultation rapide"| Query

    style WriteSide fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#000
    style Sync fill:#fef3c7,stroke:#f59e0b,stroke-width:2px,color:#000
    style ReadSide fill:#dbeafe,stroke:#3b82f6,stroke-width:2px,color:#000
```

---

## 4.4 Architectures Propres (Clean Architecture & Hexagonale)

Conçue par Alistair Cockburn (Architecture Hexagonale) et Robert C. Martin (Clean Architecture), la règle d'or est **l'indépendance de la logique métier vis-à-vis des frameworks, bases de données et interfaces graphiques**.

```mermaid
flowchart TD
    subgraph Acteurs["ACTEURS & DÉCLENCHEURS EXTERNES"]
        Web["🌐 Navigateur Web"]
        Mob["📱 Application Mobile"]
        Cron["⏰ Ordonnanceur Batch"]
    end

    subgraph Hexagone["APPLICATION & DOMAINE MÉTIER"]
        subgraph PortsIn["PORTS D'ENTRÉE (Driving Ports)"]
            PIn["Interfaces des Cas d'Usage"]
        end

        subgraph Core["CŒUR DU DOMAINE"]
            UC["Cas d'Utilisation (Use Cases)"]
            Entities["Entités & Règles Métier Pures<br><i>(Zéro dépendance externe)</i>"]
            UC --> Entities
        end

        subgraph PortsOut["PORTS DE SORTIE (Driven Ports)"]
            POut["Interfaces Répertoires & Services"]
        end

        PIn --> UC
        UC --> POut
    end

    subgraph Infra["INFRASTRUCTURE & DÉPENDANCES TECHNIQUES"]
        SQL[("🗄️ PostgreSQL")]
        Mail["✉️ Service SMTP"]
        Pay["💳 Passerelle Stripe"]
    end

    Web --> PIn
    Mob --> PIn
    Cron --> PIn

    POut --> SQL
    POut --> Mail
    POut --> Pay

    style Core fill:#fef08a,stroke:#ca8a04,stroke-width:2px,color:#000
    style PortsIn fill:#bae6fd,stroke:#0284c7,stroke-width:1.5px,color:#000
    style PortsOut fill:#bae6fd,stroke:#0284c7,stroke-width:1.5px,color:#000
    style Hexagone fill:#f8fafc,stroke:#334155,stroke-width:2px,stroke-dasharray: 5 5,color:#000
```

---

# Module 5 : Architecture des Données (Data Architecture)

## 5.1 Gestion des Données de Référence (MDM)

Dans une grande entreprise, les données critiques (clients, produits, fournisseurs) sont dispersées dans des dizaines d'applications hétérogènes.

* **Problème :** Incohérence, doublons, divergence d'adresses.
* **Solution MDM :** Mettre en place un **Référentiel Unique** établissant le **Golden Record** (la version officielle de référence vérifiée) diffusé aux autres applications.

---

## 5.2 Du Relationnel (ACID) au NoSQL (BASE & Théorème CAP)

### Théorème CAP (Eric Brewer) :

```mermaid
graph TD
    CAP["Théorème CAP"]
    CAP --- CP["Systèmes CP (Cohérence + Partition)<br>Ex: MongoDB, HBase, Spanner"]
    CAP --- AP["Systèmes AP (Disponibilité + Partition)<br>Ex: Cassandra, CouchDB, DynamoDB"]
    CAP --- CA["Systèmes CA (Cohérence + Disponibilité)<br>Théorique sans partitionnement réseau<br>Ex: RDBMS classique monomachine"]

    style CP fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#000
    style AP fill:#dcfce7,stroke:#16a34a,stroke-width:2px,color:#000
    style CA fill:#f1f5f9,stroke:#64748b,stroke-width:2px,color:#000
```

---

## 5.3 L'Évolution du Décisionnel : De l'Entrepôt au Data Mesh

```mermaid
flowchart LR
    G1["1. Data Warehouse<br><i>(1990-2010)</i><br>Données relationnelles<br>ETL batch de nuit"] --> G2["2. Data Lake<br><i>(2010-2020)</i><br>Stockage brut (S3/HDFS)<br>Schema-on-read"]
    G2 --> G3["3. Data Lakehouse<br><i>(2020+)</i><br>ACID + Objets bruts<br>Delta Lake / Iceberg"]
    G3 --> G4["4. Data Mesh<br><i>(Moderne)</i><br>Gouvernance décentralisée<br>Data as a Product"]

    style G1 fill:#f1f5f9,stroke:#64748b,color:#000
    style G2 fill:#e0f2fe,stroke:#0284c7,color:#000
    style G3 fill:#dcfce7,stroke:#16a34a,color:#000
    style G4 fill:#fef08a,stroke:#ca8a04,stroke-width:2px,color:#000
```

---

# Module 6 : Architecture d'Intégration & Échanges Inter-Applicatifs

## 6.1 Panorama des Styles d'APIs

| Protocole                | Modèle de transport          | Format des données         | Cas d'usage recommandé                                                        |
| :----------------------- | :---------------------------- | :-------------------------- | :----------------------------------------------------------------------------- |
| **REST (OpenAPI)** | HTTP/1.1 ou HTTP/2            | JSON, XML                   | APIs publiques, CRUD standard, intégration universelle                        |
| **GraphQL**        | HTTP (généralement POST)    | JSON                        | Applications mobiles & Frontends complexes (évite over/under-fetching)        |
| **gRPC**           | HTTP/2 binaire                | Protocol Buffers (Protobuf) | Communication inter-microservices à très haute performance et faible latence |
| **WebSockets**     | TCP bidirectionnel persistant | Binaire ou Texte            | Tableaux de bord boursiers en direct, chats, télémétrie temps réel         |
| **Webhooks**       | HTTP POST asynchrone          | JSON                        | Notification push d'événement (ex: Stripe validant un paiement)              |

---

## 6.2 API Management (APIM) & Service Mesh

```mermaid
flowchart TD
    Clients["🌐 Clients Externes (Web, Mobile, Tiers)"]

    subgraph Edge["PÉRIMÈTRE EXTERNE (Trafic Nord-Sud)"]
        GW["🚪 API GATEWAY<br><i>(Authentification OAuth2/OIDC, Rate Limiting, WAF, Routing)</i>"]
    end

    subgraph Cluster["CLUSTER INTERNE (Trafic Est-Ouest avec Service Mesh)"]
        subgraph PodA["Microservice Commande"]
            SA["Service Commande"]
            SideA["Sidecar Proxy (Envoy)"]
            SA <--> SideA
        end

        subgraph PodB["Microservice Facturation"]
            SB["Service Facturation"]
            SideB["Sidecar Proxy (Envoy)"]
            SB <--> SideB
        end

        subgraph PodC["Microservice Stock"]
            SC["Service Stock"]
            SideC["Sidecar Proxy (Envoy)"]
            SC <--> SideC
        end

        SideA <== "mTLS Chiffré" ==> SideB
        SideA <== "mTLS Chiffré" ==> SideC
    end

    Clients -->|"HTTPS Public"| GW
    GW -->|"Routage filtré"| SideA

    style Edge fill:#fef3c7,stroke:#f59e0b,stroke-width:2px,color:#000
    style Cluster fill:#e0f2fe,stroke:#0284c7,stroke-width:2px,color:#000
    style PodA fill:#ffffff,stroke:#0369a1,color:#000
    style PodB fill:#ffffff,stroke:#0369a1,color:#000
    style PodC fill:#ffffff,stroke:#0369a1,color:#000
```

---

# Module 7 : Architecture d'Infrastructure, Cloud & Sécurité

## 7.1 Modèles de Service Cloud & Responsabilité Partagée

| Couche d'Infrastructure                 | Sur site (On-Premise) | IaaS (AWS EC2, GCE) | PaaS (App Engine, Heroku) | SaaS (Salesforce, M365) |  Serverless (FaaS)  |
| :-------------------------------------- | :-------------------: | :-----------------: | :-----------------------: | :---------------------: | :-----------------: |
| **Données & Accès**             |     🏢 Entreprise     |    🏢 Entreprise    |       🏢 Entreprise       |      🏢 Entreprise      |    🏢 Entreprise    |
| **Code Applicatif**               |     🏢 Entreprise     |    🏢 Entreprise    |       🏢 Entreprise       |   ☁️ Cloud Provider   |    🏢 Entreprise    |
| **Runtime & Frameworks**          |     🏢 Entreprise     |    🏢 Entreprise    |    ☁️ Cloud Provider    |   ☁️ Cloud Provider   | ☁️ Cloud Provider |
| **Système d'Exploitation (OS)**  |     🏢 Entreprise     |    🏢 Entreprise    |    ☁️ Cloud Provider    |   ☁️ Cloud Provider   | ☁️ Cloud Provider |
| **Virtualisation & Hyperviseur**  |     🏢 Entreprise     | ☁️ Cloud Provider |    ☁️ Cloud Provider    |   ☁️ Cloud Provider   | ☁️ Cloud Provider |
| **Serveurs & Stockage Physique**  |     🏢 Entreprise     | ☁️ Cloud Provider |    ☁️ Cloud Provider    |   ☁️ Cloud Provider   | ☁️ Cloud Provider |
| **Réseau physique & Datacenter** |     🏢 Entreprise     | ☁️ Cloud Provider |    ☁️ Cloud Provider    |   ☁️ Cloud Provider   | ☁️ Cloud Provider |

---

## 7.2 Architecture de Sécurité : Le Modèle Zero Trust (NIST SP 800-207)

```mermaid
flowchart TD
    subgraph Piliers["LES 3 PILIERS DU MODÈLE ZERO TRUST"]
        P1["1. Ne jamais faire confiance, toujours vérifier<br><i>(Authentification MFA + OIDC + Certificats mTLS)</i>"]
        P2["2. Moindre Privilège (Least Privilege)<br><i>(Accès restreint au strict nécessaire, RBAC & ABAC)</i>"]
        P3["3. Supposer la violation (Assume Breach)<br><i>(Micro-segmentation, chiffrement au repos & traçabilité)</i>"]
    end

    style P1 fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#000
    style P2 fill:#fef3c7,stroke:#f59e0b,stroke-width:2px,color:#000
    style P3 fill:#e0f2fe,stroke:#0284c7,stroke-width:2px,color:#000
```

---

# Module 8 : Gouvernance, Trajectoire SI et Schéma Directeur (SDSI)

## 8.1 Élaboration du Schéma Directeur des SI (SDSI)

```mermaid
timeline
    title Démarche d'élaboration d'un Schéma Directeur (SDSI)
    Phase 1 : Diagnostic de l'Existant (As-Is) : Cartographie technique : Dette technique : Coûts récurrents
    Phase 2 : Définition de la Cible (To-Be) : Vision stratégique métier : Principes directeurs d'architecture
    Phase 3 : Analyse des Écarts (Gap Analysis) : Identification des ruptures : Matrice des opportunités
    Phase 4 : Trajectoire & Feuille de Route : Découpage en projets / vagues : Budgets CAPEX/OPEX : Plan de transition
```

---

## 8.2 Rationalisation du Portefeuille Applicatif : Le Modèle TIME du Gartner

```mermaid
flowchart TD
    subgraph Grid["MATRICE TIME DU GARTNER (Rationalisation du Portefeuille)"]
        subgraph TopRow["Haute Valeur Métier"]
            Tolerate["🟡 TOLERATE (Tolérer)<br>Code ancien mais critique pour le métier.<br>Action : On maintient sans investissements majeurs."]
            Invest["🟢 INVEST (Investir)<br>Haute valeur métier & haute qualité technologique.<br>Action : Développer, étendre et enrichir en priorité."]
        end
        subgraph BottomRow["Faible Valeur Métier"]
            Eliminate["🔴 ELIMINATE (Éliminer)<br>Obsolète et sans valeur ajoutée métier.<br>Action : Décommissionner d'urgence pour réduire le TCO."]
            Migrate["🔵 MIGRATE (Migrer / Refondre)<br>Forte utilité mais ruinée techniquement.<br>Action : Réécriture microservices ou remplacement SaaS."]
        end
    end

    style Invest fill:#dcfce7,stroke:#16a34a,stroke-width:2px,color:#000
    style Tolerate fill:#fef9c3,stroke:#ca8a04,stroke-width:2px,color:#000
    style Migrate fill:#e0f2fe,stroke:#0284c7,stroke-width:2px,color:#000
    style Eliminate fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#000
```

---

# Module 9 : Étude de Cas Fil Conducteur & Exercices d'Examen

## Cas Pratique Fil Conducteur : Modernisation de "BankNova"

```mermaid
flowchart LR
    subgraph Canaux["Canaux Clients"]
        Mobile["📱 App Mobile Flutter"]
        Web["💻 Portail Web React"]
    end

    subgraph Security["Zone Sécurisée DMZ"]
        GW["🛡️ API Gateway<br>(OAuth2 / OIDC / MFA)"]
    end

    subgraph CoreCloud["Plateforme Cloud Temps Réel"]
        ODS[("⚡ ODS NoSQL<br>Consultation soldes < 50ms")]
        MS["Microservices Comptes & Virements"]
        Kafka{{"📬 Apache Kafka<br>Events Streaming"}}
    end

    subgraph Legacy["Datacenter Historique"]
        CDC["CDC (Debezium)"]
        MF[("🏛️ Mainframe COBOL<br>Core Banking System")]
    end

    Canaux -->|"HTTPS"| GW
    GW -->|"Lecture solde"| ODS
    GW -->|"Ordre de virement"| MS
    MS -->|"Transaction validée"| Kafka
    Kafka -->|"Mise à jour cache"| ODS
    MF -->|"Capture écritures"| CDC
    CDC -->|"Événements"| Kafka
    Kafka -->|"Batch comptable"| MF

    style Canaux fill:#f1f5f9,stroke:#64748b,color:#000
    style Security fill:#fef3c7,stroke:#f59e0b,color:#000
    style CoreCloud fill:#e0f2fe,stroke:#0284c7,color:#000
    style Legacy fill:#fee2e2,stroke:#ef4444,color:#000
```

---

## QCM & Questions Ouvertes d'Évaluation Master (Avec Corrigés)

### Question 1 (QCM) :

Dans TOGAF ADM, quelle phase s'occupe de concevoir l'architecture des données et des applications ?

* A) Phase A
* B) Phase B
* C) Phase C
* D) Phase D

> **Réponse : C.** La Phase C est l'Architecture des Systèmes d'Information, scindée en *Data Architecture* et *Application Architecture*.

### Question 2 (Analyse d'Architecture) :

*Un développeur propose que le service de Facturation écrive directement dans la table `Commande` du service Commande pour aller plus vite.***Question :** Que lui répond l'Architecte Urbaniste du SI ? Justifiez avec deux principes fondamentaux vus en cours.

> **Réponse attendue :**L'architecte **refuse formellement** cette conception.
>
> 1. **Violation du couplage faible et de l'encapsulation :** Le service Commande doit être le seul maître légitime (*System of Record*) de son modèle de données. Tout accès direct par un composant externe viole la cohésion interne et crée un couplage fort au niveau de la structure SQL. Si le service Commande change de schéma, le service Facturation casse.
> 2. **Règle d'intégration d'urbanisme :** La communication doit impérativement s'effectuer via une interface contractuelle formalisée (API REST synchrone ou message/événement asynchrone dans un broker).

---

*Fin du document de cours — Référentiel Master SI.*
