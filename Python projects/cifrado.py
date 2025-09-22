# Cifrado César y Vigenère
# Jose Humberto Castro Garcia

def limpiar_texto(texto):
    """Convierte a mayúsculas y elimina caracteres no permitidos (solo A-Z)."""
    return "".join([c.upper() for c in texto if c.isalpha()])


# ------------------ CIFRADO CESAR ------------------
def cesar_encriptar(texto, clave):
    resultado = ""
    for c in limpiar_texto(texto):
        pos = (ord(c) - ord('A') + clave) % 26
        resultado += chr(ord('A') + pos)
    return resultado


def cesar_desencriptar(texto, clave):
    resultado = ""
    for c in limpiar_texto(texto):
        pos = (ord(c) - ord('A') - clave) % 26
        resultado += chr(ord('A') + pos)
    return resultado


# ------------------ CIFRADO VIGENERE ------------------
def generar_clave_vigenere(texto, clave):
    """Repite la clave hasta tener la misma longitud que el texto"""
    clave = limpiar_texto(clave)
    return (clave * (len(texto) // len(clave) + 1))[:len(texto)]


def vigenere_encriptar(texto, clave):
    texto = limpiar_texto(texto)
    clave_extendida = generar_clave_vigenere(texto, clave)
    resultado = ""
    for t, k in zip(texto, clave_extendida):
        pos = (ord(t) - ord('A') + (ord(k) - ord('A'))) % 26
        resultado += chr(ord('A') + pos)
    return resultado


def vigenere_desencriptar(texto, clave):
    texto = limpiar_texto(texto)
    clave_extendida = generar_clave_vigenere(texto, clave)
    resultado = ""
    for t, k in zip(texto, clave_extendida):
        pos = (ord(t) - ord('A') - (ord(k) - ord('A'))) % 26
        resultado += chr(ord('A') + pos)
    return resultado


# ------------------ PROGRAMA PRINCIPAL ------------------
def main():
    while True:
        print("\n--- MENU ---")
        print("1. Cifrado César")
        print("2. Cifrado Vigenère")
        print("3. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            texto = input("Ingresa el texto: ")
            clave = int(input("Ingresa el número de desplazamiento: "))

            encriptado = cesar_encriptar(texto, clave)
            print("Texto encriptado:", encriptado)

            desencriptado = cesar_desencriptar(encriptado, clave)
            print("Texto desencriptado:", desencriptado)

        elif opcion == "2":
            texto = input("Ingresa el texto: ")
            clave = input("Ingresa la palabra clave: ")

            encriptado = vigenere_encriptar(texto, clave)
            print("Texto encriptado:", encriptado)

            desencriptado = vigenere_desencriptar(encriptado, clave)
            print("Texto desencriptado:", desencriptado)

        elif opcion == "3":
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida, intenta de nuevo.")


if __name__ == "__main__":
    main()
