import pygame
from random import randrange
from math import sqrt

class Ajojahti:
    def __init__(self):
        pygame.init()
        self.kello = pygame.time.Clock()
        self.lataa_kuvat()
        self.leveys = 1280
        self.korkeus = 720
        self.robonopeus = 2
        self.etsi_nopeus = 1
        self.jahtaa_nopeus = 2
        self.naytto = pygame.display.set_mode((self.leveys, self.korkeus))
        self.oikealle = False
        self.vasemmalle = False
        self.ylos = False
        self.alas = False
        self.luo_laatikot()
        self.luo_hahmot()
        # self.tarkista()
        # self.liiku()
        # self.piirra()
        self.valot_paalla = False
        self.silmukka()

    def lataa_kuvat(self):
        self.hirvio = pygame.image.load("hirvio.png")
        self.hirvio_mitat = (self.hirvio.get_width(), self.hirvio.get_height())
        self.robo = pygame.image.load("robo.png")
        self.robo_mitat = (self.robo.get_width(), self.robo.get_height())
        self.kolikko = pygame.image.load("kolikko.png")
        self.kolikko_mitat = (self.kolikko.get_width(), self.kolikko.get_height())
        self.ovi = pygame.image.load("ovi.png")
        self.ovi_mitat = (self.ovi.get_width(), self.ovi.get_height())


    def luo_laatikot(self):

        #  Pelissä on näköesteenä viisi erikokoista laatikkoa, jotka sijoitetaan sattumanvaraisesti
        #  Laatikot eivät saa olla liian lähellä reunoja.
        #  Koska robo.png on mitoiltaa suurin, käytetään sitä minimietäisyyden määrittelynä.
        #  Minimietäisyys = robon mitta + 10 px

        # Laatikon pituus määritellään omalla mitalla, joka on näytön leveys / 16

        mitta = self.leveys / 16
        vara = (self.robo_mitat[0] + 10, self.robo_mitat[1] + 1)
        self.laatikot = []
        laatikot_mitat = [(2, 2), (3, 2), (2, 3), (1, 2), (1, 1)]

        for n in range(len(laatikot_mitat)):
            while len(self.laatikot) < n + 1:
                laatikko = pygame.Rect(randrange(0, self.leveys), randrange(0, self.korkeus), mitta * laatikot_mitat[n][0] + vara[0] * 2, mitta * laatikot_mitat[n][1] + vara[1] * 2)
                if laatikko.collidelistall(self.laatikot):  # Tarkistetaan, etteivät laatikot leikkaa toisiaan
                    continue
                if laatikko.x + laatikko.width > self.leveys or laatikko.y + laatikko.height > self.korkeus:
                    continue
                laatikko.inflate_ip(-vara[0] * 2, -vara[1] * 2)
                self.laatikot.append(laatikko)
                print(laatikko.x)

    def luo_hahmot(self):
        self.pelaaja = []
        self.morot = []

        pelaaja_valmis = False

        while not pelaaja_valmis:
            # Luodaan robon mittojen mukainen tilapäinen laatikko ja varmistetaan, ettei se ole minkään neliön sisällä
            x = randrange(0, self.leveys - self.robo_mitat[0])
            y = randrange(0, self.korkeus - self.robo_mitat[1])
            if not pygame.Rect(x, y, self.robo_mitat[0], self.robo_mitat[1]).collidelistall(self.laatikot):
                    self.pelaaja = [[x, y], [x + self.robo_mitat[0] / 2, y + self.robo_mitat[1] / 2], False]  # Robon tiedot sisältävät sijainnin sekä keskipisteen, josta mitataan, onko möröillä näköyhteys roboon.
                    pelaaja_valmis = True

        while len(self.morot) < 2:
            x = randrange(0, self.leveys - self.hirvio_mitat[0])
            y = randrange(0, self.korkeus - self.hirvio_mitat[1])

            if not pygame.Rect(x, y, self.hirvio_mitat[0], self.hirvio_mitat[1]).collidelistall(self.laatikot):

                osumia = False
                for laatikko in self.laatikot:
                    if laatikko.clipline(self.pelaaja[1][0], self.pelaaja[1][1], x + self.hirvio_mitat[0], y + 14 ):
                        osumia = True
                        break
                if osumia:
                    self.morot.append([[x, y], [x + self.hirvio_mitat[0] / 2, y + 14], False, self.etsi([x, y])])  # Tallennetaan möröistä sijainti, näön lähtöpiste sekä viimeisenä tieto, onko mörkö havainnut robon (True = näkee, False = ei näe)
        print(self.pelaaja)

    def liiku(self):

        # Ensin pelaajan liike

        if self.oikealle:
            self.pelaaja[0][0] += self.robonopeus
            self.pelaaja[1][0] += self.robonopeus

        if self.vasemmalle:
            self.pelaaja[0][0] -= self.robonopeus
            self.pelaaja[1][0] -= self.robonopeus

        if self.alas:
            self.pelaaja[0][1] += self.robonopeus
            self.pelaaja[1][1] += self.robonopeus

        if self.ylos:
            self.pelaaja[0][1] -= self.robonopeus
            self.pelaaja[1][1] -= self.robonopeus

        # Sitten mörköjen liike

        for morko in self.morot:
            if morko[2]:
                morko[3] = self.pelaaja[0].copy()
            else:
                if morko[0] == morko[3]:
                    morko[3] = self.etsi(morko[0])

            # Katsotaan reitti robon luo
            askeleet = max(abs(morko[3][0] - morko[0][0]), abs(morko[3][1] - morko[0][1]))
            morko[0][0] += float(morko[3][0] - morko[0][0]) / askeleet
            morko[0][1] += float(morko[3][1] - morko[0][1]) / askeleet
            morko[1][0] += float(morko[3][0] - morko[0][0]) / askeleet
            morko[1][1] += float(morko[3][1] - morko[0][1]) / askeleet


    def tarkista(self):
        nahty = 0
        for morko in self.morot:
            morko[2] = False
            osumia = False
            for laatikko in self.laatikot:
                if laatikko.clipline(self.pelaaja[1][0], self.pelaaja[1][1], morko[1][0], morko[1][1]):
                    osumia = True
                    break
            if not osumia and sqrt((self.pelaaja[1][0] - morko[1][0]) ** 2 + (self.pelaaja[1][1] - morko[1][1]) ** 2) < self.korkeus / 2:
                morko[2] = True
                nahty += 1
            # print("Näkeekö mörkö: ", morko[4])

        if nahty > 0:
            self.pelaaja[2] = True
        else:
            self.pelaaja[2] = False

        print("Onko pelaaja nähty?", self.pelaaja[2])

        
        ## Näkeekö mörkö pelaajaa?


    def valot(self):

        self.valot_paalla = False
        if self.pelaaja[2]:
            self.valot_paalla = True
        else:
            self.valot_paalla = False
        # for morko in self.morot:
        #     if morko[4]:
        #         self.valot_paalla = True
        #         break


    def piirra(self):
            if self.valot_paalla:
                self.naytto.fill((255, 255, 255))
            else:
                self.naytto.fill((0, 0, 0))
            for laatikko in self.laatikot:
                pygame.draw.rect(self.naytto, (255, 0, 0), laatikko)
            self.naytto.blit(self.robo, (self.pelaaja[0][0], self.pelaaja[0][1]))
            for morko in self.morot:
                self.naytto.blit(self.hirvio, (morko[0][0], morko[0][1]))
                if morko[2]:
                    pygame.draw.line(self.naytto, (0, 0, 255), (morko[1][0], morko[1][1]), (self.pelaaja[1][0], self.pelaaja[1][1]))


    def etsi(self, sijainti: list):
        ok = False
        while not ok:
            x = randrange(0, int(self.leveys - self.hirvio_mitat[0]))
            y = randrange(0, int(self.leveys - self.hirvio_mitat[1]))
            osumia = 0
            for laatikko in self.laatikot:
                if laatikko.clipline(sijainti[0], sijainti[1], x, y):
                    osumia += 1
            if osumia == 0:
                ok = True
        return [x, y]


    def silmukka(self):
        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    exit()
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_SPACE:
                        if self.valot_paalla:
                            self.valot_paalla = False
                        else:
                            self.valot_paalla = True

                    if tapahtuma.key == pygame.K_LEFT:
                        self.vasemmalle = True

                    if tapahtuma.key == pygame.K_RIGHT:
                        self.oikealle = True

                    if tapahtuma.key == pygame.K_UP:
                        self.ylos = True

                    if tapahtuma.key == pygame.K_DOWN:
                        self.alas = True

                if tapahtuma.type == pygame.KEYUP:

                    if tapahtuma.key == pygame.K_LEFT:
                        self.vasemmalle = False

                    if tapahtuma.key == pygame.K_RIGHT:
                        self.oikealle = False

                    if tapahtuma.key == pygame.K_UP:
                        self.ylos = False

                    if tapahtuma.key == pygame.K_DOWN:
                        self.alas = False

            self.liiku()
            self.tarkista()
            self.valot()
            self.piirra()

            pygame.display.flip()
            self.kello.tick(60)


peli = Ajojahti()


