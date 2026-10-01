#!/usr/bin/env python3
"""Vegetation vanilla pour un NBT Java, sans modifier le fichier source.

Python 3.12, numpy et Pillow (apercus uniquement). Voir LISEZ_MOI.txt.
"""
from __future__ import annotations
import argparse
import collections
import gzip
import hashlib
import json
import math
import pathlib
import struct
import time
import random
import zipfile
from array import array
import numpy as np
from PIL import Image, ImageDraw

MISSING = 65535
COLORS = ['white','orange','magenta','light_blue','yellow','lime','pink','gray',
          'light_gray','cyan','purple','blue','brown','green','red','black']
RGB = [(235,235,231),(230,135,33),(189,67,177),(74,166,212),(233,202,43),
       (128,183,47),(227,140,161),(68,74,77),(150,151,145),(26,142,148),
       (124,62,174),(52,68,168),(114,78,50),(81,115,40),(171,44,38),(32,32,35)]
COLOR_BLOCKS = {f'minecraft:{c}_{kind}': c for c in COLORS
                for kind in ['wool','concrete','concrete_powder','terracotta','stained_glass']}
SOIL = {'grass_block','dirt','podzol','rooted_dirt','moss_block'}
AIR = {'air','cave_air','void_air'}
LOW_PLANTS = {'short_grass','tall_grass','fern','large_fern','dandelion','poppy',
              'cornflower','oxeye_daisy','azure_bluet','allium','blue_orchid',
              'red_tulip','orange_tulip','white_tulip','pink_tulip','lily_of_the_valley',
              'rose_bush','peony','lilac','sunflower','torchflower','pitcher_plant'}
# Plaques identifiees dans le fichier fourni: rectangles complets, une couche,
# au-dessus du relief. Les autres blocs colores ne sont pas classes par couleur.
MARKERS = [
    ('Jaune','yellow_concrete',47,229,330,255,375),
    ('Bleu','blue_concrete',42,234,304,262,324),
    ('Magenta','magenta_concrete',36,305,290,325,310),
    ('Noir','black_concrete',40,360,312,375,323),
    ('Cyan','cyan_concrete',34,275,352,287,364),
    ('Rouge','red_concrete',48,306,350,327,378),
]
MARKER_EXTRAS = [('yellow_concrete',(256,24,364)),
                 ('cyan_concrete',(279,24,351)),('cyan_concrete',(280,24,351)),
                 ('cyan_concrete',(281,24,351)),('red_concrete',(328,49,379))]

class Reader:
    def __init__(self, data): self.data, self.p = data, 0
    def u8(self):
        v=self.data[self.p]; self.p+=1; return v
    def i32(self):
        v=struct.unpack_from('>i',self.data,self.p)[0]; self.p+=4; return v
    def string(self):
        n=struct.unpack_from('>H',self.data,self.p)[0]; self.p+=2
        s=self.data[self.p:self.p+n].decode('utf-8'); self.p+=n; return s
    def skip(self, t):
        if t in (1,2,3,4,5,6): self.p += {1:1,2:2,3:4,4:8,5:4,6:8}[t]
        elif t in (7,11,12):
            n=self.i32(); self.p += n*{7:1,11:4,12:8}[t]
        elif t == 8:
            n=struct.unpack_from('>H',self.data,self.p)[0]; self.p+=2+n
        elif t == 9:
            st=self.u8(); n=self.i32()
            if st in (1,2,3,4,5,6): self.p+=n*{1:1,2:2,3:4,4:8,5:4,6:8}[st]
            else:
                for _ in range(n): self.skip(st)
        elif t == 10:
            while True:
                st=self.u8()
                if not st: break
                self.string(); self.skip(st)
        else: raise ValueError(f'Tag inconnu {t} a {self.p}')
    def value(self,t):
        if t in (1,2,3,4,5,6):
            fmt={1:'>b',2:'>h',3:'>i',4:'>q',5:'>f',6:'>d'}[t]
            v=struct.unpack_from(fmt,self.data,self.p)[0]; self.p+=struct.calcsize(fmt); return v
        if t==8: return self.string()
        if t in (7,11,12):
            n=self.i32(); fmt={7:'b',11:'i',12:'q'}[t]
            v=struct.unpack_from('>'+str(n)+fmt,self.data,self.p)
            self.p+=n*{7:1,11:4,12:8}[t]; return list(v)
        if t==9:
            st=self.u8(); n=self.i32(); return [self.value(st) for _ in range(n)]
        if t==10:
            v={}
            while True:
                st=self.u8()
                if not st: return v
                name=self.string(); v[name]=self.value(st)
        raise ValueError(t)

def nbt_string(s):
    b=s.encode('utf-8'); return struct.pack('>H',len(b))+b
def named(t,n,p): return bytes([t])+nbt_string(n)+p
def palette_record(entry):
    b=named(8,'Name',nbt_string(entry['Name']))
    if entry.get('Properties'):
        p=b''.join(named(8,k,nbt_string(v)) for k,v in entry['Properties'].items())+b'\0'
        b+=named(10,'Properties',p)
    return b+b'\0'
def block_record(pos,state):
    return named(9,'pos',bytes([3])+struct.pack('>iiii',3,*pos))+named(3,'state',struct.pack('>i',state))+b'\0'

