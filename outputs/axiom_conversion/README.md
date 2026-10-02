# Schematics convertis en blueprints Axiom

370 fichiers `.schematic` du projet ont été convertis en `.bp`.

## Emplacement dans Minecraft

Profil : **Aximon**, Axiom 6.0.5 pour Minecraft 1.21.1.

`C:\Users\Bastien\curseforge\minecraft\Instances\Aximon\config\axiom\blueprints`

Les fichiers sont directement dans ce dossier, de `t001.bp` à `t370.bp`.
Le profil utilise le chemin par défaut, avec actualisation automatique activée.

Dans Axiom, ouvrir l'éditeur avec **Maj droite**, puis **Windows → Blueprint Browser**.
Actualiser la liste si nécessaire. Les blueprints portent les tags `tree` et
`les_echos_du_monde`. Cliquer sur un blueprint, utiliser **Ctrl+V** pour afficher
son placement, puis **Entrée** pour le confirmer.

## Conversion et contrôles

- Sources conservées dans `06_RESSOURCES\individual schematics`.
- Copies des `.bp` disponibles dans le sous-dossier `blueprints` de ce rapport.
- Correspondances des anciens identifiants de blocs fournies par WorldEdit.
- Types de blocs, orientations et propriétés convertis vers Minecraft 1.21.1.
- Les cellules d'air deviennent `structure_void` pour un placement transparent.
- Les sources ne contenaient aucune entité, entité de bloc ou tick enregistré.
- Vignettes isométriques approximatives générées pour faciliter le choix ; elles ne
  sont pas des captures de Minecraft.
- Chaque `.bp` a été relu, décompressé et comparé aux états de blocs de sa source.
- Les empreintes SHA-256 des sources confirment qu'elles sont inchangées.
- Les copies installées ont été vérifiées par SHA-256 ; aucun fichier différent
  préexistant n'a été écrasé.

La validation dans Minecraft n'a pas été effectuée. Pour la terminer, ouvrir
quelques blueprints de tailles et de types différents, vérifier leur aperçu,
puis en poser un dans une zone libre d'un monde de construction.

## Fichiers de suivi

- `rapport_conversion.json` : sources, dimensions, empreintes, vérifications et installation.
- `inventaire.csv` : inventaire lisible dans un tableur, dimensions X × Y × Z.
- `convert_schematics.py` : script de conversion reproductible.
- `tools/worldedit_legacy.json` : correspondances WorldEdit utilisées.
- `tools/AxiomSchematicFormat.reference.java` : référence du format BP consultée.
- `dependencies` : bibliothèque NBT locale utilisée par le script, conservée sur le PC et exclue de Git.

Sources techniques :

- https://github.com/EngineHub/WorldEdit/blob/master/worldedit-core/src/main/resources/com/sk89q/worldedit/world/registry/legacy.json
- https://github.com/PiTheGuy/SchemConvert/blob/master/src/main/java/pitheguy/schemconvert/converter/formats/AxiomSchematicFormat.java
- https://axiomdocs.moulberry.com/editor/windows/blueprints.html

## Refaire la conversion sur un autre PC

Le script utilise Python, `nbtlib` 2.0.4, NumPy et Pillow. Le dossier de bibliothèques téléchargées n’est pas publié dans Git. Installer ces bibliothèques dans l’environnement Python choisi avant d’exécuter la conversion. Le script accepte également `nbtlib` installé dans cet environnement lorsque le dossier `dependencies` est absent. Vérifier les chemins du profil Aximon avant toute installation des blueprints ; ce profil est distinct de Pixelmon Les Échos du Monde.
