import random

def juego_adivinanza():
    print("¡Bienvenido al Juego de Adivinanza!")
    print("Estoy pensando en un número entre 1 y 100.")
    
    # Generar número aleatorio
    numero_secreto = random.randint(1, 100)
    intentos = 0
    adivinado = False
    
    while not adivinado:
        try:
            # Pedir al usuario que adivine
            guess = int(input("Introduce tu adivinanza: "))
            intentos += 1
            
            # Verificar la adivinanza
            if guess < numero_secreto:
                print("¡Demasiado bajo! Intenta de nuevo.")
            elif guess > numero_secreto:
                print("¡Demasiado alto! Intenta de nuevo.")
            else:
                print(f"¡Felicidades! ¡Adivinaste el número en {intentos} intentos!")
                adivinado = True
                
        except ValueError:
            print("Por favor, introduce un número válido.")
    
    # Preguntar si quiere jugar de nuevo
    jugar_again = input("¿Quieres jugar de nuevo? (s/n): ").lower()
    if jugar_again == 's':
        juego_adivinanza()
    else:
        print("¡Gracias por jugar! ¡Hasta luego!")

# Iniciar el juego
if __name__ == "__main__":
    juego_adivinanza()
