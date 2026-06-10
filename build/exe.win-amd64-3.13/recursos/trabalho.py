import pygame


def pausar_jogo(tela, fonte, branco, preto, relogio):
    pygame.mixer.music.pause()
    largura, altura = tela.get_size()
    pausado = True

    while pausado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                pausado = False

        pygame.draw.rect(tela, preto, (largura // 2 - 110, altura // 2 - 45, 220, 90))
        textoPause = fonte.render("PAUSE", True, branco)
        textoContinuar = fonte.render("Pressione Space", True, branco)
        tela.blit(textoPause, (largura // 2 - textoPause.get_width() // 2, altura // 2 - 30))
        tela.blit(textoContinuar, (largura // 2 - textoContinuar.get_width() // 2, altura // 2 + 5))
        pygame.display.update()
        relogio.tick(15)

    pygame.mixer.music.unpause()
