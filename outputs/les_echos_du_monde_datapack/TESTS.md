# Tests Minecraft — prologue

Ces essais restent à effectuer dans Minecraft : l’inspection des fichiers confirme le format et la configuration du chargeur, mais ne remplace pas un lancement réel de NeoForge.

## Préparation

1. Ferme Minecraft avant toute modification du datapack.
2. Crée un nouveau monde de test dans l’instance `Pixelmon Les Échos du Monde`.
3. Vérifie que la partie démarre sans erreur de datapack. Avec les commandes activées, `/datapack list` doit inclure `les_echos_du_monde` parmi les packs activés.
4. Dans le chat du joueur avec les commandes autorisées, `/execute in les_echos_du_monde:prologue run tp @s 0.5 -4 0.5` peut servir à vérifier manuellement l’arrivée.

## Parcours demandé

1. **Création d’un nouveau monde** — Le premier chargement doit se terminer sans écran d’erreur de datapack ni retour au menu.
2. **Première connexion** — Le joueur doit arriver dans `les_echos_du_monde:prologue`, au-dessus du terrain importé depuis `plateforme_prologue.nbt`, vers `(0.5, -4, 0.5)`.
3. **Passage par la sortie** — Entre dans la zone réglée dans `function/tick.mcfunction` (par défaut x=-1..1, y=-4..-2, z=6..8). Le joueur doit arriver à `(0.5, 80, 0.5)` dans l’Overworld. Vérifie que le point est sûr et corrige `player/exit.mcfunction` si le terrain ou le village est ailleurs.
4. **Reconnexion** — Quitte puis rejoins la sauvegarde. Le joueur doit rester dans l’Overworld, sans retour automatique au prologue.
5. **Mort et réapparition** — Après la sortie, vérifie `/gamerule spawnRadius` : la valeur doit être `0`. Sans lit, exécute `/kill @s` et vérifie le retour au spawn mondial fixe `(0, 80, 0)`, sans téléportation vers le prologue.

## Cas complémentaires conseillés

- Rejoins avec un second joueur neuf : lui aussi doit faire le prologue une fois, indépendamment du premier joueur.
- Rejoins avec le même joueur après la mort : le tag `edm_prologue_done` doit empêcher une nouvelle téléportation.
- Si un joueur tombe dans le vide du prologue, il peut mourir et réapparaître normalement; la téléportation d’arrivée ne sera pas rejouée.
- Utilise `/reload` après une modification des fonctions ou des coordonnées. Pour un changement de la dimension elle-même, crée une nouvelle sauvegarde de test.
- Sur une sauvegarde où le prologue était déjà vide, `/reload` doit déclencher le placement de la structure une fois. Attends la fin du chargement, puis vérifie le sol près de `(0, -5, 0)`. Le datapack marque ensuite `platform_placed` dans le stockage de commandes de cette sauvegarde.
- Si la structure ne peut pas être placée, le joueur doit recevoir un message rouge au prochain tick. Après une modification du datapack, fermer puis rouvrir le monde recharge aussi la fonction `load`.
