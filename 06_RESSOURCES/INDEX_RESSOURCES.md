# Index des ressources et livrables

Cet index indique où retrouver les sources, les ressources de construction et les livrables récents. Il distingue les fichiers de référence des copies de travail et rappelle ce qui n’a pas encore été vérifié en jeu.

## Ressources de construction

| Emplacement | Contenu |
|---|---|
| `Blueprint Axiom/` | Schémas `.schematic` utilisés avec Axiom. |
| `individual schematics/` | Schémas individuels exportés. |
| `Structures_NBT/` | Structures Minecraft au format NBT. Les fichiers `plateforme__*.nbt` sont des versions de travail distinctes ; ne pas les remplacer sans comparer leur contenu et leur usage. |
| `Structures_NBT/Vegetation_finale/` | Copie de plateforme végétalisée, scripts et rapports de contrôle. `LISEZ_MOI.txt` décrit cette version ; elle n’est pas le datapack courant. |
| `Images/` | Images et références visuelles du projet. |
| Fichiers `.bp` à la racine | Sources Blueprint en attente de classement par structure. |

## Outils et datapack

- `../04_TECHNIQUE/AXIOM_VEGETATION_MODE_EMPLOI.md` et `../04_TECHNIQUE/AXIOM_VEGETATION.lua` : Script Brush Axiom pour végétaliser dans le jeu.
- `../outputs/axiom_conversion/` : outil de conversion des schémas, inventaire et rapport. C’est un dossier de travail/export ; conserver sa structure interne.
- `../outputs/les_echos_du_monde_datapack/` : datapack de prologue actuellement exporté dans le dépôt. Son `README.md` et son `TESTS.md` décrivent la version et les contrôles. Les journaux et la sauvegarde analysés confirment l’arrivée dans le prologue et 127 segments terminés avant le correctif des feuilles du 2 octobre. Ce correctif reste à observer en jeu ; voir `../outputs/prologue_feuilles_20261002/CORRECTIF_FEUILLES.md`.
- `../Consignes_creation_zone_depart.md` : consignes de construction et de placement de la zone de départ.

## Archives et sauvegardes locales

- `../backups/` contient des copies de retour arrière horodatées pour les chantiers de plateforme. Ces copies peuvent être volumineuses et ne sont pas synchronisées par Git.
- `../90_ARCHIVES/` contient les documents migrés et archives historiques du projet. Ne pas supprimer avant d’avoir classé les informations encore utiles.
- Les sous-dossiers de `../outputs/` sont des livrables ou des espaces de travail conservés à leur emplacement actuel. Certains chemins sont utilisés par les consignes et les outils.

## Versions de plateformes : ne pas confondre

Plusieurs ressources de plateforme coexistent : des structures NBT dans ce dossier, la copie végétalisée dans `Vegetation_finale/`, et la plateforme découpée intégrée au datapack exporté. Les dimensions, points d’arrivée et états de test ne sont pas identiques. Pour une installation, suivre la version explicitement désignée par le README du datapack et les consignes d’installation, puis vérifier les tests indiqués ; ne pas choisir une version à partir de son seul nom ou de sa date.
