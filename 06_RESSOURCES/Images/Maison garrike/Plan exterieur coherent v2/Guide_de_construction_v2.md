# Maison de Garrik - plan extérieur cohérent v2

Statut : reconstruction proposée à partir de l’image fournie. Les coordonnées sont celles d’un modèle unique, pas des mesures extraites de la photographie. Aucune vérification en jeu n’a été effectuée.

## Comment lire le plan

- Une case représente une cellule de bloc, pas un pixel décoratif.
- X augmente de gauche à droite lorsqu’on regarde la façade principale ; Z augmente de l’entrée vers l’arrière ; Y augmente vers le haut.
- Les murs occupent X=0..24 et Z=0..16 : 25 × 17 blocs. Leur sommet rectangulaire est à la hauteur 10.
- Le toit principal et le grand pignon occupent X=-1..25 et Z=-1..17 : enveloppe de 27 × 19 blocs, avec un débord d’un bloc.
- Le bloc le plus haut du faîtage est placé en Y=18 : son sommet est à la hauteur 19. Les cheminées se terminent en Y=22 : sommet à 23.
- La première marche est en Y=-1, sous le niveau de référence du socle. Préparer le terrain en conséquence.
- Les façades sont des projections du même modèle. Sur la façade arrière, X se lit de droite à gauche ; sur le côté gauche, Z se lit de droite à gauche.
- Les pages de couches gardent l’entrée en bas et X croissant vers la droite. Les pointillés indiquent l’emprise des murs, pas une cloison intérieure.

## Ordre de construction

1. Réserver les 25 × 17 blocs des murs et le débord du toit. Prévoir aussi le perron jusqu’à Z=-4 ; le jardin et la clôture sont à choisir autour de cette emprise.
2. Poser les couches Y=-1 à 4 : première marche, socle, maçonnerie, ouvertures et porte d’entrée. Ne pas remplir le centre : ce dossier représente seulement l’enveloppe extérieure.
3. Poser Y=5 à 9 : colombages, fenêtres du niveau supérieur, jardinières et auvent. Les vitres peuvent être réalisées en blocs ou panneaux selon le rendu recherché.
4. Poser Y=10 à 18 : pignons, toiture et lucarnes selon les couches. Les flèches des cellules d’escalier désignent leur côté haut ; elles ne désignent pas le nord. Les cellules H sont du bois plein, pas des demi-dalles. Aux croisements de toit, suivre la couche plutôt que prolonger chaque pente indépendamment.
5. Poursuivre les deux cheminées jusqu’à Y=22. Les cellules C occupent X=2..3 et X=21..22, avec Z=11..12. Elles traversent le toit ; une cellule ne reçoit jamais deux matériaux.
6. Ajouter les lanternes, bannières et végétation. Les cellules de végétation indiquent un volume décoratif à adapter avec feuilles, fleurs et jardinières. Ne pas compter ces éléments comme des dimensions du bâtiment.

## Ce qui est conservé et ce qui est choisi

La référence guide la silhouette, le grand pignon avant à gauche, la petite lucarne à droite, les deux niveaux, la pierre, le bois, les fenêtres, le porche, les lanternes et la végétation. Elle ne donne pas de mesures fiables et ne permet pas d’imposer un raccord de toiture unique. Les dimensions, la grille, les coordonnées des ouvertures et le placement exact des deux cheminées sont donc des choix de reconstruction, explicitement proposés.

Le toit est composé d’un toit principal à deux pentes (axe Z=8, hauteur 17), d’un grand pignon avant transversal (axe X=7, hauteur 19), d’une lucarne avant (axe X=20) et d’une lucarne arrière (axe X=12). La hauteur du grand pignon décroît derrière Z=4 pour se raccorder au toit principal. Le même calcul de surface sert aux quatre façades, à la vue du dessus et aux couches.

La clôture, le portail et l’allée du jardin sont des aménagements extérieurs libres ; ils ne sont pas cotés faute d’échelle fiable sur la référence. Aucun intérieur ni mobilier n’est défini.

## Matériaux

Les quantités ci-dessous comptent les cellules du modèle, avec les parties cachées de l’enveloppe. Ce sont des repères pour la construction : D compte séparément la moitié basse et la moitié haute d’une porte, V regroupe plusieurs possibilités de décoration ; ce n’est donc pas une liste exacte d’objets à collecter en survie.

| Code | Matériau | Cellules |
|---|---|---:|
| S | Pierre de fondation | 164 |
| B | Poutres en bois | 483 |
| P | Planches en bois | 27 |
| E | Enduit clair | 58 |
| G | Vitres | 289 |
| D | Portes : partie basse / haute | 4 |
| R | Escaliers de toiture | 498 |
| H | Bois plein : faîtage | 48 |
| C | Pierre des cheminées | 80 |
| L | Lanternes | 9 |
| V | Feuillage et jardinières | 47 |
| N | Bannières décoratives | 6 |
| A | Escaliers du perron | 8 |

## Vérifications réalisées

- Unicité des coordonnées : aucun doublon.
- Mêmes positions et mêmes matériaux dans toutes les projections.
- Sommet du toit à 19, cheminées à 23, emprise des murs 25 × 17 et enveloppe de toiture 27 × 19.
- 24 couches couvrent intégralement le modèle, de Y=-1 à Y=22.
- Le CSV répertorie chaque cellule et la direction du côté haut de chaque escalier.

Ces contrôles vérifient la cohérence du modèle. Ils ne démontrent pas une reproduction exacte de l’image ni un résultat testé dans Minecraft.
