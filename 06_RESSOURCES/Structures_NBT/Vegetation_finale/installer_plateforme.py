"""Decoupe, verifie, sauvegarde et installe la plateforme vegetalisee.

Ne modifie aucun monde, aucun JAR ni le NBT source. Installation pour nouveaux
mondes; les sauvegardes preexistantes sont mises en pause lors de leur chargement.
"""
from __future__ import annotations
import argparse
import collections
import datetime
import gzip
import hashlib
import json
import pathlib
import re
import shutil
import struct
import time
import numpy as np
from generer_vegetation import Structure, Reader, named, palette_record

HERE=pathlib.Path(__file__).resolve().parent
PROJECT=HERE.parents[2]
PACK=pathlib.Path(r'C:\Users\Bastien\curseforge\minecraft\Instances\Pixelmon Les Échos du Monde\global_packs\required_data\les_echos_du_monde')
ORIGIN=(-235,-30,-250)
ARRIVAL=(7,-3,1)
VERSION='vegetation_20261001'
EXPECTED_SHA='d86156a622a9e9bc9333f1ea80d181144b11423106ec9c0739916250385c89e3'
MASK=(1<<256)-1
FUNC='data/les_echos_du_monde/function'
STRUCT='data/les_echos_du_monde/structure/prologue_vegetation_chunks'

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def write_text(root,relative,content):
    path=root/relative; path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(content.strip()+'\n',encoding='utf-8')

def iter_records(s):
    r=Reader(s.data); r.p=s.blocks_start
    for _ in range(s.count):
        start=r.p; pos=state=po=so=None; has_nbt=False
        while True:
            t=r.u8()
            if not t: break
            name=r.string()
            if name=='pos':
                if t==9:
                    if r.u8()!=3 or r.i32()!=3: raise ValueError('pos non standard')
                elif t==11:
                    if r.i32()!=3: raise ValueError('pos non standard')
                else: raise ValueError('type pos inconnu')
                po=r.p-start; pos=struct.unpack_from('>iii',s.data,r.p); r.p+=12
            elif name=='state':
                if t!=3: raise ValueError('state non entier')
                so=r.p-start; state=r.i32()
            else:
                if name=='nbt': has_nbt=True
                r.skip(t)
        if pos is None or state is None: raise ValueError('bloc incomplet')
        yield pos,state,has_nbt,s.data[start:r.p],po,so
    if r.p!=s.blocks_end: raise ValueError('liste blocks incoherente')

def rebase(raw,po,so,pos,state):
    b=bytearray(raw); struct.pack_into('>iii',b,po,*pos); struct.pack_into('>i',b,so,state)
    return b

def write_tile(s,path,buffer,states,count):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('wb') as f:
        with gzip.GzipFile(filename='',fileobj=f,mode='wb',mtime=0,compresslevel=6) as g:
            g.write(s.header)
            for name,t,start,payload,end in s.fields:
                if name=='size': g.write(named(9,'size',bytes([3])+struct.pack('>iiii',3,16,s.Y,16)))
                elif name=='palette':
                    g.write(named(9,'palette',bytes([10])+struct.pack('>i',len(states))))
                    for st in states: g.write(palette_record(s.palette[st]))
                elif name=='blocks':
                    g.write(named(9,'blocks',bytes([10])+struct.pack('>i',count))); g.write(buffer)
                else: g.write(s.data[start:end])
            g.write(b'\0')

