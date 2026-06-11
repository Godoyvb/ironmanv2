import pygame
import random
from recursos.funcoes import inicializarBancoDeDados, limpar_tela, escreverDados, maior_pontuador
from recursos.trabalho import pausar_jogo

limpar_tela()
inicializarBancoDeDados()
pygame.init()

tamanho = (1000,700)
pygame.display.set_caption("Pior zagueiro do mundo")
icone = pygame.image.load("bases/jogador2.png")
pygame.display.set_icon(icone)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode(tamanho)
branco = (255, 255, 255)
preto = (0, 0, 0)
amarelo = (255, 221, 64)

fundo = pygame.image.load("bases/campofundo.png")
fundoDead = pygame.image.load("bases/backgroundDead.jpg")
fundoStart = pygame.image.load("bases/backgroundStart.jpg")

zagueiro = pygame.image.load("bases/jogador2.png")
zagueiro = pygame.transform.scale(zagueiro, (90,130))
atacante = pygame.image.load("bases/jogador1.png")
atacante = pygame.transform.scale(atacante, (90,130))
missileSound = pygame.mixer.Sound("bases/missile.wav")
explosaoSound = pygame.mixer.Sound("bases/apito.mp3")
pygame.mixer.music.load("bases/torcida.mp3")

try:
    telaStart = pygame.image.load("bases/telainicio.png")
    telaStart = pygame.transform.scale(telaStart, tamanho)
    telaDeadBg = pygame.image.load("bases/telamorte.png")
    telaDeadBg = pygame.transform.scale(telaDeadBg, tamanho)
    juiz = pygame.image.load("bases/juiz.png")
    juiz = pygame.transform.scale(juiz, (80, 120))
except Exception as e:
    print("Aviso: não foi possível carregar os assets de bases:", e)
    telaStart = fundoStart
    telaDeadBg = fundoDead
    juiz = pygame.Surface((80, 120))
    juiz.fill((220, 220, 0))

fonteMenu = pygame.font.SysFont("comicsans",18)
fonteTitle = pygame.font.SysFont("comicsans",36)
fonteLarge = pygame.font.SysFont("comicsans",48)

def draw_button(surface, rect, texto, text_color, button_color):
    pygame.draw.rect(surface, button_color, rect, border_radius=15)
    fonte_texto = fonteMenu.render(texto, True, text_color)
    surface.blit(
        fonte_texto,
        (
            rect.x + (rect.width - fonte_texto.get_width()) // 2,
            rect.y + (rect.height - fonte_texto.get_height()) // 2,
        ),
    )


def name_entry():
    nome = ""
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                elif evento.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]
                elif evento.key == pygame.K_RETURN:
                    if nome.strip():
                        return nome.strip()
                else:
                    if len(nome) < 15:
                        nome += evento.unicode

        tela.blit(telaStart, (0, 0))
        titulo = fonteLarge.render("Digite seu nome", True, branco)
        texto_instru = fonteMenu.render("Pressione ENTER para continuar", True, branco)
        tela.blit(titulo, (50, 120))
        tela.blit(texto_instru, (50, 180))

        caixa = pygame.Rect(50, 240, 400, 40)
        pygame.draw.rect(tela, branco, caixa, border_radius=10)
        nome_text = fonteMenu.render(nome or "...", True, preto)
        tela.blit(nome_text, (caixa.x + 10, caixa.y + 10))

        info = fonteMenu.render("Após digitar o nome, você verá a tela de boas-vindas.", True, branco)
        tela.blit(info, (50, 310))

        pygame.display.update()
        relogio.tick(30)


def welcome_screen(nome):
    iniciar_rect = pygame.Rect(420, 560, 160, 40)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            elif evento.type == pygame.MOUSEBUTTONUP:
                if iniciar_rect.collidepoint(evento.pos):
                    return True

        tela.blit(telaStart, (0, 0))
        bienvenida = fonteTitle.render(f"Bem-vindo, {nome}", True, branco)
        mecanica1 = fonteMenu.render("Use as setas para mover o zagueiro para cima e para baixo.", True, branco)
        mecanica2 = fonteMenu.render("Desvie do atacante e faça o maior número de pontos.", True, branco)
        mecanica3 = fonteMenu.render("Pressione SPACE para pausar o jogo.", True, branco)
        tela.blit(bienvenida, (50, 80))
        tela.blit(mecanica1, (50, 150))
        tela.blit(mecanica2, (50, 180))
        tela.blit(mecanica3, (50, 210))

        top_nome, top_pontos, top_data = maior_pontuador()
        if top_nome:
            melhor = fonteMenu.render(
                f"Maior pontuador: {top_nome} - {top_pontos} pontos - {top_data}", True, branco
            )
        else:
            melhor = fonteMenu.render("Ainda não há recordes salvos.", True, branco)
        tela.blit(melhor, (50, 260))

        draw_button(tela, iniciar_rect, "Iniciar Game", preto, branco)
        pygame.display.update()
        relogio.tick(60)


