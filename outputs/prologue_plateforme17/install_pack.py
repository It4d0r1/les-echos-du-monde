"""Package/sync the reviewed pack; optional installation into its exact instance path.

Does not open or write any save, add a mod or touch a jar. Refuses installation
if the current live pack has changed since the recorded backup.
"""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parents[1]
STAGE=ROOT/'datapack'
LIVE=Path(r'C:\Users\Bastien\curseforge\minecraft\Instances\Pixelmon Les Échos du Monde\global_packs\required_data\les_echos_du_monde')

def inventory(folder):
    return {p.relative_to(folder).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
            for p in folder.rglob('*') if p.is_file()}

def copy_checked(destination,expected):
    destination.mkdir(parents=True,exist_ok=True)
    for name in expected:
        target=destination/name; target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(STAGE/name,target)
    actual=inventory(destination)
    if any(actual.get(name)!=sha for name,sha in expected.items()):
        raise AssertionError('Installed copy differs from staging')
    return len(actual), sorted(set(actual)-set(expected))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--install-live',action='store_true')
    args=parser.parse_args()
    verification=json.loads((ROOT/'verification_datapack.json').read_text(encoding='utf-8'))
    if verification['new_segments']!=203 or not verification['source_hash_still_matches']:
        raise AssertionError('Validation not successful')
    expected=inventory(STAGE)
    backup=Path((ROOT/'backup_path.txt').read_text(encoding='utf-8-sig').strip())
    if args.install_live:
        baseline=inventory(backup/'datapack_installe_avant')
        current=inventory(LIVE)
        # An already identical installation is safe to verify again.
        if current!=baseline and current!=expected:
            raise RuntimeError('Live datapack changed after backup; inspect it before installation.')
        count,extra=copy_checked(LIVE,expected)
        report={'installed_at_local':datetime.now().isoformat(timespec='seconds'),
                'installed_path':str(LIVE),'backup_path':str(backup),
                'files_verified':len(expected),'target_files':count,'extra_files':extra,
                'all_staged_file_hashes_match':True,'save_files_modified':False,
                'mods_added':False,'jars_modified':False,'tested_in_minecraft':False}
        (ROOT/'rapport_installation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
        print(json.dumps(report,ensure_ascii=False))
    else:
        reference=PROJECT/'outputs/les_echos_du_monde_datapack'
        count,extra=copy_checked(reference,expected)
        archive=ROOT/'les_echos_du_monde_prologue17.zip'
        with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            for name in sorted(expected): z.write(STAGE/name,name)
        with zipfile.ZipFile(archive) as z:
            if set(z.namelist())!=set(expected): raise AssertionError('ZIP file listing mismatch')
            if any(hashlib.sha256(z.read(name)).hexdigest()!=sha for name,sha in expected.items()):
                raise AssertionError('ZIP differs from staging')
        (ROOT/'pack_file_hashes.json').write_text(json.dumps(expected,ensure_ascii=False,indent=2),encoding='utf-8')
        print(json.dumps({'project_copy':str(reference),'files_verified':len(expected),'extra_project_files':extra,
                          'zip':str(archive),'zip_bytes':archive.stat().st_size,'zip_contents_verified':True},ensure_ascii=False))

if __name__=='__main__': main()
