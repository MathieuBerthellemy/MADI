# script pion.py hjyf
from __future__ import division
from Tkinter import *
import numpy as np
from SolverGurobiDual import *
from SolverGurobiPrimal import *
from SolverIteration import *
import numpy
import math
import time

question = 2

def initialize():
    global PosX,PosY,cost, globalcost
# position initiale du robot
    PosX = 20+10*zoom
    PosY = 20+10*zoom
    for k in range(6):
        cost[k]=0
# cout et affichage
    Canevas.coords(Pion,PosX -9*zoom, PosY -9*zoom, PosX +9*zoom, PosY +9*zoom)
    w.config(text='Cost = '+ str(globalcost))

def colordraw(g,nblignes,nbcolonnes):
    global question
    pmur=-1 #0.15
    pblanc=-1 #0.55
    pverte=-1
    pbleue=-1
    prouge=-1
    pnoire=-1

    if question == 1:
        pmur=0.15 #0.15
        pblanc=0.55 #0.55
        pverte=0.1
        pbleue=0.1
        prouge=0.1
        pnoire=0.1
    elif question == 2:
        pmur=0.15 #0.15
        pblanc=0.45 #0.55
        pverte=0.0
        pbleue=0.2
        prouge=0.2
        pnoire=0.0

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
                    
    g[nblignes-1,nbcolonnes-1]=5
  

def Play(selector, li, cj):
    global PosX,PosY,cost,g, globalcost, s
    changed=0
    count_red = 0
    count_blue = 0

    touche = selector.get_move(x, y)


    if touche == 'Y' and li>1 and cj < nbcolonnes-1 and g[li-2,cj+1]>-1:
        PosY -= zoom*20*2
        PosX += zoom*20 
        cost[g[li-2,cj+1]]+=1 

        if g[li-2,cj+1] == 3: 
            count_red += 1
        if g[li-2,cj+1] == 2: 
            count_blue += 1

        changed=1
    # deplacement (-2,-1)
    if touche == 'T' and li>1 and cj > 0 and g[li-2,cj-1]>-1:
        PosY -= zoom*20*2       
        PosX -= zoom*20                 
        cost[g[li-2,cj-1]]+=1
        changed=1

        if g[li-2,cj-1] == 3: 
            count_red += 1
        if g[li-2,cj-1] == 2: 
            count_blue += 1


   # deplacement (-1,2)
    if touche == 'U' and li>0 and cj < nbcolonnes-2 and g[li-1,cj+2]>-1:
        PosY -= zoom*20        
        PosX += zoom*20*2       
        cost[g[li-1,cj+2]]+=1
        changed=1
        if g[li-1,cj+2] == 3: 
            count_red += 1
        if g[li-1,cj+2] == 2: 
            count_blue += 1
    # deplacement (-1,-2)
    if touche == 'R' and li>0 and cj >1 and g[li-1,cj-2]>-1:
        PosY -= zoom*20
        PosX -= zoom*20*2           
        cost[g[li-1,cj-2]]+=1
        changed=1
        if g[li-1,cj-2] == 3: 
            count_red += 1
        if g[li-1,cj-2] == 2: 
            count_blue += 1
     # deplacement (2,1)  
    if touche == 'H' and li<nblignes-2 and cj < nbcolonnes-1 and g[li+2,cj+1]>-1:
        PosY += zoom*20*2
        PosX += zoom*20 
        cost[g[li+2,cj+1]]+=1
        changed=1
        if g[li+2,cj+1] == 3: 
            count_red += 1
        if g[li+2,cj+1] == 2: 
            count_blue += 1
    # deplacement (2,-1)
    if touche == 'G' and li<nblignes-2 and cj > 0 and g[li+2,cj-1]>-1:
        PosY += zoom*20*2       
        PosX -= zoom*20                 
        cost[g[li+2,cj-1]]+=1
        changed=1
        if g[li+2,cj-1] == 3: 
            count_red += 1
        if g[li+2,cj-1] == 2: 
            count_blue += 1
   # deplacement (1,2)
    if touche == 'J' and li<nblignes-1 and cj < nbcolonnes-2 and g[li+1,cj+2]>-1:
        PosY += zoom*20        
        PosX += zoom*20*2       
        cost[g[li+1,cj+2]]+=1
        changed=1
        if g[li+1,cj+2] == 3: 
            count_red += 1
        if g[li+1,cj+2] == 2: 
            count_blue += 1
    # deplacement (1,-2)
    if touche == 'F' and li<nblignes-1 and cj >1 and g[li+1,cj-2]>-1:
        PosY += zoom*20
        PosX -= zoom*20*2           
        cost[g[li+1,cj-2]]+=1 
        changed=1
        if g[li+1,cj-2] == 3: 
            count_red += 1
        if g[li+1,cj-2] == 2: 
            count_blue += 1

    
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
            #print('d',dli,dcj)
            if newli>=0 and newcj>=0 and newli<=nblignes-1 and newcj<=nbcolonnes-1 and g[newli,newcj]>-1:
                PosY=NewPosY
                PosX=NewPosX        

    return count_blue, count_red    
            