def jogar(nome):
    fundoMov1 = 0
    fundoMov2 = 1129
    posicaoXPersona = 190
    posicaoYPersona = 60
    movimentoYPersona = 0
    velocidadeMovPersona = 5
    posicaoXAtacante = tamanho[0]
    posicaoYAtacante = 100
    velocidadeAtacante = 2
    pontos = 0
    pygame.mixer.Sound.play(missileSound)
    pygame.mixer.music.play(-1)
    dificuldade = 20

    juiz_pos = [random.randint(600, 900), random.randint(0, 550)]
    juiz_vel = [random.choice([-2, -1, 1, 2]), random.choice([-2, -1, 1, 2])]

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                pausar_jogo(tela, fonteMenu, branco, preto, relogio)
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_UP:
                movimentoYPersona = -velocidadeMovPersona
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_DOWN:
                movimentoYPersona = velocidadeMovPersona
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_UP:
                movimentoYPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_DOWN:
                movimentoYPersona = 0

        posicaoYPersona = posicaoYPersona + movimentoYPersona
        if posicaoYPersona < 0:
            posicaoYPersona = 0
        elif posicaoYPersona > tamanho[1] - 130:
            posicaoYPersona = tamanho[1] - 130

        posicaoXAtacante = posicaoXAtacante - velocidadeAtacante
        if posicaoXAtacante < -90:
            pygame.mixer.Sound.play(missileSound)
            posicaoXAtacante = tamanho[0]
            pontos = pontos + 1
            velocidadeAtacante = velocidadeAtacante + 1
            posicaoYAtacante = random.randint(0, 570)

        juiz_pos[0] += juiz_vel[0]
        juiz_pos[1] += juiz_vel[1]
        if juiz_pos[0] < 0 or juiz_pos[0] > tamanho[0] - 80:
            juiz_vel[0] *= -1
        if juiz_pos[1] < 0 or juiz_pos[1] > tamanho[1] - 120:
            juiz_vel[1] *= -1
        if random.randint(0, 120) == 0:
            juiz_vel = [random.choice([-3, -2, -1, 1, 2, 3]), random.choice([-3, -2, -1, 1, 2, 3])]

        tela.blit(fundo, (0, 0))

        raioSol = 22 + int(8 * abs(((pygame.time.get_ticks() // 80) % 20) - 10) / 10)
        pygame.draw.circle(tela, amarelo, (950, 55), raioSol)

        tela.blit(zagueiro, (posicaoXPersona, posicaoYPersona))
        tela.blit(atacante, (posicaoXAtacante, posicaoYAtacante))
        tela.blit(juiz, tuple(juiz_pos))

        texto = fonteMenu.render("Pontos: " + str(pontos), True, preto)
        tela.blit(texto, (700, 15))
        textoPause = fonteMenu.render("Press Space to Pause Game.", True, branco)
        tela.blit(textoPause, (tamanho[0] - textoPause.get_width() - 15, tamanho[1] - textoPause.get_height() - 15))

        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona + 90))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona + 130))
        pixelsAtacanteX = list(range(posicaoXAtacante, posicaoXAtacante + 90))
        pixelsAtacanteY = list(range(posicaoYAtacante, posicaoYAtacante + 130))
        if len(list(set(pixelsAtacanteY).intersection(set(pixelsPersonaY)))) > dificuldade:
            if len(list(set(pixelsAtacanteX).intersection(set(pixelsPersonaX)))) > dificuldade:
                escreverDados(nome, pontos)
                return dead(nome, pontos)

        pygame.display.update()
        relogio.tick(60)

def dead(nome, pontos):
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)
    startButton = pygame.Rect(420, 560, 150, 40)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            elif evento.type == pygame.MOUSEBUTTONUP:
                if startButton.collidepoint(evento.pos):
                    return True

        tela.blit(telaDeadBg, (0, 0))
        draw_button(tela, startButton, "Iniciar Game", preto, branco)

        texto_title = fonteLarge.render("Fim de Jogo", True, branco)
        texto_score = fonteMenu.render(f"Sua pontuação: {pontos}", True, branco)
        top_nome, top_pontos, top_data = maior_pontuador()
        if top_nome:
            texto_record = fonteMenu.render(
                f"Maior competidor: {top_nome} - {top_pontos} pts - {top_data}", True, branco
            )
        else:
            texto_record = fonteMenu.render("Sem registros de competidor ainda.", True, branco)

        tela.blit(texto_title, (50, 80))
        tela.blit(texto_score, (50, 140))
        tela.blit(texto_record, (50, 180))

        pygame.display.update()
        relogio.tick(60)


def start():
    nome = name_entry()
    while True:
        if not welcome_screen(nome):
            break
        if not jogar(nome):
            break

    pygame.quit()
    quit()

start()
