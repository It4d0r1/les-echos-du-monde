# Tile 256/706 at world chunk (4, -8), expanding outward from the arrival chunk.
execute in les_echos_du_monde:prologue unless data storage les_echos_du_monde:state platform_tile_forced if loaded 64 -56 -128 run data modify storage les_echos_du_monde:state platform_tile_loaded set value 1b
execute in les_echos_du_monde:prologue unless data storage les_echos_du_monde:state platform_tile_forced unless data storage les_echos_du_monde:state platform_tile_loaded run forceload add 64 -128 79 -113
execute unless data storage les_echos_du_monde:state platform_tile_forced unless data storage les_echos_du_monde:state platform_tile_loaded run data modify storage les_echos_du_monde:state platform_tile_owned set value 1b
execute unless data storage les_echos_du_monde:state platform_tile_forced run scoreboard players set #platform_wait edm_internal 0
execute unless data storage les_echos_du_monde:state platform_tile_forced run data modify storage les_echos_du_monde:state platform_tile_forced set value 1b
data remove storage les_echos_du_monde:state platform_tile_loaded
execute in les_echos_du_monde:prologue if loaded 64 -56 -128 if loaded 79 -56 -128 if loaded 64 -56 -113 if loaded 79 -56 -113 run data modify storage les_echos_du_monde:state platform_tile_loaded set value 1b
scoreboard players set #platform_place edm_internal 0
execute in les_echos_du_monde:prologue if data storage les_echos_du_monde:state platform_tile_loaded store success score #platform_place edm_internal run place template les_echos_du_monde:prologue_chunks/chunk_0255 64 -56 -128
execute in les_echos_du_monde:prologue if score #platform_place edm_internal matches 1 if data storage les_echos_du_monde:state {platform_tile_owned:1b} run forceload remove 64 -128
execute if score #platform_place edm_internal matches 1 run data remove storage les_echos_du_monde:state platform_tile_owned
execute if score #platform_place edm_internal matches 1 run data remove storage les_echos_du_monde:state platform_tile_forced
execute if score #platform_place edm_internal matches 1 run scoreboard players set #platform_wait edm_internal 0
execute in les_echos_du_monde:prologue if score #platform_place edm_internal matches 1 run schedule function les_echos_du_monde:world/platform_chunks/chunk_0256 1t replace
execute if data storage les_echos_du_monde:state platform_tile_loaded unless score #platform_place edm_internal matches 1 run data modify storage les_echos_du_monde:state platform_error set value 1b
execute in les_echos_du_monde:prologue if data storage les_echos_du_monde:state platform_tile_loaded unless score #platform_place edm_internal matches 1 if data storage les_echos_du_monde:state {platform_tile_owned:1b} run forceload remove 64 -128
execute if data storage les_echos_du_monde:state platform_tile_loaded unless score #platform_place edm_internal matches 1 run data remove storage les_echos_du_monde:state platform_tile_owned
execute if data storage les_echos_du_monde:state platform_tile_loaded unless score #platform_place edm_internal matches 1 run data remove storage les_echos_du_monde:state platform_tile_forced
execute if data storage les_echos_du_monde:state platform_tile_loaded unless score #platform_place edm_internal matches 1 run data remove storage les_echos_du_monde:state platform_building
execute unless data storage les_echos_du_monde:state platform_tile_loaded unless data storage les_echos_du_monde:state platform_error unless score #platform_place edm_internal matches 1 run scoreboard players add #platform_wait edm_internal 1
execute unless data storage les_echos_du_monde:state platform_tile_loaded unless data storage les_echos_du_monde:state platform_error unless score #platform_place edm_internal matches 1 if score #platform_wait edm_internal matches 200.. run data modify storage les_echos_du_monde:state platform_error set value 1b
execute in les_echos_du_monde:prologue unless data storage les_echos_du_monde:state platform_tile_loaded unless data storage les_echos_du_monde:state platform_error unless score #platform_place edm_internal matches 1 if score #platform_wait edm_internal matches ..199 run schedule function les_echos_du_monde:world/platform_chunks/chunk_0255 1t replace
execute in les_echos_du_monde:prologue unless data storage les_echos_du_monde:state platform_tile_loaded if score #platform_wait edm_internal matches 200.. if data storage les_echos_du_monde:state {platform_tile_owned:1b} run forceload remove 64 -128
execute unless data storage les_echos_du_monde:state platform_tile_loaded if score #platform_wait edm_internal matches 200.. run data remove storage les_echos_du_monde:state platform_tile_owned
execute unless data storage les_echos_du_monde:state platform_tile_loaded if score #platform_wait edm_internal matches 200.. run data remove storage les_echos_du_monde:state platform_tile_forced
execute unless data storage les_echos_du_monde:state platform_tile_loaded if score #platform_wait edm_internal matches 200.. run data remove storage les_echos_du_monde:state platform_building
execute if score #platform_place edm_internal matches 1 run data remove storage les_echos_du_monde:state platform_tile_loaded
