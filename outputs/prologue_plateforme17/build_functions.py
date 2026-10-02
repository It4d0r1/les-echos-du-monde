"""Build the bounded Minecraft 1.21.1 runtime for platform segment templates.

Only the supplied staging pack is modified. No live instance or save is opened.
Use: python build_functions.py --manifest segments_manifest.json --pack PACK
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


NS = "les_echos_du_monde"
BASE = f"{NS}:world/segments_v17"
STORAGE = f"{NS}:segments_v17"
LAYOUT = "segments_v17"
DIM = f"{NS}:prologue"
CTL, DONE, RETRY, TMP = "edm_seg_ctl", "edm_seg_done", "edm_seg_retry", "edm_seg_tmp"


def segment_rows(document):
    if isinstance(document, list):
        rows = document
    else:
        rows = document["segments"]
    out = []
    for index, raw in enumerate(rows):
        row = dict(raw)
        row["id"] = str(raw.get("id", raw.get("segment_id", "")))
        if not re.fullmatch(r"s_[mp]\d+_[mp]\d+", row["id"]):
            raise ValueError(f"Invalid segment ID: {row['id']!r}")
        row["sx"], row["sz"] = int(raw["sx"]), int(raw["sz"])
        row["x"] = int(raw.get("x", row["sx"] * 32))
        row["z"] = int(raw.get("z", row["sz"] * 32))
        row["y"] = int(raw.get("y", -26))
        if (row["x"], row["z"]) != (row["sx"] * 32, row["sz"] * 32):
            raise ValueError(f"Segment {row['id']} is not aligned on a 32-block cell")
        row["template"] = str(raw.get("template", f"{NS}:platform_segments_v17/{row['id']}"))
        if not re.fullmatch(r"[a-z0-9_.-]+:[a-z0-9_./-]+", row["template"]):
            raise ValueError(f"Invalid template: {row['template']!r}")
        row["number"] = index
        out.append(row)
    if len({row["id"] for row in out}) != len(out):
        raise ValueError("Duplicate segment ID")
    if len({(row["sx"], row["sz"]) for row in out}) != len(out):
        raise ValueError("Duplicate segment position")
    return out


def build(manifest: Path, pack: Path, radius: int):
    document = json.loads(manifest.read_text(encoding="utf-8-sig"))
    rows = segment_rows(document)
    lookup = {(r["sx"], r["sz"]): r for r in rows}
    spawn_rows = [lookup[(x, z)] for x in range(-1, 2) for z in range(-1, 2)]
    origin = document.get("origin_xyz", [-250, -26, -235]) if isinstance(document, dict) else [-250, -26, -235]
    size = document.get("source_size_xyz", [451, 89, 461]) if isinstance(document, dict) else [451, 89, 461]
    minimum_x, minimum_z = int(origin[0]), int(origin[2])
    maximum_x, maximum_z = minimum_x + int(size[0]) - 1, minimum_z + int(size[2]) - 1
    destination = pack / "data" / NS / "function" / "world" / "segments_v17"
    written = []

    def write(name, lines):
        path = destination / f"{name}.mcfunction"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        written.append(path)

    def fn(name):
        return f"{BASE}/{name}"

    def command_json(message, color="yellow"):
        return json.dumps({"text": message, "color": color}, ensure_ascii=False, separators=(",", ":"))

    # A shared operation slot prevents duplicate or parallel segment placement.
    write("initialize", [
        "# Only called when this runtime has never been initialized in this world.",
        f"data modify storage {STORAGE} runtime_initialized set value 1b",
        f'data modify storage {STORAGE} layout set value "{LAYOUT}"',
        "# Diagnostic metadata; these compiled values are not editable runtime settings.",
        f"data modify storage {STORAGE} generated_settings set value {{radius_segments:{radius},max_placements_per_two_ticks:1,timeout_ticks:100,max_failures_per_segment:3}}",
        f"data modify storage {STORAGE} spawn_ready set value 0b",
        f"scoreboard players set #enabled {CTL} 1",
        f"scoreboard players set #active {CTL} -1",
        f"scoreboard players set #wait {CTL} 0",
        f"scoreboard players set #completed {CTL} 0",
    ])
    write("setup", [
        "# Objective creation may report 'already exists' on reload; persistent scores are kept.",
        f"scoreboard objectives add {CTL} dummy",
        f"scoreboard objectives add {DONE} dummy",
        f"scoreboard objectives add {RETRY} dummy",
        f"scoreboard objectives add {TMP} dummy",
        f"execute unless data storage {STORAGE} runtime_initialized run function {fn('initialize')}",
        "# Reclaim only tickets this runtime previously added; no remove all command.",
        f"function {fn('cleanup_active')}",
        f"scoreboard players set #active {CTL} -1",
        f"scoreboard players set #clock {CTL} 0",
        f"scoreboard players set #budget {CTL} 0",
        f'execute unless data storage {NS}:state {{platform_layout:"{LAYOUT}"}} run function {fn("lock_layout")}',
        f'execute if data storage {NS}:state {{platform_layout:"{LAYOUT}"}} run data remove storage {STORAGE} locked_layout',
        f"execute if data storage {NS}:state {{prologue_automation_paused:1b}} run scoreboard players set #enabled {CTL} 0",
        f"function {fn('ready_spawn')}",
    ])
    write("lock_layout", [
        f"scoreboard players set #enabled {CTL} 0",
        f"data modify storage {STORAGE} locked_layout set value 1b",
        f"data modify storage {STORAGE} enabled set value 0b",
    ])
    write("tick", [
        f'execute unless data storage {NS}:state {{platform_layout:"{LAYOUT}"}} if score #active {CTL} matches 0.. run function {fn("pause_internal")}',
        f'execute unless data storage {NS}:state {{platform_layout:"{LAYOUT}"}} run return 0',
        f"execute if data storage {NS}:state {{prologue_automation_paused:1b}} run function {fn('pause_internal')}",
        f"execute unless score #enabled {CTL} matches 1 run return 0",
        f"scoreboard players add #clock {CTL} 1",
        f"execute unless score #clock {CTL} matches 2.. run return 0",
        f"scoreboard players set #clock {CTL} 0",
        f"function {fn('cycle')}",
    ])
    write("cycle", [
        f"scoreboard players set #budget {CTL} 1",
        f"execute if score #active {CTL} matches 0.. run function {fn('maintenance')}",
        f"execute if score #active {CTL} matches 0.. run scoreboard players set #budget {CTL} 0",
        f"function {fn('ready_spawn')}",
        f"execute if score #budget {CTL} matches 1 unless data storage {STORAGE} {{spawn_ready:1b}} if entity @a[tag=!edm_prologue_done] run function {fn('select_spawn')}",
        "# Random player order spreads the generation slot between multiple explorers.",
        f"execute as @a[sort=random] at @s if dimension {DIM} run function {fn('player')}",
        f"execute if score #active {CTL} matches 0.. if score #budget {CTL} matches 0 run function {fn('maintenance')}",
        f"function {fn('ready_spawn')}",
    ])
    # maintenance might otherwise poll an already active task twice during one cycle.
    # A per-cycle flag makes it run exactly once, whether selected now or earlier.
    cycle = (destination / "cycle.mcfunction").read_text(encoding="utf-8").splitlines()
    cycle.insert(1, f"scoreboard players set #polled {CTL} 0")
    write("cycle", cycle)
    write("maintenance", [
        f"execute if score #polled {CTL} matches 1 run return 0",
        f"scoreboard players set #polled {CTL} 1",
        *[f"execute if score #active {CTL} matches {r['number']} in {DIM} run function {fn('segment/' + r['id'] + '/poll')}" for r in rows],
    ])
    write("cleanup_active", [
        *[f"execute if score #active {CTL} matches {r['number']} in {DIM} run function {fn('segment/' + r['id'] + '/cleanup')}" for r in rows],
        f"scoreboard players set #active {CTL} -1",
        f"data remove storage {STORAGE} active",
    ])
    write("pause_internal", [
        f"execute if score #active {CTL} matches 0.. run function {fn('cleanup_active')}",
        f"scoreboard players set #enabled {CTL} 0",
        f"data modify storage {STORAGE} enabled set value 0b",
    ])
    write("disable", [
        f"function {fn('pause_internal')}",
        "tellraw @s " + command_json("Génération de plateforme désactivée. Segments terminés conservés."),
    ])
    write("enable", [
        f'execute unless data storage {NS}:state {{platform_layout:"{LAYOUT}"}} run tellraw @s ' + command_json("Ce monde utilise une autre plateforme. Créez un nouveau monde pour la version 17.", "red"),
        f'execute unless data storage {NS}:state {{platform_layout:"{LAYOUT}"}} run return 0',
        f"execute if data storage {NS}:state {{prologue_automation_paused:1b}} run tellraw @s " + command_json("L'automatisation globale du prologue est en pause. Réactivez-la d'abord.", "red"),
        f"execute if data storage {NS}:state {{prologue_automation_paused:1b}} run return 0",
        f"scoreboard players set #enabled {CTL} 1",
        f"data modify storage {STORAGE} enabled set value 1b",
        "tellraw @s " + command_json("Génération de plateforme activée.", "green"),
    ])
    write("ready_spawn", [
        f"scoreboard players set #ready {CTL} 1",
        *[f"execute unless score {r['id']} {DONE} matches 1 run scoreboard players set #ready {CTL} 0" for r in spawn_rows],
        f"execute if score #ready {CTL} matches 1 run data modify storage {STORAGE} spawn_ready set value 1b",
        f"execute unless score #ready {CTL} matches 1 run data modify storage {STORAGE} spawn_ready set value 0b",
    ])
    write("select_spawn", [
        "# Place arrival cell first, then the surrounding 3 x 3 cells.",
        *[f"execute if score #budget {CTL} matches 1 unless score {r['id']} {DONE} matches 1 unless score {r['id']} {RETRY} matches 3.. in {DIM} run function {fn('segment/' + r['id'] + '/start')}" for r in sorted(spawn_rows, key=lambda r: (r['sx'] ** 2 + r['sz'] ** 2, r['sx'], r['sz']))],
    ])
    write("player", [
        "# data get floors coordinates, including negatives; integer ranges avoid selector bounding-box overlap.",
        f"execute store result score #px {TMP} run data get entity @s Pos[0] 1",
        f"execute store result score #pz {TMP} run data get entity @s Pos[2] 1",
        f"scoreboard players set #safe {TMP} 0",
        *[f"execute if score #px {TMP} matches {sx * 32}..{sx * 32 + 31} run function {fn('dispatch/x_' + ('m' if sx < 0 else 'p') + str(abs(sx)).zfill(2))}" for sx in sorted({r['sx'] for r in rows})],
        "# Partial border cells contain empty padding outside the exported structure.",
        f"execute if score #px {TMP} matches ..{minimum_x - 1} run scoreboard players set #safe {TMP} 0",
        f"execute if score #px {TMP} matches {maximum_x + 1}.. run scoreboard players set #safe {TMP} 0",
        f"execute if score #pz {TMP} matches ..{minimum_z - 1} run scoreboard players set #safe {TMP} 0",
        f"execute if score #pz {TMP} matches {maximum_z + 1}.. run scoreboard players set #safe {TMP} 0",
        f"execute unless entity @s[gamemode=creative] unless entity @s[gamemode=spectator] unless score #safe {TMP} matches 1 if data storage {STORAGE} {{spawn_ready:1b}} run function {fn('transfer')}",
    ])
    write("transfer", [
        "# Fail-safe if flight or fast movement reaches terrain not yet placed.",
        f"execute unless data storage {STORAGE} {{spawn_ready:1b}} run return 0",
        f"function {NS}:player/teleport_to_prologue",
        "title @s actionbar " + command_json("Le terrain devant vous se prépare…"),
    ])
    for sx in sorted({r["sx"] for r in rows}):
        write("dispatch/x_" + ("m" if sx < 0 else "p") + str(abs(sx)).zfill(2), [
            f"execute if score #pz {TMP} matches {r['z']}..{r['z'] + 31} run function {fn('cell/' + r['id'])}"
            for r in rows if r["sx"] == sx
        ])
    for r in rows:
        nearby = [t for t in rows if max(abs(t["sx"] - r["sx"]), abs(t["sz"] - r["sz"])) <= radius]
        nearby.sort(key=lambda t: ((t["sx"] - r["sx"]) ** 2 + (t["sz"] - r["sz"]) ** 2, t["sx"], t["sz"]))
        write("cell/" + r["id"], [
            f"execute if score {r['id']} {DONE} matches 1 run scoreboard players set #safe {TMP} 1",
            *[f"execute if score #budget {CTL} matches 1 unless score {t['id']} {DONE} matches 1 unless score {t['id']} {RETRY} matches 3.. run function {fn('segment/' + t['id'] + '/start')}" for t in nearby],
        ])
        # Vanilla PlaceCommand checks pos + template.size (not size - 1).
        # Thus a 32 x 32 template needs a loaded 3 x 3 chunk rectangle.
        # Only 2 x 2 chunks receive structure blocks; the extra positive border is read-only.
        chunks = [(r["x"] + dx, r["z"] + dz) for dx in (0, 16, 32) for dz in (0, 16, 32)]
        start = [
            f"execute unless score #budget {CTL} matches 1 run return 0",
            f"execute if score #active {CTL} matches 0.. run return 0",
            f"scoreboard players set #budget {CTL} 0",
            f"scoreboard players set #active {CTL} {r['number']}",
            f"scoreboard players set #wait {CTL} 0",
            f'data modify storage {STORAGE} active set value "{r["id"]}"',
        ]
        for i, (x, z) in enumerate(chunks):
            start.extend([
                f"scoreboard players set #owned{i} {CTL} 0",
                f"scoreboard players set #forced{i} {CTL} 0",
                f"execute store success score #forced{i} {CTL} run forceload query {x} {z}",
                f"execute unless score #forced{i} {CTL} matches 1 store success score #owned{i} {CTL} run forceload add {x} {z}",
            ])
        write("segment/" + r["id"] + "/start", start)
        loaded = " ".join(f"if loaded {x} 0 {z}" for x, z in chunks)
        write("segment/" + r["id"] + "/poll", [
            f"scoreboard players add #wait {CTL} 2",
            f"execute {loaded} run function {fn('segment/' + r['id'] + '/place')}",
            f"execute if score #active {CTL} matches {r['number']} if score #wait {CTL} matches 100.. run function {fn('segment/' + r['id'] + '/fail')}",
        ])
        write("segment/" + r["id"] + "/place", [
            f"scoreboard players set #placed {CTL} 0",
            f"execute store success score #placed {CTL} run place template {r['template']} {r['x']} {r['y']} {r['z']}",
            f"execute if score #placed {CTL} matches 1 run scoreboard players set {r['id']} {DONE} 1",
            f"execute if score #placed {CTL} matches 1 run scoreboard players set {r['id']} {RETRY} 0",
            f"execute if score #placed {CTL} matches 1 run scoreboard players add #completed {CTL} 1",
            f"execute unless score #placed {CTL} matches 1 run function {fn('segment/' + r['id'] + '/fail')}",
            f"execute if score #placed {CTL} matches 1 run function {fn('segment/' + r['id'] + '/cleanup')}",
        ])
        write("segment/" + r["id"] + "/fail", [
            f"scoreboard players add {r['id']} {RETRY} 1",
            f'data modify storage {STORAGE} last_error.segment set value "{r["id"]}"',
            f"execute store result storage {STORAGE} last_error.failures int 1 run scoreboard players get {r['id']} {RETRY}",
            f"execute if score {r['id']} {RETRY} matches 3 run tellraw @a " + command_json(f"Plateforme : le segment {r['id']} a échoué 3 fois. Génération de ce segment suspendue ; consultez la documentation.", "red"),
            f"function {fn('segment/' + r['id'] + '/cleanup')}",
        ])
        cleanup = [
            *[f"execute if score #owned{i} {CTL} matches 1 run forceload remove {x} {z}" for i, (x, z) in enumerate(chunks)],
            *[f"scoreboard players set #owned{i} {CTL} 0" for i in range(len(chunks))],
            f"scoreboard players set #active {CTL} -1",
            f"data remove storage {STORAGE} active",
        ]
        write("segment/" + r["id"] + "/cleanup", cleanup)
    write("retry_errors", [
        "# Operator action: allow failed segments another 3 attempts; never reset done scores.",
        *[f"execute unless score {r['id']} {DONE} matches 1 run scoreboard players set {r['id']} {RETRY} 0" for r in rows],
        f"data remove storage {STORAGE} last_error",
        "tellraw @s " + command_json("Les segments en erreur peuvent être retentés. Les segments terminés sont conservés.", "green"),
    ])
    write("status", [
        f"data get storage {STORAGE}",
        f"scoreboard players get #completed {CTL}",
        f"scoreboard players get #enabled {CTL}",
        f"scoreboard players get #active {CTL}",
    ])
    info = {
        "manifest": str(manifest.resolve()),
        "pack": str(pack.resolve()),
        "segments": len(rows),
        "radius_segments": radius,
        "radius_chunks": radius * 2,
        "max_temporary_forceload_tickets": 9,
        "runtime_functions": len(set(written)),
        "arrival_segments": [r["id"] for r in spawn_rows],
        "layout": LAYOUT,
        "integration": {"load": fn("setup"), "tick": fn("tick"), "ready_storage": STORAGE, "ready_path": "spawn_ready"},
    }
    (manifest.parent / "runtime_manifest.json").write_text(json.dumps(info, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(info, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--pack", type=Path, required=True)
    parser.add_argument("--radius", type=int, default=2, help="Radius in 32-block segments (default: 2 = 4 chunks)")
    args = parser.parse_args()
    if not 1 <= args.radius <= 4:
        parser.error("radius must be between 1 and 4")
    build(args.manifest, args.pack, args.radius)


if __name__ == "__main__":
    main()
