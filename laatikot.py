import pygame

laatikko = pygame.Rect(200, 200, 100, 100)

laatikko.inflate_ip(-50, -50)

naytto = pygame.display.set_mode((1024, 576))

while True:

    for tapahtuma in pygame.event.get():
        if tapahtuma.type == pygame.QUIT:
            exit()

    naytto.fill((0, 0, 0))

    pygame.draw.rect(naytto, (255, 0, 0), laatikko)

    pygame.display.flip()
