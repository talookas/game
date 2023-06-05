import pygame, random

# pygame'i initsialiseerimine
pygame.init()

# järjendid, et hoida vaenlaste, objektide ja plahvatuste positsioone 
vaenlased = []
objektid = []
plahvatused = []

# hoiab ajal silma peal millal viimane vaenlane oli ekraanile pandud
vaenlase_ilmumis_aeg = 0

# paneb ülesse mängu ekraani
ekraani_laius = 800
ekraani_kõrgus = 600
ekraan = pygame.display.set_mode((ekraani_laius, ekraani_kõrgus))
pygame.display.set_caption("2D Kosmose Mäng")

# laeme mängu pildid
mängija_pilt = pygame.transform.scale(pygame.image.load("pildid/mängija.png"), (50, 50))
vaenlase_pilt = pygame.transform.scale(pygame.image.load("pildid/vaenlane.png"), (50, 50))
objekti_pilt = pygame.transform.scale(pygame.image.load("pildid/objekt.png"), (50, 50))
plahvatuse_pilt = pygame.transform.scale(pygame.image.load("pildid/plahvatus.png"), (50, 50))

# laeme helid
kuuli_heli = pygame.mixer.Sound("helid/kuul.wav")
plahvatuse_heli = pygame.mixer.Sound("helid/plahvatus.wav")

# laeme tausta muusika
pygame.mixer.music.load("muusika/tausta_muusika.mp3")
pygame.mixer.music.set_volume(3)
pygame.mixer.music.play(-1)

# mängija algne positsioon ekraanil
mängija_x = 400
mängija_y = 500

vaenlase_ilmumis_sagedus = 1500  # algne vaenlaste ilmumis sagedus
punktid = 0  # mängija algne punktide summa
punktide_lävend = 100  # vajatud punktide summa, et rohkem vaenlasi ilmuks ekraanile
sageduse_suurendus = 100  # summa, mille võrra vaenlaste ilmumis sagedust vähendatakse

clock = pygame.time.Clock()
on_jooksmas = True
on_pausil = False
on_mäng_läbi = False


# funktsioon, mis toob esile ekraanil mängu juhendi
def näita_juhend():
    juhend_font = pygame.font.Font("fondid/JOYSTIX.TTF", 50)
    juhend_tekst = juhend_font.render("KUIDAS MÄNGIDA:", True, (194, 54, 68))
    juhend_rect = juhend_tekst.get_rect(center=(ekraani_laius / 2, ekraani_kõrgus / 2 - 200))
    ekraan.blit(juhend_tekst, juhend_rect)

    klahv_font = pygame.font.Font("fondid/JOYSTIX.TTF", 25)
    klahv_tekst = klahv_font.render("LIIKUMINE: NOOLEKLAHVID", True, (130, 184, 151))
    klahv_rect = klahv_tekst.get_rect(center=(ekraani_laius / 2, ekraani_kõrgus / 2 - 100))
    ekraan.blit(klahv_tekst, klahv_rect)

    tulis_font = pygame.font.Font("fondid/JOYSTIX.TTF", 25)
    tulis_tekst = tulis_font.render("LASKMINE: TÜHIKKLAHV", True, (130, 184, 151))
    tulis_rect = tulis_tekst.get_rect(center=(ekraani_laius / 2, ekraani_kõrgus / 2 - 20))
    ekraan.blit(tulis_tekst, tulis_rect)

    menu_font = pygame.font.Font("fondid/JOYSTIX.TTF", 25)
    menu_tekst = menu_font.render("PAUS MENU: ESC", True, (130, 184, 151))
    menu_rect = menu_tekst.get_rect(center=(ekraani_laius / 2, ekraani_kõrgus / 2 + 60))
    ekraan.blit(menu_tekst, menu_rect)

    m_font = pygame.font.Font("fondid/JOYSTIX.TTF", 25)
    m_tekst = m_font.render("JUHEND MENU: C", True, (130, 184, 151))
    m_rect = m_tekst.get_rect(center=(ekraani_laius / 2, ekraani_kõrgus / 2 + 140))
    ekraan.blit(m_tekst, m_rect)

    pygame.display.update()
    pygame.time.wait(5000)


# funktsioon, mis toob ekraanile pausi menu
def paus_menu():
    paus_font = pygame.font.Font("fondid/JOYSTIX.TTF", 45)
    paus_tekst = paus_font.render("PAUSIL", True, (0, 209, 167))
    paus_rect = paus_tekst.get_rect(center=(ekraani_laius / 2, ekraani_kõrgus / 2 - 50))
    ekraan.blit(paus_tekst, paus_rect)

    jätka_font = pygame.font.Font("fondid/JOYSTIX.TTF", 30)
    jätka_tekst = jätka_font.render("Vajutage SPACE jätkamiseks", True, (171, 209, 201))
    jätka_rect = jätka_tekst.get_rect(center=(ekraani_laius / 2, ekraani_kõrgus / 2))
    ekraan.blit(jätka_tekst, jätka_rect)

    välj_font = pygame.font.Font("fondid/JOYSTIX.TTF", 30)
    väljumine_tekst = välj_font.render("Vajutage ESC väljumiseks", True, (171, 209, 201))
    väljumine_rect = väljumine_tekst.get_rect(center=(ekraani_laius / 2, ekraani_kõrgus / 2 + 50))
    ekraan.blit(väljumine_tekst, väljumine_rect)

    pygame.display.update()


