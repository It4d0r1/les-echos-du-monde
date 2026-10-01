execute if data storage les_echos_du_monde:state {prologue_automation_paused:1b} run return 0
execute unless data storage les_echos_du_monde:state {platform_layout:"vegetation_20261001"} run return 0
data remove storage les_echos_du_monde:state platform_error
data remove storage les_echos_du_monde:state platform_error_tile
data remove storage les_echos_du_monde:state platform_error_reason
data remove storage les_echos_du_monde:state platform_tile_forced
data remove storage les_echos_du_monde:state platform_tile_loaded
data remove storage les_echos_du_monde:state platform_tile_owned
scoreboard players set #platform_wait edm_internal 0
scoreboard players set #platform_place edm_internal 0
scoreboard players set #platform_progress edm_internal 0
scoreboard players set #platform_total edm_internal 933
scoreboard players set #platform_ui_clock edm_internal 0
data modify storage les_echos_du_monde:state platform_building set value 1b
schedule function les_echos_du_monde:world/vegetation_chunks/chunk_0000 1t replace
