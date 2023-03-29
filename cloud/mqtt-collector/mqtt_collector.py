import paho.mqtt.client as mqtt
from pymongo import MongoClient
import json
import os

# Ottieni la configurazione del broker MQTT dall'ambiente
mqtt_host = os.getenv('MQTT_HOST', 'localhost')
mqtt_port = int(os.getenv('MQTT_PORT', '1883'))
mqtt_topic = os.getenv('MQTT_TOPIC', 'borghi')

# Ottieni la configurazione del database MongoDB dall'ambiente
mongo_host = os.getenv('MONGODB_HOST', 'localhost')
mongo_port = int(os.getenv('MONGODB_PORT', '27017'))

# Connettiti al database MongoDB
mongo_client = MongoClient(f"mongodb://{mongo_host}:{mongo_port}/db")
print(f"mongodb://{mongo_host}:{mongo_port}/db")
db = mongo_client.mydatabase
collection = db.mydatacollection

# Definisci la funzione di callback per la connessione al broker MQTT
def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
    client.subscribe(mqtt_topic)

# Definisci la funzione di callback per la ricezione dei messaggi dal broker MQTT
def on_message(client, userdata, msg):
    print('Received message on topic ' + msg.topic + ': ' + str(msg.payload))
    
    # Parsa i dati JSON dal messaggio MQTT
    data = json.loads(msg.payload.decode('utf-8'))
    
    # Modifica il formato dei dati
    formatted_data = {
        'timestamp': data['timestamp'],
        'temperature': data['temperature'],
        'humidity': data['humidity'],
        'UV': data['UV'],
        'water': data['water']
    }
    
    # Scrivi i dati nel database MongoDB
    result = collection.insert_one(formatted_data)
    print('Inserted data with id ' + str(result.inserted_id))

# Crea il client MQTT e connettiti al broker
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_host, mqtt_port, 60)

# Avvia il loop di ricezione messaggi
client.loop_forever()
