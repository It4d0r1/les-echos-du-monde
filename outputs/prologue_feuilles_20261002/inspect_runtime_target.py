"""Read-only comparison of the installed segment and foliage near the reported leaf."""
import collections
import hashlib
import json
import pathlib
import sys

PROJECT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT / '06_RESSOURCES/Structures_NBT/Vegetation_finale'))
import generer_vegetation as reader

TARGET = (-20, -1, 6)
LIVE = pathlib.Path(r'C:\Users\Bastien\curseforge\minecraft\Instances\Pixelmon Les Échos du Monde\global_packs\required_data\les_echos_du_monde')
STAGING = PROJECT / 'outputs/prologue_plateforme17/datapack'
DEST = pathlib.Path(__file__).resolve().parent

def sid(sx, sz):
    def p(n): return ('m' if n < 0 else 'p') + f'{abs(n):02d}'
    return f's_{p(sx)}_{p(sz)}'

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

records = {}
comparisons = []
for sx in range(-2, 1):
    for sz in range(-1, 2):
        name = sid(sx, sz)
        relative = pathlib.Path('data/les_echos_du_monde/structure/platform_segments_v17') / (name + '.nbt')
        live, staged = LIVE / relative, STAGING / relative
        if not live.exists(): continue
        piece = reader.Structure(live)
        for pos, state, *_ in piece.blocks():
            x, y, z = pos
            records[(x + sx*32, y - 26, z + sz*32)] = piece.palette[state]
        comparisons.append({'segment': name, 'size': list(piece.size), 'block_count': piece.count,
                            'live_sha256': sha(live), 'same_as_staging': staged.exists() and sha(live) == sha(staged)})

def leaf(state): return state['Name'].endswith('_leaves')
def log(state): return state['Name'].endswith(('_log', '_wood', '_stem', '_hyphae'))
def dist(pos): return sum(abs(pos[i] - TARGET[i]) for i in range(3))
def neighbours(pos):
    for axis in range(3):
        for delta in (-1, 1):
            p = list(pos); p[axis] += delta
            yield tuple(p)

leaves = {p: s for p, s in records.items() if leaf(s)}
logs = {p: s for p, s in records.items() if log(s)}
component = {TARGET} if TARGET in leaves else set()
queue = collections.deque(component)
while queue:
    pos = queue.popleft()
    for n in neighbours(pos):
        if n in leaves and n not in component:
            component.add(n); queue.append(n)

nearest = sorted(logs, key=dist)[:12]
touching_logs = {n for p in component for n in neighbours(p) if n in logs}
local_states = [{'world_xyz': list(p), 'state': records.get(p, 'ABSENT')}
                for p in [TARGET, *neighbours(TARGET)]]

functions = ['segment/s_m01_p00/place', 'segment/s_m01_p00/start', 'segment/s_m01_p00/poll',
             'select_spawn', 'cycle', 'ready_spawn', 'player']
function_comparisons = []
for name in functions:
    relative = pathlib.Path('data/les_echos_du_monde/function/world/segments_v17') / (name + '.mcfunction')
    live, staged = LIVE / relative, STAGING / relative
    function_comparisons.append({'function': name, 'same_as_staging': live.exists() and staged.exists() and sha(live) == sha(staged)})

report = {'target_world_xyz': list(TARGET), 'target_template': 's_m01_p00', 'target_template_local_xyz': [12,25,6],
          'read_only': True, 'segment_comparisons': comparisons, 'function_comparisons': function_comparisons,
          'target_and_neighbours': local_states, 'leaf_connected_component_count': len(component),
          'leaf_component_min_xyz': [min(p[i] for p in component) for i in range(3)] if component else None,
          'leaf_component_max_xyz': [max(p[i] for p in component) for i in range(3)] if component else None,
          'touching_log_count': len(touching_logs),
          'nearest_logs': [{'world_xyz': list(p), 'manhattan_distance': dist(p), 'state': logs[p]} for p in nearest],
          'target_component_leaves_in_radius_6': [{'world_xyz': list(p), 'state': leaves[p]} for p in sorted(component) if dist(p) <= 6]}
out = DEST / 'runtime_target_report.json'
out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: report[k] for k in ['target_world_xyz','target_and_neighbours','leaf_connected_component_count','touching_log_count','nearest_logs']},ensure_ascii=False,indent=2))
