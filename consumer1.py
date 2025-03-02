from kafka import KafkaConsumer
import json
import pandas as pd
import dask.dataframe as dd
import datetime

KAFKA_TOPIC = "weather_data"
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

data_list = []
for message in consumer:
    data = message.value
    temp_data = data["hourly"]["temperature_2m"]
    df = pd.DataFrame(temp_data, columns=["temperature"])
    df["timestamp"] = pd.to_datetime(datetime.datetime.now())
    data_list.append(df)

    if len(data_list) >= 5:  # Procesa cada 5 mensajes
        ddf = dd.from_pandas(pd.concat(data_list), npartitions=2)
        result = ddf.groupby("timestamp").mean().compute()
        result.to_parquet("processed_weather.parquet")
        print("Datos procesados y guardados")
        data_list = []