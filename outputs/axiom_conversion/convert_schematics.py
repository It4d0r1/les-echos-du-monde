"""Convert legacy MCEdit schematics to Axiom blueprints; verify every voxel.

Format reference: PiTheGuy/SchemConvert AxiomSchematicFormat.java.
Block mappings: EngineHub/WorldEdit legacy.json. Both references are retained
in tools/. Original schematic files are never modified.
"""
from __future__ import annotations

import csv
import gzip
import hashlib
import io
import json
import math
from pathlib import Path
import struct
import sys

BASE = Path(__file__).resolve().parent
PROJECT = BASE.parent.parent
sys.path.insert(0, str(BASE / "dependencies"))
import nbtlib as nbt
import numpy as np
from PIL import Image, ImageDraw

MAGIC = 0x0AE5BB36
DATA_VERSION = 3955  # Minecraft Java 1.21.1
OUTPUT = BASE / "blueprints"


def serialize(compound):
    stream = io.BytesIO()
    nbt.File(compound).write(stream)
    return stream.getvalue()


def block_tag(state):
    name, _, tail = state.partition("[")
    result = nbt.Compound({"Name": nbt.String(name)})
    if tail:
        result["Properties"] = nbt.Compound({
            k: nbt.String(v) for k, v in
            (part.split("=", 1) for part in tail.rstrip("]").split(","))
        })
    return result


def state_string(tag):
    name = str(tag["Name"])
    props = tag.get("Properties", {})
    if props:
        name += "[" + ",".join(f"{k}={props[k]}" for k in sorted(props)) + "]"
    return name


def base_color(state):
    if "leaves" in state:
        if "spruce" in state: return (45, 91, 55)
        if "birch" in state: return (113, 142, 67)
        if "acacia" in state: return (92, 128, 63)
        return (65, 130, 54)
    if "birch_log" in state or "birch_wood" in state: return (212, 211, 187)
    if "log" in state or "wood" in state: return (111, 83, 48)
    if "planks" in state or "slab" in state or "stairs" in state: return (131, 101, 60)
    if "pumpkin" in state: return (192, 119, 25)
    if "cocoa" in state: return (130, 83, 35)
    if "mushroom" in state: return (152, 55, 42)
    if "green" in state or "lime" in state: return (84, 134, 45)
    if "white" in state or "web" in state: return (225, 225, 211)
    if "pink" in state: return (213, 149, 169)
    if "purple" in state or "magenta" in state: return (146, 88, 165)
    if "red" in state: return (158, 66, 49)
    if "orange" in state: return (177, 103, 41)
    if "yellow" in state: return (191, 166, 52)
    return (124, 128, 112)


def thumbnail(codes, states):
    """Approximate isometric voxel preview; not a Minecraft screenshot."""
    h, length, width = codes.shape
    occupied = codes != 0
    cells = np.argwhere(occupied)
    image = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    if not len(cells):
        raise ValueError("Empty schematic")
    xmin, xmax = cells[:, 2].min(), cells[:, 2].max() + 1
    zmin, zmax = cells[:, 1].min(), cells[:, 1].max() + 1
    ymin, ymax = cells[:, 0].min(), cells[:, 0].max() + 1
    corners = [(x-z, .5*(x+z)-y) for x in [xmin,xmax]
               for y in [ymin,ymax] for z in [zmin,zmax]]
    umin, umax = min(c[0] for c in corners), max(c[0] for c in corners)
    vmin, vmax = min(c[1] for c in corners), max(c[1] for c in corners)
    scale = min(232/max(1,umax-umin), 232/max(1,vmax-vmin))
    ox, oy = 128-(umin+umax)*scale/2, 128-(vmin+vmax)*scale/2
    def p(x,y,z): return (ox+(x-z)*scale, oy+(.5*(x+z)-y)*scale)
    def tint(color, factor): return tuple(min(255,int(v*factor)) for v in color)+(255,)
    draw = ImageDraw.Draw(image)
    colors = {c: base_color(s) for c,s in states.items()}
    for y,z,x in sorted(cells.tolist(), key=lambda q:(sum(q),q[0])):
        color = colors[int(codes[y,z,x])]
        if x == width-1 or not occupied[y,z,x+1]:
            draw.polygon([p(x+1,y,z),p(x+1,y,z+1),p(x+1,y+1,z+1),p(x+1,y+1,z)],fill=tint(color,.83))
        if z == length-1 or not occupied[y,z+1,x]:
            draw.polygon([p(x,y,z+1),p(x+1,y,z+1),p(x+1,y+1,z+1),p(x,y+1,z+1)],fill=tint(color,.68))
        if y == h-1 or not occupied[y+1,z,x]:
            draw.polygon([p(x,y+1,z),p(x+1,y+1,z),p(x+1,y+1,z+1),p(x,y+1,z+1)],fill=tint(color,1.12))
    out=io.BytesIO();image.save(out,format="PNG")
    return out.getvalue()


