# Technique à vérifier

## Format

| Fonction voulue | Système envisagé | Preuve ou test | Résultat | Décision |
|---|---|---|---|---|
| Nom de la fonction | Mod concerné | Ce qui a été fait en jeu | Fonctionne ou non | Suite à donner |

## État actuel

| Fonction voulue | Système envisagé | Preuve ou test | Résultat | Décision |
|---|---|---|---|---|
| Fabriquer les 18 Plaques d’Arceus selon leur couleur | 18 grilles façonnées 3 × 3 distinctes dans le datapack global, feuilles de laiton Create et tessons Pixelmon | Mélanges estimés depuis les couleurs des textures ; 18 recettes ajoutées, JSON lisibles et grilles distinctes ; IDs vérifiés dans les ressources des mods | À tester dans JEI et en jeu | Charger un monde, vérifier les 18 recettes et essayer les recettes. |
| Compter toutes les bûches ou pousses | FTB Quests avec tag d’objet | Le menu de tâche ne propose pas la conversion en filtre de tag. | Non confirmé. | Vérifier la présence de FTB Filter System et FTB XMod Compat. |
| Compter une capture ou un combat Pokémon | Pixelmon Research | Documentation Pixelmon : objectifs de capture et de combat possibles. | À tester dans le modpack. | Ne pas lier au questbook avant test. |
| Dialogue d’un PNJ Pixelmon | NPC Editor Pixelmon | Le mod propose des dialogues et des interactions. | À tester en jeu. | Utiliser pour l’ambiance ; FTB garde la progression. |
| Valider une quête FTB après un dialogue Pixelmon | Commande ou datapack | Aucun lien automatique confirmé. | À tester. | Utiliser un Checkmark FTB en attendant. |
| Suivre le PokéStop de la gare abandonnée pour Q-06 | FTB Quests ou Pixelmon Research | Aucun type de tâche ne permet encore de confirmer qu’un PokéStop précis, placé près de la gare, est suivi. | À tester. | Placer le PokéStop, l’activer en jeu, puis vérifier son suivi et le comptage des 15 combats. |
| Verrouiller la sortie de la zone de départ pendant le prologue | Récompense Stage et Stage Barrier FTB Quests | FTB Quests 1.21.1 contient des récompenses Stage, des tâches Stage et le bloc Stage Barrier. Le stage `prologue_sortie` est prévu comme récompense de Q-09A. | À tester. | Configurer le Stage Barrier pour exiger `prologue_sortie`, puis vérifier que la sortie reste fermée avant Q-09A et s’ouvre après. |
| Fabriquer et suivre les objets d’exploration de Q-10 | Explorer’s Compass, Nature’s Compass, mod de sac à dos et FTB Quests | Présence des mods et de leurs objets non vérifiée dans le modpack. | Non confirmé. | Vérifier les recettes en jeu, puis créer trois tâches d’objet exactes dans FTB Quests. |
| Détruire le village de Garrick après Q-11 | Bloc repère, commande FTB Quests et fonction de destruction | FTB Quests peut lancer une commande comme récompense, mais le repère, le moment du déclenchement et la destruction du village ne sont pas testés. | Non confirmé. | Poser un bloc repère protégé au centre du village lors de sa création, puis tester une fonction exécutée une seule fois autour de ce repère. |
| Ajouter une photographie au butin des cités pour Q-11 | Lootr, Lost Cities et table de butin | Les tables `big_lost_city:chests/tier_1` à `tier_4` existent. Des coffres Lootr de niveau 1 et 2 ont été confirmés en jeu. | Partiellement confirmé. | Ajouter la photographie aux quatre tables, puis tester son apparition et sa détection par FTB Quests. |
| Valider Q-14 avec l’hôtel de ville MineColonies | FTB Quests et MineColonies | L’objet `minecolonies:blockhuttownhall` est placé dans les coffres générés par les blueprints de camp et de bateau de ravitaillement. | À tester. | Créer une tâche d’objet FTB avec `minecolonies:blockhuttownhall`, puis vérifier le contenu du coffre et la validation de la quête. |
| Débloquer Q-14 après Q-13A ou Q-13B | Dépendances FTB Quests | La configuration doit accepter qu’une seule des deux quêtes de ravitaillement soit terminée. | À tester. | Configurer Q-14 avec la condition « une quête terminée », puis vérifier les deux parcours. |
| Afficher une quête dans deux emplacements du questbook | Quêtes liées FTB Quests | Documentation FTB : une quête liée peut être affichée à plusieurs endroits du questbook. | À tester dans le modpack. | Utiliser une quête liée pour l’arc de l’oiseau, sans dupliquer la récompense. |
| Verrouiller les deux oiseaux non choisis | Stages, dépendances et récompenses de commande FTB Quests | FTB Quests contient des tâches et récompenses Stage. Le verrouillage définitif des voies non choisies n’est pas encore testé. | Non confirmé. | Tester une sélection irréversible avec des stages avant de construire les trois branches. |
| Débloquer la quête de l’oiseau choisi après Q-16A ou Q-16B | Visibilité d’un chapitre FTB et dépendance à la quête du champion | Q-16A mène à Artikodin. Q-16B doit proposer un choix unique entre Électhor et Sulfura. Ce raccord n’est pas testé dans le modpack. | Non confirmé. | Configurer Q-16A comme dépendance d’Artikodin et Q-16B comme dépendance du choix Électhor/Sulfura, puis tester l’affichage et le verrouillage. |
| Protéger durablement des zones après génération de la carte | Ajouter FTB Chunks, ou utiliser un datapack avec le mode Aventure | FTB Chunks absent du modpack ; le code charge et sauvegarde les données des chunks par équipe dans un fichier | Possible, persistance à tester | Protéger les zones après génération, redémarrer le monde pour vérifier, puis définir comment réappliquer la protection si une nouvelle carte est créée. |

## Règle

Une fonction devient `Validée` seulement après un test réussi dans le modpack de Bastien.

