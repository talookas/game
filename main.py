import pygame, random

# Pygame'i initsialiseerimine
pygame.init()

# järjendid, et hoida vaenlaste, objektide ja plahvatuste positsioone 
vaenlased = []
objektid = []
plahvatused = []

# Hoiab ajal silma peal millal viimane vaenlane oli ekraanile pandud
vaenlase_ilmumis_aeg = 0

# Paneb ülesse mängu ekraani
ekraani_laius = 800
ekraani_kõrgus = 600
ekraan = pygame.display.set_mode((ekraani_laius, ekraani_kõrgus))
pygame.display.set_caption("2D Kosmose Mäng")

# Laeme mängu pildid
mängija_pilt = pygame.transform.scale(pygame.image.load("pildid/mängija.png"), (50, 50))
vaenlase_pilt = pygame.transform.scale(pygame.image.load("pildid/vaenlane.png"), (50, 50))
objekti_pilt = pygame.transform.scale(pygame.image.load("pildid/objekt.png"), (50, 50))
plahvatuse_pilt = pygame.transform.scale(pygame.image.load("pildid/plahvatus.png"), (50, 50))

# Laeme helid
kuuli_heli = pygame.mixer.Sound("helid/kuul.wav")
plahvatuse_heli = pygame.mixer.Sound("helid/plahvatus.wav")

# Laeme tausta muusika
pygame.mixer.music.load("muusika/tausta_muusika.mp3")
pygame.mixer.music.set_volume(3)
pygame.mixer.music.play(-1)

# Mängija algne positsioon ekraanil
mängija_x = 400
mängija_y = 500

# Seadistab punktide summa teksti font
skoori_font = pygame.font.Font(None, 36)

vaenlase_ilmumis_sagedus = 1500  # algne vaenlaste ilmumis sagedus
punktid = 0  # mängija algne punktide summa
punktide_lävend = 100  # vajatud punktide summa, et rohkem vaenlasi ilmuks ekraanile
sageduse_suurendus = 100  # summa, mille võrra vaenlaste ilmumis sagedust vähendatakse iga kord, kui vajatud punktide summa saavutatakse

# Teeme mängu tsükli
clock = pygame.time.Clock()
on_jooksmas = True
on_pausil = False
on_mäng_läbi = False

def kontrolli_kokkupuuteid(objek_x, objek_y, objek_w, objek_h, vaenlane_x, vaenlane_y, vaenlane_w, vaenlane_h):
        # teeb objektide ja vaenlaste jaoks piiri kastid
        objek_rect = pygame.Rect(objek_x, objek_y, objek_w, objek_h)
        vaenlane_rect = pygame.Rect(vaenlane_x, vaenlane_y, vaenlane_w, vaenlane_h)
        # tagastab kas objekti ja vaenlase piiri kastid põrkuvad või mitte
        return objek_rect.colliderect(vaenlane_rect)

