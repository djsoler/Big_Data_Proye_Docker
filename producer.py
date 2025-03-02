from kafka import KafkaProducer
import requests
import json
import time

# API de SECOP II
SECOP_API_URL = "https://www.datos.gov.co/resource/p6dx-8zbt.json"
KAFKA_TOPIC = "secop_data"

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

while True:
    response = requests.get(SECOP_API_URL)
    if response.status_code == 200:
        data = response.json()
        producer.send(KAFKA_TOPIC, data)
        print("Datos de SECOP II enviados a Kafka:", data[:2])  # Solo mostramos los primeros 2 registros
    else:
        print("Error al obtener datos de SECOP II:", response.status_code)

    time.sleep(10)  # Enviar datos cada 10 segundos
