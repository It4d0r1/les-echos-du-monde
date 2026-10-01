# Tile 581/706 at world chunk (-9, -12), expanding outward from the arrival chunk.
execute in les_echos_du_monde:prologue unless data storage les_echos_du_monde:state platform_tile_forced if loaded -144 -56 -192 run data modify storage les_echos_du_monde:state platform_tile_loaded set value 1b
execute in les_echos_du_monde:prologue unless data storage les_echos_du_monde:state platform_tile_forced unless data storage les_echos_du_monde:state platform_tile_loaded run forceload add -144 -192 -129 -177
execute unless data storage les_echos_du_monde:state platform_tile_forced unless data storage les_echos_du_monde:state platform_tile_loaded run data modify storage les_echos_du_monde:state platform_tile_owned set value 1b
execute unless data storage les_echos_du_monde:state platform_tile_forced run scoreboard players set #platform_wait edm_internal 0
execute unless data storage les_echos_du_monde:state platform_tile_forced run data modify storage les_echos_du_monde:state platform_tile_forced set value 1b
data remove storage les_echos_du_monde:state platform_tile_loaded
execute in les_echos_du_monde:prologue if loaded -144 -56 -192 if loaded -129 -56 -192 if loaded -144 -56 -177 if loaded -129 -56 -177 run data modify storage les_echos_du_monde:state platform_tile_loaded set value 1b
scoreboard players set #platform_place edm_internal 0
execute in les_echos_du_monde:prologue if data storage les_echos_du_monde:state platform_tile_loaded store success score #platform_place edm_internal run place template les_echos_du_monde:prologue_chunks/chunk_0580 -144 -56 -192
execute in les_echos_du_monde:prologue if score #platform_place edm_internal matches 1 if data storage les_echos_du_monde:state {platform_tile_owned:1b} run forceload remove -144 -192
execute if score #platform_place edm_internal matches 1 run data remove storage les_echos_du_monde:state platform_tile_owned
execute if score #platform_place edm_internal matches 1 run data remove storage les_echos_du_monde:state platform_tile_forced
execute if score #platform_place edm_internal matches 1 run scoreboard players set #platform_wait edm_internal 0
execute in les_echos_du_monde:prologue if score #platform_place edm_internal matches 1 run schedule function les_echos_du_monde:world/platform_chunks/chunk_0581 1t replace
execute if data storage les_echos_du_monde:state platform_tile_loaded unless score #platform_place edm_internal matches 1 run data modify storage les_echos_du_monde:state platform_error set value 1b
execute in les_echos_du_monde:prologue if data storage les_echos_du_monde:state platform_tile_loaded unless score #platform_place edm_internal matches 1 if data storage les_echos_du_monde:state {platform_tile_owned:1b} run forceload remove -144 -192
execute if data storage les_echos_du_monde:state platform_tile_loaded unless score #platform_place edm_internal matches 1 run data remove storage les_echos_du_monde:state platform_tile_owned
execute if data storage les_echos_du_monde:state platform_tile_loaded unless score #platform_place edm_internal matches 1 run data remove storage les_echos_du_monde:state platform_tile_forced
execute if data storage les_echos_du_monde:state platform_tile_loaded unless score #platform_place edm_internal matches 1 run data remove storage les_echos_du_monde:state platform_building
execute unless data storage les_echos_du_monde:state platform_tile_loaded unless data storage les_echos_du_monde:state platform_error unless score #platform_place edm_internal matches 1 run scoreboard players add #platform_wait edm_internal 1
execute unless data storage les_echos_du_monde:state platform_tile_loaded unless data storage les_echos_du_monde:state platform_error unless score #platform_place edm_internal matches 1 if score #platform_wait edm_internal matches 200.. run data modify storage les_echos_du_monde:state platform_error set value 1b
execute in les_echos_du_monde:prologue unless data storage les_echos_du_monde:state platform_tile_loaded unless data storage les_echos_du_monde:state platform_error unless score #platform_place edm_internal matches 1 if score #platform_wait edm_internal matches ..199 run schedule function les_echos_du_monde:world/platform_chunks/chunk_0580 1t replace
execute in les_echos_du_monde:prologue unless data storage les_echos_du_monde:state platform_tile_loaded if score #platform_wait edm_internal matches 200.. if data storage les_echos_du_monde:state {platform_tile_owned:1b} run forceload remove -144 -192
execute unless data storage les_echos_du_monde:state platform_tile_loaded if score #platform_wait edm_internal matches 200.. run data remove storage les_echos_du_monde:state platform_tile_owned
execute unless data storage les_echos_du_monde:state platform_tile_loaded if score #platform_wait edm_internal matches 200.. run data remove storage les_echos_du_monde:state platform_tile_forced
execute unless data storage les_echos_du_monde:state platform_tile_loaded if score #platform_wait edm_internal matches 200.. run data remove storage les_echos_du_monde:state platform_building
execute if score #platform_place edm_internal matches 1 run data remove storage les_echos_du_monde:state platform_tile_loaded
