"""Proyecto: Análisis Avanzado de Ventas
Descripción:
El objetivo de este proyecto es realizar un análisis detallado de las ventas de una empresa
para obtener información útil sobre el rendimiento de los productos y las regiones.
Analizarás datos de ventas y generarás informes que ayuden a comprender mejor las tendencias y
patrones en las ventas.

Requerimientos:

Datos de Entrada:

Archivos CSV con datos de ventas que incluyen información sobre productos, regiones,
 fechas de ventas y cantidades.
Tareas:






6. Generación de Reportes:

Crea reportes en formato CSV o Excel que resuman tus hallazgos:
Un reporte con ventas totales y promedio por región.
Un reporte con ventas totales y promedio por producto.
Incluye gráficos en los reportes si es posible.
Entregables:

Código Python (.py) que realiza las tareas descritas.
Archivos CSV o Excel con los reportes generados.
Gráficos en formato PNG o PDF que visualicen los datos analizados.
Opcional:

Si te sientes cómodo, considera agregar análisis de tendencias estacionales o
predictivas usando técnicas básicas de series temporales."""
from wsgiref.handlers import format_date_time

import pandas as pd
from operator import index
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
"""1. Carga y Limpieza de Datos:
Carga los datos desde los archivos CSV en un DataFrame utilizando pandas.
Realiza una limpieza inicial de los datos, manejando valores nulos y asegurándote de que
todos los tipos de datos sean correctos."""
#LEER ARCHIVOS
df_enero= pd.read_csv("ventas_enero.csv")
df_febrero=pd.read_csv("ventas_febrero.csv")
df_marzo=pd.read_csv("ventas_marzo.csv")
df_ventas=pd.concat([df_enero,df_febrero,df_marzo],ignore_index=True)

print(df_ventas)
#LIMPIEZA
#df_ventas_limpia= df_ventas[df_ventas.notnull().all(axis=1)].reset_index(drop=True)
df_ventas["Ventas"]=pd.to_numeric(df_ventas["Ventas"],errors="coerce")
df_ventas["Clientes"]=pd.to_numeric(df_ventas["Clientes"],errors="coerce")
df_ventas["Categoría"]=df_ventas["Categoría"].replace("",pd.NA).fillna("No especificado")
df_ventas_limpia= df_ventas.dropna().reset_index(drop=True)
print(f"\n\n{df_ventas_limpia}")

"""2. Transformación de Datos:

Añade columnas adicionales si es necesario (por ejemplo, convertir fechas a un formato adecuado,
 añadir categorías de productos si no están presentes)."""

df_ventas_limpia["Fecha"]=pd.to_datetime(df_ventas_limpia["Fecha"],format="%Y-%m-%d")
df_ventas_limpia["Fecha"].dt.strftime("%d-%m-%y")
df_ventas_limpia.sort_values(by=["Fecha"],ascending=True)
print(f"\n\n{df_ventas_limpia}")

"""3. Análisis por Región:

Agrupa los datos por región y calcula las siguientes métricas:
Ventas totales por región.
Ventas promedio por región.
Número total de transacciones por región."""

df_ventas_region=df_ventas_limpia.groupby("Región").agg({
    "Ventas" : "sum",
    "Clientes": "sum"
}).reset_index()
print(df_ventas_region)
#VENTAS TOTALES POR REGION
df_ventas_totales_region=df_ventas_region[["Región","Ventas"]]
print(df_ventas_totales_region)
#VENTAS PROMEDIO POR REGION
df_ventas_promedio_region= df_ventas_region[["Región"]].copy().reset_index()
df_ventas_promedio_region["Ventas Promedio"]=df_ventas_region["Ventas"]/df_ventas_region["Clientes"]
print(df_ventas_promedio_region)
#TRANSACCIONES POR REGION
df_trans_region=df_ventas_limpia.groupby("Región").size().reset_index(name="Numero de transacciones")
print(df_trans_region)

"""4. Análisis por Producto:
Agrupa los datos por producto y calcula las siguientes métricas:
Ventas totales por producto.
Ventas promedio por producto.
Número total de transacciones por producto."""
df_ventas_productos=df_ventas_limpia.groupby("Producto").agg({
    "Ventas":"sum",
    "Clientes":"sum"}).reset_index()
#VENTAS TOTALES POR PRODUCTO
df_ventas_totales_producto=df_ventas_productos[["Producto","Ventas"]]
#VENTAS PROMEDIO POR PRODUCTO
df_ventas_promedio_producto=df_ventas_productos[["Producto"]].copy().reset_index()
df_ventas_promedio_producto["Ventas Promedio"]=df_ventas_productos["Ventas"]/df_ventas_productos["Clientes"]
#NUMERO TOTAL DE TRANSACCIONES POR PRODUCTO
df_trans_producto=df_ventas_limpia.groupby("Producto").size().reset_index(name="Numero de transacciones")
print(df_trans_producto)

"""5. Visualización de Datos:
Usa matplotlib o seaborn para crear gráficos que muestren:
Tendencias de ventas a lo largo del tiempo para cada región.
Comparaciones de ventas entre regiones.
Comparaciones de ventas entre productos."""

#TENDENCIAS DE VENTAS A LO LARGO DEL TIEMPO PARA CADA REGION
#ENTONCES DEBO AGRUPAR LAS VENTAS EN REGIONES PERO MANTENIENDO LA FECHA DE ESTAS
df_ventas_grafica_ventasregiontiempo=df_ventas_limpia.groupby(["Fecha","Región"])["Ventas"].sum().reset_index()
plt.figure(figsize=(10,6))
sns.lineplot(data=df_ventas_grafica_ventasregiontiempo,x="Fecha",y="Ventas",hue="Región",markers="0")
plt.xlabel("Tiempo")
plt.ylabel("Ventas")
plt.title("TENDENCIA DE VENTAS A LO LARGO DEL TIEMPO")
plt.show()
#COMPARACIONES DE VENTAS ENTRE REGIONES
df_ventas_grafica_ventasregiones=df_ventas_limpia.groupby("Región").agg({
    "Ventas":"sum",
    "Clientes":"sum"
})
plt.figure()
sns.barplot(data=df_ventas_grafica_ventasregiones,x="Región",y="Ventas")
plt.xlabel("Región")
plt.ylabel("Ventas")
plt.title("VENTAS POR REGION")
plt.show()
#COMPARACIONES DE VENTAS ENTRE PRODUCTOS

plt.figure()
sns.barplot(data=df_ventas_totales_producto, x="Producto",y="Ventas")
plt.xlabel("Producto")
plt.ylabel("Ventas")
plt.title("VENTAS POR PRODUCTO")
plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(100))
plt.show()

