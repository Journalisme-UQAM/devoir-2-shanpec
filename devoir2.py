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
