# Les Échos du Monde

Dossier de conception et de production du modpack Pixelmon **Les Échos du Monde**.

Commencer par le [guide du projet](00_PILOTAGE/00_GUIDE_DU_PROJET.md), qui indique quel document fait référence pour chaque sujet.

Pour synchroniser les fichiers entre le PC et Android, suivre le [guide de synchronisation](SYNCHRONISATION_PC_ANDROID.md).

## Plateforme du prologue — version 17

La [source `plateforme__17.nbt`](06_RESSOURCES/Structures_NBT/plateforme__17.nbt) mesure **451 × 89 × 461 blocs**. Le [datapack exporté](outputs/les_echos_du_monde_datapack/README.md) utilise **203 segments**, une origine `(-250, -26, -235)` et une arrivée `(0, -4, 0)`. Les anciennes plateformes restent conservées comme historiques.

Les [consignes de construction](Consignes_creation_zone_depart.md) et la [procédure de test](outputs/les_echos_du_monde_datapack/TESTS.md) indiquent les fichiers et coordonnées actuels. Les journaux et la sauvegarde analysés dans le [diagnostic récent](outputs/prologue_feuilles_20261002/runtime_analysis.md) confirment une arrivée dans le prologue et 127 segments terminés avant le correctif des feuilles. **Le correctif des feuilles n’a pas encore été observé en jeu** ; son [rapport](outputs/prologue_feuilles_20261002/CORRECTIF_FEUILLES.md) décrit les contrôles et l’essai restant à faire.

## Structure

- `00_PILOTAGE/` — guide et règles de travail.
- `01_LORE/` — lore général validé.
- `02_QUETES/` — quêtes, progression et arcs des légendaires.
- `03_ECONOMIE/` — économie, références Pokémon et catalogue.
- `04_TECHNIQUE/` — notes techniques et diagnostics.
- `05_PRODUCTION/` — éléments à créer et à vérifier.
- `06_RESSOURCES/` — images et structures NBT.
- `07_RETOURS_TESTEURS/` — retours sur le lore, les quêtes, les idées et les bugs.
- `90_ARCHIVES/` — documents migrés et sauvegardes historiques.
- `99_IDEES_A_EXPLORER/` — propositions non validées et registre `IDEES_ABANDONNEES.md` pour faciliter leur réutilisation.
- `Addons/` — espace de travail MCreator.
- `outputs/` et `patch.mjs` — exports et outil associé ; leurs chemins actuels sont conservés.

## Où ranger les prochains fichiers

- Les scripts et modes d’emploi Axiom vont dans `04_TECHNIQUE/` ; les schémas, fichiers NBT et images sources vont dans `06_RESSOURCES/`.
- Les livrables générés et les datapacks restent dans `outputs/`. Chaque chantier daté ou outil autonome garde son propre sous-dossier et son README si son usage n’est pas évident.
- Les copies de retour arrière liées à un chantier vont dans `backups/<nom_du_chantier>/`. Ce dossier est local et n’est pas synchronisé par Git. Les archives historiques du projet restent dans `90_ARCHIVES/`.
- Avant de déplacer un fichier, vérifier s’il est référencé par une consigne, un script ou le profil Minecraft : les chemins des exports actuels sont utilisés par le projet.
- Les `.bp` sont des fichiers sources Blueprint ; ils restent à la racine de `06_RESSOURCES/` tant que leur provenance et leur classement par structure n’ont pas été identifiés avec certitude.

Consulter l’[index des ressources et livrables](06_RESSOURCES/INDEX_RESSOURCES.md) pour retrouver les principales versions et leurs limites de validation.

Les archives migrées et les sauvegardes ont été rangées sans modifier leur contenu. Le doublon d’idées déplacé dans `90_ARCHIVES/DOUBLONS_IDENTIQUES/` est identique au fichier conservé dans `99_IDEES_A_EXPLORER/`.


