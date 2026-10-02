# Consignes — création de la zone de départ

## Objectif

Construire la zone d’arrivée du prologue, puis noter ici les éléments nécessaires à son intégration au datapack.

## Consignes de construction

- Construire et tester la zone dans la dimension du prologue.
- Garder une arrivée sûre pour le joueur : point fixé exactement à `(0, -4, 0)`. Vérifier le sol, l’espace libre au-dessus et l’absence de danger.
- Définir clairement les limites de la zone et noter les coordonnées des constructions importantes.
- Prévoir une sortie visible et accessible vers le village principal.
- Conserver le NBT original intact. Générer une copie avec les scripts documentés plutôt que modifier ses données manuellement.
- Pour chaque bâtiment sauvegardé avec un bloc de structure, utiliser deux repères `CORNER` et un bloc `SAVE`, tous avec le même nom.
- Vérifier le cadre détecté, puis sauvegarder et tester le chargement du bâtiment dans une zone vide.
- Noter les fichiers `.nbt` obtenus et leur emplacement.

## Génération et découpage de la plateforme

### Version actuelle — plateforme 17

La source `06_RESSOURCES/Structures_NBT/plateforme__17.nbt` mesure réellement **451 × 89 × 461 blocs**. Elle est conservée intacte. L’origine du terrain est **(-250, -26, -235)**, sans rotation ni miroir ; l’arrivée du joueur est exactement **(0, -4, 0)**, avec sol à **Y=-5**.

Le datapack utilise **203 segments de 32 × 89 × 32 blocs**, soit **quatre chunks (2 × 2)** par segment. Les neuf segments proches de l’arrivée sont préparés avant la première téléportation. Les autres se placent autour des joueurs, avec un rayon de deux segments et au plus un placement toutes les deux ticks. Les segments terminés ne sont jamais remis à zéro automatiquement.

```text
monde_x = nbt_x - 250
monde_y = nbt_y - 26
monde_z = nbt_z - 235
segment_x = floor(monde_x / 32)
segment_z = floor(monde_z / 32)
local_x = monde_x - 32 * segment_x
local_z = monde_z - 32 * segment_z
origine_segment = (32 * segment_x, -26, 32 * segment_z)
```

Les repères en béton ont été enregistrés puis retirés. Le village délimité en marron reçoit **48 herbes et 17 fleurs**. Les autres repères réservent les bâtiments, avec une marge de quatre blocs sans végétation ajoutée. Les repères gris enterrés ont été remplacés par pierre ou terre selon leur couverture. Aucun arbre ni buisson ajouté ; les arbres existants sont conservés.

Trois blocs LOAD et leurs données sont préservés : `ferme`, `poke_shop`, `poke_centre`. Le datapack fournit ces trois NBT ; il ne déclenche pas leur chargement automatique. Leurs tailles vérifiées sont **27 × 22 × 46**, **29 × 17 × 21** et **22 × 22 × 29**. Ces tailles lues dans les fichiers priment sur les calculs approximatifs des anciens tableaux.

Fichiers de travail : `outputs/prologue_plateforme17/`. Code : `prepare_platform.py`, `build_functions.py`, `integrate_pack.py`. Instructions, réglages et tests : **[TESTS_ET_UTILISATION.md](outputs/prologue_plateforme17/TESTS_ET_UTILISATION.md)**. Plan des réserves : `plan_zones.png`. Rapport : `rapport_preparation.json`.

Le chargement reste assuré par `global_packs/required_data/les_echos_du_monde/`. Les anciens mondes sont mis en pause pour protéger les constructions. Aucun essai de cette version n’a été réalisé dans Minecraft.

Les informations suivantes décrivent les anciennes versions et restent conservées comme historique.

### Historique — ancienne plateforme 4, installée le 1er octobre 2026

Les informations ci-dessous sont confirmées dans les fichiers. **Aucun essai dans Minecraft n’a été effectué pour cette version.**

