"""Build the instance CraftScript directly from the measured exterior CSV."""
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / '06_RESSOURCES/Images/Maison garrike/Plan exterieur coherent v2'
INSTANCE = Path('C:/Users/Bastien/curseforge/minecraft/Instances/Pixelmon Les Échos du Monde')
TARGET = INSTANCE / 'config/worldedit/craftscripts/Maison_Garrik.js'

with (PLAN / 'Modele_exterieur_v2.csv').open(encoding='utf-8-sig', newline='') as f:
    rows = list(csv.DictReader(f, delimiter=';'))
cells = [(int(r['X']), int(r['Y']), int(r['Z']), r['Code'], r['Montee_escalier']) for r in rows]
occupied = {(x,y,z):code for x,y,z,code,direction in cells}

directions = {'X+':'west','X-':'east','Z+':'south','Z-':'north'}
records=[]
for x,y,z,code,direction in cells:
    axis='y'
    if code=='B':
        if (x,y-1,z) in occupied or (x,y+1,z) in occupied: axis='y'
        elif (x-1,y,z) in occupied or (x+1,y,z) in occupied: axis='x'
        elif (x,y,z-1) in occupied or (x,y,z+1) in occupied: axis='z'
    records.append(f'    [{x},{y},{z},"{code}","{directions.get(direction, "")}","{axis}"]')

script='''/*
 * Maison de Garrik — WorldEdit 7.3.8 / Minecraft 1.21.1 NeoForge
 * Données tirées du modèle extérieur cohérent v2 (CSV du plan).
 *
 * Origine : place-toi sur un terrain plat, un bloc au nord et à l'est
 * du coin gauche de la façade. La façade regarde au nord (-Z).
 * Le bloc sous tes pieds reste intact. La base du bâtiment commence
 * dans la première couche d'air au-dessus du terrain.
 *
 * X du plan augmente vers la droite de la façade ; Z va vers l'arrière.
 * Hauteurs du plan : murs 10, faîtage 19, cheminées 23.
 * Le script ne crée aucun plancher ni aménagement intérieur.
 * Chaque position occupée remplace le bloc qui s'y trouve. WorldEdit
 * conserve cette opération dans son historique : //undo annule la pose.
 */

var BlockVector3 = com.sk89q.worldedit.math.BlockVector3;
var player = context.getPlayer();
var ground = player.getBlockOn().toVector().toBlockPoint();
var originX = ground.getBlockX() - 1;
var originY = ground.getBlockY() + 1;
var originZ = ground.getBlockZ() + 1;

// Les cellules vides ne sont jamais modifiées.
var cells = [
'''+',\n'.join(records)+'''
];

function block(id) {
    return context.getBlock("minecraft:" + id);
}

var palette = {};
function remember(key, id) { palette[key] = block(id); }

// Préparer et valider les états avant toute modification du monde.
remember("stone", "stone_bricks");
remember("stone_mossy", "mossy_stone_bricks");
remember("stone_cracked", "cracked_stone_bricks");
remember("wood", "spruce_planks");
remember("beam_x", "spruce_log[axis=x]");
remember("beam_y", "spruce_log[axis=y]");
remember("beam_z", "spruce_log[axis=z]");
remember("enduit", "calcite");
remember("vitre", "glass_pane");
remember("faîtage", "spruce_planks");
remember("cheminee", "stone_bricks");
remember("vegetation", "oak_leaves[distance=1,persistent=true]");
remember("banniere", "blue_banner[rotation=8]");
remember("lanterne", "lantern[hanging=false]");
remember("support", "spruce_fence");
remember("jardiniere", "spruce_slab[type=bottom,waterlogged=false]");
remember("perron_stone", "stone_brick_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]");
remember("door_left_lower", "spruce_door[facing=north,half=lower,hinge=left,open=false,powered=false]");
remember("door_left_upper", "spruce_door[facing=north,half=upper,hinge=left,open=false,powered=false]");
remember("door_right_lower", "spruce_door[facing=north,half=lower,hinge=right,open=false,powered=false]");
remember("door_right_upper", "spruce_door[facing=north,half=upper,hinge=right,open=false,powered=false]");
var stairDirections = ["north", "south", "east", "west"];
for (var i = 0; i < stairDirections.length; i++) {
    var facing = stairDirections[i];
    remember("roof_" + facing, "spruce_stairs[facing=" + facing + ",half=bottom,shape=straight,waterlogged=false]");
    remember("step_" + facing, "stone_brick_stairs[facing=" + facing + ",half=bottom,shape=straight,waterlogged=false]");
}

function facadeB(x, y, z) {
    // Small deterministic stone variation keeps the foundation natural.
    var n = Math.abs((x * 31 + y * 17 + z * 13) % 11);
    if (n === 0) return "stone_mossy";
    if (n === 3) return "stone_cracked";
    return "stone";
}

var session = context.remember();
var placed = 0;
function put(x, y, z, state) {
    session.setBlock(BlockVector3.at(originX + x, originY + y, originZ + z), state);
    placed++;
}

for (var n = 0; n < cells.length; n++) {
    var c = cells[n];
    var x = c[0], y = c[1], z = c[2], code = c[3], facing = c[4], axis = c[5];
    var state;

    if (code === "S") state = palette[facadeB(x, y, z)];
    else if (code === "B") state = palette["beam_" + axis];
    else if (code === "P") state = palette.wood;
    else if (code === "E") state = palette.enduit;
    else if (code === "G") state = palette.vitre;
    else if (code === "D") {
        var leftDoor = x === 6;
        state = palette["door_" + (leftDoor ? "left_" : "right_") + (y === 1 ? "lower" : "upper")];
    }
    else if (code === "R") state = palette["roof_" + facing];
    else if (code === "H") state = palette["faîtage"];
    else if (code === "C") state = palette.cheminee;
    else if (code === "L") state = palette.lanterne;
    else if (code === "V") state = palette.vegetation;
    else if (code === "N") {
        // One standing banner per three-cell drawing; the source has no custom NBT.
        if (y !== 7) continue;
        state = palette.banniere;
    }
    else if (code === "A") state = palette["step_" + facing];
    else throw new Error("Code de bloc inconnu dans le modèle : " + code);

    put(x, y, z, state);

    // Attach lanterns to their wall brackets, and support the flower boxes.
    if (code === "L") put(x, y - 1, z, palette.support);
    if (code === "N" && y === 7) put(x, y - 1, z, palette.support);
    if (code === "V" && y === 5 && z === -1) put(x, y - 1, z, palette.jardiniere);
}

player.print("Maison de Garrik posée : " + placed + " blocs. Annulation WorldEdit : //undo");
'''

