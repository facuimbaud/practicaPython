"""
: Calculadora de Estadísticas de Datos
Objetivo: Crear un programa que lea una lista de números desde un archivo de texto y calcule varias estadísticas de esos datos. La calculadora deberá incluir las siguientes funcionalidades:

Leer Datos:

Lee los números desde un archivo de texto. Cada número estará en una línea separada.
El nombre del archivo será ingresado por el usuario.
Calcular Estadísticas:

Media (Promedio): La media de los números.
Mediana: El valor central cuando los números están ordenados.
Moda: El número que aparece con mayor frecuencia.
Desviación Estándar: Mide la cantidad de variación o dispersión de los números.
Manejo de Errores:

Asegúrate de manejar casos en los que el archivo no existe o el archivo está vacío.
Verifica que el archivo contenga solo números válidos.
Guardar Resultados:

Guarda las estadísticas calculadas en un nuevo archivo de texto. El nombre del archivo de salida debe ser proporcionado por el usuario.
"""
import statistics
import os

"""def extraerDatos(nombreArchivo):
    datos = []
    try:
        with open(nombreArchivo,"r") as archivo:
            for linea in archivo:
                try:
                    numero= float(linea.strip())
                    datos.append(numero)
                except ValueError:
                    print("El archivo no solo contiene numeros")
    except FileNotFoundError:
        print("No se encontro ningun archivo con ese nombre")
    return datos
"""
def extraerDatos(nombreArchivo):
    datos = []
    if os.path.exists(nombreArchivo):
        with open(nombreArchivo,"r") as archivo:
            for linea in archivo:
                try:
                    numero= float(linea.strip())
                    datos.append(numero)
                except ValueError:
                    print("El archivo no solo contiene numeros")
            #print(datos)
    else:
        print("No se encontro ningun archivo con ese nombre")
    return datos

""" try:
        moda=statistics.mode(datos)
        moda=round(moda,2)
    except statistics.StatisticsError:
        moda="-"
        """

def calculo(datos):
    if not datos: return None,None,None,None
    list.sort(datos)
    media= round(statistics.mean(datos),2)
    #media=round(media,2)
    mediana= round(statistics.median(datos),2)
    #mediana=round(mediana,2)
    modas = statistics.multimode(datos)
    if len(modas) == 1:
        moda = round(modas[0], 2)
    else:
        moda = "-"  # No hay una moda única
    desviacion=round(statistics.stdev(datos) if len(datos)>1 else 0,2)
    #desviacion=round(desviacion,2)
    return media,mediana,moda,desviacion

def guardarResultados(nombreArchivo,resultados,cantidad):
    cantidad+=1
    with open(nombreArchivo,"a") as archivo:
        archivo.write(f"\nArchivo numero {cantidad}: ")
        archivo.write(f"\n\tMedia= {resultados[0]} ")
        archivo.write(f"\n\tMediana= {resultados[1]} ")
        archivo.write(f"\n\tModa= {resultados[2]} ")
        archivo.write(f"\n\tDesviacion= {resultados[3]} ")

def analizarIteraciones(nombreArchivo):
    if os.path.exists(nombreArchivo):
        with open(nombreArchivo,"r") as archivo:
            try:
                contenedor=archivo.read()
                numeroIteraciones= int(contenedor.split("=")[-1].strip())
                return numeroIteraciones
            except ValueError:
                return 0
    else:
        return 0

def guardarIteraciones(nombreArchivo,iteraciones):
    if os.path.exists(nombreArchivo):
        with open(nombreArchivo,"w") as archivo:
            archivo.write(f"Numero de archivos analizados = {iteraciones+1}")
    else:
        print("No existe un archivo con ese nombre")


def main():
    archivoConteo="practica002conteo.txt"
    archivoGuardar="practica002estadisticas.txt"
    archivoLeer=input("Ingrese el nombre del archivo a leer")
    numeroIteraciones= analizarIteraciones(archivoConteo)
    datos=extraerDatos(archivoLeer)
    if datos:
        resultados=calculo(datos)
        guardarResultados(archivoGuardar,resultados,numeroIteraciones)
        guardarIteraciones(archivoConteo,numeroIteraciones)
        print(f"Estadisticas guardadas en {archivoGuardar}")
    else:
        print("El archivo posee datos invalidos")

if __name__ == "__main__":
    main()




