#!/usr/bin/python3


"""
Dans ce TP, on se propose d'implémenter l'algorithme de Huffman en Python.
L'objectif est de compresser efficacement un texte en exploitant le fait que
les caractères aient une fréquence d'apparition loin d'être uniforme.
(Par exemple, le "e" est beaucoup plus fréquent que le "w", donc on va
faire en sorte qu'il prenne moins de place en mémoire.)
"""


def compterOccurences(texte):
    """
    Renvoie une liste qui associe à chaque caractère son nombre d'apparitions.
    Chaque lettre est donc dottée d'un poids (son nombre d'occurences), et
    plus son poids est élevé, plus elle sera légère en mémoire.
    (L'objectif étant ici la compression, donc d'échanger de la puissance
    de calcul contre de l'espace de stockage.)
    """
    lettres = [[0, chr(i)] for i in range(256)]
    for i in texte:
        lettres[ord(i)][0] += 1
    return lettres


def creerArbre(lettres):
    """
    Crée un arbre binaire à partir des lettres et de leur poids.
    On choisit de représenter un arbre de la façon suivante :
      * Une feuille est un 2-uplet : le nombre d'occurences et la lettre
        On notera que compterOccurences renvoie en fait une liste de feuilles.
      * Un noeud est un 3-uplet : la somme des occurences de toutes
        les feuilles descendantes, le fils gauche et le fils droit.
    Ensuite, on construit l'arbre en piochant les deux noeuds de poids
    le plus faible, on en fait un nouveau noeud que l'on remet dans le tas.
    On s'arrête dès qu'il reste un unique noeud (qui est l'arbre voulu)
    """
    # On commence par enlever les lettres qui ne sont pas présentes
    noeuds = [(k, v) for (k, v) in lettres if k > 0]
    # Puis on récupère les deux noeuds (ou feuilles) de poids le plus faible,
    # et on en fait un noeud, de poids la somme des deux petits poids
    # On boucle tant qu'il y a reste au moins deux noeuds
    l = len(noeuds)
    while l >= 2:
        # Indice et noeud des minima des poids
        # (on initialise avec les deux premières valeurs)
        petitMin = (0, noeuds[0])
        grandMin = (1, noeuds[1])
        for i in range(2, l):
            if noeuds[i][0] <= petitMin[1][0]:  # poids < petitMin < grandMin
                grandMin = petitMin
                petitMin = (i, noeuds[i])
            elif noeuds[i][0] <= grandMin[1][0]:  # petitMin < poids < grandMin
                grandMin = (i, noeuds[i])
        nouveauNoeud = (
            petitMin[1][0] + grandMin[1][0],
            noeuds[petitMin[0]],
            noeuds[grandMin[0]]
        )
        # On enlève les deux noeuds (ou feuilles) précedentes
        # et on ajoute le nouveau noeud
        noeuds[petitMin[0]] = nouveauNoeud
        noeuds.pop(grandMin[0])
        # On a au final un noeud de moins (-2 +1)
        l -= 1
    # À cet instant il ne reste plus qu'un noeud, qui est la racine de
    # l'arbre de Huffman
    return noeuds[0]


"""
On remarquera que moins une lettre est présente, plus elle est profonde dans l'arbre.
L'idée maintenant va être d'attribuer à chaque lettre un code en binaire de la façon
suivante :
  * la longueur du code est égale à la profondeur dans l'arbre
  * pour chaque lettre (donc chaque feuille), on part de la racine et on ajoute un 0
    si on prend la branche de gauche, un 1 si on passe par celle de droite.
Ainsi, plus une lettre est fréquente, plus son code binaire est court.
"""


