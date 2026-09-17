# 📋 Procédure Générale d'Escalade des Incidents Techniques TECHCORP

> **Identifiant :** `PROC-OPS-GEN-002`  
> **Champ d'application :** Équipes Support N1, Exploitation Système & Réseau  
> **Source :** [procedures/procedure_incidents.txt](file:///c:/Users/alves/Desktop/Lyc%C3%A9e,%20bts%20,%20formation,%20master/CFA-insta/Master%201%20SI/TP/TPFINALE/procedures/procedure_incidents.txt)

---

## 1. Classification des Priorités

- **`CRITICAL` :** Service de production indisponible (ex : PostgreSQL `SRV-DB-01` inaccessible, DNS indisponible).
- **`HIGH` :** Dégradation de performance majeure ou redondance perdue.
- **`MEDIUM` :** Dysfonctionnement partiel sans interruption de service globale.
- **`LOW` :** Anomalie mineure ou demande de maintenance préventive.

---

## 2. Règle d'Arbitrage entre Inventaire et Mesure Technique

- L'état déclaré en inventaire (CMDB) est indicatif et historique.
- Seule la sonde temps réel (socket TCP ou ping vérifié) fait foi pour l'état d'exploitation en direct.
- **Si contradiction constatée (Inventaire `UP` mais Socket `DOWN`) :**
  1. Notifier immédiatement la discordance formelle dans le diagnostic.
  2. Vérifier l'état du port cible (ex : port `5432` pour PostgreSQL, port `80`/`443` pour Nginx).
  3. Vérifier les erreurs récentes dans la table `events`.
  4. Ne jamais conclure à la panne d'une machine sans avoir testé à la fois l'hôte et son service applicatif.
