# Plateforme du prologue — utilisation et tests

## Ce qui est prévu

Le datapack `les_echos_du_monde` prépare la plateforme dans la dimension `les_echos_du_monde:prologue`. Il prépare d'abord les segments nécessaires à l'arrivée, puis téléporte automatiquement chaque nouveau joueur une seule fois. Les autres segments se construisent progressivement autour des joueurs présents dans cette dimension.

La source est `06_RESSOURCES/Structures_NBT/plateforme__17.nbt`. Elle est conservée sans modification. Ses dimensions lues dans le fichier sont **451 × 89 × 461 blocs**, dans l'ordre **X, Y, Z**. Ce fichier ne mesure donc pas 300 × 300 blocs. Ses limites verticales ne correspondent pas non plus à la hauteur de 40 blocs déduite des anciens coins fournis.

Le découpage est fait en segments de **32 × 32 blocs horizontalement**, soit **2 × 2 chunks = 4 chunks par segment**. Chaque segment conserve la hauteur de la source. Le rayon choisi par défaut est de **4 chunks autour du joueur**. Ces deux valeurs désignent des choses différentes : la taille d'un segment et la distance de génération.

Chaque segment terminé est enregistré dans les données du monde. Une reconnexion, une mort ou un rechargement du datapack ne doit pas le replacer. Les constructions ajoutées ensuite par le joueur doivent donc rester intactes.

## Coordonnées

Toutes les coordonnées ci-dessous sont données dans l'ordre **X, Y, Z**.

| Élément | X | Y | Z | Explication |
| --- | ---: | ---: | ---: | --- |
| Origine de placement du NBT complet | -250 | -26 | -235 | Coordonnées retenues pour convertir les positions locales du NBT en positions dans le prologue. |
| Arrivée du joueur dans le prologue | 0 | -4 | 0 | Position des pieds du joueur demandée par Bastien. |
| Bloc de sol sous cette arrivée | 0 | -5 | 0 | Le sol doit être une case sous les pieds. La sécurité doit aussi être contrôlée sur les cases voisines touchées par le joueur. |
| Limite minimale de la plateforme | -250 | -26 | -235 | Limite issue de l'origine et des dimensions réelles. |
| Limite maximale de la plateforme | 200 | 62 | 225 | Limite inclusive issue de l'origine et des dimensions réelles. |
| Arrivée dans l'Overworld | 0.5 | 80 | 0.5 | Téléportation au centre du bloc X=0, Z=0 ; point provisoire. Spawn du monde : 0, 80, 0. |

Formule de placement : **position dans le prologue = position locale du NBT + origine de placement**. Il n'y a pas de rotation ni de miroir.

### Où modifier les coordonnées

| Réglage | Fichier ou emplacement final |
| --- | --- |
| Origine de la plateforme et génération des segments | `outputs/prologue_plateforme17/prepare_platform.py` : constante `ORIGIN`, puis reconstruire le NBT, les segments et les fonctions. Utiliser un nouveau monde. |
| Point d'arrivée dans le prologue | `data/les_echos_du_monde/function/player/teleport_to_prologue.mcfunction` : commande `tp @s 0 -4 0`. Les neuf segments préparés au démarrage sont centrés sur X=0, Z=0 dans `build_functions.py` ; les adapter si l’arrivée est déplacée loin. |
| Zone de sortie : coin minimal et dimensions | `data/les_echos_du_monde/function/world/detect_exit.mcfunction` : `x=-1,y=-4,z=6,dx=2,dy=2,dz=2` (zone provisoire X=-1..1, Y=-4..-2, Z=6..8). |
| Point d’arrivée dans l’Overworld | `data/les_echos_du_monde/function/player/exit.mcfunction` : `tp @s 0.5 80 0.5`. |
| Rayon et rythme de génération | `outputs/prologue_plateforme17/build_functions.py` : option `--radius 2` = rayon de 2 cellules de 32 blocs (4 chunks). Rythme, délai maximal et tentatives sont définis dans le générateur ; reconstruire les fonctions après modification. |

Déplacer seulement la commande de téléportation ne déplace pas le terrain. Un changement d'origine exige de recalculer les segments et leurs fonctions de placement. Il faut ensuite utiliser un nouveau monde de test ou une procédure de migration volontaire : les segments déjà terminés ne sont pas automatiquement déplacés.

## Repères et végétation

