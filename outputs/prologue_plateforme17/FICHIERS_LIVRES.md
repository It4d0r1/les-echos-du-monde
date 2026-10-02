# Fichiers livrés — plateforme 17

## Installation

Datapack installé : `C:\Users\Bastien\curseforge\minecraft\Instances\Pixelmon Les Échos du Monde\global_packs\required_data\les_echos_du_monde`.

Les **4 860 fichiers** du datapack installé correspondent exactement à la copie préparée, à l’export du projet et au contenu du ZIP. Le contrôle SHA-256 ne relève aucun fichier différent, absent ou supplémentaire. Le rapport `fichiers_changes.json` compare la dernière copie de synchronisation, déjà identique : ses compteurs n’indiquent pas le nombre de modifications depuis l’ancienne plateforme.

## Principaux fichiers livrés

- `data/les_echos_du_monde/structure/platform_segments_v17/` : **203 NBT** de 32 × 89 × 32 blocs.
- `data/les_echos_du_monde/function/world/segments_v17/` : **1 249 fonctions** de génération, attente, pause, reprise et contrôle.
- `data/les_echos_du_monde/function/player/teleport_to_prologue.mcfunction` : arrivée du joueur.
- `data/les_echos_du_monde/function/world/detect_exit.mcfunction` : zone de sortie.
- `data/les_echos_du_monde/function/world/pause_legacy_automation.mcfunction` : annulation des anciennes chaînes.
- `data/les_echos_du_monde/structure/ferme.nbt`, `poke_shop.nbt`, `poke_centre.nbt` : sources existantes copiées sans modification, disponibles aux blocs LOAD.
- `GENERATION_SEGMENTS.md` et archives de documentation précédente.

## Correctif des feuilles du 2 octobre

- `data/les_echos_du_monde/function/world/leaves_v17/` : 15 fonctions, dont 12 helpers par chunk.
- Les segments corrigés ne contiennent plus les 109 feuilles de chêne isolées recensées. Le nettoyage des mondes existants cible ces mêmes positions sans remplacer les segments terminés.
- `CORRECTIF_FEUILLES.md` et `../prologue_feuilles_20261002/verification_correctif.json` indiquent les preuves et les limites.

## Dans le projet

- `Consignes_creation_zone_depart.md` : nouvelle version, coordonnées et méthode de découpage ; anciennes versions conservées comme historique.
- `outputs/les_echos_du_monde_datapack/` : copie identique du datapack installé.
- `outputs/prologue_plateforme17/plateforme__17_preparee.nbt` : copie préparée du NBT original.
- `outputs/prologue_plateforme17/les_echos_du_monde_prologue17.zip` : paquet partageable, contenu vérifié.
- `prepare_platform.py`, `build_functions.py`, `integrate_pack.py`, `validate_pack.py`, `install_pack.py` : scripts de reproduction et contrôle.
- `TESTS_ET_UTILISATION.md`, `plan_zones.png` et rapports JSON : instructions et preuves des vérifications hors jeu.

Le NBT original, les sauvegardes de monde, les configurations GlobalPacks/OpenLoader et les fichiers `.jar` n’ont pas été modifiés. Aucun mod ajouté.

## Essai au retour

Redémarrer complètement Minecraft, puis créer un **nouveau monde de test**. Suivre `TESTS_ET_UTILISATION.md` : première arrivée, exploration, sortie, reconnexion, mort/réapparition, durabilité des constructions, pause/reprise et multijoueur.

La vérification des fichiers et la lecture des commandes vanilla ont réussi. Les journaux et la sauvegarde confirment l’arrivée et 127 segments terminés avant le correctif. **Le correctif des feuilles reste à observer dans Minecraft.** L’arrivée Overworld à `0.5 80 0.5` reste provisoire et son sol doit être contrôlé avant le partage du modpack.
