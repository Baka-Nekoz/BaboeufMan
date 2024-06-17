--------------------------------------------------------------------------
PRESENTATION DU JEU :

Baboeuf Man est un jeu de plateforme de type shooter dans lequel le joueur incarne Baboeuf, mi-homme, mi-oeuf, 
possédant des armes de guerre et se battant contre des ennemis qui tentent de l'atteindre 
afin de lui infliger des dégats jusqu'à ce qu'il décède. 
Mais Baboeuf est fort, il se bat avec rage et doit faire face le plus longtemps aux hordes de monstres 
rampants, volants, mais aussi bien cachés, tapis dans l'ombre.

---------------------------------------------------------------------------
FONCTIONNEMENT DU JEU :

Le jeu est constitué de plusieurs fichiers python qui ont chachun un rôle :

- main.py, le fichier à lancer pour lancer le jeu.
    C'est le programme central du jeu, il va gérer l'update du jeu à chaque tick et afficher les éléments.
    Il contient une classe Game qui contient :
        display, pour afficher les éléments
        handle_events, qui récupère les données des touches de périphériques (frappes)
        update, qui va recharger le jeu à chaque tick avec les changements

- arm.py, le fichier qui gère le bras de Baboeuf et des ennemis.
    Qui gère le bras, sa rotation, le changement d'arme avec la molette de souris et le tir

- background.py, comme son nom l'indique, gère le fond d'écran.
    R.A.S

- bullet.py, qui gère l'affichage et le mouvement des balles.
    R.A.S

- ground.py, comme son nom l'indique, gère le sol.
    R.A.S

- player.py, gère le joueur.
    Qui gère les déplaements, la gravité, les sauts, et la vélocité des mouvements de Baboeuf.

- pointer.py, qui gère l'affichage de la cible qui suit le pointeur de souris.
    R.A.S

- shooter.py, qui gère un ennemi qui tire.
    En réutilisant des attributs de Baboeuf tels que arm.py

---------------------------------------------------------------------------
LES ASSETS :

Les assets (images et textures) sont stockés dans assets/images et sont des images de types .png
Ces assets correspondent aux balles, bras, armes, ennemis, etc...