def prepare_tiles(s,stage):
    if s.size!=(562,93,536) or s.meta.get('DataVersion')!=3955: raise ValueError('NBT inattendu')
    if s.meta.get('entities'): raise ValueError('Gestion des entites requise avant decoupage')
    buckets={}; grid=np.full((s.Y,s.Z,s.X),65535,np.uint16); checksum=0; nbt_count=0
    for i,(pos,st,has_nbt,raw,po,so) in enumerate(iter_records(s)):
        x,y,z=pos
        if not (0<=x<s.X and 0<=y<s.Y and 0<=z<s.Z and 0<=st<len(s.palette)): raise ValueError('bloc hors volume/palette')
        if grid[y,z,x]!=65535: raise ValueError('Position dupliquee dans la source')
        grid[y,z,x]=st; checksum=(checksum+int.from_bytes(hashlib.sha256(raw).digest(),'big'))&MASK
        nbt_count+=has_nbt
        wx,wz=x+ORIGIN[0],z+ORIGIN[2]; cx,cz=wx//16,wz//16
        b=buckets.setdefault((cx,cz),{'raw':bytearray(),'states':[],'map':{},'count':0})
        if st not in b['map']: b['map'][st]=len(b['states']); b['states'].append(st)
        b['raw'].extend(rebase(raw,po,so,(wx-cx*16,y,wz-cz*16),b['map'][st])); b['count']+=1
        if i and i%1000000==0: print(f'Decoupage : {i:,}/{s.count:,} blocs',flush=True)
    acx,acz=ARRIVAL[0]//16,ARRIVAL[2]//16
    ordered=sorted(buckets,key=lambda p:(max(abs(p[0]-acx),abs(p[1]-acz)),
                                        (p[0]-acx)**2+(p[1]-acz)**2,p[1],p[0]))
    if ordered[0]!=(acx,acz): raise ValueError('Chunk d arrivee absent')
    manifest=[]
    for i,(cx,cz) in enumerate(ordered):
        b=buckets.pop((cx,cz)); fn=f'chunk_{i:04d}'
        path=stage/STRUCT/(fn+'.nbt'); write_tile(s,path,b['raw'],b['states'],b['count'])
        manifest.append({'id':fn,'chunk':[cx,cz],'placement':[cx*16,ORIGIN[1],cz*16],
                         'blocks':b['count'],'original_palette_indices':b['states'],
                         'bytes':path.stat().st_size,'sha256':sha(path)})
    print(f'{len(manifest)} morceaux ecrits. Controle integral en cours.',flush=True)
    reconstructed=np.full(grid.shape,65535,np.uint16); restored_checksum=0; restored_count=0; restored_nbt=0
    for i,m in enumerate(manifest):
        tile=Structure(stage/STRUCT/(m['id']+'.nbt'))
        expected_meta=dict(s.meta,size=[16,s.Y,16])
        if tile.meta!=expected_meta: raise ValueError('Metadonnees de tuile inattendues')
        if tile.count!=m['blocks'] or tile.palette!=[s.palette[k] for k in m['original_palette_indices']]: raise ValueError('Tuile incorrecte')
        for pos,st,has_nbt,raw,po,so in iter_records(tile):
            x,y,z=pos
            if not (0<=x<16 and 0<=y<s.Y and 0<=z<16): raise ValueError('Bloc hors morceau')
            ox=x+m['placement'][0]-ORIGIN[0]; oz=z+m['placement'][2]-ORIGIN[2]
            if not (0<=ox<s.X and 0<=oz<s.Z): raise ValueError('Bloc hors source reconstituee')
            original_st=m['original_palette_indices'][st]
            if reconstructed[y,oz,ox]!=65535: raise ValueError('Chevauchement de morceaux')
            reconstructed[y,oz,ox]=original_st
            normalized=rebase(raw,po,so,(ox,y,oz),original_st)
            restored_checksum=(restored_checksum+int.from_bytes(hashlib.sha256(normalized).digest(),'big'))&MASK
            restored_count+=1; restored_nbt+=has_nbt
        if i and i%200==0: print(f'Controle : {i}/{len(manifest)} morceaux',flush=True)
    if restored_count!=s.count or restored_checksum!=checksum or not np.array_equal(grid,reconstructed) or restored_nbt!=nbt_count:
        raise ValueError('La reconstitution ne correspond pas a la source')
    for wx in (6,7):
        for wz in (0,1):
            sx,sz=wx-ORIGIN[0],wz-ORIGIN[2]
            for wy in (-4,-3,-2):
                st=int(reconstructed[wy-ORIGIN[1],sz,sx]); name=s.palette[st]['Name']
                if name!=('minecraft:grass_block' if wy==-4 else 'minecraft:air'): raise ValueError('Arrivee incompatible apres decoupage')
    return manifest,{'blocks':restored_count,'block_entities':restored_nbt,'exact_grid_match':True,
                     'normalized_records_multiset_sha256_sum':f'{checksum:064x}',
                     'records_and_nbt_preserved':True,'overlaps':0,'missing_blocks':0,'arrival_verified':True}

