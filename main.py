#main.py
"""
à rajouter:

"""

import pygame               #bibliothèque pour le 2d
from pygame.locals import *
from random import randint  #pour poper la poly aléatoirement
from math import *

pygame.init()

from objet import *

import sys, os


clock = pygame.time.Clock() #initialise une horloge pour gerer le temps et les fps

#_________________variables_________________:
quitter = False	#pour sortir du jeu
fps = 32 	#modifier le nombre de frame per seconde. Permet d'être plus précis, moins de tremblement, plus stable mais plus lent lorsqu'on l'augmente
surfaceX = 1830	#taille en pixels de la fenêtre
surfaceY = 1000
tailleFenetre = (surfaceX,surfaceY)


#init objets
list_poly = list()	#liste des polys


#Creation de la surface:
surface = pygame.display.set_mode(tailleFenetre)#on crée notre fenêtre


pygame.event.pump()#pour ne pas avoir de "ne répond plus"

surface_fond = pygame.display.get_surface().copy() #Copy du fond pour effacer la poly

#________________main________________:

while quitter == False:
    list_poly = list()
    list_poly.append(Polygon(400,300, 100, 5, pi/2, (0,255,0), 4, 1,1/2,pi/200)) #x,y,radius, n, tilt, color, width, wx, wy, w
    list_poly.append(Polygon(1000, 600, 50, 4, 0, (120,120,255), 4, -1,-1/4,pi/400))
    list_poly.append(Polygon(800, 800, 70, 3, 0, (155,155,155), 4, 1/4,-2,pi/400))
    list_poly.append(Polygon(900, 300, 700, 2, 2*pi/3, (155,200,100), 4, 0,0, 0))
    
    draw_regular_polygon(surface, pygame, list_poly)
    pygame.display.flip()#on rafraichit la fenêtre pour afficher les images qui étaient dans le buffer
    replay = False #pour recommencer


    while quitter == False and replay == False: #boucle de jeu, on sort pour recommencer ou quitter
        for event in pygame.event.get():    #on parcourt tous les évènements pygame (souris, clavier etc) pour savoir si on est intervenu
            if event.type == pygame.QUIT:   #si on clique sur la croix ça quitte
                quitter = True

    
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE: #recommencer
                    replay = True
            
        num = 1
        longueur = len(list_poly)
        for p in list_poly: #pour chaque poly
            p.deplacement() #on la déplace
            try:
                #Collision
                for num_poly in range(num, longueur):#on teste chaque couple qu'une fois
                    #on regarde d'habord si on est dans le rayon du pylogone, avant de faire un algo coûteux pour trouver les collisions.
                    if (p.x - list_poly[num_poly].x)**2 + (p.y - list_poly[num_poly].y)**2 < (p.radius + list_poly[num_poly].radius)**2:#si les polys sont assez proches
                        collision(surface, pygame, p, list_poly[num_poly]) #collision entre 2 polys
                num += 1
            
            except SyntaxError:#le poly sort de l'écran, ne fonctionne qu'à droite et en bas à  cause des indices négatifs dans les listes, faudra le changer
                print("index error")
                """
                posx = poly.position_X
                posy = poly.position_Y
                if posx < poly.taille or posx > surfaceX - poly.taille or posy < poly.taille or posy > surfaceY - poly.taille:#on supprime la poly si elle est sortie de l'écran (condition non utile)
                    list_poly.remove(poly)

                if list_poly == []: #si plus de poly on recommence
                    replay = True
                """
        #____________________________
        surface.blit(surface_fond, (0,0))   #on affiche le fond
        draw_regular_polygon(surface, pygame, list_poly)
        pygame.display.flip()   #on rafraîchit
        clock.tick(fps)         #on modère les fps
        #ça serait peut-être plus interessant de ne pas limiter les fps et de calculer la vitesse de la poly. On serait ainsi plus précis avec peu de polys et on pourrait avoir plus de polys. Seul problème, le processeur risque de ne pas aimer.

pygame.quit()   #on quitte pygame pour sortir proprement