def kontrolli_kokkupuuteid(objek_x, objek_y, objek_w, objek_h, objek2_x, objek2_y, objek2_w, objek2_h):
    # teeb objektide jaoks piiri kastid
    objek_rect = pygame.Rect(objek_x, objek_y, objek_w, objek_h)
    objek2_rect = pygame.Rect(objek2_x, objek2_y, objek2_w, objek2_h)
    # tagastab kas objekti ja objekt2 piiri kastid põrkuvad või mitte
    return objek_rect.colliderect(objek2_rect)


näita_juhend()

while on_jooksmas:
    # haldab sündmusi
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            on_jooksmas = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # lisab objekti järjendisse, mis asub natukene üleval pool mängija asukohast ja teeb heli
                objektid.append([mängija_x + mängija_pilt.get_width() / 2 - objekti_pilt.get_width() / 2, mängija_y])
                kuuli_heli.play()
            if event.key == pygame.K_ESCAPE:
                on_pausil = not on_pausil
                
    # haldab pausi menu sündmusi
    if on_pausil:
        paus_menu()
        # ootab kuni mängija otsustab ära kas minna tagasi mängu või väljuda
        while on_pausil:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        on_pausil = False
                    if event.key == pygame.K_ESCAPE:
                        on_jooksmas = False
                        on_pausil = False
    elif not on_mäng_läbi:
        # uuendab mängu seisu
        klahvid = pygame.key.get_pressed()
        if klahvid[pygame.K_LEFT] and mängija_x > 0:
            mängija_x -= 10
        if klahvid[pygame.K_RIGHT] and mängija_x < ekraani_laius - mängija_pilt.get_width():
            mängija_x += 10
        if klahvid[pygame.K_UP] and mängija_y > 0:
            mängija_y -= 10
        if klahvid[pygame.K_DOWN] and mängija_y < ekraani_kõrgus - mängija_pilt.get_height():
            mängija_y += 10
        if klahvid[pygame.K_c]:
            näita_juhend()

        # toob ekraanile uue vaenlase
        vaenlase_ilmumis_aeg += clock.get_time()
        if vaenlase_ilmumis_aeg >= vaenlase_ilmumis_sagedus:
            vaenlased.append([random.randint(0, ekraani_laius - vaenlase_pilt.get_width()), -vaenlase_pilt.get_height()])
            vaenlase_ilmumis_aeg = 0

        # liigutab vaenlasi alla ja eemaldab nad kui lähevad alt ära
        for vaenlane in vaenlased:
            vaenlane[1] += 3
            if vaenlane[1] > ekraani_kõrgus:
                vaenlased.remove(vaenlane)

    # toob ekraanile mängu objektid (taust, mängija)
    tausta_pilt = pygame.image.load("pildid/tausta_pilt.png")
    tausta_pilt = pygame.transform.scale(tausta_pilt, (ekraani_laius, ekraani_kõrgus))
    ekraan.blit(tausta_pilt, (0, 0))
    ekraan.blit(mängija_pilt, (mängija_x, mängija_y))

    # liigutab kuule ekraanil üles ja eemaldab need
    for objekt in objektid:
        objekt[1] -= 5
        if objekt[1] < -objekti_pilt.get_height():
            objektid.remove(objekt)
        else:
            # kontrollib kuulide kokku puutumist vaenlastega
            for vaenlane in vaenlased:
                if kontrolli_kokkupuuteid(objekt[0], objekt[1], objekti_pilt.get_width(), objekti_pilt.get_height(), vaenlane[0], vaenlane[1], vaenlase_pilt.get_width(), vaenlase_pilt.get_height()):
                    objektid.remove(objekt)
                    vaenlased.remove(vaenlane)
                    plahvatuse_rect = plahvatuse_pilt.get_rect(center=(vaenlane[0] + vaenlase_pilt.get_width() / 2, vaenlane[1] + vaenlase_pilt.get_height() / 2))
                    # lisab plahvatuse informatsioon loendisse sõnastikkuna
                    plahvatused.append({'ristkülik': plahvatuse_rect, 'aeg': pygame.time.get_ticks()})
                    plahvatuse_heli.play()
                    punktid += 10
                    # toob esile rohkem vaenlasi
                    if punktid >= punktide_lävend:
                        vaenlase_ilmumis_sagedus -= sageduse_suurendus
                        punktide_lävend += 100
                    break
        ekraan.blit(objekti_pilt, (objekt[0], objekt[1]))

    # kontrollib loendis olevat plahvatust
    for plahvatus in plahvatused:
        if pygame.time.get_ticks() - plahvatus['aeg'] <= 500:
            ekraan.blit(plahvatuse_pilt, plahvatus['ristkülik'])
        else:
             plahvatused.remove(plahvatus)

    # toome esile vaenlased ja kontrollime mängu kaotus seisu
    for vaenlane in vaenlased:
        ekraan.blit(vaenlase_pilt, (vaenlane[0], vaenlane[1]))
        if vaenlane[1] > ekraani_kõrgus - vaenlase_pilt.get_height() - 10:
            on_jooksmas = False
        elif kontrolli_kokkupuuteid(mängija_x, mängija_y, mängija_pilt.get_width(), mängija_pilt.get_height(), vaenlane[0], vaenlane[1], vaenlase_pilt.get_width(), vaenlase_pilt.get_height()):
            on_jooksmas = False

    # toob esile punktide summa ekraanil
    skoori_font = pygame.font.Font("fondid/JOYSTIX.TTF", 25)
    skoori_tekst = skoori_font.render(f"Punktid: {punktid}", True, (227, 174, 51))
    ekraan.blit(skoori_tekst, (10, 10))

    pygame.display.update()

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