def chunk_function(m,index,total):
    fn=m['id']; x,y,z=m['placement']; target=f'les_echos_du_monde:world/vegetation_chunks/{fn}'
    next_target=f'les_echos_du_monde:world/vegetation_chunks/chunk_{index+1:04d}'
    lines=[f'# Morceau {index+1}/{total}, chunk monde {m["chunk"]}.',
           'execute if data storage les_echos_du_monde:state {prologue_automation_paused:1b} run return 0',
           'execute unless data storage les_echos_du_monde:state platform_building run return 0',
           f'execute unless data storage les_echos_du_monde:state {{platform_layout:"{VERSION}"}} run return 0',
           f'execute in les_echos_du_monde:prologue unless data storage les_echos_du_monde:state platform_tile_forced if loaded {x} {y} {z} run data modify storage les_echos_du_monde:state platform_tile_loaded set value 1b',
           'execute unless data storage les_echos_du_monde:state platform_tile_forced run scoreboard players set #platform_forceload_added edm_internal 0',
           f'execute in les_echos_du_monde:prologue unless data storage les_echos_du_monde:state platform_tile_forced unless data storage les_echos_du_monde:state platform_tile_loaded store success score #platform_forceload_added edm_internal run forceload add {x} {z}',
           'execute unless data storage les_echos_du_monde:state platform_tile_forced if score #platform_forceload_added edm_internal matches 1 run data modify storage les_echos_du_monde:state platform_tile_owned set value 1b',
           'execute unless data storage les_echos_du_monde:state platform_tile_forced run scoreboard players set #platform_wait edm_internal 0',
           'data modify storage les_echos_du_monde:state platform_tile_forced set value 1b',
           'data remove storage les_echos_du_monde:state platform_tile_loaded',
           f'execute in les_echos_du_monde:prologue if loaded {x} {y} {z} if loaded {x+15} {y} {z+15} run data modify storage les_echos_du_monde:state platform_tile_loaded set value 1b',
           'scoreboard players set #platform_place edm_internal 0',
           f'execute in les_echos_du_monde:prologue if data storage les_echos_du_monde:state platform_tile_loaded store success score #platform_place edm_internal run place template les_echos_du_monde:prologue_vegetation_chunks/{fn} {x} {y} {z}',
           f'execute in les_echos_du_monde:prologue if score #platform_place edm_internal matches 1 if data storage les_echos_du_monde:state {{platform_tile_owned:1b}} run forceload remove {x} {z}',
           'execute if score #platform_place edm_internal matches 1 run data remove storage les_echos_du_monde:state platform_tile_owned',
           'execute if score #platform_place edm_internal matches 1 run data remove storage les_echos_du_monde:state platform_tile_forced',
           'execute if score #platform_place edm_internal matches 1 run data remove storage les_echos_du_monde:state platform_tile_loaded',
           f'execute if score #platform_place edm_internal matches 1 run scoreboard players set #platform_progress edm_internal {index+1}']
    if index+1<total: lines.append(f'execute if score #platform_place edm_internal matches 1 run schedule function {next_target} 1t replace')
    else: lines.append('execute if score #platform_place edm_internal matches 1 run function les_echos_du_monde:world/finish_platform')
    lines += ['execute if score #platform_place edm_internal matches 1 run return 1',
              'execute if data storage les_echos_du_monde:state platform_tile_loaded run data modify storage les_echos_du_monde:state platform_error_reason set value "placement_refused"',
              'execute if data storage les_echos_du_monde:state platform_tile_loaded run data modify storage les_echos_du_monde:state platform_error set value 1b',
              'scoreboard players add #platform_wait edm_internal 1',
              'execute if score #platform_wait edm_internal matches 200.. unless data storage les_echos_du_monde:state platform_tile_loaded run data modify storage les_echos_du_monde:state platform_error_reason set value "chunk_load_timeout"',
              'execute if score #platform_wait edm_internal matches 200.. run data modify storage les_echos_du_monde:state platform_error set value 1b',
              f'execute if data storage les_echos_du_monde:state platform_error run data modify storage les_echos_du_monde:state platform_error_tile set value {index}',
              f'execute in les_echos_du_monde:prologue if data storage les_echos_du_monde:state platform_error if data storage les_echos_du_monde:state {{platform_tile_owned:1b}} run forceload remove {x} {z}',
              'execute if data storage les_echos_du_monde:state platform_error run data remove storage les_echos_du_monde:state platform_tile_owned',
              'execute if data storage les_echos_du_monde:state platform_error run data remove storage les_echos_du_monde:state platform_tile_forced',
              'execute if data storage les_echos_du_monde:state platform_error run data remove storage les_echos_du_monde:state platform_tile_loaded',
              'execute if data storage les_echos_du_monde:state platform_error run data remove storage les_echos_du_monde:state platform_building',
              f'execute unless data storage les_echos_du_monde:state platform_error run schedule function {target} 1t replace']
    return '\n'.join(lines)

