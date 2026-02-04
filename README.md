

```markdown
# Système de Surveillance Météo IoT - Architecture Distribuée

**Étudiant :** LOBANDJI LOPAKA Charles  
**Cours :** Programmation Distribuée  
**Projet :** Station Météo Connectée (ESP32 / MQTT / Flask)

---

## 1. Présentation du Projet
Ce projet consiste en une application IoT complète permettant de récupérer, traiter et afficher des données environnementales (température et humidité) en temps réel. L'architecture repose sur une communication distribuée utilisant le protocole MQTT entre un automate simulé et un serveur web Flask.

## 2. Architecture du Système
Le système suit un modèle de communication Publish/Subscribe :
1. **Le Terminal (Edge) :** Un microcontrôleur ESP32 simulé sur Wokwi. Il mesure les données via un capteur DHT22 et les publie au format JSON.
2. **Le Broker (Middleware) :** Le serveur public HiveMQ (`broker.mqttdashboard.com`) qui centralise et redirige les messages.
3. **Le Client (Application) :** Une application Python utilisant le framework Flask. Elle s'abonne au flux de données, ajoute un horodatage local et sert les informations via une interface web.



## 3. Structure du Répertoire
```text
projet_meteo/
│
├── app.py                # Serveur Flask et logique client MQTT
├── requirements.txt      # Dépendances Python (flask, paho-mqtt)
└── templates/            # Dossier contenant les vues HTML
    └── index.html        # Interface utilisateur (Dashboard)

```

## 4. Prérequis et Installation

### Simulation

* Accès à la simulation Wokwi via le lien fourni dans le code source de l'automate.

### Installation Locale

1. Cloner ce dépôt ou copier les fichiers dans un dossier local.
2. Installer les bibliothèques requises via le terminal :
```bash
pip install flask paho-mqtt

```



## 5. Fonctionnement Technique

### Connexion et Flux de Données

* **Liaison MQTT :** La liaison entre l'automate et le script Python est établie via l'adresse du Broker (`broker.mqttdashboard.com`) sur le port `1883`. Ils communiquent via un canal spécifique appelé topic : `wokwi-weather`.
* **Récupération des données :** Le script `app.py` utilise la bibliothèque `paho-mqtt`. La fonction `on_message` intercepte les paquets arrivant sur le broker, décode le JSON et stocke les valeurs dans une variable globale.

### Interface Web

* **Flask :** Le framework Python gère le serveur web local.
* **Jinja2 :** Le moteur de template permet d'injecter les données de température et d'humidité directement dans le fichier `index.html`.
* **Horodatage :** L'heure affichée sur le dashboard est générée par le serveur Python au moment précis de la réception du message MQTT.

## 6. Guide d'Exécution

1. Lancer la simulation sur **Wokwi** et s'assurer que l'ESP32 affiche "Connected".
2. Exécuter le serveur Python :
```bash
python app.py

```


3. Ouvrir un navigateur à l'adresse suivante : `http://127.0.0.1:5000`
4. Modifier les curseurs de température/humidité sur Wokwi pour voir les données se mettre à jour sur le dashboard web.

---

© 2026 - LOBANDJI LOPAKA Charles

```