TARGET.parent.mkdir(parents=True, exist_ok=True)
TARGET.write_text(script,encoding='utf-8')

guide='''SCRIPT WORLDEDIT — MAISON DE GARRIK

Instance détectée : Minecraft 1.21.1, NeoForge, WorldEdit 7.3.8.
Le CraftScript est installé dans le dossier craftscripts de cette instance.

UTILISATION
1. Dans le monde, repère un terrain plat et libre.
2. Place-toi sur le bloc au nord et à l’est du futur coin gauche de la façade. C’est-à-dire un bloc devant la façade et un bloc à gauche en la regardant depuis le nord. La façade sera tournée vers le nord.
3. Lance : /cs Maison_Garrik

L’origine est calculée depuis le bloc sous les pieds. Le script commence la maison un bloc à l’ouest, un bloc au sud et une couche au-dessus de ce bloc. Le sol où tu te tiens n’est pas remplacé. Le plan place le bâtiment en X=0..24 et Z=0..16, son toit déborde jusqu’à X=-1..25 et Z=-1..17. Le perron avance jusqu’à Z=-4. La structure monte jusqu’à Y=22 (23 blocs au-dessus du niveau d’origine).

La maison suit le modèle extérieur v2 ; la palette devient des blocs Minecraft vanilla : briques de pierre patinées, rondins et planches d’épicéa, calcite, vitres, escaliers, lanternes, feuillage et bannières bleues. Les bannières de l’image n’ayant pas de motif exportable depuis le modèle, WorldEdit crée des bannières bleues simples.

Le script remplace les blocs aux positions prévues. Fais la pose sur un site libre. Pour l’annuler, utilise immédiatement //undo avant toute autre opération WorldEdit. Aucun sol intérieur ni ameublement n’est ajouté.

Le fichier est construit depuis Modele_exterieur_v2.csv. Le script est un CraftScript WorldEdit JavaScript (commande /cs), et non un fichier datapack .mcfunction.
'''
(PLAN/'Utiliser_le_script_WorldEdit.txt').write_text(guide,encoding='utf-8')
print('Script créé :',TARGET)
print('Cellules du modèle :',len(cells),'; étapes et supports ajoutent des blocs de pose.')
