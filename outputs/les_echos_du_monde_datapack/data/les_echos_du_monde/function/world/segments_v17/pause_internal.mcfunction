execute if score #active edm_seg_ctl matches 0.. run function les_echos_du_monde:world/segments_v17/cleanup_active
scoreboard players set #enabled edm_seg_ctl 0
data modify storage les_echos_du_monde:segments_v17 enabled set value 0b
