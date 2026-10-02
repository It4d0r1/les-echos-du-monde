# Objective creation may report 'already exists' on reload; persistent scores are kept.
scoreboard objectives add edm_seg_ctl dummy
scoreboard objectives add edm_seg_done dummy
scoreboard objectives add edm_seg_retry dummy
scoreboard objectives add edm_seg_tmp dummy
execute unless data storage les_echos_du_monde:segments_v17 runtime_initialized run function les_echos_du_monde:world/segments_v17/initialize
# Reclaim only tickets this runtime previously added; no remove all command.
function les_echos_du_monde:world/segments_v17/cleanup_active
scoreboard players set #active edm_seg_ctl -1
scoreboard players set #clock edm_seg_ctl 0
scoreboard players set #budget edm_seg_ctl 0
execute unless data storage les_echos_du_monde:state {platform_layout:"segments_v17"} run function les_echos_du_monde:world/segments_v17/lock_layout
execute if data storage les_echos_du_monde:state {platform_layout:"segments_v17"} run data remove storage les_echos_du_monde:segments_v17 locked_layout
execute if data storage les_echos_du_monde:state {prologue_automation_paused:1b} run scoreboard players set #enabled edm_seg_ctl 0
function les_echos_du_monde:world/segments_v17/ready_spawn
