from kafka import KafkaConsumer
import json
import pandas as pd

KAFKA_TOPIC = "secop_data"

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

data_list = []
for message in consumer:
    data = message.value
    df = pd.DataFrame(data)  # Convertir a DataFrame
    data_list.append(df)

    if len(data_list) >= 5:  # Procesar cada 5 lotes de datos
        final_df = pd.concat(data_list)
        final_df.to_csv("secop_data.csv", index=False)  # Guardar en CSV
        print("Datos de SECOP II procesados y guardados.")
        data_list = []  # Limpiar lista para el siguiente batch