def prepare_functions(stage,manifest):
    total=len(manifest)
    for i,m in enumerate(manifest): write_text(stage,FUNC+'/world/vegetation_chunks/'+m['id']+'.mcfunction',chunk_function(m,i,total))
    def func(name,text): write_text(stage,FUNC+'/'+name+'.mcfunction',text)
    func('load',f'''
# Nouveau monde : initialise l'origine de cette version. Ancien monde : pause explicite.
execute unless data storage les_echos_du_monde:state initialized run function les_echos_du_monde:world/initialize
execute unless data storage les_echos_du_monde:state platform_score_ready run function les_echos_du_monde:world/setup_platform_score
execute unless data storage les_echos_du_monde:state {{platform_layout:"{VERSION}"}} run function les_echos_du_monde:world/guard_existing_prologue
scoreboard players set #platform_ui_clock edm_internal 0
''')
    initialize=(PACK/FUNC/'world/initialize.mcfunction').read_text(encoding='utf-8').split('data modify storage les_echos_du_monde:state platform_layout')[0].strip()
    func('world/initialize',initialize+f'\ndata modify storage les_echos_du_monde:state platform_layout set value "{VERSION}"\ndata remove storage les_echos_du_monde:state prologue_automation_paused\ndata remove storage les_echos_du_monde:state platform_requires_new_world')
    func('world/guard_existing_prologue','''
# Evite de superposer automatiquement deux modeles d'origines differentes dans une ancienne sauvegarde.
function les_echos_du_monde:world/pause_automation
data modify storage les_echos_du_monde:state platform_requires_new_world set value 1b
''')
    func('tick','''
execute if data storage les_echos_du_monde:state {platform_requires_new_world:1b} as @a[tag=!edm_prologue_update_notice] run function les_echos_du_monde:player/report_existing_world
execute unless data storage les_echos_du_monde:state {prologue_automation_paused:1b} if entity @a unless data storage les_echos_du_monde:state platform_placed unless data storage les_echos_du_monde:state platform_building unless data storage les_echos_du_monde:state platform_error run function les_echos_du_monde:world/place_platform
execute unless data storage les_echos_du_monde:state {prologue_automation_paused:1b} unless data storage les_echos_du_monde:state platform_placed as @a[tag=!edm_prologue_done,tag=!edm_prologue_waiting] run function les_echos_du_monde:player/wait_prologue
execute unless data storage les_echos_du_monde:state {prologue_automation_paused:1b} if data storage les_echos_du_monde:state platform_building run scoreboard players add #platform_ui_clock edm_internal 1
execute unless data storage les_echos_du_monde:state {prologue_automation_paused:1b} if data storage les_echos_du_monde:state platform_building if score #platform_ui_clock edm_internal matches 20.. run function les_echos_du_monde:world/report_progress
execute unless data storage les_echos_du_monde:state {prologue_automation_paused:1b} if data storage les_echos_du_monde:state platform_placed as @a[tag=!edm_prologue_done] at @s run function les_echos_du_monde:player/first_join
execute unless data storage les_echos_du_monde:state {prologue_automation_paused:1b} as @a[tag=!edm_platform_error_reported] if data storage les_echos_du_monde:state platform_error run function les_echos_du_monde:player/report_platform_error
execute unless data storage les_echos_du_monde:state {prologue_automation_paused:1b} if data storage les_echos_du_monde:state platform_placed in les_echos_du_monde:prologue as @a[tag=edm_prologue_done,x=-1,y=-4,z=6,dx=2,dy=2,dz=2] run function les_echos_du_monde:player/exit
''')
    func('player/wait_prologue','''
tag @s add edm_prologue_waiting
tellraw @s {"text":"La zone de départ se prépare. Tu seras envoyé dans le prologue dès qu'elle sera prête.","color":"gold"}
''')
    func('player/first_join','''
# Coordonnees exactes, apres placement integral et verification hors jeu du sol.
execute unless data storage les_echos_du_monde:state platform_placed run return 0
scoreboard players set #prologue_tp edm_internal 0
execute in les_echos_du_monde:prologue store success score #prologue_tp edm_internal run tp @s 7 -3 1
execute if score #prologue_tp edm_internal matches 1 run tag @s add edm_prologue_done
execute if score #prologue_tp edm_internal matches 1 run tag @s remove edm_prologue_waiting
''')
    func('player/report_existing_world','''
tag @s add edm_prologue_update_notice
tellraw @s {"text":"Le prologue a été renouvelé. Crée un nouveau monde pour essayer cette version sans superposer les plateformes.","color":"gold"}
''')
    func('world/place_platform',f'''
execute if data storage les_echos_du_monde:state {{prologue_automation_paused:1b}} run return 0
execute unless data storage les_echos_du_monde:state {{platform_layout:"{VERSION}"}} run return 0
data remove storage les_echos_du_monde:state platform_error
data remove storage les_echos_du_monde:state platform_error_tile
data remove storage les_echos_du_monde:state platform_error_reason
data remove storage les_echos_du_monde:state platform_tile_forced
data remove storage les_echos_du_monde:state platform_tile_loaded
data remove storage les_echos_du_monde:state platform_tile_owned
scoreboard players set #platform_wait edm_internal 0
scoreboard players set #platform_place edm_internal 0
scoreboard players set #platform_progress edm_internal 0
scoreboard players set #platform_total edm_internal {total}
scoreboard players set #platform_ui_clock edm_internal 0
data modify storage les_echos_du_monde:state platform_building set value 1b
schedule function les_echos_du_monde:world/vegetation_chunks/chunk_0000 1t replace
''')
    func('world/report_progress','''
scoreboard players set #platform_ui_clock edm_internal 0
execute as @a[tag=!edm_prologue_done] run title @s actionbar [{"text":"Préparation du prologue : ","color":"gold"},{"score":{"name":"#platform_progress","objective":"edm_internal"}},{"text":" / "},{"score":{"name":"#platform_total","objective":"edm_internal"}}]
''')
    func('world/finish_platform','''
data modify storage les_echos_du_monde:state platform_placed set value 1b
data remove storage les_echos_du_monde:state platform_building
execute as @a[tag=edm_prologue_waiting] run title @s actionbar {"text":"Le prologue est prêt.","color":"green"}
''')
    func('player/report_platform_error','''
tag @s add edm_platform_error_reported
tellraw @s {"text":"La préparation du prologue s'est arrêtée. Reste dans l'Overworld et consulte latest.log et le numéro du morceau dans le stockage les_echos_du_monde:state.","color":"red"}
''')
    # Annulation des anciennes chaines conservee pour nettoyer leurs seuls tickets possedes.
    pause=(PACK/FUNC/'world/pause_automation.mcfunction').read_text(encoding='utf-8').split('# Nouvelle plateforme vegetalisee :')[0].strip()
    pause += '\n# Nouvelle plateforme vegetalisee : annule et libere uniquement son ticket possede.\n'
    for m in manifest:
        x,y,z=m['placement']; target='les_echos_du_monde:world/vegetation_chunks/'+m['id']
        pause+=f'execute store success score #edm_cancelled edm_internal run schedule clear {target}\n'
        pause+=f'execute in les_echos_du_monde:prologue if score #edm_cancelled edm_internal matches 1 if data storage les_echos_du_monde:state {{platform_tile_owned:1b}} run forceload remove {x} {z}\n'
        pause+='execute if score #edm_cancelled edm_internal matches 1 run data remove storage les_echos_du_monde:state platform_tile_owned\n'
    pause+='data remove storage les_echos_du_monde:state platform_building\ndata remove storage les_echos_du_monde:state platform_tile_forced\ndata remove storage les_echos_du_monde:state platform_tile_loaded\n'
    func('world/pause_automation',pause)
    func('world/resume_automation',f'''
execute unless data storage les_echos_du_monde:state {{platform_layout:"{VERSION}"}} run return 0
data remove storage les_echos_du_monde:state prologue_automation_paused
data remove storage les_echos_du_monde:state platform_error
data remove storage les_echos_du_monde:state platform_error_tile
data remove storage les_echos_du_monde:state platform_error_reason
''')