- Les zones sont enregistrées avant le retrait des repères en béton coloré.
- Le contour marron délimite le village. On y ajoute seulement un peu d'herbe et de fleurs, en gardant dégagés les chemins, l'arrivée et les emplacements réservés aux bâtiments.
- Les autres couleurs délimitent des emplacements réservés aux constructions. On n'y ajoute pas de végétation.
- Aucun arbre ni buisson n'est ajouté. Les arbres et décorations déjà présents dans la source sont conservés. Bastien ajoutera les nouveaux arbres avec des blocs de structure.
- Certains repères gris et gris clair sont enterrés sous le terrain. Ils sont remplacés par de la pierre ou de la terre selon le terrain qui les recouvre, pour éviter de créer des trous. C'est une réparation déduite de leur voisinage : le fichier ne contient pas l'ancien bloc qu'ils ont remplacé.
- Les repères flottants sont retirés. Les blocs colorés qui appartiennent aux décorations existantes ne sont pas assimilés automatiquement à des repères.

## Bâtiments et blocs de structure

Les trois blocs de structure en mode `LOAD` présents dans la source sont préservés, avec les noms suivants :

| Nom de structure | Dimensions X × Y × Z |
| --- | --- |
| `les_echos_du_monde:ferme` | 27 × 22 × 46 |
| `les_echos_du_monde:poke_shop` | 29 × 17 × 21 |
| `les_echos_du_monde:poke_centre` | 22 × 22 × 29 |

Leurs positions de blocs LOAD dans le prologue sont respectivement **(-32, -6, 43)**, **(-27, -6, 17)** et **(45, -5, 63)**, avec un décalage de structure de `(0, 1, 0)`.

Leurs fichiers NBT sont fournis avec le datapack pour rendre ces noms disponibles. La génération de la plateforme ne déclenche pas à elle seule le chargement des bâtiments. La maison de Garrik n'est pas ajoutée sans une source et un placement vérifiés.

Aucun verrouillage lié à FTB Quests n'est ajouté dans cette étape.

## Chargement automatique et anciens mondes

Le datapack doit être installé dans le dossier de données requis de GlobalPacks, pour être chargé automatiquement à la création de chaque monde. OpenLoader reste présent dans le profil ; il ne faut pas installer une seconde copie de ce même datapack dans un autre dossier de chargement.

**Dossier d’installation :** `C:\Users\Bastien\curseforge\minecraft\Instances\Pixelmon Les Échos du Monde\global_packs\required_data\les_echos_du_monde`.

Les mondes qui portent l'identifiant d'une ancienne disposition de plateforme sont protégés : la nouvelle génération y est bloquée. Ce blocage évite de superposer la nouvelle plateforme aux constructions existantes. Il ne faut pas supprimer les états de génération ni forcer la reprise dans ces mondes sans avoir prévu leur migration et leur sauvegarde.

Le point Overworld reste provisoire : cette étape ne crée pas de village, de sol de secours ni de Waystone à cet emplacement. La sécurité de cette arrivée doit être vérifiée en jeu.

## Commandes utiles pour Bastien

Les joueurs du modpack partagé n'ont pas besoin de permission de commande pour la première arrivée, la génération des segments ou la sortie automatique. Les commandes ci-dessous sont destinées au créateur et aux tests.

Ces commandes fonctionnent avec les permissions d’administration habituelles. La génération ne demande aucune commande aux joueurs.

| Action | Commande exacte |
| --- | --- |
| Mettre en pause la génération | `/function les_echos_du_monde:world/pause_automation` |
| Reprendre la génération dans un monde utilisant cette version | `/function les_echos_du_monde:world/resume_automation` |
| Consulter l'état de génération | `/function les_echos_du_monde:world/segments_v17/status` |
| Aller dans le prologue pour inspection | `/function les_echos_du_monde:player/teleport_to_prologue` (attendre `spawn_ready:1b` avant utilisation) |
| Quitter le prologue vers le point provisoire de l'Overworld | `/function les_echos_du_monde:player/exit` |
| Recharger les fonctions après une modification compatible | `/reload` |

La pause concerne la génération du terrain. Un joueur déjà présent doit pouvoir emprunter la sortie automatique même pendant cette pause. La reprise ne doit pas contourner la protection d'un ancien monde.

Pour relancer uniquement les segments en erreur, après avoir corrigé la cause :

```text
/function les_echos_du_monde:world/segments_v17/retry_errors
```

Les valeurs `generated_settings` affichées dans le storage sont des informations ; elles ne modifient pas le rayon ou le rythme en jeu.

## Vérifications de fichiers et tests dans Minecraft

### Vérifications hors jeu

Contrôles réalisés : NBT source inchangé (SHA256), dimensions et DataVersion 3955, **3 905 411 entrées** reconstituées à l’identique depuis **203 segments**, aucun chevauchement ni perte, trois blocs de structure avec données NBT préservées, zéro repère restant, zéro plante ajoutée dans une réserve, zéro arbre ou buisson ajouté. Sol et deux blocs libres contrôlés sur les quatre colonnes touchées par le joueur à **0, -4, 0**. Détail dans `rapport_preparation.json`. Les références des nouvelles fonctions et templates ont été contrôlées.

