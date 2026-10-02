# Végétation du village avec le Script Brush d’Axiom

## Fichier à utiliser

Le script est `AXIOM_VEGETATION.lua`, dans le même dossier que ce guide.

Il ajoute des herbes, des fougères, huit variétés de petites fleurs, des groupes d’azalées et des arbres en chêne, bouleau ou sapin. Les arbres sont des formes construites en blocs vanilla par le script. Les feuilles portent la propriété `persistent=true`.

Le Script Brush d’Axiom utilise du Lua et permet de lire et de poser des blocs avec `getBlock` et `setBlock`. Le code comprend des expressions `$int(...)$`, `$float(...)$` et `$boolean(...)$` : Axiom les transforme en réglages dans la fenêtre **Tool Options**. Ce fichier est destiné à cet éditeur.

## Utilisation

1. Ouvrir la plateforme dans le profil de construction où Axiom fonctionne déjà.
2. Ouvrir `AXIOM_VEGETATION.lua` et copier tout son contenu.
3. Dans Minecraft, passer en mode éditeur Axiom avec **Maj droite**, si la touche par défaut a été conservée.
4. Dans **Tools**, choisir **Script Brush**.
5. Coller le code dans l’éditeur de **Tool Options**.
6. Choisir une forme **Sphere** et un rayon de **4** pour commencer. Laisser le gazon du sol dans le volume du brush : le script part des blocs de gazon.
7. Peindre les espaces verts du village. La flore apparaît au-dessus du sol. Un arbre peut dépasser le rayon du brush, car sa forme est calculée autour de son point de plantation.
8. Enregistrer ce réglage dans les **Tool Presets** pour le retrouver.

Pour garder un arbre complet, le volume de travail doit englober son tronc et sa couronne. Choisir une zone libre et une sélection assez grande si une sélection est active. Utiliser **History** ou **Ctrl+Z** pour annuler une opération.

## Réglages proposés

| Réglage dans Axiom | Valeur initiale | Effet |
| --- | --- | --- |
| Graine | 101 | Répartition reproductible à partir des coordonnées |
| Flore pourcent | 20 | Probabilité de petite plante sur un emplacement admissible |
| Fleurs pourcent de la flore | 25 | Part des fleurs parmi les petites plantes ajoutées |
| Arbres | Activé | Ajout d’arbres dans les zones admissibles |
| Arbres pourcent | 0,25 | Probabilité de candidature d’un arbre par bloc de gazon |
| Buissons | Activé | Ajout de petites azalées |
| Buissons pourcent | 0,6 | Probabilité de candidature d’un groupe de buissons |
| Hauteur tronc minimum / maximum | 5 / 7 | Hauteur des troncs ; la couronne peut monter un bloc plus haut |
| Marge batiments | 4 | Bordure libre autour des six emplacements réservés |
| Rayon libre arrivee | 5 | Demi-largeur de la zone carrée libre autour du point d’arrivée |

Ces probabilités s’appliquent aux positions admissibles. Elles ne garantissent pas un nombre de plantes ou d’arbres par clic. Une candidature peut être refusée par les protections ou par un manque de place.

Pour ajouter seulement de l’herbe et des fleurs, désactiver **Arbres** et **Buissons**. Pour obtenir davantage d’arbres sur une zone libre, augmenter **Arbres pourcent**, par exemple à **1**.

Le hasard dépend de la position et de la graine. Repasser avec les mêmes valeurs retrouve les mêmes candidatures ; les emplacements déjà occupés sont conservés. Changer la graine permet de proposer d’autres positions. L’ordre des passages peut influencer les arbres qui trouvent suffisamment d’espace.

## Zones protégées

### Arrivée du joueur

La référence est **X = 7, Y = −3, Z = 1**. Avec le rayon initial de 5, le script garde libre de tout ajout la zone **X = 2 à 12**, **Z = −4 à 6**, inclusivement, quelle que soit la hauteur.

Cette protection concerne les ajouts de végétation. Le placement du joueur et l’état du sol relèvent du monde et du datapack.

### Maison de Garrik

Les arbres et les buissons sont exclus de **X = −16 à 31**, **Z = −80 à −33**, inclusivement. Ce rectangle de **48 × 48 blocs** correspond au chunk **X = 0, Z = −4** et à ses huit voisins. Chaque bloc d’une couronne est contrôlé avant sa pose, y compris si le tronc serait situé hors du rectangle.

Les petites herbes et les fleurs restent possibles dans cette zone, en dehors des emplacements réservés aux bâtiments et du point d’arrivée.

### Six bâtiments repérés sur la plateforme

Les limites proviennent du relevé de `plateforme__4.nbt` dans `06_RESSOURCES/Structures_NBT/Vegetation_finale/rapport_verification.json`. L’origine X/Z initiale reprend l’hypothèse **X = −235, Z = −250**. Elle reste provisoire.

| Repère | Limites X du monde | Limites Z du monde |
| --- | --- | --- |
| Jaune | −6 à 20 | 80 à 125 |
| Bleu | −1 à 27 | 54 à 74 |
| Magenta | 70 à 90 | 40 à 60 |
| Noir | 125 à 140 | 62 à 73 |
| Cyan | 40 à 52 | 102 à 114 |
| Rouge | 71 à 92 | 100 à 128 |

Le script ajoute la **Marge batiments** à ces limites. Ces protections fonctionnent également après le retrait des carrés colorés.

Si la plateforme a été collée à une autre position, régler **Origine plateforme X** et **Origine plateforme Z** avec les coordonnées du coin minimum du volume exporté. Ces valeurs déplacent les protections des six bâtiments ; elles ne déplacent pas la carte. Les réserves de Garrik et de l’arrivée restent exprimées directement en coordonnées du monde.

Des contrôles de terrain évitent également les marqueurs colorés encore présents à proximité des ajouts. Pour ajouter une autre réserve, compléter la table `BUILDINGS` du script avec ses limites locales X/Z.

## Comportement et limites

Le point de plantation doit être un bloc de gazon exposé, avec de l’air au-dessus. Les plantes sont posées dans l’air. Les chemins en gravier, pierres, terre stérile ou dirt path servent de bordures à conserver ; le script produit exclusivement des blocs de végétation.

Avant un arbre ou un groupe de buissons, le script examine le sol autour du point choisi, puis tous les blocs de sa forme. Il renonce à cette forme si un emplacement est occupé ou réservé. Cette lecture préalable vise à éviter les troncs incomplets et les feuilles dans les constructions. Le comportement effectif des sélections et masques dépend aussi de l’outil Axiom actif.

Les contrôles autour du sol sont conservateurs : certaines pentes, les abords des constructions et les zones déjà très végétalisées peuvent recevoir peu d’ajouts.

Les fonctions et les réglages utilisés ont été comparés à la documentation officielle d’Axiom. Le script n’a pas été exécuté dans Minecraft : le rendu et le comportement de la version installée restent à observer en jeu.

## Références

- [Script Brush : Lua, accès aux blocs et réglages](https://axiomdocs.moulberry.com/tools/painting/scriptbrush.html)
- [Mode éditeur et touche d’ouverture](https://axiomdocs.moulberry.com/editor/intro.html)
- [Tool Options](https://axiomdocs.moulberry.com/editor/windows/tooloptions.html)
- [Historique des modifications](https://axiomdocs.moulberry.com/editor/windows/history.html)
