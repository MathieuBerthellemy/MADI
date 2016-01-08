import numpy as np
class SolverIteration:

    def __init__(self, grid, weight):
        self.grid = grid
        # Coment appeler la fonction, a integrer dans le code
        states = self.trouverStates()
        self.solution = np.chararray((len(grid), len(grid[0])))
        solution = self.iterationValeur(states, weight, 0.5, 0.9)


        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                if (i, j) in states:
                    self.solution[i, j] = solution[states.index((i, j))]
                else:
                    self.solution[i, j] = "_"



    # Renvoie sous forme de liste de cases les cases adjacentes a la case en question
    # Arguments : g = la matrice, x et y = coordonnees du point
    def trouverAdjacents(self, x, y):
        g = self.grid
        nombreAdjacents = 0
        adjacents = []
        # Coin en haut a gauche
        if x == 0 and y == 0:
            if g[0,1] > -1:
                adjacents.append((0, 1))
            if g[1,0] > -1:
                adjacents.append((1, 0))
            if g[1,1] > -1:
                adjacents.append((1, 1))

        # Coin en haut a droite
        elif x == 0 and y == g.shape[1] - 1:
            if g[0, y - 1] > -1:
                adjacents.append((0, y - 1))
            if g[1, y - 1] > -1:
                adjacents.append((1, y - 1))
            if g[1, y] > -1:
                adjacents.append((1, y))

        # Coin en bas a gauche
        elif x == g.shape[0] - 1 and y == 0:
            if g[x - 1, 0] > -1:
                adjacents.append((x - 1, 0))
            if g[x - 1, 1] > -1:
                adjacents.append((x - 1, 1))
            if g[x, 1] > -1:
                adjacents.append((x, 1))
        # Coin en bas a droite
        elif x == g.shape[0] - 1 and y == g.shape[1] - 1:
            if g[x - 1, y] > -1:
                adjacents.append((x - 1, y))
            if g[x, y - 1] > -1:
                adjacents.append((x, y - 1))
            if g[x - 1, y - 1] > -1:
                adjacents.append((x - 1, y - 1))
        # Ligne du haut
        elif x == 0:
            if g[x, y + 1] > -1:
                adjacents.append((x, y + 1))
            if g[x, y - 1] > -1:
                adjacents.append((x, y - 1))
            if g[x + 1, y] > -1:
                adjacents.append((x + 1, y))
            if g[x + 1, y - 1] > -1:
                adjacents.append((x + 1, y - 1))
            if g[x + 1, y + 1] > -1:
                adjacents.append((x + 1, y + 1))

        # Ligne du bas
        elif x == g.shape[0] - 1:
            adjacents.extend([(x, y + 1), (x, y - 1), (x - 1, y), (x - 1, y - 1), (x - 1, y + 1)])
            if g[x, y + 1] > -1:
                adjacents.append((x, y + 1))
            if g[x, y - 1] > -1:
                adjacents.append((x, y - 1))
            if g[x - 1, y] > -1:
                adjacents.append((x - 1, y))
            if g[x - 1, y - 1] > -1:
                adjacents.append((x - 1, y - 1))
            if g[x - 1, y + 1] > -1:
                adjacents.append((x - 1, y + 1))
                             
        # Ligne de la gauche
        elif y == 0:
            if g[x + 1, y] > -1:
                adjacents.append((x + 1, y))
            if g[x - 1, y] > -1:
                adjacents.append((x - 1, y))
            if g[x, y + 1] > -1:
                adjacents.append((x, y + 1))
            if g[x + 1, y + 1] > -1:
                adjacents.append((x + 1, y + 1))
            if g[x - 1, y + 1] > -1:
                adjacents.append((x - 1, y + 1))
                             
        # Ligne de la droite
        elif y == g.shape[1] - 1:
            if g[x + 1, y] > -1:
                adjacents.append((x + 1, y))
            if g[x - 1, y] > -1:
                adjacents.append((x - 1, y))
            if g[x, y - 1] > -1:
                adjacents.append((x, y - 1))
            if g[x + 1, y - 1] > -1:
                adjacents.append((x + 1, y - 1))
            if g[x - 1, y - 1] > -1:
                adjacents.append((x - 1, y - 1))

        # Toutes les autres cases
        else:
            if g[x + 1, y] > -1:
                adjacents.append((x + 1, y))
            if g[x - 1, y] > -1:
                adjacents.append((x - 1, y))
            if g[x, y - 1] > -1:
                adjacents.append((x, y - 1))
            if g[x + 1, y - 1] > -1:
                adjacents.append((x + 1, y - 1))
            if g[x - 1, y - 1] > -1:
                adjacents.append((x - 1, y - 1))
            if g[x + 1, y + 1] > -1:
                adjacents.append((x + 1, y + 1))
            if g[x, y + 1] > -1:
                adjacents.append((x, y + 1))
            if g[x - 1, y + 1] > -1:
                adjacents.append((x - 1, y + 1))

        return adjacents


    #def bellman(g, x, y, poids, gamma):
    #    maximum = - 999
    #    voisins = trouverVoisins(g, x, y)
    #    for i in range(len(voisins)):
    #        adjacents = trouverAdjacents(g, voisins[i][0], voisins[i][1])
    #        q = adjacents[0]
    #        caseEchec = adjacents[1]
    #        reussite = bellman(g, voisins[i][0], voisins[i][1], poids, gamma)
    #        
    #        echec = 0
    #        for j in range(q):
    #            echec += 1/16 * bellman(g, adjacents[1][j][0], adjacents[1][j][1], poids, gamma)
    #
    #        possibilite = - (poids(g[voisins[i][0], voisins[i][1]]) - 1) + gamma * ((1 - q/16) * reussite + echec)
    #        if possibilite > maximum:
    #            maximum = possibilite
    #    return maximum


    # Renvoie les etats possibles = les cases qui ne sont pas noires
    def trouverStates(self):
        g = self.grid
        states = []
        tailleG = g.shape
        for ligne in range(tailleG[0]):
            for colonne in range(tailleG[1]):
                if g[ligne, colonne] > -1:
                    states.append((ligne, colonne))
        return states

    # Renvoie les actions possibles a partir de l'etat actuel, sous forme de liste
    def trouverActions(self, state):
        g = self.grid
        actions = ["F", "G", "R", "T", "U", "Y", "H", "J"]
        x = state[0]
        y = state[1]

        if "F" in actions:
            if x == g.shape[0] - 1 or y <= 1 or g[x+1, y-2] == -1:
                actions.remove("F")
        if "G" in actions:
            if x >= g.shape[0] - 2 or y == 0 or g[x+2, y-1] == -1:
                actions.remove("G")
        if "R" in actions:
            if x == 0 or y <= 1 or g[x-1, y-2] == -1:
                actions.remove("R")
        if "T" in actions:
            if x <=1 or y == 0 or g[x-2, y-1] == -1:
                actions.remove("T")
        if "U" in actions:
            if x == 0 or y >= g.shape[1] - 2 or g[x-1, y+2] == -1:
                actions.remove("U")
        if "Y" in actions:
            if x <= 1 or y == g.shape[1] - 1 or g[x-2, y+1] == -1:
                actions.remove("Y")
        if "H" in actions:
            if x >= g.shape[0] - 2 or y == g.shape[1] - 1 or g[x+2, y+1] == -1:
                actions.remove("H")
        if "J" in actions:
            if x == g.shape[0] - 1 or y >= g.shape[1] - 2 or g[x+1, y+2] == -1:
                actions.remove("J")

        return actions

    # Renvoie la case lorsque l'on applique l'action a l'etat atuel
    def trouverCaseSuivante(self, state, action):
        g = self.grid
        if action == "F":
            suivante = (state[0] + 1, state[1] - 2)
        elif action == "G":
            suivante = (state[0] + 2, state[1] - 1)
        elif action == "H":
            suivante = (state[0] + 2, state[1] + 1)
        elif action == "J":
            suivante = (state[0] + 1, state[1] + 2)
        elif action == "R":
            suivante = (state[0] - 1, state[1] - 2)
        elif action == "T":
            suivante = (state[0] - 2, state[1] - 1)
        elif action == "U":
            suivante = (state[0] - 1, state[1] + 2)
        else:
            suivante = (state[0] - 2, state[1] + 1)
        return suivante


    def get_move(self, lin, col):
        return self.solution[lin, col]

    # Algo, renvoie la matrice de la politique optimale
    def iterationValeur(self, states, rewards, gamma, epsilon):
        g = self.grid
        self.values = np.zeros(g.shape)
        valeurs = [np.zeros(g.shape)]
        Q_t_a = []
        t = 0
        while 1:
            t = t+1
            Q_t_a.append(np.zeros((len(states), 8)))
            valeurs.append(np.zeros(g.shape))
            for abcisse in range(len(states)):
                actions = self.trouverActions(states[abcisse])
                for ordonnee in range(len(actions)):
                    caseSuivante = self.trouverCaseSuivante(states[abcisse], actions[ordonnee])
                    casesAdjacentes = self.trouverAdjacents(caseSuivante[0], caseSuivante[1])
                    somme = (1 - len(casesAdjacentes)) * valeurs[t-1][caseSuivante[0], caseSuivante[1]] / 16
                    for case in casesAdjacentes:
                        somme += valeurs[t-1][case[0], case[1]] / 16
                    Q_t_a[t-1][abcisse][ordonnee] = -rewards[g[states[abcisse][0], states[abcisse][1]]] - 1 + gamma * (somme)

                valeurs[t][states[abcisse][0], states[abcisse][1]] = Q_t_a[t-1][abcisse].max()
            self.values = valeurs[t]
            valeurs_soustraction = valeurs[t] - valeurs[t-1]
            if valeurs_soustraction.max() < epsilon:
                break
                    
        meilleuresActions = []
        for abcisse in range(len(states)):
            meilleureRecompense = -9999
            meilleureAction = "_"
            actions = self.trouverActions(states[abcisse])
            for ordonnee in range(len(actions)):
                if Q_t_a[t - 1][abcisse][ordonnee] > meilleureRecompense:
                    meilleureAction = actions[ordonnee]
                    meilleureRecompense = Q_t_a[t - 1][abcisse][ordonnee]
            meilleuresActions.append(meilleureAction)

        return meilleuresActions

        
