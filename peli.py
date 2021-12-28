# Ajojahti
# Lähdekoodi: https://github.com/jukper/ajojahti

import pygame
from random import randrange, choice
from math import sqrt

class Ajojahti:
    def __init__(self):
        pygame.init()
        self.kello = pygame.time.Clock()
        self.lataa_kuvat()
        self.leveys = 1280
        self.korkeus = 720
        self.robonopeus = 2.2
        self.etsi_nopeus = 1
        self.jahtaa_nopeus = 2
        self.naytto = pygame.display.set_mode((self.leveys, self.korkeus))
        self.oikealle = False
        self.vasemmalle = False
        self.ylos = False
        self.alas = False
        self.luo_laatikot()
        self.luo_hahmot()
        self.pisteet = 0
        self.pelikerrat = []
        # self.tarkista()
        # self.liiku()
        # self.piirra()
        self.valot_paalla = False
        self.aarre_loydetty = False
        self.fontti = pygame.font.SysFont("Arial", 24)
        self.otsikkofontti = pygame.font.SysFont("Arial", 40, True)
        pygame.display.set_caption("Ajojahti!")
        self.aloitusruutu()
        self.silmukka()

    def aloitusruutu(self):
        aloita = False
        lopeta = False
        komento_ok = False
        otsikko = self.otsikkofontti.render("AJOJAHTI", True, (255, 0, 0))
        ohje1 = self.fontti.render("1. Etsi kätketty aarre", True, (255, 0, 0))
        ohje2 = self.fontti.render("2. Pakene huoneesta", True, (255, 0, 0))
        ohje3 = self.fontti.render("3. Älä jää kiinni", True, (255, 0, 0))
        x = -100
        y = 100
        teksti = self.fontti.render("F2: Aloita peli. ESC: lopeta peli", True, (255, 0, 0))
        while not komento_ok:
            self.naytto.fill((0, 0, 0))
            self.naytto.blit(self.robo, (x, y))
            self.naytto.blit(self.hirvio, (x -200, y))
            self.naytto.blit(otsikko, (self.leveys / 2 - otsikko.get_width() / 2, 20))

            self.naytto.blit(ohje1, (self.leveys / 2 - ohje1.get_width() / 2, 250))
            self.naytto.blit(ohje2, (self.leveys / 2 - ohje1.get_width() / 2, 300))
            self.naytto.blit(ohje3, (self.leveys / 2 - ohje1.get_width() / 2, 350))

            self.naytto.blit(teksti, (self.leveys / 2 - teksti.get_width() / 2, 500))

            # self.naytto.blit(teksti, (self.leveys / 2 - teksti.get_width() / 2, self.korkeus / 2 - teksti.get_height() / 2))
            # self.naytto.blit(teksti, (self.leveys / 2 - teksti.get_width() / 2, self.korkeus / 2 - teksti.get_height() / 2))
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    exit()
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_F2:
                        aloita = True
                        komento_ok = True
                    if tapahtuma.key == pygame.K_ESCAPE:
                        lopeta = True
                        komento_ok = True
            pygame.display.flip()
            x += 5
            if x > self.leveys + 300:
                x = -100
            self.kello.tick(60)

        if aloita:
            return
        if lopeta:
            exit()

    def uusi_peli(self):
        aloita = False
        lopeta = False
        ennatys = False
        tulostaulukko = self.pelikerrat.copy()
        tulostaulukko.sort(reverse=True)
        pisteet = []
        for n in range(len(tulostaulukko)):
            if n > 2:
                break
            if tulostaulukko[n] != 1:
                pisteet.append(self.fontti.render(f'{n + 1}. sija: {tulostaulukko[n]} pistettä', True, (255, 0, 0)))
            else:
                pisteet.append(self.fontti.render(f'{n + 1}. sija: {tulostaulukko[n]} piste', True, (255, 0, 0)))

        if len(self.pelikerrat) > 0 and 0 < self.pisteet > max(self.pelikerrat):
            ennatys = True
        self.pelikerrat.append(self.pisteet)
        komento_ok = False
        while not komento_ok:
            self.naytto.fill((0, 0, 0))

            if ennatys:
                teksti1 = self.fontti.render(f'Jäit kiinni. Pistemääräsi: {self.pisteet} (UUSI ENNÄTYS!)', True, (255, 0, 0))
            else:
                teksti1 = self.fontti.render(f'Jäit kiinni. Pistemääräsi: {self.pisteet}', True, (255, 0, 0))

            pistevali = 30
            for piste in pisteet:
                self.naytto.blit(piste, (self.leveys / 2 - piste.get_width() / 2, 450 + pistevali))
                pistevali += 30

            teksti2 = self.fontti.render("F2: Uusi peli. ESC: lopeta peli", True, (255, 0, 0))
            self.naytto.blit(teksti1, (self.leveys / 2 - teksti1.get_width() / 2, self.korkeus / 2 - (teksti1.get_height() + 10 + teksti2.get_height()) / 2 ))
            self.naytto.blit(teksti2, (self.leveys / 2 - teksti2.get_width() / 2, self.korkeus / 2 - teksti2.get_height() / 2 + 20))
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    exit()
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_F2:
                        aloita = True
                        komento_ok = True
                    if tapahtuma.key == pygame.K_ESCAPE:
                        lopeta = True
                        komento_ok = True
            pygame.display.flip()
        if aloita:
            self.oikealle = False
            self.vasemmalle = False
            self.ylos = False
            self.alas = False
            self.pisteet = 0
            self.uusi_huone()
        if lopeta:
            exit()



    def uusi_huone(self):
        print("pisteitä:", self.pisteet)
        self.valot_paalla = False
        self.aarre_loydetty = False
        self.luo_laatikot()
        self.luo_hahmot()


    def lataa_kuvat(self):
        self.hirvio = pygame.image.load("hirvio.png")
        self.hirvio_mitat = (self.hirvio.get_width(), self.hirvio.get_height())
        self.robo = pygame.image.load("robo.png")
        self.robo_mitat = (self.robo.get_width(), self.robo.get_height())
        self.kolikko = pygame.image.load("kolikko.png")
        self.kolikko_mitat = (self.kolikko.get_width(), self.kolikko.get_height())
        self.ovi = pygame.image.load("ovi.png")
        self.ovi_mitat = (self.ovi.get_width(), self.ovi.get_height())
        # Pelihahmoja varten määritellään offset, jolla lasketaan ne pisteet, joista möröt katsovat ja jonka ne robossa näkevät
        self.robo_nakopiste = (self.robo_mitat[0] / 2, self.robo_mitat[1] / 2)
        self.morko_nakopiste = (self.hirvio_mitat[0] / 2, 14)


    def luo_laatikot(self):

        #  Pelissä on näköesteenä erikokoisia laatikoita, jotka sijoitetaan huoneeseen sattumanvaraisesti
        #  Laatikot eivät saa olla liian lähellä reunoja.
        #  Koska robo.png on mitoiltaa suurin, käytetään sitä minimietäisyyden määrittelynä.
        #  Minimietäisyys = robon mitta + 10 px

        # Laatikon pituus määritellään omalla mitalla, joka on näytön leveys / 16

        mitta = self.leveys / 16
        vara = (self.robo_mitat[0] + 10, self.robo_mitat[1] + 1)
        self.laatikot = []
        laatikot_mitat = [ (3, 2), (2, 4), (1, 1), (3,0.5), (0.5, 4), (1.5, 1.5)]

        for n in range(len(laatikot_mitat)):
            while len(self.laatikot) < n + 1:
                laatikko = pygame.Rect(randrange(0, self.leveys), randrange(0, self.korkeus), mitta * laatikot_mitat[n][0] + vara[0] * 2, mitta * laatikot_mitat[n][1] + vara[1] * 2)
                if laatikko.collidelistall(self.laatikot):  # Tarkistetaan, etteivät laatikot leikkaa toisiaan
                    continue
                if laatikko.x + laatikko.width > self.leveys or laatikko.y + laatikko.height > self.korkeus:
                    continue
                laatikko.inflate_ip(-vara[0] * 2, -vara[1] * 2)
                self.laatikot.append(laatikko)

    def luo_hahmot(self):
        self.pelaaja = []
        self.morot = []
        self.uloskaynti = []
        self.aarre = []
        morkoja = 2

        pelaaja_valmis = False

        while not pelaaja_valmis:
            # Luodaan robon mittojen mukainen tilapäinen laatikko ja varmistetaan, ettei se ole minkään neliön sisällä
            x = randrange(0, self.leveys - self.robo_mitat[0])
            y = randrange(0, self.korkeus - self.robo_mitat[1])
            if not pygame.Rect(x, y, self.robo_mitat[0], self.robo_mitat[1]).collidelistall(self.laatikot):
                    self.pelaaja = [[x, y], False]  # Robon tiedot sisältävät sijainnin sekä keskipisteen, josta mitataan, onko möröillä näköyhteys roboon.
                    pelaaja_valmis = True

        while len(self.morot) < morkoja:
            x = randrange(0, self.leveys - self.hirvio_mitat[0])
            y = randrange(0, self.korkeus - self.hirvio_mitat[1])

            if not pygame.Rect(x, y, self.hirvio_mitat[0], self.hirvio_mitat[1]).collidelistall(self.laatikot):

                osumia = False
                for laatikko in self.laatikot:
                    if laatikko.clipline(self.katse([x, y])):
                        osumia = True
                        break
                if osumia:
                    self.morot.append([[x, y], False, self.etsi([x, y])])  # Tallennetaan möröistä sijainti, näön lähtöpiste sekä viimeisenä tieto, onko mörkö havainnut robon (True = näkee, False = ei näe)

        aarre_valmis = False
        while not aarre_valmis:
            x = randrange(0, self.leveys - self.kolikko_mitat[0])
            y = randrange(0, self.korkeus - self.kolikko_mitat[1])
            if not self.kolikko.get_rect(topleft=[x, y]).collidelistall(self.laatikot):
                self.aarre.append([x, y])
                aarre_valmis = True

        uloskaynti_valmis = False
        while not uloskaynti_valmis:
            x = randrange(0, self.leveys - self.ovi_mitat[0])
            y = randrange(0, self.korkeus - self.ovi_mitat[1])
            if not self.ovi.get_rect(topleft=[x, y]).collidelistall(self.laatikot):
                self.uloskaynti.append([x, y])
                self.uloskaynti.append(False)
                uloskaynti_valmis = True


    def liiku(self):

        # Ensin pelaajan liike

        if self.oikealle and self.pelaaja[0][0] + self.robo_mitat[0] + self.robonopeus <= self.leveys:
            if self.robo.get_rect(topleft=[self.pelaaja[0][0] + self.robonopeus, self.pelaaja[0][1]]).collidelist(self.laatikot) < 0:
                self.pelaaja[0][0] += self.robonopeus

        if self.vasemmalle and self.pelaaja[0][0] >= self.robonopeus:
            if self.robo.get_rect(topleft=[self.pelaaja[0][0] - self.robonopeus, self.pelaaja[0][1]]).collidelist(self.laatikot) < 0:
                self.pelaaja[0][0] -= self.robonopeus

        if self.alas and self.pelaaja[0][1] + self.robo_mitat[1] + self.robonopeus <= self.korkeus:
            if self.robo.get_rect(topleft=[self.pelaaja[0][0], self.pelaaja[0][1] + self.robonopeus]).collidelist(self.laatikot) < 0:
                self.pelaaja[0][1] += self.robonopeus

        if self.ylos and self.pelaaja[0][1] >= self.robonopeus:
            if self.robo.get_rect(topleft=[self.pelaaja[0][0], self.pelaaja[0][1] - self.robonopeus]).collidelist(self.laatikot) < 0:
                self.pelaaja[0][1] -= self.robonopeus

        # Sitten mörköjen liike

        for morko in self.morot:
            if morko[1]:
                morko[2] = self.pelaaja[0].copy()
            else:
                # Mikäli mörkö on 10 pikselin päässä kohteesta, se valitsee uuden kohteen
                if sqrt((morko[2][0] - morko[0][0]) ** 2 + (morko[2][1] - morko[0][1]) ** 2) < 10:
                    morko[2] = self.etsi(morko[0])

            # Katsotaan reitti kohteen luo
            askeleet = max(abs(morko[2][0] - morko[0][0]), abs(morko[2][1] - morko[0][1]))


            if morko[1] or self.uloskaynti[1]:
                nopeus = 2
            else:
                nopeus = 1

            morko[0][0] += float(morko[2][0] - morko[0][0]) / askeleet * nopeus
            morko[0][1] += float(morko[2][1] - morko[0][1]) / askeleet * nopeus


            # Ei törmätä laatikkoon

            self.osumakorjaus(morko)

    def katse(self, morko_sijainti: list):
        robon_piste = [self.pelaaja[0][0] + self.robo_nakopiste[0], self.pelaaja[0][1] + self.robo_nakopiste[1]]
        moron_piste = [morko_sijainti[0] + self.morko_nakopiste[0], morko_sijainti[1] + self.morko_nakopiste[1]]
        return [robon_piste, moron_piste]


    def osumakorjaus(self, morko: list):

        osumalaatikko = self.hirvio.get_rect(topleft=morko[0])

        osumakynnys = 5
        x = osumalaatikko.x
        y = osumalaatikko.y

        for n in osumalaatikko.collidelistall(self.laatikot):
            if abs(self.laatikot[n].left - osumalaatikko.right) < osumakynnys:
                x = self.laatikot[n].left - osumalaatikko.w - osumakynnys
                morko[2][1] = morko[0][1] + choice([10, -10])



            if abs(self.laatikot[n].right - osumalaatikko.left) < osumakynnys:
                x = self.laatikot[n].right + osumakynnys
                morko[2][1] = morko[0][1] + choice([10, -10])

            if abs(self.laatikot[n].top - osumalaatikko.bottom) < osumakynnys:
                y = self.laatikot[n].top - osumalaatikko.h - osumakynnys
                morko[2][0] = morko[0][0] + choice([10, -10])


            if abs(self.laatikot[n].bottom - osumalaatikko.top) < osumakynnys:
                y = self.laatikot[n].bottom + osumakynnys
                morko[2][0] = morko[0][0] + choice([10, -10])

        morko[0][0] = x
        morko[0][1] = y

        return morko

    def tarkista(self):

        # Onko kolikko napattu?

        if len(self.aarre) > 0:
            if self.robo.get_rect(topleft=self.pelaaja[0]).colliderect(self.kolikko.get_rect(topleft=self.aarre[0])):
                self.aarre.pop(0)
                self.uloskaynti[1] = True
                print("Kolikko saatu! Sitten ulko-ovelle.")

        # Onko pelaaja päässyt ovelle saatuaan aarteen?
        if self.uloskaynti[1]:
            if self.robo.get_rect(topleft=self.pelaaja[0]).colliderect(self.ovi.get_rect(topleft=self.uloskaynti[0])):
                self.pisteet += 1
                self.uusi_huone()

        nahty = 0
        for morko in self.morot:

            # Onko robo napattu?
            if self.hirvio.get_rect(topleft=morko[0]).colliderect(self.robo.get_rect(topleft=self.pelaaja[0])):
                print("Peli loppui!")
                self.uusi_peli()

            # Näkeekö mörkö robon?

            morko[1] = False
            osumia = False
            katsevektori = self.katse(morko[0])

            # Katsotaan, onko möröllä näkesteitä

            for laatikko in self.laatikot:
                if laatikko.clipline(katsevektori[0], katsevektori[1]):
                    osumia = True
                    break
            if not osumia and sqrt((katsevektori[0][0] - katsevektori[1][0]) ** 2 + (katsevektori[0][1] - katsevektori[1][1]) ** 2) < self.korkeus / 2:
                morko[1] = True
                nahty += 1
            # print("Näkeekö mörkö: ", morko[4])


        if nahty > 0:
            self.pelaaja[1] = True
        else:
            self.pelaaja[1] = False


        # Tarkistetaan, ettei kukaan liiku ikkunan ulkopuolelle



    def valot(self):

        if self.uloskaynti[1]:
            self.valot_paalla = True
            return

        self.valot_paalla = False
        if self.pelaaja[1]:
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
                if len(self.aarre) > 0:
                    self.naytto.blit(self.kolikko, self.aarre[0])
                self.naytto.blit(self.ovi, self.uloskaynti[0])
            else:
                self.naytto.fill((0, 0, 0))
            for laatikko in self.laatikot:
                pygame.draw.rect(self.naytto, (255, 0, 0), laatikko)
            self.naytto.blit(self.robo, (self.pelaaja[0][0], self.pelaaja[0][1]))
            for morko in self.morot:
                self.naytto.blit(self.hirvio, (morko[0][0], morko[0][1]))
                if morko[1]:
                    viiva = self.katse(morko[0])
                    pygame.draw.line(self.naytto, (255, 0, 0), viiva[0], viiva[1])
            teksti1 = self.fontti.render(f'Pisteitä: {self.pisteet}', True, (255, 0, 0))

            if self.uloskaynti[1]:
                teksti2 = self.fontti.render(f'Pakene huoneesta!', True, (255, 0, 0))
            else:
                teksti2 = self.fontti.render(f'Etsi aarre.', True, (255, 0, 0))
            self.naytto.blit(teksti1, (self.leveys - teksti1.get_width(), 0))
            self.naytto.blit(teksti2, (self.leveys - teksti2.get_width(), self.korkeus - teksti2.get_height()))

                # print(f'Mörön sijainti: {morko[0]}, mörön kohde{morko[2]}')


    def etsi(self, sijainti: list):
        ok = False
        while not ok:
            x = randrange(0, int(self.leveys - self.hirvio_mitat[0]))
            y = randrange(0, int(self.korkeus - self.hirvio_mitat[1]))
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

            self.tarkista()
            self.liiku()
            self.valot()
            self.piirra()

            pygame.display.flip()
            self.kello.tick(60)

peli = Ajojahti()
