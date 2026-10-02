scoreboard players set #ready edm_seg_ctl 1
execute unless score s_m01_m01 edm_seg_done matches 1 run scoreboard players set #ready edm_seg_ctl 0
execute unless score s_m01_p00 edm_seg_done matches 1 run scoreboard players set #ready edm_seg_ctl 0
execute unless score s_m01_p01 edm_seg_done matches 1 run scoreboard players set #ready edm_seg_ctl 0
execute unless score s_p00_m01 edm_seg_done matches 1 run scoreboard players set #ready edm_seg_ctl 0
execute unless score s_p00_p00 edm_seg_done matches 1 run scoreboard players set #ready edm_seg_ctl 0
execute unless score s_p00_p01 edm_seg_done matches 1 run scoreboard players set #ready edm_seg_ctl 0
execute unless score s_p01_m01 edm_seg_done matches 1 run scoreboard players set #ready edm_seg_ctl 0
execute unless score s_p01_p00 edm_seg_done matches 1 run scoreboard players set #ready edm_seg_ctl 0
execute unless score s_p01_p01 edm_seg_done matches 1 run scoreboard players set #ready edm_seg_ctl 0
execute if score #ready edm_seg_ctl matches 1 run data modify storage les_echos_du_monde:segments_v17 spawn_ready set value 1b
execute unless score #ready edm_seg_ctl matches 1 run data modify storage les_echos_du_monde:segments_v17 spawn_ready set value 0b
