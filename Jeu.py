import json

from tkinter import*
from tkinter.messagebox import *
from tkinter.filedialog import *

import time

from random import *

from Grille import *

from Constante import *

from Sommet import *

from Graphe import *

from GenerationArbreCoups import *

from IA_hex import *

class Jeu:

    def __init__(self):
        
        self.taille = None
        # stocke la configuration (IA ou joueur) de chacun des joueurs
        self.joueurs = {} 
        self.coups = 0

        self.menu()

        # matrice de Sommet utilisée dans les graphes et taille n*n
        self.sommets = []
        for i in range(self.taille):
            self.sommets.append([])
        for i in range(self.taille):
            for j in range(self.taille):
                self.sommets[i].append(Sommet())
                
        # ajoute tous les sommets qui touchent un bord dans un Graphe correspondant
        Graphe(LIBRE,B_HAUT_BLEU|B_GAUCHE_ROUGE).ajoutSommet(self.sommets[0][0])
        Graphe(LIBRE,B_HAUT_BLEU|B_DROIT_ROUGE).ajoutSommet(self.sommets[0][self.taille-1])
        Graphe(LIBRE,B_BAS_BLEU|B_GAUCHE_ROUGE).ajoutSommet(self.sommets[self.taille-1][0])
        Graphe(LIBRE,B_BAS_BLEU|B_DROIT_ROUGE).ajoutSommet(self.sommets[self.taille-1][self.taille-1])
        
        for i in range(self.taille):
            if i == 0:
                for j in range(1,self.taille-1):
                    Graphe(LIBRE,B_HAUT_BLEU).ajoutSommet(self.sommets[i][j])
            elif i == self.taille-1:
                for j in range(1,self.taille-1):
                    Graphe(LIBRE,B_BAS_BLEU).ajoutSommet(self.sommets[i][j])
            else:
                Graphe(LIBRE,B_GAUCHE_ROUGE).ajoutSommet(self.sommets[i][0])
                Graphe(LIBRE,B_DROIT_ROUGE).ajoutSommet(self.sommets[i][self.taille-1])
        
        # ajoute les voisins correspondants pour chacun des Sommet
        for x in range(self.taille):
            for y in range(self.taille):
                if x != 0:
                    self.sommets[x][y].ajoutVoisin(self.sommets[x-1][y])
                if y != 0:
                    self.sommets[x][y].ajoutVoisin(self.sommets[x][y-1])
                    if x != self.taille-1:
                        self.sommets[x][y].ajoutVoisin(self.sommets[x+1][y-1])
                if x != self.taille-1:
                    self.sommets[x][y].ajoutVoisin(self.sommets[x+1][y])
                if y != self.taille-1:
                    if x != 0:
                        self.sommets[x][y].ajoutVoisin(self.sommets[x-1][y+1])
                    self.sommets[x][y].ajoutVoisin(self.sommets[x][y+1])
        self.NN = Neuron(self.taille)
        self.grille = Grille(Point(10,30),self.taille,self.sommets)
        
        self.tourActuel = ROUGE

        self.plateaux = {}
        if (self.taille <= 4):
            self.genererPlateaux()

        self.canvas = 0
        self.fenetre = 0
        self.commencer()

    # afficher le menu de configuration de la partie
    def menu(self):
        fenetreMenu = Tk(className='configuration')
        fenetreMenu.resizable(width=False, height=False)
        fenetreMenu.geometry('320x200+700+300')

        FrameTaille = Frame(fenetreMenu,pady=10,padx=10)
        texteTaille = Label(FrameTaille, text="Taille : ", font="Arial 15")
        texteTaille.pack(side='left')
        taille = Spinbox(FrameTaille,from_=2, to=11,font="Arial 15",width=15)
        taille.pack(side='right')
        FrameTaille.pack()
            
        FrameJoueur = Frame(fenetreMenu,pady=10)
        Frame1 = Frame(FrameJoueur)
        choix1 = [("Joueur","Joueur"),("IA","IA")]

        texteJoueur1 = Label(Frame1,text="Joueur 1 : ",fg=COULEUR_ROUGE, font="Arial 15")
        texteJoueur1.pack(side='left')

        choix1 = [("Joueur",0),("IA",1)]
        var1 = StringVar()
        for text, val in choix1 :
            rb = Radiobutton(Frame1, text=text, variable=var1, value=val, font="Arial 15")
            # valeur par defaut : joueur 1 IA
            if (val == 1):
                rb.select()
            rb.pack(side='right')
        Frame1.pack()

        Frame2 = Frame(FrameJoueur, pady=10)
        texteJoueur2 = Label(Frame2,text="Joueur 2 : ", fg=COULEUR_BLEU,font="Arial 15")
        texteJoueur2.pack(side='left')

        choix2 = [("Joueur",0),("IA",1)]
        var2 = StringVar()
        for text, val in choix2:
            rb2 = Radiobutton(Frame2, text=text, variable=var2, value=val, font="Arial 15")
            # valeur par defaut : joueur 2 Joueur
            if (val == 0):
                rb2.select()
            rb2.pack(side='right')
        Frame2.pack()
        FrameJoueur.pack()

        b = Button(fenetreMenu,text="Jouer",command=lambda: self.verifier(fenetreMenu,taille.get(),var1.get(),var2.get()))
        b.pack()

        fenetreMenu.mainloop()

    # verifier que les parametres saisis via le menu sont corrects
    def verifier(self,fenetre,taille,J1,J2):
        # verifier que la taille saisie est un entier
        if (taille.isdigit()):
            if (not (int(taille) >= 2 and int(taille) <= 11)):
                showerror('Taille de grille incorrecte','Veuillez selectionner une taille de grille comprise entre 2 et 11.')
                return False
        else:
            showerror('Taille de grille incorrecte','Veuillez selectionner une taille de grille comprise entre 2 et 11.')
            return False
        if (J1 != '0' and J1 != '1'):
            showerror('Joueur 1 non selectionné','Veuillez selectionner entre IA et Joueur.')
            return False
        if (J2 != '0' and J2 != '1'):
            showerror('Joueur 2 non selectionné','Veuillez selectionner entre IA et Joueur.')
            return False
        self.taille = int(taille)
        self.joueurs[ROUGE] = int(J1)
        self.joueurs[BLEU] = int(J2) 
        fenetre.destroy()

    # commencer une partie
    def commencer(self):
        global canvasTour
        global oval

        self.fenetre = Tk(className="Jeu de Hex")
        self.fenetre.resizable(width=False, height=False)

        FrameGrille = Frame(self.fenetre,relief=GROOVE)
        self.canvas = Canvas(FrameGrille, width=self.grille.taille*100, height=self.grille.taille*67 + 30, background='#ddd')
        
        FrameOptions = Frame(self.fenetre,relief=GROOVE)
        nouvPartieButton = Button(FrameOptions, text="Nouv. partie", command=lambda: self.nouvPartie())
        nouvPartieButton.grid(row=0,column=0,padx=10,pady=10)
        quitterButton = Button(FrameOptions, text="Quitter", fg='red', command=self.fenetre.destroy)
        quitterButton.grid(row=0,column=2,padx=10,pady=10)
        canvasTour = Canvas(FrameOptions, width=40, height=40)
        oval = canvasTour.create_oval(10,10,30,30,width=2,fill=COULEUR_ROUGE,outline='')
        canvasTour.grid(row=0,column=1,pady=10)
        
        FrameGrille.pack(side=TOP)
        FrameOptions.pack(side=BOTTOM)

        self.grille.tracer(self.canvas)
        self.canvas.bind("<Button-1>",self.jouer)    
        self.canvas.pack()
        self.fenetre.after(1000,self.jouerIA)
        self.fenetre.mainloop()

    #Créer une nouvelle partie (réglages différents)
    def nouvPartie(self):
        self.fenetre.destroy()
        Graphe.gagnant = ""
        self.taille = 3
        self.sommets = []
        for i in range(self.taille):
            self.sommets.append([])
        for i in range(self.taille):
            for j in range(self.taille):
                self.sommets[i].append(Sommet())
                
        # ajoute tous les sommets qui touchent un bord dans un Graphe correspondant
        Graphe(LIBRE,B_HAUT_BLEU|B_GAUCHE_ROUGE).ajoutSommet(self.sommets[0][0])
        Graphe(LIBRE,B_HAUT_BLEU|B_DROIT_ROUGE).ajoutSommet(self.sommets[0][self.taille-1])
        Graphe(LIBRE,B_BAS_BLEU|B_GAUCHE_ROUGE).ajoutSommet(self.sommets[self.taille-1][0])
        Graphe(LIBRE,B_BAS_BLEU|B_DROIT_ROUGE).ajoutSommet(self.sommets[self.taille-1][self.taille-1])
        
        for i in range(self.taille):
            if i == 0:
                for j in range(1,self.taille-1):
                    Graphe(LIBRE,B_HAUT_BLEU).ajoutSommet(self.sommets[i][j])
            elif i == self.taille-1:
                for j in range(1,self.taille-1):
                    Graphe(LIBRE,B_BAS_BLEU).ajoutSommet(self.sommets[i][j])
            else:
                Graphe(LIBRE,B_GAUCHE_ROUGE).ajoutSommet(self.sommets[i][0])
                Graphe(LIBRE,B_DROIT_ROUGE).ajoutSommet(self.sommets[i][self.taille-1])
        
        # ajoute les voisins correspondants pour chacun des Sommet
        for x in range(self.taille):
            for y in range(self.taille):
                if x != 0:
                    self.sommets[x][y].ajoutVoisin(self.sommets[x-1][y])
                if y != 0:
                    self.sommets[x][y].ajoutVoisin(self.sommets[x][y-1])
                    if x != self.taille-1:
                        self.sommets[x][y].ajoutVoisin(self.sommets[x+1][y-1])
                if x != self.taille-1:
                    self.sommets[x][y].ajoutVoisin(self.sommets[x+1][y])
                if y != self.taille-1:
                    if x != 0:
                        self.sommets[x][y].ajoutVoisin(self.sommets[x-1][y+1])
                    self.sommets[x][y].ajoutVoisin(self.sommets[x][y+1])
        self.NN = Neuron(self.taille)
        self.NN.load()
        self.grille = Grille(Point(10,30),self.taille,self.sommets)
        
        self.tourActuel = ROUGE

        self.plateaux = {}
        if (self.taille <= 4):
            self.genererPlateaux()

        self.canvas = 0
        self.fenetre = 0
        self.commencer()
 
    # verifier si la grille actuelle est gagnante pour un des joueur
    def victoire(self):

        if(Graphe.gagnant=="ROUGE"):
            Graphe.gagnant = ""
            self.tourActuel = -1
            self.NN.backward(self.l_res_back,2)
            self.NN.save()
            self.nouvPartie()
            return ROUGE
            
        elif(Graphe.gagnant=="BLEU"):
            Graphe.gagnant = ""
            self.tourActuel = -1
            self.NN.backward(self.l_res_back,-2)
            self.NN.save()
            self.nouvPartie()
            return BLEU

        return False
        
    # passer au tour suivant
    def tourSuivant(self):
        global canvasTour
        global oval

        canvasTour.delete(oval)
        if (self.tourActuel == ROUGE):
            self.tourActuel = BLEU
            oval = canvasTour.create_oval(10,10,30,30,width=2,fill=COULEUR_BLEU,outline='')
        else:
            self.tourActuel = ROUGE
            oval = canvasTour.create_oval(10,10,30,30,width=2,fill=COULEUR_ROUGE,outline='')
            
    # verifier si l'arbre des coups a jouer a deja ete genere, sinon le generer
    def genererPlateaux(self):
        voisin(self.taille)
        if (not (os.path.isfile("./plateaux/"+str(self.taille)+"/"+str(self.coups)+".txt"))):
            self.plateaux = ArbreCoups(self.code(),self.tourActuel,self.coups).json(self.coups,self.taille)
            ecrireFichier(genFichier(self.taille,self.coups),self.plateaux)
        with open("./plateaux/"+str(self.taille)+"/"+str(self.coups)+".txt") as json_file:
            self.plateaux = json.load(json_file)
            if(not self.index() in self.plateaux):
                self.plateaux.update(ArbreCoups(self.code(),self.tourActuel,self.coups).json(self.coups,self.taille))
                ecrireFichier(genFichier(self.taille,self.coups),self.plateaux)
            
    # retourner l'index correspondant au plateau actuel
    def index(self):
        index = 0
        for i in range(len(self.sommets)):
            for j in range(len(self.sommets[i])):
                index = index + self.sommets[i][j].couleur*pow(3,i*self.taille + j)
        return str(int(index))

    # retourner un code correspondant a l'etat de chacune des cases (0: LIBRE, 1: ROUGE, 2: BLEU)
    def code(self):
        code = list()
        for i in range(len(self.sommets)):
            for j in range(len(self.sommets[i])):
                code.append(self.sommets[i][j].couleur)
        code = ''.join(map(str,code))
        
        return code

    # placer un pion (pour un joueur humain)
    def jouer(self,event):
        global canvasTour
        global oval
        
        if (self.joueurs[self.tourActuel] == 0):
            p = Point(event.x,event.y)
            hexagone = self.grille.trouver(p)
            # verifier si l'endroit clique est une case et s'il n'y a pas de pion dessus
            if((hexagone) and (hexagone.estLibre())) :
                hexagone.sommet.jouer(self.tourActuel)
                self.grille.placer(self.tourActuel,hexagone,self.canvas)
                                        
                self.coups = self.coups + 1
                self.tourSuivant()

                victoire = self.victoire()
                if (not victoire):
                    # si le prochain tour est un IA, le lancer
                    if (self.joueurs[self.tourActuel] == 1): 
                        self.fenetre.after(1000,self.jouerIA)

    def get_neighbors(self, x, y):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        neighbors = []
        for dx, dy in directions:
            nx = x + dx
            ny = y + dy
            if nx >= 0 and ny >= 0 and nx < self.taille and ny < self.taille :
                neighbors.append((nx, ny))
        return neighbors

    # placer un pion (pour une IA)
    def jouerIA(self):
        global canvasTour
        global oval
        liste = self.code()
        self.liste_res = [[]for i in range(self.taille)]
        for i in range(len(liste)) :
            if liste[i] == '2' :
                self.liste_res[i//self.taille] += [-200000]
            elif liste[i] == '1' :
                self.liste_res[i//self.taille] += [-100000]
            else :
                self.liste_res[i//self.taille] += [0]

        for x in range(self.taille) :
            for y in range(self.taille) :
                if self.liste_res[x][y] > -100 :
                    nei = self.get_neighbors(x,y)
                    for i in nei :
                        compt = self.liste_res[x][y] 
                        if self.liste_res[i[0]][i[1]] == -100000:
                            compt+=1000
                        if self.liste_res[i[0]][i[1]] == -200000:
                            compt+=800
                    self.liste_res[x][y] = compt

        if (self.joueurs[self.tourActuel] == 1):
            
            self.out = self.NN.forward(self.liste_res)
            res = np.argmax(self.out)
            if (not(self.index() in self.plateaux)):
                self.genererPlateaux()
            self.l_res_back = self.liste_res
            self.l_res_back[res//self.taille][res%self.taille]= -100000
            if (self.grille.hexagones[res//self.taille][res%self.taille].estLibre()!=True) :
                self.NN.backward(self.l_res_back,-3)
                self.NN.save()
            else :
                self.NN.backward(self.l_res_back,1)
                self.NN.save()
            hexagone = self.grille.hexagones[res//self.taille][res%self.taille]
            hexagone.sommet.jouer(self.tourActuel)
            self.grille.placer(self.tourActuel,hexagone,self.canvas)

            self.coups = self.coups + 1
            self.tourSuivant()

            victoire = self.victoire()
            if (not victoire):
                if (self.joueurs[self.tourActuel] == 1): #Si le prochain tour est un IA, le lancer
                    self.fenetre.after(10,self.jouerIA)
Jeu()