# on dessine le pion a sa nouvelle position
    Canevas.coords(Pion,PosX -9*zoom, PosY -9*zoom, PosX +9*zoom, PosY +9*zoom)       
    globalcost=0    
    for k in range(5):
        globalcost+=cost[k]*weight[k]
    w.config(text='Cost = '+ str(globalcost))  

def Clavier(event):
    global PosX,PosY,cost,g, globalcost, s
    touche = event.keysym
    cj=(PosX-30)/(20*zoom)
    li=(PosY-30)/(20*zoom)
    changed=0
    # deplacement aleatoire en appuyant sur space
    if touche == 'space':
        t=np.random.randint(6)
        #lettre = ['f','g','h','j','y','u',]
        #lettre = 
        #touche=lettre[t]
        print s.get_move(li, cj)
        touche = s.get_move(li, cj).lower()
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

Mafenetre = Tk()
Mafenetre.title('MDP')


zoom = 2


alea = 1 #transitions aleatoires si alea =1 sinon mettre alea=0

#taille de la grille
nblignes=10
nbcolonnes=10
 
globalcost=0

# Creation d'un widget Canvas (pour la grille)
Largeur = zoom*20*nbcolonnes+40
Hauteur = zoom*20*nblignes+40
 
# valeurs de la grille
g = np.zeros((nblignes,nbcolonnes), dtype=numpy.int)
cost= np.zeros(6, dtype=numpy.int)
weight= np.zeros(6, dtype=numpy.int)

if question == 1:
    weight[0] = 1
    weight[1] = 10
    weight[2] = 20
    weight[3] = 30
    weight[4] = 40
    weight[5] = 998
elif question == 2:
    weight[0] = 0
    weight[1] = 0
    weight[2] = 1
    weight[3] = 1
    weight[4] = 0
    weight[5] = 1000

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
PosX = 20+10*zoom
PosY = 20+10*zoom
Pion = Canevas.create_oval(PosX-10,PosY-10,PosX+10,PosY+10,width=2,outline='black',fill=myyellow)



 
Canevas.focus_set()
Canevas.bind('<Key>',Clavier)
Canevas.pack(padx =5, pady =5)




# Creation d'un widget Button (bouton Quitter)
Button(Mafenetre, text ='Restart', command = initialize).pack(side=LEFT,padx=5,pady=5)
Button(Mafenetre, text ='Quit', command = Mafenetre.destroy).pack(side=LEFT,padx=5,pady=5)

w = Label(Mafenetre, text='Cost = '+str(globalcost),fg=myblack,font = "Verdana 14 bold")
w.pack() 



(width, height) = g.shape
initialize()
for i in range(nblignes+1):
    ni=zoom*20*i+20
    Canevas.create_line(20, ni, Largeur-20,ni)
for j in range(nbcolonnes+1):
    nj=zoom*20*j+20
    Canevas.create_line(nj, 20, nj, Hauteur-20)
colordraw(g,nblignes,nbcolonnes)

print g
if question == 1:
    s = SolverIteration2(g, weight)
    #print s.solution
    #print s.values
elif question == 2:
    s = SolverGurobiDual(g, weight)
    #s = SolverGurobiPrimal(g, weight)
    #print s.solution
    #print s.values



def echelle(c1, c2, c3, val, min_val, max_val):
    r1, g1, b1 = c1[0], c1[1], c1[2]
    r2, g2, b2 = c2[0], c2[1], c2[2]
    r3, g3, b3 = c3[0], c3[1], c3[2]
    
    r = 0
    g = 0
    b = 0

    middle = (max_val + min_val)/2

    if val < middle:
        alpha = 1 - (val - min_val) / max((middle - min_val), 1)
        beta = val / max((middle - min_val), 1)

        r = int(r1 * alpha + r2 * beta)
        g = int(g1 * alpha + g2 * beta)
        b = int(b1 * alpha + b2 * beta)
    else:
        alpha = 1 - (val - middle) / max((max_val - middle), 1)
        beta = (val - middle) /   max((max_val - middle), 1)

        r = int(r2 * alpha + r3 * beta)
        g = int(g2 * alpha + g3 * beta)
        b = int(b2 * alpha + b3 * beta)

    return (min(r, 254), min(g, 254), min(b, 254))

