"""Offline consistency checks. Does not launch Minecraft or claim game testing."""
from pathlib import Path
import hashlib
import json
import re
import sys
import numpy as np

ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parents[1]
PACK=ROOT/'datapack'
sys.path.insert(0,str(PROJECT/'06_RESSOURCES/Structures_NBT/Vegetation_finale'))
import generer_vegetation as nbt

def main():
    files=list(PACK.rglob('*')); functions={f'les_echos_du_monde:{p.relative_to(PACK/"data/les_echos_du_monde/function").with_suffix("").as_posix()}':p
            for p in (PACK/'data/les_echos_du_monde/function').rglob('*.mcfunction')}
    missing=[]; function_refs=template_refs=0
    for identifier,path in functions.items():
        text=path.read_text(encoding='utf-8-sig')
        if text.startswith('\ufeff'): raise AssertionError('BOM in function')
        for line in text.splitlines():
            if not line.strip() or line.lstrip().startswith('#'): continue
            if line.startswith('/'): raise AssertionError(f'Slash in function {path}')
            refs=re.findall(r'\bfunction (les_echos_du_monde:[a-z0-9_./-]+)',line)
            refs+=re.findall(r'\bschedule clear (les_echos_du_monde:[a-z0-9_./-]+)',line)
            for ref in refs:
                function_refs+=1
                if ref not in functions: missing.append({'file':str(path),'function':ref})
            for ref in re.findall(r'\bplace template (les_echos_du_monde:[a-z0-9_./-]+)',line):
                template_refs+=1
                target=PACK/'data/les_echos_du_monde/structure'/(ref.split(':')[1]+'.nbt')
                if not target.is_file(): missing.append({'file':str(path),'template':ref})
    if missing: raise AssertionError(json.dumps(missing[:20],ensure_ascii=False))
    json_count=0
    for path in files:
        if path.is_file() and (path.suffix=='.json' or path.name=='pack.mcmeta'):
            json.loads(path.read_text(encoding='utf-8-sig')); json_count+=1
    if json.loads((PACK/'pack.mcmeta').read_text(encoding='utf-8'))['pack']['pack_format']!=48:
        raise AssertionError('Wrong format for Minecraft1.21.1')
    for kind in ('load','tick'):
        tag=json.loads((PACK/f'data/minecraft/tags/function/{kind}.json').read_text(encoding='utf-8'))
        if f'les_echos_du_monde:{kind}' not in tag['values']: raise AssertionError('Missing automatic function tag')
    manifest=json.loads((ROOT/'segments_manifest.json').read_text(encoding='utf-8'))
    for seg in manifest['segments']:
        path=PACK/'data/les_echos_du_monde/structure'/(seg['template'].split(':')[1]+'.nbt')
        if hashlib.sha256(path.read_bytes()).hexdigest()!=seg['sha256']: raise AssertionError('Segment changed')
        runtime=PACK/'data/les_echos_du_monde/function/world/segments_v17/segment'/seg['id']
        if (runtime/'poll.mcfunction').read_text(encoding='utf-8').count('if loaded')!=9: raise AssertionError('Wrong chunk loading checks')
        if (runtime/'cleanup.mcfunction').read_text(encoding='utf-8').count('run forceload remove')!=9: raise AssertionError('Wrong cleanup ownership checks')
        place=(runtime/'place.mcfunction').read_text(encoding='utf-8')
        if f"place template {seg['template']} {seg['x']} {seg['y']} {seg['z']}" not in place: raise AssertionError('Wrong placement')
    report=json.loads((ROOT/'rapport_preparation.json').read_text(encoding='utf-8'))
    source=Path(report['source'])
    if hashlib.sha256(source.read_bytes()).hexdigest()!=report['validation']['source_sha256']: raise AssertionError('Source changed')
    # Check actual exit ground separately: its former fixed coordinates are provisional.
    final=nbt.Structure(ROOT/'plateforme__17_preparee.nbt'); final.load_grid()
    exit_columns=[]; ox,oy,oz=manifest['origin_xyz']
    for x in range(-1,2):
        for z in range(6,9):
            lx,lz=x-ox,z-oz
            top=int(final.top[lz,lx]); st=int(final.top_state[lz,lx])
            exit_columns.append({'world_xz':[x,z],'surface_y':top+oy,
                                 'surface_block':final.palette[st]['Name'] if st!=nbt.MISSING else None})
    document={
        'pack_format':48,'json_files_parsed':json_count,'function_files':len(functions),
        'function_references_resolved':function_refs,'template_references_resolved':template_refs,
        'new_segments':len(manifest['segments']),'segment_hashes_match':True,
        'source_hash_still_matches':True,'load_tick_tags_present':True,
        'nine_loading_and_ownership_cleanup_checks_per_segment':True,
        'exit_ground_columns':exit_columns,
        'minecraft_executed':False,
        'limit':'Static consistency and NBT checks; command compatibility reviewed against installed vanilla1.21.1 bytecode. This is not a Minecraft execution test.'
    }
    (ROOT/'verification_datapack.json').write_text(json.dumps(document,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(document,ensure_ascii=False),flush=True)

if __name__=='__main__': main()
