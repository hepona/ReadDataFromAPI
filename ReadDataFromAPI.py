#!/usr/bin/python3
# Bibliothèque pour effectuer des requêtes HTTP
import requests

# Module personnalisé 'Meteo' contenant la classe Meteoapi pour gérer les données météorologiques
from Meteo import Meteoapi

# Bibliothèque pour gérer les arguments de la ligne de commande
from sys import argv

# Bibliothèque pour charger les variables d'environnement depuis un fichier .env
from dotenv import load_dotenv

# Bibliothèque pour interagir avec le système d'exploitation, utilisée ici pour obtenir les variables d'environnement
import os

# Bibliothèque client MQTT (Message Queuing Telemetry Transport) pour la communication avec ThingsBoard
import paho.mqtt.client as mqtt

# Bibliothèque pour introduire des délais, utilisée pour ajouter une pause entre les requêtes API
import time

# Bibliothèque pour travailler avec des données JSON
import json

# load api key from .env
load_dotenv()

# connexion to thingboard.cloud
iot_hub = "mqtt.thingsboard.cloud"
port = 1883
username = os.getenv("tb_token")
password = ""
topic = "v1/devices/me/telemetry"

try:
    iot_hub_client = mqtt.Client()
    iot_hub_client.username_pw_set(username, password)
    iot_hub_client.connect(iot_hub, port)
    print(iot_hub_client.connect(iot_hub, port))
    iot_hub_client.loop_start()  # start the MQTT client's network loop
    print("---Connected to Thingboard---")
except Exception as e:
    print(e)
    exit(1)

# Get data from openweathermap constally
while True:
    # check if the  city name has been entered

    if len(argv) < 2:
        print("Veuillez indiquer le nom de la ville")
        print("Usage: <nom de ville>")
        exit(
            1
        )  # exit the program with error message if the city doesn'r exist with code 1

    url = f"http://api.openweathermap.org/data/2.5/weather?appid={os.getenv('api_key')}&q={argv[1]}"

    # send a request  to openweathermap
    resp = requests.get(url)
    # stock it in a variable in json format
    data = resp.json()
    if resp.status_code == 200:
        # if the city exist (code statue == 200) stock data in variable
        print(data)
        temp = data["main"]["temp"]
        hum = data["main"]["humidity"]
        wspeed = data["wind"]["speed"]
        wdirection = data["wind"]["deg"]
        city = data["name"]
        # create object m1 from Meteoapi class and pirnt in the shell
        m1 = Meteoapi(temp, hum, wspeed, wdirection, city)
        print("Your city: {}".format(m1.name))
        print(
            "{} temperature: {:.2f}°C, Humidity: {}%, wind speed: {}km/h".format(
                m1.name, m1.temptocels(), m1.hum, m1.wspeed
            )
        )
        # create a dictionary with  all the data gotten from openweathermap
        d = dict()
        d["City"] = str(m1.name)
        d["temperature"] = float(m1.temptocels())
        d["humidity"] = float(m1.hum)
        d["speed"] = float(m1.wspeed)
        d["direction"] = float(m1.wdirection)
        data_out = json.dumps(d)
        # send the data dictionnary to Thingboard
        iot_hub_client.publish(topic, data_out, 0)
        print(data_out)

        time.sleep(10)
    if resp.status_code != 200:
        # if the does not exist (code statue != 200 ) print code statue and the error
        print(f"Erreur {resp.status_code}: {data.get('message', 'Erreur inconnue')}")
        print(f"Response content: {resp.content.decode('utf-8')}")
        break
