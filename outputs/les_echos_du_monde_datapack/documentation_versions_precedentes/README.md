# Les Échos du Monde — prologue végétalisé

Minecraft Java 1.21.1 / NeoForge. GlobalPacks charge ce dossier dans les datapacks obligatoires.

## Nouveau monde

Relance complètement Minecraft, puis crée un nouveau monde dans l'instance **Pixelmon Les Échos du Monde**. Le joueur attend dans l'Overworld pendant la préparation du prologue; un indicateur affiche le nombre de morceaux placés. Il est ensuite téléporté automatiquement dans `les_echos_du_monde:prologue`, exactement à **X=7, Y=-3, Z=1**.

## Plateforme

La copie végétalisée mesure **562 × 93 × 536**, pour **5 593 060 blocs**. Elle est placée à l'origine **provisoire** `-235 -30 -250`, sans rotation ni miroir. Le sol à l'arrivée est à Y=-4.

Le placement utilise **933 morceaux**, alignés sur les chunks, depuis le chunk `0, 0` vers l'extérieur. Chaque morceau attend que son chunk soit chargé. Un seul nouveau chunk est forcé à la fois; seuls les chargements forcés ajoutés par cette chaîne sont retirés.

Les anciennes structures et fonctions restent conservées, mais le démarrage des nouveaux mondes utilise `structure/prologue_vegetation_chunks` et `function/world/vegetation_chunks`.

La végétation ajoutée respecte les six réserves de bâtiments et leur marge de 4 blocs. Aucun arbre ni buisson ajouté ne pénètre dans la réserve de Garrik : **X=-16..31, Z=-80..-33**, limites incluses. L'origine reste à confirmer visuellement avant de construire les bâtiments définitifs.

## Anciennes sauvegardes

Leur automatisation est mise en pause pour éviter la superposition de modèles ayant des origines différentes. Crée un nouveau monde pour cet essai. Aucun fichier de sauvegarde n'a été modifié pendant l'installation.

## Sortie et réapparition

La sortie provisoire reste `X=-1..1, Y=-4..-2, Z=6..8`. Elle envoie le joueur dans l'Overworld à `0.5 80 0.5`. Le spawn Overworld reste `0 80 0`, avec `spawnRadius=0`. Ces points sont provisoires et ne désignent pas un village vérifié.

## Vérifications

Le découpage a été reconstitué et comparé à la copie complète : mêmes positions, mêmes états, données NBT préservées, aucun bloc manquant ni chevauchement. Les références de fonctions et de modèles ainsi que les messages JSON ont été vérifiés.

**Aucun essai dans Minecraft n'a été effectué.** Voir `TESTS.md` pour l'essai en jeu. Aucun mod ni fichier JAR n'a été ajouté ou modifié.

Sauvegarde complète avant installation :
`C:/Users/Bastien/Desktop/Les Echo du monde/90_ARCHIVES/Sauvegardes_datapack/prologue_vegetation_20261001_175619/datapack`

Rapport et script d'installation :
`C:/Users/Bastien/Desktop/Les Echo du monde/06_RESSOURCES/Structures_NBT/Vegetation_finale/`