class Structure:
    def __init__(self,path):
        self.path=pathlib.Path(path)
        self.sha256=hashlib.sha256(self.path.read_bytes()).hexdigest()
        raw=self.path.read_bytes()
        self.compression='gzip' if raw[:2]==b'\x1f\x8b' else 'none'
        self.data=gzip.decompress(raw) if self.compression=='gzip' else raw
        r=Reader(self.data)
        if r.u8()!=10: raise ValueError('Le NBT racine doit etre un compound.')
        self.root_name=r.string(); self.header=self.data[:r.p]; self.fields=[]
        self.meta={}; self.palette=[]
        while True:
            start=r.p; t=r.u8()
            if not t: break
            name=r.string(); payload=r.p
            if name=='blocks':
                if t!=9 or r.u8()!=10: raise ValueError('blocks doit etre une liste de compounds')
                self.count=r.i32(); self.blocks_start=r.p
                for _ in range(self.count): r.skip(10)
                self.blocks_end=r.p
            elif name=='palette':
                if t!=9: raise ValueError('palette invalide')
                self.palette=r.value(t)
            else:
                self.meta[name]=r.value(t)
            self.fields.append((name,t,start,payload,r.p))
        if r.p!=len(self.data): raise ValueError('Octets apres le NBT racine')
        if 'palettes' in self.meta: raise ValueError('Les palettes multiples exigent une gestion explicite')
        self.size=tuple(self.meta['size']); self.X,self.Y,self.Z=self.size
        if len(self.palette)>=MISSING: raise ValueError('Palette trop grande')
    def blocks(self):
        r=Reader(self.data); r.p=self.blocks_start
        for _ in range(self.count):
            begin=r.p; pos=state=state_offset=None; has_nbt=False
            while True:
                t=r.u8()
                if not t: break
                n=r.string()
                if n=='pos':
                    if t==9:
                        subtype=r.u8(); count=r.i32()
                        if subtype!=3 or count!=3: raise ValueError('pos invalide')
                    elif t==11:
                        if r.i32()!=3: raise ValueError('pos invalide')
                    else: raise ValueError('Type pos invalide')
                    pos=struct.unpack_from('>iii',self.data,r.p); r.p+=12
                elif n=='state':
                    if t!=3: raise ValueError('state doit etre un int')
                    state_offset=r.p; state=r.i32()
                else:
                    if n=='nbt': has_nbt=True
                    r.skip(t)
            if pos is None or state is None: raise ValueError('Bloc sans pos/state')
            yield pos,state,has_nbt,begin,r.p,state_offset
        if r.p!=self.blocks_end: raise ValueError('Fin de liste blocks incoherente')
    def load_grid(self):
        self.grid=np.full((self.Y,self.Z,self.X),MISSING,dtype=np.uint16)
        self.block_entities=[]; counts=collections.Counter(); dup=0
        start=time.monotonic()
        for i,(pos,state,has_nbt,*_) in enumerate(self.blocks()):
            x,y,z=pos
            if not (0<=x<self.X and 0<=y<self.Y and 0<=z<self.Z):
                raise ValueError(f'Position hors taille declaree: {pos}')
            if not 0<=state<len(self.palette): raise ValueError('Index palette invalide')
            if self.grid[y,z,x]!=MISSING: dup+=1
            self.grid[y,z,x]=state; counts[state]+=1
            if has_nbt: self.block_entities.append(pos)
            if i and i%1000000==0: print(f'Lecture: {i:,}/{self.count:,} blocs',flush=True)
        self.counts=counts; self.duplicates=dup
        if dup: raise ValueError(f'{dup} positions dupliquees; generation interrompue')
        self.names=[p['Name'].removeprefix('minecraft:') for p in self.palette]
        lut=np.ones(MISSING+1,dtype=bool); lut[MISSING]=False
        for i,n in enumerate(self.names):
            if n in AIR or n=='structure_void': lut[i]=False
        occupied=lut[self.grid]
        self.top=np.where(occupied.any(axis=0),self.Y-1-np.argmax(occupied[::-1],axis=0),-1)
        zz,xx=np.indices((self.Z,self.X))
        self.top_state=self.grid[np.maximum(self.top,0),zz,xx].copy()
        self.top_state[self.top<0]=MISSING
        print(f'Grille lue en {time.monotonic()-start:.1f}s',flush=True)
    def entry(self,pos):
        x,y,z=pos
        if not (0<=x<self.X and 0<=y<self.Y and 0<=z<self.Z): return 'OUTSIDE'
        i=int(self.grid[y,z,x]); return 'ABSENT' if i==MISSING else self.palette[i]

def components(mask):
    seen=np.zeros(mask.shape,bool); out=[]; H,W=mask.shape
    for z,x in zip(*np.where(mask)):
        if seen[z,x]: continue
        seen[z,x]=True; todo=[(int(x),int(z))]; pts=[]
        while todo:
            px,pz=todo.pop(); pts.append((px,pz))
            for nx,nz in ((px-1,pz),(px+1,pz),(px,pz-1),(px,pz+1)):
                if 0<=nx<W and 0<=nz<H and mask[nz,nx] and not seen[nz,nx]:
                    seen[nz,nx]=True; todo.append((nx,nz))
        out.append(pts)
    return out

def dilate(mask,r):
    result=np.zeros(mask.shape,bool); H,W=mask.shape
    for dz in range(-r,r+1):
        for dx in range(-r,r+1):
            zs=slice(max(0,-dz),min(H,H-dz)); xs=slice(max(0,-dx),min(W,W-dx))
            result[max(0,dz):min(H,H+dz),max(0,dx):min(W,W+dx)] |= mask[zs,xs]
    return result

