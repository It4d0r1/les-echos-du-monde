# Les Échos du Monde — prologue

Datapack pour Minecraft Java 1.21.1 / NeoForge. Identifiant : `les_echos_du_monde`.

## Chargement automatique

Le datapack est installé dans `global_packs/required_data/les_echos_du_monde`. La configuration actuelle de GlobalPacks inclut déjà `global_packs/required_data/` dans les datapacks obligatoires. OpenLoader est présent et activé pour les datapacks, mais aucun emplacement additionnel ne lui est nécessaire. Aucun mod ou fichier `.jar` n’a été ajouté ou modifié.

## Coordonnées et fichiers à régler

- **Arrivée dans le prologue** : `data/les_echos_du_monde/function/player/first_join.mcfunction` — `tp @s 0.5 -4 0.5`.
- **Position de la carte copiée** : `data/les_echos_du_monde/function/world/place_platform.mcfunction` — la commande `place template` place la structure avec son centre horizontal proche de `(0, 0)`. L’ancrage choisi aligne le sol repéré à la coordonnée locale `(224, 51, 243)` sur le bloc du monde `(0, -5, 0)`.
- **Fichier de carte** : `data/les_echos_du_monde/structure/plateforme_prologue.nbt` — export Axiom, boîte de structure de `449 × 93 × 486` blocs, environ 4,95 millions de blocs.
- **Zone de sortie** : `data/les_echos_du_monde/function/tick.mcfunction` — boîte `x=-1..1, y=-4..-2, z=6..8`. Ajuste le sélecteur à l’emplacement réel de ta sortie.
- **Arrivée Overworld** : `data/les_echos_du_monde/function/player/exit.mcfunction` — `tp @s 0.5 80 0.5` (provisoire; remplace par l’emplacement du village de Garrick).
- **Spawn Overworld après une mort** : `data/les_echos_du_monde/function/world/initialize.mcfunction` — `setworldspawn 0 80 0` et `gamerule spawnRadius 0` (provisoire).

Les téléportations utilisent `.5` sur X/Z pour centrer le joueur sur le bloc. Le terrain repéré dans l’export a son sol central au niveau local Y=51; l’origine choisie le place au niveau Y=-5 pour que le joueur arrive à Y=-4.

## Fonctionnement et limites

Le datapack crée la dimension `les_echos_du_monde:prologue`, générée comme un vide. Au chargement du datapack, il tente de placer la structure Axiom une seule fois par sauvegarde et n’enregistre le marqueur que si la commande confirme le placement. En cas d’échec, le joueur reçoit un message en jeu. Au premier tick où un joueur est présent, une fonction lui ajoute le tag persistant `edm_prologue_done` puis le téléporte au-dessus du terrain copié. Le tag n’est pas retiré à la sortie, à la reconnexion ou à la mort : ces événements ne relancent donc pas l’arrivée.

La sortie est vérifiée chaque tick uniquement dans la dimension du prologue. Entrer dans la boîte définie dans `tick.mcfunction` téléporte vers l’Overworld. La position par défaut de cette boîte est provisoire et doit correspondre à la sortie construite dans la carte.

Minecraft Java ne choisit pas intentionnellement un village comme point d’apparition; la proximité peut être fortuite. Le datapack fixe le spawn mondial à `(0, 80, 0)` et met `spawnRadius` à `0`, ce qui retire la dispersion des réapparitions. Cela ne désactive pas la génération des villages.

Les datapacks qui ajoutent des dimensions doivent être présents dès la création du monde. Pour un monde existant, crée une nouvelle sauvegarde de test avec le pack activé; ne compte pas sur `/reload` pour enregistrer la nouvelle dimension dans une sauvegarde ancienne. La structure est volumineuse : teste d’abord dans un monde jetable et laisse le jeu finir de charger avant de juger le premier démarrage.
