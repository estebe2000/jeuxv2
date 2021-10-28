
import pygame

from player import Player
from src.dialog import DialogBox
from src.map import MapManager
from src.fx_rain import *
from src.fx_fire import *
import platform



class Game:

    def __init__(self):
        self.running = True
        # Affichage de la fenêtre
        self.screen = pygame.display.set_mode((800, 600))

        pygame.display.set_caption("Menu- Jeux")


        self.groupeGlobal = pygame.sprite.Group()

        # Générer le joeur
        self.player = Player()
        self.dialog_box = DialogBox()

        # Définir le logo du jeu
        pygame.display.set_icon(self.player.image)

        # menu
        self.items = []

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

        texts, langs = [], []
        with open(f"../textes/menu.txt", "r") as f:
            for line in f:
                line = line.replace('"', '').strip()
                self.items.append([line.split()[0], line.split()[1]])
                # list languages
                texts.append(smallfont.render(line.split()[0], True, color))
                langs.append(line.split()[1])

        # Visual menu
        image_fond = pygame.image.load("../medias/fond.png")
        logo_fond = pygame.image.load("../medias/logo.png")
        logo_fond = pygame.transform.scale(logo_fond, (width, height // 5))

        self.screen.blit(image_fond, (0, 0))
        self.screen.blit(logo_fond, (0, 0))

        while True:
            self.screen.blit(image_fond, (0, 0))
            self.screen.blit(logo_fond, (0, 0))

            Particle_fire(640, 430, res=2, screen=self.screen).show_particle()
            Particle_rain( y=0, vit=5, screen=self.screen).show_particle()

            for ev in pygame.event.get():

                if ev.type == pygame.QUIT:
                    pygame.quit()

                    # checks if a mouse is clicked
                if ev.type == pygame.MOUSEBUTTONDOWN:

                    # if the mouse is clicked on the
                    for i in range(len(self.items)):

                        if width / 2 - 70 <= mouse[0] <= width / 2 + 70 and (height / 2) + 100 <= mouse[
                            1] <= height / 2 + 160:
                            pygame.quit()
                        elif width / 2 - 70 <= mouse[0] <= width / 2 + 70 and (height / 2) - 100 + i * 50 <= mouse[
                            1] <= height / 2 - 60 + i * 50:
                            self.language = langs[i]
                            self.run(self.language)


            mouse = pygame.mouse.get_pos()

            # if mouse is hovered on a button it
            # changes to lighter shade
            for i in range(len(self.items)):
                if width / 2 - 70 <= mouse[0] <= width / 2 + 70 and (height / 2) - 100 + i * 50 <= mouse[
                    1] <= height / 2 - 60 + i * 50:
                    pygame.draw.rect(self.screen, color_light, [width / 2 - 70, (height / 2) - 100 + i * 50, 140, 40])
                else:
                    pygame.draw.rect(self.screen, color_dark, [width / 2 - 70, (height / 2) - 100 + i * 50, 140, 40])
                # superimposing the text onto our button
                self.screen.blit(texts[i], ((width / 2) - 65, (height / 2) - 90 + i * 50))
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
            caption = 'NSI JEUX -FPS: {} - Python {}  Pygame {} - Language {} '.format(int(clock.get_fps()),platform.python_version(),pygame.version.ver,self.language)
            pygame.display.set_caption(caption)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.map_manager.check_npc_collision(self.dialog_box)
                        self.map_manager.check_key_collection(self.dialog_box,["trop tot"])
            clock.tick(60)

        pygame.quit()

    def _initialiser(self):
        try:
            self.ecran.detruire()
            # Suppression de tous les sprites du groupe
            self.groupeGlobal.empty()
        except AttributeError:
            pass