- Source intacte : `06_RESSOURCES/Structures_NBT/plateforme__4.nbt`.
- Copie végétalisée : `06_RESSOURCES/Structures_NBT/Vegetation_finale/plateforme__4_vegetalisee.nbt`.
- Dimensions réelles : **562 × 93 × 536** ; DataVersion **3955** ; **5 593 060** entrées de blocs dans la copie finale.
- Origine de placement **provisoire** : **(-235, -30, -250)**, sans rotation ni miroir.
- Arrivée exacte du joueur : **(7, -3, 1)**. Sol à Y=-4 et espace libre vérifiés dans le NBT.
- Datapack exporté dans Git : `outputs/les_echos_du_monde_datapack/`.
- Installation locale : `global_packs/required_data/les_echos_du_monde/` dans l’instance CurseForge.

Les coins approximatifs précédemment fournis donnent 461 × 96 × 476 et ne correspondent pas à la boîte réelle du NBT. L’étendue, avec l’origine provisoire, est X=-235..326, Y=-30..62, Z=-250..285, limites incluses. Toutes les réserves exprimées en coordonnées du monde dépendent de cette origine.

### Ancien découpage : 933 morceaux

1. Convertir chaque position locale du NBT en coordonnées du monde avec l’origine provisoire.
2. Regrouper les blocs par chunk du monde, avec une division arrondie vers le bas, y compris pour les coordonnées négatives.
3. Replacer chaque bloc dans une tuile locale X/Z=0..15, Y=0..92. Conserver les états et données NBT des blocs.
4. Enregistrer les **933 tuiles non vides** de taille 16 × 93 × 16 sous les noms `chunk_0000.nbt` à `chunk_0932.nbt`, du chunk (0, 0) vers l’extérieur.
5. Attendre le chargement de chaque chunk, placer sa tuile, puis passer à la suivante. Libérer uniquement les chargements forcés ajoutés par cette chaîne.

```text
monde_x = nbt_x - 235
monde_y = nbt_y - 30
monde_z = nbt_z - 250
chunk_x = floor(monde_x / 16)
chunk_z = floor(monde_z / 16)
tuile_x = monde_x - 16 * chunk_x
tuile_z = monde_z - 16 * chunk_z
```

Chaque tuile est placée à `(16 * chunk_x, -30, 16 * chunk_z)`. Le découpage a été reconstitué et comparé au NBT final : mêmes positions et états, 24 blocs avec leurs données NBT préservées, aucun bloc perdu ni chevauchement.

Le joueur attend dans l’Overworld avec un indicateur de progression, puis rejoint le prologue à (7, -3, 1) après la préparation complète. Les anciennes sauvegardes sont mises en pause pour éviter de superposer les deux plateformes. Pour l’essai, relancer complètement Minecraft et créer un nouveau monde.

### Fichiers et scripts à conserver

- Génération de la végétation : `06_RESSOURCES/Structures_NBT/Vegetation_finale/generer_vegetation.py`.
- Découpage, contrôle et installation : `06_RESSOURCES/Structures_NBT/Vegetation_finale/installer_plateforme.py`.
- Zones protégées et paramètres : `06_RESSOURCES/Structures_NBT/Vegetation_finale/LISEZ_MOI.txt`.
- Rapport : `06_RESSOURCES/Structures_NBT/Vegetation_finale/Installation_20261001_175619/rapport_installation.json`.
- Démarrage : `data/les_echos_du_monde/function/world/place_platform.mcfunction`.
- Fonctions de placement : `data/les_echos_du_monde/function/world/vegetation_chunks/chunk_XXXX.mcfunction`.
- Tuiles NBT : `data/les_echos_du_monde/structure/prologue_vegetation_chunks/chunk_XXXX.nbt`.
- Procédure de test : `outputs/les_echos_du_monde_datapack/TESTS.md`.

Les scripts Python nécessitent NumPy et Pillow. L’installateur comporte des chemins propres à ce PC : les adapter avant de le lancer ailleurs. Le NBT complet reste volumineux ; le datapack utilise les morceaux, pas le placement du modèle complet.

### Réserves de construction

