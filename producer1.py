from kafka import KafkaProducer
import requests
import json
import time

API_URL = "https://api.open-meteo.com/v1/forecast?latitude=4.6097&longitude=-74.0817&hourly=temperature_2m"
KAFKA_TOPIC = "weather_data"

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

while True:
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        producer.send(KAFKA_TOPIC, data)
        print("Datos enviados a Kafka:", data)
    time.sleep(10)  # Envía datos cada 10 segundos


import requests

url = "https://www.datos.gov.co/resource/p6dx-8zbt.json"

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    print("Ejemplo de datos recibidos:", data[:5])  # Muestra los primeros 5 registros
else:
    print("Error al obtener los datos:", response.status_code)


from kafka import KafkaProducer
import json
import requests
import time

# Configurar el productor de Kafka
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

topic = "secop_data"
url = "https://www.datos.gov.co/resource/p6dx-8zbt.json"

while True:
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for record in data[:5]:  # Enviar solo los primeros 5 registros para prueba
            producer.send(topic, record)
            print("Enviado a Kafka:", record)
    else:
        print("Error al obtener datos:", response.status_code)

    time.sleep(60)  # Esperar 1 minuto antes de la siguiente consulta
