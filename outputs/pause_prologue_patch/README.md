# Patch de mise en pause du prologue

Fichiers prepares depuis l'etat actuel du datapack:
- `data/les_echos_du_monde/function/load.mcfunction`: lance une fois la mise en pause persistante par sauvegarde.
- `data/les_echos_du_monde/function/tick.mcfunction`: garde les quatre automatisations existantes derriere le marqueur de pause.
- `data/les_echos_du_monde/function/world/pause_automation.mcfunction`: annule les 706 tuiles planifiees, nettoie leur ticket de forceload si une tuile en attente en possedait un, et annule les 32 anciennes fonctions lineaires. La syntaxe Java est `/schedule clear <fonction>`.\n- `data/les_echos_du_monde/function/world/migrate_platform_marker.mcfunction`: corrige les 32 annulations historiques vers la syntaxe Java valide.

Le fichier de dimension et les fonctions de teleportation/placement restent presents. Les blocs deja places ne sont pas effaces. Aucune sauvegarde de monde ni aucun JAR n'est modifie par ce patch.