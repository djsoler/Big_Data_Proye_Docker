from kafka import KafkaConsumer
import json
import pandas as pd
import dask.dataframe as dd
import datetime

# Configurar Consumer para ambos topics
KAFKA_TOPICS = ["weather_data", "secop_data"]
consumer = KafkaConsumer(
    *KAFKA_TOPICS,
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)

# Procesar datos en paralelo con Dask
data_list_meteo = []
data_list_secop = []

for message in consumer:
    topic = message.topic
    data = message.value

    if topic == "weather_data":
        temp_data = data["hourly"]["temperature_2m"]
        df = pd.DataFrame(temp_data, columns=["temperature"])
        df["timestamp"] = pd.to_datetime(datetime.datetime.now())
        data_list_meteo.append(df)

    elif topic == "secop_data":
        df = pd.DataFrame(data)
        df["valor_contrato"] = pd.to_numeric(df["valor_contrato"], errors="coerce")
        data_list_secop.append(df)

    # Guardar cada 5 mensajes
    if len(data_list_meteo) >= 5:
        ddf_meteo = dd.from_pandas(pd.concat(data_list_meteo), npartitions=2)
        ddf_meteo.to_parquet("processed_weather.parquet")
        print("Datos METEO procesados y guardados")
        data_list_meteo = []

    if len(data_list_secop) >= 5:
        ddf_secop = dd.from_pandas(pd.concat(data_list_secop), npartitions=2)
        ddf_secop.to_parquet("processed_secop.parquet")
        print("Datos SECOP procesados y guardados")
        data_list_secop = []
