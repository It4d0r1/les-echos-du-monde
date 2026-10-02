# Brushes WorldEdit — chemins, place, flore et arbres du village

Ces configurations utilisent les commandes de WorldEdit 7.3. WorldEdit 7.3.8 a été trouvé dans le profil Pixelmon Les Échos du Monde. Les commandes ont été vérifiées dans la documentation officielle ; elles n'ont pas été exécutées dans Minecraft.

## Préparer les outils

Prendre un bâton pour les chemins, une tige de blaze pour la place, une plume pour la flore et un os pour les arbres. Tenir l'objet concerné pendant la saisie de ses commandes : le brush est associé à cet objet. Il s'utilise ensuite par clic droit sur le terrain.

Les brushes des chemins et de la place travaillent sur les blocs d'herbe ou de terre qui ont de l'air immédiatement au-dessus. Retirer les fleurs et les herbes du tracé avant de peindre. Le masque ne remplace pas les blocs en bois, les pierres des bâtiments, les blocs de structure ou l'air. Il peut toucher un jardin en herbe ou en terre si celui-ci se trouve dans la zone du clic.

## Chemins — mélange de terre et de gravier

Tenir le bâton, puis saisir les commandes séparément :

```text
/brush sphere 45%gravel,25%coarse_dirt,20%andesite,10%cobblestone 2
/mask "grass_block,dirt <air"
```

Le rayon 2 donne un tracé d'environ 5 blocs de large sur un sol plat. Avancer le long du parcours en faisant des clics proches. Le mélange comprend environ 45 % de gravier, 25 % de terre stérile, 20 % d'andésite et 10 % de pierres. Tous ces blocs ont une hauteur complète.

La forme suit le relief existant ; ce brush n'aplanit pas le terrain. La largeur peut varier sur une pente.

Pour une ruelle plus étroite, tenir le bâton et saisir :

```text
/size 1
```

Pour un chemin principal plus large :

```text
/size 3
```

## Place du village — pavage en pierre

Tenir la tige de blaze, puis saisir les commandes séparément :

```text
/brush sphere 50%stone_bricks,30%andesite,15%cobblestone,5%cracked_stone_bricks 5
/mask "grass_block,dirt <air"
```

Chaque clic couvre environ 11 blocs de diamètre sur un sol plat. Des clics voisins permettent de dessiner une place plus grande. Le mélange comprend environ 50 % de pierre taillée, 30 % d'andésite, 15 % de pierres et 5 % de pierre taillée craquelée.

Préparer une surface plane si la place doit être plate : le brush conserve les niveaux existants. Poser les bordures, marches et dalles ensuite à la main pour garder leur orientation.

## Place ronde avec //cyl

Sur un sol plat, `//cyl` permet de réaliser la place en une opération. Utiliser une hauteur de 1 pour une seule couche. Sans réglage de placement, le cylindre commence au niveau des pieds du joueur ; pour remplacer le sol à son niveau actuel, choisir le bloc central du sol comme origine :

1. Regarder le bloc du sol au centre souhaité, puis saisir `//hpos1`.
2. Saisir `/toggleplace`. Vérifier que le message indique que le placement utilise le premier point de sélection, ou `pos1`. Si le message indique la position du joueur, saisir de nouveau `/toggleplace`.
3. Exécuter les trois commandes ci-dessous séparément.

```text
//gmask "grass_block,dirt <air"
//cyl 50%stone_bricks,30%andesite,15%cobblestone,5%cracked_stone_bricks 8 1
//gmask
```

Le rayon 8 donne une place d'environ 17 blocs de diamètre ; la hauteur 1 remplace une seule couche. Changer 8 pour modifier le rayon. Le résultat reste au même niveau Y : il ne suit pas les pentes.

Le masque global limite l'opération aux blocs d'herbe et de terre ayant de l'air au-dessus. Il conserve les autres matériaux, qui peuvent donc laisser des interruptions dans le disque. Le masque local `/mask` du brush ne s'applique pas à `//cyl`. La dernière commande efface le masque global temporaire.

Après l'opération, saisir `/toggleplace` pour revenir au placement à la position du joueur, en vérifiant le message. Utiliser `//undo` pour annuler le cylindre si nécessaire.

## Flore — herbe et petites fleurs

Tenir une plume, puis saisir les commandes séparément :

```text
//gmask
/brush sphere 60%short_grass,10%fern,10%dandelion,10%poppy,5%cornflower,5%oxeye_daisy 4
/mask "air >grass_block %25"
/tracemask #solid
```

La première commande efface un éventuel masque global, notamment celui utilisé pour `//cyl`. Le brush a un rayon de 4 blocs. Faire un clic droit en visant le gazon pour ajouter un mélange d'herbe courte, de fougères, de pissenlits, de coquelicots, de bleuets et de marguerites.

Le masque exige un emplacement vide directement au-dessus d'un bloc de gazon. `%25` limite la plantation à environ 25 % des emplacements admissibles par passage. Les chemins en gravier, terre stérile, andésite ou pierres ne sont pas des supports autorisés ; les plantes déjà présentes ne sont pas remplacées. Le filtre de visée `#solid` permet de viser le sol à travers les petites plantes.

Les plantes utilisées occupent toutes un seul bloc : aucune moitié supérieure de grande fleur n'est à ajouter.

Pour une zone plus fleurie, tenir la plume et remplacer le masque par :