Les six anciens rectangles de repérage et leur marge de quatre blocs restent sans végétation ajoutée. Les chemins et constructions existants ont été préservés. Aucun arbre ni buisson ajouté n’empiète sur la réserve de Garrik : **X=-16..31, Z=-80..-33**, limites incluses. Le détail des rectangles et les marges figurent dans `LISEZ_MOI.txt`.

### Historique

La précédente plateforme mesurait 449 × 93 × 486, avec 706 morceaux et une origine (-224, -56, -243). Ses anciens fichiers restent conservés mais ne sont plus utilisés pour le démarrage des nouveaux mondes. Le diagnostic de cette version est conservé dans `04_TECHNIQUE/Diagnostic_dimension_prologue.txt`. Ne pas réutiliser ses morceaux ou ses coordonnées pour la plateforme actuelle.

## À compléter

### Plan général

- Dimensions de la zone :
- Thème et ambiance :
- Éléments du décor :

### Points importants

- Arrivée du joueur :
- Sortie vers le village :
- Autres points à repérer :

### Bâtiments

**La taille exacte est très importante** : recopie celle affichée par le bloc `SAVE`, en blocs et dans l’ordre `X × Y × Z`. Elle servira à vérifier le NBT et à préparer son découpage. Pour les coordonnées, écris les valeurs dans l’ordre `X, Y, Z`, comme dans Minecraft.

| Structure | Nom des blocs de structure | Poteau 1 `CORNER` (X, Y, Z) | Poteau 2 `CORNER` (X, Y, Z) | Taille calculée (X × Y × Z, blocs) | Fichier `.nbt` |
|---|---|---|---|---|---|
| Plateforme actuelle | `plateforme__17` | Origine de placement : X=-250 ; Y=-26 ; Z=-235 | Limite inclusive : X=200 ; Y=62 ; Z=225 | 451 × 89 × 461 (NBT vérifié) | `plateforme__17_preparee.nbt` |
| Waystone | `waypoint` | X=-2 ; Y=-5 ; Z=1 | X=2 ; Y=0 ; Z=--3 | À confirmer : 5 × 6 × 5 si Z=-3 ; 5 × 6 × 3 si Z=3 | `waypoint.nbt` |
| Pokécentre | `poke_centre` | X=49 ; Y=-5 ; Z=64 | X=70 ; Y=17 ; Z=92 | 22 × 23 × 29 | `poke_centre.nbt` |
| Pokéshop | `poke_shop` | X=-7 ; Y=-6 ; Z=35 | X=-35 ; Y=11 ; Z=15 | 29 × 18 × 21 | `poke_shop.nbt` |
| Arène | `arene` | X=44 ; Y=-10 ; Z=3 | X=64 ; Y=4 ; Z=23 | 21 × 15 × 21 | `arene.nbt` |
| Mine | `mine` | X=100 ; Y=8 ; Z=42 | X=115 ; Y=-5 ; Z=31 | 16 × 14 × 12 | `mine.nbt` |
| Ferme | `ferme` | X=-4 ; Y=-6 ; Z=93 | X=-30 ; Y=16 ; Z=48 | 27 × 23 × 46 | `ferme.nbt` |
| Maison 1 | `maison_1` | X=14 ; Y=-6 ; Z=65 | X=26 ; Y=3 ; Z=77 | 13 × 10 × 13 | `maison_1.nbt` |
| maelle | `maelle` | X=11 ; Y=14 ; Z=139 | X=-27 ; Y=11 ; Z=177 | À calculer après saisie des coordonnées | `maelle.nbt` |

Les tailles calculées comptent les deux positions `CORNER` dans la sélection : pour chaque axe, taille = différence absolue entre les deux coordonnées + 1. Vérifie-les avec la taille affichée par le bloc `SAVE`. Pour la Waystone, remplace `Z=--3` par la valeur voulue avant de valider sa taille.

### Vérifications en jeu

- Le joueur apparaît sans tomber ni être coincé.
- Les bâtiments sont chargés au bon endroit et dans la bonne orientation.
- La sortie est facile à trouver et fonctionne.
- Aucun bâtiment ne se chevauche ni ne remplace une construction existante.

## Notes

<!-- Ajoute ici les détails et décisions de construction. -->

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
