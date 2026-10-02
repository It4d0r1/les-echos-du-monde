# Génération des segments de la plateforme 17

Les fonctions sont produites par `build_functions.py` à partir de
`segments_manifest.json`. Le script reçoit le dossier du datapack préparé via
`--pack`; il n'ouvre aucune sauvegarde Minecraft et n'installe rien dans le profil.

## Intégration

- L'initialisation d'un **nouveau monde** doit enregistrer
  `les_echos_du_monde:state {platform_layout:"segments_v17"}`.
- La fonction principale `load` appelle
  `les_echos_du_monde:world/segments_v17/setup`.
- La fonction principale `tick` appelle
  `les_echos_du_monde:world/segments_v17/tick`.
- La première téléportation attend
  `les_echos_du_monde:segments_v17 {spawn_ready:1b}`.
- Le point d'arrivée doit être défini dans le helper commun
  `les_echos_du_monde:player/teleport_to_prologue`.
- Les anciens mondes avec un autre `platform_layout` sont bloqués. Modifier le
  nom du layout dans une ancienne sauvegarde ne constitue pas une migration sûre.

## Fonctionnement

Chaque cellule représente **2 × 2 chunks**, soit 32 × 32 blocs horizontalement.
Sa hauteur est celle du terrain exporté. Le rayon compilé par défaut est de deux
cellules autour de la cellule occupée, donc quatre chunks dans chaque direction.
Le contrôleur peut couvrir jusqu'à 5 × 5 cellules autour d'un joueur. Il place au
plus un segment toutes les deux ticks, avec un seul segment actif pour le monde.
Les joueurs du prologue sont examinés dans un ordre aléatoire afin de répartir les
placements lorsque plusieurs personnes explorent.

Avant la première arrivée, le contrôleur prépare les neuf cellules autour de
`X=0, Z=0` (indices -1 à 1), en commençant par celle de l'arrivée. Les joueurs non
encore accueillis restent dans l'Overworld pendant cette préparation.

Les scores `edm_seg_done` enregistrent la réussite de chaque segment. Ils ne sont
pas remis à zéro au rechargement du datapack, à la reconnexion ou à la mort.
Les segments terminés ne sont plus placés, ce qui conserve les modifications des
joueurs et les bâtiments ajoutés ensuite.

Le placement est autorisé seulement quand les chunks requis sont chargés. Le
contrôleur attend au plus 100 ticks pour une tentative, puis libère ses tickets.
Après trois échecs, il suspend ce segment et affiche une erreur. Il ne marque la
réussite qu'après le succès de `/place template`.

Les joueurs en survie ou en aventure qui atteignent un segment encore incomplet
ou les limites extérieures de l'export sont ramenés au point d'arrivée prêt. Le
mode créatif et le mode spectateur sont exempts de cette garde, pour la
construction. La garde est coupée quand la génération est désactivée.

## Pourquoi neuf chunks sont temporairement chargés

Le segment reste un carré de **quatre chunks modifiés**. Cependant, la commande
vanilla 1.21.1 `/place template` vérifie le rectangle allant de `pos` à
`pos + template.size`, et non `pos + size - 1`. Une structure de taille 32 × 32
alignée sur les chunks exige donc aussi le bord positif : **3 × 3 chunks chargés**.

Cette différence a été vérifiée dans le bytecode de la classe vanilla
`PlaceCommand.placeTemplate` du fichier local `client-1.21.1-official.jar` :
instructions 60 à 86, appel à `getSize`, `BlockPos.offset` puis `checkLoaded`.
La lecture est archivée dans `PlaceCommand_1.21.1_bytecode.txt`.
Aucun fichier `.jar` d'un mod n'a été modifié.

Le contrôleur ajoute au plus neuf tickets, uniquement sur les chunks qui
n'étaient pas déjà forcés. Il libère uniquement ces tickets à la réussite, à
l'échec, à la désactivation et au rechargement. Il n'utilise jamais
`forceload remove all`. Les tickets existants au début de la tentative sont
conservés.

## Commandes réservées au créateur ou aux administrateurs

```text
/function les_echos_du_monde:world/segments_v17/status
/function les_echos_du_monde:world/segments_v17/disable
/function les_echos_du_monde:world/segments_v17/enable
/function les_echos_du_monde:world/segments_v17/retry_errors
```

`retry_errors` autorise trois nouvelles tentatives sur les segments incomplets.
Il ne supprime pas les scores des segments terminés. `enable` refuse les mondes
qui utilisent un autre layout et respecte la pause globale du prologue.

Les valeurs `generated_settings` du storage sont des **informations de diagnostic**.
Les modifier en jeu ne change pas les fonctions déjà compilées. Pour changer le
rayon, relancer le script avec `--radius 1`, `2`, `3` ou `4`, puis remplacer le
datapack préparé et documenter la nouvelle version. Les valeurs 100 ticks, trois
échecs et une opération toutes les deux ticks sont définies dans le générateur.

## Contrôles à effectuer dans Minecraft

1. Créer un nouveau monde : attendre le prologue dans l'Overworld, puis vérifier
   l'arrivée à `0, -4, 0`, au-dessus du sol et avec deux blocs d'air libres.
2. Marcher vers des cellules éloignées : observer leur apparition, puis vérifier
   qu'un passage trop rapide en survie ramène au point sûr.
3. Modifier un bloc dans un segment terminé, se reconnecter et revenir : le bloc
   doit être conservé. Répéter après fermeture et réouverture du jeu.
4. Vérifier `/execute in les_echos_du_monde:prologue run forceload query` avant,
   pendant et après une tentative : aucun ticket du contrôleur ne doit rester
   après la fin ou la pause. Un ticket ajouté avant une tentative doit rester.
5. Mettre la génération en pause pendant une tentative : vérifier que le segment
   actif est libéré, puis réactiver et vérifier la reprise.
6. Faire approcher deux joueurs du même segment : un seul placement doit avoir
   lieu, sans remise à zéro des scores.
7. Dans une copie de test seulement, provoquer une erreur de template : vérifier
   les trois tentatives au maximum et la libération des tickets. Corriger puis
   utiliser `retry_errors`.
8. Ouvrir un ancien monde : vérifier que son terrain n'est pas remplacé.
9. Vérifier séparément la sortie, la reconnexion après sortie, la mort et la
   réapparition avec le contrôleur d'accueil du datapack.

Ces vérifications en jeu ne sont pas remplacées par l'analyse des fichiers.

## Sources de compatibilité des commandes

- [Notes officielles Minecraft 23w03a : `execute if loaded`](https://www.minecraft.net/en-us/article/minecraft-snapshot-23w03a).
- [Notes officielles Minecraft 22w18a : `place template`](https://www.minecraft.net/en-us/article/minecraft-snapshot-22w18a).
- Classe vanilla locale 1.21.1 `PlaceCommand`, lecture du bytecode uniquement.
