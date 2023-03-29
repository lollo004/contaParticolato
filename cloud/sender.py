import paho.mqtt.client as mqtt
from datetime import datetime
import time
import random
import json

# definisci la funzione di callback quando si stabilisce la connessione con il broker MQTT
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

# definisci il broker MQTT e il topic
broker_address = "mqtt.ssh.edu.it"
topic = "borghi"

# crea un client MQTT e assegna la funzione di callback
client = mqtt.Client()
client.on_connect = on_connect

# connettiti al broker MQTT
client.connect(broker_address, 1883, 60)

# datetime object containing current date and time
now = datetime.now()

# dd/mm/YY H:M:S
# dt_string = now.strftime("%d/%m %H:%M:%S")
# print("date and time =", dt_string)

# invia dati di temperatura e umidità di prova al broker MQTT ogni 5 secondi
while True:
    # genera dati casuali di temperatura e umidità nel formato specificato
    now = datetime.now()
    data = {
        "timestamp": now.strftime("%d/%m %H:%M:%S"),
        "temperature": round(random.uniform(15, 25), 2),
        "humidity": round(random.uniform(40, 60), 2),
        "UV": round(random.uniform(0, 10), 2),
        "water": round(random.uniform(0, 1), 2)
    }
    
    # converte i dati in formato JSON
    formatted_data = {
        'timestamp': data['timestamp'],
        'temperature': data['temperature'],
        'humidity': data['humidity'],
        'UV': data['UV'],
        'water': data['water']
    }
    payload = json.dumps(formatted_data)
    
    # pubblica i dati sul topic specificato
    client.publish(topic, payload)
    
    # attendi 5 secondi prima di inviare i dati successivi
    time.sleep(5)