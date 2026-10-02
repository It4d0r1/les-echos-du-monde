"""Record this correction against its own pre-correction snapshot."""
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parents[1]
WORK=PROJECT/'outputs/prologue_plateforme17'
sys.path.insert(0,str(WORK))
from install_pack import inventory, STAGE, LIVE

backup=Path((ROOT/'backup_path.txt').read_text(encoding='utf-8-sig').strip())
before=inventory(backup/'datapack_installe_avant')
stage=inventory(STAGE); installed=inventory(LIVE)
if stage!=installed: raise AssertionError('Installed pack differs from validated staging')
result={'backup_before_leaf_correction':str(backup),'installed_root':str(LIVE),
        'installed_files_verified':len(installed),'installed_matches_staging':True,
        'created':sorted(set(stage)-set(before)),
        'modified':sorted(name for name in set(stage)&set(before) if stage[name]!=before[name]),
        'removed':sorted(set(before)-set(stage)),
        'original_source_unchanged':True,'minecraft_cleanup_tested':False}
(ROOT/'rapport_installation_correctif.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:result[k] for k in ('installed_files_verified','installed_matches_staging','backup_before_leaf_correction')},ensure_ascii=False))
print(json.dumps({'created':len(result['created']),'modified':len(result['modified']),'removed':len(result['removed'])}))
