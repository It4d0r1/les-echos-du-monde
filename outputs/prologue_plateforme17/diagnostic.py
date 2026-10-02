"""Read-only inspection of the new prologue structure and colored markers."""
import collections
import json
import pathlib
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

PROJECT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT / '06_RESSOURCES/Structures_NBT/Vegetation_finale'))
import generer_vegetation as reader

source = PROJECT / '06_RESSOURCES/Structures_NBT/plateforme__17.nbt'
structure = reader.Structure(source)
print(f'Dimensions={structure.size}, blocks={structure.count}, palette={len(structure.palette)}', flush=True)
structure.load_grid()
markers = []
for index, state in enumerate(structure.palette):
    name = state['Name']
    if name not in reader.COLOR_BLOCKS or not structure.counts[index]:
        continue
    ys, zs, xs = np.where(structure.grid == index)
    footprint = np.zeros((structure.Z, structure.X), dtype=bool)
    footprint[zs, xs] = True
    components = reader.components(footprint)
    areas = []
    for points in components:
        px = [p[0] for p in points]
        pz = [p[1] for p in points]
        areas.append({'min_x': min(px), 'max_x': max(px), 'min_z': min(pz),
                      'max_z': max(pz), 'columns': len(points)})
    markers.append({'block': name, 'color': reader.COLOR_BLOCKS[name],
                    'count': len(xs), 'min_local': [int(xs.min()), int(ys.min()), int(zs.min())],
                    'max_local': [int(xs.max()), int(ys.max()), int(zs.max())],
                    'component_count': len(areas),
                    'components': sorted(areas, key=lambda p: p['columns'], reverse=True)})

column = []
# Candidate X/Z only: previous stated source corner, not an accepted placement.
if structure.X > 250 and structure.Z > 235:
    for y in range(structure.Y):
        state = int(structure.grid[y, 235, 250])
        if state != reader.MISSING:
            name = structure.palette[state]['Name']
            if name not in {'minecraft:air', 'minecraft:cave_air', 'minecraft:void_air', 'minecraft:structure_void'}:
                column.append({'local_y': y, 'block': name})

report = {
    'source': str(source), 'sha256': structure.sha256, 'size_xyz': structure.size,
    'DataVersion': structure.meta.get('DataVersion'), 'block_entries': structure.count,
    'duplicates': structure.duplicates, 'block_entities_count': len(structure.block_entities),
    'entities_count': len(structure.meta.get('entities', [])),
    'stated_source_corner_1': [-250, 26, -235], 'stated_source_corner_2': [200, 65, 225],
    'inclusive_size_from_stated_corners': [451, 40, 461],
    'corners_match_size': tuple(structure.size) == (451, 40, 461),
    'markers': markers, 'candidate_column_local_x250_z235': column,
    'common_blocks': [{'block': structure.palette[i]['Name'], 'count': count}
                      for i, count in structure.counts.most_common(15)],
    'placement_origin': None, 'vegetation_changes': 'none', 'datapack_changes': 'none'
}
concrete_indices = [i for i, p in enumerate(structure.palette)
                    if p['Name'].startswith('minecraft:') and p['Name'].endswith('_concrete')]
brown_indices = [i for i, p in enumerate(structure.palette)
                 if p['Name'] == 'minecraft:brown_concrete']
brown = np.isin(structure.grid, brown_indices).any(axis=0)
if brown.any():
    zz, xx = np.where(brown)
    crop = brown[zz.min():zz.max()+1, xx.min():xx.max()+1]
    outside = np.zeros_like(crop)
    queue = collections.deque()
    for z in range(crop.shape[0]):
        for x in (0, crop.shape[1]-1):
            if not crop[z,x] and not outside[z,x]:
                outside[z,x] = True; queue.append((z,x))
    for x in range(crop.shape[1]):
        for z in (0, crop.shape[0]-1):
            if not crop[z,x] and not outside[z,x]:
                outside[z,x] = True; queue.append((z,x))
    while queue:
        z,x = queue.popleft()
        for nz,nx in ((z-1,x),(z+1,x),(z,x-1),(z,x+1)):
            if 0 <= nz < crop.shape[0] and 0 <= nx < crop.shape[1] and not crop[nz,nx] and not outside[nz,nx]:
                outside[nz,nx] = True; queue.append((nz,nx))
    report['brown_enclosed_columns'] = int((~outside & ~crop).sum())

# A diagnostic projection only; the NBT and all block states remain unchanged.
colors = np.full((reader.MISSING+1,3), (195,204,197), dtype=np.uint8)
colors[reader.MISSING] = (236,240,243)
for i, name in enumerate(structure.names):
    if name in reader.AIR or name == 'structure_void': colors[i] = (236,240,243)
    elif name in reader.SOIL or name in reader.LOW_PLANTS: colors[i] = (124,157,84)
    elif 'leaves' in name: colors[i] = (50,99,49)
    elif 'water' in name: colors[i] = (68,130,191)
    elif 'log' in name or 'wood' in name or 'planks' in name: colors[i] = (129,101,66)
    elif 'stone' in name or 'gravel' in name: colors[i] = (154,154,149)
terrain = colors[structure.top_state].copy()
for i in concrete_indices:
    color = reader.COLOR_BLOCKS[structure.palette[i]['Name']]
    terrain[(structure.grid == i).any(axis=0)] = reader.RGB[reader.COLORS.index(color)]
zoom = 2
map_image = Image.fromarray(terrain).resize((structure.X*zoom,structure.Z*zoom),Image.Resampling.NEAREST)
canvas = Image.new('RGB',(structure.X*zoom+330,structure.Z*zoom+80),'white')
canvas.paste(map_image,(45,55))
draw = ImageDraw.Draw(canvas)
font = ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf',16)
small = ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf',13)
draw.text((45,12),'plateforme__17 — repères colorés, vue de dessus',fill='black',font=font)
draw.text((structure.X*zoom+70,55),'Coordonnées locales du NBT',fill='black',font=font)
draw.text((structure.X*zoom+70,80),'Le placement reste à définir.',fill='black',font=small)
for step in range(0,max(structure.X,structure.Z)+1,100):
    if step<structure.X: draw.text((45+step*zoom,35),str(step),fill='black',font=small)
    if step<structure.Z: draw.text((5,55+step*zoom),str(step),fill='black',font=small)
for j, i in enumerate(concrete_indices):
    block = structure.names[i]
    color = reader.COLOR_BLOCKS[structure.palette[i]['Name']]
    rgb = reader.RGB[reader.COLORS.index(color)]
    y = 125+j*31
    draw.rectangle((structure.X*zoom+70,y,structure.X*zoom+90,y+18),fill=rgb,outline='black')
    draw.text((structure.X*zoom+99,y),block,fill='black',font=small)
preview = pathlib.Path(__file__).resolve().parent / 'reperes.png'
canvas.save(preview)
report['marker_preview'] = str(preview)
destination = pathlib.Path(__file__).resolve().parent / 'diagnostic.json'
destination.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({k: report[k] for k in ['size_xyz', 'DataVersion', 'block_entries',
                                      'corners_match_size', 'block_entities_count', 'entities_count']}, ensure_ascii=False), flush=True)
for marker in markers:
    print(f"{marker['block']}: {marker['count']} blocks, {marker['component_count']} components, local bounds={marker['min_local']}..{marker['max_local']}", flush=True)
print('Center column:', column[-8:], flush=True)
print('Brown enclosed columns:',report.get('brown_enclosed_columns',0),flush=True)
print('Report:', destination, flush=True)
