import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_parquet("processed_weather.parquet")
df.plot(x="timestamp", y="temperature", kind="line", title="Temperatura en Bogotá")
plt.show()


import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("secop_data.csv")

# Convertir columna de valores a numérica
df["valor_contrato"] = pd.to_numeric(df["valor_contrato"], errors="coerce")

# Graficar los valores de contrato por entidad
df.groupby("entidad")["valor_contrato"].sum().nlargest(10).plot(kind="bar", figsize=(10, 5))
plt.title("Top 10 Entidades con Mayor Valor Contratado")
plt.xlabel("Entidad")
plt.ylabel("Valor Total del Contrato")
plt.xticks(rotation=90)
plt.show()
