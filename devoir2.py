#coding: utf-8

#CONSIGNES : https://github.com/jhroy/syllabus-edm5240-H2017/blob/master/devoir2.md

#Je tiens à remercier Sydney Armand, mon colocataire, qui m'a fortement aidé dans la rédaction de ce script.

#On importe le module csv pour pouvoir interagir avec le fichier .csv qui va nous servir de base de travail pour ce devoir.
import csv
#J'importe le module re puisque nous allons nous servir d'expressions régulières dans la 3ème partie de ce devoir.
import re

#Déclaration de la fonction de traduction des chiffres romains en integer (trouvé en intégralité sur stackoverflow)
def rom_to_int(value):
    s = 0;
    a = dict();
    b = dict();
    r = value;
    
    a['CM'] = 900;
    a['IX'] = 9;
    a['IV'] = 4;
    a['XL'] = 40;
    a['CD'] = 400;
    a['XC'] = 90;
    
    b['M'] = 1000;
    b['C'] = 100;
    b['D'] = 500;
    b['X'] = 10;
    b['V'] = 5;
    b['L'] = 50;
    b['I'] = 1;
    
    # Handle the tricky 4's and 9's first and remove them from the string
    
    for key in a:
            if key in r:
                r = re.sub(key,'',r)
                s+=a[key];
    # Then straightforward multiplication of the not-so-tricky ones by their count.
    
    for key in b:
             s+= r.count(key) * b[key];
    
    return s 
    #s sera le chiffre romain sous forme d'integer, donc la solution que nous cherchions


#On lie le fichier concordia1.csv au script devoir2.py
fichier="concordia1.csv"
concordia=open(fichier)
# lignes=concordia.readlines() 
#Après l'avoir testée, cette ligne fonctionne mais trop bizarrement pour être exploitée correctement. Nous utiliserons celle ci-après:
lignes=csv.reader(concordia)

# On utilise la commande ci-dessous pour ignorer la première ligne de titres de colonnes
next(lignes)


#On stock dès maintenant le titre du papier et les nom/prénom de chacun dans des listes distinctes pour une utilisation dans le print final
titre=[]
nom=[]
prenom=[]

for ligne in lignes:
    titre.append(ligne[2])
    nom.append(ligne[0])
    prenom.append(ligne[1])
# print(titre)
    

#On remet le curseur de lecture du fichier à la position 0 et on évite l'entête qui contient les titres des colonnes dans le csv
concordia.seek(0)
next(lignes)


#I) LONGUEUR du TITRE
#le titre se trouve à la 3ème ligne, donc la colonne 2 du fichier

longTitre=[]
#On ajoute la longueur en nombre de caractères de ce que contient la colonne title, c'est-à-dire ligne[2]
for ligne in lignes:
    longTitre.append(len(ligne[2]))
#print(longTitre)

#On remet le curseur de lecture du fichier à la position 0 et on évite l'entête qui contient les titres des colonnes dans le csv
concordia.seek(0)
next(lignes)


#2) MÉMOIRE ou THÈSE ?
#À partir de la colonne thesis_degree_name, s'il s'agit d'une maîtrise ou d'un doctorat = colonne 7, donc 6
#On créé une liste vide où sera rangé le type de chaque papier dans l'ordre, appelée moud pour "Maîtrise ou Doctorat"
moud=[]
for ligne in lignes:
    #On demande d'écrire Doctorat à chaque fois que le script voit un de ces cas-là dans la colonne thesis_degree_name.
    #Il y a plusieurs cas pour les doctorats, car la manière d'écrire dans le document que c'en est un n'est pas régulière (Ph. D., PhD, Ph.D., Ph.D, D. Eng)
    if "D." in ligne[6]:
        moud.append("Doctorat")
    elif "PhD" in ligne[6]:
        moud.append("Doctorat")
    elif "Ph.D" in ligne[6]:
        moud.append("Doctorat")
    #Les maîtrises ne sont désignées que par un "M." dans la colonne thesis_degree_name,et il n'y a pas d'erreur de typo pour ce cas là. 
    elif "M." in ligne[6]:
        moud.append("Maîtrise")
    else:
        moud.append("WAT")
        print(ligne) 
        #Cette ligne fait que si le script voit quelque chose n'est pas compris dans les conditions ci-dessus, 
        #il m'affiche la ligne problématique pour que je vois moi-même ce qui ne va pas.
# print(moud)



#3) NOMBRE de PAGES
#à partir des informations contenues dans la colonne pages_aacr, soit la colonne 6, donc la 5
# nombre Romain + nombre Arabe = nombre Total

#pour transformer des chiffres romains en chiffres : http://stackoverflow.com/questions/19308177/converting-roman-numerals-to-integers-in-python


# On remet le curseur de lecture du fichier à la position 0 et on évite l'entête qui contient les titres des colonnes dans le csv
concordia.seek(0)
next(lignes)


#Ceci est une tentative inachevée d'utiliser la fonction search() du module re, avec des expresions réguilières, à partir de tutoriels trouvés sur le net. 
# for ligne in lignes:
    # m=re.search(\^([0-9])\d+\g,ligne[5])
    # print(m)


