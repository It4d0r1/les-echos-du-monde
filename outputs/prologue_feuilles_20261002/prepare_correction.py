"""Back up v17, record unsupported oak fragments, and build an exact-position repair."""
from collections import defaultdict
from datetime import datetime
import json
from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parents[1]
WORK=PROJECT/'outputs/prologue_plateforme17'
PACK=WORK/'datapack'
LIVE=Path(r'C:\Users\Bastien\curseforge\minecraft\Instances\Pixelmon Les Échos du Monde\global_packs\required_data\les_echos_du_monde')
ORIGIN=(-250,-26,-235)
NS='les_echos_du_monde'
BASE=f'{NS}:world/leaves_v17'

def identifier(prefix,x,z):
    part=lambda n:('m' if n<0 else 'p')+f'{abs(n):02d}'
    return f'{prefix}_{part(x)}_{part(z)}'

def write(name,lines):
    file=PACK/f'data/{NS}/function/world/leaves_v17/{name}.mcfunction'
    file.parent.mkdir(parents=True,exist_ok=True)
    file.write_text('\n'.join(lines)+'\n',encoding='utf-8')

def main():
    report=json.loads((ROOT/'diagnostic_feuilles.json').read_text(encoding='utf-8'))
    selected=[c for c in report['components'] if c['floating_no_support']
              and set(c['blocks'])=={'minecraft:oak_leaves'}
              and c['nearest_wood']['minimum_bbox_manhattan']>6]
    positions=sorted({tuple(pos) for c in selected for pos in c['points_local']})
    if len(positions)!=109 or tuple(report['target_local_xyz']) not in positions:
        raise AssertionError('Unexpected correction selection; review before changing the pack.')
    persistent_records=json.loads((ROOT/'persistent_orphans.json').read_text(encoding='utf-8'))
    persistent_positions={tuple(p['local']) for p in persistent_records}
    if len(persistent_positions)!=6 or not persistent_positions.issubset(positions):
        raise AssertionError('Unexpected persistent source fragments')
    backup=PROJECT/'backups'/('feuilles_prologue_'+datetime.now().strftime('%Y%m%d_%H%M%S'))
    if (ROOT/'backup_path.txt').exists():
        backup=Path((ROOT/'backup_path.txt').read_text(encoding='utf-8-sig').strip())
    else:
        backup.mkdir(parents=True,exist_ok=False)
        shutil.copytree(LIVE,backup/'datapack_installe_avant')
        working=backup/'travail_avant'; working.mkdir()
        for path in WORK.iterdir():
            if path.is_file(): shutil.copy2(path,working/path.name)
        shutil.copy2(PROJECT/'Consignes_creation_zone_depart.md',backup/'Consignes_creation_zone_depart_avant.md')
        (ROOT/'backup_path.txt').write_text(str(backup)+'\n',encoding='utf-8')
    (WORK/'backup_path.txt').write_text(str(backup)+'\n',encoding='utf-8')
    manifest={'source_sha256':report['source_sha256'],'origin_xyz':list(ORIGIN),
              'revision':'floating_oak_20261002','removed_block':'minecraft:oak_leaves',
              'count':len(positions),'component_count':len(selected),'positions_local':positions,
              'persistent_source_positions_local':sorted(persistent_positions),
              'criterion':'Unsupported oak-only 26-connected fragments, no adjacent trunk/ground/decor, nearest log more than6 Manhattan blocks from boundingbox. Cherry and azalea fragments left unchanged.'}
    (ROOT/'feuilles_a_retirer.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    groups=defaultdict(list)
    for lx,ly,lz in positions:
        x,y,z=lx+ORIGIN[0],ly+ORIGIN[1],lz+ORIGIN[2]
        groups[x//16,z//16].append((x,y,z))
    write('setup',[
        '# Keep completed repair scores across reloads; player progress is untouched.',
        'scoreboard objectives add edm_leaf_fix dummy',
        f'data modify storage {NS}:leaves_v17 revision set value "floating_oak_20261002"',
        f'data modify storage {NS}:leaves_v17 known_orphan_positions set value {len(positions)}',
    ])
    tick=[f'execute unless data storage {NS}:state {{platform_layout:"segments_v17"}} run return 0',
          f'execute if data storage {NS}:state {{prologue_automation_paused:1b}} run return 0',
          'execute unless score #enabled edm_seg_ctl matches 1 run return 0',
          '# Inspect only already placed, loaded chunks. This repair adds no force-load tickets.']
    for (cx,cz),coords in sorted(groups.items()):
        chunk=identifier('c',cx,cz); seg=identifier('s',cx//2,cz//2)
        tick.append(f'execute in {NS}:prologue if score {seg} edm_seg_done matches 1 unless score {chunk} edm_leaf_fix matches 1 if loaded {cx*16} 0 {cz*16} run function {BASE}/chunks/{chunk}')
        lines=['# Exact orphan positions recorded in the original export; preserve other blocks and different leaf states.']
        for x,y,z in coords:
            local=(x-ORIGIN[0],y-ORIGIN[1],z-ORIGIN[2])
            props='persistent=true,distance=7,waterlogged=false' if local in persistent_positions else 'persistent=false'
            lines.append(f'execute if block {x} {y} {z} minecraft:oak_leaves[{props}] run setblock {x} {y} {z} minecraft:air')
        lines.append(f'scoreboard players set {chunk} edm_leaf_fix 1')
        write('chunks/'+chunk,lines)
    write('tick',tick)
    write('status',[f'data get storage {NS}:leaves_v17','scoreboard players list'])
    manifest['cleanup_chunks']=len(groups)
    manifest['backup_path']=str(backup)
    (ROOT/'rapport_correctif.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'leaves':len(positions),'components':len(selected),'chunks':len(groups),'backup':str(backup)},ensure_ascii=False),flush=True)

if __name__=='__main__': main()
