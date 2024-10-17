import datetime
import mysql.connector
import schedule
import time
import threading

# Objetivo: Crear una aplicación para gestionar reservas de mesas en un
# restaurante. La aplicación deberá permitir agregar, modificar, y eliminar reservas, así como
# consultar la disponibilidad de mesas para una fecha y hora específicas.
# También debe mantener un historial de reservas pasadas.


def obtener_conexion():
    try:
        cnx = mysql.connector.connect(
            user="root", password="124837", host="localhost", database="practica006"
        )
        return cnx
    except mysql.connector.Error as err:
        print(f"Ocurrio un error al conectar la base de datos {err}")
        exit(1)


"""
SQL:
Crea una base de datos con tablas para reservas, clientes, y mesas.
Define relaciones entre las tablas, por ejemplo, una reserva puede estar asociada a un cliente 
y a una mesa.
Implementa funciones de consulta avanzadas para verificar la disponibilidad de mesas y manejar 
modificaciones.
Dificultad Adicional:
Validaciones y Restricciones:
Implementa validaciones como evitar reservas duplicadas para la misma mesa en la misma franja
horaria.
Asegura que las modificaciones de reservas no creen conflictos de disponibilidad.
Reporte de Reservas:
Crea un reporte que muestre el historial de reservas en un rango de fechas dado, con opciones
para filtrar por cliente o número de mesa.
Automatización:
Implementa una funcionalidad que automáticamente marca las reservas como "históricas" cuando
ha pasado la fecha de la reserva.
Interfaz de Usuario Mejorada:
Si deseas, puedes agregar una interfaz gráfica simple usando tkinter o PyQt para hacer la 
aplicación más interactiva."""


def agregar_reserva(cliente):
    cnx = obtener_conexion()
    try:
        with cnx.cursor() as cursor:
            if cliente:
                reserva = disponibilidad()
                fecha = reserva[0]
                fecha_final = reserva[0] + datetime.timedelta(minutes=90)
                mesa = reserva[1]
                personas = reserva[2]
                agregar_query = "INSERT INTO RESERVAS (cliente_id,mesa_id,horario_inicio,horario_final,personas) VALUES (%s,%s,%s,%s,%s)"
                cursor.execute(
                    agregar_query, (cliente, mesa, fecha, fecha_final, personas)
                )
                print("Mesa reservada correctamente")
                cnx.commit()
                return
    finally:
        cnx.close()


def eliminar_reserva(cliente):
    cnx = obtener_conexion()
    try:
        with cnx.cursor() as cursor:
            if cliente:
                eliminar_query = "DELETE FROM RESERVAS WHERE CLIENTE_ID=%s"
                cursor.execute(eliminar_query, cliente)
                print("Su reserva se elimino correctamente")
                cnx.commit()
                return
            else:
                print(
                    "No se pudo encontrar su reserva, revise los datos proporcionados"
                )
                return
    finally:
        cnx.close()


def pedir_fecha():
    while True:
        fecha_hoy = datetime.datetime.now().date()
        fecha_limite = fecha_hoy + datetime.timedelta(days=90)
        print("INGRESE LA FECHA")
        dia_decision = int(input("\tIngrese el dia"))
        mes_decision = int(input("\tIngrese el mes"))
        ano_decision = int(input("\tIngrese el año"))

        try:
            fecha_decision = datetime.date(ano_decision, mes_decision, dia_decision)
            if fecha_decision < fecha_hoy:
                print("No puede elegir una fecha en el pasado")
                continue
            if fecha_decision > fecha_limite:
                print("No puede reservar con mas de 90 dias de anticipacion")
                decision = input("Desea elegir otra fecha? (s/n)").lower()
                if decision == "s":
                    continue
                else:
                    return False
            else:
                return fecha_decision
        except ValueError:
            print("Fecha invalida, intente nuevamente")
            continue


def pedir_horario(ano, mes, dia):
    while True:
        horario_decision = input("Que horario busca reservar? (hh:mm)").split(":")
        hora = int(horario_decision[0])
        minuto = int(horario_decision[1])

        try:
            tiempo_decision = datetime.datetime(ano, mes, dia, hora, minuto, 0)
            return tiempo_decision
        except ValueError:
            print("Horario incorrecto, intente nuevamente")
            continue


