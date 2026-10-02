execute unless data storage les_echos_du_monde:state {platform_layout:"segments_v17"} run return 0
execute if data storage les_echos_du_monde:state {prologue_automation_paused:1b} run return 0
execute unless score #enabled edm_seg_ctl matches 1 run return 0
execute unless data storage les_echos_du_monde:segments_v17 {spawn_ready:1b} run return 0
scoreboard players set #prologue_tp edm_internal 0
execute store success score #prologue_tp edm_internal run function les_echos_du_monde:player/teleport_to_prologue
execute if score #prologue_tp edm_internal matches 1 run tag @s add edm_prologue_done
execute if score #prologue_tp edm_internal matches 1 run tag @s remove edm_prologue_waiting