def read_source(path, mapping):
    root = nbt.load(path)
    width,height,length = (int(root[k]) for k in ("Width","Height","Length"))
    if min(width,height,length) <= 0: raise ValueError("Invalid dimensions")
    for key in ("Entities","TileEntities","TileTicks"):
        if len(root.get(key, [])):
            raise ValueError(f"Nonempty {key}: conversion needs explicit support")
    blocks = np.asarray(root["Blocks"],dtype=np.int64)&255
    data = np.asarray(root["Data"],dtype=np.int64)&15
    if len(blocks)!=width*height*length or len(data)!=len(blocks):
        raise ValueError("Invalid Blocks/Data length")
    if "AddBlocks" in root:
        extra=np.asarray(root["AddBlocks"],dtype=np.int64)&255
        expanded=np.empty(len(extra)*2,dtype=np.int64)
        expanded[::2]=extra&15;expanded[1::2]=extra>>4
        blocks |= expanded[:len(blocks)]<<8
    codes=(blocks*16+data).reshape(height,length,width)
    states={}
    for code in np.unique(codes):
        key=f"{code//16}:{code%16}"
        if key not in mapping: raise ValueError(f"Unknown legacy block {key}")
        states[int(code)]=state_string(block_tag(mapping[key]))
    return codes,states


def write_blueprint(path, source, codes, states):
    height,length,width=codes.shape
    regions=[]
    for ry in range(math.ceil(height/16)):
        for rz in range(math.ceil(length/16)):
            for rx in range(math.ceil(width/16)):
                tile=np.zeros((16,16,16),dtype=np.int64)
                portion=codes[ry*16:min(height,(ry+1)*16),rz*16:min(length,(rz+1)*16),rx*16:min(width,(rx+1)*16)]
                tile[:portion.shape[0],:portion.shape[1],:portion.shape[2]]=portion
                if not np.any(tile): continue
                unique=np.unique(tile)
                palette=[block_tag("minecraft:structure_void" if int(c)==0 else states[int(c)]) for c in unique]
                indices=np.searchsorted(unique,tile.reshape(-1)).astype(np.uint64)
                bits=max(4,(len(palette)-1).bit_length());per_long=64//bits
                packed=np.zeros(math.ceil(4096/per_long),dtype=np.uint64)
                for k in range(per_long):
                    section=indices[k::per_long]
                    packed[:len(section)] |= section << np.uint64(k*bits)
                regions.append(nbt.Compound({
                    "X":nbt.Int(rx),"Y":nbt.Int(ry),"Z":nbt.Int(rz),
                    "BlockStates":nbt.Compound({"palette":nbt.List[nbt.Compound](palette),"data":nbt.LongArray(packed.view(np.int64))})
                }))
    header=serialize(nbt.Compound({
        "ThumbnailYaw":nbt.Float(0),"ThumbnailPitch":nbt.Float(45),
        "ContainsAir":nbt.Byte(0),"LockedThumbnail":nbt.Byte(0),
        "Version":nbt.Long(1),"Author":nbt.String(""),"Name":nbt.String(source.stem),
        "Tags":nbt.List[nbt.String](["tree","les_echos_du_monde"]),
        "BlockCount":nbt.Int(int(np.count_nonzero(codes)))
    }))
    png=thumbnail(codes,states)
    payload=gzip.compress(serialize(nbt.Compound({
        "DataVersion":nbt.Int(DATA_VERSION),"BlockRegion":nbt.List[nbt.Compound](regions),
        "BlockEntities":nbt.List[nbt.Compound]([])
    })),mtime=0)
    result=struct.pack(">I",MAGIC)
    for item in (header,png,payload): result+=struct.pack(">i",len(item))+item
    path.write_bytes(result)


