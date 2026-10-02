# Fichiers livrés — plateforme 17

## Installation

Datapack installé : `C:\Users\Bastien\curseforge\minecraft\Instances\Pixelmon Les Échos du Monde\global_packs\required_data\les_echos_du_monde`.

**0 fichiers créés et 0 fichiers modifiés** par rapport au datapack sauvegardé. Aucun fichier supprimé. Liste exhaustive dans `fichiers_changes.json`, chemins relatifs au dossier ci-dessus. Les **4,860 fichiers** du datapack installé correspondent aux empreintes de la copie préparée.

## Principaux fichiers créés

- `data/les_echos_du_monde/structure/platform_segments_v17/` : **203 NBT** de 32 × 89 × 32 blocs.
- `data/les_echos_du_monde/function/world/segments_v17/` : **1 249 fonctions** de génération, attente, pause, reprise et contrôle.
- `data/les_echos_du_monde/function/player/teleport_to_prologue.mcfunction` : arrivée du joueur.
- `data/les_echos_du_monde/function/world/detect_exit.mcfunction` : zone de sortie.
- `data/les_echos_du_monde/function/world/pause_legacy_automation.mcfunction` : annulation des anciennes chaînes.
- `data/les_echos_du_monde/structure/ferme.nbt`, `poke_shop.nbt`, `poke_centre.nbt` : sources existantes copiées sans modification, disponibles aux blocs LOAD.
- `GENERATION_SEGMENTS.md` et archives de documentation précédente.

## Fichiers modifiés dans le datapack


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

La vérification des fichiers et la lecture des commandes vanilla ont réussi. **Aucun test exécuté dans Minecraft.** L’arrivée Overworld à `0.5 80 0.5` reste provisoire et son sol doit être contrôlé avant le partage du modpack.
