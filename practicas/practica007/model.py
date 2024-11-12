import mysql.connector
import datetime


class ReservaDB:
    def __init__(self):
        # Conectarse a la base de datos
        self.conexion = mysql.connector.connect(
            host="localhost",
            user="root",  # Asegúrate de usar tu usuario de MySQL
            password="124837",  # Asegúrate de usar tu contraseña de MySQL
            database="practica006",
        )
        self.cursor = self.conexion.cursor()

    def agregar_reserva(
        self,
        cliente_id: int,
        mesa_id: int,
        fecha_inicio: datetime,
        fecha_final: datetime,
    ):
        query = "INSERT INTO reservas (cliente_id,mesa_id,fecha_inicio,fecha_final) VALUES (%s,%s,%s,%s)"
        self.cursor.execute(query, (cliente_id, mesa_id, fecha_inicio, fecha_final))
        self.conexion.commit()

    def existencia_cliente(self, dni: int) -> bool:
        # returns id from client, if there isnt a cliente return none
        query = "SELECT id FROM clientes WHERE dni=%s"
        self.cursor.execute(query, (dni,))
        resultado = self.cursor.fetchone
        if resultado:
            return resultado[0]
        else:
            return None

    def agregar_cliente(
        self, nombre: str, apellido: str, dni: int, direccion: str, telefono: int
    ):
        resultado = self.existencia_cliente(dni)
        if resultado:
            print("No se pudo crear ya que existe otro usuario con ese dni")
        else:
            query = "INSERT INTO clientes (nombre,apellido,dni,direccion,telefono) VALUES (%s,%s,%s,%s,%s)"
            self.cursor.execute(query)
            self.conexion.commit()

    def eliminar_cliente(self, dni: int) -> bool:
        resultado = self.existencia_cliente(dni)
        if resultado:
            cliente_id = resultado[0]
            self.cursor.execute(
                "SELECT COUNT(*) FROM reservas WHERE cliente_id=%s", (cliente_id,)
            )
            cantidad_reservas = self.cursor.fetchone()[0]
            if cantidad_reservas > 0:
                print("No se puede eliminar el usuario ya que tiene reservas activas")
                return False
            else:
                query = "DELETE FROM clientes WHERE id=%s"
                self.cursor.execute(query, (cliente_id,))
                self.conexion.commit
                print("Se ha eliminado con exito el usuario")
                return True
        else:
            print("No se encontraron usuarios con ese DNI")


class Usuario:
    def __init__(self, nombre: str, apellido: str, dni: int):
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni


class Cliente(Usuario):
    def __init__(
        self, nombre: str, apellido: str, dni: int, direccion: str, telefono: int
    ):
        super.__init__(self, nombre, apellido, dni)
        self.direccion = direccion
        self.telefono = telefono


class Administrador(Usuario):
    def __init__(self, nombre: str, apellido: str, dni: int, permisos: list[str]):
        super.__init__(self, nombre, apellido, dni)
        self.permisos = permisos


class Mesa:
    def __init__(self, numero: int, ocupado: bool):
        self.numero = numero
        self.ocupado = False


class Reserva:
    def __init__(
        self,
        cliente: Cliente,
        mesa: Mesa,
        fecha_inicio: datetime,
        fecha_final: datetime,
    ):
        self.cliente = cliente
        self.mesa = mesa
        self.fecha_inicio = fecha_inicio
        self.fecha_final = fecha_final
