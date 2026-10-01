# Les Échos du Monde

Dossier de conception et de production du modpack Pixelmon **Les Échos du Monde**.

Commencer par le [guide du projet](00_PILOTAGE/00_GUIDE_DU_PROJET.md), qui indique quel document fait référence pour chaque sujet.

Pour synchroniser les fichiers entre le PC et Android, suivre le [guide de synchronisation](SYNCHRONISATION_PC_ANDROID.md).

## Plateforme du prologue — version du 1er octobre 2026

La [copie végétalisée et ses scripts](06_RESSOURCES/Structures_NBT/Vegetation_finale/LISEZ_MOI.txt) sont conservés avec les ressources. Le [datapack exporté](outputs/les_echos_du_monde_datapack/README.md) correspond à la version installée sur le PC : 933 morceaux, arrivée exacte `(7, -3, 1)`, origine **provisoire** `(-235, -30, -250)`.

Les fichiers ont été vérifiés ; **aucun essai en jeu n’a été effectué** pour cette version. Voir les [consignes de construction](Consignes_creation_zone_depart.md) et la [procédure de test](outputs/les_echos_du_monde_datapack/TESTS.md). Les sauvegardes complètes et les caches restent locaux.

## Structure

- `00_PILOTAGE/` — guide et règles de travail.
- `01_LORE/` — lore général validé.
- `02_QUETES/` — quêtes, progression et arcs des légendaires.
- `03_ECONOMIE/` — économie, références Pokémon et catalogue.
- `04_TECHNIQUE/` — notes techniques et diagnostics.
- `05_PRODUCTION/` — éléments à créer et à vérifier.
- `06_RESSOURCES/` — images et structures NBT.
- `90_ARCHIVES/` — documents migrés et sauvegardes historiques.
- `99_IDEES_A_EXPLORER/` — propositions non validées et registre `IDEES_ABANDONNEES.md` pour faciliter leur réutilisation.
- `Addons/` — espace de travail MCreator.
- `outputs/` et `patch.mjs` — exports et outil associé ; leurs chemins actuels sont conservés.

Les archives migrées et les sauvegardes ont été rangées sans modifier leur contenu. Le doublon d’idées déplacé dans `90_ARCHIVES/DOUBLONS_IDENTIQUES/` est identique au fichier conservé dans `99_IDEES_A_EXPLORER/`.


