# Imports
from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.mouse import *
from PPlay.keyboard import *
import game


def menu():
    # Definição de janela (900, 600)
    janela = Window(900, 600)
    #alouuuu testa ai
    # Definição da imagem de fundo
    fundo = GameImage("png/fundo_menu_PES.jpg")

    # Definição do input do mouse como variável
    mouse = Mouse()

    # Definição do input do teclado como variável
    teclado = Keyboard()

    # Definição da Sprite dos botões
    botao_1 = Sprite("png/botao.png")
    botao_1.x = 100
    botao_1.y = 200

    botao_2 = Sprite("png/botao.png")
    botao_2.x = 100
    botao_2.y = 280

    botao_3 = Sprite("png/botao.png")
    botao_3.x = 100
    botao_3.y = 360

    botao_4 = Sprite("png/botao.png")
    botao_4.x = 100
    botao_4.y = 440

    botao_5 = Sprite("png/botao_transparente.png")
    botao_5.x = 370
    botao_5.y = 450

    # Definição da variável referente ao estado do jogo (0 = Menu, 1 = Gameplay, 2 = Tela de dificuldade)
    estado = 0

    # Game Loop
    while True:
        fundo.draw()

        if estado != 1:

            # Escrita do título
            janela.draw_text("Python", 100, 30, 50, (255,69,0), "Arial", True, True)
            janela.draw_text("Evolution", 100, 70, 50, (255,140,0), "Arial", True, True)
            janela.draw_text("Soccer", 100, 110, 50, (255,250,240), "Arial", True, True)

            # Desenho dos botões
            botao_1.draw()
            botao_2.draw()
            botao_3.draw()
            botao_4.draw()

            # Seleção do botão "Sair"
            if mouse.is_over_object(botao_4) and mouse.is_button_pressed(1):
                janela.close()

            if estado == 0:
                # Escrita dos botões
                janela.draw_text("Novo Jogo", 140, 207, 30, (255, 255, 255), "Arial")
                janela.draw_text("Continuar", 145, 287, 30, (255, 255, 255), "Arial")
                janela.draw_text("Dificuldade", 141, 367, 30, (255, 255, 255), "Arial")
                janela.draw_text("Sair", 175, 447, 30, (255, 255, 255), "Arial")

                # Seleção do botão "Sair"
                if mouse.is_over_object(botao_4) and mouse.is_button_pressed(1):
                    janela.close()

                # Seleção do botão "Novo Jogo"
                elif (mouse.is_over_object(botao_1)) and mouse.is_button_pressed(1):
                    estado = 1

                # Seleção do botão "Continuar"
                elif mouse.is_over_object(botao_2) and mouse.is_button_pressed(1):
                    estado = 2

                # Seleção do botão "Dificuldade"
                elif mouse.is_over_object(botao_3) and mouse.is_button_pressed(1):
                    estado = 3

            if estado == 3:
                # Escrita dos botões de dificuldade
                janela.draw_text("Fácil", 175, 207, 30, (255, 255, 255), "Arial")
                janela.draw_text("Médio", 170, 287, 30, (255, 255, 255), "Arial")
                janela.draw_text("Difícil", 172, 367, 30, (255, 255, 255), "Arial")
                janela.draw_text("Sair", 175, 447, 30, (255, 255, 255), "Arial")

                # Ao pressionar Esc, volta ao Menu
                if teclado.key_pressed("esc"):
                    estado = 0

        if estado == 1:
            fundo1 = GameImage("png/tutorial1.jpg")
            fundo1.draw()
            botao_5.draw()
            if mouse.is_over_object(botao_5) and mouse.is_button_pressed(1):
                estado = 2

        if estado == 2:
            janela.set_background_color([0, 0, 0])
            game.jogar(False)

            # Ao pressionar Esc, volta ao Menu
            if teclado.key_pressed("esc"):
                estado = 0

        # Update da janela
        janela.update()


menu()
