



import pandas as pd
import matplotlib.pyplot as plt
from operator import index

df_productos=pd.read_csv("productos_categorias.csv")
df_ventas=pd.read_csv("ventas.csv")

#(df_productos.info())
#print(df_ventas.isnull().sum())
#ORDENAR POR FECHA Y HORA
print(df_ventas)
df_ventas= df_ventas.sort_values(by=["Fecha","Hora"],ascending=[True,True])
print(df_ventas)
#VERIFICACION DE DATOS INGRESADOS
#   VERIFICACION DE DATOS
df_ventas["Ventas"]= pd.to_numeric(df_ventas["Ventas"],errors="coerce")
df_ventas["Clientes"]= pd.to_numeric(df_ventas["Clientes"],errors="coerce")
df_ventas["Ventas"]=df_ventas["Ventas"].fillna(0)
df_ventas["Clientes"]=df_ventas["Clientes"].fillna(0)
df_ventas['Fecha'] = pd.to_datetime(df_ventas['Fecha'],format="%Y-%m-%d")
df_ventas['Hora'] = pd.to_datetime(df_ventas['Hora'], format='%H:%M').dt.time
print(df_ventas)
#   VERIFICACION DE PRODUCTOS INCONSISTENTES CON CATEGORIA
df_combinado= pd.merge(df_ventas,df_productos,on="Producto",how="left",suffixes=("_Ventas","_Productos"))
df_ventas["Categoría"]=df_combinado["Categoría_Productos"]
# Total de ventas por producto
df_ventas_producto=df_ventas.groupby("Producto")["Ventas"].sum().reset_index()
print(df_ventas_producto)
# Total de ventas por categoría
df_ventas_categoria= df_ventas.groupby("Categoría")["Ventas"].sum().reset_index()
print(df_ventas_categoria)
# Total de ventas por mes
df_ventas['Mes'] = df_ventas['Fecha'].dt.month
df_ventas_mes=df_ventas.groupby("Mes")["Ventas"].sum().reset_index()
print(df_ventas_mes)
# Promedio de ventas por cliente
prom_cliente=df_ventas["Ventas"].sum()/df_ventas["Clientes"].sum() if df_ventas["Clientes"].sum()>0 else 0
print(prom_cliente)

with pd.ExcelWriter("reporte_ventas.xlsx") as writer:
    df_ventas.to_excel(writer,sheet_name="Ventas")
    df_ventas_producto.to_excel(writer,sheet_name="Ventas por producto")
    df_ventas_categoria.to_excel(writer,sheet_name="Ventas por categoria")
    df_ventas_mes.to_excel(writer,sheet_name="Ventas por mes")
    pd.DataFrame({"Ventas promedio por cliente:":[prom_cliente]}).to_excel(writer,sheet_name="Ventas promedio por cliente")

plt.figure(figsize=(10,6))
plt.bar(df_ventas_producto["Producto"],df_ventas_producto["Ventas"])
plt.xlabel("Producto")
plt.ylabel("Ventas")
plt.title("Ventas en funcion del producto")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

