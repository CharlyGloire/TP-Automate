import json
import time
from datetime import datetime
from flask import Flask, render_template
import paho.mqtt.client as mqtt
from threading import Thread

app = Flask(__name__)

# --- CONFIGURATION MQTT ---
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_PORT = 1883
MQTT_TOPIC = "wokwi-weather"

# Variable globale pour stocker la dernière donnée reçue
# On l'initialise avec des valeurs vides
current_data = {
    "temp": "--",
    "humidity": "--",
    "timestamp": "En attente de données..."
}

# --- FONCTIONS MQTT ---

# Cette fonction se déclenche quand on reçoit un message du broker
def on_message(client, userdata, message):
    global current_data
    try:
        # 1. Décoder le message reçu (de bytes à string)
        payload = message.payload.decode("utf-8")
        print(f"Message reçu : {payload}") # Pour voir dans la console
        
        # 2. Convertir le JSON (texte) en Dictionnaire Python
        data = json.loads(payload)
        
        # 3. Mettre à jour notre variable globale
        current_data["temp"] = data.get("temp")
        current_data["humidity"] = data.get("humidity")
        
        # 4. AJOUTER L'HEURE (car l'ESP32 ne l'envoie pas)
        now = datetime.now()
        current_data["timestamp"] = now.strftime("%d/%m/%Y à %H:%M:%S")
        
    except Exception as e:
        print(f"Erreur lors de la lecture du message : {e}")

def start_mqtt():
    client = mqtt.Client()
    client.on_message = on_message
    
    print("Connexion au broker MQTT...")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    
    client.subscribe(MQTT_TOPIC)
    print(f"Abonné au topic : {MQTT_TOPIC}")
    
    # Lance une boucle infinie pour écouter, mais sans bloquer le reste du code
    client.loop_start()

# --- PARTIE FLASK (SITE WEB) ---

@app.route('/')
def index():
    # On envoie la variable 'current_data' à la page HTML
    return render_template('index.html', meteo=current_data)

if __name__ == '__main__':
    # On démarre le module MQTT avant de lancer le serveur web
    start_mqtt()
    
    # On lance le serveur web Flask
    # debug=True permet de voir les erreurs, use_reloader=False évite de lancer MQTT deux fois
    app.run(debug=True, port=5000, use_reloader=False)