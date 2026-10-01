# Morceau 173/933, chunk monde [0, 7].
execute if data storage les_echos_du_monde:state {prologue_automation_paused:1b} run return 0
execute unless data storage les_echos_du_monde:state platform_building run return 0
execute unless data storage les_echos_du_monde:state {platform_layout:"vegetation_20261001"} run return 0
execute in les_echos_du_monde:prologue unless data storage les_echos_du_monde:state platform_tile_forced if loaded 0 -30 112 run data modify storage les_echos_du_monde:state platform_tile_loaded set value 1b
execute unless data storage les_echos_du_monde:state platform_tile_forced run scoreboard players set #platform_forceload_added edm_internal 0
execute in les_echos_du_monde:prologue unless data storage les_echos_du_monde:state platform_tile_forced unless data storage les_echos_du_monde:state platform_tile_loaded store success score #platform_forceload_added edm_internal run forceload add 0 112
execute unless data storage les_echos_du_monde:state platform_tile_forced if score #platform_forceload_added edm_internal matches 1 run data modify storage les_echos_du_monde:state platform_tile_owned set value 1b
execute unless data storage les_echos_du_monde:state platform_tile_forced run scoreboard players set #platform_wait edm_internal 0
data modify storage les_echos_du_monde:state platform_tile_forced set value 1b
data remove storage les_echos_du_monde:state platform_tile_loaded
execute in les_echos_du_monde:prologue if loaded 0 -30 112 if loaded 15 -30 127 run data modify storage les_echos_du_monde:state platform_tile_loaded set value 1b
scoreboard players set #platform_place edm_internal 0
execute in les_echos_du_monde:prologue if data storage les_echos_du_monde:state platform_tile_loaded store success score #platform_place edm_internal run place template les_echos_du_monde:prologue_vegetation_chunks/chunk_0172 0 -30 112
execute in les_echos_du_monde:prologue if score #platform_place edm_internal matches 1 if data storage les_echos_du_monde:state {platform_tile_owned:1b} run forceload remove 0 112
execute if score #platform_place edm_internal matches 1 run data remove storage les_echos_du_monde:state platform_tile_owned
execute if score #platform_place edm_internal matches 1 run data remove storage les_echos_du_monde:state platform_tile_forced
execute if score #platform_place edm_internal matches 1 run data remove storage les_echos_du_monde:state platform_tile_loaded
execute if score #platform_place edm_internal matches 1 run scoreboard players set #platform_progress edm_internal 173
execute if score #platform_place edm_internal matches 1 run schedule function les_echos_du_monde:world/vegetation_chunks/chunk_0173 1t replace
execute if score #platform_place edm_internal matches 1 run return 1
execute if data storage les_echos_du_monde:state platform_tile_loaded run data modify storage les_echos_du_monde:state platform_error_reason set value "placement_refused"
execute if data storage les_echos_du_monde:state platform_tile_loaded run data modify storage les_echos_du_monde:state platform_error set value 1b
scoreboard players add #platform_wait edm_internal 1
execute if score #platform_wait edm_internal matches 200.. unless data storage les_echos_du_monde:state platform_tile_loaded run data modify storage les_echos_du_monde:state platform_error_reason set value "chunk_load_timeout"
execute if score #platform_wait edm_internal matches 200.. run data modify storage les_echos_du_monde:state platform_error set value 1b
execute if data storage les_echos_du_monde:state platform_error run data modify storage les_echos_du_monde:state platform_error_tile set value 172
execute in les_echos_du_monde:prologue if data storage les_echos_du_monde:state platform_error if data storage les_echos_du_monde:state {platform_tile_owned:1b} run forceload remove 0 112
execute if data storage les_echos_du_monde:state platform_error run data remove storage les_echos_du_monde:state platform_tile_owned
execute if data storage les_echos_du_monde:state platform_error run data remove storage les_echos_du_monde:state platform_tile_forced
execute if data storage les_echos_du_monde:state platform_error run data remove storage les_echos_du_monde:state platform_tile_loaded
execute if data storage les_echos_du_monde:state platform_error run data remove storage les_echos_du_monde:state platform_building
execute unless data storage les_echos_du_monde:state platform_error run schedule function les_echos_du_monde:world/vegetation_chunks/chunk_0172 1t replace