for lin in range(width):
    for col in range(height):
        y = col*20*zoom+20
        x = lin*20*zoom+20
            
        
        if g[lin][col] != -1 :

            (red, green, blue) = echelle((92, 84, 164), (252, 254, 180), (175, 16, 71), int(s.values[lin][col]), int(np.nanmin(s.values)), int(np.nanmax(s.values)))
            
            # print s.values[lin][col], min_except(s.values, -1), s.values.max()
            # print red, green, blue
            case_color = "#%02x%02x%02x"%(red, green, blue) 
            rec = Canevas.create_rectangle(y, x, y+zoom*20, x+zoom*20, fill=case_color)

            Canevas.tag_lower(rec)   
            Canevas.create_text(y +10, x +10, text=s.get_move(lin, col))
            Canevas.create_text(y + 20, x +30, text=int(s.values[lin][col]))


if question == 1:
    pass
elif question == 2:
    do_PL_dual = True
    do_PL_primal = False

    s_1 = None
    s_2 = None

    rouge_1 = []
    bleu_1 = []

    cum_count_coup_1 = 0
    cum_count_score_1 = 0
    cum_count_time_1 = 0
    rouge_2 = []
    bleu_2 = []

    cum_count_coup_2 = 0
    cum_count_score_2 = 0
    cum_count_time_2 = 0

    if do_PL_dual:
        t0_1 = time.time()
        s_1 = SolverGurobiDual(g, weight)
        count_time_1 = time.time() - t0_1

        

    if do_PL_primal:
        t0_2 = time.time()
        s_2 = SolverIteration(g, weight)
        count_time_2 = time.time() - t0_2

        

    rep = 1000
    for i in range(rep):
        print "experience: ", i

        if do_PL_dual:
            initialize()
            
            count_red_1 = 0
            count_blue_1 = 0
            count_coup_1 = 0
            count_score_1 = 0
            #print "rep", i
            while True:
                count_score_1 -= 2
                count_score_1 = count_score_1 + red + blue
                
                count_coup_1 += 1
               
                y=int((PosX-30)/(20*zoom))
                x=int((PosY-30)/(20*zoom))

                blue, red = Play(s_1, x, y)
                count_blue_1 += blue
                count_red_1 += red

                #print x, y
                if x == nblignes-1 and y == nbcolonnes-1:
                    count_score_1 += 1000
                    #print "fini: ", count_blue, count_red
                    rouge_1.append(count_red_1)
                    bleu_1.append(count_blue_1)
                    cum_count_coup_1 += count_coup_1
                    cum_count_score_1 += count_score_1
                    break
        
        
        if do_PL_primal:
            initialize()
            count_red_2 = 0
            count_blue_2 = 0
            count_coup_2 = 0
            count_score_2 = 0
            #print "rep", i
            while True:

                count_score_2 -= 2
                count_score_2 = count_score_2 + red + blue
                
                count_coup_2 += 1
               
                y=int((PosX-30)/(20*zoom))
                x=int((PosY-30)/(20*zoom))

                blue, red = Play(s_2, x, y)
                count_blue_2 += blue
                count_red_2 += red

                #print x, y
                if x == nblignes-1 and y == nbcolonnes-1:
                    count_score_2 += 1000
                    #print "fini: ", count_blue, count_red
                    rouge_2.append(count_red_2)
                    bleu_2.append(count_blue_2)
                    cum_count_coup_2 += count_coup_2
                    cum_count_score_2 += count_score_2
                    break
        
        
    if do_PL_dual:
        print "######## PL ########"
        print "BLUE: ", np.mean(bleu_1)
        print "RED: ", np.mean(rouge_1)
        print "Coups: ", cum_count_coup_1/float(rep)
        print "Score: ", cum_count_score_1/float(rep)
        print "Computing: %.2f"%count_time_1
        print "####################"

    if do_PL_primal:
        print "#### Iteration ####"
        print "BLUE: ", np.mean(bleu_2)
        print "RED: ", np.mean(rouge_2)
        print "Coups: ", cum_count_coup_2/float(rep)
        print "Score: ", cum_count_score_2/float(rep)
        print "Computing: %.2f"%count_time_2
        print "###################"




Mafenetre.mainloop()





