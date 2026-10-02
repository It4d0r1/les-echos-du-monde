"""Integrate the prepared platform/runtime into a staging copy of the current pack."""
from pathlib import Path
import hashlib
import json
import shutil

ROOT=Path(__file__).resolve().parent
PACK=ROOT/'datapack'
FUNC=PACK/'data/les_echos_du_monde/function'
STORAGE='les_echos_du_monde:state'
NS='les_echos_du_monde'
RUNTIME=f'{NS}:world/segments_v17'

def write(name,content):
    path=FUNC/(name+'.mcfunction'); path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(content.strip()+'\n',encoding='utf-8')

def main():
    legacy=FUNC/'world/pause_legacy_automation.mcfunction'
    if not legacy.exists(): shutil.copy2(FUNC/'world/pause_automation.mcfunction',legacy)
    write('load',f'''
# Scores persist across reloads. "Already exists" for an objective is harmless.
scoreboard objectives add edm_internal dummy
execute unless data storage {STORAGE} initialized run function {NS}:world/initialize
function {RUNTIME}/setup
function {NS}:world/leaves_v17/setup
execute unless data storage {STORAGE} {{platform_layout:"segments_v17"}} run function {NS}:world/guard_existing_prologue
scoreboard players set #platform_ui_clock edm_internal 0
''')
    write('world/initialize',f'''
# New worlds only. Do not reset existing platform/player progress.
setworldspawn 0 80 0
gamerule spawnRadius 0
data modify storage {STORAGE} initialized set value 1b
data modify storage {STORAGE} platform_layout set value "segments_v17"
data remove storage {STORAGE} prologue_automation_paused
data remove storage {STORAGE} platform_requires_new_world
''')
    write('world/guard_existing_prologue',f'''
# Cancel previous placement chains once, retaining their ownership cleanup.
execute unless data storage {STORAGE} legacy_cleanup_done run function {NS}:world/pause_legacy_automation
data modify storage {STORAGE} legacy_cleanup_done set value 1b
function {NS}:world/pause_automation
data modify storage {STORAGE} platform_requires_new_world set value 1b
''')
    write('world/pause_automation',f'''
# Pause generation and first arrival. The automatic exit remains available.
data modify storage {STORAGE} prologue_automation_paused set value 1b
function {RUNTIME}/pause_internal
''')
    write('world/resume_automation',f'''
execute unless data storage {STORAGE} {{platform_layout:"segments_v17"}} run tellraw @s {{"text":"Ce monde utilise une ancienne plateforme. La nouvelle génération reste bloquée pour protéger les constructions.","color":"red"}}
execute unless data storage {STORAGE} {{platform_layout:"segments_v17"}} run return 0
data remove storage {STORAGE} prologue_automation_paused
function {RUNTIME}/enable
''')
    write('player/teleport_to_prologue',f'''
# Change the player arrival here. Moving the terrain requires regenerating segments.
return run execute in {NS}:prologue run tp @s 0 -4 0
''')
    write('player/first_join',f'''
execute unless data storage {STORAGE} {{platform_layout:"segments_v17"}} run return 0
execute if data storage {STORAGE} {{prologue_automation_paused:1b}} run return 0
execute unless score #enabled edm_seg_ctl matches 1 run return 0
execute unless data storage {NS}:segments_v17 {{spawn_ready:1b}} run return 0
scoreboard players set #prologue_tp edm_internal 0
execute store success score #prologue_tp edm_internal run function {NS}:player/teleport_to_prologue
execute if score #prologue_tp edm_internal matches 1 run tag @s add edm_prologue_done
execute if score #prologue_tp edm_internal matches 1 run tag @s remove edm_prologue_waiting
''')
    write('player/exit',f'''
# Provisional destination. Change X/Y/Z here once the Garrik village location is fixed.
scoreboard players set #overworld_tp edm_internal 0
execute in minecraft:overworld store success score #overworld_tp edm_internal run tp @s 0.5 80 0.5
execute if score #overworld_tp edm_internal matches 1 run tag @s add edm_prologue_done
execute if score #overworld_tp edm_internal matches 1 run tag @s remove edm_prologue_waiting
''')
    write('world/detect_exit',f'''
# Box coordinates: X=-1..1, Y=-4..-2, Z=6..8. Change this selector to move the exit.
# Only the current dimension's players are considered, even while generation is paused.
execute in {NS}:prologue as @a[tag=edm_prologue_done,x=-1,y=-4,z=6,dx=2,dy=2,dz=2] run function {NS}:player/exit
''')
    write('tick',f'''
execute if data storage {STORAGE} {{platform_requires_new_world:1b}} as @a[tag=!edm_prologue_update_notice] run function {NS}:player/report_existing_world
function {RUNTIME}/tick
function {NS}:world/leaves_v17/tick
execute if data storage {STORAGE} {{platform_layout:"segments_v17"}} unless data storage {STORAGE} {{prologue_automation_paused:1b}} if score #enabled edm_seg_ctl matches 1 unless data storage {NS}:segments_v17 {{spawn_ready:1b}} as @a[tag=!edm_prologue_done,tag=!edm_prologue_waiting] run function {NS}:player/wait_prologue
execute if data storage {STORAGE} {{platform_layout:"segments_v17"}} unless data storage {STORAGE} {{prologue_automation_paused:1b}} if score #enabled edm_seg_ctl matches 1 if data storage {NS}:segments_v17 {{spawn_ready:1b}} as @a[tag=!edm_prologue_done] at @s run function {NS}:player/first_join
scoreboard players add #platform_ui_clock edm_internal 1
execute if score #platform_ui_clock edm_internal matches 20.. if score #enabled edm_seg_ctl matches 1 run title @a[tag=edm_prologue_waiting] actionbar {{"text":"Préparation du terrain de départ…","color":"gold"}}
execute if score #platform_ui_clock edm_internal matches 20.. unless score #enabled edm_seg_ctl matches 1 run title @a[tag=edm_prologue_waiting] actionbar {{"text":"La génération du prologue est en pause.","color":"gray"}}
execute if score #platform_ui_clock edm_internal matches 20.. run scoreboard players set #platform_ui_clock edm_internal 0
function {NS}:world/detect_exit
''')
    buildings=Path(r'C:\Users\Bastien\curseforge\minecraft\Instances\Pixelmon Les Échos du Monde\saves\Nouveau monde\generated\les_echos_du_monde\structures')
    expected={'ferme':'8a76e2d9624feb45d4a6bea8465038d4df588fc0e6ff04390097aab3cc62f2d7',
              'poke_shop':'5097717dc59eeecd935f0bd11c05c2bfcb22c79b871003745dcea20dca3bd303',
              'poke_centre':'e2edb92f029c3285a6d7a693b040e9e02334cb7b93dc4b808cd63948a2b5f69b'}
    for name,sha in expected.items():
        source=buildings/(name+'.nbt')
        if hashlib.sha256(source.read_bytes()).hexdigest()!=sha: raise ValueError('Building source changed: '+name)
        shutil.copy2(source,PACK/f'data/{NS}/structure/{name}.nbt')
    # Preserve earlier user documents, then publish current documentation.
    archive=PACK/'documentation_versions_precedentes'; archive.mkdir(exist_ok=True)
    for name in ('README.md','TESTS.md'):
        file=PACK/name
        if file.exists() and not (archive/name).exists(): shutil.copy2(file,archive/name)
    print(json.dumps({'staging':str(PACK),'building_sources_preserved':list(expected),'layout':'segments_v17'},ensure_ascii=False))

if __name__=='__main__': main()
