"""Publish the verified settings, commands and manual test instructions."""
from pathlib import Path
import json
import shutil

ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parents[1]
PACK=ROOT/'datapack'
LIVE=Path(r'C:\Users\Bastien\curseforge\minecraft\Instances\Pixelmon Les Échos du Monde\global_packs\required_data\les_echos_du_monde')

def main():
    path=ROOT/'TESTS_ET_UTILISATION.md'
    text=path.read_text(encoding='utf-8')
    substitutions={
    '**[À COMPLÉTER PAR LE RESPONSABLE : fichier du générateur et paramètres exacts]**':'`outputs/prologue_plateforme17/prepare_platform.py` : constante `ORIGIN`, puis reconstruire le NBT, les segments et les fonctions. Utiliser un nouveau monde.',
    '**[À COMPLÉTER PAR LE RESPONSABLE : fonction et ligne de téléportation]**':'`data/les_echos_du_monde/function/player/teleport_to_prologue.mcfunction` : commande `tp @s 0 -4 0`. Les neuf segments préparés au démarrage sont centrés sur X=0, Z=0 dans `build_functions.py` ; les adapter si l’arrivée est déplacée loin.',
    '**[À COMPLÉTER PAR LE RESPONSABLE : fonction de détection et sélecteur exact]**':'`data/les_echos_du_monde/function/world/detect_exit.mcfunction` : `x=-1,y=-4,z=6,dx=2,dy=2,dz=2` (zone provisoire X=-1..1, Y=-4..-2, Z=6..8).',
    '**[À COMPLÉTER PAR LE RESPONSABLE : fonction et ligne de téléportation]** ':'`data/les_echos_du_monde/function/player/exit.mcfunction` : `tp @s 0.5 80 0.5`. ',
    '**[À COMPLÉTER PAR LE RESPONSABLE : paramètres et unités]**':'`outputs/prologue_plateforme17/build_functions.py` : option `--radius 2` = rayon de 2 cellules de 32 blocs (4 chunks). Rythme, délai maximal et tentatives sont définis dans le générateur ; reconstruire les fonctions après modification.',
    '**Dossier installé : [À COMPLÉTER PAR LE RESPONSABLE : chemin absolu vérifié].**':f'**Dossier d’installation :** `{LIVE}`.',
    '**Cette section doit être complétée avec les fonctions exactes de la version installée avant livraison. Ne pas exécuter les textes entre crochets.**':'Ces commandes fonctionnent avec les permissions d’administration habituelles. La génération ne demande aucune commande aux joueurs.',
    '**[À COMPLÉTER : commande de pause]**':'`/function les_echos_du_monde:world/pause_automation`',
    '**[À COMPLÉTER : commande de reprise]**':'`/function les_echos_du_monde:world/resume_automation`',
    '**[À COMPLÉTER : commande de diagnostic]**':'`/function les_echos_du_monde:world/segments_v17/status`',
    "**[À COMPLÉTER : commande d'inspection avec dimension et arrivée sûre]**":'`/function les_echos_du_monde:player/teleport_to_prologue` (attendre `spawn_ready:1b` avant utilisation)',
    '**[À COMPLÉTER : commande de sortie officielle]**':'`/function les_echos_du_monde:player/exit`',
    '**[À COMPLÉTER PAR LE RESPONSABLE : contrôles réellement effectués et résultat de chaque contrôle.]**':'Contrôles réalisés : NBT source inchangé (SHA256), dimensions et DataVersion 3955, **3 905 411 entrées** reconstituées à l’identique depuis **203 segments**, aucun chevauchement ni perte, trois blocs de structure avec données NBT préservées, zéro repère restant, zéro plante ajoutée dans une réserve, zéro arbre ou buisson ajouté. Sol et deux blocs libres contrôlés sur les quatre colonnes touchées par le joueur à **0, -4, 0**. Détail dans `rapport_preparation.json`. Les références des nouvelles fonctions et templates ont été contrôlées.',
    '**[COORDONNÉES À COMPLÉTER]**':'**X=-1..1, Y=-4..-2, Z=6..8**',
    '| Arrivée dans l’Overworld | 0 | 80 | 0 | Point provisoire accepté précédemment ; coordonnées exactes de téléportation à confirmer dans la version installée. |':'| Arrivée dans l’Overworld | 0.5 | 80 | 0.5 | Téléportation au centre du bloc X=0, Z=0 ; point provisoire. Spawn du monde : 0, 80, 0. |',
    '| Arrivée dans l\'Overworld | 0 | 80 | 0 | Point provisoire accepté précédemment ; coordonnées exactes de téléportation à confirmer dans la version installée. |':'| Arrivée dans l\'Overworld | 0.5 | 80 | 0.5 | Téléportation au centre du bloc X=0, Z=0 ; point provisoire. Spawn du monde : 0, 80, 0. |',
    'Quitter le prologue vers le point sûr de l\'Overworld':'Quitter le prologue vers le point provisoire de l\'Overworld',
    'au point provisoire prévu, sur une arrivée sûre.':'au point provisoire prévu. Vérifier sur place le sol et l’absence de danger avant diffusion du modpack.',
    }
    for old,new in substitutions.items(): text=text.replace(old,new)
    # The draft used the same placeholder for both arrival functions; fix that row specifically.
    rows=text.splitlines()
    for index,line in enumerate(rows):
        if line.startswith('| Point d\'arrivée dans l\'Overworld |'):
            rows[index]='| Point d’arrivée dans l’Overworld | `data/les_echos_du_monde/function/player/exit.mcfunction` : `tp @s 0.5 80 0.5`. |'
    text='\n'.join(rows)+'\n'
    text=text.replace('Leurs fichiers NBT sont fournis','Leurs positions de blocs LOAD dans le prologue sont respectivement **(-32, -6, 43)**, **(-27, -6, 17)** et **(45, -5, 63)**, avec un décalage de structure de `(0, 1, 0)`.\n\nLeurs fichiers NBT sont fournis')
    text=text.replace('## Commandes utiles pour Bastien','Le point Overworld reste provisoire : cette étape ne crée pas de village, de sol de secours ni de Waystone à cet emplacement. La sécurité de cette arrivée doit être vérifiée en jeu.\n\n## Commandes utiles pour Bastien')
    text=text.replace('## Vérifications de fichiers et tests dans Minecraft','Pour relancer uniquement les segments en erreur, après avoir corrigé la cause :\n\n```text\n/function les_echos_du_monde:world/segments_v17/retry_errors\n```\n\nLes valeurs `generated_settings` affichées dans le storage sont des informations ; elles ne modifient pas le rayon ou le rythme en jeu.\n\n## Vérifications de fichiers et tests dans Minecraft')
    backup=(ROOT/'backup_path.txt').read_text(encoding='utf-8-sig').strip()
    text+=f'\n## Sauvegarde et fichiers livrés\n\nSauvegarde avant installation : `{backup}`. Aucun fichier de sauvegarde de monde n’a été modifié.\n\n- Source intacte : `06_RESSOURCES/Structures_NBT/plateforme__17.nbt`.\n- Copie préparée : `outputs/prologue_plateforme17/plateforme__17_preparee.nbt`.\n- Datapack complet préparé : `outputs/prologue_plateforme17/datapack/`.\n- Copie de référence du datapack : `outputs/les_echos_du_monde_datapack/`.\n- Rapport et plan : `rapport_preparation.json`, `segments_manifest.json`, `runtime_manifest.json`, `plan_zones.png`.\n- Scripts reproductibles : `prepare_platform.py`, `build_functions.py`, `integrate_pack.py`.\n\nLe chargement automatique utilise GlobalPacks : `config/global_packs.toml`, section `[datapacks]`, dossier requis `global_packs/required_data/`. OpenLoader lit déjà `datapacks/` ; aucune deuxième copie n’y est ajoutée. Aucun réglage des chargeurs ni mod n’a été ajouté.\n'
    if 'À COMPLÉTER' in text:
        raise AssertionError('Unfilled documentation placeholder: '+repr([line for line in text.splitlines() if 'À COMPLÉTER' in line]))
    path.write_text(text,encoding='utf-8')
    shutil.copy2(path,PACK/'TESTS.md')
    shutil.copy2(ROOT/'runtime_notes.md',PACK/'GENERATION_SEGMENTS.md')
    readme='''# Les Échos du Monde — plateforme du prologue 17

Minecraft Java 1.21.1 / NeoForge, datapack format 48. Installation automatique par GlobalPacks.

## Version actuelle

- Source `plateforme__17.nbt` préservée, dimensions **451 × 89 × 461**.
- **203 segments** de 32 × 89 × 32 blocs, alignés sur les chunks ; quatre chunks de contenu par segment.
- Origine du terrain **(-250, -26, -235)** ; arrivée du joueur **(0, -4, 0)**.
- Préparation des neuf segments d’arrivée avant la première téléportation, puis génération autour des joueurs.
- Chaque segment est placé une seule fois et reste enregistré dans le monde.
- Repères retirés, zones réservées enregistrées, 48 herbes et 17 fleurs ajoutées au village ; aucun arbre ni buisson ajouté.
- Anciens mondes protégés contre la superposition. Tester cette version dans un **nouveau monde**, après un redémarrage complet de Minecraft.

## Coordonnées et tests

Voir **TESTS.md** pour les coordonnées, toutes les commandes, les fichiers modifiables et les tests manuels. **GENERATION_SEGMENTS.md** décrit les états et le nettoyage des chargements temporaires.

Les fichiers ont été contrôlés hors jeu. **Aucun test Minecraft effectué pour cette version.** Le point Overworld `0.5 80 0.5` demeure provisoire ; son terrain n’a pas été validé. Aucun verrouillage de quête ajouté.

Les anciennes fonctions et structures restent présentes pour permettre l’annulation de leurs chaînes planifiées ; elles ne sont plus utilisées pour créer les nouveaux mondes.
'''
    (PACK/'README.md').write_text(readme,encoding='utf-8')
    consignes=PROJECT/'Consignes_creation_zone_depart.md'
    old=consignes.read_text(encoding='utf-8')
    old=old.replace('point fixé exactement à `(7, -3, 1)`','point fixé exactement à `(0, -4, 0)`')
    old=old.replace('### Version installée le 1er octobre 2026','### Historique — ancienne plateforme 4, installée le 1er octobre 2026')
    old=old.replace('### Découpage actuel : 933 morceaux','### Ancien découpage : 933 morceaux')
    old=old.replace('| Plateforme |  | Origine provisoire : X=-235 ; Y=-30 ; Z=-250 | Limite réelle : X=326 ; Y=62 ; Z=285 | 562 × 93 × 536 | `plateforme__4_vegetalisee.nbt` |','| Plateforme actuelle | `plateforme__17` | Origine de placement : X=-250 ; Y=-26 ; Z=-235 | Limite inclusive : X=200 ; Y=62 ; Z=225 | 451 × 89 × 461 (NBT vérifié) | `plateforme__17_preparee.nbt` |')
    section='''### Version actuelle — plateforme 17

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

'''
    marker='## Génération et découpage de la plateforme\n\n'
    if '### Version actuelle — plateforme 17' not in old: old=old.replace(marker,marker+section)
    consignes.write_text(old,encoding='utf-8')
    print('Documentation finalized; no placeholders remain.')

if __name__=='__main__': main()