def disponibilidad():
    while True:
        fecha = pedir_fecha()
        tiempo_decision = pedir_horario(fecha.year, fecha.month, fecha.day)
        cantidad_decision = None

        while (
            cantidad_decision is None
        ):  # Asegurarse que cantidad_decision sea un número válido
            try:
                cantidad_decision = int(input("¿Cuántas personas asistirán? "))
                if cantidad_decision <= 0:
                    print("La cantidad debe ser mayor a cero.")
                    cantidad_decision = None  # Para continuar pidiendo el valor
            except ValueError:
                print("Debe ingresar un número válido.")
        mesas_disponibles = disponibilidad_mesa(tiempo_decision, cantidad_decision)
        while True:
            if mesas_disponibles:
                print("Las siguientes mesas estan disponibles en el horario deseado:")
                for mesa_id in mesas_disponibles:
                    print(mesa_id)
                mesa_decision = int(input("Que mesa prefiere?").strip())
                print(f"USTED ELIGIO {mesa_decision}")
                if mesa_decision in mesas_disponibles:
                    print(
                        f"Usted eligio el horario:{tiempo_decision.strftime('%H:%M')} y la mesa {mesa_decision} ({cantidad_decision} personas)"
                    )
                    verificacion = input("Es esto correcto? (s/n)").lower()
                    if verificacion == "s":
                        return [tiempo_decision, mesa_decision, cantidad_decision]
                    else:
                        print("Porfavor elija de nuevo")
                else:
                    print(
                        "Esa mesa no esta disponible, debe elegir de la lista proporcionada"
                    )
                    continue
            else:
                print("No se encuentran mesas disponibles para ese horario")
                cambiar_horario = input(
                    "Quiere reservar en otro horario? (s/n)"
                ).lower()
                if cambiar_horario == "s":
                    break
                else:
                    return False


def disponibilidad_mesa(tiempo, cantidad):
    cnx = obtener_conexion()
    try:
        with cnx.cursor() as cursor:
            disponibilidad_query = (
                "SELECT id "
                "FROM mesas "
                "WHERE id "
                "NOT IN "
                "(SELECT mesa_id FROM reservas "
                "WHERE %s BETWEEN horario_inicio AND horario_final) "
                "AND capacidad >= %s"
            )
            cursor.execute(disponibilidad_query, (tiempo, cantidad))

            mesas_disponibles = [row[0] for row in cursor.fetchall()]
            return mesas_disponibles
    finally:
        cnx.close()


def historial():
    cnx = obtener_conexion()
    try:
        with cnx.cursor() as cursor:
            historial_query = (
                "INSERT INTO historial (cliente_id,horario_inicio,horario_final,mesa_id) "
                "SELECT  cliente_id,horario_inicio,horario_final,mesa_id FROM RESERVAS "
                "WHERE horario_final < NOW()"
            )
            cursor.execute(historial_query, ())
            eliminar_query = "DELETE FROM reservas WHERE horario_final < NOW()"
            cursor.execute(eliminar_query)
    finally:
        cnx.close()


def correr_scheduler():
    while True:
        schedule.run_pending()  # Revisa y ejecuta las tareas programadas
        time.sleep(1)  # Pausa de 1 segundo


# PROGRAMACION DE TIEMPO PARA EJECUTAR HISTORIAL AUTOMATICAMENTE
# Programar una tarea con schedule
schedule.every().day.at("00:00").do(historial)
# Crear un hilo para ejecutar el bucle infinito
scheduler_thread = threading.Thread(target=correr_scheduler)
scheduler_thread.daemon = (
    True  # Esto asegura que el hilo se cierre cuando el programa principal termine
)
scheduler_thread.start()

"""Gestión de Mesas:
Administrar las mesas del restaurante, incluyendo el número de mesa, la capacidad, y su estado
(disponible, reservado, etc.).
def gestion_mesas():"""


def verificar_cliente():
    cnx = obtener_conexion()
    try:
        with cnx.cursor() as cursor:
            verificar = input("Usted ya esta registrado? (s/n)").lower()
            if verificar == "s":
                verificar_query = "SELECT DNI FROM CLIENTES WHERE DNI=%s"
                dni = int(input("Ingrese su DNI:"))
                cursor.execute(verificar_query, (dni,))
                coincidencia = cursor.fetchone()
                if coincidencia:
                    telefono_query = "SELECT TELEFONO FROM CLIENTES WHERE DNI=%s"
                    cursor.execute(telefono_query, (dni,))
                    telefono = cursor.fetchone()[0]
                    telefono_digitos = str(telefono)[-4:]
                    decision = input(
                        f"Su numero de telefono termina en {telefono_digitos}?"
                    ).lower()
                    if decision == "s":
                        print("Usuario verificado exitosamente")
                        id_query = "SELECT id FROM clientes WHERE DNI=%s"
                        cursor.execute(id_query, (dni,))
                        id_cliente = cursor.fetchone()
                        return int(id_cliente[0])
                    else:
                        print("Ingrese nuevamente los datos")
                        return False
                else:
                    print(
                        "No se encontraron clientes registrados con ese DNI, intente nuevamente"
                    )
                    return False
            else:
                decision = input("Desea registrarse? (s/n)?").lower()
                if decision == "s":
                    id_cliente = registrar_cliente()
                    return id_cliente
                else:
                    return False
    finally:
        cnx.close()


