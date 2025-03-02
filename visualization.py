import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos desde Parquet
df_meteo = pd.read_parquet("processed_weather.parquet")
df_secop = pd.read_parquet("processed_secop.parquet")

# Graficar temperatura
df_meteo.plot(x="timestamp", y="temperature", kind="line", title="Temperatura en Bogotá")
plt.show()

# Graficar contratos más altos
df_secop["valor_contrato"] = pd.to_numeric(df_secop["valor_contrato"], errors="coerce")
df_secop.groupby("entidad")["valor_contrato"].sum().nlargest(10).plot(
    kind="bar", figsize=(10, 5)
)
plt.title("Top 10 Entidades con Mayor Valor Contratado")
plt.xlabel("Entidad")
plt.ylabel("Valor Total del Contrato")
plt.xticks(rotation=90)
plt.show()