def creerDico(arbre):
    """
    Renvoie un dictionnaire {lettre: code binaire}.
    On va explorer l'arbre à l'aide d'une file : si on rencontre une feuille,
    on la traite, si on rencontre un noeud, on ajoute les deux branches à la file.
    Le premier composant d'un élément de la file est le code binaire jusqu'à cet élément,
    le second est un noeud ou une feuille.
    """
    fileExploration = [("", arbre)]
    dico = {}
    l = 1
    # On boucle tant que la file n'est pas vide
    while l >= 1:
        code, truc = fileExploration.pop(0)  # On défile le premier élément
        l -= 1
        if len(truc) == 2:  # C'est une feuille
            dico[truc[1]] = code  # On ajoute la lettre et son code au dico
        elif len(truc) == 3:  # C'est un noeud
            # On continue l'exploration en respectant la règle pour obtenir le code :
            # Gauche -> 0, droite -> 1
            fileExploration.append((code + "0", truc[1]))
            fileExploration.append((code + "1", truc[2]))
            l += 2
    return dico


def compresser(texte):
    """
    On se contente de remplacer les lettres du texte par le code binaire
    obtenu à l'aide de la fonction creerDico.
    """
    lettres = compterOccurences(texte)
    arbre = creerArbre(lettres)
    dico = creerDico(arbre)
    texteCompresse = ""
    for i in texte:
        texteCompresse += dico[i]
    # On n'oublie pas de renvoyer aussi le dictionnaire,
    # sinon il sera impossible de décompresser le texte
    return texteCompresse, dico


# Par exemple, pour ce texte en "latin" :
texte = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent fermentum aliquam ipsum non vehicula. Sed placerat aliquam aliquet. Donec magna mauris, gravida sed volutpat vitae, molestie at massa. Pellentesque et metus quis lacus tempor placerat. Aliquam erat volutpat. Vivamus dapibus mi nec nisi aliquam, et euismod augue molestie. Nunc interdum."
# On le compresse
texteCompresse, dico = compresser(texte)
print("Avant : {} bits / Après : {} bits".format(len(texte) * 8, len(texteCompresse)))
# Avant : 2816 bits / Après : 1522 bits
# (On rappelle que 1 octet = 8 bits)


"""
On cherche maintenant à décompresser le texte, cependant une nouvelle difficulté
va apparaître :
Par exemple, décompressons "10111" avec le dictionnaire
{"a": "1", "b": "10", "c": "100"}
On commence par remplacer "1" par "a", on a alors "a" + "0111"
Puis on cherche à remplacer le début de "0111" par un caractère mais c'est impossible.
Alors on revient en arrière et on essaie "b", on a alors
"b" + "111", qui se décompresse en "baaa".
On remarquera donc qu'un texte compressé peut se décompresser partiellement mais pas
intégralement si un mauvais caractère est utilisé. On va donc prendre en compte ce
problème en testant toutes les décompressions possibles jusqu'à en trouver une totale.
(La démonstration de l'unicité de la forme décompressée est laissée en exercice.)
"""


def decompresser(texteCompresse, dicoRetourne):
    """
    Décompresse un texte à l'aide de son dico.
    Une fois encore, on utilise une file. C'est un outil très puissant
    qui permet de ne jamais écrire de fonction récursive. Chaque élément
    de la file est un 2-uplet, le premier élément est le texte décompressé
    jusque là, le second est le code binaire restant à décompresser.
    """
    # On retourne le dico
    dico = {v: k for (k, v) in dicoRetourne.items()}
    # Nombre maximum de bits d'un caractère compressé
    limite = max(len(k) for k in dico.keys())
    fileExploration = [("", texteCompresse)]
    l = 1
    while l >= 1:
        fait, restant = fileExploration.pop(0)  # On défile le premier élément
        l -= 1
        # On regarde si la décompression est terminée
        if restant == "":
            return fait
        # Sinon, on tente de remplacer les i premiers bits de restant par un caractère
        i = 0
        bits = ""
        for bit in restant:
            bits += bit
            i += 1
            if i > limite:
                # C'est pas la peine de continuer, bits est trop long
                # pour correspondre à un caractère
                break
            elif bits in dico:
                # On a la possibilité de remplacer quelques 0 et 1 par un caractère
                # alors on le fait, sans pour autant considérer que l'on a choisi
                # le bon remplacement
                fileExploration.append((fait + dico[bits], restant[i:]))
                l += 1
                # Puis on continue à explorer les possibilités
    # Aucune décompression n'a fonctionné, on ne renvoie rien
    return None


if texte == decompresser(texteCompresse, dico):
    print("La décompression a fonctionné")
