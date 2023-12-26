import pygame
import random
import sys

# Initialisation de Pygame
pygame.init()

# Paramètres du jeu
largeur_ecran = 800
hauteur_ecran = 400
fps = 60
clock = pygame.time.Clock()

# Couleurs
blanc = (255, 255, 255)
noir = (0, 0, 0)
bleu = (0, 0, 255)

# Redimensionnement des images
personnage_image = pygame.transform.scale(pygame.image.load('typinggame/vaisseau.png'), (50, 50))
passerelle_image = pygame.transform.scale(pygame.image.load('typinggame/passerelle.png'), (200, 20))
obstacle_image = pygame.transform.scale(pygame.image.load('typinggame/astéroide.png'), (50, 50))

# Classe pour le personnage
class Personnage(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = personnage_image
        self.rect = self.image.get_rect()
        self.rect.center = (100, hauteur_ecran // 2)
        self.vitesse_y = 0
        self.vitesse_x = 0  # Vitesse horizontale initiale
        self.peut_sauter = False  # Nouvelle variable pour autoriser le saut

    def sauter(self):
        if self.peut_sauter:  # Vérifier si le saut est autorisé
            self.vitesse_y = -15
            self.peut_sauter = False  # Désactiver le saut après le premier saut

    def update(self):
        self.vitesse_y += 1
        self.rect.y += self.vitesse_y
        if self.rect.bottom > hauteur_ecran:
            self.rect.bottom = hauteur_ecran

        # Déplacement horizontal
        self.rect.x += self.vitesse_x
        if self.rect.right > largeur_ecran:
            self.rect.left = 0

        if self.rect.left < 0:
            self.rect.right = largeur_ecran

    def deplacer(self, x):
        self.vitesse_x = x

# Classe pour les passerelles
class Passerelle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = passerelle_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        pass  # Les passerelles restent fixes, donc pas besoin de mise à jour

# Classe pour les obstacles
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = obstacle_image
        self.rect = self.image.get_rect()
        self.rect.center = (largeur_ecran + 20, hauteur_ecran // 2)

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.rect.left = largeur_ecran + 20
            self.rect.centery = random.randint(50, hauteur_ecran - 50)

# Classe pour la gestion des mots
class GestionMots:
    def __init__(self):
        self.mots = ["espace", "voyage", "vaisseau", "étoiles", "galaxie", "astronaute", "exploration"]
        self.mot_courant = random.choice(self.mots)
        self.mot_entre = ""

    def nouveau_mot(self):
        self.mot_courant = random.choice(self.mots)
        self.mot_entre = ""

# Initialisation de la gestion des mots
gestion_mots = GestionMots()

# Groupes de sprites
tous_les_sprites = pygame.sprite.Group()
passerelles = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
personnage = Personnage()
tous_les_sprites.add(personnage)

# Ajout des passerelles fixes
passerelle1 = Passerelle(100, 300)
passerelle2 = Passerelle(400, 200)
passerelle3 = Passerelle(600, 100)
passerelles.add(passerelle1, passerelle2, passerelle3)
tous_les_sprites.add(passerelle1, passerelle2, passerelle3)

# Police de caractères pour l'affichage des mots
font = pygame.font.Font(None, 36)

# Création de la fenêtre
fenetre = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
pygame.display.set_caption("Typing Game")

# Affichage du menu d'accueil
def afficher_menu():
    fenetre.fill(noir)
    texte_titre = font.render("Voyage Spatial", True, blanc)
    texte_instructions = font.render("Appuyez sur ESPACE pour sauter", True, blanc)
    texte_commencer = font.render("Appuyez sur ENTREE pour commencer", True, bleu)
    fenetre.blit(texte_titre, (largeur_ecran // 2 - 150, hauteur_ecran // 2 - 50))
    fenetre.blit(texte_instructions, (largeur_ecran // 2 - 200, hauteur_ecran // 2))
    fenetre.blit(texte_commencer, (largeur_ecran // 2 - 300, hauteur_ecran // 2 + 50))
    pygame.display.flip()

afficher_menu()

# Boucle de jeu
jeu_en_cours = False
victoire = False
defaite = False
score = 0

while not jeu_en_cours:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                jeu_en_cours = True

# Boucle principale
while jeu_en_cours:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jeu_en_cours = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                personnage.sauter()
            elif event.key == pygame.K_BACKSPACE:
                gestion_mots.mot_entre = gestion_mots.mot_entre[:-1]
            elif event.key == pygame.K_RETURN:
                if gestion_mots.mot_entre == gestion_mots.mot_courant:
                    score += 1
                    gestion_mots.nouveau_mot()
                else:
                    defaite = True
            elif event.key == pygame.K_LEFT:
                personnage.deplacer(-5)  # Déplacement vers la gauche
            elif event.key == pygame.K_RIGHT:
                personnage.deplacer(5)  # Déplacement vers la droite

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                personnage.deplacer(0)  # Arrêter le déplacement horizontal

    # Mise à jour
    tous_les_sprites.update()

    # Gestion des collisions
    collisions_passerelle = pygame.sprite.spritecollide(personnage, passerelles, False)
    if collisions_passerelle:
        personnage.peut_sauter = True  # Activer la possibilité de sauter sur la passerelle
        score += 1

    collisions_obstacle = pygame.sprite.spritecollide(personnage, obstacles, False)
    if collisions_obstacle:
        defaite = True

    # Génération aléatoire des obstacles
    if random.randint(0, 100) < 5:
        obstacle = Obstacle()
        obstacles.add(obstacle)
        tous_les_sprites.add(obstacle)

    # Suppression des obstacles hors de l'écran
    for obstacle in obstacles:
        if obstacle.rect.right < 0:
            obstacle.kill()

    # Affichage du fond
    fenetre.fill(noir)

    # Affichage des sprites
    tous_les_sprites.draw(fenetre)

    # Affichage du mot à saisir
    texte_mot = font.render(gestion_mots.mot_courant, True, blanc)
    fenetre.blit(texte_mot, (largeur_ecran // 2 - 50, 10))

    # Affichage de la saisie du joueur
    texte_saisie = font.render(gestion_mots.mot_entre, True, blanc)
    fenetre.blit(texte_saisie, (largeur_ecran // 2 - 50, hauteur_ecran - 40))

    # Rafraîchissement de l'écran
    pygame.display.flip()

    # Contrôle des FPS
    clock.tick(fps)

    # Gestion de la défaite
    if defaite:
        jeu_en_cours = False

# Écran de défaite
while defaite:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            defaite = False

    fenetre.fill(noir)
    texte_defaite = font.render("Défaite !", True, blanc)
    texte_score = font.render("Score: {}".format(score), True, blanc)
    fenetre.blit(texte_defaite, (largeur_ecran // 2 - 70, hauteur_ecran // 2 - 50))
    fenetre.blit(texte_score, (largeur_ecran // 2 - 60, hauteur_ecran // 2))
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
sys.exit()
