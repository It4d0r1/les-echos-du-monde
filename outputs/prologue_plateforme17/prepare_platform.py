"""Prepare plateforme__17 without changing its source; split into world-aligned 2x2 chunks.

Python + NumPy + Pillow. This script only writes under its output directory.
All source records, including block entity NBT, are copied byte for byte except
the explicitly recorded palette-state edits and segment-local block positions.
"""
from __future__ import annotations
import argparse
import collections
import gzip
import hashlib
import json
from pathlib import Path
import random
import struct
import sys
import types
import numpy as np
from PIL import Image, ImageDraw, ImageFont

PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT / '06_RESSOURCES/Structures_NBT/Vegetation_finale'))
import generer_vegetation as nbt

ORIGIN = (-250, -26, -235)
SPAWN = (0, -4, 0)
SEED = 20261001
BUILDING_MARGIN = 4
PATH_MARGIN = 2
SPAWN_RADIUS = 5

def filled(mask):
    """Fill holes enclosed by a projected marker contour, without filling its bounding box."""
    outside = np.zeros_like(mask)
    q = collections.deque()
    H, W = mask.shape
    for z in range(H):
        for x in (0, W-1):
            if not mask[z,x] and not outside[z,x]:
                outside[z,x] = True; q.append((z,x))
    for x in range(W):
        for z in (0, H-1):
            if not mask[z,x] and not outside[z,x]:
                outside[z,x] = True; q.append((z,x))
    while q:
        z,x = q.popleft()
        for nz,nx in ((z-1,x),(z+1,x),(z,x-1),(z,x+1)):
            if 0 <= nz < H and 0 <= nx < W and not mask[nz,nx] and not outside[nz,nx]:
                outside[nz,nx] = True; q.append((nz,nx))
    return ~outside

def bounds(mask):
    zz,xx = np.where(mask)
    return [[int(xx.min())+ORIGIN[0], int(zz.min())+ORIGIN[2]],
            [int(xx.max())+ORIGIN[0], int(zz.max())+ORIGIN[2]]]

def identifier(sx,sz):
    def part(n): return ('m' if n < 0 else 'p') + f'{abs(n):02d}'
    return f's_{part(sx)}_{part(sz)}'

