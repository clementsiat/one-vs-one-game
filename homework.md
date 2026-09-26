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