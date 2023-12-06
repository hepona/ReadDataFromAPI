import requests
from Meteo import Meteoapi
from sys import argv
from dotenv import load_dotenv
import os
import paho.mqtt.client as mqtt
import time
import json

#load api key from .env
load_dotenv()

iot_hub = "mqtt.thingsboard.cloud"
port = 1883
username = os.getenv('tb_token')
password = ""
topic = "v1/devices/me/telemetry"

iot_hub_client = mqtt.Client()
iot_hub_client.username_pw_set(username, password)
iot_hub_client.connect(iot_hub, port)
iot_hub_client.loop_start() # start the MQTT client's network loop
print("---Connected to iot_hub---")

while True:
    # Vérifier que le nom de la ville à été saisie
    try:
        if len(argv) < 2:
            print("Veuillez indiquer le nom de la ville")
            print("Usage: <nom de ville>")
            exit(1)

        url = f"http://api.openweathermap.org/data/2.5/weather?appid={os.getenv('api_key')}&q={argv[1]}"

        resp = requests.get(url)
        data = resp.json()

        if resp.status_code == 200:
            # dans le cas où la ville existe
            temp = data['main']['temp']
            hum =  data['main']['humidity']
            wspeed = data['wind']['speed']
            city = data['name']

            m1 = Meteoapi(temp, hum, wspeed, city)

            print("Your city: {}".format(m1.name))
            print("{} temperature: {:.2f}°C, Humidity: {}%, wind speed: {}km/h".format(m1.name, m1.temptocels(), m1.hum, m1.wspeed))

            d = dict()
            d["City"] = str(m1.name)
            d["temperature"] = float(m1.temptocels())
            d["humidity"] = float(m1.hum)
            d["wind_speed"] = float(m1.wspeed)
            data_out = json.dumps(d)
            iot_hub_client.publish(topic, data_out, 0)
            print(data_out)

            time.sleep(1)
        else:
            # dans le cas où la ville n'existe pas
            print(f"Erreur {resp.status_code}: {data.get('message', 'Erreur inconnue')}")
            print(f"Response content: {resp.content.decode('utf-8')}")
    except Exception as e:
        print(e)