def audit(s,origin,out):
    origin=tuple(origin); out.mkdir(parents=True,exist_ok=True)
    color_ids=[i for i,p in enumerate(s.palette) if p['Name'] in COLOR_BLOCKS]
    mask=np.isin(s.top_state,color_ids)
    comps=components(mask); info=[]
    for j,pts in enumerate(sorted(comps,key=len,reverse=True)):
        xs=[p[0] for p in pts]; zs=[p[1] for p in pts]; xx=np.array(xs); zz=np.array(zs)
        lo=(min(xs),min(zs)); hi=(max(xs),max(zs)); ys=s.top[zz,xx]
        color_count=collections.Counter(s.names[int(k)] for k in s.top_state[zz,xx])
        info.append({'id':j,'count':len(pts),'local_xz':[list(lo),list(hi)],
                     'world_xz':[[lo[0]+origin[0],lo[1]+origin[2]],[hi[0]+origin[0],hi[1]+origin[2]]],
                     'y_local':[int(ys.min()),int(ys.max())],
                     'y_counts':{str(k):v for k,v in collections.Counter(map(int,ys)).items()},
                     'colors':dict(color_count)})
    spawn=(7-origin[0],-3-origin[1],1-origin[2])
    inside=all(0<=spawn[i]<s.size[i] for i in range(3))
    arrival={'world':[7,-3,1],'local':list(spawn),'inside_structure':inside,
             'column_top_local':int(s.top[spawn[2],spawn[0]]) if inside else None,
             'column_top_world':int(s.top[spawn[2],spawn[0]])+origin[1] if inside else None,
             'blocks':{str(dy):s.entry((spawn[0],spawn[1]+dy,spawn[2])) for dy in range(-3,4)}}
    report={'source':str(s.path),'source_sha256':s.sha256,'compressed_bytes':s.path.stat().st_size,
            'uncompressed_bytes':len(s.data),'size':list(s.size),'DataVersion':s.meta.get('DataVersion'),
            'blocks':s.count,'palette_count':len(s.palette),'entities_count':len(s.meta.get('entities',[])),
            'block_entities_count':len(s.block_entities),'duplicates':s.duplicates,
            'origin_provisional':list(origin),'palette':[dict(p,count=s.counts[i]) for i,p in enumerate(s.palette)],
            'colored_surface_components':info,'arrival':arrival}
    volumes=[]
    for i in color_ids:
        yy,zz,xx=np.where(s.grid==i)
        if not len(xx): continue
        ys=collections.Counter(map(int,yy))
        slabs=[]
        for y,n in ys.items():
            if n<50: continue
            for pts in components(s.grid[y]==i):
                if len(pts)<30: continue
                px=[v[0] for v in pts]; pz=[v[1] for v in pts]
                slabs.append({'y':y,'count':len(pts),'xz':[[min(px),min(pz)],[max(px),max(pz)]],
                              'rectangular':len(pts)==(max(px)-min(px)+1)*(max(pz)-min(pz)+1)})
        volumes.append({'name':s.palette[i]['Name'],'count':len(xx),
                        'local_bounds':[[int(xx.min()),int(yy.min()),int(zz.min())],
                                        [int(xx.max()),int(yy.max()),int(zz.max())]],
                        'y_counts':dict(sorted(ys.items())),'slabs':slabs})
    report['colored_volumes']=volumes
    columns={}
    for r in info[:8]:
        lo,hi=r['local_xz']; x=(lo[0]+hi[0])//2; z=(lo[1]+hi[1])//2
        columns[str(r['id'])]={'xz':[x,z],'blocks':[[y,s.names[int(s.grid[y,z,x])]]
                            for y in range(s.Y) if s.grid[y,z,x]!=MISSING]}
    report['colored_center_columns']=columns
    (out/'analyse_source.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    render(s,out/'terrain_source.png',info,origin)
    return report,comps

def refresh_top(s):
    lut=np.ones(MISSING+1,dtype=bool); lut[MISSING]=False
    for i,p in enumerate(s.palette):
        if p['Name'].removeprefix('minecraft:') in AIR: lut[i]=False
    occupied=lut[s.grid]
    s.top=np.where(occupied.any(axis=0),s.Y-1-np.argmax(occupied[::-1],axis=0),-1)
    zz,xx=np.indices((s.Z,s.X))
    s.top_state=s.grid[np.maximum(s.top,0),zz,xx].copy(); s.top_state[s.top<0]=MISSING
    s.names=[p['Name'].removeprefix('minecraft:') for p in s.palette]

def profile_masks(s,args):
    if s.size!=(562,93,536):
        raise ValueError('Ce profil de marqueurs est prevu pour 562 x 93 x 536; revoir MARKERS avant de traiter une autre structure.')
    building=np.zeros((s.Z,s.X),bool); regions=[]
    for label,name,y,x1,z1,x2,z2 in MARKERS:
        ids=[i for i,p in enumerate(s.palette) if p['Name']=='minecraft:'+name]
        if not ids or not np.isin(s.grid[y,z1:z2+1,x1:x2+1],ids).all():
            raise ValueError(f'La plaque {label} ne correspond plus au profil; revoir MARKERS.')
        building[max(0,z1-args.building_margin):min(s.Z,z2+args.building_margin+1),
                 max(0,x1-args.building_margin):min(s.X,x2+args.building_margin+1)]=True
        regions.append({'label':label,'block':'minecraft:'+name,'local_y':y,
                        'local_xz':[[x1,z1],[x2,z2]],
                        'world_xz':[[x1+args.origin[0],z1+args.origin[2]],
                                    [x2+args.origin[0],z2+args.origin[2]]],
                        'count':(x2-x1+1)*(z2-z1+1),'margin':args.building_margin})
    zz,xx=np.indices((s.Z,s.X)); wx=xx+args.origin[0]; wz=zz+args.origin[2]
    garrik=(wx>=-16)&(wx<=31)&(wz>=-80)&(wz<=-33)
    spawn=(wx-7)**2+(wz-1)**2<=args.spawn_radius**2
    return building,garrik,spawn,regions

class Generator:
    def __init__(self,s,args):
        self.s,self.args=s,args; self.rng=random.Random(args.seed)
        self.original_palette_count=len(s.palette)
        self.changed={}; self.added={}; self.change_reasons={}; self.features=[]
        self.index={self.key(p):i for i,p in enumerate(s.palette)}
        self.building,self.garrik,self.spawn,self.regions=profile_masks(s,args)
    @staticmethod
    def key(p): return p['Name'],tuple(sorted(p.get('Properties',{}).items()))
    def state(self,name,**props):
        entry={'Name':'minecraft:'+name}
        if props: entry['Properties']={k:str(v) for k,v in props.items()}
        k=self.key(entry)
        if k not in self.index:
            self.index[k]=len(self.s.palette); self.s.palette.append(entry)
        return self.index[k]
    def empty(self,pos):
        x,y,z=pos; s=self.s
        if not (0<=x<s.X and 0<=y<s.Y and 0<=z<s.Z): return False
        i=int(s.grid[y,z,x])
        return i==MISSING or s.palette[i]['Name'].removeprefix('minecraft:') in AIR
    def change(self,pos,state,reason):
        x,y,z=pos; old=int(self.s.grid[y,z,x])
        if old==state: return
        if pos in self.added: self.added[pos]=state
        elif old==MISSING: self.added[pos]=state
        else: self.changed[pos]=state
        self.change_reasons[pos]=reason; self.s.grid[y,z,x]=state
    def add_shape(self,shape,kind,center):
        forbidden=self.building|self.spawn|self.path_clear|self.construction_clear
        if kind in ('tree','bush'): forbidden=forbidden|self.garrik
        for pos in shape:
            x,y,z=pos
            if not self.empty(pos) or forbidden[z,x]: return False
        for pos,st in shape.items(): self.change(pos,st,kind)
        xs=[v[0] for v in shape]; ys=[v[1] for v in shape]; zs=[v[2] for v in shape]
        self.features.append({'kind':kind,'center_local':list(center),
                              'center_world':[center[i]+self.args.origin[i] for i in range(3)],
                              'blocks':len(shape),'local_bounds':[[min(xs),min(ys),min(zs)],[max(xs),max(ys),max(zs)]]})
        return True
    def remove_markers_and_clear(self):
        s=self.s; air=self.state('air'); grass=self.state('grass_block',snowy='false')
        marker_positions=[]
        for label,n,y,x1,z1,x2,z2 in MARKERS:
            for z in range(z1,z2+1):
                for x in range(x1,x2+1): marker_positions.append(((x,y,z),n))
        marker_positions+= [(pos,n) for n,pos in MARKER_EXTRAS]
        for pos,n in marker_positions:
            x,y,z=pos; old=int(s.grid[y,z,x])
            if old==MISSING or s.palette[old]['Name']!='minecraft:'+n:
                raise ValueError(f'Marqueur inattendu a {pos}')
            if pos in s.block_entities: raise ValueError('Marqueur avec NBT: aucune suppression automatique')
            # Les quatre reperes au niveau du sol sont remplaces par de l'herbe;
            # les plaques suspendues et le point rouge par de l'air explicite.
            st=grass if n in ('yellow_concrete','cyan_concrete') and y==24 else air
            self.change(pos,st,'marker_ground' if st==grass else 'marker_air')
        refresh_top(s)
        # Sol de terre decouvert sous les plaques: meme hauteur, herbe coherente.
        for _,_,_,x1,z1,x2,z2 in MARKERS:
            for z in range(z1,z2+1):
                for x in range(x1,x2+1):
                    y=int(s.top[z,x])
                    if y>=0 and s.palette[int(s.grid[y,z,x])]['Name']=='minecraft:dirt':
                        self.change((x,y,z),grass,'marker_soil_grass')
        plant_ids=[i for i,p in enumerate(s.palette) if p['Name'].removeprefix('minecraft:') in LOW_PLANTS]
        yy,zz,xx=np.where(np.isin(s.grid,plant_ids)&(self.building|self.spawn)[None,:,:])
        for y,z,x in zip(yy,zz,xx):
            pos=(int(x),int(y),int(z))
            if pos in s.block_entities: raise ValueError('Plante avec NBT dans une reserve')
            self.change(pos,air,'existing_low_plant_clearance')
        # Une copie sparse ne nettoie pas les cellules absentes lors du placement.
        # On inscrit de l'air autour de l'arrivee sans toucher aux obstacles solides.
        sx,sy,sz=7-self.args.origin[0],-3-self.args.origin[1],1-self.args.origin[2]
        obstructions=[]
        for z in range(sz-1,sz+2):
            for x in range(sx-1,sx+2):
                for y in range(sy,sy+3):
                    if self.empty((x,y,z)): self.change((x,y,z),air,'spawn_explicit_air')
                    else: obstructions.append([x,y,z])
        self.spawn_obstructions=obstructions
        refresh_top(s)
    def masks_and_candidates(self):
        s=self.s
        path_names={'dirt_path','gravel','coarse_dirt','stone_bricks','cobblestone',
                    'andesite','polished_andesite','mossy_cobblestone','cracked_stone_bricks',
                    'cobbled_deepslate','smooth_stone','granite','smooth_sandstone','cut_sandstone'}
        path_ids=[i for i,p in enumerate(s.palette) if p['Name'].removeprefix('minecraft:') in path_names]
        path=np.isin(s.top_state,path_ids)
        self.path_clear=dilate(path,self.args.path_margin)
        artificial=[]; existing_tree_ids=[]
        for i,p in enumerate(s.palette):
            n=p['Name'].removeprefix('minecraft:')
            if 'leaves' in n or n in ('oak_log','cherry_log','birch_log','spruce_log'): existing_tree_ids.append(i)
            if (any(v in n for v in ('stairs','slab','planks','fence','trapdoor','door','wall','concrete','terracotta','wool','glass','lantern','structure_block','furnace'))
                or n in ('crafting_table','anvil','campfire','chain','iron_bars','cauldron','sculk_sensor','lava')):
                artificial.append(i)
        # Toute colonne contenant une construction, y compris cachee par du sol,
        # conserve une marge. Cette precaution garde les materiaux colores reels.
        construction=np.isin(s.grid,artificial).any(axis=0)
        for x,y,z in s.block_entities: construction[z,x]=True
        self.construction_clear=dilate(construction,3)
        existing_trees=np.isin(s.grid,existing_tree_ids).any(axis=0)
        self.tree_spacing_mask=dilate(existing_trees,3)
        soil_ids=[i for i,p in enumerate(s.palette) if p['Name'].removeprefix('minecraft:') in SOIL]
        self.candidate=np.isin(s.top_state,soil_ids)&~(self.building|self.spawn|self.path_clear|self.construction_clear)
        self.candidate[:4]=False; self.candidate[-4:]=False
        self.candidate[:,:4]=False; self.candidate[:,-4:]=False
        # Des variations larges creees par une graine, pour conserver des clairieres.
        zz,xx=np.indices((s.Z,s.X)); phase=self.rng.uniform(0,math.tau)
        self.patch=np.clip(.48+.23*np.sin(xx/24+np.sin(zz/43)+phase)
                           +.23*np.cos(zz/31-xx/62-phase),.06,.95)
        self.slope=np.zeros((s.Z,s.X),int)
        for dz,dx in ((0,1),(0,-1),(1,0),(-1,0)):
            self.slope=np.maximum(self.slope,np.abs(s.top-np.roll(s.top,(dz,dx),(0,1))))
        self.initial_candidates=int(self.candidate.sum())
    def tree_shape(self,x,y,z,species):
        rng=self.rng; h=rng.randint(5,7) if species=='oak' else rng.randint(6,8)
        logs={(x,y+i,z):self.state(species+'_log',axis='y') for i in range(1,h+1)}
        if species=='oak' and rng.random()<.4:
            dx,dz=rng.choice([(1,0),(-1,0),(0,1),(0,-1)])
            for a in (1,2): logs[(x+dx*a,y+h-2,z+dz*a)]=self.state('oak_log',axis='x' if dx else 'z')
        leaves=set(); wide=species=='oak' and rng.random()<.45
        layers=[(h-3,2),(h-2,3 if wide else 2),(h-1,3 if wide else 2),(h,2),(h+1,1)]
        for dy,r in layers:
            for dx in range(-r,r+1):
                for dz in range(-r,r+1):
                    if dx*dx+dz*dz>r*r+1: continue
                    if abs(dx)==r and abs(dz)==r and rng.random()<.5: continue
                    pos=(x+dx,y+dy,z+dz)
                    if pos not in logs: leaves.add(pos)
        # Distances exactes dans le graphe tronc/feuilles; aucun feuillage detache.
        distances={}; todo=collections.deque((pos,0) for pos in logs)
        while todo:
            (px,py,pz),d=todo.popleft()
            for nx,ny,nz in ((px-1,py,pz),(px+1,py,pz),(px,py-1,pz),(px,py+1,pz),(px,py,pz-1),(px,py,pz+1)):
                pos=(nx,ny,nz)
                if pos in leaves and pos not in distances:
                    distances[pos]=d+1; todo.append((pos,d+1))
        if set(distances)!=leaves or max(distances.values(),default=0)>7:
            raise ValueError('Couronne deconnectee du tronc')
        shape=dict(logs)
        for pos,d in distances.items(): shape[pos]=self.state(species+'_leaves',distance=d,persistent='true',waterlogged='false')
        return shape
    def generate(self):
        self.remove_markers_and_clear(); self.masks_and_candidates(); s=self.s; rng=self.rng
        pts=[(int(x),int(z)) for z,x in zip(*np.where(self.candidate))]; rng.shuffle(pts)
        target=round(len(pts)*self.args.tree_density); centers=[]
        for x,z in pts:
            if len(centers)>=target: break
            if self.garrik[z,x] or self.tree_spacing_mask[z,x] or self.slope[z,x]>1: continue
            if self.patch[z,x]<.26 or rng.random()>self.patch[z,x]*.6: continue
            if any((x-tx)**2+(z-tz)**2<self.args.tree_spacing**2 for tx,tz in centers): continue
            y=int(s.top[z,x]); species='birch' if rng.random()<.27 else 'oak'
            if self.add_shape(self.tree_shape(x,y,z,species),'tree',(x,y,z)):
                centers.append((x,z)); self.features[-1]['species']=species
        bush_centers=[]; bush_target=round(len(pts)*self.args.bush_density)
        for x,z in pts:
            if len(bush_centers)>=bush_target: break
            if self.garrik[z,x] or self.slope[z,x]>1 or self.patch[z,x]<.25: continue
            if any((x-bx)**2+(z-bz)**2<25 for bx,bz in bush_centers): continue
            y=int(s.top[z,x]); shape={}
            if rng.random()<.7:
                offsets=rng.sample([(0,0),(1,0),(-1,0),(0,1),(0,-1)],rng.randint(1,3))
                for dx,dz in offsets:
                    nx,nz=x+dx,z+dz
                    if not self.candidate[nz,nx]: break
                    ny=int(s.top[nz,nx])
                    shape[(nx,ny+1,nz)]=self.state('flowering_azalea' if rng.random()<.18 else 'azalea')
                else:
                    if self.add_shape(shape,'bush',(x,y,z)): bush_centers.append((x,z))
                continue
            if not np.all(s.top[z-1:z+2,x-1:x+2]==y): continue
            leaf=self.state('oak_leaves',distance=7,persistent='true',waterlogged='false')
            for dx,dz in ((0,0),(1,0),(-1,0),(0,1),(0,-1)): shape[(x+dx,y+1,z+dz)]=leaf
            shape[(x,y+2,z)]=leaf
            if self.add_shape(shape,'bush',(x,y,z)): bush_centers.append((x,z))
        flowers=['dandelion','poppy','oxeye_daisy','cornflower','azure_bluet','allium','white_tulip','pink_tulip']
        # Palette florale par tache de 14 blocs, avec quelques variations locales.
        flower_tiles={}
        for x,z in pts:
            if self.slope[z,x]>2: continue
            chance=self.args.plant_density*(.35+1.5*self.patch[z,x])
            if rng.random()>chance: continue
            y=int(s.top[z,x]); pos=(x,y+1,z)
            if not self.empty(pos): continue
            r=rng.random()
            if r<.69: shape={pos:self.state('short_grass')}
            elif r<.85: shape={pos:self.state('fern')}
            elif r<.89:
                n='large_fern' if rng.random()<.55 else 'tall_grass'
                shape={pos:self.state(n,half='lower'),(x,y+2,z):self.state(n,half='upper')}
            else:
                tile=(x//14,z//14)
                if tile not in flower_tiles: flower_tiles[tile]=rng.choice(flowers)
                n=flower_tiles[tile] if rng.random()<.85 else rng.choice(flowers)
                shape={pos:self.state(n)}
            self.add_shape(shape,'plant',(x,y,z))
        refresh_top(s)
        self.verify_planned(); return self
    def verify_planned(self):
        s=self.s
        for pos,reason in self.change_reasons.items():
            if reason not in ('tree','bush','plant'): continue
            x,y,z=pos
            if self.building[z,x] or self.spawn[z,x] or self.path_clear[z,x] or self.construction_clear[z,x]:
                raise ValueError('Vegetation dans une reserve')
            if reason in ('tree','bush') and self.garrik[z,x]: raise ValueError('Feuillage dans la reserve de Garrik')
        if self.spawn_obstructions: print('ATTENTION: obstacles a l arrivee:',self.spawn_obstructions,flush=True)
    def check_assets(self,jar):
        if not jar or not jar.exists(): return {'verified':False,'reason':'JAR 1.21.1 non disponible pour lecture'}
        added_palette=slice(self.original_palette_count,None)
        with zipfile.ZipFile(jar) as f:
            version=json.loads(f.read('version.json'))
            if version['id']!='1.21.1' or version['world_version']!=3955: raise ValueError('JAR de mauvaise version')
            checked=[]
            for p in self.s.palette[added_palette]:
                name=p['Name'].split(':')[1]; asset='assets/minecraft/blockstates/'+name+'.json'
                if asset not in f.namelist(): raise ValueError(f'Bloc absent de Minecraft 1.21.1: {name}')
                props=p.get('Properties',{})
                if name.endswith('_leaves'):
                    if not set(props)<= {'distance','persistent','waterlogged'}: raise ValueError('Propriete leaves inconnue')
                    if not 1<=int(props['distance'])<=7 or props['persistent']!='true' or props['waterlogged']!='false': raise ValueError('Etat de feuillage invalide')
                elif name.endswith('_log'):
                    if props!={'axis':'y'} and props!={'axis':'x'} and props!={'axis':'z'}: raise ValueError('Axe de tronc invalide')
                elif name in ('tall_grass','large_fern'):
                    if props not in ({'half':'lower'},{'half':'upper'}): raise ValueError('Demi-plante invalide')
                elif name=='grass_block':
                    if props!={'snowy':'false'}: raise ValueError('Sol invalide')
                elif props: raise ValueError(f'Proprietes non prevues: {p}')
                checked.append(p)
        return {'verified':True,'jar_read_only':str(jar),'version':version['id'],
                'world_version':version['world_version'],'added_states':checked}
    def write(self,path):
        s=self.s; offsets=[]; originals_changed=collections.Counter()
        for pos,st,has_nbt,begin,end,off in s.blocks():
            if pos in self.changed:
                if has_nbt: raise ValueError(f'Refus de changer un bloc avec NBT: {pos}')
                offsets.append((off,self.changed[pos])); originals_changed[s.palette[st]['Name']]+=1
        if len(offsets)!=len(self.changed): raise ValueError('Changements incomplets')
        offsets.sort(); path.parent.mkdir(parents=True,exist_ok=True)
        temp=path.with_suffix('.nbt.part')
        with temp.open('wb') as raw:
            with gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0,compresslevel=6) as f:
                f.write(s.header)
                for name,t,start,payload,end in s.fields:
                    if name=='palette':
                        f.write(s.data[start:payload]); f.write(bytes([10])+struct.pack('>i',len(s.palette)))
                        for entry in s.palette: f.write(palette_record(entry))
                    elif name=='blocks':
                        f.write(s.data[start:payload]); f.write(bytes([10])+struct.pack('>i',s.count+len(self.added)))
                        cursor=s.blocks_start
                        for off,state in offsets:
                            if cursor<off: f.write(s.data[cursor:off])
                            f.write(struct.pack('>i',state)); cursor=off+4
                        f.write(s.data[cursor:s.blocks_end])
                        for pos,st in sorted(self.added.items()): f.write(block_record(pos,st))
                    else: f.write(s.data[start:end])
                f.write(b'\0')
        temp.replace(path)
        self.originals_changed=dict(originals_changed)
        print(f'Copie ecrite: {path.name}, {path.stat().st_size:,} octets',flush=True)
    def validate_output(self,path):
        source=self.s; out=Structure(path)
        if out.size!=source.size or out.meta!=source.meta or out.palette!=source.palette:
            raise ValueError('Metadonnees, taille ou palette modifiees de facon inattendue')
        iterator=out.blocks(); original_nbt=0; unchanged=changed=0
        for pos,st,has_nbt,begin,end,off in source.blocks():
            op,ost,onbt,ob,oe,ooff=next(iterator)
            if op!=pos or ost!=self.changed.get(pos,st) or has_nbt!=onbt: raise ValueError(f'Difference inattendue a {pos}')
            raw=source.data[begin:end]
            if pos in self.changed:
                r=bytearray(raw); struct.pack_into('>i',r,off-begin,self.changed[pos]); raw=bytes(r); changed+=1
            else: unchanged+=1
            if raw!=out.data[ob:oe]: raise ValueError(f'Donnees NBT alterees a {pos}')
            if has_nbt: original_nbt+=1
        seen=set()
        for pos,st,has_nbt,*_ in iterator:
            if pos not in self.added or st!=self.added[pos] or has_nbt or pos in seen: raise ValueError('Ajout inattendu ou duplique')
            seen.add(pos)
        if seen!=set(self.added): raise ValueError('Ajouts manquants')
        current_sha=hashlib.sha256(source.path.read_bytes()).hexdigest()
        if current_sha!=source.sha256: raise ValueError('Le fichier source a change pendant la generation')
        self.validation={'source_unchanged':True,'source_sha256':current_sha,'output_sha256':out.sha256,
                         'size_unchanged':True,'root_metadata_unchanged':True,'entities_unchanged':True,
                         'original_blocks_identical':unchanged,'original_blocks_authorized_state_changes':changed,
                         'original_block_entity_records_identical':original_nbt,'added_records':len(seen),
                         'output_blocks':out.count,'output_palette_states':len(out.palette),
                         'protected_zones_added_vegetation':0,'garrik_added_trees_or_bushes':0,
                         'new_trees_connected_and_complete':True,'tested_in_minecraft':False}
        print('Verification complete: source intacte, donnees originales conservees, reserves respectees.',flush=True)
    def reports(self,path,source_report,assets):
        s=self.s; reasons=collections.Counter(self.change_reasons.values())
        feature_counts=collections.Counter(f['kind'] for f in self.features)
        species=collections.Counter(f['species'] for f in self.features if f['kind']=='tree')
        new_blocks=collections.Counter(s.palette[st]['Name'] for pos,st in {**self.changed,**self.added}.items()
                                      if self.change_reasons[pos] in ('tree','bush','plant'))
        sx,sy,sz=7-self.args.origin[0],-3-self.args.origin[1],1-self.args.origin[2]
        # Le centre exact X=7,Z=1 touche les quatre colonnes voisines (largeur 0,6).
        floor=[]; clear=[]
        for x in (sx-1,sx):
            for z in (sz-1,sz):
                floor.append(s.entry((x,sy-1,z)))
                for y in (sy,sy+1): clear.append(s.entry((x,y,z)))
        arrival_ok=(all(isinstance(v,dict) and v['Name']=='minecraft:grass_block' for v in floor)
                    and all(isinstance(v,dict) and v['Name']=='minecraft:air' for v in clear)
                    and not self.spawn_obstructions)
        report={'validation':self.validation,'origin_provisional':list(self.args.origin),
                'placement_bounds_inclusive':[[v for v in self.args.origin],
                    [self.args.origin[i]+s.size[i]-1 for i in range(3)]],
                'seed':self.args.seed,'densities':{'tree':self.args.tree_density,'bush':self.args.bush_density,'plant':self.args.plant_density},
                'candidate_surface_columns':self.initial_candidates,'added_features':dict(feature_counts),
                'added_tree_species':dict(species),'added_vegetation_blocks':dict(new_blocks),
                'change_reasons_blocks':dict(reasons),'modified_original_block_types':self.originals_changed,
                'building_reserves':self.regions,'garrik_world_xz_inclusive':[[-16,-80],[31,-33]],
                'spawn_world':[7,-3,1],'spawn_local':[sx,sy,sz],'spawn_clearance_radius':self.args.spawn_radius,
                'arrival_floor_and_clearance_verified':arrival_ok,'spawn_obstructions_local':self.spawn_obstructions,
                'block_assets_verification':assets,'features':[f for f in self.features if f['kind']!='plant'],
                'limitations':['Origine provisoire; les reserves en coordonnees du monde dependent de cette origine.',
                  'Aucun test ni placement dans Minecraft.',
                  'Un NBT de structure ne definit pas le point de teleportation du joueur.',
                  'Les constructions presentes dans le fichier source sont conservees.',
                  'Le NBT source est sparse: les cellules absentes restent inchangées dans le monde cible.']}
        (path.parent/'rapport_verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
        render(s,path.parent/'terrain_vegetalise.png',self.regions,self.args.origin)
        self.make_preview(path.parent/'apercu_zones.png')
        self.documentation(path,report)
        return report
    def documentation(self,path,report):
        v=report['validation']; f=report['added_features']; changes=report['change_reasons_blocks']
        rows=[]
        for r in self.regions:
            (x1,z1),(x2,z2)=r['world_xz']
            rows.append(f"  {r['label']:<8} X {x1:>4} a {x2:<4} | Z {z1:>4} a {z2:<4}")
        ox,oy,oz=self.args.origin
        arrival='COMPATIBLE dans le NBT : sol à Y=-4 et air aux pieds/à la tête' if report['arrival_floor_and_clearance_verified'] else 'INCOMPATIBLE : consulter les obstacles et les blocs dans les rapports'
        text=f'''PLATEFORME DE DÉPART VÉGÉTALISÉE — Minecraft Java 1.21.1 / NeoForge

1. FICHIERS
plateforme__4_vegetalisee.nbt : copie finale.
generer_vegetation.py : script réglable.
apercu_zones.png : schéma vu du dessus, pas une capture en jeu.
rapport_verification.json / analyse_source.json : preuves et coordonnées détaillées.

2. CONFIRMÉ / PROVISOIRE
Dimensions vérifiées : 562 × 93 × 536. DataVersion : 3955, identique à celui du
JAR Minecraft 1.21.1 consulté en lecture seule. Blocs ajoutés exclusivement vanilla.
Origine PROVISOIRE : ({ox}, {oy}, {oz}), sans rotation ni miroir.
Étendue inclusive : X={ox}..{ox+561}, Y={oy}..{oy+92}, Z={oz}..{oz+535}.
Les coins approximatifs donnent 461 × 96 × 476, donc ne définissent pas ce NBT.
Toutes les réserves en coordonnées du monde dépendent de l'origine provisoire.
Le fichier contient déjà des constructions, conservées conformément à la consigne.

3. MODIFICATIONS
{f.get('tree',0)} arbres complets ({report['added_tree_species'].get('oak',0)} chênes,
{report['added_tree_species'].get('birch',0)} bouleaux), {f.get('bush',0)} groupes de buissons,
{f.get('plant',0)} plantes : herbes, fougères et fleurs en petites taches, avec des clairières.
Troncs et couronnes connectés; feuilles persistantes pour empêcher leur disparition.
Six plaques rectangulaires suspendues et cinq points de repérage retirés :
{changes.get('marker_air',0)} blocs remplacés par de l'air, {changes.get('marker_ground',0)} par un sol d'herbe.
{changes.get('marker_soil_grass',0)} blocs de terre exposés sous les plaques rétablis en herbe à hauteur identique.
{changes.get('existing_low_plant_clearance',0)} plantes basses existantes retirées des réserves et de l'arrivée.
Autres matériaux colorés, constructions et feuillage décoratif existant conservés.

4. ZONES PROTÉGÉES — MONDE, LIMITES INCLUSES
Anciennes plaques :
{chr(10).join(rows)}
Marge de {self.args.building_margin} blocs autour de chaque rectangle; aucune végétation ajoutée.
Chemins : marge de {self.args.path_margin} blocs. Constructions/blocs avec NBT : marge de 3 blocs.
Garrik : X=-16..31, Z=-80..-33 (48 × 48), local X={-16-ox}..{31-ox}, Z={-80-oz}..{-33-oz}.
Aucun tronc, branche, feuille ou buisson ajouté, même depuis un arbre extérieur.
Les arbres existants restent; les herbes et fleurs sont permises.
Arrivée : rayon de {self.args.spawn_radius} blocs sans ajout de végétation.

5. ARRIVÉE EXACTE : X=7, Y=-3, Z=1
Résultat : {arrival}.
Position locale : ({7-ox}, {-3-oy}, {1-oz}). Contrôle des quatre colonnes touchées
par le joueur; volume 3 × 3 × 3 explicitement dégagé lorsque libre dans la source.
Un NBT ne définit pas la téléportation. Dans la fonction exécutée en tant que joueur :
execute in les_echos_du_monde:prologue run tp @s 7 -3 1
Ce script de végétation ne règle pas la fonction du datapack; l'installation
est une étape distincte, documentée dans le dossier Installation_ correspondant.

6. CONTRÔLES
Source intacte. {v['original_blocks_identical']:,} blocs identiques octet par octet;
{v['original_blocks_authorized_state_changes']:,} états modifiés seulement pour les marqueurs, leur sol et les plantes à dégager.
Données des {v['original_block_entity_records_identical']} blocs avec NBT, dimensions et métadonnées conservées.
Réserves contrôlées. Total final : {v['output_blocks']:,} blocs. Aucun test dans Minecraft.
Source SHA-256 : {v['source_sha256']}
Copie SHA-256 : {v['output_sha256']}

7. REFAIRE / AJUSTER
Python 3.12 + numpy + Pillow, déjà disponibles sur ce PC. Depuis ce dossier :
& 'C:\\Users\\Bastien\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe' '.\\generer_vegetation.py'
Options : --origin {ox} {oy} {oz} --seed {self.args.seed}
--tree-density {self.args.tree_density} --bush-density {self.args.bush_density} --plant-density {self.args.plant_density}
--tree-spacing {self.args.tree_spacing} --building-margin {self.args.building_margin} --path-margin {self.args.path_margin}
--output 'autre_copie.nbt' ; --audit-only pour analyser sans générer.
Le script refuse d'écraser la source. MARKERS et MARKER_EXTRAS décrivent ce fichier
précis : les revoir si les marqueurs changent. Une nouvelle origine recalcule les
réserves de Garrik et de l'arrivée; consulter de nouveau les résultats des contrôles.

8. À VÉRIFIER EN JEU
Dans un monde de test : placement à l'origine indiquée, sans rotation ni miroir;
arrivée exacte et espace du joueur; six réserves et accès; limites de Garrik;
aspect des arbres, circulation et survie des plantes avec l'éclairage réel.
Le modèle complet reste volumineux. Si tu utilises le placement par morceaux,
régénère les morceaux à partir de CE NBT. La copie ne corrige pas les problèmes
de chargement/mémoire du placement complet. Les cellules absentes et les éventuels
vides du relief source sont conservés : prévoir une zone de placement appropriée.

Référence des propriétés des feuilles, en complément du JAR vérifié :
https://lexxie.dev/neoforge/1.21.1/net/minecraft/world/level/block/LeavesBlock.html
'''
        (path.parent/'LISEZ_MOI.txt').write_text(text,encoding='utf-8')
    def make_preview(self,path):
        s=self.s
        im=Image.open(path.parent/'terrain_vegetalise.png').convert('RGB'); d=ImageDraw.Draw(im)
        for f in self.features:
            x,y,z=f['center_local']; col={'tree':(30,60,16),'bush':(55,91,18),'plant':(149,213,67)}[f['kind']]
            if f['kind']=='plant': continue
            r=3 if f['kind']=='tree' else 1
            d.ellipse((x*2-r,z*2-r,x*2+r,z*2+r),outline=col,width=1)
        canvas=Image.new('RGB',(im.width,im.height+70),(23,31,38)); canvas.paste(im,(0,70)); d=ImageDraw.Draw(canvas)
        d.text((16,10),'Vue schematique du NBT - nord vers le haut (+Z vers le bas)',fill='white')
        d.text((16,28),'Blanc : reserves + marge 4 blocs | Orange : Garrik | Cyan : arrivee 7, -3, 1',fill='white')
        d.text((16,46),'Relief et constructions conserves. Origine provisoire : -235, -30, -250. Pas de test en jeu.',fill='white')
        canvas.save(path)

def render(s,path,regions,origin,generated=None):
    pix=np.full((s.Z,s.X,3),(22,31,40),np.uint8)
    for i,n in enumerate(s.names):
        col=(133,133,130)
        if n in SOIL: col=(104,139,73)
        if n=='dirt_path': col=(183,160,104)
        if n in ('gravel','coarse_dirt'): col=(160,144,118)
        if n in ('sand','sandstone'): col=(214,200,144)
        if n=='water': col=(59,107,170)
        if 'leaves' in n: col=(57,109,54)
        if 'log' in n or 'wood' in n: col=(116,84,58)
        if s.palette[i]['Name'] in COLOR_BLOCKS: col=RGB[COLORS.index(COLOR_BLOCKS[s.palette[i]['Name']])]
        pix[s.top_state==i]=col
    heights=np.maximum(s.top,0)
    shade=np.clip(.91+(heights-np.roll(heights,1,axis=0))*.05,.6,1.25)
    pix=np.clip(pix.astype(float)*shade[:,:,None],0,255).astype(np.uint8)
    im=Image.fromarray(pix).resize((s.X*2,s.Z*2),Image.Resampling.NEAREST); d=ImageDraw.Draw(im)
    for r in regions:
        lo,hi=r['local_xz']; d.rectangle((lo[0]*2,lo[1]*2,hi[0]*2+1,hi[1]*2+1),outline='white',width=1)
        if r.get('margin'):
            m=r['margin']; d.rectangle(((lo[0]-m)*2,(lo[1]-m)*2,(hi[0]+m)*2+1,(hi[1]+m)*2+1),outline=(195,195,195),width=1)
        if r['count']>=15: d.text((lo[0]*2,lo[1]*2),str(r.get('label',r.get('id'))),fill='white',stroke_width=1,stroke_fill='black')
    x1,x2=-16-origin[0],31-origin[0]; z1,z2=-80-origin[2],-33-origin[2]
    d.rectangle((x1*2,z1*2,x2*2+1,z2*2+1),outline=(255,116,44),width=2)
    x,z=7-origin[0],1-origin[2]
    d.ellipse((x*2-6,z*2-6,x*2+6,z*2+6),outline='cyan',width=2)
    im.save(path)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parent.parent/'plateforme__4.nbt')
    p.add_argument('--output',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parent/'plateforme__4_vegetalisee.nbt')
    p.add_argument('--origin',nargs=3,type=int,default=(-235,-30,-250))
    p.add_argument('--seed',type=int,default=20261001)
    p.add_argument('--tree-density',type=float,default=.0018)
    p.add_argument('--bush-density',type=float,default=.0016)
    p.add_argument('--plant-density',type=float,default=.10)
    p.add_argument('--tree-spacing',type=int,default=11)
    p.add_argument('--building-margin',type=int,default=4)
    p.add_argument('--path-margin',type=int,default=2)
    p.add_argument('--spawn-radius',type=int,default=5)
    p.add_argument('--minecraft-jar',type=pathlib.Path,default=pathlib.Path(r'C:\Users\Bastien\curseforge\minecraft\Install\versions\1.21.1\1.21.1.jar'))
    p.add_argument('--audit-only',action='store_true')
    a=p.parse_args()
    if a.source.resolve()==a.output.resolve(): p.error('La sortie doit differer de la source.')
    if min(a.tree_density,a.bush_density,a.plant_density)<0 or a.plant_density>1: p.error('Densites invalides')
    if min(a.building_margin,a.path_margin,a.spawn_radius)<0 or a.tree_spacing<1: p.error('Marges invalides')
    s=Structure(a.source); print(f'Taille {s.size}; {s.count:,} blocs; {len(s.palette)} etats',flush=True)
    s.load_grid(); report,comps=audit(s,a.origin,a.output.parent)
    print(json.dumps({k:report[k] for k in ['size','DataVersion','blocks','entities_count','block_entities_count','arrival']},ensure_ascii=False,indent=2),flush=True)
    if a.audit_only: return
    generator=Generator(s,a).generate(); assets=generator.check_assets(a.minecraft_jar)
    print('Vegetation creee:',dict(collections.Counter(f['kind'] for f in generator.features)),flush=True)
    generator.write(a.output); generator.validate_output(a.output)
    final=generator.reports(a.output,report,assets)
    print(json.dumps({k:final[k] for k in ['added_features','added_tree_species','change_reasons_blocks','arrival_floor_and_clearance_verified']},ensure_ascii=False,indent=2),flush=True)

if __name__=='__main__': main()
