import pygame


from player import Player
from src.dialog import DialogBox
from src.map import MapManager


class Game:

    def __init__(self):
        self.running = True
        # Affichage de la fenêtre
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("BasiqueGame")
        self.groupeGlobal = pygame.sprite.Group()

        # Générer le joeur
        self.player = Player()
        self.dialog_box = DialogBox()

        # Définir le logo du jeu
        pygame.display.set_icon(self.player.image)

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_ESCAPE]:
            self.running = False
        elif pressed[pygame.K_UP]:
            self.player.move_up()
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()


    def update(self):
        self.map_manager.update()

    def menu(self):
        color = (255, 255, 255)
        color_light = (0, 200, 0)
        color_dark = (100, 100, 100)
        width = self.screen.get_width()
        height = self.screen.get_height()
        smallfont = pygame.font.SysFont('Corbel', 25)

        # rendering a text written in
        self.items = []
        with open(f"../textes/menu.txt", "r") as filin:
            for ligne in filin:
                ligne = ligne.replace('"', '').strip()
                self.items.append((ligne))
        print(self.items)


        # this font
        text1 = smallfont.render(self.items[0], True, color)
        text2 = smallfont.render(self.items[1], True, color)
        text3 = smallfont.render(self.items[2], True, color)
        text4 = smallfont.render(self.items[3], True, color)
        text5 = smallfont.render(self.items[4], True, color)

        image_fond = pygame.image.load("../medias/fond.png")
        logo_fond = pygame.image.load("../medias/logo.png")
        logo_fond = pygame.transform.scale(logo_fond, (width, height // 5))

        self.screen.blit(image_fond, (0, 0))
        self.screen.blit(logo_fond, (0, 0))

        while True:

            for ev in pygame.event.get():

                if ev.type == pygame.QUIT:
                    pygame.quit()

                    # checks if a mouse is clicked
                if ev.type == pygame.MOUSEBUTTONDOWN:

                    # if the mouse is clicked on the

                    if width / 2 <= mouse[0] <= width / 2 + 140 and (height / 2) - 100 <= mouse[1] <= height / 2 - 60:
                        self.language = 'fr'
                        self.run(self.language)
                    elif width / 2 <= mouse[0] <= width / 2 + 140 and (height / 2) - 50 <= mouse[1] <= height / 2 - 10:
                        self.language = 'en'
                        self.run(self.language)
                    elif width / 2 <= mouse[0] <= width / 2 + 140 and height / 2 <= mouse[1] <= height / 2 + 40:
                        self.language = 'de'
                        self.run(self.language)
                    elif width / 2 <= mouse[0] <= width / 2 + 140 and (height / 2) + 50 <= mouse[1] <= height / 2 + 90:
                        self.language = 'sp'
                        self.run(self.language)
                    elif width / 2 <= mouse[0] <= width / 2 + 140 and (height / 2) + 100 <= mouse[1] <= height / 2 + 160:
                        pygame.quit()

            mouse = pygame.mouse.get_pos()

            # if mouse is hovered on a button it
            # changes to lighter shade
            if width / 2 <= mouse[0] <= width / 2 + 140 and height / 2 <= mouse[1] <= height / 2 + 40:
                pygame.draw.rect(self.screen, color_light, [width / 2, height / 2, 140, 40])

            elif width / 2 <= mouse[0] <= width / 2 + 140 and (height / 2) + 50 <= mouse[1] <= height / 2 + 90:
                pygame.draw.rect(self.screen, color_light, [width / 2, (height / 2) + 50, 140, 40])

            elif width / 2 <= mouse[0] <= width / 2 + 140 and (height / 2) - 50 <= mouse[1] <= height / 2 - 10:
                pygame.draw.rect(self.screen, color_light, [width / 2, (height / 2) - 50, 140, 40])

            elif width / 2 <= mouse[0] <= width / 2 + 140 and (height / 2) - 100 <= mouse[1] <= height / 2 - 60:
               pygame.draw.rect(self.screen, color_light, [width / 2, (height / 2) - 100, 140, 40])

            elif width / 2 <= mouse[0] <= width / 2 + 140 and (height / 2) + 100 <= mouse[1] <= height / 2 + 160:
               pygame.draw.rect(self.screen, color_light, [width / 2, (height / 2) + 100, 140, 40])
            else:
                pygame.draw.rect(self.screen, color_dark, [width / 2, height / 2, 140, 40])
                pygame.draw.rect(self.screen, color_dark, [width / 2, (height / 2) + 50, 140, 40])
                pygame.draw.rect(self.screen, color_dark, [width / 2, (height / 2) - 50, 140, 40])
                pygame.draw.rect(self.screen, color_dark, [width / 2, (height / 2) - 100, 140, 40])
                pygame.draw.rect(self.screen, color_dark, [width / 2, (height / 2) + 100, 140, 40])

                # superimposing the text onto our button

            self.screen.blit(text1, ((width / 2) + 5, (height / 2) - 100))
            self.screen.blit(text2, ((width / 2) + 5, (height / 2) - 50))
            self.screen.blit(text3, ((width / 2) + 5, (height / 2)))
            self.screen.blit(text4, ((width / 2) + 5, (height / 2) + 50))
            self.screen.blit(text5, ((width / 2) + 5, (height / 2) + 100))

            # updates the frames of the game
            pygame.display.update()



    def run(self, language):
        clock = pygame.time.Clock()
        self.language = language
        self.map_manager = MapManager(self.screen, self.player, self.language)

        # Clock
        while self.running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.map_manager.draw()
            self.dialog_box.render(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.map_manager.check_npc_collision(self.dialog_box)

            clock.tick(60)

        pygame.quit()

    def _initialiser(self):
        try:
            self.ecran.detruire()
            # Suppression de tous les sprites du groupe
            self.groupeGlobal.empty()
        except AttributeError:
            pass