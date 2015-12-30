# script pion.py hjyf
from Tkinter import *
import numpy
import numpy as np

def initialize():
    global PosX,PosY,cost, globalcost
# position initiale du robot
    PosX = 20+10*zoom
    PosY = 20+10*zoom
    for k in range(5):
        cost[k]=0
# cout et affichage
    Canevas.coords(Pion,PosX -9*zoom, PosY -9*zoom, PosX +9*zoom, PosY +9*zoom)
    w.config(text='Cost = '+ str(globalcost))

def colordraw(g,nblignes,nbcolonnes):
    pmur=0.15 #0.15
    pblanc=0.55 #0.55
    pverte=0.1
    pbleue=0.1
    prouge=0.1
    pnoire=0.1
    for i in range(nblignes):
        for j in range(nbcolonnes):
            z=np.random.uniform(0,1)
            if z < pmur:
                c=-1
            else:
                if z < pmur+ pblanc:
                    c=0
                else:    
                    if z < pmur+ pblanc + pverte:
                        c=1
                    else:
                        if z < pmur+ pblanc +pverte + pbleue:
                            c=2
                        else:
                            if z< pmur + pblanc + pverte + pbleue +prouge:
                                c=3
                            else:
                                c=4   
            g[i,j]=c
    g[0,0]=0
    g[0,1]=0
    g[2,0]=0    
    g[nblignes-1,nbcolonnes-1]=0
    g[nblignes-2,nbcolonnes-1]=0
    g[nblignes-1,nbcolonnes-2]=0
    for i in range(nblignes):
        for j in range(nbcolonnes):          
            y =zoom*20*i+20
            x =zoom*20*j+20
            if g[i,j]>0:            
                Canevas.create_oval(x+zoom*(10-3),y+zoom*(10-3),x+zoom*(10+3),y+zoom*(10+3),width=1,outline=color[g[i,j]],fill=color[g[i,j]])
            else:
                if g[i,j]<0:
                    Canevas.create_rectangle(x, y, x+zoom*20, y+zoom*20, fill=myblack)
                    Canevas.create_rectangle(x, y, x+zoom*20, y+zoom*20, fill=myblack)
  
def Clavier(event):
    global PosX,PosY,cost,g, globalcost
    touche = event.keysym
    cj=(PosX-30)/(20*zoom)
    li=(PosY-30)/(20*zoom)
    changed=0
    # deplacement aleatoire en appuyant sur space
    if touche == 'space':
        t=np.random.randint(6)
        lettre = ['f','g','h','j','y','u',]
        touche=lettre[t]
    # deplacement (-2,1)
    if touche == 'y' and li>1 and cj < nbcolonnes-1 and g[li-2,cj+1]>-1:
        PosY -= zoom*20*2
        PosX += zoom*20 
        cost[g[li-2,cj+1]]+=1 
        changed=1
    # deplacement (-2,-1)
    if touche == 't' and li>1 and cj > 0 and g[li-2,cj-1]>-1:
        PosY -= zoom*20*2       
        PosX -= zoom*20                 
        cost[g[li-2,cj-1]]+=1
        changed=1
   # deplacement (-1,2)
    if touche == 'u' and li>0 and cj < nbcolonnes-2 and g[li-1,cj+2]>-1:
        PosY -= zoom*20        
        PosX += zoom*20*2       
        cost[g[li-1,cj+2]]+=1
        changed=1
    # deplacement (-1,-2)
    if touche == 'r' and li>0 and cj >1 and g[li-1,cj-2]>-1:
        PosY -= zoom*20
        PosX -= zoom*20*2           
        cost[g[li-1,cj-2]]+=1
        changed=1
     # deplacement (2,1)  
    if touche == 'h' and li<nblignes-2 and cj < nbcolonnes-1 and g[li+2,cj+1]>-1:
        PosY += zoom*20*2
        PosX += zoom*20 
        cost[g[li+2,cj+1]]+=1
        changed=1
    # deplacement (2,-1)
    if touche == 'g' and li<nblignes-2 and cj > 0 and g[li+2,cj-1]>-1:
        PosY += zoom*20*2       
        PosX -= zoom*20                 
        cost[g[li+2,cj-1]]+=1
        changed=1
   # deplacement (1,2)
    if touche == 'j' and li<nblignes-1 and cj < nbcolonnes-2 and g[li+1,cj+2]>-1:
        PosY += zoom*20        
        PosX += zoom*20*2       
        cost[g[li+1,cj+2]]+=1
        changed=1
    # deplacement (1,-2)
    if touche == 'f' and li<nblignes-1 and cj >1 and g[li+1,cj-2]>-1:
        PosY += zoom*20
        PosX -= zoom*20*2           
        cost[g[li+1,cj-2]]+=1 
        changed=1


