"""Read-only diagnostic of leaf components in the exported source and prepared NBT."""
import collections
import hashlib
import json
from pathlib import Path
import sys
import numpy as np

ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parents[1]
sys.path.insert(0,str(PROJECT/'06_RESSOURCES/Structures_NBT/Vegetation_finale'))
import generer_vegetation as nbt
ORIGIN=(-250,-26,-235)
TARGET=(-20,-1,6)
NEIGHBORS=[(x,y,z) for x in (-1,0,1) for y in (-1,0,1) for z in (-1,0,1) if (x,y,z)!=(0,0,0)]

def analyze(s):
    leaf_ids={i for i,p in enumerate(s.palette) if p['Name'].endswith('_leaves')}
    wood_ids={i for i,p in enumerate(s.palette) if p['Name'].endswith(('_log','_wood','_stem','_hyphae','bamboo_block'))}
    soil_ids={i for i,p in enumerate(s.palette) if p['Name'].split(':')[-1] in
              {'grass_block','dirt','coarse_dirt','rooted_dirt','podzol','moss_block','stone','stone_bricks','cobblestone','andesite','gravel','sand'}}
    natural_decor_ids={i for i,p in enumerate(s.palette) if p['Name'] in {'minecraft:magenta_terracotta','minecraft:pink_wool'}}
    ys,zs,xs=np.where(np.isin(s.grid,list(leaf_ids)))
    remaining={(int(x),int(y),int(z)) for x,y,z in zip(xs,ys,zs)}
    woods=np.array([(x,y,z) for y,z,x in zip(*np.where(np.isin(s.grid,list(wood_ids))))],dtype=np.int32)
    comps=[]
    while remaining:
        start=min(remaining); remaining.remove(start); todo=[start]; points=[]
        wood_contacts=ground_contacts=decor_contacts=0
        while todo:
            x,y,z=todo.pop(); points.append((x,y,z))
            for dx,dy,dz in NEIGHBORS:
                nx,ny,nz=x+dx,y+dy,z+dz
                if not (0<=nx<s.X and 0<=ny<s.Y and 0<=nz<s.Z): continue
                pos=(nx,ny,nz)
                if pos in remaining:
                    remaining.remove(pos); todo.append(pos)
                index=int(s.grid[ny,nz,nx])
                wood_contacts+=index in wood_ids
                decor_contacts+=index in natural_decor_ids
                if dy==-1: ground_contacts+=index in soil_ids
        arr=np.array(points)
        blocks=collections.Counter(s.palette[int(s.grid[y,z,x])]['Name'] for x,y,z in points)
        nearest=None
        if len(woods):
            # Bounding-box distance is sufficient for classifying obvious floating fragments.
            lo,hi=arr.min(axis=0),arr.max(axis=0)
            d=np.maximum(np.maximum(lo-woods,woods-hi),0).sum(axis=1)
            i=int(d.argmin()); nearest={'minimum_bbox_manhattan':int(d[i]),'world_xyz':(woods[i]+ORIGIN).tolist()}
        lo=(arr.min(axis=0)+ORIGIN).tolist(); hi=(arr.max(axis=0)+ORIGIN).tolist()
        target_local=tuple(TARGET[i]-ORIGIN[i] for i in range(3))
        comps.append({'count':len(points),'blocks':dict(blocks),'world_bounds_inclusive':[lo,hi],
                      'wood_contacts':wood_contacts,'ground_contacts':ground_contacts,'decor_contacts':decor_contacts,
                      'nearest_wood':nearest,'contains_target':target_local in points,
                      'floating_no_support':not (wood_contacts or ground_contacts or decor_contacts),
                      'points_local':points})
    return sorted(comps,key=lambda c:(not c['contains_target'],-c['count'],c['world_bounds_inclusive'][0]))

def main():
    source=PROJECT/'06_RESSOURCES/Structures_NBT/plateforme__17.nbt'
    final=PROJECT/'outputs/prologue_plateforme17/plateforme__17_preparee.nbt'
    s=nbt.Structure(source); s.load_grid()
    local=tuple(TARGET[i]-ORIGIN[i] for i in range(3))
    components=analyze(s)
    target=s.entry(local)
    floating=[c for c in components if c['floating_no_support']]
    report={'source':str(source),'source_sha256':s.sha256,'origin_xyz':ORIGIN,
            'target_world_xyz':TARGET,'target_local_xyz':local,'source_target_block':target,
            'source_leaves':[{**p,'count':s.counts[i]} for i,p in enumerate(s.palette) if p['Name'].endswith('_leaves')],
            'source_wood_blocks':[{**p,'count':s.counts[i]} for i,p in enumerate(s.palette) if p['Name'].endswith(('_log','_wood','_stem','_hyphae'))],
            'components':components,'floating_component_count':len(floating),'floating_block_count':sum(c['count'] for c in floating),
            'criterion':'26-connected leaf components with no adjacent log/wood, soil beneath any adjacent leaf, or pink-wool/magenta-terracotta natural decoration.',
            'modified_files':False}
    del s
    f=nbt.Structure(final); f.load_grid()
    report['prepared_target_block']=f.entry(local)
    report['source_and_prepared_target_identical']=report['source_target_block']==report['prepared_target_block']
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'diagnostic_feuilles.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    summary={k:report[k] for k in ('target_world_xyz','source_target_block','prepared_target_block','source_and_prepared_target_identical','floating_component_count','floating_block_count')}
    summary['target_component']=[{k:v for k,v in c.items() if k!='points_local'} for c in components if c['contains_target']]
    summary['floating_components']=[{k:v for k,v in c.items() if k!='points_local'} for c in floating]
    print(json.dumps(summary,ensure_ascii=False),flush=True)

if __name__=='__main__': main()