def verify_functions(stage,manifest):
    union={p.relative_to(PACK/FUNC).with_suffix('').as_posix() for p in (PACK/FUNC).rglob('*.mcfunction')}
    union |= {p.relative_to(stage/FUNC).with_suffix('').as_posix() for p in (stage/FUNC).rglob('*.mcfunction')}
    valid_templates={'prologue_vegetation_chunks/'+m['id'] for m in manifest}
    for p in (stage/FUNC).rglob('*.mcfunction'):
        content=p.read_text(encoding='utf-8')
        for ref in re.findall(r'(?:function|schedule clear) les_echos_du_monde:([a-z0-9_./]+)',content):
            if ref not in union: raise ValueError(f'Reference de fonction manquante {ref}')
        for ref in re.findall(r'place template les_echos_du_monde:([a-z0-9_./]+)',content):
            if ref not in valid_templates: raise ValueError('Modele manquant')
        for line in content.splitlines():
            if 'tellraw ' in line or 'actionbar ' in line:
                suffix=line.split('tellraw @s ',1)[1] if 'tellraw @s ' in line else line.split('actionbar ',1)[1]
                json.loads(suffix)
    for i,m in enumerate(manifest):
        text=(stage/FUNC/'world/vegetation_chunks'/(m['id']+'.mcfunction')).read_text(encoding='utf-8')
        next_refs=re.findall(r'schedule function les_echos_du_monde:world/vegetation_chunks/(chunk_\d+) 1t replace',text)
        expected=([manifest[i+1]['id']] if i+1<len(manifest) else [])+[m['id']]
        if next_refs!=expected: raise ValueError('Chaine de placement invalide')
        success_return=text.index('matches 1 run return 1')
        if text.index('matches 200..')<success_return: raise ValueError('Retour apres logique de nouvelle tentative')
        if 'store success score #platform_forceload_added edm_internal run forceload add' not in text:
            raise ValueError('Resultat de forceload add non verifie')
        owned_line=next(line for line in text.splitlines() if 'platform_tile_owned set value 1b' in line)
        if 'if score #platform_forceload_added edm_internal matches 1' not in owned_line:
            raise ValueError('Possession du ticket sans confirmation de son ajout')
    load=(stage/FUNC/'load.mcfunction').read_text(encoding='utf-8')
    if 'run function les_echos_du_monde:world/pause_automation' in load: raise ValueError('Pause automatique du nouveau monde')
    return {'function_references_present':True,'template_references_present':True,'json_messages_valid':True,
            'all_tiles_linked_once_in_sequence':True,'successful_tile_does_not_reschedule_itself':True,
            'forceload_owned_only_if_added_successfully':True,
            'arrival_waits_for_entire_structure':True,'no_minecraft_runtime_test':True}

