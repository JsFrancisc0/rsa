import random
import math

# Test de primalidad de Miller-Rabin
def miller_rabin(n, k):
    if n == 2:
        return True
    if n % 2 == 0 or n == 1:
        return False
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# Generación de claves RSA
def get_keys(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 0
    for i in range(2, phi):
        if math.gcd(phi, i) == 1:
            e = i
            break
    d = multiplicative_inverse(e, phi)
    return n, e, d, phi

def multiplicative_inverse(e, phi):
    return extended_euclid(e, phi)[1] % phi

def extended_euclid(a, b):
    if b == 0:
        return a, 1, 0
    else:
        d2, x2, y2 = extended_euclid(b, a % b)
        d, x, y = d2, y2, x2 - (a // b) * y2
        return d, x, y

# Algoritmo de square and multiply
def square(x, y, s):
    if y == 0:
        return 1
    elif y % 2 == 0:
        a = (x ** (y // 2)) % s
        return (a ** 2) % s
    else:
        a = (x ** ((y - 1) // 2)) % s
        return (a ** 2 * x) % s

# Convertir texto a números ASCII
def text_to_ascii(text):
    return [ord(c) for c in text]

# Convertir números ASCII a texto
def ascii_to_text(ascii_list):
    return ''.join(chr(i) for i in ascii_list)

# Cifrado RSA
def encrypt(message, e, n):
    ascii_values = text_to_ascii(message)
    encrypted = [square(m, e, n) for m in ascii_values]
    return encrypted

# Descifrado RSA
def decrypt(encrypted_message, d, n):
    decrypted = [square(c, d, n) for c in encrypted_message]
    return ascii_to_text(decrypted)

# Función principal para ejecutar el programa
def main():
    # Pedir al usuario p y q y verificar si son primos
    while True:
        p = int(input("Ingrese un número primo 'p': "))
        if miller_rabin(p, 40):
            print(f"{p} es primo.")
            break
        else:
            print(f"{p} no es primo. Intente nuevamente.")

    while True:
        q = int(input("Ingrese un número primo 'q': "))
        if miller_rabin(q, 40):
            print(f"{q} es primo.")
            break
        else:
            print(f"{q} no es primo. Intente nuevamente.")

    # Generar las claves RSA
    n, e, d, phi = get_keys(p, q)
    print(f"Valores generados:\np = {p}\nq = {q}\nn = {n}\ne = {e}\nd = {d}\nphi(n) = {phi}")

    # Ciclo para cifrar/descifrar repetidamente
    while True:
        print("\nSeleccione una opción:\n1. Cifrar un mensaje\n2. Descifrar un mensaje\n3. Salir")
        choice = input("Ingrese el número de la opción: ")

        if choice == '1':
            message = input("Ingrese el mensaje a cifrar: ")
            encrypted_message = encrypt(message, e, n)
            print(f"Mensaje cifrado: {encrypted_message}")

        elif choice == '2':
            encrypted_message = input("Ingrese el mensaje cifrado (como lista de números separados por comas): ")
            encrypted_message = list(map(int, encrypted_message.split(',')))
            decrypted_message = decrypt(encrypted_message, d, n)
            print(f"Mensaje descifrado: {decrypted_message}")

        elif choice == '3':
            print("Saliendo...")
            break

        else:
            print("Opción no válida, intente nuevamente.")

# Ejecutar el programa
if __name__ == "__main__":
    main()
