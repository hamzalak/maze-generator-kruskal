#Auteur : LAKHAL Hamza
#Date 03/05/2019
#Ce code permet de tracer une labyrinth en utilisant l'algorithme de Kruskal
# (fusion aléatoire de chemins en français)


# importation du module  qui fait l'union entre les cellule (c'est un Tree)

from disjoint_set import DisjointSet

#outils connus

from random import *
import  random
import pygame
import sys

# La cellule
class Cell:
    def __init__(self,i , j, south , west ):
         self.i = i
         self.j = j
         self.south = True
         self.west = True
    def __str__(self):
          return   str(self.i) +"  "+str(self.j)+str(self.west) +" "+str(self.south)
#Le mur sud

class South :
    def __init__(self, i, j ):
        self.i = i
        self.j = j
# Le mur West
class West :
    def __init__(self, i, j):
        self.i = i
        self.j = j

#La fonction Main
def main() :
    # definition de la longueur et largeur de l'ecran qui seront modifié
    w, h =1, 1;
    while (h < 2 and w < 2):
        print("veuillez entrer la largeur du labyrinth, elle doit pas être inférieur à 1 ")
        w = int(input())
        print("veuillez entrer la longueur du labyrinth, elle doit pas être inférieur à 1")
        h = int(input())
    hScreen , wScreen = 600 , 600

    #Les cellules son des carreaux hCell = wCell

    hCell = (hScreen*2)/(3*h)

    # Logic de remplissage des List
    maze = [[Cell(x,y,True,True) for x in range(w)] for y in range(h)]
    wests = [West(x, y) for x in range(1,h) for y in range(w)]
    souths = [South(x, y) for x in range(h) for y in range(w-1)]
    walls =  wests +souths
    #Mélange aléatoires des murs
    random.shuffle(walls)

    #List qui stock les coordonées des murs qui seront supprimer du labyrinth

    coordonates = []


    #Instantion de l'arbre (voir documentation dans le fichier descriptif)

    ds = DisjointSet()

    #Longic de connexion entre les cellules

    while(len(walls)!=0):
        wall = walls.pop()
        if isinstance(wall,West):
            if not ds.connected(ds.find(maze[wall.i][wall.j]),ds.find(maze[wall.i-1][wall.j])):
                maze[wall.i][wall.j].west = False
                ds.union(ds.find(maze[wall.i][wall.j]), ds.find(maze[wall.i - 1][wall.j]))
        elif isinstance(wall,South):
            if not ds.connected(ds.find(maze[wall.i][wall.j]),ds.find(maze[wall.i][wall.j + 1])):
                maze[wall.i][wall.j].south = False
                ds.union(ds.find(maze[wall.i][wall.j]), ds.find(maze[wall.i][wall.j+1]))

    #Debuggage pour afficher les cellule et leurs murs
    for i in range(h) :
        for l in range(w):
            print(maze[i][l])
    for i in range(h):
        for j in range(w):
            print("south(", maze[i][j].south, ")", "(", maze[i][j].i, maze[i][j].j, ")")
            print("west(", maze[i][j].west, ")", "(", maze[i][j].i, maze[i][j].j, ")")

    # remplissage des murs qui seront supprimer
    for k in range(h):
        for l in range(w):
            m = maze[k][l].i + 2
            n = maze[k][l].j + 2
            if maze[k][l].west == False and maze[k][l].south == True:
                coordonates.append([(n * hCell, m * hCell + hCell),(n * hCell, m * hCell)])
            elif maze[k][l].south == False and maze[k][l].west == True:
                coordonates.append([(n * hCell, m * hCell + hCell), (n * hCell + hCell, m * hCell + hCell)])
            elif maze[k][l].south == False and maze[k][l].west == False:
                coordonates.append([(n * hCell, m * hCell + hCell),(n * hCell, m * hCell)])
                coordonates.append([(n * hCell, m * hCell + hCell), (n * hCell + hCell, m * hCell + hCell)])

    #Initialisation des objets pygame
    pygame.init()
    disp_surf = pygame.display.set_mode((hScreen, wScreen))
    pygame.display.set_caption('Labyrinth')
    disp_surf.fill((255, 255, 255))
    FPS = 24;
    FRAME_DELAY = 10000 // 24;
    i = 0

    # Tracé du labyrinth avec les murs
    for k in range(h):
        for l in range(w):
            empty_rect = pygame.Rect(hCell * (k + 2), hCell * (l + 2), hCell, hCell)
            pygame.draw.rect(disp_surf, (255, 0, 0), empty_rect, 3)

    #Debut de la logic d'affichage

    while True:
        frameStart = pygame.time.get_ticks();
        if (i < len(coordonates)):
            pygame.draw.line(disp_surf, (255, 255, 255), coordonates[i][0], coordonates[i][1], 5)
        for eve in pygame.event.get():
            if eve.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        i = i + 1
        pygame.display.flip();
        frameEnd = pygame.time.get_ticks();

        frameTime = frameEnd - frameStart;

        if FRAME_DELAY - frameTime > 0:
            pygame.time.delay(FRAME_DELAY - frameTime);
        for eve in pygame.event.get():
            if eve.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    main()

