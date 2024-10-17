import mysql.connector
import re
def validar_entrada(texto):
    return bool(re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', texto))

def obtener_conexion():
    try:
        cnx = mysql.connector.connect(
            user='root',
            password='124837',
            host='localhost',
            database='practica005'
        )
        return cnx
    except mysql.connector.Error as err:
        print(f"Ocurrio un error al conectar la base de datos {err}")
        exit(1)

def producto_add():
    cnx=obtener_conexion()
    with cnx.cursor() as cursor:
        while True:
            nombre = input("Introduzca el nombre del producto").strip()
            if validar_entrada(nombre):
                break
            else:
                print("Nombre invalido, ingrese nuevamente")

        while True:
            categoria = input("Introduzca la categoria del producto").strip()
            if validar_entrada(categoria):
                break
            else:
                print("Nombre invalido, no debe poseer numeros ni caracteres especiales")

        while True:
            try:
                precio = float(input("Introduzca el precio del producto").strip())
                if precio > 0:
                    break
                else:
                    print("El precio debe ser un número positivo. Inténtelo de nuevo.")
            except ValueError:
                print("Precio invalido, debe ingresar un numero")

        while True:
            try:
                stock = float(input("Cuantos productos desea cargar?").strip())
                break
            except ValueError:
                print("Debe ingresar un numero")

        add_producto="INSERT INTO PRODUCTOS(nombre,categoria,precio,stock)""VALUES (%s,%s,%s,%s)"
        data_producto=(nombre,categoria,precio,stock)
        cursor.execute(add_producto,data_producto)
        cnx.commit()
        print("Producto añadido con exito.")
    cnx.close()

def producto_delete():
    cnx = obtener_conexion()
    with cnx.cursor() as cursor:
        while True:
            producto_nombre= input("Ingrese el nombre del producto a eliminar").strip()
            if validar_entrada(producto_nombre):
                exact_nombre="SELECT * FROM PRODUCTOS WHERE NOMBRE = %s"
                cursor.execute(exact_nombre,(producto_nombre,))
                resultados= cursor.fetchall()
                delete_nombre="DELETE FROM PRODUCTOS WHERE NOMBRE = %s"
                if resultados:
                    cursor.execute(delete_nombre,(producto_nombre,))
                    cnx.commit()
                    print(f"El producto {producto_nombre} se ha eliminado con exito")
                    return
                else:
                    producto_nombre = "%" + producto_nombre + "%"
                    filter_nombre="SELECT * FROM PRODUCTOS WHERE NOMBRE LIKE %s"
                    cursor.execute(filter_nombre,(producto_nombre,))
                    resultados= cursor.fetchall()
                if resultados:
                    print("No se encontro un producto con ese nombre exacto,pero los siguientes productos coinciden parcialmente con su busqueda:")
                    for resultado in resultados:
                        print(f"ID={resultado[0]} NOMBRE={resultado[1]} ")
                else:
                    print("No se encontraron productos con ese nombre")
                eleccion = input("Desea continuar? (s/n)").strip().lower()
                if eleccion != "s":
                    return
            else:
                print("El nombre no puede contener numeros ni caracteres especiales")
    cnx.close()

def stock_cambiar():
    cnx = obtener_conexion()
    with cnx.cursor() as cursor:
        while True:
            producto_nombre = input("Ingrese el nombre del producto para ajustar stock").strip()
            if validar_entrada(producto_nombre):
                exact_nombre = "SELECT * FROM PRODUCTOS WHERE NOMBRE = %s"
                cursor.execute(exact_nombre, (producto_nombre,))
                resultados = cursor.fetchone()
                update_stock = ("UPDATE PRODUCTOS "
                                "SET STOCK= %s "
                                "WHERE NOMBRE = %s")
                if resultados:
                    while True:
                        try:
                            final_stock = float(input("Ingrese el stock actual:").strip())
                            break
                        except ValueError:
                            print("Incorrecto, debe ingresar un numero")

                    cursor.execute(update_stock, (final_stock,producto_nombre))
                    cnx.commit()
                    print(f"El stock del producto {producto_nombre} se ha modificado con exito")
                    return
                else:
                    producto_nombre = "%" + producto_nombre + "%"
                    filter_nombre = "SELECT * FROM PRODUCTOS WHERE NOMBRE LIKE %s"
                    cursor.execute(filter_nombre, (producto_nombre,))
                    resultados = cursor.fetchall()
                if resultados:
                    print(
                        "No se encontro un producto con ese nombre exacto,pero los siguientes productos coinciden parcialmente con su busqueda:")
                    for resultado in resultados:
                        print(f"ID={resultado[0]} NOMBRE={resultado[1]} ")
                else:
                    print("No se encontraron productos con ese nombre")
                eleccion = input("Desea continuar? (s/n)").strip().lower()
                if eleccion != "s":
                    return
            else:
                print("El nombre no puede contener numeros ni caracteres especiales")
        cnx.close()

def producto_editar():
    cnx = obtener_conexion()
    with cnx.cursor() as cursor:
        campos=["nombre","categoria","precio","stock"]
        actualizar={}
        while True:
            producto_nombre = input("Ingrese el nombre del producto a editar").strip()
            if validar_entrada(producto_nombre):
                exact_nombre = "SELECT * FROM PRODUCTOS WHERE NOMBRE = %s"
                cursor.execute(exact_nombre, (producto_nombre,))
                resultados = cursor.fetchone()
                if resultados:
                    print("Se encontro el producto:\t")
                    print(resultados)
                    #CAMBIO DE NOMBRE
                    decision=input("Desea modificar el nombre? (s/n)").lower()
                    if decision=="s":
                        while True:
                            final_nombre = input("Ingrese el nuevo nombre:").strip()
                            if validar_entrada(final_nombre):
                                actualizar[campos[0]]=final_nombre
                                break
                            else:
                                print("Incorrecto, el nombre no puede contener numeros ni caracteres especiales")
                    #CAMBIO CATEGORIA
                    decision=input("Desea modificar la categoria? (s/n)").lower()
                    if decision=="s":
                        while True:
                            final_categoria = input("Ingrese la nueva categoria:").strip()
                            if validar_entrada(final_categoria):
                                actualizar[campos[1]] = final_categoria
                                break
                            else:
                                print("Incorrecto, la categoria no puede contener numeros ni caracteres especiales")
                    #CAMBIO PRECIO
                    decision = input("Desea modificar el precio? (s/n)").lower()
                    if decision=="s":
                        while True:
                            try:
                                final_precio = float(input("Ingrese el nuevo precio:").strip())
                                actualizar[campos[2]] = final_precio
                                break
                            except ValueError:
                                print("Incorrecto, debe ingresar un numero")
                    #CAMBIO STOCK
                    decision = input("Desea modificar el stock del producto? (s/n)").lower()
                    if decision == "s":
                        while True:
                            try:
                                final_stock = float(input("Ingrese el stock actual:").strip())
                                actualizar[campos[3]] = final_stock
                                break
                            except ValueError:
                                print("Incorrecto, debe ingresar un numero")
                    if actualizar:
                        set_clause = ", ".join([f"{campo} = %s" for campo in actualizar.keys()])
                        valores= list(actualizar.values()) + [producto_nombre]
                        update_query=f"UPDATE PRODUCTOS SET {set_clause} WHERE NOMBRE=%s"
                        cursor.execute(update_query, valores)
                        cnx.commit()
                        print(f"El producto {producto_nombre} se ha modificado con exito")
                    return
                else:
                    producto_nombre = "%" + producto_nombre + "%"
                    filter_nombre = "SELECT * FROM PRODUCTOS WHERE NOMBRE LIKE %s"
                    cursor.execute(filter_nombre, (producto_nombre,))
                    resultados = cursor.fetchall()
                if resultados:
                    print(
                        "No se encontro un producto con ese nombre exacto,pero los siguientes productos coinciden parcialmente con su busqueda:")
                    for resultado in resultados:
                        print(f"ID={resultado[0]} NOMBRE={resultado[1]} ")
                else:
                    print("No se encontraron productos con ese nombre")
                eleccion = input("Desea continuar? (s/n)").strip().lower()
                if eleccion != "s":
                    return
            else:
                print("El nombre no puede contener numeros ni caracteres especiales")
        cnx.close()

def listarProductos():
    cnx = obtener_conexion()
    with cnx.cursor() as cursor:
        print("PRODUCTOS: ")
        select_query = "SELECT * FROM PRODUCTOS"
        cursor.execute(select_query)
        productos = cursor.fetchall()
        for producto in productos:
            print(f"\t{producto}")
        while True:
            print("OPCIONES:")
            print("\t1-ORDENAR POR NOMBRE")
            print("\t2-ORDENAR POR CATEGORIA")
            print("\t3-ORDENAR POR PRECIO")
            print("\t4-ORDENAR POR STOCK")
            print("\t5-BUSCAR POR NOMBRE")
            print("\t6-SALIR")
            while True:
                try:
                    eleccion= int(input("Seleccione la opcion que desee").strip())
                    break
                except ValueError:
                    print("Error. Debe ingresar un numero")
            while True:
                if eleccion==1:
                    print("Productos ordenados por nombre: ")
                    query1="SELECT * FROM PRODUCTOS ORDER BY NOMBRE"
                    cursor.execute(query1)
                    productos = cursor.fetchall()
                    for producto in productos:
                        print(f"\t{producto}")
                    break
                elif eleccion==2:
                    print("Productos ordenados por categoria: ")
                    query2 = "SELECT * FROM PRODUCTOS ORDER BY CATEGORIA"
                    cursor.execute(query2)
                    productos = cursor.fetchall()
                    for producto in productos:
                        print(f"\t{producto}")
                    break
                elif eleccion == 3:
                    print("Productos ordenados por precio: ")
                    query3 = "SELECT * FROM PRODUCTOS ORDER BY PRECIO"
                    cursor.execute(query3)
                    productos = cursor.fetchall()
                    for producto in productos:
                        print(f"\t{producto}")
                    break
                elif eleccion == 4:
                    print("Productos ordenados por stock: ")
                    query4 = "SELECT * FROM PRODUCTOS ORDER BY STOCK"
                    cursor.execute(query4)
                    productos = cursor.fetchall()
                    for producto in productos:
                        print(f"\t{producto}")
                    break
                elif eleccion == 5:

                    nombre_buscar=input("Buscar por nombre: ").strip()
                    nombre_buscar= "%" + nombre_buscar + "%"
                    query5 = "SELECT * FROM PRODUCTOS WHERE NOMBRE LIKE %s"
                    cursor.execute(query5,(nombre_buscar,))
                    productos = cursor.fetchall()
                    if productos:
                        print("Productos que coinciden con la busqueda: ")
                        for producto in productos:
                            print(f"\t{producto}")
                        break
                    else:
                        print("No se encontraron productos que coincidan con su busqueda")
                        break
                elif eleccion == 6:
                    return
            else:
                print("No ingreso una opcion valida")
    cnx.close()

def main():
    while True:
        try:
            print("GESTIONADOR DE PRODUCTOS")
            print("Opcion 1: Agregar producto")
            print("Opcion 2: Eliminar producto")
            print("Opcion 3: Editar producto")
            print("Opcion 4: Ver lista de productos")
            print("Opcion 5: Modificar stock")
            print("Opcion 6: Salir")
            eleccion=int(input("Seleccione una opcion").strip())
            if eleccion==1:
                producto_add()
            elif eleccion==2:
                producto_delete()
            elif eleccion==3:
                producto_editar()
            elif eleccion==4:
                listarProductos()
            elif eleccion==5:
                stock_cambiar()
            elif eleccion==6:
                break
            else:
                print("Opcion invalida, intente de nuevo")
        except ValueError:
            print("Opcion invalida, debe ingresar un numero")
        except KeyboardInterrupt:
            print("\nInterrupcion del programa detectada, cerrando programa")

main()

#PARA MANEJAR ERRORES AL ABRIR LA BASE DE DATOS
"""try:
    cnx = mysql.connector.connect(
        user='root',
        password='124837',
        host='localhost',
        database='practica005'
    )
except mysql.connector.Error as err:
    print(f"Error al conectar a la base de datos: {err}")
    exit(1)"""
#PARA MANEJAR ERRORES AL USAR UN EXECUTE
"""try:
    cursor.execute(add_producto, data_producto)
    cnx.commit()
except mysql.connector.Error as err:
    print(f"Error en la operación de la base de datos: {err}")
    cnx.rollback()"""
