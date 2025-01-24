from PPlay.window import *
from PPlay.gameimage import *
import menu


def game_over():
    janela = Window(800, 400)
    janela.set_title("Game Over")
    teclado = Window.get_keyboard()
    fundo = GameImage("png/game_over.png")

    while True:

        if teclado.key_pressed("ESC"):  # Voltar para o menu principal
            menu.menu()
            break

        fundo.draw()
        janela.update()


def vitoria():
    janela = Window(800, 400)
    janela.set_title("HEXA!!!")
    fundo = GameImage("png/campeao.png")
    teclado = Window.get_keyboard()

    while True:
        if teclado.key_pressed("ESC"):  # Voltar para o menu principal
            menu.menu()
            break

        fundo.draw()
        janela.update()
