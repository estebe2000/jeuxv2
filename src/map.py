from dataclasses import dataclass
import pygame, pytmx, pyscroll

from src.player import NPC
import xml.etree.ElementTree as ET

import datetime

now = datetime.datetime.now()

@dataclass
class Portal:
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str


@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]
    npcs: list[NPC]
    key2cont: str


class MapManager:

    def __init__(self, screen, player, language):
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.current_map = "story"
        # lancer font sonore
        self.ma_musique_de_fond(self.current_map)
        self.language = language

        self.register_maps()

        self.teleport_player("player")
        self.teleport_npc()

        self.keyok = False

        self.info_key = False
        self.logo = pygame.image.load("../medias/loupe.png")



    def check_npc_collision(self, dialog_box):

        for sprite in self.get_group().sprites():
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC:
                dialog_box.execute(sprite.dialog)
                sprite.talking()
                if sprite.is_name() == self.key2continus:
                    self.keyok = True
                    self.logo = pygame.image.load("../medias/loupe1.png")

                    print("ok", self.key2continus)


    def check_key_collection(self,dialog_box,info=[]):

        for portal in self.get_map().portals:
            if portal.from_world == self.current_map :
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)
                if self.player.feet.colliderect(rect) and not(self.keyok) and not(self.info_key):
                    dialog_box.execute(info)
                    self.info_key = True
                elif self.player.feet.colliderect(rect) and not(self.keyok) and self.info_key:
                    dialog_box.next_text()
                    self.info_key = False

    def check_collisions(self):
        # portails
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map :
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect) and self.keyok:
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)
                    # lancer font sonore
                    self.ma_musique_de_fond(self.current_map)


        # collision
        for sprite in self.get_group().sprites():

            if type(sprite) is NPC:
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = 1

            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

    def teleport_player(self, name):
        if self.get_key() == 'None':
            self.keyok = True
            self.logo = pygame.image.load("../medias/loupe1.png")
        else:
            self.key2continus = self.get_key()
            self.keyok = False
            self.logo = pygame.image.load("../medias/loupe.png")

        print(self.keyok, self.get_key())
        point = self.get_object(name)

        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def register_map(self, name, portals=[], npcs=[]):
        # Charger la carte clasique
        tmx_data = pytmx.util_pygame.load_pygame(f"../maps/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # Les collisions
        walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner les différents calques
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        group.add(self.player)

        # recuperer tous les npcs pour les ajouter au groupe
        for npc in npcs:
            group.add(npc)

        # Creer un objet map
        self.maps[name] = Map(name, walls, group, tmx_data, portals, npcs)

    def register_maps(self):
        doc = ET.parse('../textes/maps.xml')

        # pour toutes les maps dans le xml
        for AAA in doc.findall('map'):
            portals = []
            npcs = []
            nbport = (len(AAA.findall('portal')))
            npnpc = (len(AAA.findall('npc')))
            name = AAA[0].text
            key = AAA[1].text
            # print(f"La map {name} a {nbport} portails et {npnpc} PNJ")

            # Charger la carte
            tmx_data = pytmx.util_pygame.load_pygame(f"../maps/{name}.tmx")
            map_data = pyscroll.data.TiledMapData(tmx_data)
            map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
            map_layer.zoom = 2

            # Les collisions
            walls = []

            for obj in tmx_data.objects:
                if obj.type == "collision":
                    walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

            # Dessiner les différents calques
            group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
            group.add(self.player)

            # ajout des portails
            for port in range(nbport):
                portals.append(Portal(from_world=f'{AAA[2 + port][0].text}', origin_point=f'{AAA[2 + port][1].text}',
                                      target_world=f'{AAA[2 + port][2].text}',
                                      teleport_point=f'{AAA[2 + port][3].text}'))
            # ajout des npcs
            for pnj in range(npnpc):
                new_dial = []
                nom_pnj = AAA[2 + nbport + pnj][0].text
                nbpoint = int(AAA[2 + nbport + pnj][1].text)
                dial_pnj = f"[{AAA[2 + nbport + pnj][2].text}]"
                if dial_pnj != '[None]':
                    txt_dial = str(dial_pnj).split(",")
                    for txt in range(len(txt_dial)):
                        new_dial.append(txt_dial[txt].replace("[", "").replace("]", "").replace("'", ""))

                npcs.append(NPC(nom_pnj, nb_points=nbpoint, dialog=new_dial, lang=(self.get_language())))

            # recuperer tous les npcs pour les ajouter au groupe
            for npc in npcs:
                group.add(npc)

            # Creer un objet map
            self.maps[name] = Map(name, walls, group, tmx_data, portals, npcs, key)

    def get_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_map().group

    def get_key(self):
        return str(self.get_map().key2cont)

    def get_walls(self):
        return self.get_map().walls

    def get_language(self):
        return self.language

    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    def teleport_npc(self):
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs

            for npc in npcs:
                npc.load_points(map_data.tmx_data)
                npc.teleport_spawn()

    def draw(self):
        self.get_group().draw(self.screen)
        myfont = pygame.font.Font("../dialogs/dialog_font.ttf", 18)
        now2 = datetime.datetime.now()
        dif = str(now2 - now)
        nowstr = now2.strftime("%Y-%m-%d %H:%M:%S")
        date = myfont.render(nowstr, 1, (255, 255, 0))
        self.screen.blit(date, (10, 10))
        score_display = myfont.render(dif, 1, (255, 255, 0))
        self.screen.blit(score_display, (10, 40))
        key = self.get_key()
        self.screen.blit(self.logo, (720, 10))


        self.get_group().center(self.player.rect.center)

    def ma_musique_de_fond(self, choix_musique):
        # definir la musique
        pygame.mixer.init()
        file = '../sounds/' + choix_musique + '.wav'
        pygame.mixer.music.load(file)
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)  # If the loops is -1 then the music will repeat indefinitely.

    def update(self):

        self.get_group().update()
        self.check_collisions()

        for npc in self.get_map().npcs:
            npc.move()