def relocate(raw, pos):
    prefix = nbt.named(9, 'pos', bytes([3])+struct.pack('>i',3))
    off = raw.find(prefix)
    if off < 0:
        prefix = nbt.named(11, 'pos', struct.pack('>i',3))
        off = raw.find(prefix)
    if off < 0: raise ValueError('Record with no supported pos tag')
    b = bytearray(raw)
    struct.pack_into('>iii', b, off+len(prefix), *pos)
    return b

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source', type=Path, default=PROJECT/'06_RESSOURCES/Structures_NBT/plateforme__17.nbt')
    p.add_argument('--out', type=Path, default=Path(__file__).resolve().parent)
    args = p.parse_args(); out = args.out.resolve(); out.mkdir(parents=True, exist_ok=True)
    s = nbt.Structure(args.source)
    if s.size != (451,89,461) or s.meta.get('DataVersion') != 3955:
        raise ValueError('Unexpected source size/version; reconsider placement and masks.')
    if s.meta.get('entities'): raise ValueError('Entity splitting must be implemented before processing entities.')
    s.load_grid()
    original_palette = list(s.palette)
    marker_ids = {i for i,p in enumerate(s.palette) if p['Name'].startswith('minecraft:') and p['Name'].endswith('_concrete')}
    projected = {s.names[i]: (s.grid==i).any(axis=0) for i in marker_ids}
    village = filled(projected['brown_concrete'])
    protected = np.zeros((s.Z,s.X), bool)
    regions = []
    for name,mask in sorted(projected.items()):
        area = filled(mask)
        if name != 'brown_concrete': protected |= nbt.dilate(area, BUILDING_MARGIN)
        regions.append({'block':'minecraft:'+name, 'columns':int(mask.sum()),
                        'filled_columns':int(area.sum()), 'world_xz_inclusive':bounds(area),
                        'usage':'village' if name=='brown_concrete' else 'reserved_building',
                        'components':[{'world_xz_inclusive':bounds(component), 'columns':int(component.sum())}
                                      for component in component_masks(mask)]})
    changed = {}; added = {}; reasons = collections.Counter(); original_types = collections.Counter()
    def state(name, properties=None):
        record = {'Name':'minecraft:'+name}
        if properties: record['Properties'] = properties
        try: return s.palette.index(record)
        except ValueError: s.palette.append(record); return len(s.palette)-1
    air, dirt, stone = state('air'),state('dirt'),state('stone')
    def set_block(pos, st, reason):
        x,y,z=pos; old=int(s.grid[y,z,x])
        if old==st: return
        if pos in s.block_entities: raise ValueError(f'Attempt to change block entity at {pos}')
        if old==nbt.MISSING: added[pos]=st
        else:
            changed[pos]=st; original_types[original_palette[old]['Name']]+=1
        s.grid[y,z,x]=st; reasons[reason]+=1
    # Inspect the ORIGINAL column for solid non-marker cover, ignoring air/structure_void.
    empty_ids = {i for i,p in enumerate(s.palette) if p['Name'].split(':')[-1] in nbt.AIR|{'structure_void'}}
    empty_ids.add(nbt.MISSING)
    source_grid=s.grid.copy()
    yy,zz,xx=np.where(np.isin(source_grid,list(marker_ids)))
    for y,z,x in zip(map(int,yy),map(int,zz),map(int,xx)):
        cover=None
        for cy in range(y+1,s.Y):
            above=int(source_grid[cy,z,x])
            if above not in marker_ids and above not in empty_ids:
                cover=s.palette[above]['Name'].split(':')[-1]; break
        if cover in {'stone','andesite','diorite','granite','deepslate'}:
            set_block((x,y,z),stone,'buried_marker_stone')
        elif cover in {'grass_block','dirt','coarse_dirt','rooted_dirt','podzol'}:
            set_block((x,y,z),dirt,'buried_marker_dirt')
        else:
            set_block((x,y,z),air,'floating_marker_air')
    del source_grid
    nbt.refresh_top(s)
    # The exact integer teleport point straddles four columns. Require full solid
    # support at world Y=-5 and two blocks of air; avoid inventing a replacement pad.
    sx,sy,sz = (SPAWN[i]-ORIGIN[i] for i in range(3))
    arrival=[]
    solid_floor={'grass_block','coarse_dirt','dirt','stone','cobblestone','stone_bricks','gravel'}
    for x in (sx-1,sx):
        for z in (sz-1,sz):
            floor=s.entry((x,sy-1,z)); clear=[s.entry((x,y,z)) for y in (sy,sy+1)]
            ok=isinstance(floor,dict) and floor['Name'].split(':')[-1] in solid_floor
            gravel_supported=True
            if isinstance(floor,dict) and floor['Name']=='minecraft:gravel':
                gravel_supported=False
                for by in range(sy-2,-1,-1):
                    below=s.entry((x,by,z))
                    if isinstance(below,dict) and below['Name']=='minecraft:gravel': continue
                    gravel_supported=isinstance(below,dict) and below['Name'].split(':')[-1] in solid_floor-{'gravel'}
                    break
                ok=ok and gravel_supported
            ok=ok and all(v=='ABSENT' or (isinstance(v,dict) and v['Name'].split(':')[-1] in nbt.AIR) for v in clear)
            arrival.append({'world_xz':[x+ORIGIN[0],z+ORIGIN[2]],'floor':floor,'gravel_supported':gravel_supported,'clearance':clear,'safe':ok})
    if not all(c['safe'] for c in arrival):
        raise ValueError('Arrival floor/clearance is unsafe: '+json.dumps(arrival,ensure_ascii=False))
    zz2,xx2=np.indices((s.Z,s.X))
    spawn_area=(xx2-sx)**2+(zz2-sz)**2 <= SPAWN_RADIUS**2
    # Existing paths and built surfaces get a margin; existing natural trees and
    # all source decorations are preserved. Only add one-block plants on free soil.
    ground_names={'grass_block','dirt','rooted_dirt'}
    path_names={'dirt_path','coarse_dirt','gravel','cobblestone','stone_bricks','mossy_cobblestone'}
    ground_ids=[i for i,p in enumerate(s.palette) if p['Name'].split(':')[-1] in ground_names]
    path_ids=[i for i,p in enumerate(s.palette) if p['Name'].split(':')[-1] in path_names]
    path_area=nbt.dilate(np.isin(s.top_state,path_ids),PATH_MARGIN)
    candidates=village & ~protected & ~spawn_area & ~path_area & np.isin(s.top_state,ground_ids)
    flowers=['dandelion','poppy','cornflower','oxeye_daisy']
    grass_state=state('short_grass'); flower_states=[state(f) for f in flowers]
    randomizer=random.Random(SEED); plants=collections.Counter(); plant_positions=[]
    for z,x in zip(*np.where(candidates)):
        y=int(s.top[z,x])+1
        if y<1 or y+1>=s.Y: continue
        if int(s.grid[y,z,x]) not in empty_ids or int(s.grid[y+1,z,x]) not in empty_ids: continue
        r=randomizer.random()
        if r<0.007: st=randomizer.choice(flower_states)
        elif r<0.047: st=grass_state
        else: continue
        pos=(int(x),y,int(z)); set_block(pos,st,'village_plant')
        plants[s.palette[st]['Name']]+=1; plant_positions.append(pos)
    if any(not village[z,x] or protected[z,x] or spawn_area[z,x] for x,y,z in plant_positions):
        raise AssertionError('A plant overlaps a protected column')
    if np.isin(s.grid,list(marker_ids)).any(): raise AssertionError('Concrete marker remains')
    # Optional, audited correction for fragments already floating in the source.
    # Run after vegetation selection so all previously added plants stay identical.
    leaf_fix=PROJECT/'outputs/prologue_feuilles_20261002/feuilles_a_retirer.json'
    removed_leaves=0
    if leaf_fix.exists():
        leaf_manifest=json.loads(leaf_fix.read_text(encoding='utf-8'))
        if leaf_manifest['source_sha256']!=s.sha256 or tuple(leaf_manifest['origin_xyz'])!=ORIGIN:
            raise ValueError('Leaf correction belongs to another source or placement; re-audit first.')
        for raw_pos in leaf_manifest['positions_local']:
            pos=tuple(raw_pos); entry=s.entry(pos)
            if not isinstance(entry,dict) or entry['Name']!='minecraft:oak_leaves':
                raise ValueError(f'Expected an audited oak leaf at {pos}')
            set_block(pos,air,'orphan_oak_leaf_air'); removed_leaves+=1
    # Reuse the original writer/validator, whose byte-level check proves all
    # unlisted source records and all block entities have remained unchanged.
    writer=types.SimpleNamespace(s=s,changed=changed,added=added)
    final_path=out/'plateforme__17_preparee.nbt'
    nbt.Generator.write(writer,final_path)
    nbt.Generator.validate_output(writer,final_path)
    validation=dict(writer.validation)
    validation.pop('new_trees_connected_and_complete',None)
    # Segment records are copied from the source with only state/position edits.
    payloads={}; counts=collections.Counter(); expected_entities={}
    def add_record(pos, raw, has_nbt=False):
        x,y,z=pos; wx,wz=x+ORIGIN[0],z+ORIGIN[2]; sx,sz=wx//32,wz//32
        local=(wx-sx*32,y,wz-sz*32)
        relocated=relocate(raw,local)
        payloads.setdefault((sx,sz),bytearray()).extend(relocated); counts[sx,sz]+=1
        if has_nbt: expected_entities[pos]=bytes(relocate(raw,(0,0,0)))
    for pos,st,has_nbt,begin,end,off in s.blocks():
        raw=s.data[begin:end]
        if pos in changed:
            raw=bytearray(raw); struct.pack_into('>i',raw,off-begin,changed[pos])
        add_record(pos,raw,has_nbt)
    for pos,st in sorted(added.items()): add_record(pos,nbt.block_record(pos,st))
    target=out/'datapack/data/les_echos_du_monde/structure/platform_segments_v17'
    target.mkdir(parents=True,exist_ok=True)
    common=nbt.named(3,'DataVersion',struct.pack('>i',3955))
    common+=nbt.named(9,'size',bytes([3])+struct.pack('>iiii',3,32,s.Y,32))
    common+=nbt.named(9,'palette',bytes([10])+struct.pack('>i',len(s.palette))+b''.join(nbt.palette_record(p) for p in s.palette))
    segments=[]
    for (sx,sz),payload in sorted(payloads.items()):
        name=identifier(sx,sz); path=target/(name+'.nbt')
        with gzip.open(path,'wb',compresslevel=6) as f:
            f.write(b'\x0a\x00\x00'+common)
            f.write(nbt.named(9,'blocks',bytes([10])+struct.pack('>i',counts[sx,sz])))
            f.write(payload); f.write(nbt.named(9,'entities',bytes([10])+struct.pack('>i',0))+b'\0')
        segments.append({'id':name,'sx':sx,'sz':sz,'x':sx*32,'y':ORIGIN[1],'z':sz*32,
                         'template':'les_echos_du_monde:platform_segments_v17/'+name,
                         'block_count':counts[sx,sz],'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    del payloads
    # Reassemble every declared record into one grid: catches off-by-one errors,
    # negative-coordinate errors, duplicate placement and lost/altered state.
    rebuilt=np.full(s.grid.shape,nbt.MISSING,dtype=np.uint16); rebuilt_entities={}; reconstructed=0
    for seg in segments:
        piece=nbt.Structure(target/(seg['id']+'.nbt'))
        if piece.size!=(32,s.Y,32) or piece.palette!=s.palette: raise AssertionError('Segment metadata mismatch')
        for pos,st,has_nbt,begin,end,_ in piece.blocks():
            x,y,z=pos; x+=seg['x']-ORIGIN[0]; z+=seg['z']-ORIGIN[2]
            if not (0<=x<s.X and 0<=y<s.Y and 0<=z<s.Z): raise AssertionError('Unexpected padding record')
            if rebuilt[y,z,x]!=nbt.MISSING: raise AssertionError('Overlapping records')
            rebuilt[y,z,x]=st; reconstructed+=1
            if has_nbt: rebuilt_entities[x,y,z]=bytes(relocate(piece.data[begin:end],(0,0,0)))
    if not np.array_equal(rebuilt,s.grid): raise AssertionError('Reconstructed segments differ from edited source')
    if rebuilt_entities!=expected_entities: raise AssertionError('A block entity was lost/altered')
    manifest={'layout':'segments_v17','origin_xyz':list(ORIGIN),'source_size_xyz':list(s.size),
              'spawn_xyz':list(SPAWN),'segment_size_xz':[32,32],'radius_chunks':4,
              'source_sha256':s.sha256,'segments':segments}
    (out/'segments_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    validation.update({'segments_reassembled_identically':True,'segment_records':reconstructed,
                       'segment_count':len(segments),'segment_block_entity_records_identical':len(rebuilt_entities),
                       'markers_remaining':0,'added_trees':0,'added_bushes':0,
                       'orphan_oak_leaves_removed':removed_leaves})
    report={'source':str(s.path),'source_size_xyz':list(s.size),'origin_xyz':list(ORIGIN),
            'world_bounds_inclusive':[list(ORIGIN),[ORIGIN[i]+s.size[i]-1 for i in range(3)]],
            'arrival_xyz':list(SPAWN),'arrival_floor_world_y':-5,'arrival_columns':arrival,
            'village_columns':int(village.sum()),'plant_candidate_columns':int(candidates.sum()),
            'seed':SEED,'grass_probability':0.04,'flower_probability':0.007,
            'building_margin':BUILDING_MARGIN,'path_margin':PATH_MARGIN,'spawn_radius':SPAWN_RADIUS,
            'changes':dict(reasons),'plants':dict(plants),'regions':regions,'validation':validation,
            'terrain_repair_inference':'Buried concrete covered by stone replaced by stone; covered by grass/dirt replaced by dirt. Original material cannot be recovered.',
            'source_corner_discrepancy':'Stated Y26..65 gives40 blocks; actual NBT height89. Y origin calculated from actual arrival floor.',
            'tested_in_minecraft':False}
    (out/'rapport_preparation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    preview(s,village,protected,plant_positions,out/'plan_zones.png')
    print(json.dumps({'segments':len(segments),'plants':dict(plants),'changes':dict(reasons),'validation':validation},ensure_ascii=False),flush=True)

def component_masks(mask):
    for points in nbt.components(mask):
        component=np.zeros_like(mask)
        for x,z in points: component[z,x]=True
        yield component

def preview(s,village,protected,plants,path):
    nbt.refresh_top(s)
    lut=np.full((nbt.MISSING+1,3),(150,150,145),dtype=np.uint8)
    lut[nbt.MISSING]=(237,242,246)
    for i,p in enumerate(s.palette):
        name=p['Name'].split(':')[-1]
        if name in nbt.AIR: lut[i]=(237,242,246)
        elif name in nbt.SOIL or name in nbt.LOW_PLANTS: lut[i]=(116,151,79)
        elif 'leaves' in name: lut[i]=(51,101,50)
        elif name=='water': lut[i]=(65,128,188)
        elif 'log' in name or 'planks' in name: lut[i]=(138,106,70)
    rgb=lut[s.top_state].copy()
    rgb[village & ~protected]=(162,183,117)
    rgb[protected]=(192,157,128)
    for x,y,z in plants: rgb[z,x]=(255,232,139)
    img=Image.fromarray(rgb).resize((s.X*2,s.Z*2),Image.Resampling.NEAREST)
    canvas=Image.new('RGB',(s.X*2+320,s.Z*2+60),'white'); canvas.paste(img,(30,45))
    d=ImageDraw.Draw(canvas); font=ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf',16)
    d.text((30,10),'plateforme__17 — zones enregistrées et réserves',fill='black',font=font)
    x=250*2+30; z=235*2+45; d.ellipse((x-5,z-5,x+5,z+5),fill='red')
    d.text((s.X*2+45,60),'Rouge : arrivée (0, -4, 0)\nBeige : réserves + marge 4\nVert clair : village\nJaune : herbes et fleurs ajoutées\n\nSchéma, pas une capture en jeu.\nRepères retirés dans le NBT.\nArbres existants conservés.\nAucun arbre ajouté.',fill='black',font=font,spacing=8)
    canvas.save(path)

if __name__=='__main__': main()
