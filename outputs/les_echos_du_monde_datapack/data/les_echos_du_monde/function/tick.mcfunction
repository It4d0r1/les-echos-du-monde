execute if data storage les_echos_du_monde:state {platform_requires_new_world:1b} as @a[tag=!edm_prologue_update_notice] run function les_echos_du_monde:player/report_existing_world
function les_echos_du_monde:world/segments_v17/tick
function les_echos_du_monde:world/leaves_v17/tick
execute if data storage les_echos_du_monde:state {platform_layout:"segments_v17"} unless data storage les_echos_du_monde:state {prologue_automation_paused:1b} if score #enabled edm_seg_ctl matches 1 unless data storage les_echos_du_monde:segments_v17 {spawn_ready:1b} as @a[tag=!edm_prologue_done,tag=!edm_prologue_waiting] run function les_echos_du_monde:player/wait_prologue
execute if data storage les_echos_du_monde:state {platform_layout:"segments_v17"} unless data storage les_echos_du_monde:state {prologue_automation_paused:1b} if score #enabled edm_seg_ctl matches 1 if data storage les_echos_du_monde:segments_v17 {spawn_ready:1b} as @a[tag=!edm_prologue_done] at @s run function les_echos_du_monde:player/first_join
scoreboard players add #platform_ui_clock edm_internal 1
execute if score #platform_ui_clock edm_internal matches 20.. if score #enabled edm_seg_ctl matches 1 run title @a[tag=edm_prologue_waiting] actionbar {"text":"Préparation du terrain de départ…","color":"gold"}
execute if score #platform_ui_clock edm_internal matches 20.. unless score #enabled edm_seg_ctl matches 1 run title @a[tag=edm_prologue_waiting] actionbar {"text":"La génération du prologue est en pause.","color":"gray"}
execute if score #platform_ui_clock edm_internal matches 20.. run scoreboard players set #platform_ui_clock edm_internal 0
function les_echos_du_monde:world/detect_exit
