"""List precise created/changed installed files relative to the recorded backup."""
from pathlib import Path
import json
from install_pack import inventory, ROOT, PROJECT, STAGE, LIVE

def main():
    backup=Path((ROOT/'backup_path.txt').read_text(encoding='utf-8-sig').strip())
    before=inventory(backup/'datapack_installe_avant'); after=inventory(STAGE)
    created=sorted(set(after)-set(before))
    modified=sorted(name for name in set(after)&set(before) if after[name]!=before[name])
    removed=sorted(set(before)-set(after))
    if removed: raise AssertionError('Unexpected removal')
    document={'installed_root':str(LIVE),'created':created,'modified':modified,'removed':removed,
              'counts':{'created':len(created),'modified':len(modified),'removed':len(removed)},
              'list_is_relative_to_installed_root':True}
    (ROOT/'fichiers_changes.json').write_text(json.dumps(document,ensure_ascii=False,indent=2),encoding='utf-8')
    text=f'''# Fichiers livrés — plateforme 17

## Installation

Datapack installé : `{LIVE}`.

**{len(created)} fichiers créés et {len(modified)} fichiers modifiés** par rapport au datapack sauvegardé. Aucun fichier supprimé. Liste exhaustive dans `fichiers_changes.json`, chemins relatifs au dossier ci-dessus. Les **{len(after):,} fichiers** du datapack installé correspondent aux empreintes de la copie préparée.

## Principaux fichiers créés

- `data/les_echos_du_monde/structure/platform_segments_v17/` : **203 NBT** de 32 × 89 × 32 blocs.
- `data/les_echos_du_monde/function/world/segments_v17/` : **1 249 fonctions** de génération, attente, pause, reprise et contrôle.
- `data/les_echos_du_monde/function/player/teleport_to_prologue.mcfunction` : arrivée du joueur.
- `data/les_echos_du_monde/function/world/detect_exit.mcfunction` : zone de sortie.
- `data/les_echos_du_monde/function/world/pause_legacy_automation.mcfunction` : annulation des anciennes chaînes.
- `data/les_echos_du_monde/structure/ferme.nbt`, `poke_shop.nbt`, `poke_centre.nbt` : sources existantes copiées sans modification, disponibles aux blocs LOAD.
- `GENERATION_SEGMENTS.md` et archives de documentation précédente.

## Fichiers modifiés dans le datapack

'''
    for name in modified: text+=f'- `{name}`\n'
    text+='''
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
'''
    (ROOT/'FICHIERS_LIVRES.md').write_text(text,encoding='utf-8')
    if (backup/'Consignes_creation_zone_depart_avant.md').exists():
        print(json.dumps(document['counts']))
        return
    # Reconstruct the previous instruction document by reversing only this task's
    # known edits; label it explicitly rather than claim an unknown original hash.
    current=(PROJECT/'Consignes_creation_zone_depart.md').read_text(encoding='utf-8')
    start=current.index('### Version actuelle — plateforme 17')
    end=current.index('### Historique — ancienne plateforme 4, installée le 1er octobre 2026')
    prior=current[:start]+current[end:]
    prior=prior.replace('### Historique — ancienne plateforme 4, installée le 1er octobre 2026','### Version installée le 1er octobre 2026')
    prior=prior.replace('### Ancien découpage : 933 morceaux','### Découpage actuel : 933 morceaux')
    prior=prior.replace('point fixé exactement à `(0, -4, 0)`','point fixé exactement à `(7, -3, 1)`')
    prior=prior.replace('| Plateforme actuelle | `plateforme__17` | Origine de placement : X=-250 ; Y=-26 ; Z=-235 | Limite inclusive : X=200 ; Y=62 ; Z=225 | 451 × 89 × 461 (NBT vérifié) | `plateforme__17_preparee.nbt` |','| Plateforme |  | Origine provisoire : X=-235 ; Y=-30 ; Z=-250 | Limite réelle : X=326 ; Y=62 ; Z=285 | 562 × 93 × 536 | `plateforme__4_vegetalisee.nbt` |')
    (backup/'Consignes_creation_zone_depart_avant_reconstitue.md').write_text(prior,encoding='utf-8')
    print(json.dumps(document['counts']))

if __name__=='__main__': main()
