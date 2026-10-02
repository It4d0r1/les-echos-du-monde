"""Prove the prepared NBT differs only at the 109 reviewed orphan leaf records."""
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parents[1]
WORK=PROJECT/'outputs/prologue_plateforme17'
sys.path.insert(0,str(PROJECT/'06_RESSOURCES/Structures_NBT/Vegetation_finale'))
import generer_vegetation as nbt

def main():
    manifest=json.loads((ROOT/'feuilles_a_retirer.json').read_text(encoding='utf-8'))
    positions={tuple(p) for p in manifest['positions_local']}
    backup=Path((ROOT/'backup_path.txt').read_text(encoding='utf-8-sig').strip())
    before=nbt.Structure(backup/'travail_avant/plateforme__17_preparee.nbt')
    after=nbt.Structure(WORK/'plateforme__17_preparee.nbt')
    if before.size!=after.size or before.meta!=after.meta or before.palette!=after.palette or before.count!=after.count:
        raise AssertionError('Unexpected structural metadata difference')
    seen=set(); unchanged=0; persistent=[]
    for previous,current in zip(before.blocks(),after.blocks(),strict=True):
        pos,state,has_nbt,begin,end,offset=previous
        npos,nstate,nnbt,nbegin,nend,noffset=current
        if pos!=npos or has_nbt!=nnbt: raise AssertionError('Record reordered or lost')
        old=before.data[begin:end]; new=after.data[nbegin:nend]
        if pos in positions:
            if before.palette[state]['Name']!='minecraft:oak_leaves' or after.palette[nstate]['Name']!='minecraft:air' or has_nbt:
                raise AssertionError('Unexpected correction')
            if before.palette[state]['Properties']['persistent']!='false':
                persistent.append({'local':pos,'world':[pos[i]+manifest['origin_xyz'][i] for i in range(3)],'state':before.palette[state]})
            raw=bytearray(old); struct.pack_into('>i',raw,offset-begin,nstate)
            if bytes(raw)!=new: raise AssertionError('NBT field changed beyond leaf state')
            seen.add(pos)
        elif old!=new:
            raise AssertionError(f'Unexpected change outside reviewed leaves: {pos}')
        else: unchanged+=1
    if seen!=positions: raise AssertionError('Some leaf positions missing')
    if {tuple(p['local']) for p in persistent}!={tuple(p) for p in manifest['persistent_source_positions_local']}:
        raise AssertionError('Persistent original fragments do not match correction filter')
    source=PROJECT/'06_RESSOURCES/Structures_NBT/plateforme__17.nbt'
    if hashlib.sha256(source.read_bytes()).hexdigest()!=manifest['source_sha256']: raise AssertionError('Source changed')
    func=WORK/'datapack/data/les_echos_du_monde/function'
    root=func/'world/leaves_v17'
    parsed=set()
    import re
    for path in (root/'chunks').glob('*.mcfunction'):
        text=path.read_text(encoding='utf-8')
        for x,y,z,props in re.findall(r'execute if block (-?\d+) (-?\d+) (-?\d+) minecraft:oak_leaves\[([^\]]+)\] run setblock',text):
            local=tuple(int(v)-manifest['origin_xyz'][i] for i,v in enumerate((x,y,z)))
            if local in parsed: raise AssertionError('Repeated cleanup coordinate')
            expected='persistent=true,distance=7,waterlogged=false' if local in {tuple(p['local']) for p in persistent} else 'persistent=false'
            if props!=expected: raise AssertionError('Wrong source-state filter')
            parsed.add(local)
        if 'forceload' in text or 'place template' in text or 'edm_seg_done' in text:
            raise AssertionError('Repair attempts to replace terrain or rewrite segment progress')
    if parsed!=positions: raise AssertionError('Cleanup commands differ from NBT correction')
    result={'reviewed_orphan_oak_leaves':len(seen),'other_records_identical':unchanged,
            'metadata_and_palette_identical':True,'entities_and_block_entities_identical':True,
            'original_source_unchanged':True,'existing_world_cleanup_positions_match_exactly':True,
            'cleanup_does_not_replace_segments':True,'persistent_source_orphans':len(persistent),'minecraft_cleanup_tested':False}
    (ROOT/'verification_correctif.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False),flush=True)

if __name__=='__main__': main()
