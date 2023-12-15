# Importer les modules nécessaires
import pygame
from pygame import mixer
import os

# Initialiser Pygame est nécessaire pour utiliser les fonctionnalités de Pygame
pygame.init()

# Initialiser le mixer est nécessaire pour utiliser les fonctionnalités audio de Pygame
mixer.init()

# Crée une fenêtre de 600 pixels de large et 400 pixels de haut
fenetre = pygame.display.set_mode((600, 400))

# Charger les icônes
# Les icônes sont des images que nous utiliserons comme boutons dans notre interface
icone_pause = pygame.image.load('icon_pause.png')
icone_suivant = pygame.image.load('icon_suivant.png')
icone_volume_plus = pygame.image.load('icon_volume_plus.png')
icone_volume_moins = pygame.image.load('icon_volume_moins.png')

# Redimensionner les icônes pour qu'elles aient toutes la même taille
largeur_icone = 50
hauteur_icone = 50
icone_pause = pygame.transform.scale(icone_pause, (largeur_icone, hauteur_icone))
icone_suivant = pygame.transform.scale(icone_suivant, (largeur_icone, hauteur_icone))
icone_volume_plus = pygame.transform.scale(icone_volume_plus, (largeur_icone, hauteur_icone))
icone_volume_moins = pygame.transform.scale(icone_volume_moins, (largeur_icone, hauteur_icone))

# Liste des fichiers audio
# Ces sont les pistes que notre lecteur de musique sera capable de jouer
pistes = ['bells.mp3', 'bells2.mp3', 'bells3.mp3']
index_piste = 0 # Nous commençons par la première piste de la liste

# Liste des images qui seront affichées à l'écran pendant que la musique correspondante est jouée
images = ['image1.png', 'image2.png', 'image3.png']

# Charger un fichier audio
# Nous utilisons le module os pour obtenir le chemin absolu du fichier audio
chemin_absolu = os.path.abspath(pistes[index_piste])
mixer.music.load(chemin_absolu) # Charger le fichier audio dans le mixer

# Charger l'image correspondante à la piste audio
image = pygame.image.load(images[index_piste])

# Jouer le fichier audio
mixer.music.play()

# Boucle principale
# Cette boucle s'exécute tant que le programme est en cours d'exécution
continuer = True
while continuer:
    # Dessiner l'image sur la fenêtre
    fenetre.blit(image, (0, 0)) # Dessiner l'image à la position (0, 0)
    
    # Dessiner les icônes sur la fenêtre
    espace = 10  # Espacement de 10 pixels entre les icônes
    marge_bas = fenetre.get_height() // 2 - hauteur_icone // 2  # Centrer verticalement
    debut = fenetre.get_width() // 2 - (4 * largeur_icone + 3 * espace) // 2  # Centrer horizontalement
    fenetre.blit(icone_pause, (debut, marge_bas))
    fenetre.blit(icone_suivant, (debut + espace + largeur_icone, marge_bas))
    fenetre.blit(icone_volume_plus, (debut + 2*espace + 2*largeur_icone, marge_bas))
    fenetre.blit(icone_volume_moins, (debut + 3*espace + 3*largeur_icone, marge_bas))
    
    for event in pygame.event.get(): # Parcourir tous les événements qui se sont produits
        if event.type == pygame.QUIT: # Si l'utilisateur a cliqué sur le bouton de fermeture de la fenêtre
            continuer = False # Arrêter la boucle
        elif event.type == pygame.MOUSEBUTTONDOWN: # Si l'utilisateur a cliqué avec la souris
            x, y = pygame.mouse.get_pos() # Obtenir la position de la souris
            # Vérifier si l'utilisateur a cliqué sur une icône
            if debut <= x <= debut + largeur_icone and marge_bas <= y <= marge_bas + hauteur_icone:
                # Mettre en pause ou reprendre la lecture
                if mixer.music.get_busy(): # Si la musique est en cours de lecture
                    mixer.music.pause() # Mettre la musique en pause
                else:
                    mixer.music.unpause() # Reprendre la lecture de la musique
            elif debut + espace + largeur_icone <= x <= debut + 2*espace + 2*largeur_icone and marge_bas <= y <= marge_bas + hauteur_icone:
                # Passer à la chanson suivante
                index_piste = (index_piste + 1) % len(pistes) # Passer à la piste suivante dans la liste
                chemin_absolu = os.path.abspath(pistes[index_piste]) # Obtenir le chemin absolu de la nouvelle piste
                mixer.music.load(chemin_absolu) # Charger la nouvelle piste dans le mixer
                mixer.music.play() # Commencer à jouer la nouvelle piste
                image = pygame.image.load(images[index_piste]) # Charger l'image correspondante à la nouvelle piste
            elif debut + 2*espace + 2*largeur_icone <= x <= debut + 3*espace + 3*largeur_icone and marge_bas <= y <= marge_bas + hauteur_icone:
                # Augmenter le volume
                volume = min(1, mixer.music.get_volume() + 0.1) # Augmenter le volume de 10%, mais ne pas dépasser 100%
                mixer.music.set_volume(volume) # Appliquer le nouveau volume
            elif debut + 3*espace + 3*largeur_icone <= x <= debut + 4*espace + 4*largeur_icone and marge_bas <= y <= marge_bas + hauteur_icone:
                # Diminuer le volume
                volume = max(0, mixer.music.get_volume() - 0.1) # Diminuer le volume de 10%, mais ne pas descendre en dessous de 0%
                mixer.music.set_volume(volume) # Appliquer le nouveau volume

    # Mettre à jour l'affichage pour montrer les nouvelles images
    pygame.display.flip()
    
# Quitter Pygame (nécessaire pour arrêter correctement Pygame)
pygame.quit()