while on_jooksmas:
    # Haldab sündmusi
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            on_jooksmas = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Lisab objekti järjendisse, mis asub natukene üleval pool mängija asukohast ja teeb heli
                objektid.append([mängija_x + mängija_pilt.get_width() / 2 - objekti_pilt.get_width() / 2, mängija_y])
                kuuli_heli.play()
            if event.key == pygame.K_ESCAPE:
                on_pausil = not on_pausil
                
    # Haldab pausi menu sündmusi
    if on_pausil:
        # Toob ekraanile pausi menu
        paus_font = pygame.font.SysFont("Arial", 50)
        paus_tekst = paus_font.render("Pausil", True, (255,255,255))
        paus_rect = paus_tekst.get_rect(center=(ekraani_laius/2, ekraani_kõrgus/2 - 50))
        ekraan.blit(paus_tekst, paus_rect)

        jätka_tekst = skoori_font.render("Vajutage SPACE jätkamiseks", True, (255,255,255))
        jätka_rect = jätka_tekst.get_rect(center=(ekraani_laius/2, ekraani_kõrgus/2))
        ekraan.blit(jätka_tekst, jätka_rect)

        väljumine_tekst = skoori_font.render("Vajutage ESC väljumiseks", True, (255,255,255))
        väljumine_rect = väljumine_tekst.get_rect(center=(ekraani_laius/2, ekraani_kõrgus/2 + 50))
        ekraan.blit(väljumine_tekst, väljumine_rect)

        pygame.display.update()

        # Ootab kuni mängija otsustab ära kas minna tagasi mängu või väljuda
        while on_pausil:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        on_pausil = False
                    if event.key == pygame.K_ESCAPE:
                        on_jooksmas = False
                        on_pausil = False
    elif not on_mäng_läbi:
        # Uuendab mängu seisu
        klahvid = pygame.key.get_pressed()
        if klahvid[pygame.K_LEFT] and mängija_x > 0:
            mängija_x -= 10
        if klahvid[pygame.K_RIGHT] and mängija_x < ekraani_laius - mängija_pilt.get_width():
            mängija_x += 10
        if klahvid[pygame.K_UP] and mängija_y > 0:
            mängija_y -= 10
        if klahvid[pygame.K_DOWN] and mängija_y < ekraani_kõrgus - mängija_pilt.get_height():
            mängija_y += 10

        # Toob ekraanile uue vaenlase
        vaenlase_ilmumis_aeg += clock.get_time()
        if vaenlase_ilmumis_aeg >= vaenlase_ilmumis_sagedus:
            vaenlased.append([random.randint(0, ekraani_laius - vaenlase_pilt.get_width()), -vaenlase_pilt.get_height()])
            vaenlase_ilmumis_aeg = 0

        # Liigutab vaenlasi alla ja eemaldab nad kui lähevad alt ära
        for vaenlane in vaenlased:
            vaenlane[1] += 3
            if vaenlane[1] > ekraani_kõrgus:
                vaenlased.remove(vaenlane)

    # Toob ekraanile mängu objektid (taust, mängija)
    tausta_pilt = pygame.image.load("pildid/tausta_pilt.png")
    tausta_pilt = pygame.transform.scale(tausta_pilt, (ekraani_laius, ekraani_kõrgus))
    ekraan.blit(tausta_pilt, (0, 0))
    ekraan.blit(mängija_pilt, (mängija_x, mängija_y))

    # Liigutab kuule ekraanil üles ja eemaldab need, kui need üleval ekraanist välja lähevad
    for objekt in objektid:
        objekt[1] -= 5
        if objekt[1] < -objekti_pilt.get_height():
            objektid.remove(objekt)
        else:
            # Kontrollib kuulide kokku puutumist vaenlastega
            for vaenlane in vaenlased:
                if kontrolli_kokkupuuteid(objekt[0], objekt[1], objekti_pilt.get_width(), objekti_pilt.get_height(), vaenlane[0], vaenlane[1], vaenlase_pilt.get_width(), vaenlase_pilt.get_height()):
                    objektid.remove(objekt)
                    vaenlased.remove(vaenlane)
                    plahvatuse_rect = plahvatuse_pilt.get_rect(center=(vaenlane[0] + vaenlase_pilt.get_width() / 2, vaenlane[1] + vaenlase_pilt.get_height() / 2))
                    # Lisab plahvatuse informatsioon loendisse koos selle kujutise ristküliku positsiooni ja plahvatuse toimumise ajaga
                    plahvatused.append({'ristkülik': plahvatuse_rect, 'aeg': pygame.time.get_ticks()})
                    plahvatuse_heli.play()
                    punktid += 10
                    # Toob esile rohkem vaenlasi iga kord, kui kogutud punktide summa suureneb vajatud lävendini
                    if punktid >= punktide_lävend:
                        vaenlase_ilmumis_sagedus -= sageduse_suurendus
                        punktide_lävend += 100
                    break
        ekraan.blit(objekti_pilt, (objekt[0], objekt[1]))

    # Kontrollib, kas iga loendis olev plahvatus on endiselt nähtava kestusega 500 millisekundit
    for explosion in plahvatused:
        if pygame.time.get_ticks() - explosion['aeg'] <= 500:
            # Kui tõsi, joonistab plahvatuspilt aknale selle asendi, kasutades sõnastikku salvestatud ristküliku teavet
            ekraan.blit(plahvatuse_pilt, explosion['ristkülik'])
        else:
             # Kui ei, eemaldab plahvatussõnastik loendist, kuna seda pole enam vaja
             plahvatused.remove(explosion)

    for vaenlane in vaenlased:
        ekraan.blit(vaenlase_pilt, (vaenlane[0], vaenlane[1]))
        if vaenlane[1] > ekraani_kõrgus - vaenlase_pilt.get_height() - 10:
            # Vaenlane jõudis alla, mängi läbi
            on_jooksmas = False
        elif kontrolli_kokkupuuteid(mängija_x, mängija_y, mängija_pilt.get_width(), mängija_pilt.get_height(), vaenlane[0], vaenlane[1], vaenlase_pilt.get_width(), vaenlase_pilt.get_height()):
            # Mängija põrkus kokku vaenlasega, mäng läbi
            on_jooksmas = False

    # Toob esile punktide summa ekraanil
    skoori_font = pygame.font.SysFont("Arial", 25)
    skoori_tekst = skoori_font.render(f"Punktid: {punktid}", True, (255,255,255))
    ekraan.blit(skoori_tekst, (10, 10))

    pygame.display.update()

    # Limit frame rate
    clock.tick(60)

mängläbi_pilt = pygame.transform.scale(pygame.image.load("pildid/mäng_läbi.png"), (400, 250))
mängläbi_rect = mängläbi_pilt.get_rect(center=(ekraani_laius/2, ekraani_kõrgus/2))
ekraan.blit(mängläbi_pilt, mängläbi_rect)
pygame.display.update()
pygame.mixer.music.stop()
mängläbi_heli = pygame.mixer.Sound("helid/mäng_läbi.mp3")
mängläbi_heli.play()

pygame.time.wait(5000)
pygame.quit()