-- Les Echos du Monde : Script Brush Axiom / Minecraft 1.21.1.
-- Copier tout ce fichier dans Tools > Script Brush > Tool Options.
-- Les expressions $...$ sont les reglages documentes d'Axiom.
-- Coordonnees en blocs DU MONDE, sans deplacement de la plateforme.
-- Voir AXIOM_VEGETATION_MODE_EMPLOI.md pour les emplacements reserves.

local seed = $int(Graine,101,1,999999)$
local plantChance = $float(Flore pourcent,20,0,80)$ / 100
local flowerShare = $float(Fleurs pourcent de la flore,25,0,100)$ / 100
local treesEnabled = $boolean(Arbres,true)$
local treeChance = $float(Arbres pourcent,0.25,0,3)$ / 100
local bushesEnabled = $boolean(Buissons,true)$
local bushChance = $float(Buissons pourcent,0.6,0,5)$ / 100
local heightMin = $int(Hauteur tronc minimum,5,4,9)$
local heightMax = $int(Hauteur tronc maximum,7,4,10)$
local originX = $int(Origine plateforme X,-235,-30000000,30000000)$
local originZ = $int(Origine plateforme Z,-250,-30000000,30000000)$
local buildingMargin = $int(Marge batiments,4,0,16)$
local spawnRadius = $int(Rayon libre arrivee,5,2,16)$

local function air(id)
    return id == blocks.air or id == blocks.cave_air or id == blocks.void_air
end

-- Chaque passage travaille depuis un bloc de gazon expose.
-- Les chemins, l'eau et les plantes existantes ne sont pas remplaces.
if getBlock(x, y, z) ~= blocks.grass_block then return end
if not air(getBlock(x, y + 1, z)) then return end
if getHighestBlockYAt(x, z) ~= y then return end

local SPAWN = { x = 7, y = -3, z = 1 }
-- Chunk (0, -4) et ses huit voisins : limites inclusives X/Z.
local GARRIK = { minX = -16, maxX = 31, minZ = -80, maxZ = -33 }

-- Rectangles LOCAUX du NBT plateforme__4, releves dans rapport_verification.json.
-- L'origine provisoire transforme ces rectangles en coordonnees du monde.
-- Ils restent reserves apres le retrait de leurs marqueurs colores.
local BUILDINGS = {
    { name = "Jaune",   minX = 229, maxX = 255, minZ = 330, maxZ = 375 },
    { name = "Bleu",    minX = 234, maxX = 262, minZ = 304, maxZ = 324 },
    { name = "Magenta", minX = 305, maxX = 325, minZ = 290, maxZ = 310 },
    { name = "Noir",    minX = 360, maxX = 375, minZ = 312, maxZ = 323 },
    { name = "Cyan",    minX = 275, maxX = 287, minZ = 352, maxZ = 364 },
    { name = "Rouge",   minX = 306, maxX = 327, minZ = 350, maxZ = 378 },
}

local function inSpawn(px, pz)
    return math.abs(px - SPAWN.x) <= spawnRadius
        and math.abs(pz - SPAWN.z) <= spawnRadius
end

local function inGarrik(px, pz)
    return px >= GARRIK.minX and px <= GARRIK.maxX
        and pz >= GARRIK.minZ and pz <= GARRIK.maxZ
end

local function inBuilding(px, pz)
    local lx, lz = px - originX, pz - originZ
    for _, box in ipairs(BUILDINGS) do
        if lx >= box.minX - buildingMargin and lx <= box.maxX + buildingMargin
            and lz >= box.minZ - buildingMargin and lz <= box.maxZ + buildingMargin then
            return true
        end
    end
    return false
end

local function reserved(px, pz, woody)
    return inSpawn(px, pz) or inBuilding(px, pz) or (woody and inGarrik(px, pz))
end

if reserved(x, z, false) then return end

-- Hasard reproductible par coordonnees : les passages repetes n'augmentent
-- pas les probabilites. Changer la graine change la repartition.
local function randomAt(px, pz, salt)
    local n = math.sin(px * 12.9898 + pz * 78.233 + seed * 0.137 + salt * 37.719)
        * 43758.5453
    return n - math.floor(n)
end

local TERRAIN = {
    [blocks.grass_block] = true,
    [blocks.dirt] = true,
    [blocks.rooted_dirt] = true,
    [blocks.podzol] = true,
    [blocks.moss_block] = true,
    [blocks.stone] = true,
}

local LOW_PLANTS = {
    [blocks.short_grass] = true, [blocks.tall_grass] = true,
    [blocks.fern] = true, [blocks.large_fern] = true,
    [blocks.dandelion] = true, [blocks.poppy] = true,
    [blocks.cornflower] = true, [blocks.oxeye_daisy] = true,
    [blocks.allium] = true, [blocks.blue_orchid] = true,
    [blocks.azure_bluet] = true, [blocks.lily_of_the_valley] = true,
    [blocks.red_tulip] = true, [blocks.orange_tulip] = true,
    [blocks.white_tulip] = true, [blocks.pink_tulip] = true,
    [blocks.rose_bush] = true, [blocks.peony] = true,
    [blocks.lilac] = true, [blocks.sunflower] = true,
    [blocks.torchflower] = true, [blocks.pitcher_plant] = true,
}

local MARKER = {}
local COLORS = {
    "white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray",
    "light_gray", "cyan", "purple", "blue", "brown", "green", "red", "black",
}
for _, color in ipairs(COLORS) do
    MARKER[blocks[color .. "_concrete"]] = true
    MARKER[blocks[color .. "_concrete_powder"]] = true
    MARKER[blocks[color .. "_wool"]] = true
    MARKER[blocks[color .. "_terracotta"]] = true
