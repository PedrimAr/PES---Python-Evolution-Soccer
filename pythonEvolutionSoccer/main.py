from menu import menu
from game import jogar
from game_over import game_over


def main():
    while True:
        estado = menu()  # Retorna 0 para sair, 1 para jogar
        if estado == 1:
            resultado = jogar(False)  # Retorna 0 para Game Over
            if resultado == 0:
                game_over()


if _name_ == "_main_":
    main()