def backup_and_install(stage,backup):
    print('Sauvegarde du datapack existant.',flush=True)
    backup.mkdir(parents=True,exist_ok=False); dest=backup/'datapack'
    shutil.copytree(PACK,dest)
    files=[p for p in PACK.rglob('*') if p.is_file()]
    hashes={p.relative_to(PACK).as_posix():sha(p) for p in files}
    for rel,h in hashes.items():
        if sha(dest/rel)!=h: raise ValueError('Sauvegarde incomplete')
    (backup/'sha256.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
    overwritten=[]; added=[]
    for p in sorted(stage.rglob('*'),key=lambda p:p.name=='load.mcfunction'):
        if not p.is_file(): continue
        rel=p.relative_to(stage); target=PACK/rel
        if target.exists(): overwritten.append(rel.as_posix())
        else: added.append(rel.as_posix())
        target.parent.mkdir(parents=True,exist_ok=True)
        temp=target.with_name(target.name+'.installation_tmp'); shutil.copyfile(p,temp); temp.replace(target)
        if sha(target)!=sha(p): raise ValueError(f'Installation incorrecte: {target}')
    return {'backup':str(backup),'backup_files':len(files),'overwritten_files':overwritten,
            'added_files':added,'installed_files_sha256_verified':True}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=pathlib.Path,default=HERE/'plateforme__4_vegetalisee.nbt')
    p.add_argument('--stamp',default=datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
    p.add_argument('--prepare-only',action='store_true')
    a=p.parse_args(); stage_root=HERE/('Installation_'+a.stamp); stage=stage_root/'datapack_patch'
    backup=PROJECT/'90_ARCHIVES'/'Sauvegardes_datapack'/('prologue_vegetation_'+a.stamp)
    if stage_root.exists(): raise ValueError('Dossier de preparation deja existant; choisir un autre --stamp')
    if sha(a.source)!=EXPECTED_SHA: raise ValueError('La copie vegetalisee differe de celle verifiee; refaire les controles avant installation')
    stage.mkdir(parents=True)
    s=Structure(a.source); print(f'Source : {s.count:,} blocs, origine {ORIGIN}',flush=True)
    manifest,verification=prepare_tiles(s,stage); prepare_functions(stage,manifest)
    checks=verify_functions(stage,manifest)
    report={'source':str(a.source),'source_sha256':s.sha256,'origin_provisional':list(ORIGIN),
            'arrival':list(ARRIVAL),'version':VERSION,'tiles':len(manifest),
            'maximum_blocks_per_tile':max(m['blocks'] for m in manifest),
            'maximum_compressed_tile_bytes':max(m['bytes'] for m in manifest),
            'total_tile_bytes':sum(m['bytes'] for m in manifest),'nbt_verification':verification,
            'function_checks':checks,'manifest':manifest,'tested_in_minecraft':False}
    if not a.prepare_only: report['installation']=backup_and_install(stage,backup)
    if sha(a.source)!=s.sha256: raise ValueError('Source modifiee pendant le travail')
    (stage_root/'rapport_installation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    text=f'''INSTALLATION DU PROLOGUE VÉGÉTALISÉ
Datapack : {PACK}
Origine provisoire : -235, -30, -250. Arrivée exacte : 7, -3, 1.
{len(manifest)} morceaux alignés sur les chunks, en partant du chunk 0, 0.
{s.count:,} blocs reconstitués à l'identique; données NBT préservées.
Un seul chunk forcé à la fois; attente de son chargement avant placement.
Le joueur reste dans l'Overworld pendant la préparation, avec un indicateur,
puis est téléporté automatiquement lorsque la plateforme entière est placée.
La pause automatique au démarrage des nouveaux mondes a été retirée.
Les anciennes sauvegardes sont mises en pause afin d'éviter la superposition
des modèles. Aucun fichier de monde n'a été modifié par l'installation.
Les fichiers NBT originaux et les anciens morceaux restent conservés.

Sauvegarde avant remplacement : {backup}
Rapport : rapport_installation.json (contrôles, coordonnées et sommes SHA-256).
Minecraft n'a pas été lancé pour tester : les vérifications portent sur les fichiers.

ESSAI : ferme complètement Minecraft, relance le modpack et crée un nouveau monde.
Attends la préparation du prologue dans l'Overworld : l'arrivée est automatique.
En cas d'erreur, conserve latest.log et le stockage les_echos_du_monde:state.
L'origine reste à confirmer visuellement pour la réserve de Garrik.

RETOUR ARRIÈRE : restaurer le dossier datapack de la sauvegarde à la place du
datapack installé, jeu fermé. La sauvegarde contient l'intégralité de la version précédente.
'''
    (stage_root/'INSTALLATION.txt').write_text(text,encoding='utf-8')
    print(json.dumps({k:report[k] for k in ['tiles','maximum_blocks_per_tile','total_tile_bytes','nbt_verification','function_checks']},ensure_ascii=False,indent=2),flush=True)
    print('Installation terminee.' if not a.prepare_only else 'Preparation terminee, non installee.',flush=True)

if __name__=='__main__': main()
