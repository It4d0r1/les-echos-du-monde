scoreboard players set #placed edm_seg_ctl 0
execute store success score #placed edm_seg_ctl run place template les_echos_du_monde:platform_segments_v17/s_m03_p02 -96 -26 64
execute if score #placed edm_seg_ctl matches 1 run scoreboard players set s_m03_p02 edm_seg_done 1
execute if score #placed edm_seg_ctl matches 1 run scoreboard players set s_m03_p02 edm_seg_retry 0
execute if score #placed edm_seg_ctl matches 1 run scoreboard players add #completed edm_seg_ctl 1
execute unless score #placed edm_seg_ctl matches 1 run function les_echos_du_monde:world/segments_v17/segment/s_m03_p02/fail
execute if score #placed edm_seg_ctl matches 1 run function les_echos_du_monde:world/segments_v17/segment/s_m03_p02/cleanup
