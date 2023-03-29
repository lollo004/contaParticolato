from flask import Flask, render_template
from bson.json_util import dumps
from pymongo import MongoClient
import os

# Ottieni la configurazione del database MongoDB dall'ambiente
mongo_host = os.getenv('MONGODB_HOST', 'localhost')
mongo_port = int(os.getenv('MONGODB_PORT', '27017'))

# Connettiti al database MongoDB
mongo_client = MongoClient(f"mongodb://{mongo_host}:{mongo_port}/db")
print(f"mongodb://{mongo_host}:{mongo_port}/db")
db = mongo_client.mydatabase
collection = db.mydatacollection

# Crea l'app Flask
app = Flask(__name__, template_folder='templates')

# Definisci la route per i dati in formato JSON
@app.route('/data')
def get_data():
    # Recupera i dati dal database
    cursor = collection.find()
    # Restituisci i dati in formato JSON
    return dumps(list(cursor))

# Definisci la route principale dell'app
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