# La variable alea =1 si on veut des effets aleatoires sinon les transitions sont deterministes
    #On ajoute un effet aleatoire dans les transitions
    if alea==1 and changed==1:
        t=np.random.uniform(0,1)    
        if t>0.5:
            d=np.random.randint(8)
            dli=0
            if d== 0 or d==1 or d==2:
                dli=-1
            if d== 4 or d==5 or d==6:
                dli==1
            dcj=0
            if d==0 or d==7 or d==6:
                dcj=-1
            if d==2 or d==3 or d==4:
                dcj=1    
        # l'effet aleatoire est applique s'il cree un deplacement sur une case admissible     
            NewPosY = PosY+zoom*20*dli
            NewPosX = PosX+zoom*20*dcj        
            newcj=(NewPosX-30)/(20*zoom)
            newli=(NewPosY-30)/(20*zoom)
            print('d',dli,dcj)
            if newli>=0 and newcj>=0 and newli<=nblignes-1 and newcj<=nbcolonnes-1 and g[newli,newcj]>-1:
                PosY=NewPosY
                PosX=NewPosX            
            
# on dessine le pion a sa nouvelle position
    Canevas.coords(Pion,PosX -9*zoom, PosY -9*zoom, PosX +9*zoom, PosY +9*zoom)       
    globalcost=0    
    for k in range(5):
        globalcost+=cost[k]*weight[k]
    w.config(text='Cost = '+ str(globalcost))

def trouverVoisins(g, x, y):
    voisins = []
    # Coin en haut a gauche
    if x == 0 and y == 0:
        #J
        if g[1, 2] > -1:
            voisins.append([1, 2])
        #H
        if g[2, 1] > -1:
            voisins.append([2, 1])

    # Coin en haut a droite
    elif x == 0 and y == g.shape[1] - 1:
        #F
        if g[1, g.shape[1] - 3] > -1:
            voisins.append([1, g.shape[1] - 3])
        #G
        if g[2, g.shape[1] - 2] > -1:
            voisins.append([2, g.shape[1] - 2])

    # Coin en bas a gauche
    elif x == g.shape[0] - 1 and y == 0:
        #Y
        if g[g.shape[0] - 3, 1] > -1:
            voisins.append([g.shape[0] - 3, 1])
        #U
        if g[g.shape[0] - 2, 2] > -1:
            voisins.append([g.shape[0] - 2, 2])

    # Coin en bas a droite -> Case finale donc pas vraiment de voisins ?
    # elif x == g.shape[0] - 1 and y == g.shape[1] - 1:
    #     if(g[, g.shape[1] - 3] > -1):
    #         voisins.append(g[1, g.shape[1] - 3])
    #     if(g[1, g.shape[1] - 3] > -1):
    #         voisins.append(g[1, g.shape[1] - 3])

    # Toutes les autres cases
    else:
        #R
        if g[x-1, y-2] > -1:
            voisins.append([x-1, y-2])
        #T
        if g[x-2, y-1] > -1:
            voisins.append([x-2, y-1])
        #Y
        if g[x-2, y+1] > -1:
            voisins.append([x-2, y-1])
        #U
        if g[x-1, y+2] > -1:
            voisins.append([x-1, y+2])
        #J
        if g[x+1, y+2] > -1:
            voisins.append([x+1, y+2])
        #H
        if g[x+2, y+1] > -1:
            voisins.append([x+2, y+1])
        #G
        if g[x+2, y-1] > -1:
            voisins.append([x+2, y-1])
        #F
        if g[x+1, y-2] > -1:
            voisins.append([x+1, y-2])
    return voisins

