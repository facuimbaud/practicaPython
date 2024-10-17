"""Problema: Análisis Básico de Datos de Ventas
Supongamos que tienes un negocio pequeño y deseas analizar tus datos de ventas. Dispones de varios archivos en formato CSV que contienen la información de las ventas por mes. Necesitas responder preguntas como:

Total de ventas por producto: ¿Cuáles son los productos más vendidos?
Total de ventas por mes: ¿Cuál fue el mes con más ventas?
Ventas promedio por cliente: ¿Cuánto gastan en promedio tus clientes?
Análisis de categorías de productos: ¿Qué categorías de productos generan más ingresos?"""
from operator import index

import pandas as pd

df_enero= pd.read_csv("ventas_enero.csv")
df_febrero=pd.read_csv("ventas_febrero.csv")
df_marzo=pd.read_csv("ventas_marzo.csv")

df_enero["Mes"]="Enero"
df_febrero["Mes"]="Febrero"
df_marzo["Mes"]="Marzo"

##MAL YA QUE NO PUEDO SABER DE QUE MES ES Y ADEMAS HAY UNA FUNCION PARA ESO##
# df_mayor_venta= max(sum(df_enero["Ventas"]),sum(df_febrero["Ventas"],sum(df_marzo)["Ventas"]))
df_total= pd.concat([df_enero,df_febrero,df_marzo],ignore_index=True)

#TOTAL DE VENTAS POR PRODUCTO
df_total_ordenado= df_total.groupby(["Producto","Categoría"]).agg({
    "Ventas":"sum",
    "Clientes":"sum"}).reset_index()

#TOTAL DE VENTAS POR MES
df_ventas_mes=df_total[["Ventas","Mes"]].groupby("Mes")["Ventas"].sum().reset_index()

#VENTAS PROMEDIO POR CLIENTE
promedio_ventas_clientes= df_total_ordenado["Ventas"].sum()/df_total_ordenado["Clientes"].sum()

#QUE CATEGORIA DE PRODUCTOS GENERAN MAS INGRESOS
df_categoria_ventas= df_total[["Categoría","Ventas"]].groupby("Categoría")["Ventas"].sum().reset_index()

#PRODUCTOS INCONSISTENTES
productos_inconsistentes= df_total.groupby("Producto")["Categoría"].nunique()
productos_inconsistentes= productos_inconsistentes[productos_inconsistentes>1].index.tolist()
if productos_inconsistentes:
    print(f"Se encontraron los siguientes productos inconsistentes  {",".join(productos_inconsistentes)}")


print(df_total)
print("\n\n",df_total_ordenado)
print("\n\n",df_ventas_mes)
print("\n\nEl promedio de ventas por cliente es:"+ str(promedio_ventas_clientes))
print("\n\n",df_categoria_ventas)