```text
/mask "air >grass_block %50"
```

Un nouveau passage peut ajouter des plantes dans les emplacements encore libres ; limiter les clics répétés pour garder un aspect aéré. Utiliser `//undo` pour annuler la dernière opération.

## Arbres — brush pour les espaces libres

Tenir un os, puis saisir les commandes séparément :

```text
//gmask
/brush forest sphere 6 3 oak
/mask
/tracemask #solid
```

Faire un clic droit sur une zone de gazon dégagée pour tenter d'y générer des chênes complets. Le rayon de la zone de plantation est de 6 blocs. La densité 3 correspond à une probabilité de tentative de plantation de 3 % aux emplacements parcourus ; elle ne signifie pas trois arbres par clic. Selon la place disponible et les conditions de croissance, un clic peut ne produire aucun arbre.

Les commandes `//gmask` et `/mask` effacent respectivement le masque global et le masque du brush. Ne pas conserver le masque de la flore `air >grass_block %25` : il empêcherait la pose normale des troncs et des feuilles en hauteur. La taille des arbres est déterminée par le générateur Minecraft ; les feuilles peuvent dépasser la zone de plantation. Laisser de l'espace autour des maisons et des chemins.

Pour changer d'essence, tenir l'os et utiliser l'une de ces commandes :

| Essence | Commande |
| --- | --- |
| Chêne | `/brush forest sphere 6 3 oak` |
| Bouleau | `/brush forest sphere 6 3 birch` |
| Sapin | `/brush forest sphere 6 3 spruce` |

Augmenter la densité, par exemple de 3 à 8, augmente le nombre de tentatives. Commencer avec un seul clic, regarder le résultat et utiliser `//undo` avant d'ajuster si nécessaire.

### Un arbre à un emplacement précis

Pour placer les arbres près du village un par un, tenir l'os et saisir :

```text
//gmask
/tool tree oak
```

Faire un clic droit directement sur le bloc de gazon où planter le chêne. L'outil utilise le générateur Minecraft et nécessite un sol adapté ainsi que suffisamment d'espace. Remplacer `oak` par `birch` ou `spruce` pour changer d'essence.

Cette commande remplace le brush forêt associé à l'os. Pour revenir au brush forêt, reprendre ses commandes de configuration ci-dessus. Pour retirer l'outil arbre de l'os, saisir `/tool none` en le tenant.

## Ordre de travail

1. Préparer le sol et retirer les plantes du tracé.
2. Peindre la place centrale avec la tige de blaze.
3. Tracer les chemins depuis les sorties de la place avec le bâton.
4. Raccorder les chemins aux entrées des bâtiments et ajouter les bordures.
5. Planter les arbres dans les espaces libres avec l'os, puis ajouter la flore avec la plume.
6. Exporter la plateforme avec ses chemins, sa place, ses arbres et sa flore dans le nouveau NBT. Inclure toute la hauteur des arbres et leurs feuilles dans la sélection.

Les matériaux produits par les brushes des chemins et de la place ne font pas partie de leur masque d'entrée. Un nouveau clic conserve donc les zones déjà peintes et travaille sur l'herbe ou la terre encore présente. Cela évite de modifier le mélange à chaque passage.

## Annuler ou retirer un brush

Annuler la dernière opération WorldEdit :

```text
//undo
```

Retirer le brush de l'objet actuellement tenu :

```text
/brush none
```

Si aucun bloc ne change alors que le sol est bien en herbe ou en terre avec de l'air au-dessus, vérifier les autres masques actifs. Un masque global se cumule avec le masque du brush. Pour effacer un ancien masque global :

```text
//gmask
```

## Contrôle dans Minecraft

Faire un premier clic sur une petite zone libre. Pour les chemins et la place, vérifier que seule la surface est remplacée, que la largeur convient et que le relief est conservé. Pour la flore, vérifier que les plantes reposent sur le gazon, que la densité convient et que les chemins restent libres. Pour les arbres, vérifier que les troncs et les feuilles sont complets, que la densité convient et que les entrées des bâtiments restent accessibles. Utiliser `//undo` si nécessaire avant de poursuivre. Aucun contrôle en jeu n'a encore été réalisé par Codex.

## Références

Pour retrouver ce guide dans Gitling et lire les commandes avec Markor, consulter [Lire les commandes sur Android](LIRE_LES_COMMANDES_SUR_ANDROID.md).

- [Brushes WorldEdit 7.3](https://worldedit.enginehub.org/en/7.3.19/usage/tools/brushes/)
- [Outil de génération d'arbres](https://worldedit.enginehub.org/en/7.3.19/usage/tools/tools/#tree-generation-tool)
- [Commande du brush forêt dans le code de WorldEdit 7.3.8](https://github.com/EngineHub/WorldEdit/blob/7.3.8/worldedit-core/src/main/java/com/sk89q/worldedit/command/BrushCommands.java)
- [Noms des essences dans WorldEdit 7.3](https://github.com/EngineHub/WorldEdit/blob/version/7.3.x/worldedit-core/src/main/java/com/sk89q/worldedit/util/TreeGenerator.java)
- [Mélanges de blocs](https://worldedit.enginehub.org/en/7.3.19/usage/general/patterns/)
- [Masques et condition de surface](https://worldedit.enginehub.org/en/7.3.19/usage/general/masks/)
- [Génération de cylindres](https://worldedit.enginehub.org/en/7.3.19/usage/generation/)
