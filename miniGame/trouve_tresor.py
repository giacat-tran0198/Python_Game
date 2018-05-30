#Sonar Treasure Hunt
#có một số lỗi:
#không hiện ra bảng mới sau mỗi lệnh

import random
import sys
import math

def creatGrille():
    grille = []
    for x in range(60):
        grille.append([])
        for y in range(15):
            if random.randint(0,1) == 0:
                grille[x].append('~')
            else:
                grille[x].append('`')
    return grille

def dessinGrille(grille):
    dixChLigne = '   ' #ligne de chiffres des dizaines
    for nb in range(1,6):
        dixChLigne += (' '*9) + str(nb)
    print(dixChLigne)
    print("   " + ("0123456789"*6))
    print()
    
    #dessiner l'ocean
    for rang in range(15):
        if rang < 10:
            if rang < 10 :
                space = " "
            else:
                space = ""
        grilleRang = ""
        for colonne in range (60):
            grilleRang += grille[colonne][rang]
        print (space, rang, grilleRang, rang)

# Creater les Tresor
def creatRandomTresor(numTresor):
    tresor = []
    while len(tresor) < numTresor:
        temp = [random.randint(0,59),random.randint(0,14)]
        if temp not in tresor:
            tresor.append(temp)
    return tresor

#determiner les mouvements valide
def dansGrille(x,y):
    return (0<=x<=59) and (0<=y<=14)

#verifier les tresors retrouve
def Deplace(grille, tresor, x, y):
    petitDistance = 100
    for nbLg, nbCol in tresor:
        distance = math.sqrt((nbLg-x)**2 + (nbCol-y)**2)
        if distance < petitDistance:
            petitDistance = distance
    if petitDistance == 0:
        tresor.remove([x,y])
        return "Vous avez trouve un tresor"
    elif petitDistance < 10:
        grille[x][y] = str(petitDistance)
        return "Trésors détectés à une distance de %s" + str(petitDistance)
    else:
        grille[x][y] = "X"
        return "Sonar n'a rien detecte"

def entreMvt(avantMvt):
    print ("Entrez la position (x0-59, y:0-14) ou '.' pour terminer")
    while True:
        mvt = input()
        if mvt == ".":
            print ("Merci pour jeu")
            sys.exit()
        mvt = mvt.split()
        if len(mvt) == 2 and mvt[0].isdigit() and mvt[1].isdigit():
            if [int(mvt[0]),int(mvt[1])] in avantMvt:
                print ("Vous avez déjà déménagé là-bas")
                continue
            return [int(mvt[0]),int(mvt[1])]

def main():
    print ("SONAR \n")
    while True:
    #jeu installer
        sonar = 20
        grille = creatGrille()
        tresor = creatRandomTresor(3)
        dessinGrille(grille)
        avantMvt = []
        while sonar > 0:
            print ("Vous avez %s sonar et %s tresor trouve"%(sonar,len(tresor)))
            x, y = entreMvt(avantMvt)
            avantMvt.append([x,y])
            mvtResultat = Deplace(grille,tresor,x,y)
            if mvtResultat == False :
                continue
            elif mvtResultat == "Vous avez trouve un tresor":
                for x,y in avantMvt:
                    Deplace(grille,tresor,x,y)
                dessinGrille(grille)
                print (mvtResultat)
            if len(tresor) == 0:
                print ("Vous avez trouve tous les tresors")
                break
            sonar -= 1
        if sonar == 0:
            print ("Jeu terminé")
            print ("Tous les tresors sont ici:")
            for x,y in tresor:
                print ("%d %d "%(x,y))
        print ("Vous voulez continue? (oui - non)")
        if not input().lower().startswith("o"):
            sys.exit()

main()