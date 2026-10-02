execute unless data storage les_echos_du_monde:state {platform_layout:"segments_v17"} if score #active edm_seg_ctl matches 0.. run function les_echos_du_monde:world/segments_v17/pause_internal
execute unless data storage les_echos_du_monde:state {platform_layout:"segments_v17"} run return 0
execute if data storage les_echos_du_monde:state {prologue_automation_paused:1b} run function les_echos_du_monde:world/segments_v17/pause_internal
execute unless score #enabled edm_seg_ctl matches 1 run return 0
scoreboard players add #clock edm_seg_ctl 1
execute unless score #clock edm_seg_ctl matches 2.. run return 0
scoreboard players set #clock edm_seg_ctl 0
function les_echos_du_monde:world/segments_v17/cycle
