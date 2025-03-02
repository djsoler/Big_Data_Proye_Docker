from kafka import KafkaProducer
import requests
import json
import time

# Definir las APIs
API_METEO = "https://api.open-meteo.com/v1/forecast?latitude=4.6097&longitude=-74.0817&hourly=temperature_2m"
API_SECOP = "https://www.datos.gov.co/resource/p6dx-8zbt.json"  # API SECOP II

KAFKA_TOPIC_METEO = "weather_data"
KAFKA_TOPIC_SECOP = "secop_data"

# Configurar el productor de Kafka
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

while True:
    # Obtener datos de Open-Meteo
    response_meteo = requests.get(API_METEO)
    if response_meteo.status_code == 200:
        data_meteo = response_meteo.json()
        producer.send(KAFKA_TOPIC_METEO, data_meteo)
        print("Datos METEO enviados a Kafka:", data_meteo)

    # Obtener datos de SECOP II
    response_secop = requests.get(API_SECOP)
    if response_secop.status_code == 200:
        data_secop = response_secop.json()
        producer.send(KAFKA_TOPIC_SECOP, data_secop)
        print("Datos SECOP enviados a Kafka:", data_secop[:3])  # Muestra los primeros 3

    time.sleep(10)  # Esperar 10 segundos