#On créé la liste, pour l'instant vide qu'on va remplir par la suite.
nbPages=[]

for ligne in lignes:
    n=ligne[5] #J'itère sur la colonne pages_aacr du csv
    #On commence par séparer la ligne qui contient le nombre de pages en deux cases de tableau distinctes.
    #On coupe, grâce à une fonction qui contient des expressions régulières, à l'endroit de, suivant le cas, "leaves", "p.", "l." ou ":"
    autourdeLeaves=re.split("leaves|p\.|l\.|:", n)
    #La seule valeur qui nous intéresse est la première de ce qu'on a obtenu en sortie du re.split. La seconde valeur est justement tout ce qui ne nous intéresse pas dans la ligne de la colonne pages_aacr
    brutPages=autourdeLeaves[0]
    #Dans la valeur brutPages, nous avons toujours 2 informations dans le même string, et qui ne sont donc pas indépendantes l'une de l'autre. 
    #Comme elles sont séparées par une virgule, on les split à l'endroit de la virgule.
    netPages=brutPages.split(",")
    if len(netPages)==2:
        #Là, on est dans le cas où on a des chiffres romains et où il va falloir les gérer.
        #On utilise donc la fonction rom_to_int qu'on a défini au début de ce script.
        traduit=rom_to_int(netPages[0])
        #On vient de traduire le chiffre romain, qu'on a appelé «traduit»
        #Maintenant on créé la varaible netPagessansesp, qui est «le nombre de pages sans espace dedans», grâce à la fonction .strip()
        netPagessansesp=netPages[1].strip()
        if netPagessansesp.isdigit() is False:
            #Ici, on utlise un dispositif de sécurité pour les cas (qui existent dans le csv) où l'écriture ne respecte pas ce standard : «[chiffres romains si nécessaire], [chiffres arabes] ["leaves" ou "p." ou "l." ou ":"]».
            #Pour ce faire, on utlise la fonction isdigit(), qui permet de vérifier si le string est entièrement composé de chiffres. A cette étape-ci, netPagessansesp est censée être composé de chiffres si tout va bien.
            #Si cette valeur n'est pas composée uniquement de chiffres, c'est que tout ne va pas bien et que le script ne peut pas gérer ce cas.
            #Certains cas de nombre de pages ne sont pas clairs quand au nombre de pages, même pour un humain. On met alors un "Non valide" dans la liste.
            nbPages.append("### (Non Valide parce que : {})".format(n))
        else:
            #nbrPages est toujours un string à ce niveau. Pour pouvoir l'aadditionner à traduit
            nbrPages=int(netPagessansesp)
            #On ajoute traduit et nbrPages, afin d'avoir le nombre total 
            total=traduit+nbrPages
            nbPages.append(total)
            #Et on ajoute ce total de pages à notre liste du début.
    elif len(netPages)==1:
        #Nous sommes dans le cas où il n'a pas de chiffre romain. Dans netPages, nous n'avons alors que le nombre de pages, avec potentiellement un ou des espace(s).
        netPagessansesp=netPages[0].strip()
        #Grâce à la fonction strip(), on enlève les espaces éventuels qui auraient pu arriver dans la création de netPages[0]
        if netPagessansesp.isdigit() is False:
            #Comme plus haut, on insère un message d'erreur si le cas n'est pas traitable par le script.
            nbPages.append("### (Non Valide parce que : {})".format(n))
        else:
            #netPagessansesp est encore un string, et il faut le transformer en integer
            nbrPages=int(netPagessansesp)
            nbPages.append(nbrPages)
            #Et on ajoute ce total de pages à notre liste du début.
#Et après tout ça, on a juste le nombre de pages des thèses ou mémoires !

# print(nbPages)


#On remet le curseur de lecture du fichier à la position 0 et on évite l'entête qui contient les titres des colonnes dans le csv
concordia.seek(0)
next(lignes)


#On regroupe les informations qu'on a obtenu jusque là, pour les afficher dans une phrase.
for index in range(len(longTitre)):
#Pour autant de lignes que d'éléments que comporte longTitre (soit 9153 éléments, comme moud, nbPages, titre, nom, prénom), on va chercher les informations correspondantes à chaque ligne.
#Comme ça, on associe bien le bon titre à la bonne personne, au bon nombre de pages, ...
    currentlongTitre = longTitre[index]
    currentType = moud[index]
    currentnbPages = nbPages[index]
    currentTitre = titre[index]
    currentNom = nom[index]
    currentPrenom = prenom[index]
    print("Le papier de {} de {} {}, appelé «{}» ({} caractères), possède {} pages.".format(currentType, currentPrenom, currentNom, currentTitre, currentlongTitre, currentnbPages ))


#POUR ÉCRIRE LES TRUCS DANS LE CSV À LA FIN
# c=csv.writer(open(fichier2 ,"a"))

# c.writerow("longTitre")
# c.writerow("type")
# c.writerow("nbPages")

#Et c'est enfin terminé ! Après plusieurs jours entiers de très dur labeur !
#Bye !