def registrar_cliente():
    cnx = obtener_conexion()
    try:
        with cnx.cursor() as cursor:
            print("Registro:")
            while True:
                nombre = input("Ingrese su nombre: ").strip()
                if nombre.isalpha():
                    break
                else:
                    print("Su nombre no puede contener numeros o caracteres especiales")

            while True:
                apellido = input("Ingrese su apellido: ")
                if apellido.isalpha():
                    break
                else:
                    print(
                        "Su apellido no puede contener numeros o caracteres especiales"
                    )

            while True:
                try:
                    dni = int(input("Ingrese su dni: "))
                    break
                except ValueError:
                    print("Su numero de DNI solo puede contener numeros")

            while True:
                try:
                    telefono = int(input("Ingrese su telefono: "))
                    break
                except ValueError:
                    print("Su numero de telefono solo puede contener numeros")

            direccion = input("Ingrese su direccion: ")

            registrar_query = (
                "INSERT INTO clientes (DNI,nombre,apellido,direccion,telefono)"
                "VALUES (%s,%s,%s,%s,%s)"
            )
            cursor.execute(
                registrar_query, (dni, nombre, apellido, direccion, telefono)
            )
            print("Se registró correctamente")
            cnx.commit()
            retornar_query = "SELECT id FROM clientes WHERE DNI=%s"
            cursor.execute(retornar_query, (dni,))
            cliente_creado = cursor.fetchone()
            return cliente_creado
    finally:
        cnx.close()


def ver_reserva():
    cnx = obtener_conexion()
    try:
        with cnx.cursor() as cursor:
            cliente = verificar_cliente()
            if cliente:
                print(cliente)
                ver_reserva_query = "SELECT * FROM RESERVAS WHERE cliente_id= %s"
                cursor.execute(ver_reserva_query, (cliente,))
                reserva = cursor.fetchone()
                print("Su reserva: ")
                print(reserva)
                decision = input("Desea modificar su reserva?(s/n)").lower()
                horario = reserva[2]
                if decision == "s":
                    decision_fecha = input("Desea cambiar la fecha?(s/n)").lower()
                    if decision_fecha == "s":
                        fecha = pedir_fecha()
                        horario = pedir_horario(fecha.year, fecha.month, fecha.day)
                        horario_final = horario + datetime.timedelta(minutes=90)
                        cantidad = reserva[5]
                        mesas_disponibles = disponibilidad_mesa(horario, cantidad)
                        if reserva[4] in mesas_disponibles:
                            cambiar_fecha_query = "UPDATE reservas SET horario_inicio=%s ,  horario_final=%s WHERE cliente_id=%s"
                            cursor.execute(
                                cambiar_fecha_query, (horario, horario_final, cliente)
                            )
                            print("La fecha de su reserva ha cambiado con exito")
                            cnx.commit()
                    decision_mesa = input("Desea cambiar la mesa? (s/n)").lower()
                    if decision_mesa == "s":
                        mesas = disponibilidad_mesa(horario, cantidad)
                        if mesas:
                            print(
                                "Se encuentran disponibles las siguientes mesas para el horario especificado:"
                            )
                            for mesa in mesas:
                                print(f"{mesa}")
                            mesa_nueva = None
                            if mesa_nueva is None:
                                while True:
                                    try:
                                        mesa_nueva = int(input("Que mesa desea?"))
                                        if mesa_nueva in mesas:
                                            cambiar_mesa_query = "UPDATE reservas SET mesa_ID=%s WHERE cliente_id=%s"
                                            cursor.execute(
                                                cambiar_mesa_query,
                                                (mesa_nueva, cliente),
                                            )
                                            cnx.commit()
                                            print(
                                                "Se cambio la mesa de la reservacion correctamente"
                                            )
                                        else:
                                            print(
                                                "Esa mesa no esta disponible, debe elegir de la lista proporcionada"
                                            )
                                            continue
                                        break
                                    except ValueError:
                                        print("Debe ingresar el numero de mesa")

                        else:
                            print(
                                "No se encontraron mesas para el horario especificado"
                            )
    finally:
        cnx.close()


def main():
    while True:
        print("MENU:")
        print("Opcion 1: Registrarse")
        print("Opcion 2: Agregar reserva")
        print("Opcion 3: Eliminar reserva")
        print("Opcion 4: Ver reserva realizada")
        print("Opcion 5: Salir")
        opcion = input("Ingrese la opcion que desee:")
        if opcion == "1":
            historial()
            registrar_cliente()
            continue
        elif opcion == "2":
            historial()
            agregar_reserva(verificar_cliente())
            continue
        elif opcion == "3":
            historial()
            eliminar_reserva(verificar_cliente())
            continue
        elif opcion == "4":
            historial()
            ver_reserva()
        elif opcion == "5":
            return
        else:
            print("Ingrese una opcion valida")


main()
