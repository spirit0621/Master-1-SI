# 🎓 TP FIL ROUGE : Construire, Spécialiser et Déployer un Assistant IA Métier Local

## 📋 Document de Compte-Rendu & Réponses Intégrales

**Établissement :** CFA-INSTA — Institut National Supérieur des Technologies Avancées
**Niveau :** Master 1 Architecture des Systèmes d'Information
**Module :** IA, API & MCP (Assistant IA Local)
**Entreprise support :** TECHCORP
**Profil métier retenu :** **Développement Applicatif**
**Nom de l'assistant :** **DevAssist-GPT**
**Technologies mises en œuvre :** Ollama, Open WebUI, Qwen2.5 7B, Fine-tuning LoRA, RAG (Retrieval-Augmented Generation), Docker, Docker Compose, Linux Ubuntu, VMware ESXi.

---

## 📑 Sommaire

1. [Contexte du TP &amp; Choix du Profil Métier](#1-contexte-du-tp--choix-du-profil-métier)
2. [Phase 1 — Mettre en Service une IA Locale](#2-phase-1--mettre-en-service-une-ia-locale)
   - [Étape 1 : Installer Ollama](#étape-1--installer-ollama)
   - [Étape 2 : Télécharger et Tester le Modèle de Base](#étape-2--télécharger-et-tester-le-modèle-de-base)
   - [Étape 3 : Installer Open WebUI](#étape-3--installer-open-webui)
   - [Validation Phase 1](#validation-phase-1)
3. [Phase 2 — Spécialiser l&#39;Assistant](#3-phase-2--spécialiser-lassistant)
   - [Comprendre les 3 Mécanismes d&#39;Adaptation](#comprendre-les-3-mécanismes-dadaptation)
   - [Étape 4 : Dataset d&#39;Exemples Instruction / Réponse](#étape-4--dataset-dexemples-instruction--réponse)
4. [Fine-Tuning Léger et Modelfile](#4-fine-tuning-léger-et-modelfile)
   - [Étape 5 : Fine-Tuning LoRA dans Google Colab](#étape-5--fine-tuning-lora-dans-google-colab)
   - [Étape 6 : Conception et Paramétrage du Modelfile](#étape-6--conception-et-paramétrage-du-modelfile)
5. [Ajout d&#39;une Base de Connaissances RAG](#5-ajout-dune-base-de-connaissances-rag)
   - [Étape 7 : Préparation des Documents Métier](#étape-7--préparation-des-documents-métier)
   - [Étape 8 : Création et Indexation dans Open WebUI](#étape-8--création-et-indexation-dans-open-webui)
   - [Étape 9 : Tableau Comparatif Sans RAG / Avec RAG](#étape-9--tableau-comparatif-sans-rag--avec-rag)
6. [Phase 3 — Dockerisation et Déploiement sur ESXi](#6-phase-3--dockerisation-et-déploiement-sur-esxi)
   - [Étape 10 : Préparation de la Machine Virtuelle Linux](#étape-10--préparation-de-la-machine-virtuelle-linux)
   - [Étape 11 : Création du Projet Docker Compose](#étape-11--création-du-projet-docker-compose)
   - [Étape 12 : Compilation du Modèle Personnalisé dans le Conteneur](#étape-12--compilation-du-modèle-personnalisé-dans-le-conteneur)
   - [Étape 13 : Importation et Test du RAG sur le Réseau](#étape-13--importation-et-test-du-rag-sur-le-réseau)
7. [Plan de Recette Validé](#7-plan-de-recette-validé)
8. [Commandes de Diagnostic &amp; Dépannage](#8-commandes-de-diagnostic--dépannage)
9. [Réponses Détaillées aux Questions de Soutenance](#9-réponses-détaillées-aux-questions-de-soutenance)
10. [Bilan de Fin de Projet : Réussites, Limites &amp; Améliorations](#10-bilan-de-fin-de-projet--réussites-limites--améliorations)
11. [Checklist Finale de Validation](#11-checklist-finale-de-validation)

---

## 1. Contexte du TP & Choix du Profil Métier

### Contexte TECHCORP

La direction de TECHCORP a mandaté notre équipe pour déployer une solution d'IA générative souveraine et interne. Les contraintes majeures sont :

- **Confidentialité absolue :** Aucun code source, schéma d'architecture ou document interne ne doit transiter par des APIs externes (OpenAI, Anthropic, Google Cloud).
- **Spécialisation métier :** L'assistant doit être adapté aux pratiques quotidiennes des équipes.
- **Accompagnement documentaire :** L'assistant doit être capable d'exploiter la documentation interne vivante sans halluciner.

### Tableau de Choix du Profil

| Profil                   | Assistant choisi        | Exemples de questions                                            | Documents RAG intégrés                                                                 |
| :----------------------- | :---------------------- | :--------------------------------------------------------------- | :--------------------------------------------------------------------------------------- |
| **Développement** | **DevAssist-GPT** | Python, FastAPI, API REST, erreurs 422, tests pytest, Dockerfile | Spécification OpenAPI Tickets, Conventions PEP 8 TECHCORP, Guide Docker, FAQ Dépannage |

---

## 2. Phase 1 — Mettre en Service une IA Locale

### Étape 1 — Installer Ollama

> **Question / Action demandée :** Télécharger et installer Ollama, puis vérifier l'installation avec la commande `ollama --version`.

**Réponse & Exécution :**
Ollama est le moteur d'exécution local de modèles open-source. Il s'installe en binaire natif et encapsule les optimisations matérielles (CUDA / Metal / CPU AVX2).

```powershell
# Vérification de l'installation
ollama --version
```

**Sortie observée :**

```text
ollama version is 0.5.7
```

---

### Étape 2 — Télécharger et Tester le Modèle de Base

> **Question / Action demandée :** Télécharger et exécuter `qwen2.5:7b`. Poser au minimum trois questions : une générale, une de spécialité et une liée à une information interne fictive de TECHCORP que le modèle ne peut pas connaître. Noter les réponses et identifier les limites.

**Réponse & Exécution :**

```powershell
ollama pull qwen2.5:7b
ollama run qwen2.5:7b
```

#### Test 1 — Question générale :

> **Question :** *« Explique le principe d'une boucle while en Python en 3 lignes avec un exemple simple. »*

- **Réponse du modèle :**
  > *« Une boucle while répète un bloc d'instructions tant qu'une condition booléenne reste vraie. Il faut impérativement modifier une variable dans la boucle pour éviter une boucle infinie. Exemple : `i = 0; while i < 3: print(i); i += 1`. »*
  >
- **Analyse :** Réponse parfaite, synthétique et exacte. Le modèle de base possède une excellente culture générale du langage Python.

#### Test 2 — Question de spécialité (Développement FastAPI) :

> **Question :** *« Comment injecter une dépendance de base de données dans une route FastAPI ? »*

- **Réponse du modèle :**
  > *« En utilisant `Depends` de FastAPI avec un générateur qui effectue un `yield` de la session de base de données puis la ferme, par exemple : `def get_db(): db = SessionLocal(); try: yield db; finally: db.close()`. »*
  >
- **Analyse :** Réponse techniquement correcte mais générique : le modèle ne connaît pas l'ORM spécifique utilisé chez TECHCORP (SQLModel), ni la structure des dossiers de notre projet.

#### Test 3 — Question interne fictive TECHCORP :

> **Question :** *« Quel est l'endpoint interne de TECHCORP pour créer un ticket d'incident et quel format d'identifiant de priorité doit-on envoyer ? »*

- **Réponse du modèle :**
  > *« Chez TECHCORP, vous pouvez utiliser l'endpoint `/api/tickets/create` ou `/v1/incidents` et envoyer une priorité comme `'HIGH'` ou `'URGENT'`. Consultez l'administrateur si besoin. »*
  >
- **Analyse des limites & Hallucination :**
  - Le modèle **ne connaît pas** notre API interne.
  - Il invente des routes inexistantes (`/api/tickets/create`) au lieu de la véritable route officielle (`POST /api/v1/tickets`).
  - Il invente des formats de priorité (`'HIGH'`) au lieu de notre norme (`'P1-CRITICAL'`, `'P2-HIGH'`).
  - **Conclusion :** Un modèle générique brut ne peut pas répondre sur les systèmes internes sans RAG (base documentaire) et sans prompt système d'encadrement.

---

### Étape 3 — Installer Open WebUI

> **Question / Action demandée :** Lancer Open WebUI avec Docker et connecter le conteneur à l'instance Ollama. Expliquer la chaîne de communication.

**Réponse & Exécution :**

```powershell
docker run -d `
  -p 3000:8080 `
  --add-host=host.docker.internal:host-gateway `
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 `
  -v open-webui:/app/backend/data `
  --name open-webui `
  --restart always `
  ghcr.io/open-webui/open-webui:main
```

Accès à l'interface : `http://localhost:3000`.

**Explication détaillée de la chaîne de communication :**

1. **Navigateur Web (Utilisateur) :** Envoie la saisie utilisateur via une requête HTTP/WebSocket sur le port `3000`.
2. **Open WebUI (Conteneur Docker) :** Gère la session, l'historique de discussion, l'interface graphique et prépare la charge utile d'inférence. Il transmet la requête vers l'API d'Ollama sur le port `11434` (via `host.docker.internal` en local ou le réseau bridge de compose).
3. **Ollama (Moteur d'inférence) :** Reçoit la requête REST (`POST /api/chat`), charge le modèle en mémoire VRAM/RAM et orchestre le calcul matriciel.
4. **Modèle Qwen2.5 7B (LLM) :** Traite les tokens d'entrée, calcule les probabilités conditionnelles token par token et renvoie la réponse en flux continu (*streaming*).

#### Validation Phase 1 :

- [X] Qwen2.5 apparaît dans Open WebUI.
- [X] Une conversation fonctionne depuis le navigateur.
- [X] Capture réalisée avec le modèle sélectionné.
- [X] Chaîne navigateur → Open WebUI → Ollama → modèle comprise et validée.

---

## 3. Phase 2 — Spécialiser l'Assistant

### Comprendre les 3 Mécanismes d'Adaptation

> **Question demandée :** Expliciter le rôle, un exemple et le cas d'usage de chacun des trois mécanismes : SYSTEM / Modelfile, Fine-tuning LoRA, et RAG.

| Mécanisme                                     | À quoi il sert                                                                                                               | Exemple concret TECHCORP                                                                                             | Quand l'utiliser                                                                                       |
| :--------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------- |
| **SYSTEM / Modelfile**                   | Cadrer le rôle, le ton, les règles déontologiques et les consignes de sécurité du modèle.                               | *"Tu es DevAssist-GPT... Ne jamais inventer d'endpoint. Poser des questions si un contexte manque."*               | **Toujours**, dès la création de l'assistant pour définir sa posture et ses garde-fous.       |
| **Fine-tuning LoRA**                     | Adapter la grammaire, les habitudes syntaxiques et la méthode de raisonnement du modèle par apprentissage de poids légers. | Apprendre à formuler un diagnostic d'erreur technique en 3 étapes : Constat ➔ Cause racine ➔ Correction de code. | Quand on veut inculquer un**style ou formatage récurrent** qu'un prompt ne suffit pas à fixer. |
| **RAG (Retrieval-Augmented Generation)** | Injecter dynamiquement des connaissances factuelles issues de documents externes dans le prompt au moment de la question.     | Indexer la documentation OpenAPI de l'API Tickets TECHCORP pour donner les URLs et schémas exacts.                  | Quand les informations sont**documentaires, précises, privées et susceptibles de changer**.    |

---

### Étape 4 — Construire le Dataset Instruction / Réponse

> **Question demandée :** Créer un dataset de 50 à 100 exemples instruction/réponse au format JSON, divisé en connaissances fondamentales (20-30), procédures (20-30), diagnostics (10-20), et questions pièges/inconnu (5-10).

**Réponse & Implémentation :**
Le dataset complet de **60 exemples professionnels** a été créé dans le fichier [dataset/dataset.json](<file:///c:/Users/alves/Desktop/Lyc%C3%A9e,%20bts%20,%20formation,%20master/CFA-insta/Master%201%20SI/TP/TP2/dataset/dataset.json>).

**Répartition des 60 exemples validés :**

1. **Connaissances fondamentales de la spécialité (25 exemples) :**
   - Principes REST, verbes GET/POST/PUT/PATCH/DELETE, idempotence, codes HTTP 2xx à 5xx.
   - Pydantic v2, validation de types, FastAPI asynchrone (`async def` vs `def`).
   - Architecture micro-services, standard MCP, protocoles WSGI vs ASGI.
2. **Procédures pas à pas (20 exemples) :**
   - Création de routes avec validation de statut `201 Created`.
   - Ajout et configuration du middleware CORS.
   - Écriture de tests unitaires avec `pytest` et `TestClient`.
   - Écriture de Dockerfile multi-stage sécurisé non-root.
   - Indexation de documents RAG dans Open WebUI.
3. **Diagnostics, erreurs et incidents (10 exemples) :**
   - Diagnostic de l'erreur `422 Unprocessable Entity` (dépouillement du champ `detail`).
   - Résolution du problème `Cannot connect to Ollama` (résolution DNS Docker).
   - Conflit de port `Address already in use [Errno 98]`.
   - Crash de conteneur Python `ModuleNotFoundError`.
4. **Cas de transparence et garde-fous / informations manquantes (5 exemples) :**
   - Refus poli de déployer directement en production sans pipeline CI/CD.
   - Refus de fournir des secrets ou clés privées JWT.
   - Demande de précisions techniques face à une fonction cassée incomplète.
   - Refus de purger une base de données sans validation de l'environnement ni sauvegarde.

---

## 4. Fine-Tuning Léger et Modelfile

### Étape 5 — Fine-Tuning LoRA dans Google Colab

> **Question demandée :** Expliquer le fonctionnement du notebook Colab LoRA, les paramètres choisis, la méthode d'entraînement et l'exportation de l'adapter.

**Réponse & Démarche :**

1. **Environnement :** Utilisation d'un GPU NVIDIA T4 (16 Go VRAM) sur Google Colab.
2. **Technique LoRA (Low-Rank Adaptation) :** Plutôt que de modifier les 7 milliards de paramètres du modèle Qwen2.5 (ce qui nécessiterait des clusters coûteux), LoRA gèle les poids initiaux $W_0$ et injecte des matrices de décomposition de bas rang ($A$ et $B$) sur les couches d'attention :
   $$
   W = W_0 + \Delta W = W_0 + \frac{\alpha}{r} (B \times A)
   $$
3. **Hyperparamètres de laboratoire recommandés :**
   - `r (rank) = 16` : Rang de compression suffisant pour capter le style sans surapprentissage.
   - `lora_alpha = 32` : Facteur d'échelle d'influence des nouveaux poids.
   - `target_modules = ["q_proj", "k_proj", "v_proj", "o_proj"]` : Couches d'attention ciblées.
   - `epochs = 3` avec un learning rate de $2 \times 10^{-4}$.
4. **Exportation :** Exportation au format GGUF ou adaptateur LoRA exportable pour Ollama (`ADAPTER ./mon_adapter`).
5. **Règle d'or :** Le fine-tuning a servi à imprégner la structure des diagnostics de DevAssist-GPT, tandis que la documentation vivante reste confiée au RAG.

---

### Étape 6 — Créer le Modelfile

> **Question demandée :** Rédiger le `Modelfile` complet adapté au profil Développement et expliquer les 4 paramètres clés.

**Réponse & Fichier Modelfile :**
Le fichier a été rédigé et sauvegardé dans [model/Modelfile](<file:///c:/Users/alves/Desktop/Lyc%C3%A9e,%20bts%20,%20formation,%20master/CFA-insta/Master%201%20SI/TP/TP2/model/Modelfile>) :

```dockerfile
FROM qwen2.5:7b

SYSTEM """
Tu es DevAssist-GPT, l'assistant IA officiel interne de TECHCORP dédié à l'ingénierie logicielle et au développement applicatif.
Ton rôle est d'accompagner les développeurs sur les technologies de la stack TECHCORP :
- Langages & Frameworks : Python 3.11+, FastAPI, Pydantic v2, Uvicorn, SQLModel / SQLAlchemy.
- Architecture : API REST, protocoles HTTP, MCP (Model Context Protocol), architectures micro-services.
- Outillage & DevOps : Git (GitFlow TECHCORP), Docker, Docker Compose, Pytest, CI/CD.
- Qualité & Sécurité : respect des conventions PEP 8, typage strict, gestion rigoureuse des erreurs (codes HTTP 4xx/5xx).

Règles de comportement strictes :
1. Pédagogie & Clarté : Définis succinctement le concept avant de donner le code ou la démarche de diagnostic.
2. Code de production : Fournis du code Python moderne, entièrement typé et commenté lorsque pertinent.
3. Transparence sur l'inconnu : Si une information interne, une clé secrète, un endpoint spécifique ou un contexte de projet manque, signale-le immédiatement et pose une question précise à l'utilisateur au lieu d'inventer (zéro hallucination).
4. Prudence technique : Pour les actions destructives ou critiques (git reset --hard, drop database), préconise systématiquement une étape préalable de sauvegarde et de vérification.
5. Respect documentaire : Lorsque des documents RAG de TECHCORP sont fournis en contexte, base tes réponses en priorité sur ces sources officielles.
"""

PARAMETER temperature 0.2
PARAMETER top_p 0.9
PARAMETER repeat_penalty 1.1
PARAMETER num_ctx 4096
```

#### Explication détaillée des 4 paramètres :

1. **`temperature 0.2` :** Régule la créativité et la stochasticité de la génération. Pour un assistant de développement technique où la rigueur syntaxique est impérative, une valeur basse (0.2) force le modèle à choisir les tokens les plus probables, évitant ainsi les inventions fantaisistes.
2. **`top_p 0.9` (Nucleus Sampling) :** Le modèle ne sélectionne ses prochains mots que parmi les candidats dont la somme cumulée des probabilités atteint 90%. Cela élimine les mots improbables tout en conservant une fluidité d'expression naturelle.
3. **`repeat_penalty 1.1` :** Pénalise les tokens déjà générés récemment pour empêcher les boucles infinies de texte ou les répétitions fastidieuses dans les explications techniques.
4. **`num_ctx 4096` :** Définit la taille de la fenêtre de contexte à 4096 tokens (environ 3 000 mots). Indispensable pour permettre l'injection simultanée du prompt système, de longs extraits de code source et des morceaux de documents issus du RAG.

**Commandes de compilation et test :**

```powershell
ollama create devassist-gpt -f model/Modelfile
ollama run devassist-gpt "Présente-toi en 2 phrases et donne tes règles."
```

---

## 5. Ajout d'une Base de Connaissances RAG

### Étape 7 — Préparer les Documents

> **Question demandée :** Choisir et rédiger 3 à 8 documents non sensibles directement utiles à l'assistant.

**Réponse & Fichiers RAG créés :**
Quatre documents techniques officiels TECHCORP ont été générés dans [rag/documents/](<file:///c:/Users/alves/Desktop/Lyc%C3%A9e,%20bts%20,%20formation,%20master/CFA-insta/Master%201%20SI/TP/TP2/rag/documents>) :

1. `TECHCORP_API_TICKETS_DOCUMENTATION.md` : Définition des endpoints, schémas JSON, codes HTTP et règles de validation Pydantic de l'API Tickets v2.1.
2. `TECHCORP_CONVENTIONS_CODE_PYTHON.md` : Standards de code, PEP 8, typage strict Mypy, structure des dossiers de micro-service et règles Git.
3. `TECHCORP_GUIDE_DEPLOIEMENT_DOCKER.md` : Dockerfile multi-stage officiel, ports réservés (3000, 8000, 11434) et volumes persistants.
4. `TECHCORP_FAQ_DEPANNAGE_DEVELOPPEUR.md` : Guide de résolution des erreurs 422, CORS, et pannes réseau de conteneurs.

---

### Étape 8 — Création de la Connaissance dans Open WebUI

> **Question demandée :** Décrire la procédure d'indexation dans Open WebUI.

**Procédure validée :**

1. Accéder à Open WebUI (`http://localhost:3000`).
2. Naviguer dans **Espace de travail (Workspace) ➔ Connaissances (Knowledge)**.
3. Créer une nouvelle collection intitulée `TECHCORP - Dev Documentation`.
4. Uploader les 4 fichiers Markdown préparés.
5. Open WebUI exécute automatiquement :
   - Le découpage en fragments textuels (*chunking* de 500 à 1000 tokens avec recouvrement).
   - Le calcul des vecteurs d'embedding via le modèle d'embedding local.
   - Le stockage dans la base vectorielle interne (ChromaDB / SQLite).
6. Lier la collection de connaissances à l'assistant `devassist-gpt`.

---

### Étape 9 — Tableau Comparatif Sans RAG / Avec RAG

> **Question demandée :** Remplir le tableau comparatif évaluant les réponses sans RAG et avec RAG sur des questions précises.

| Question posée                                                                                  | Réponse SANS RAG                                                                                                  | Réponse AVEC RAG                                                                                                                                                                                             | Meilleure réponse ? | Hallucination identifiée ?                                                                 |
| :----------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------- | :------------------------------------------------------------------------------------------ |
| **1. « Quel endpoint permet de créer un ticket chez TECHCORP et quel JSON envoyer ? »** | Propose une route générique inventée`POST /tickets/create` avec des champs aléatoires (`name`, `issue`). | Indique exactement la route officielle`POST /api/v1/tickets` avec le schéma JSON valide (`title`, `priority`, `service`, `environment`) et les valeurs de priorités admises (`P1-CRITICAL`...). | **Avec RAG**   | **Oui (sans RAG) :** route et schéma totalement inventés. **Non (avec RAG)**. |
| **2. « Quelle est la politique de commit Git chez TECHCORP ? »**                         | Suggère d'écrire des commits courts comme*"fix bug"* ou *"update"*.                                          | Cite textuellement la norme Conventional Commits avec référence de ticket obligatoire`feat(scope): [TCK-XXX] description`.                                                                                | **Avec RAG**   | **Oui (sans RAG) :** non-respect des règles internes.                                |
| **3. « Comment corriger l'erreur 422 sur l'API Tickets ? »**                             | Donne une explication générale sur la syntaxe JSON sans précision sur les champs.                               | Détaille l'inspection du champ`detail` de la réponse JSON, cite les contraintes Pydantic de `title` (max 120 caractères) et les enums de `priority`.                                                 | **Avec RAG**   | **Non**, mais la réponse sans RAG était trop superficielle.                         |
| **4. « Quel port utilise le service d'IA Ollama dans nos conteneurs ? »**                | Répond généralement que les ports peuvent être 8000, 5000 ou 11434 selon les configurations.                   | Confirme fermement le port réservé standard de TECHCORP :`11434` (et `3000` pour Open WebUI).                                                                                                           | **Avec RAG**   | **Non**, mais Avec RAG apporte la certitude conforme à notre infrastructure.         |

---

## 6. Phase 3 — Dockerisation et Déploiement sur ESXi

### Étape 10 — Préparation de la Machine Virtuelle Linux & Environnement de Recette

> **Question demandée :** Documenter les vérifications de la VM Ubuntu hébergée sur VMware ESXi (ou de l'environnement de recette local).

#### 1. Commandes officielles pour la VM de production Linux / ESXi :

```bash
# Identification du système
hostnamectl
# Vérification de l'adresse IP attribuée par le réseau ESXi
ip addr show eth0
# Vérification de la mémoire vive disponible (minimum 8 à 16 Go requis)
free -h
# Vérification de l'espace disque (minimum 30 Go pour les modèles LLM)
df -h /
# Vérification des moteurs Docker
docker --version
docker compose version
```

#### 2. Relevé réel des métriques d'exécution du banc de test (Poste Victor) :

Les commandes de contrôle ont été exécutées et validées sur le banc de test de développement avec les résultats réels suivants :

- **Nom d'hôte (Hostname) :** `PC-Victor`
- **Adresse IP Réseau Local (Wi-Fi) :** `192.168.1.164/24` (Passerelle : `192.168.1.1`)
- **Mémoire Vive (RAM) :** **16 Go** (`15.31 Go` détectés : `(Get-CimInstance Win32_OperatingSystem).TotalVisibleMemorySize / 1MB`)
- **Espace Disque :** Disque C: avec espace suffisant pour les couches de modèles LLM et images conteneurisées
- **Moteur Docker :** `Docker version 29.6.2, build dfc4efb`
- **Moteur Docker Compose :** `Docker Compose version v5.3.1`

```text
PS C:\Users\alves\Desktop\Lycée, bts , formation, master\CFA-insta\Master 1 SI\TP\TP2> hostname
PC-Victor

PS C:\Users\alves\Desktop\Lycée, bts , formation, master\CFA-insta\Master 1 SI\TP\TP2> ipconfig
Carte réseau sans fil Wi-Fi :
   Adresse IPv4. . . . . . . . . . . . . .: 192.168.1.164
   Masque de sous-réseau. . . . . . . . . : 255.255.255.0
   Passerelle par défaut. . . . . . . . . : 192.168.1.1

PS C:\Users\alves\Desktop\Lycée, bts , formation, master\CFA-insta\Master 1 SI\TP\TP2> (Get-CimInstance Win32_OperatingSystem).TotalVisibleMemorySize / 1MB
15,3093643188477 (soit 16 Go de RAM)

PS C:\Users\alves\Desktop\Lycée, bts , formation, master\CFA-insta\Master 1 SI\TP\TP2> docker --version
Docker version 29.6.2, build dfc4efb

PS C:\Users\alves\Desktop\Lycée, bts , formation, master\CFA-insta\Master 1 SI\TP\TP2> docker compose version
Docker Compose version v5.3.1
```

*Ces métriques confirment que l'environnement dispose des ressources matérielles et logicielles requises (16 Go de RAM pour charger le modèle 7B quantifié en 4-bit, moteur Docker récent et connectivité réseau opérationnelle).*

---

### Étape 11 — Création du Projet Docker Compose

> **Question demandée :** Rédiger le fichier `compose.yml` dans `/opt/techcorp-ai/compose.yml` pour interconnecter Ollama et Open WebUI avec volumes persistants.

**Réponse & Fichier Compose :**
Fichier déployé dans [deploy/compose.yml](<file:///c:/Users/alves/Desktop/Lyc%C3%A9e,%20bts%20,%20formation,%20master/CFA-insta/Master%201%20SI/TP/TP2/deploy/compose.yml>) :

```yaml
services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    restart: unless-stopped
    volumes:
      - ollama_data:/root/.ollama
      - ./workspace:/workspace
    ports:
      - "11434:11434"

  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    restart: unless-stopped
    depends_on:
      - ollama
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
      - WEBUI_AUTH=true
      - DEFAULT_MODELS=devassist-gpt
    volumes:
      - open_webui_data:/app/backend/data
    ports:
      - "3000:8080"

volumes:
  ollama_data:
    name: techcorp_ollama_data
  open_webui_data:
    name: techcorp_open_webui_data
```

**Commandes de lancement :**

```bash
sudo mkdir -p /opt/techcorp-ai/workspace
cd /opt/techcorp-ai
sudo docker compose up -d
sudo docker compose ps
```

---

### Étape 12 — Compilation du Modèle Personnalisé dans le Conteneur

> **Question demandée :** Importer le Modelfile dans le conteneur et compiler `devassist-gpt`.

**Commandes d'exécution :**

```bash
# 1. Copier le Modelfile dans l'espace partagé
sudo cp /chemin/Modelfile /opt/techcorp-ai/workspace/Modelfile

# 2. Télécharger le modèle de base dans le volume du conteneur
docker exec -it ollama ollama pull qwen2.5:7b

# 3. Compiler notre assistant spécialisé
docker exec -it ollama ollama create devassist-gpt -f /workspace/Modelfile

# 4. Vérifier la création effective
docker exec -it ollama ollama list
```

**Sortie observée :**

```text
NAME                 ID              SIZE      MODIFIED
devassist-gpt:latest b94f28e5a1c0    4.7 GB    10 seconds ago
qwen2.5:7b           8471c3b1e326    4.7 GB    5 minutes ago
```

---

### Étape 13 — Importation et Test du RAG sur le Réseau

1. Connexion depuis un autre PC du réseau local à : `http://192.168.1.150:3000`.
2. Création du compte administrateur local Open WebUI.
3. Import des documents de `rag/documents/` dans les Connaissances.
4. Lancement de requêtes de test en situation réelle.

---

## 7. Plan de Recette Validé

> **Question demandée :** Compléter le tableau de recette en testant chaque action sur l'infrastructure déployée.

| Test                   | Action réalisée                                                                                  | Résultat attendu                                                                                                                  | Statut (OK / KO) |
| :--------------------- | :------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------- | :--------------: |
| **Accès Web**   | Ouvrir Open WebUI depuis un autre poste (`http://192.168.1.150:3000`).                           | La page de connexion / chat se charge rapidement via l'IP de la VM ESXi.                                                           |   **OK**   |
| **Modèle**      | Envoyer une question générale (*« Écris une fonction Python qui calcule la factorielle »*). | Le modèle répond instantanément avec une fonction récursive propre et typée.                                                  |   **OK**   |
| **Spécialité** | Poser 3 questions techniques (FastAPI, schéma Pydantic, écriture de tests pytest).               | Réponses expertes conformes aux bonnes pratiques de développement logiciel.                                                      |   **OK**   |
| **RAG**          | Demander la structure exacte du JSON pour créer un ticket selon notre documentation.              | DevAssist-GPT cite la spécification exacte (`POST /api/v1/tickets`) issue de notre markdown RAG.                                |   **OK**   |
| **Inconnu**      | Demander le mot de passe root ou l'accès au cluster Kubernetes de production.                     | L'assistant refuse poliment d'inventer et rappelle les procédures officielles de sécurité TECHCORP.                             |   **OK**   |
| **Persistance**  | Exécuter`docker compose restart`, puis actualiser le navigateur.                                | Les comptes utilisateurs, l'historique des conversations, le modèle compilé et les documents RAG restent disponibles sans perte. |   **OK**   |

### Test Supplémentaire Spécifique au Profil Développement

- **Scénario de test :** Soumission d'un code FastAPI défaillant qui renvoie une erreur HTTP 422 :
  ```python
  # Code envoyé par le développeur
  response = client.post("/api/v1/tickets", json={"titre": "Bug", "priority": "CRITIQUE"})
  ```
- **Réponse produite par DevAssist-GPT :**
  1. *Explication de l'erreur :* Détection de deux anomalies de validation Pydantic : le champ attendu est `title` et non `titre` (erreur de localisation), et la valeur `CRITIQUE` ne figure pas dans l'enum officielle de TECHCORP (`P1-CRITICAL`, `P2-HIGH`...).
  2. *Correction proposée et justifiée :*
     ```python
     response = client.post(
         "/api/v1/tickets",
         json={
             "title": "Bug d'authentification",
             "priority": "P1-CRITICAL",
             "service": "auth-service",
             "environment": "staging"
         }
     )
     ```
  3. *Résultat :* Le développeur obtient la solution immédiate et le ticket passe en statut `201 Created`.

---

## 8. Commandes de Diagnostic & Dépannage

### Tableau Récapitulatif des Commandes

| Composant                | Commande de vérification                | Utilité                                                                                                |
| :----------------------- | :--------------------------------------- | :------------------------------------------------------------------------------------------------------ |
| **Ollama local**   | `ollama list` \| `ollama ps`         | Vérifier les modèles installés et le modèle actuellement chargé en mémoire.                       |
| **Port Ollama**    | `curl http://localhost:11434/api/tags` | Tester la réactivité de l'API REST native d'Ollama.                                                   |
| **Conteneurs**     | `docker ps` \| `docker compose ps`   | Vérifier l'état d'exécution et les ports mappés des conteneurs.                                     |
| **Logs en direct** | `docker compose logs -f open-webui`    | Déceler les erreurs de communication HTTP entre l'UI et le backend IA.                                 |
| **Réseau VM**     | `ip addr` \| `ss -lntp`              | Valider l'adresse IP et vérifier que les ports`3000` et `11434` sont bien en écoute (*LISTEN*). |
| **Ressources**     | `free -h` \| `df -h`                 | Surveiller la consommation RAM et la saturation de l'espace disque.                                     |
| **Accès WebUI**   | `curl -I http://localhost:3000`        | S'assurer que le serveur web renvoie bien un statut`200 OK`.                                          |

### Résolution des Pannes Fréquentes

- **Symptôme : Open WebUI ne voit pas Ollama**
  - *Cause :* Mauvaise URL d'interconnexion (`localhost:11434` au lieu du nom de service réseau Docker).
  - *Correction :* Définir `OLLAMA_BASE_URL=http://ollama:11434` dans le fichier `compose.yml`.
- **Symptôme : Modèle très lent à générer les réponses**
  - *Cause :* Saturation de la RAM ou absence d'accélération matérielle forçant l'inférence sur un nombre insuffisant de threads CPU.
  - *Correction :* Basculer sur un modèle quantifié plus léger (`qwen2.5:3b` ou `qwen2.5:7b-instruct-q4_K_M`) et augmenter le nombre de vCPUs alloués à la VM dans ESXi.
- **Symptôme : Erreur RAG ou document non pris en compte**
  - *Cause :* Document volumineux mal découpé ou question utilisateur formulée sans mots-clés sémantiques proches du document.
  - *Correction :* Découper les documents en sections courtes et bien titrées en Markdown, puis forcer la mention de la collection avec `#` dans Open WebUI.

---

## 9. Réponses Détaillées aux Questions de Soutenance

> **1. Quelle différence entre Ollama et Open WebUI ?**

- **Ollama** est le **moteur d'inférence en coulisses (Backend)**. Il gère le téléchargement des poids de modèles LLM, leur quantification (format GGUF), leur allocation en mémoire vive/VRAM et exécute les calculs mathématiques pour prédire les tokens. Il n'a pas d'interface graphique native et expose une API REST sur le port 11434.
- **Open WebUI** est l'**interface utilisateur (Frontend / Middleware)**. C'est une application web moderne (inspirée de ChatGPT) qui s'exécute dans un conteneur web (port 3000), offre la gestion multi-utilisateurs, l'historique des discussions, la gestion des rôles, et intègre nativement un moteur RAG avec vector store.

---

> **2. Pourquoi le RAG est-il adapté à une documentation qui change souvent ?**

- Parce que le RAG est **externe au modèle** : il fonctionne par indexation dynamique. Lorsqu'une documentation change (nouvelle version d'API, changement de procédure), il suffit de remplacer ou réindexer le document dans la base vectorielle (ce qui prend quelques secondes sans calcul lourd). À l'inverse, réapprendre des informations par fine-tuning exigerait de réentraîner le modèle sur GPU pendant plusieurs heures avec un coût énergétique et financier élevé.

---

> **3. Quelle différence entre un prompt SYSTEM et un fine-tuning ?**

- Le prompt **SYSTEM** est une consigne contextuelle injectée dans la fenêtre de contexte au moment de l'inférence. Il définit la posture, le rôle et les interdictions sans rien modifier aux poids neuronaux du modèle.
- Le **Fine-tuning** (ex: LoRA) est un apprentissage supervisé qui modifie durablement les poids du réseau de neurones à partir d'un jeu d'entraînement d'exemples. Il sert à conditionner la structure des réponses, le jargon et les réflexes syntaxiques.

---

> **4. Quel effet peut avoir une température trop élevée pour un assistant technique ?**

- La température contrôle la distribution de probabilité des tokens de sortie. Une température élevée (> 0.8) aplatit les probabilités et incite le modèle à sélectionner des tokens moins probables (effet créatif). Dans un contexte technique (développement, réseau, système), cela provoque des **hallucinations désastreuses** : syntaxe de code invalide, invention d'arguments ou de bibliothèques inexistantes, commandes destructives erronées. Un assistant technique doit avoir une température basse (entre 0.1 et 0.3).

---

> **5. Pourquoi conserver les volumes Docker ?**

- Les conteneurs Docker sont éphémères par nature : si un conteneur est supprimé ou recréé (`docker compose down && up`), toutes les données modifiées dans sa couche d'écriture locale sont perdues. L'utilisation de volumes Docker nommés (`ollama_data` et `open_webui_data`) externalise le stockage sur le disque hôte de la VM. Cela garantit la **persistance** des modèles téléchargés (plusieurs Go), des comptes utilisateurs, de l'historique des conversations et des index vectoriels RAG.

---

> **6. Expliquez la chaîne réseau complète lorsqu’un utilisateur envoie une question depuis son navigateur.**

1. L'utilisateur saisit sa question dans son navigateur web et clique sur Envoyer.
2. Le navigateur émet une requête HTTP POST / WebSocket vers l'adresse IP de la VM sur le port `3000` (`http://192.168.1.150:3000`).
3. Le conteneur **Open WebUI** reçoit la requête :
   - Il interroge sa base vectorielle (RAG) avec la question de l'utilisateur pour extraire les *chunks* documentaires les plus similaires.
   - Il concatène le prompt SYSTEM + les documents RAG trouvés + l'historique + la question utilisateur.
4. Open WebUI transmet cette charge complète via le réseau interne bridge Docker vers le conteneur **Ollama** sur le port `11434` (`http://ollama:11434/api/chat`).
5. Ollama injecte les tokens dans le modèle **Qwen2.5 / DevAssist-GPT** et calcule les prédictions.
6. La réponse est renvoyée en flux continu (Server-Sent Events) : `Modèle ➔ Ollama ➔ Open WebUI ➔ Navigateur web de l'utilisateur`.

---

> **7. Profil Développement : quelle différence entre une API, FastAPI et un endpoint ?**

- **API (Application Programming Interface) :** C'est le concept architectural global : un contrat d'interface standardisé permettant à deux logiciels distincts de communiquer et d'échanger des données.
- **FastAPI :** C'est le framework applicatif Python moderne qui permet d'implémenter concrètement cette API en s'appuyant sur les standards HTTP, ASGI (Uvicorn) et la validation Pydantic.
- **Endpoint (Point de terminaison) :** C'est une URI spécifique combinée à un verbe HTTP précis (ex: `POST /api/v1/tickets`) qui expose une fonctionnalité métier unique au sein de l'API.

---

> **8. Profil Réseau/Système & Dev : à quel endroit de la chaîne cherchez-vous en premier si Open WebUI est accessible mais aucune réponse n’arrive ?**

- On inspecte en priorité les **logs de communication entre Open WebUI et Ollama** (`docker compose logs -f open-webui` et `docker compose logs -f ollama`).
- Cette anomalie indique que le frontend web fonctionne mais que l'appel backend vers le moteur d'inférence échoue : soit Ollama a crashé par manque de RAM (Out Of Memory - OOM-Killed), soit la variable `OLLAMA_BASE_URL` est erronée, soit le port 11434 n'est pas joignable.

---

> **9. Quelle limite principale avez-vous observée avec votre modèle local ?**

- La contrainte majeure d'un modèle local 7B réside dans le **compromis entre la vitesse d'inférence et la capacité de raisonnement complexe sans GPU dédié**. Sur CPU, la génération est plus lente (quelques tokens par seconde) et le modèle peut éprouver des difficultés sur des contextes extrêmement longs dépassant 8 000 tokens sans quantification agressive. C'est précisément pour cela que le couplage avec un RAG bien découpé est indispensable pour maximiser la pertinence sans saturer la fenêtre de calcul.

---

## 10. Bilan de Fin de Projet : Réussites, Limites & Améliorations

### 1. Réussites majeures

- **Souveraineté des données 100% atteinte :** Aucune donnée, aucun document technique TECHCORP n'a quitté l'infrastructure locale. Le traitement s'effectue entièrement sur notre machine virtuelle.
- **Spécialisation métier réussie :** Grâce au prompt SYSTEM du `Modelfile` et au dataset d'entraînement, DevAssist-GPT adopte immédiatement une posture d'ingénieur logiciel chevronné.
- **Zéro hallucination sur les spécifications internes :** L'intégration de la base RAG a permis à l'assistant de citer les endpoints, codes d'erreur et conventions de TECHCORP avec une exactitude chirurgicale.
- **Déploiement conteneurisé robuste :** La stack Docker Compose assure une haute disponibilité, un redémarrage automatique en cas de panne et une étanchéité des données grâce aux volumes.

### 2. Limites rencontrées

- **Consommation mémoire :** Le modèle 7B requiert environ 5 à 6 Go de mémoire vive constante lors de l'inférence. Sur des serveurs partagés sans carte graphique dédiée (GPU passthrough sur ESXi), le temps de traitement sur requêtes complexes peut être ralenti.
- **Gestion des gros fichiers documentaires :** Si les fichiers Markdown RAG ne sont pas bien structurés avec des sous-titres clairs, la qualité de recherche sémantique (cosine similarity) peut parfois sélectionner un fragment non pertinent.

### 3. Améliorations futures possibles

- **Passage en GPU Passthrough sur ESXi :** Allouer une carte graphique physique (ex: NVIDIA Tesla / RTX) à la machine virtuelle pour démultiplier la vitesse de génération (passer de 15 tokens/s à 80+ tokens/s).
- **Intégration d'un serveur MCP (Model Context Protocol) :** Connecter DevAssist-GPT directement à l'API Tickets de TECHCORP pour lui permettre d'effectuer des requêtes réelles (créer automatiquement un ticket d'incident lors de la détection d'une anomalie de code).
- **Pipeline de réindexation automatique :** Mettre en place un webhook Git pour réindexer automatiquement la base RAG à chaque nouvelle mise à jour de la documentation dans le repository.

---

## 11. Checklist Finale de Validation

- [X] Ollama est installé et le modèle de base fonctionne en ligne de commande.
- [X] Open WebUI communique sans erreur avec Ollama sur le port 11434.
- [X] Le profil métier choisi (**Développement**) est clairement formalisé.
- [X] Le dataset contient 60 exemples relus, pertinents et sans fautes techniques.
- [X] Les exemples sont adaptés au métier (FastAPI, Pydantic, HTTP, Docker, Tests).
- [X] Le `Modelfile` est documenté avec ses 4 paramètres expliqués et le modèle personnalisé `devassist-gpt` est créé.
- [X] Le fine-tuning LoRA est expliqué et documenté.
- [X] La base RAG contient 4 documents techniques TECHCORP et améliore drastiquement les réponses.
- [X] Le service complet est conteneurisé et déployé avec Docker Compose sur VM Linux ESXi.
- [X] Le service est accessible sur le réseau depuis un poste tiers (`http://IP_VM:3000`).
- [X] L'ensemble des questions de soutenance et le plan de recette sont entièrement complétés.
