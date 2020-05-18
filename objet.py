from math import *
import sys, os



def prod_scal(u,v):
    return sum([x * y for x, y in zip(u, v)])

def norm(u):
    return sqrt(prod_scal(u,u))


class Polygon():
    def __init__(self, x, y, radius, n, tilt, color, width, vx, vy, w):
        self.x = x
        self.y = y
        self.radius = radius
        self.n = n #num_sides
        self.tilt = tilt
        self.color = color
        self.width = width
        self.edges = list()
        
        s = 1
        self.speed = s 
        self.v = [vx*s,vy*s,0] #speed
        self.w = [0,0,w*s] #rotation

    def deplacement(self):
        self.x += self.v[0]
        self.y += self.v[1]
        self.tilt = (self.tilt + self.w[2])%(2*pi)
  

def se_rapproche(p, p2, temps):
    #si les balles s'éloignent ne pas faire de collision 
    pass
    """
    posx = p.position_X
    posy = p.position_Y
    posx2 = p2.position_X
    posy2 = p2.position_Y

    nposx = posx + cos(p.direction)*p.vitesse*temps * m
    nposy = posy - sin(p.direction)*p.vitesse*temps* m
    nposx2 = posx2 + cos(p2.direction)*p2.vitesse*temps * m
    nposy2 = posy2 - sin(p2.direction)*p2.vitesse*temps* m
    dist = norm((posx - posx2, posy - posy2))
    ndist = norm((nposx - nposx2, nposy - nposy2))

    return ndist < dist
    """

###________________Collisions balles___________________:
def between(a,b,c): #return True si a est entre b et c
    return (a>=min(b,c) and a<=max(b,c))

def point_colli(surface, pygame, p, p2): 
    list_colli = list()
    
    #________________trouver l'intersection précise_____________
    e = p.edges
    e2 = p2.edges
    ed = e
    ed2 = e2
    for i in range(p.n):#pour chaque angle i du poly
        j = (i+1)%(p.n) #j angle suivant
        #pygame.draw.line(surface, (250, 0, 200), e[i], e[j], 5)#à_suppr
        #pygame.display.flip()#à_suppr
        #équation de l'arête de p:
        M = e[i][1] - e[j][1]# [1] -> y
        N = e[j][0] - e[i][0]# [0] -> x
        Q = -M*e[j][0] - N*e[j][1] #Mx+Ny+Q == 0

        #équation des arêtes de p2:
        for k in range(p2.n):#pour chaque angle k du poly
            l = (k+1)%(p2.n) #l angle suivant
            #pygame.draw.line(surface, (250, 200, 0), e2[k], e2[l], 5)#à_suppr
            #pygame.display.flip()#à_suppr
            #équation de l'arête de p2:
            A = e2[k][1] - e2[l][1]# [1] -> y
            B = e2[l][0] - e2[k][0]# [0] -> x
            C = -A*e2[k][0] - B*e2[k][1] #Ax+By+C == 0
            
            if A*N - B*M == 0 and B*Q - C*N == 0: #parallèle
                print("//")
                #on regarde maintenant si les polygones se touchent:
                if between(ed2[k][0], ed[i][0], ed[j][0]) and between(ed2[k][1], ed[i][1], ed[j][1]):
                    list_colli.append(ed2[k])
                if between(ed2[l][0], ed[i][0], ed[j][0]) and between(ed2[l][1], ed[i][1], ed[j][1]):
                    list_colli.append(ed2[l])
                if between(ed[i][0], ed[k][0], ed2[l][0]) and between(ed[i][1], ed[k][1], ed[l][1]):
                    list_colli.append(ed[i])
                if between(ed[j][0], ed[k][0], ed2[l][0]) and between(ed[j][1], ed[k][1], ed[l][1]):
                    list_colli.append(ed[j])
            
            elif A*N - B*M != 0:
                #intersection en X, Y
                X = (B*Q - C*N) / (A*N - B*M)
                Y = (A*Q - M*C) / (M*B - A*N)
                
                #pygame.draw.rect(surface, (255,150,150), [X-3,Y-3,6,6], 5)#à_suppr
                #pygame.display.flip()#à_suppr
                #print(X, ed[i][0], ed[j][0], ed2[k][0],ed2[l][0])
                #print(Y, ed[i][1], ed[j][1], ed2[k][1],ed2[l][1])
                #input()
                #on vérifie que l'intersection est dans les arêtes
                #pygame.draw.rect(surface, (0,0,0), [X-3,Y-3,6,6], 5)#à_suppr
                #pygame.display.flip()#à_suppr
                if between(X, ed[i][0], ed[j][0]) and between(X, ed2[k][0], ed2[l][0]) and between(Y, ed[i][1], ed[j][1]) and between(Y, ed2[k][1], ed2[l][1]):
                    list_colli.append([X,Y])
        
            
            #pygame.draw.line(surface, p2.color, e2[k], e2[l], 5)#à_suppr
        #pygame.draw.line(surface, p.color, e[i], e[j], 5)#à_suppr

    if list_colli != []: #les collisions existent
        for pos in list_colli:
            pos[0]-=3
            pos[1]-=3
            if len(pos) < 4:
                pos.append(6) #add dimension
                pos.append(6) #add dimension
            pygame.draw.rect(surface, (255,50,50), pos, 10)
            pygame.display.flip()
            #print("collisions !")

    return list_colli

def collision(surface, pygame, p, p2):
    pts_colli = point_colli(surface, pygame, p,p2)
    if pts_colli == []:
        return
    


def draw_regular_polygon(surface, pygame, list_poly): #color, n ,tilt_angle, x, y, radius, width)
    for p in list_poly:
        n = p.n #num_sides
        x = p.x
        y = p.y
        r = p.radius
        pts_poly = list()
        for k in range(n):
            pts_poly.append([x + r*cos(2*pi*k/n+p.tilt), y + r*sin(2*pi*k/n+p.tilt)])
        pygame.draw.polygon(surface, p.color, pts_poly, p.width)
        pygame.draw.line(surface, p.color, [x,y], pts_poly[0],1)
        p.edges = pts_poly
