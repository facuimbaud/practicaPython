def pedirNumero(mensaje):
    while True:
        entrada=input(mensaje)
        try:
            numero=int(entrada)
            return numero
        except ValueError:
            try:
                numero=float(entrada)
                return numero
            except ValueError:
                print("Entrada incorrecta, Porfavor Ingrese un Numero")
"""
def convertirTemperatura(temperatura, escalaOrigen, escalaDestino):
        if escalaOrigen == "C":
            if escalaDestino =="F":
                return temperatura * 9 / 5 + 32
            elif escalaDestino == "K":
                return temperatura + 273.15
        elif escalaOrigen == "F":
            if escalaDestino == "C":
                return (temperatura - 32) * 5 / 9
            elif escalaDestino == "K":
                return (temperatura - 32) * 5 / 9 + 273.15
        elif escalaOrigen == "K":
            if escalaDestino == "C":
                return temperatura - 273.15
            elif escalaDestino == "F":
                return (temperatura - 273.15) * 9 / 5 + 32
        else:
            return None
"""
def convertirTemperatura(temperatura, escalaOrigen, escalaDestino):
    conversiones= {
    ("C","F"):lambda x:x * 9 / 5 + 32,
    ("C","K"):lambda x:x+ 273.15,
    ("F","C"):lambda x:(x - 32) * 5 / 9,
    ("F","K"):lambda x:(x - 32) * 5 / 9 + 273.15,
    ("K","C"):lambda x:x - 273.15,
    ("K","F"):lambda x:(x - 273.15) * 9 / 5 + 32
    }
    return (conversiones.get((escalaOrigen,escalaDestino),lambda x:None)(temperatura))

def pedirEscala():
    while True:
        escalaOrigen= input("Porfavor Ingrese la Escala origen (C/F/K)").upper()
        escalaDestino = input("Porfavor Ingrese la Escala destino (C/F/K)").upper()
        if (escalaOrigen in ["C","F","K"]):
            if (escalaDestino) in ["C", "F", "K"]:
                if (escalaDestino != escalaOrigen):
                    return [escalaOrigen,escalaDestino]
                else:
                    print("La escala a convertir no puede ser la misma que la inicial")
            else:
                print("Escala destino no valida, debe ser C/F/K")
        else:
            print("Escala origen no valida, debe ser C/F/K")




def main():
    while True:
        temperatura = pedirNumero("Por favor ingrese la temperatura a convertir: ")
        escalas = pedirEscala()
        escalaOrigen = escalas[0]
        escalaDestino = escalas[1]
        resultado = convertirTemperatura(temperatura, escalaOrigen, escalaDestino)

        if resultado is not None:
            print(f"{temperatura}°{escalaOrigen} es igual a {resultado}°{escalaDestino}")
            break  # Salir del bucle si la conversión fue exitosa
        else:
            print("La conversión no pudo realizarse. Por favor, inténtelo de nuevo.")


if __name__ == "__main__":
    main()