Les contrôles à consigner sont : dimensions et version du NBT, conservation de la source, retrait des repères, protection des emplacements, conservation des blocs de structure, sécurité de l'arrivée, correspondance des segments et existence de toutes les fonctions et structures référencées.

**Les tests ci-dessous se font dans Minecraft Java 1.21.1 avec le profil NeoForge du modpack. Une inspection des fichiers ne remplace pas un test en jeu. Aucun succès en jeu ne doit être annoncé sans avoir lancé le jeu et observé le résultat.**

### Préparation

1. Fermer Minecraft avant toute installation ou restauration du datapack.
2. Conserver la sauvegarde du datapack précédent. Pour tester un monde existant, conserver également une copie complète de ce monde.
3. Lancer le profil habituel du modpack et créer un **nouveau monde de test**, sans réutiliser un monde ayant l'ancienne plateforme.
4. Faire les essais de joueur sans droits de commande. Utiliser un compte administrateur uniquement pour les contrôles techniques nécessaires.
5. Noter la date, le nom du monde et le résultat de chaque essai. En cas d'échec, garder le journal `logs/latest.log` avant le lancement suivant.

### Scénarios à tester

| N° | Action | Résultat attendu | Résultat observé |
| --- | --- | --- | --- |
| 1 | Créer un nouveau monde. | Le datapack est chargé automatiquement. La dimension `les_echos_du_monde:prologue` existe. Le terrain nécessaire à l'arrivée est préparé avant la téléportation. | À remplir |
| 2 | Entrer pour la première fois avec un joueur neuf. | Le joueur arrive à **0, -4, 0**, posé sur le sol, sans chute dans le vide, suffocation ni blocage. La première téléportation est enregistrée une seule fois. | À remplir |
| 3 | Observer le village et les emplacements réservés. | Aucun repère en béton ne reste visible. L'herbe et les fleurs sont peu nombreuses dans la zone marron ; les chemins et emplacements réservés sont dégagés. Aucun arbre supplémentaire n'apparaît. | À remplir |
| 4 | Marcher doucement vers une zone encore non générée, puis franchir plusieurs limites de segments. | Les segments apparaissent autour du joueur, aux bonnes positions, sans décalage ni changement d'orientation. La génération respecte son rythme et ne remplace pas un segment déjà terminé. | À remplir |
| 5 | Entrer dans la zone de sortie **X=-1..1, Y=-4..-2, Z=6..8** sans utiliser de commande. | Le joueur est téléporté dans l'Overworld au point provisoire prévu. Vérifier sur place le sol et l’absence de danger avant diffusion du modpack. Aucun droit de commande ni quête n'est requis. | À remplir |
| 6 | Se déconnecter après la sortie, puis revenir. | Le joueur reste à son emplacement enregistré et n'est pas renvoyé automatiquement au prologue. | À remplir |
| 7 | Après la sortie, mourir et réapparaître. | La réapparition suit le point de réapparition normal du joueur ou du monde. Le datapack ne renvoie pas le joueur au prologue. | À remplir |
| 8 | Dans le prologue, modifier un bloc d'un segment terminé. S'éloigner, revenir, se reconnecter, puis recharger les fonctions. | La modification reste présente à chaque étape ; aucun segment terminé n'est replacé. | À remplir |
| 9 | Mettre la génération en pause pendant qu'elle travaille, puis attendre. | Aucun nouveau segment n'est placé. Les tickets de chargement ajoutés temporairement par la génération sont libérés. Les segments terminés restent enregistrés. | À remplir |
| 10 | Pendant la pause, faire entrer un joueur déjà présent dans la zone de sortie. | La sortie fonctionne toujours. | À remplir |
| 11 | Reprendre la génération dans ce même nouveau monde. | La génération repart là où elle s'était arrêtée, sans replacer les segments terminés. | À remplir |
| 12 | Faire rejoindre le monde par un second joueur neuf, puis explorer dans deux directions différentes. | Le second joueur reçoit sa première téléportation. Les deux joueurs sont pris en compte. Un même segment n'est pas placé deux fois. | À remplir |
| 13 | Quitter le monde pendant une génération en cours, puis le relancer. | La génération reprend proprement. Les segments terminés sont conservés ; les chargements temporaires ne s'accumulent pas. | À remplir |
| 14 | Ouvrir une copie d'un monde utilisant une ancienne disposition de plateforme. | La nouvelle génération est bloquée et les constructions existantes restent intactes. | À remplir |
| 15 | Inspecter les trois blocs de structure préservés. | Ils portent les noms `ferme`, `poke_shop` et `poke_centre` dans le namespace `les_echos_du_monde`. Leurs templates sont disponibles sans ajout de mod. | À remplir |

