# 📄 Bilan de Fin de Projet : Assistant IA Métier Local (DevAssist-GPT)

**Auteur / Binôme :** Master 1 Architecture des Systèmes d'Information (CFA-INSTA)  
**Projet :** Assistant IA Interne Souverain pour TECHCORP  
**Date :** Année Universitaire 2025-2026  

---

## 1. 🎯 Réussites du Projet
- **Souveraineté et Confidentialité Totale :** Le service a été conçu et déployé intégralement en local (Ollama) et sur une machine virtuelle Linux sous VMware ESXi, sans qu'aucune donnée sensible de TECHCORP ne soit transmise à des tiers ou des APIs de Cloud public.
- **Spécialisation Comportementale et Technique :** Grâce au fichier `Modelfile` et à son prompt `SYSTEM` rigoureux, DevAssist-GPT adopte immédiatement le ton, la méthodologie et le niveau d'exigence d'un ingénieur logiciel senior spécialisé en Python, FastAPI et micro-services.
- **Élimination des Hallucinations grâce au RAG :** L'indexation de la documentation interne officielle (API Tickets TECHCORP, conventions de code PEP 8, normes Docker) a permis au modèle de citer avec une fidélité absolue des routes et schémas JSON introuvables sur le web public.
- **Robustesse de l'Infrastructure Docker Compose :** La mise en place de volumes nommés (`ollama_data` et `open_webui_data`) garantit la pérennité des modèles, des comptes utilisateurs et des bases vectorielles après chaque redémarrage.

---

## 2. ⚠️ Limites Identifiées
- **Ressources et Débit d'Inférence (Tokens/seconde) :** En l'absence de GPU dédié sur la VM de laboratoire ESXi, l'inférence du modèle Qwen2.5 7B repose entièrement sur les vCPUs partagés, limitant la vitesse de frappe à environ 12-15 tokens/seconde lors de charges complexes.
- **Gestion des Requêtes Multi-Documents :** Lors de questions croisant simultanément deux procédures volumineuses, la sélection sémantique du RAG doit être finement guidée par des mots-clés explicites pour éviter d'omettre un fragment contextuel.

---

## 3. 🛠️ Erreurs Rencontrées et Solutions Apportées
1. **Échec de communication Open WebUI ➔ Ollama (`Connection Refused`) :**
   - *Problème :* Open WebUI tentait de joindre `localhost:11434`, qui pointait vers le conteneur lui-même.
   - *Solution :* Déclaration de `OLLAMA_BASE_URL=http://ollama:11434` sur le même réseau Docker bridge dans `compose.yml`.
2. **Hallucination initiale sur l'API Tickets sans RAG :**
   - *Problème :* Le modèle de base inventait l'endpoint `POST /tickets/create` avec des champs non conformes.
   - *Solution :* Intégration de la spécification Markdown dans la collection de connaissances RAG et réglage de la température à `0.2`.
3. **Erreur de compilation du modèle dans le conteneur :**
   - *Problème :* Le fichier `Modelfile` n'était pas accessible depuis l'intérieur du conteneur Ollama.
   - *Solution :* Montage d'un volume bind `./workspace:/workspace` permettant d'injecter facilement le Modelfile et d'exécuter `ollama create devassist-gpt -f /workspace/Modelfile`.

---

## 4. 🚀 Axes d'Amélioration & Perspectives
- **Accélération Matérielle (GPU Passthrough) :** Allouer une carte graphique NVIDIA physique à la VM ESXi (vGPU / DDA) pour quadrupler la cadence d'inférence.
- **Connexion MCP (Model Context Protocol) :** Développer un connecteur FastMCP permettant à DevAssist-GPT d'interagir directement avec l'API Tickets (création automatique d'un ticket lors de la détection d'une anomalie critique).
- **Synchronisation CI/CD Documentaire :** Automatiser la mise à jour de la base vectorielle RAG par un webhook lors de chaque commit sur la branche `main` du repository de documentation.