end

-- Cette bordure reste libre a cote des chemins et des constructions.
-- Les sols artificiels, dont dirt_path et coarse_dirt, ne sont pas du terrain
-- autorise pour ce controle. Aucun dirt_path n'est produit par le script.
local function clearNaturalArea(radius, woody)
    for dx = -radius, radius do
        for dz = -radius, radius do
            local px, pz = x + dx, z + dz
            if reserved(px, pz, woody) then return false end
            local topY = getHighestBlockYAt(px, pz)
            local top = getBlock(px, topY, pz)
            if not TERRAIN[top] and not LOW_PLANTS[top] then return false end
            if math.abs(topY - y) > 3 then return false end
            -- Marqueurs/constructions a proximite du niveau de plantation.
            for dy = -1, 3 do
                local id = getBlock(px, y + dy, pz)
                if MARKER[id] or id == blocks.structure_block then return false end
                if dy >= 1 and not air(id) and not LOW_PLANTS[id] then return false end
            end
        end
    end
    return true
end

local function newPlan()
    return { positions = {}, occupied = {} }
end

local function addToPlan(plan, px, py, pz, state)
    local key = px .. ":" .. py .. ":" .. pz
    if not plan.occupied[key] then
        plan.occupied[key] = true
        plan.positions[#plan.positions + 1] = { x = px, y = py, z = pz, state = state }
    end
end

local function applyPlan(plan, woody)
    -- Lire TOUS les emplacements avant d'ecrire le premier bloc.
    for _, pos in ipairs(plan.positions) do
        if reserved(pos.x, pos.z, woody) then return false end
        if pos.y < -64 or pos.y > 319 then return false end
        if not air(getBlock(pos.x, pos.y, pos.z)) then return false end
    end
    for _, pos in ipairs(plan.positions) do
        setBlock(pos.x, pos.y, pos.z, pos.state)
    end
    return true
end

local function treePlan()
    local low = math.min(heightMin, heightMax)
    local high = math.max(heightMin, heightMax)
    local height = low + math.floor(randomAt(x, z, 23) * (high - low + 1))
    local species = randomAt(x, z, 29)
    local log, leaf
    if species < 0.65 then
        log, leaf = blocks.oak_log, blocks.oak_leaves
    elseif species < 0.90 then
        log, leaf = blocks.birch_log, blocks.birch_leaves
    else
        log, leaf = blocks.spruce_log, blocks.spruce_leaves
    end
    log = withBlockProperty(log, "axis=y")
    leaf = withBlockProperty(leaf, "persistent=true")
    local plan = newPlan()
    -- Les troncs sont prioritaires sur les feuilles aux memes positions.
    for dy = 1, height do
        addToPlan(plan, x, y + dy, z, log)
    end
    if species >= 0.90 then
        -- Sapin : etages de feuilles et pointe, tronc continu.
        for dy = 2, height do
            local radius = 1
            if dy <= height - 2 and dy % 2 == 0 then radius = 2 end
            for dx = -radius, radius do
                for dz = -radius, radius do
                    if math.abs(dx) + math.abs(dz) <= radius + 1 then
                        addToPlan(plan, x + dx, y + dy, z + dz, leaf)
                    end
                end
            end
        end
        addToPlan(plan, x, y + height + 1, z, leaf)
    else
        -- Chene/bouleau : couronne compacte avec des coins arrondis.
        for dy = height - 2, height + 1 do
            local radius = 2
            if dy == height + 1 then radius = 1 end
            for dx = -radius, radius do
                for dz = -radius, radius do
                    if math.abs(dx) + math.abs(dz) <= radius + 1 then
                        addToPlan(plan, x + dx, y + dy, z + dz, leaf)
                    end
                end
            end
        end
    end
    return plan
end

-- Les arbres sont des formes construites par ce script, en blocs vanilla.
-- Le controle du sol couvre la couronne et une bordure supplementaire.
if treesEnabled and randomAt(x, z, 11) < treeChance then
    if clearNaturalArea(3, true) and applyPlan(treePlan(), true) then return end
end

if bushesEnabled and randomAt(x, z, 41) < bushChance then
    if clearNaturalArea(2, true) then
        local plan = newPlan()
        local flowering = randomAt(x, z, 43) < 0.25
        local bush = flowering and blocks.flowering_azalea or blocks.azalea
        addToPlan(plan, x, y + 1, z, bush)
        local dx = randomAt(x, z, 47) < 0.5 and -1 or 1
        local sideY = getHighestBlockYAt(x + dx, z)
        if getBlock(x + dx, sideY, z) == blocks.grass_block
            and math.abs(sideY - y) <= 1 then
            addToPlan(plan, x + dx, sideY + 1, z, blocks.azalea)
        end
        if applyPlan(plan, true) then return end
    end
end

if randomAt(x, z, 59) >= plantChance then return end
if not clearNaturalArea(1, false) then return end

local plant
if randomAt(x, z, 61) < flowerShare then
    local flowers = {
        blocks.dandelion, blocks.poppy, blocks.cornflower,
        blocks.oxeye_daisy, blocks.allium, blocks.azure_bluet,
        blocks.white_tulip, blocks.pink_tulip,
    }
    plant = flowers[1 + math.floor(randomAt(x, z, 67) * #flowers)]
else
    plant = randomAt(x, z, 71) < 0.20 and blocks.fern or blocks.short_grass
end

local plan = newPlan()
addToPlan(plan, x, y + 1, z, plant)
applyPlan(plan, false)
