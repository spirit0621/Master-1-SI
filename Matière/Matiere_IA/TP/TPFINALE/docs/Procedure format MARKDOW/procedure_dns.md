# 📋 Procédure d'Exploitation TECHCORP : Incident DNS Critique

> **Identifiant :** `PROC-NET-DNS-001`  
> **Niveau de criticité :** `CRITICAL` / `HIGH`  
> **Dernière mise à jour :** Septembre 2026  
> **Source :** [procedures/procedure_dns.txt](file:///c:/Users/alves/Desktop/Lyc%C3%A9e,%20bts%20,%20formation,%20master/CFA-insta/Master%201%20SI/TP/TPFINALE/procedures/procedure_dns.txt)

---

## 1. Contexte et Impact

Le service DNS interne (`SRV-DNS-01` — `192.168.56.53`) assure la résolution de noms pour l'ensemble des serveurs applicatifs et de base de données.

En cas de défaillance DNS :

- Les applications ne peuvent plus joindre les services par leur hostname.
- Des erreurs de timeout ou de connexion `'host unreachable'` apparaissent dans les logs.

---

## 2. Vérifications Immédiates (Niveau 1 Support)

### a. Tester la joignabilité réseau de SRV-DNS-01

```bash
ping -c 3 192.168.56.53
```

### b. Vérifier l'écoute du port 53 (UDP / TCP)

```bash
nc -zvu 192.168.56.53 53
```

### c. Tester une résolution directe

```bash
dig @192.168.56.53 srv-app-01.techcorp.local +short
```

---

## 3. Procédure de Remédiation (Niveau 2 Réseau / Système)

### a. Connexion d'administration

Se connecter en console ou SSH d'administration sur `SRV-DNS-01`.

### b. Vérifier l'état du démon DNS (bind9 ou named)

```bash
systemctl status bind9
```

### c. Redémarrage du service si arrêté ou en échec

```bash
systemctl restart bind9
```

### d. Consultation des logs techniques

Consulter les 50 dernières lignes de logs :

```bash
journalctl -u bind9 -n 50 --no-pager
```

---

## 4. Escalade et Communication

- Si la panne persiste plus de 10 minutes : escalader immédiatement à l'astreinte Réseau (Responsable Astreinte).
- Créer un ticket incident prioritaire `CRITICAL` dans l'outil de gestion des tickets avec le titre : *"Indisponibilité résolveur DNS principal SRV-DNS-01"*.
- Informer les équipes applicatives de basculer temporairement sur le DNS de secours secondaire (`192.168.56.54`) si configuré.
