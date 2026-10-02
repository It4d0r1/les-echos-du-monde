scoreboard players set #budget edm_seg_ctl 1
scoreboard players set #polled edm_seg_ctl 0
execute if score #active edm_seg_ctl matches 0.. run function les_echos_du_monde:world/segments_v17/maintenance
execute if score #active edm_seg_ctl matches 0.. run scoreboard players set #budget edm_seg_ctl 0
function les_echos_du_monde:world/segments_v17/ready_spawn
execute if score #budget edm_seg_ctl matches 1 unless data storage les_echos_du_monde:segments_v17 {spawn_ready:1b} if entity @a[tag=!edm_prologue_done] run function les_echos_du_monde:world/segments_v17/select_spawn
# Random player order spreads the generation slot between multiple explorers.
execute as @a[sort=random] at @s if dimension les_echos_du_monde:prologue run function les_echos_du_monde:world/segments_v17/player
execute if score #active edm_seg_ctl matches 0.. if score #budget edm_seg_ctl matches 0 run function les_echos_du_monde:world/segments_v17/maintenance
function les_echos_du_monde:world/segments_v17/ready_spawn
