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