def verify_blueprint(path,codes,states):
    stream=io.BytesIO(path.read_bytes())
    if struct.unpack(">I",stream.read(4))[0]!=MAGIC:raise ValueError("Invalid BP signature")
    parts=[]
    for _ in range(3):
        count=struct.unpack(">i",stream.read(4))[0];data=stream.read(count)
        if len(data)!=count:raise ValueError("Truncated BP section")
        parts.append(data)
    if stream.read():raise ValueError("Trailing data")
    header=nbt.File.parse(io.BytesIO(parts[0]))
    Image.open(io.BytesIO(parts[1])).verify()
    root=nbt.File.parse(io.BytesIO(gzip.decompress(parts[2])))
    height,length,width=codes.shape
    reverse={state:code for code,state in states.items() if code!=0}
    reverse["minecraft:structure_void"]=0
    restored=np.zeros_like(codes)
    for region in root["BlockRegion"]:
        x,y,z=(int(region[k])*16 for k in ("X","Y","Z"))
        blockstates=region["BlockStates"]
        palette=[state_string(t) for t in blockstates["palette"]]
        bits=max(4,(len(palette)-1).bit_length());per_long=64//bits;mask=(1<<bits)-1
        packed=np.asarray(blockstates["data"],dtype=np.int64).view(np.uint64)
        positions=np.arange(4096)
        indices=((packed[positions//per_long]>>(positions%per_long*bits).astype(np.uint64))&np.uint64(mask)).astype(np.int64)
        decoded=np.array([reverse[s] for s in palette],dtype=np.int64)[indices].reshape(16,16,16)
        dy,dz,dx=min(16,height-y),min(16,length-z),min(16,width-x)
        restored[y:y+dy,z:z+dz,x:x+dx]=decoded[:dy,:dz,:dx]
    # Several legacy metadata values describe the same modern block state.
    lookup={code:state for code,state in states.items()}
    for original,new in zip(codes.reshape(-1),restored.reshape(-1)):
        if lookup[int(original)]!=lookup[int(new)]:raise ValueError("Block state mismatch after BP reread")
    if int(header["BlockCount"])!=int(np.count_nonzero(codes)):raise ValueError("Block count mismatch")
    return len(root["BlockRegion"])


def main():
    OUTPUT.mkdir(parents=True,exist_ok=True)
    mapping=json.loads((BASE/"tools/worldedit_legacy.json").read_text(encoding="utf-8"))["blocks"]
    sources=sorted(PROJECT.rglob("*.schematic"))
    if not sources:raise ValueError("No .schematic files")
    rows=[];failed=[];used=set()
    for i,source in enumerate(sources,1):
        try:
            before=hashlib.sha256(source.read_bytes()).hexdigest()
            target=OUTPUT/(source.stem+".bp")
            if target.name in used:raise ValueError("Duplicate filename; explicit resolution needed")
            used.add(target.name)
            codes,states=read_source(source,mapping)
            write_blueprint(target,source,codes,states)
            regions=verify_blueprint(target,codes,states)
            if hashlib.sha256(source.read_bytes()).hexdigest()!=before:raise ValueError("Source file changed")
            h,l,w=codes.shape
            rows.append({"source":str(source),"blueprint":str(target),"X":w,"Y":h,"Z":l,
                         "blocks":int(np.count_nonzero(codes)),"regions":regions,"source_sha256":before,
                         "blueprint_sha256":hashlib.sha256(target.read_bytes()).hexdigest(),"status":"verified"})
        except Exception as exc:
            failed.append({"source":str(source),"error":str(exc)})
            print(f"FAIL {source.name}: {exc}",flush=True)
        if i%25==0 or i==len(sources):print(f"{i}/{len(sources)}: {len(rows)} verified, {len(failed)} failures",flush=True)
    report={"source_count":len(sources),"converted":len(rows),"failed":failed,"files":rows,
            "format_reference":"https://github.com/PiTheGuy/SchemConvert/blob/master/src/main/java/pitheguy/schemconvert/converter/formats/AxiomSchematicFormat.java",
            "mapping_source":"https://github.com/EngineHub/WorldEdit/blob/master/worldedit-core/src/main/resources/com/sk89q/worldedit/world/registry/legacy.json",
            "data_version":DATA_VERSION,"air_policy":"Air cells become structure_void: transparent paste.",
            "thumbnail":"Approximate isometric voxel previews, not game screenshots.",
            "minecraft_test":"Not performed; complete binary and block state reread verification performed."}
    (BASE/"rapport_conversion.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    if rows:
        with (BASE/"inventaire.csv").open("w",encoding="utf-8-sig",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=";");writer.writeheader();writer.writerows(rows)
    if failed:raise SystemExit(1)


if __name__=="__main__":main()