def trouverAdjacents(g, x, y):
    nombreAdjacents = 0
    adjacents = []
    # Coin en haut a gauche
    if x == 0 and y == 0:
        if g[0, 1] > -1:
            nombreAdjacents += 1
            adjacents.append([0, 1])
        if g[1, 1] > -1:
            nombreAdjacents += 1
            adjacents.append([1, 1])
        if g[1, 0] > -1:
            nombreAdjacents += 1
            adjacents.append([1, 0])
    # Coin en haut a droite
    elif x == 0 and y == g.shape[1] - 1:
        if g[0, g.shape[1] - 2] > -1:
            nombreAdjacents += 1
            adjacents.append([0, g.shape[1] - 2])
        if g[1, g.shape[1] - 2] > -1:
            nombreAdjacents += 1
            adjacents.append([1, g.shape[1] - 2])
        if g[1, g.shape[1] - 1] > -1:
            nombreAdjacents += 1
            adjacents.append([1, g.shape[1] - 1])

    # Coin en bas a gauche
    elif x == g.shape[0] - 1 and y == 0:
        if g[g.shape[0] - 2, 0] > -1:
            nombreAdjacents += 1
            adjacents.append([g.shape[0] - 2, 0])
        if g[g.shape[0] - 2, 1] > -1:
            nombreAdjacents += 1
            adjacents.append([g.shape[0] - 2, 1])
        if g[g.shape[0] - 1, 1] > -1:
            nombreAdjacents += 1
            adjacents.append([g.shape[0] - 1, 1])

    # Toutes les autres cases
    else:
        nombreAdjacents = 8
        if g[x-1, y-1] > -1:
            nombreAdjacents += 1
            adjacents.append([x-1, y-1])
        if g[x-1, y] > -1:
            nombreAdjacents += 1
            adjacents.append([x-1, y])
        if g[x-1, y+1] > -1:
            nombreAdjacents += 1
            adjacents.append([x-1, y+1])
        if g[x, y-1] > -1:
            nombreAdjacents += 1
            adjacents.append([x, y-1])
        if g[x, y+1] > -1:
            nombreAdjacents += 1
            adjacents.append([x, y+1])
        if g[x+1, y-1] > -1:
            nombreAdjacents += 1
            adjacents.append([x+1, y-1])
        if g[x+1, y] > -1:
            nombreAdjacents += 1
            adjacents.append([x+1, y])
        if g[x+1, y+1] > -1:
            nombreAdjacents += 1
            adjacents.append([x+1, y+1])

    return [nombreAdjacents, adjacents]


def bellman(g, x, y, poids, gamma):
    maximum = - 999
    voisins = trouverVoisins(g, x, y)
    for i in range(len(voisins)):
        adjacents = trouverAdjacents(g, voisins[i][0], voisins[i][1])
        q = adjacents[0]
        caseEchec = adjacents[1]
        reussite = bellman(g, voisins[i][0], voisins[i][1], poids, gamma)
        
        echec = 0
        for j in range(q):
            echec += 1/16 * bellman(g, adjacents[1][j][0], adjacents[1][j][1], poids, gamma)

        possibilite = - (poids(g[voisins[i][0], voisins[i][1]]) - 1) + gamma * ((1 - q/16) * reussite + echec)
        if possibilite > maximum:
            maximum = possibilite
    return maximum

Mafenetre = Tk()
Mafenetre.title('MDP')

zoom=2

alea = 0 #transitions aleatoires si alea =1 sinon mettre alea=0

#taille de la grille
nblignes=10
nbcolonnes=15
 
globalcost=0

# Creation d'un widget Canvas (pour la grille)
Largeur = zoom*20*nbcolonnes+40
Hauteur = zoom*20*nblignes+40
 
# valeurs de la grille
g= np.zeros((nblignes,nbcolonnes), dtype=numpy.int)
cost= np.zeros(5, dtype=numpy.int)
weight= np.zeros(5, dtype=numpy.int)
weight[0] = 1
weight[1] = 10
weight[2] = 20
weight[3] = 30
weight[4] = 40

# def des couleurs
myred="#D20B18"
mygreen="#25A531"
myblue="#0B79F7"
mygrey="#E8E8EB"
myyellow="#F9FB70"
myblack="#2D2B2B"
mywalls="#5E5E64"
mywhite="#FFFFFF"
color=[mywhite,mygreen,myblue,myred,myblack]

# ecriture du quadrillage et coloration
Canevas = Canvas(Mafenetre, width = Largeur, height =Hauteur, bg =mywhite)
for i in range(nblignes+1):
    ni=zoom*20*i+20
    Canevas.create_line(20, ni, Largeur-20,ni)
for j in range(nbcolonnes+1):
    nj=zoom*20*j+20
    Canevas.create_line(nj, 20, nj, Hauteur-20)
colordraw(g,nblignes,nbcolonnes)

 
Canevas.focus_set()
Canevas.bind('<Key>',Clavier)
Canevas.pack(padx =5, pady =5)

PosX = 20+10*zoom
PosY = 20+10*zoom

# Creation d'un widget Button (bouton Quitter)
Button(Mafenetre, text ='Restart', command = initialize).pack(side=LEFT,padx=5,pady=5)
Button(Mafenetre, text ='Quit', command = Mafenetre.destroy).pack(side=LEFT,padx=5,pady=5)

w = Label(Mafenetre, text='Cost = '+str(globalcost),fg=myblack,font = "Verdana 14 bold")
w.pack() 

Pion = Canevas.create_oval(PosX-10,PosY-10,PosX+10,PosY+10,width=2,outline='black',fill=myyellow)

initialize()

Mafenetre.mainloop()
