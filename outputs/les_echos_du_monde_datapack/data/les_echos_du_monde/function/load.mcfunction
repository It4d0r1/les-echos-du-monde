# Scores persist across reloads. "Already exists" for an objective is harmless.
scoreboard objectives add edm_internal dummy
execute unless data storage les_echos_du_monde:state initialized run function les_echos_du_monde:world/initialize
function les_echos_du_monde:world/segments_v17/setup
function les_echos_du_monde:world/leaves_v17/setup
execute unless data storage les_echos_du_monde:state {platform_layout:"segments_v17"} run function les_echos_du_monde:world/guard_existing_prologue
scoreboard players set #platform_ui_clock edm_internal 0
