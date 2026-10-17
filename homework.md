Donné le 12 09

Créer un fichier de classe Inventory contenant une liste d'items, une longueur, des fonctions ( add, remove, select, get_selected_item ).

A la création d'un personnage, initialiser un nouvel inventaire.

-----------------------------

Créer une classe Potion, créer une instance 'potion de vie', l'ajouter a l'inventaire, ajouter l'arme de base dans l'inventaire.


-----

Créer une classe Item Qui va permettre aux potions et aux armes d'en hériter. Ajoutez une fonction dans la classe item qui permet de dessiner Et qui sera appelé par l'inventaire afin de dessiner à la fois les potions et les armes en fonction des emplacements qu'ils occupent.

Modifier dans l'affichage de l'inventaire La couleur de la case actuellement sélectionnée pour que le joueur soit au courant De quelles armes Ou qu'elle slot est actuellement activé.

----------------

Mousescrollup, Mousescrolldown qui va faire bouger la selection du personnage ( si potion selectionné, afficher le nombre ( comme actuellement ) sinon rien ), l'attaque va donc pouvoir se trigger uniquement si l'arme est selectionnée.

Afficher l'inventaire sous la forme de petits carrés gris avec les items dedans ( faire une fonction display dans la classe Inventory qui pourra êtr appelé par main_game )

-------

Nous faisons face à un nouveau problème dans notre classe Item, Ils ne trouvent pas L'image d'un objet.
Il faut impérativement tester si l'image existe pour pouvoir l'afficher , De plus actuellement le programme Affiche Ou cherche à afficher toutes les images de ton inventaire même si l'item n'existe pas à la position i

Il y a donc 2 actions à effectuer :
- Regardez si un item existe à la position I pour lancer le dessin
- Tester si l'item en question a bien une image À afficher, Et si c'est pas le cas on le dessine pas

Modifier dans l'affichage de l'inventaire La couleur de la case actuellement sélectionnée pour que le joueur soit au courant De quelles armes Ou qu'elle slot est actuellement activé.




ligne 428-429

Continuer à créer Les classes de drop jusqu'à l'affichage des drops sur l'écran.
Drop manager va appeler l'affichage des drop Qui va appeler l'affichage des items Pour que ça apparaisse sur le screen.
Il faudra ensuite gérer en fonction de la taille de l'image et la position du drop Une manière de récupérer le drop dans l'inventaire par le personnage

Petite chose : Corriger le sélecteur jaune en fonction de l'objet sélectionné dans l'inventaire , Enquêter sur la place de l'Admin Dagger dans l'inventaire