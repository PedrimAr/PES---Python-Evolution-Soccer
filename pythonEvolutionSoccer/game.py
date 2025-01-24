import random
from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
import game_over


def jogar(copa):
    janela = Window(800, 400)
    janela.set_title("Python Evolution Soccer")
    fundo = GameImage("png/estadio.png")

    # Configuração do Pygame para efeitos sonoros e gravidade
    pygame.init()

    # Personagem principal
    if not copa:
        player_sprites = ["png/player_sprite1.png", "png/player_sprite2.png",
                          "png/player_sprite3.png", "png/player_sprite4.png"]
    else:
        player_sprites = ["png/playerBR_sprite1.png", "png/playerBR_sprite2.png",
                          "png/playerBR_sprite3.png", "png/playerBR_sprite4.png"]

    player = Sprite(player_sprites[0])  # Inicializa com o primeiro sprite
    player.x, player.y = 100, janela.height - 100  # Posição inicial do personagem
    player.speed_x = 200  # Velocidade horizontal (usada no cenário)
    player.speed_y = 0  # Velocidade vertical
    gravity = 800  # Gravidade (píxeis/s²)
    jump_power = -400  # Força do salto

    # Controle de animação
    sprite_timer = 0
    sprite_interval = 0.15  # Troca de sprite a cada 0.15 segundos
    current_sprite_index = 0

    # Obstáculos e plataforma
    obstacles = []
    pos_x = 600  # Distância inicial entre os obstáculos
    for i in range(5):
        obs = Sprite("png/carrinho.png")
        obs.set_position(pos_x, janela.height - obs.height - 50)
        obstacles.append(obs)
        pos_x += random.randint(300, 400)

    ground = Sprite("png/ground.png")  # Plataforma base (chão)
    ground.set_position(0, janela.height - ground.height)

    # Ícone coletável
    icon = Sprite("png/gol.png")  # Imagem do ícone
    icon.set_position(random.randint(300, 700), janela.height - ground.height - random.randint(100, 180))  # Posição inicial do ícone
    total_gols = 0

    # Ícone de balada
    drink = Sprite("png/drink.png")
    drink.set_position(janela.width + random.randint(1000, 2000), janela.height - ground.height - random.randint(100, 180))

    mini_game_active = False
    mini_game_timer = 0
    mini_game_duration = 30  # Duração do mini-game em segundos
    aguas = 0

    # Pontuação
    gols = 0
    vidas = 12

    # Controle de input
    teclado = Window.get_keyboard()

    # Game loop
    running = False
    clock = pygame.time.Clock()
    cooldown = 0

    while True:
        delta = janela.delta_time()  # Tempo decorrido entre frames
        janela.set_background_color((135, 206, 235))  # Redesenha o fundo

        if teclado.key_pressed("SPACE"):
            running = True

        # Troca de sprites do player
        if running:
            sprite_timer += delta
            if sprite_timer >= sprite_interval:
                sprite_timer = 0
                current_sprite_index = (current_sprite_index + 1) % len(player_sprites)

                # Recria o sprite com a nova imagem, mantendo posição e velocidade
                new_sprite = Sprite(player_sprites[current_sprite_index])
                new_sprite.x, new_sprite.y = player.x, player.y
                new_sprite.speed_x, new_sprite.speed_y = player.speed_x, player.speed_y
                player = new_sprite  # Atualiza o player

        # Salto do player
        if teclado.key_pressed("W") and player.y >= janela.height - player.height - ground.height:
            player.speed_y = jump_power

        # Aplicação da gravidade
        player.speed_y += gravity * delta
        player.y += player.speed_y * delta

        # Colisão com o chão
        if player.y >= janela.height - player.height - ground.height:
            player.y = janela.height - player.height - ground.height
            player.speed_y = 0

        # Movimento do fundo (rolagem contínua)
        if running:
            fundo.x -= player.speed_x * delta
            if fundo.x <= -fundo.width:
                fundo.x = 0  # Reinicia a posição do fundo

            # Movimenta os obstáculos
            for i, obs in enumerate(obstacles):
                obs.x -= player.speed_x * delta
                if obs.x + obs.width < 0:
                    # Calcula a nova posição baseada no último obstáculo
                    last_obstacle_x = obstacles[(i - 1) % len(obstacles)].x
                    new_x = last_obstacle_x + random.randint(300, 400)
                    obs.set_position(new_x, janela.height - obs.height - 50)

            # Movimenta o ícone coletável
            icon.x -= player.speed_x * delta
            if icon.x + icon.width < 0:  # Reinicia a posição do ícone ao sair da tela
                total_gols += 1
                icon.set_position(janela.width + random.randint(100, 300), janela.height - ground.height - random.randint(100, 180))

            # Movimenta o ícone de drink
            if drink != 0:
                drink.x -= player.speed_x * delta
                if drink.x + drink.width < 0:
                    drink.set_position(janela.width + random.randint(1000, 2000), janela.height - ground.height - random.randint(100, 180))

        # Verificação de colisão com o ícone
        if player.collided(icon) and not mini_game_active:
            print("Ícone coletado!")
            gols += 1
            total_gols += 1
            icon.set_position(janela.width + random.randint(100, 300), janela.height - ground.height - random.randint(100, 180))

        # Verificando a colisão com o drink
        if drink != 0 and player.collided(drink):
            drink = 0
            print("Balada!")
            mini_game_active = True
            mini_game_timer = mini_game_duration

            fundo = GameImage("png/boate.png")
            # Criar novo ícone mantendo posição
            new_icon = Sprite("png/agua.png")
            new_icon.x, new_icon.y = icon.x, icon.y

            # Criar novos obstáculos mantendo posições
            for i in range(len(obstacles)):
                new_obs = Sprite("png/organizada.png")
                new_obs.x, new_obs.y = obstacles[i].x, obstacles[i].y
                obstacles[i] = new_obs  # Substitui o obstáculo na lista

        # Desenho dos elementos
        fundo.draw()
        fundo.draw()  # Desenha o fundo na posição atual
        # Ajusta a posição para desenhar o segundo fundo ao lado
        fundo.set_position(fundo.x + fundo.width, fundo.y)
        fundo.draw()
        # Restaura a posição original para manter o movimento contínuo
        fundo.set_position(fundo.x - fundo.width, fundo.y)
        # Desenha o fundo duplicado para continuidade

        if mini_game_active:
            mini_game_timer -= delta

            new_icon.x -= player.speed_x * delta
            if new_icon.x + icon.width < 0:  # Reinicia a posição do ícone ao sair da tela
                new_icon.set_position(janela.width + random.randint(100, 300), janela.height - ground.height - random.randint(100, 180))

            # Verificação de colisão com a água
            if player.collided(new_icon):
                print("Água coletada!")
                aguas += 1
                new_icon.set_position(janela.width + random.randint(100, 300), janela.height - ground.height - random.randint(100, 180))

            new_icon.draw()

            placar_aguas = GameImage("png/icone_agua.png")
            placar_aguas.set_position(470, 10)
            placar_aguas.draw()
            janela.draw_text(f'{aguas}', 520, 9, 36, (255, 255, 255), "Arial", False, False)

            if aguas == 5:
                mini_game_active = False

                fundo = GameImage("png/estadio.png")

                # Restaurar os obstáculos originais
                for i in range(len(obstacles)):
                    obs = Sprite("png/carrinho.png")
                    obs.x, obs.y = obstacles[i].x, obstacles[i].y
                    obstacles[i] = obs

            elif mini_game_timer <= 0 and aguas < 5:
                running = False
                game_over.game_over()

        player.draw()
        ground.draw()
        for obs in obstacles:
            obs.draw()

        if not mini_game_active:
            icon.draw()
            placar_gols = GameImage("png/icone_gol.png")
            placar_gols.set_position(450, 10)
            placar_gols.draw()
            janela.draw_text(f'{gols}', 520, 9, 36, (255, 255, 255), "Arial", False, False)

        janela.draw_text("VIDA:", 580, 5, 42, (255, 255, 255), "Arial", True, False)
        janela.draw_text(f'{vidas}', 700, 9, 36, (255, 255, 255), "Arial", False, False)

        if drink != 0:
            drink.draw()

        # Verificação de colisões com obstáculos
        for obs in obstacles:
            if player.collided(obs) and cooldown <= 0:
                vidas -= 1
                cooldown = 1
                print(vidas)

        if cooldown > 0:
            cooldown -= delta

        if (vidas <= 0 or total_gols >= 50) and gols < 30:
            running = False
            game_over.game_over()

        elif gols == 10:
            jogar(True)

        # Atualiza o jogo
        janela.update()
        clock.tick(60)  # Limita o jogo a 60 FPS
