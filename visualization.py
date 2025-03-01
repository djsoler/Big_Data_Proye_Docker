import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_parquet("processed_weather.parquet")
df.plot(x="timestamp", y="temperature", kind="line", title="Temperatura en Bogotá")
plt.show()