### Informations à conserver en cas d'échec

- Numéro du scénario et résultat obtenu.
- Nom du monde et joueur utilisé ; préciser si ce joueur avait déjà rejoint le monde.
- Dimension et coordonnées au moment du problème.
- État de pause/reprise et état du segment concerné, si ces informations sont disponibles.
- Capture d'écran et copie du journal `latest.log` du lancement concerné.

Ne pas effacer l'état des segments pour masquer un échec : cela pourrait provoquer un replacement sur les constructions déjà réalisées.

## Sauvegarde et fichiers livrés

Sauvegarde avant installation : `C:\Users\Bastien\Desktop\Les Echo du monde\backups\prologue_plateforme17_20261001_232713`. Aucun fichier de sauvegarde de monde n’a été modifié.

- Source intacte : `06_RESSOURCES/Structures_NBT/plateforme__17.nbt`.
- Copie préparée : `outputs/prologue_plateforme17/plateforme__17_preparee.nbt`.
- Datapack complet préparé : `outputs/prologue_plateforme17/datapack/`.
- Copie de référence du datapack : `outputs/les_echos_du_monde_datapack/`.
- Rapport et plan : `rapport_preparation.json`, `segments_manifest.json`, `runtime_manifest.json`, `plan_zones.png`.
- Scripts reproductibles : `prepare_platform.py`, `build_functions.py`, `integrate_pack.py`.

Le chargement automatique utilise GlobalPacks : `config/global_packs.toml`, section `[datapacks]`, dossier requis `global_packs/required_data/`. OpenLoader lit déjà `datapacks/` ; aucune deuxième copie n’y est ajoutée. Aucun réglage des chargeurs ni mod n’a été ajouté.

## Correctif du 2 octobre 2026 — feuilles flottantes

La feuille de chêne visée sur la capture à **(-20, -1, 6)** existe déjà dans le NBT original. Elle appartient à un fragment de neuf feuilles sans tronc ni support voisin. La préparation et le découpage avaient conservé ce fragment. En jeu, sa distance aux troncs a été recalculée de 1 à 7.

La copie préparée et ses segments retirent désormais **109 feuilles de chêne**, réparties en **14 fragments isolés** : aucune connexion à un tronc, au sol ou au décor proche. Les feuilles des arbres et des buissons soutenus sont conservées. Les fragments de cerisier proches des canopées et les feuilles d’azalée n’ont pas été modifiés par ce correctif.

### Monde déjà créé

Au prochain démarrage du monde utilisant `segments_v17`, les fonctions `world/leaves_v17` nettoient automatiquement les **positions exactes** de ces fragments, lorsque leur chunk déjà généré est chargé. Aucune commande joueur nécessaire. La réparation est enregistrée par chunk et ne remplace pas les segments terminés. Les constructions restent en place. Les autres types de blocs aux positions recensées sont conservés.

Parmi les fragments d’origine, **103 feuilles sont non persistantes** et **6 sont persistantes**. Le nettoyage vérifie ce caractère à chaque position ; pour les six persistantes, il exige aussi `distance=7` et `waterlogged=false`. Une feuille de chêne ajoutée depuis avec exactement ces mêmes propriétés et au même emplacement serait également retirée lors du premier passage du correctif.

La réparation respecte la pause du prologue. Si la génération est volontairement en pause, utiliser la reprise habituelle lorsque le nettoyage est souhaité.

### Vérification au retour

1. Redémarrer complètement Minecraft, puis ouvrir le monde actuel **1**.
2. Revenir près de **(-20, -1, 6)** : le fragment de la capture doit avoir disparu.
3. Parcourir la zone pour charger les autres chunks concernés ; vérifier que les arbres complets et les buissons posés au sol restent présents.
4. Vérifier qu’une construction ou un bloc modifié dans un segment terminé reste intact ; se reconnecter et vérifier à nouveau.
5. Facultatif : créer un nouveau monde de test et vérifier l’absence de ces mêmes fragments.

Contrôles hors jeu : source originale inchangée ; comparaison de la copie avant/après limitée aux **109 états de feuilles remplacés par de l’air** ; toutes les autres entrées, les plantes ajoutées et les données NBT conservées. Le nettoyage utilise uniquement les coordonnées enregistrées, ajoute zéro chargement forcé et ne remet aucun score de génération à zéro.

Les journaux et la sauvegarde du monde 1 confirment le chargement du datapack, l’arrivée dans le prologue et **127 segments terminés** avant ce correctif. **Le nettoyage correctif n’a pas encore été observé dans Minecraft.**
